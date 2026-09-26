#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Check the timing table against the specification and the firmware architecture.

    python realtime/check_timing.py

tasks.csv is the one place each task's layer, rate, deadline, stage budget and
deadline class are written. This check holds it to three things:

  1. The rule of spec 07.1: every DEADLINE_HARD task is FIRMWARE.
  2. Arithmetic: a periodic task's deadline is its period, and the stage budgets
     of a pipeline add up to its deadline, margin included.
  3. Agreement: the rates and classes in spec 07.2 and the stage budgets in
     firmware/ARCHITECTURE.md §2 and §3 are the ones in the table.

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
LAYERS = {"FIRMWARE", "SOFTWARE"}
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
            errs.append("%s: layer must be FIRMWARE or SOFTWARE" % w)
        if t["deadline_class"] == "DEADLINE_HARD" and t["layer"] != "FIRMWARE":
            errs.append("%s: DEADLINE_HARD but not FIRMWARE (spec 07.1)" % w)
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
    hard = sum(t["deadline_class"] == "DEADLINE_HARD" for t in tasks)
    print("OK  %d tasks, %d DEADLINE_HARD, all FIRMWARE; stage budgets and spec 07.2 agree."
          % (len(tasks), hard))
    return 0


if __name__ == "__main__":
    sys.exit(main())
