#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Check bom.csv and summarise what is and is not yet sourced and priced.

    python hardware/bom/check_bom.py

A row may leave its source and price empty — that is how an unverified item is
recorded. What a row may not do is carry half a claim: a price without the page
and date it was read from, or a part number without a manufacturer and source.
Those are refused, because a number nobody can trace is worse than a blank.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = ["id", "subsystem", "item", "spec_ref", "requirement", "qty",
          "qty_basis", "maturity", "level", "selection", "manufacturer",
          "part_number", "source_url", "unit_price", "currency", "price_date",
          "price_url", "notes"]
MATURITY = {"TM", "LAB"}
LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5"}
ID_RE = re.compile(r"^[A-Z]{3}-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
QTY_RE = re.compile(r"^\d+(\.\d+)?( m2)?$")


def check(rows):
    errors = []
    seen = set()
    for n, row in enumerate(rows, start=2):
        rid = row["id"]
        where = "line %d (%s)" % (n, rid or "no id")
        if not ID_RE.match(rid):
            errors.append("%s: id must look like ABC-01" % where)
        if rid in seen:
            errors.append("%s: duplicate id" % where)
        seen.add(rid)
        for f in ("subsystem", "item", "spec_ref"):
            if not row[f]:
                errors.append("%s: %s is empty" % (where, f))
        if row["maturity"] not in MATURITY:
            errors.append("%s: maturity must be one of %s" % (where, sorted(MATURITY)))
        if row["level"] not in LEVELS:
            errors.append("%s: level must be L0-L5" % where)
        if row["qty"] and not QTY_RE.match(row["qty"]):
            errors.append("%s: qty must be a number, optionally in m2" % where)
        if row["qty"] == "" and not row["qty_basis"]:
            errors.append("%s: an empty qty needs a qty_basis saying why" % where)
        if row["part_number"] and not (row["manufacturer"] and row["source_url"]):
            errors.append("%s: a part number needs a manufacturer and a source_url" % where)
        if row["unit_price"]:
            try:
                float(row["unit_price"])
            except ValueError:
                errors.append("%s: unit_price must be a number" % where)
            for f in ("currency", "price_date", "price_url"):
                if not row[f]:
                    errors.append("%s: a price needs %s" % (where, f))
            if row["price_date"] and not DATE_RE.match(row["price_date"]):
                errors.append("%s: price_date must be YYYY-MM-DD" % where)
        elif row["currency"] or row["price_date"] or row["price_url"]:
            errors.append("%s: price fields filled without a unit_price" % where)
        if row["maturity"] == "LAB" and row["part_number"]:
            errors.append("%s: a LAB item has no part number to give" % where)
    return errors


def summary(rows):
    by_sub = defaultdict(Counter)
    totals = defaultdict(float)
    unpriced = 0
    for row in rows:
        c = by_sub[row["subsystem"]]
        c["rows"] += 1
        c["sourced"] += bool(row["source_url"])
        c["priced"] += bool(row["unit_price"])
        c["LAB"] += row["maturity"] == "LAB"
        if row["unit_price"] and row["qty"] and not row["qty"].endswith("m2"):
            totals[row["currency"]] += float(row["unit_price"]) * float(row["qty"])
        elif not row["unit_price"]:
            unpriced += 1

    print("%-12s %5s %8s %7s %5s" % ("subsystem", "rows", "sourced", "priced", "LAB"))
    print("-" * 42)
    grand = Counter()
    for sub, c in by_sub.items():
        print("%-12s %5d %8d %7d %5d" % (sub, c["rows"], c["sourced"], c["priced"], c["LAB"]))
        grand.update(c)
    print("-" * 42)
    print("%-12s %5d %8d %7d %5d" % ("total", grand["rows"], grand["sourced"],
                                     grand["priced"], grand["LAB"]))
    levels = Counter(r["level"] for r in rows)
    print("\nlevels: " + "  ".join("%s %d" % (l, levels[l]) for l in sorted(LEVELS) if levels[l]))
    if totals:
        print("priced subtotal: " + ", ".join("%s %.2f" % (k, v) for k, v in totals.items()))
    print("rows without a price: %d — the total is not a cost estimate until this is 0"
          % unpriced)


def main():
    path = Path(__file__).with_name("bom.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            print("header does not match the declared columns:\n  %s" % ",".join(FIELDS))
            return 1
        rows = list(reader)
    errors = check(rows)
    for e in errors:
        print("ERROR " + e)
    if errors:
        return 1
    summary(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
