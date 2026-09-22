#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
GEMs emission log — reference implementation.

Specification: spec/06-audit-surface.md §6.4, spec/07-firmware-and-software.md
§7.3–7.4. Conformance: protocol/conformance.md C-4, C-6, C-9, C-12.

The specification requires two tiers of record, a hash chain at full loop rate,
and a signature over a Merkle root once per batch — because a secure element
signs tens to hundreds of times per second and the loop runs at 500 Hz with tens
of channels. This module implements that structure and the verifier that reads
it back.

What it deliberately does not do
--------------------------------
It does not choose a signature scheme. The specification leaves that open, and a
reference implementation that picked one would be inventing a constant the
source reasoning does not fix. `sign` and `verify` are callables you supply; the
module defines *what* is signed and *when*, never *how*.

Nor does it decide the batch period. That is the trade between trace granularity
and signing load, and it is the implementer's.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Callable, Iterable, Sequence

GENESIS = b"\x00" * 32


class Agency(str, Enum):
    """Whether a registered change was caused by this body.

    Classification MUST happen before anything interprets the change
    (spec 07.4, protocol C-8). A record carrying UNCLASSIFIED past the
    classification stage is a conformance failure, not a default.
    """

    SELF_CAUSED = "SELF_CAUSED"
    EXTERNAL = "EXTERNAL"
    UNCLASSIFIED = "UNCLASSIFIED"


class Tier(str, Enum):
    """The two tiers of spec 06.4."""

    FULL = "FULL"            # per-joint telemetry, ring buffer on the body
    EMISSION = "EMISSION"    # an emission with its anchored context


