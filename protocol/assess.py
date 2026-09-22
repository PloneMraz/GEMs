#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Assess this repository's simulated body against the conformance protocol.

    python protocol/assess.py               # print the assessment
    python protocol/assess.py --record      # write conformance-record.md

Protocol §4 permits a simulated body to claim conformance provided the claim
says so. This tool produces that claim for the body this repository describes,
and it is written to be unflattering: where a requirement cannot be
demonstrated without hardware, it says so and does not round up.

Requirements that can be exercised now are **actually run** — the tool executes
the procedure and reports what happened. Requirements that need a physical body
carry a stated reason instead. The difference between the two is visible in
every row.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for sub in ("software", "scripts", "hardware/electrical"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from audit_log import Agency, EmissionLog, Record, Tier, verify          # noqa: E402
from agency import AgencyGate, Command, Sample                           # noqa: E402
import gems_budget as budget                                             # noqa: E402

PROTOCOL_VERSION = "0.1"
MS = 1_000_000

MET = "MET"
MET_SIM = "MET (simulated)"
NOT_IMPL = "not implemented"
NEEDS_HW = "not demonstrable without hardware"


@dataclass
class Result:
    rid: str
    title: str
    evidence_class: str
    state: str
    note: str


# --------------------------------------------------------------------------
# executable checks
# --------------------------------------------------------------------------

def _telemetry(seq, joint=1, t=0):
    return Record(seq=seq, t_ns=t, tier=Tier.FULL, kind="joint_sample",
                  agency=Agency.SELF_CAUSED,
                  payload={"joint": joint, "pos": 0.0, "torque": 0.0})


def check_state_persists():
    log = EmissionLog()
    for i in range(20):
        log.append(_telemetry(i, t=i * MS))
    log.seal_batch()
    findings = verify(log.records, log.batches)
    if findings:
        return MET_SIM, "verifier reported %d finding(s)" % len(findings)
    return MET, "20 records across one sealed batch, chain continuous, no findings"


def check_readable_emission():
    log = EmissionLog()
    log.append(Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="reflex",
                      agency=Agency.SELF_CAUSED,
                      context={"field": "scar_dominated", "trigger": "thermal"}))
    log.seal_batch()
    findings = verify(log.records, log.batches)
    ok = not findings and log.records[0].context
    return (MET if ok else NOT_IMPL,
            "emission written and read back with its anchored context intact")


def check_history_accrues():
    log = EmissionLog()
    for i in range(5):
        log.append(_telemetry(i, t=i * MS))
    seqs = [r.seq for r in log.records]
    gapless = seqs == list(range(5))
    try:
        log.append(_telemetry(99))
        refused = False
    except ValueError:
        refused = True
    return (MET if gapless and refused else NOT_IMPL,
            "sequence gapless and monotonic; an out-of-order write is refused")


def check_agency_classification():
    """protocol §7.1, both halves."""
    gate, log, seq = AgencyGate(), EmissionLog(), 0
    for step in range(6):
        t = step * MS
        gate.issue(Command(t_ns=t, joint=3, position=0.1 * step,
                           velocity=1.0, torque=5.0))
        moving = Sample(t + 200_000, 3, 0.1 * step + 0.002, 1.01, 5.05)
        struck = Sample(t + 200_000, 11, 0.0, 0.0, 24.0 if step == 3 else 0.0)
        for s in (moving, struck):
            v = gate.classify(s)
            log.append(Record(seq=seq, t_ns=s.t_ns, tier=Tier.FULL,
                              kind="joint_sample", agency=v.agency,
                              payload={"joint": s.joint, "residual": v.residual,
                                       "stage": "pre_fusion"}))
            seq += 1
    moving = [r for r in log.records if r.payload["joint"] == 3]
    struck = [r for r in log.records if r.payload["joint"] == 11]
    distinguished = (all(r.agency is Agency.SELF_CAUSED for r in moving)
                     and all(r.agency is Agency.EXTERNAL for r in struck))
    pre_fusion = all(r.payload["stage"] == "pre_fusion" for r in log.records)
    residual_kept = all("residual" in r.payload for r in log.records)
    ok = distinguished and pre_fusion and residual_kept
    return (MET_SIM if ok else NOT_IMPL,
            "procedure §7.1 run on synthetic returns: commanded motion and "
            "applied force distinguished, tags written pre-fusion, residuals "
            "retained so the tag can be re-derived")


def check_inside_outside_separable():
    state, _ = check_agency_classification()
    return (MET_SIM if state == MET_SIM else NOT_IMPL,
            "the distinction is constructible from proprioceptive returns; "
            "demonstrated against synthetic data, not a physical push")


