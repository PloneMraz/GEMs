#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Check the real-time configuration against the specification and the
firmware architecture.

    python realtime_config/check_timing.py

Two files, two tiers. tasks.csv is the requirement: each task's layer, rate,
deadline, stage budget and deadline class. scheduler.csv is how it is met: the
platform, scheduling policy and priority, and how the worst-case latency is
bounded. The check holds them to four things:

  1. The rule of spec 07.1: every DEADLINE_HARD task runs on a platform whose
     worst-case latency is bounded — by construction on a microcontroller, or by
     measurement, recorded as evidence, under a real-time Linux policy.
  2. The layer and the platform agree: firmware runs on a microcontroller,
     software under Linux.
  3. Arithmetic: a periodic task's deadline is its period, a pipeline's stage
     budgets add up to its deadline, and SCHED_DEADLINE parameters satisfy
     runtime <= deadline <= period.
  4. Agreement: the rates and classes in spec 07.2 and the stage budgets in
     firmware/ARCHITECTURE.md §2 and §3 are the ones in tasks.csv.

Deadline classes are named DEADLINE_HARD / _FIRM / _SOFT / _NONE rather than
hard/firm/soft, so that a timing class cannot be misread as a layer — firmware,
software, hardware — in code or in data.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLASSES = {"DEADLINE_HARD", "DEADLINE_FIRM", "DEADLINE_SOFT", "DEADLINE_NONE"}
LAYERS = {"FIRMWARE", "SOFTWARE", "IMPL"}          # IMPL: decided by D-3
PLATFORMS = {"MCU_BARE_METAL", "MCU_RTOS", "LINUX_RT", "LINUX", "IMPL"}
POLICIES = {"ISR", "RTOS_FIXED_PRIORITY", "SCHED_FIFO", "SCHED_DEADLINE",
            "SCHED_OTHER", "IMPL"}
BASES = {"CONSTRUCTION", "MEASUREMENT", "NONE", "IMPL"}
FIRMWARE_PLATFORMS = {"MCU_BARE_METAL", "MCU_RTOS", "IMPL"}
SOFTWARE_PLATFORMS = {"LINUX_RT", "LINUX", "IMPL"}
EPS = 1e-9


def num(s):
    return float(s) if s else None


def md_rows(text, heading):
    """Rows of the first table after a heading, as lists of cell strings."""
    i = text.index(heading)
    rows = []
    for line in text[i:].splitlines()[1:]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not set(cells[0]) <= set("-: "):
                rows.append(cells)
        elif rows:
            break
    return rows[1:]                      # drop the header row


