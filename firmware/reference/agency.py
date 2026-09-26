#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Agency tagging, reference implementation — did this body cause that change,
or did something else?

This is the specification the firmware port (plan F-7) is checked against. The
runtime tag is written by firmware at acquisition; this module is the golden
model, which is why it lives under firmware/ although it is Python.

Specification: spec/05-sensing.md §5.5, spec/07-firmware-and-software.md §7.3
(guarantee 7). Contract: RSIL INV-6 (spec 08.1).
Conformance: protocol/conformance.md C-1, C-8, with the test procedure at §7.1.

The mechanism is an efference copy. Every command the body issues is held
briefly; when a sensor sample arrives, it is matched to the command that was in
flight for that joint, a forward model predicts what the command alone should
have produced, and the residual decides. Motion or force the command does not
account for came from somewhere else.

WHY THIS RUNS EARLY
-------------------
The classification must happen before anything interprets the sample — before
fusion, before compression. This is not a matter of tidiness. The evidence that
separates "I moved" from "something moved me" is the residual between one
command and one channel's return, and fusion averages exactly that away. A
pipeline that classifies afterwards produces a log that looks right and cannot
be checked, which is the failure protocol §7.1 tests for by reading *where* in
the pipeline the tag was written, not whether a tag is present.

WHAT IT DOES NOT DO
-------------------
It does not decide what the external contact meant, or what to do about it.
It writes a tag and passes the sample on.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# The agency tag is a record type shared with software (plan S-0).
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "software"))
from audit_log import Agency  # noqa: E402

# Matching window between a command and the return it explains. The
# specification leaves this open (spec 07.7); it is bounded above by the reflex
# budget, since a window approaching 10 ms has already broken the reflex path.
DEFAULT_WINDOW_NS = 2_000_000          # 2 ms


@dataclass(frozen=True)
class Command:
    """One actuator command, timestamped on the shared time base."""

    t_ns: int
    joint: int
    position: float          # rad
    velocity: float          # rad/s
    torque: float            # Nm, feed-forward


@dataclass(frozen=True)
class Sample:
    """One proprioceptive return, timestamped on the same base."""

    t_ns: int
    joint: int
    position: float
    velocity: float
    torque: float


@dataclass(frozen=True)
class Tolerance:
    """Residual beyond which a return is not explained by the command.

    These are `⟦IMPL⟧`: they depend on encoder resolution, actuator backlash
    and joint friction, none of which are fixed until parts are chosen. The
    values here are placeholders for testing the mechanism, not a declaration.
    """

    position: float = 0.010          # rad
    velocity: float = 0.100          # rad/s
    torque: float = 2.000            # Nm


@dataclass
class Verdict:
    sample: Sample
    agency: Agency
    residual: dict
    reason: str

    def dominant(self) -> str:
        return max(self.residual, key=lambda k: self.residual[k])


class ForwardModel:
    """Predicts the return a command alone should produce.

    Deliberately trivial: the commanded state *is* the prediction. A real body
    needs joint dynamics here, and replacing this class is how that arrives —
    the gate does not care how the prediction is made, only that there is one.
    """

    def predict(self, cmd: Command, at_t_ns: int) -> Sample:
        return Sample(t_ns=at_t_ns, joint=cmd.joint, position=cmd.position,
                      velocity=cmd.velocity, torque=cmd.torque)


class UnclassifiableSample(Exception):
    """Raised when a sample cannot be classified at all.

    This is an error and not an UNCLASSIFIED tag. A sample with no usable time
    base cannot be matched to a command, and a pipeline that quietly tags it
    UNCLASSIFIED and carries on has defeated INV-6 while appearing to satisfy
    it — the tag is present and means nothing.
    """


class AgencyGate:
    """Holds recent commands and classifies returns against them."""

    def __init__(self, model: ForwardModel | None = None,
                 tolerance: Tolerance | None = None,
                 window_ns: int = DEFAULT_WINDOW_NS):
        self.model = model or ForwardModel()
        self.tol = tolerance or Tolerance()
        self.window_ns = window_ns
        self._inflight: dict[int, list[Command]] = {}

    def issue(self, cmd: Command) -> None:
        self._inflight.setdefault(cmd.joint, []).append(cmd)

    def _match(self, s: Sample) -> Command | None:
        cmds = self._inflight.get(s.joint)
        if not cmds:
            return None
        # keep only commands still inside the window, newest first
        live = [c for c in cmds if 0 <= s.t_ns - c.t_ns <= self.window_ns]
        self._inflight[s.joint] = [c for c in cmds if s.t_ns - c.t_ns <= self.window_ns]
        return max(live, key=lambda c: c.t_ns) if live else None

    def classify(self, s: Sample) -> Verdict:
        if s.t_ns is None or s.t_ns < 0:
            raise UnclassifiableSample(
                "sample for joint %d carries no usable timestamp; without the "
                "shared time base of spec 07.2 it cannot be matched to a "
                "command (protocol C-15)" % s.joint)

        cmd = self._match(s)
        if cmd is None:
            return Verdict(
                sample=s, agency=Agency.EXTERNAL,
                residual={"position": abs(s.position), "velocity": abs(s.velocity),
                          "torque": abs(s.torque)},
                reason="no command in flight for this joint within %d ns; "
                       "nothing this body did accounts for the return"
                       % self.window_ns)

        pred = self.model.predict(cmd, s.t_ns)
        res = {
            "position": abs(s.position - pred.position),
            "velocity": abs(s.velocity - pred.velocity),
            "torque": abs(s.torque - pred.torque),
        }
        over = [k for k in res
                if res[k] > getattr(self.tol, k)]
        if over:
            return Verdict(s, Agency.EXTERNAL, res,
                           "residual exceeds tolerance on " + ", ".join(sorted(over)))
        return Verdict(s, Agency.SELF_CAUSED, res,
                       "return is within tolerance of the commanded state")

    def classify_stream(self, samples: Iterable[Sample]) -> list[Verdict]:
        return [self.classify(s) for s in samples]


def summarise(verdicts: list[Verdict]) -> dict:
    out = {"total": len(verdicts), "self_caused": 0, "external": 0}
    for v in verdicts:
        out["self_caused" if v.agency is Agency.SELF_CAUSED else "external"] += 1
    return out