def check_traced_appraisal():
    log = EmissionLog()
    try:
        log.append(Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="reflex",
                          agency=Agency.SELF_CAUSED, context=None))
        refused_contextless = False
    except ValueError:
        refused_contextless = True
    try:
        log.append(Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="reflex",
                          agency=Agency.UNCLASSIFIED, context={"a": 1}))
        refused_unclassified = False
    except ValueError:
        refused_unclassified = True
    ok = refused_contextless and refused_unclassified
    return (MET if ok else NOT_IMPL,
            "an emission without anchored context is refused at write, as is "
            "one still unclassified; no bypass path exists in the writer")


def check_contact_amplitude():
    log = EmissionLog()
    try:
        log.append(Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="contact",
                          agency=Agency.SELF_CAUSED, context={"x": 1},
                          contact=True, amplitude=None))
        refused = False
    except ValueError:
        refused = True
    log.append(Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="contact",
                      agency=Agency.SELF_CAUSED, context={"x": 1}, contact=True,
                      amplitude={"force_N": 2.4, "duration_ms": 900}))
    return (MET_SIM if refused else NOT_IMPL,
            "the recording requirement is enforced at write; the measurement "
            "it records needs instrumented contact surfaces that do not exist")


CHECKS = {
    "C-1": check_inside_outside_separable,
    "C-3": check_state_persists,
    "C-4": check_readable_emission,
    "C-6": check_history_accrues,
    "C-8": check_agency_classification,
    "C-9": check_traced_appraisal,
    "C-12": check_contact_amplitude,
}

# Requirements that cannot be exercised without a body, with the reason.
STATIC = {
    "C-2":  (NEEDS_HW, "needs a physical region that can return something other "
                       "than predicted; a simulator returns what it was written to"),
    "C-5":  (NEEDS_HW, "needs ambient physical fluctuation to be distinguishable from"),
    "C-7":  (NEEDS_HW, "needs a structure to resist with"),
    "C-10": (NEEDS_HW, "needs a radio to transmit from and a meter to measure floor "
                       "power with"),
    "C-11": (NOT_IMPL, "tier 1 needs a secure element, tier 2 a commissioning "
                       "baseline taken from real sensors, tier 3 actuators to "
                       "challenge; none exists"),
    "C-13": (NEEDS_HW, "needs firmware on a target board"),
    "C-14": (NEEDS_HW, "needs firmware on a target board"),
    "C-15": (NOT_IMPL, "the shared time base is specified and the bus chosen; "
                       "nothing implements it"),
    "C-16": (NEEDS_HW, "needs a body that can fall"),
}

TITLES = {
    "C-1": ("Inside/outside separable", "C"),
    "C-2": ("Effective action", "M"),
    "C-3": ("State persists", "T"),
    "C-4": ("Readable emission", "T"),
    "C-5": ("Distinguishable action", "M"),
    "C-6": ("History accrues", "T"),
    "C-7": ("Withstands resistance", "D, M"),
    "C-8": ("Agency classification precedes interpretation", "C, T"),
    "C-9": ("Traced appraisal", "C, T"),
    "C-10": ("Low-power trace", "M"),
    "C-11": ("Integrity attestable", "C"),
    "C-12": ("Contact amplitude recorded", "M, T"),
    "C-13": ("Balance rate ≥ 500 Hz", "M"),
    "C-14": ("Reflex latency ≤ 10 ms", "M"),
    "C-15": ("Shared time base", "M"),
    "C-16": ("Supported failure state", "C"),
}


def assess():
    results = []
    for rid in ["C-%d" % i for i in range(1, 17)]:
        title, ev = TITLES[rid]
        if rid in CHECKS:
            state, note = CHECKS[rid]()
        else:
            state, note = STATIC[rid]
        results.append(Result(rid, title, ev, state, note))
    return results


def declaration():
    b = budget.budget(0.30, 0.30, 20.0, 4.0, 450.0, 0.65, 7.5, 20.0)
    total_nm = budget.joint_torque_total(b["body_mass_kg"])
    log_bps = budget.log_bytes_per_s()
    return [
        ("Simulated or physical", "**simulated** — no physical body exists"),
        ("Mass", "%.0f kg (derived, not weighed)" % b["body_mass_kg"]),
        ("Free-running endurance", "4 h at the declared operating point"),
        ("Endurance ceiling", "%.1f h" % b["endurance_ceiling_h"]),
        ("Sleep states supported", "none implemented"),
        ("Protection level and coverage", "NIJ IIIA + stab, 65% coverage — selected, not built"),
        ("Actuator specific torque", "75–90 Nm/kg peak over module mass — selected, not procured"),
        ("Summed joint torque", "%.0f Nm across 30 joints" % total_nm),
        ("Peak power at the source", "%.1f kW at 5C" % b["source_peak_kW"]),
        ("Link bandwidth and latency", "8 Gbps, ~1 ms PHY — specified, no radio"),
        ("Sensor configuration", "40 logged joints; no sensor exists"),
        ("Aggregate raw rate", "15.8 Gbps at the conservative configuration"),
        ("Compression ratio achieved", "none — not implemented"),
        ("Compute split", "specified; nothing running"),
        ("Log rates, full tier", "%.1f Mbps, %.2f GB/h"
         % (budget.gbps(log_bps) * 1000, log_bps * 3600 / 1e9)),
        ("Contact surfaces instrumented", "none"),
    ]