def main():
    errs = []
    with open(HERE / "tasks.csv", newline="", encoding="utf-8") as f:
        tasks = list(csv.DictReader(f))
    by_id = {t["task"]: t for t in tasks}
    stages = defaultdict(list)

    for t in tasks:
        w = t["task"]
        if t["deadline_class"] not in CLASSES:
            errs.append("%s: deadline_class must be one of %s" % (w, sorted(CLASSES)))
        if t["layer"] not in LAYERS:
            errs.append("%s: layer must be one of %s" % (w, sorted(LAYERS)))
        rate, dl = num(t["rate_hz"]), num(t["deadline_ms"])
        if rate and dl and abs(dl - 1000.0 / rate) > EPS:
            errs.append("%s: deadline %.3g ms is not the period of %g Hz" % (w, dl, rate))
        if t["parent"]:
            if t["parent"] not in by_id:
                errs.append("%s: unknown parent %s" % (w, t["parent"]))
            stages[t["parent"]].append(t)

    for parent, st in stages.items():
        total = sum(num(s["budget_ms"]) or 0.0 for s in st)
        dl = num(by_id[parent]["deadline_ms"])
        if dl is None or abs(total - dl) > EPS:
            errs.append("%s: stages add to %.2f ms, deadline is %s ms" % (parent, total, dl))

    # scheduler.csv: platform, policy, bound
    with open(HERE / "scheduler.csv", newline="", encoding="utf-8") as f:
        sched = {r["task"]: r for r in csv.DictReader(f)}
    top = {t["task"] for t in tasks if not t["parent"]}
    for tid in sorted(top - set(sched)):
        errs.append("scheduler.csv: no row for task %s" % tid)
    for tid in sorted(set(sched) - top):
        errs.append("scheduler.csv: %s is not a top-level task in tasks.csv" % tid)
    pending = []
    for tid, r in sched.items():
        if tid not in by_id:
            continue
        t, w = by_id[tid], "scheduler %s" % tid
        plat, pol, basis = r["platform"], r["sched_policy"], r["bound_basis"]
        if plat not in PLATFORMS or pol not in POLICIES or basis not in BASES:
            errs.append("%s: unknown platform, policy or bound_basis" % w)
            continue
        if t["layer"] == "FIRMWARE" and plat not in FIRMWARE_PLATFORMS:
            errs.append("%s: FIRMWARE task on %s" % (w, plat))
        if t["layer"] == "SOFTWARE" and plat not in SOFTWARE_PLATFORMS:
            errs.append("%s: SOFTWARE task on %s" % (w, plat))
        if pol in ("SCHED_FIFO", "SCHED_DEADLINE", "SCHED_OTHER") and plat not in ("LINUX", "LINUX_RT"):
            errs.append("%s: %s is a Linux policy, platform is %s" % (w, pol, plat))
        if pol in ("ISR", "RTOS_FIXED_PRIORITY") and not plat.startswith("MCU"):
            errs.append("%s: %s is a microcontroller policy, platform is %s" % (w, pol, plat))
        if pol == "SCHED_DEADLINE":
            try:
                rt, dl, pe = (int(r[k]) for k in ("runtime_us", "deadline_us", "period_us"))
                if not 0 < rt <= dl <= pe:
                    errs.append("%s: SCHED_DEADLINE needs runtime <= deadline <= period" % w)
            except ValueError:
                errs.append("%s: SCHED_DEADLINE needs integer runtime, deadline, period" % w)
        if t["deadline_class"] == "DEADLINE_HARD":
            if plat == "LINUX":
                errs.append("%s: DEADLINE_HARD on Linux without a real-time kernel (spec 07.1)" % w)
            elif plat == "LINUX_RT" and (pol not in ("SCHED_FIFO", "SCHED_DEADLINE")
                                         or basis != "MEASUREMENT" or not r["evidence"]):
                errs.append("%s: DEADLINE_HARD on LINUX_RT needs SCHED_FIFO or SCHED_DEADLINE, "
                            "bound_basis MEASUREMENT and evidence (spec 07.1)" % w)
            elif plat.startswith("MCU") and basis != "CONSTRUCTION":
                errs.append("%s: DEADLINE_HARD on a microcontroller is bounded by CONSTRUCTION" % w)
            elif basis == "NONE":
                errs.append("%s: DEADLINE_HARD with no latency bound" % w)
            if plat == "IMPL" or basis == "IMPL":
                pending.append(tid)

    # spec 07.2
    spec = (ROOT / "spec" / "07-firmware-and-software.md").read_text(encoding="utf-8")
    want = {"Proprioceptive sampling": ("1 kHz", "proprio_sampling"),
            "Balance": ("500 Hz", "balance"),
            "Reflex, end to end": ("10 ms", "reflex"),
            "Joint current control": (None, "current_loop")}
    for loop, rate, cls, *_ in md_rows(spec, "## 7.2 Real-time requirements"):
        if loop not in want:
            errs.append("spec 07.2: loop %r is not in tasks.csv" % loop)
            continue
        figure, tid = want.pop(loop)
        if figure and figure not in rate:
            errs.append("spec 07.2: %s rate %r does not state %s" % (loop, rate, figure))
        if "DEADLINE_" + cls.upper() != by_id[tid]["deadline_class"]:
            errs.append("spec 07.2: %s is %s, tasks.csv says %s" % (loop, cls, by_id[tid]["deadline_class"]))
    for loop in want:
        errs.append("spec 07.2: row %r missing" % loop)

    # firmware/ARCHITECTURE.md §2, §3
    arch = (ROOT / "firmware" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    for heading, parent in (("## 2. The reflex budget", "reflex"), ("## 3. The balance loop", "balance")):
        doc = {}
        for row in md_rows(arch, heading):
            name = row[0].strip("*")
            m = re.search(r"([\d.]+)\s*ms", row[1])
            if m and name != "Total":
                doc[name] = float(m.group(1))
        table = {s["name"]: num(s["budget_ms"]) for s in stages[parent]}
        if doc != table:
            errs.append("firmware/ARCHITECTURE %s differs from tasks.csv: %s vs %s"
                        % (heading[3:], doc, table))

    for e in errs:
        print("ERROR " + e)
    if errs:
        return 1
    hard = sum(t["deadline_class"] == "DEADLINE_HARD" and not t["parent"] for t in tasks)
    print("OK  %d tasks and stages; %d top-level DEADLINE_HARD tasks, none on an unbounded "
          "platform; stage budgets and spec 07.2 agree." % (len(tasks), hard))
    if pending:
        print("    Bound not yet established — platform or basis IMPL: %s" % ", ".join(sorted(pending)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