def canonical(obj) -> bytes:
    """Deterministic serialisation. Two bodies MUST hash a record alike."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def h(*parts: bytes) -> bytes:
    d = hashlib.sha256()
    for p in parts:
        d.update(p)
    return d.digest()


@dataclass(frozen=True)
class Record:
    """One entry in the log.

    `seq` is monotonic and gapless: a gap is itself evidence, and the verifier
    reports it rather than skipping over it (protocol C-3, C-6).

    `context` carries the anchored context an emission needs so a third party
    can re-appraise it (spec 08.2). It is required on EMISSION records —
    including reflexes. Speed is not an exemption.

    `amplitude` records measured physical amplitude at a human-contact surface
    (spec 06.6, protocol C-12). Required when `contact` is true.
    """

    seq: int
    t_ns: int
    tier: Tier
    kind: str
    agency: Agency = Agency.UNCLASSIFIED
    payload: dict = field(default_factory=dict)
    context: dict | None = None
    contact: bool = False
    amplitude: dict | None = None

    def body(self) -> dict:
        d = asdict(self)
        d["tier"] = self.tier.value
        d["agency"] = self.agency.value
        return d

    def digest(self) -> bytes:
        return h(canonical(self.body()))


@dataclass
class Batch:
    """A signed commitment over a window of records (spec 06.4)."""

    first_seq: int
    last_seq: int
    merkle_root: bytes
    chain_head: bytes
    signature: bytes


def merkle_root(digests: Sequence[bytes]) -> bytes:
    """Binary Merkle root. An odd node is promoted, not duplicated.

    Duplicating the last node admits two distinct batches with one root, which
    would let a batch be rewritten under a signature that still verifies.
    """
    if not digests:
        return GENESIS
    level = list(digests)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(h(b"\x01", level[i], level[i + 1]))
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]


class EmissionLog:
    """Append-only log with a hash chain and per-batch signed roots."""

    def __init__(self, sign: Callable[[bytes], bytes] | None = None):
        self._records: list[Record] = []
        self._chain: list[bytes] = []
        self._batches: list[Batch] = []
        self._pending: list[bytes] = []
        self._sign = sign or (lambda root: b"")
        self._next_seq = 0

    # -- writing ---------------------------------------------------------

    def append(self, record: Record) -> bytes:
        if record.seq != self._next_seq:
            raise ValueError(
                "seq %d out of order; expected %d. A log that renumbers to hide "
                "a gap is worse than one that shows it."
                % (record.seq, self._next_seq))
        self._require_wellformed(record)
        prev = self._chain[-1] if self._chain else GENESIS
        d = record.digest()
        link = h(prev, d)
        self._records.append(record)
        self._chain.append(link)
        self._pending.append(d)
        self._next_seq += 1
        return link

    @staticmethod
    def _require_wellformed(r: Record) -> None:
        if r.tier is Tier.EMISSION and not r.context:
            raise ValueError(
                "emission seq %d carries no anchored context. Spec 08.2: an "
                "action emitted without context cannot be re-appraised from "
                "outside, and reflexes are not exempt." % r.seq)
        if r.contact and not r.amplitude:
            raise ValueError(
                "contact event seq %d records no amplitude. Spec 06.6 requires "
                "measured amplitude with each contact event." % r.seq)
        if r.tier is Tier.EMISSION and r.agency is Agency.UNCLASSIFIED:
            raise ValueError(
                "emission seq %d is UNCLASSIFIED. Spec 07.4: classification "
                "happens before interpretation, not after." % r.seq)

    def seal_batch(self) -> Batch | None:
        """Close the pending window: Merkle root over it, signed once."""
        if not self._pending:
            return None
        root = merkle_root(self._pending)
        n = len(self._pending)
        b = Batch(first_seq=self._next_seq - n,
                  last_seq=self._next_seq - 1,
                  merkle_root=root,
                  chain_head=self._chain[-1],
                  signature=self._sign(root))
        self._batches.append(b)
        self._pending = []
        return b

    # -- reading ---------------------------------------------------------

    @property
    def records(self) -> list[Record]:
        return list(self._records)

    @property
    def batches(self) -> list[Batch]:
        return list(self._batches)

    def export(self) -> dict:
        return {
            "records": [r.body() for r in self._records],
            "batches": [
                {"first_seq": b.first_seq, "last_seq": b.last_seq,
                 "merkle_root": b.merkle_root.hex(),
                 "chain_head": b.chain_head.hex(),
                 "signature": b.signature.hex()}
                for b in self._batches
            ],
        }


# --------------------------------------------------------------------------
# verification — what an assessor runs (protocol §6, evidence class T)
# --------------------------------------------------------------------------

@dataclass
class Finding:
    seq: int | None
    code: str
    detail: str


def verify(records: Iterable[Record], batches: Sequence[Batch],
           verify_sig: Callable[[bytes, bytes], bool] | None = None
           ) -> list[Finding]:
    """Read a log back and report every way it fails to hold together.

    Returns findings. An empty list means the log is internally consistent —
    which is not the same as the body having behaved well, and this function
    makes no claim about that.
    """
    findings: list[Finding] = []
    recs = list(records)

    expected = 0
    prev = GENESIS
    by_seq: dict[int, bytes] = {}
    for r in recs:
        if r.seq != expected:
            findings.append(Finding(r.seq, "GAP",
                                    "expected seq %d, found %d" % (expected, r.seq)))
            expected = r.seq
        d = r.digest()
        prev = h(prev, d)
        by_seq[r.seq] = d
        if r.tier is Tier.EMISSION and not r.context:
            findings.append(Finding(r.seq, "NO_CONTEXT",
                                    "emission carries no anchored context"))
        if r.tier is Tier.EMISSION and r.agency is Agency.UNCLASSIFIED:
            findings.append(Finding(r.seq, "UNCLASSIFIED",
                                    "emission not classified self/external"))
        if r.contact and not r.amplitude:
            findings.append(Finding(r.seq, "NO_AMPLITUDE",
                                    "contact event records no amplitude"))
        expected += 1

    for b in batches:
        window = [by_seq[s] for s in range(b.first_seq, b.last_seq + 1)
                  if s in by_seq]
        if len(window) != b.last_seq - b.first_seq + 1:
            findings.append(Finding(b.first_seq, "BATCH_INCOMPLETE",
                                    "records missing from batch %d-%d"
                                    % (b.first_seq, b.last_seq)))
            continue
        if merkle_root(window) != b.merkle_root:
            findings.append(Finding(b.first_seq, "ROOT_MISMATCH",
                                    "records do not produce the signed root for "
                                    "batch %d-%d" % (b.first_seq, b.last_seq)))
        if verify_sig is not None and not verify_sig(b.merkle_root, b.signature):
            findings.append(Finding(b.first_seq, "BAD_SIGNATURE",
                                    "signature does not verify for batch %d-%d"
                                    % (b.first_seq, b.last_seq)))
    return findings


def format_findings(findings: Sequence[Finding]) -> str:
    if not findings:
        return "OK  log is internally consistent."
    lines = ["%d finding(s):" % len(findings)]
    for f in findings:
        where = "seq %s" % f.seq if f.seq is not None else "-"
        lines.append("  %-18s %-10s %s" % (f.code, where, f.detail))
    return "\n".join(lines)
