#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Body differentiation, reference implementation — did this body cause that
change, did one of its declared faculties, or did something else?

This is the specification the firmware port (plan F-7) is checked against. The
runtime tag is written by firmware at acquisition; this module is the golden
model it is checked against, and lives in reference/ because it runs on no
target at all.

Specification: spec/05-sensing.md §5.5, spec/07-firmware-and-software.md §7.3
(guarantee 7). Contract: RSIL §3.3 and layer R2; INV-6 (spec 08.1).
Binding: software/RSIL-in-GEMs.md.
Conformance: protocol/conformance.md C-1, C-8, with the test procedure at §7.1.

The mechanism is an efference copy. Every command the body carries out is held
briefly; when a sensor sample arrives, it is matched to the command that was in
flight for that joint, a model of the body's own execution gives what the
command alone should have produced, and the residual decides:

    within tolerance of the command                      BODY_CAUSED
    otherwise, and a declared faculty acted on the joint HOST_REACTED
    otherwise                                            ENV_PUSHED

A declared faculty is what the substrate does of itself — a drive's fault
reaction, safe torque off, a battery cut-off (RSIL §7.2). A reaction reported
under a faculty that was never declared explains nothing: it is kept in
`undeclared`, for the record, and the change it would have explained stays
ENV_PUSHED (RSIL §7.3: only a declared faculty reacts; what else happens under
attack is damage).

THE MODEL IS NOT AN EXPECTATION
-------------------------------
The execution model says what this body's own command produces. It is fixed,
or loaded by the Main Controller; it is never learned here. It does not predict
what the region will return — that is the Main Controller's expectation, cast
with the command (DIL §6.1) — and the residual is not a prediction error: it
is a datum the body returns with the tag (RSIL §6, R2).

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
It does not decide what an external contact meant, or what to do about it,
and it does not decide whose act a change was for the self: the Main
Controller tags that beside this tag (RSIL §3.3). It writes a tag and passes
the sample on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from audit_log import Agency

# Matching window between a command (or a reaction) and the return it
# explains. The specification leaves this open (spec 07.7; RSIL DECIDE@IMPL-R2);
# it is bounded above by the reflex budget, since a window approaching 10 ms
# has already broken the reflex path.
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
class Reaction:
    """A faculty of the body acting of itself, as the body reports it.

    `joints` names the joints it acted on; None means the whole body (a safe
    torque off, a battery disconnect).
    """

    t_ns: int
    faculty: str
    joints: frozenset | None = None

    def covers(self, joint: int) -> bool:
        return self.joints is None or joint in self.joints


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
    """Gives the return a command alone should produce: a model of the body's
    own execution, not an expectation of the region.

    Deliberately trivial: the commanded state *is* the prediction. A real body
    needs joint dynamics here, and replacing this class is how that arrives —
    the gate does not care how the prediction is made, only that there is one.
    """

    def predict(self, cmd: Command, at_t_ns: int) -> Sample:
        return Sample(t_ns=at_t_ns, joint=cmd.joint, position=cmd.position,
                      velocity=cmd.velocity, torque=cmd.torque)


class UnclassifiableSample(Exception):
    """Raised when a sample cannot be classified at all.

    This is an error and not an UNDECIDED tag. A sample with no usable time
    base cannot be matched to a command, and a pipeline that quietly tags it
    UNDECIDED and carries on has defeated INV-6 while appearing to satisfy
    it — the tag is present and means nothing.
    """


class AgencyGate:
    """Holds recent commands and reactions, and classifies returns against them."""

    def __init__(self, model: ForwardModel | None = None,
                 tolerance: Tolerance | None = None,
                 window_ns: int = DEFAULT_WINDOW_NS,
                 declared_faculties: Iterable[str] = ()):
        self.model = model or ForwardModel()
        self.tol = tolerance or Tolerance()
        self.window_ns = window_ns
        self.declared = frozenset(declared_faculties)
        self.undeclared: list[Reaction] = []
        self._inflight: dict[int, list[Command]] = {}
        self._reactions: list[Reaction] = []

    def issue(self, cmd: Command) -> None:
        self._inflight.setdefault(cmd.joint, []).append(cmd)

    def react(self, reaction: Reaction) -> bool:
        """Take in a faculty's report. Returns whether the faculty is declared.

        An undeclared faculty is kept for the record and explains nothing.
        """
        if reaction.faculty not in self.declared:
            self.undeclared.append(reaction)
            return False
        self._reactions.append(reaction)
        return True

    def _match(self, s: Sample) -> Command | None:
        cmds = self._inflight.get(s.joint)
        if not cmds:
            return None
        # keep only commands still inside the window, newest first
        live = [c for c in cmds if 0 <= s.t_ns - c.t_ns <= self.window_ns]
        self._inflight[s.joint] = [c for c in cmds if s.t_ns - c.t_ns <= self.window_ns]
        return max(live, key=lambda c: c.t_ns) if live else None

    def _reaction(self, s: Sample) -> Reaction | None:
        live = [r for r in self._reactions
                if r.covers(s.joint) and 0 <= s.t_ns - r.t_ns <= self.window_ns]
        return max(live, key=lambda r: r.t_ns) if live else None

    def _unexplained(self, s: Sample, res: dict, why: str) -> Verdict:
        r = self._reaction(s)
        if r is not None:
            return Verdict(s, Agency.HOST_REACTED, res,
                           "%s; the declared faculty %r acted on this joint"
                           % (why, r.faculty))
        return Verdict(s, Agency.ENV_PUSHED, res, why)

    def classify(self, s: Sample) -> Verdict:
        if s.t_ns is None or s.t_ns < 0:
            raise UnclassifiableSample(
                "sample for joint %d carries no usable timestamp; without the "
                "shared time base of spec 07.2 it cannot be matched to a "
                "command (protocol C-15)" % s.joint)

        cmd = self._match(s)
        if cmd is None:
            return self._unexplained(
                s, {"position": abs(s.position), "velocity": abs(s.velocity),
                    "torque": abs(s.torque)},
                "no command in flight for this joint within %d ns; "
                "nothing this body did accounts for the return" % self.window_ns)

        pred = self.model.predict(cmd, s.t_ns)
        res = {
            "position": abs(s.position - pred.position),
            "velocity": abs(s.velocity - pred.velocity),
            "torque": abs(s.torque - pred.torque),
        }
        over = [k for k in res
                if res[k] > getattr(self.tol, k)]
        if over:
            return self._unexplained(
                s, res, "residual exceeds tolerance on " + ", ".join(sorted(over)))
        return Verdict(s, Agency.BODY_CAUSED, res,
                       "return is within tolerance of the commanded state")

    def classify_stream(self, samples: Iterable[Sample]) -> list[Verdict]:
        return [self.classify(s) for s in samples]


def summarise(verdicts: list[Verdict]) -> dict:
    out = {"total": len(verdicts), "body_caused": 0, "env_pushed": 0,
           "host_reacted": 0}
    for v in verdicts:
        out[v.agency.value.lower()] += 1
    return out