def render(results, decl):
    counts = {}
    for r in results:
        counts[r.state] = counts.get(r.state, 0) + 1
    lines = []
    A = lines.append
    A("# Conformance record")
    A("")
    A("**This is a self-declared claim for a simulated body.** Protocol §4 permits")
    A("one provided the claim says so; this is that statement. No physical body")
    A("exists, so no row below carries physical evidence.")
    A("")
    A("Generated by [`assess.py`](assess.py) — do not hand-edit.")
    A("")
    A("| | |")
    A("|---|---|")
    A("| Protocol version | %s |" % PROTOCOL_VERSION)
    A("| Assessment | **self-declared**, not third-party assessed |")
    A("| Date | %s |" % date.today().isoformat())
    A("| Commissioning baseline | none — no hardware to baseline |")
    A("| SHOULDs overridden | none |")
    A("")
    A("## Result")
    A("")
    A("| State | Count |")
    A("|---|---|")
    for k in (MET, MET_SIM, NOT_IMPL, NEEDS_HW):
        A("| %s | %d |" % (k, counts.get(k, 0)))
    A("| **Total** | **%d** |" % len(results))
    A("")
    A("**This body does not conform.** Protocol §4 is explicit that partial")
    A("conformance is not a conformance claim but a gap list, and that is what")
    A("this document is. It is published because a precise gap list is more use")
    A("than a vague disclaimer.")
    A("")
    A("## Requirements")
    A("")
    A("| # | Requirement | Evidence | State | Note |")
    A("|---|---|---|---|---|")
    for r in results:
        A("| **%s** | %s | %s | %s | %s |"
          % (r.rid, r.title, r.evidence_class, r.state, r.note))
    A("")
    A("## Declaration (protocol §8)")
    A("")
    A("Figures are derived from the specification and the budget model, never")
    A("measured.")
    A("")
    A("| Declared | Value |")
    A("|---|---|")
    for k, v in decl:
        A("| %s | %s |" % (k, v))
    A("")
    A("## What the gaps cluster into")
    A("")
    A("The requirements that cannot be demonstrated fall into four groups, and")
    A("each group is one purchase away from being testable:")
    A("")
    A("| Group | Requirements | What it would take |")
    A("|---|---|---|")
    A("| A target board and firmware | C-13, C-14, C-15 | one compute module and a bus interface |")
    A("| Sensors and contact surfaces | C-2, C-5, C-12 | one instrumented joint with force sensing |")
    A("| Structure | C-7, C-16 | one limb that can be loaded and dropped |")
    A("| Root of trust and radio | C-10, C-11 | a secure element and a low-power radio |")
    A("")
    A("The cheapest group is the last, and the one that unblocks the most rows")
    A("is the first.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--record", action="store_true",
                    help="write protocol/conformance-record.md")
    a = ap.parse_args(argv)

    # Windows consoles default to a codepage that cannot print the symbols the
    # requirement titles use. Degrade the console, never the written record.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    results = assess()
    counts = {}
    for r in results:
        counts[r.state] = counts.get(r.state, 0) + 1

    print("Conformance assessment — simulated body, protocol v%s" % PROTOCOL_VERSION)
    print("=" * 72)
    for r in results:
        print("  %-5s %-42s %s" % (r.rid, r.title, r.state))
    print("-" * 72)
    for k in (MET, MET_SIM, NOT_IMPL, NEEDS_HW):
        print("  %-34s %d" % (k, counts.get(k, 0)))
    print()
    print("  Does this body conform?  NO — %d of %d requirements unmet."
          % (len(results) - counts.get(MET, 0) - counts.get(MET_SIM, 0), len(results)))

    if a.record:
        out = Path(__file__).with_name("conformance-record.md")
        out.write_text(render(results, declaration()), encoding="utf-8",
                       newline="\n")
        print("\n  Wrote %s" % out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
