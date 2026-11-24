#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Room for the battery pack: how many catalogue pouch cells fit in each part of
the trunk, around the joint modules of layout.csv (plan M-2, D-5).

    python3 hardware/mechanical/modules/pack_fit.py        # needs numpy; a few minutes

Cells are boxes at their largest printed tolerance with 0.5 mm between faces, laid
by a greedy lattice in free space 2 mm fine. Nothing is kept for walls, terminals,
cooling, compression, a crush zone or a vent, so a real pack holds less; the fill
is not optimal either, so a better lattice holds somewhat more. 4 mm is kept
from every module, 10 from hip pitch, which turns, and 18 from the trunk's own,
which turn against the segment.
"""

import itertools
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import generate_modules as g  # noqa: E402

S = 2.0
# Amprius product catalogue, Q4 2026: length, width, thickness at 30% charge
# with their tolerances, mm; Wh typical; g
CELLS = {"SA147 (preliminary)": (58.0, 51.0, 5.9 + 0.5, 15.0, 33.6),
         "SA03": (139.6, 54.0, 6.57 + 0.5, 40.26, 102.0)}
ZONES = [  # name, x from, x to, half width, z from, z to, mm in the URDF frame
    ("upper torso, back to -100", -100, 40, 124, 240, 424),
    ("upper torso, back to -125", -125, 40, 124, 240, 424),
    ("upper torso, back to -150", -150, 40, 124, 240, 424),
    ("upper torso, back to -180", -180, 40, 124, 240, 424),
    ("lower thoracic, back to -125", -125, 100, 155, 125, 205),
    ("lumbar, back to -125", -125, 100, 155, 15, 95),
    ("pelvis, back to -125", -125, 85, 135, -145, -8),
]


def free(x0, x1, yh, z0, z1, rows):
    X, Y, Z = (np.arange(a + S / 2, b, S) for a, b in ((x0, x1), (-yh, yh), (z0, z1)))
    p = np.stack(np.meshgrid(X, Y, Z, indexing="ij"), -1)
    ok = np.ones(p.shape[:3], bool)
    for m in rows:
        n = m["name"]
        if any(k in n for k in ("knee", "ankle", "wrist", "elbow")):
            continue
        c, d, r, h = g.cyl(m)
        e = 18.0 if n.startswith("trunk") else 10.0 if n.endswith("hip_pitch") else 4.0
        w = p - np.array(c)
        t = (w * np.array(d)).sum(-1)
        rad = np.sqrt(np.maximum(0, (w ** 2).sum(-1) - t * t))
        ok &= ~((np.abs(t) < h / 2 + e) & (rad < r + e))
    return ok


def fill(ok, dims):
    best = 0
    orient = sorted(set(itertools.permutations(dims)))
    for order in itertools.product(orient, repeat=2):
        o, n = ok.copy(), 0
        for dm in order:
            k = [int(np.ceil(v / S)) for v in dm]
            for x in range(o.shape[0] - k[0] + 1):
                col = o[x:x + k[0]].all(0)
                for y in range(o.shape[1] - k[1] + 1):
                    strip = col[y:y + k[1]].all(0)
                    z = 0
                    while z + k[2] <= o.shape[2]:
                        if strip[z:z + k[2]].all():
                            o[x:x + k[0], y:y + k[1], z:z + k[2]] = False
                            col[y:y + k[1], z:z + k[2]] = False
                            strip[z:z + k[2]] = False
                            n += 1
                            z += k[2]
                        else:
                            z += 1
        best = max(best, n)
    return best


def main():
    rows = g.place()[2]
    for name, x0, x1, yh, z0, z1 in ZONES:
        ok = free(x0, x1, yh, z0, z1, rows)
        cells = []
        for c, (a, b, t, wh, gm) in CELLS.items():
            n = fill(ok, (a, b, t))
            cells.append("%s: %d cells, %.2f kWh" % (c, n, n * wh / 1000))
        print("%-30s free %.1f L   %s" % (name, ok.sum() * S ** 3 / 1e6, "; ".join(cells)), flush=True)


if __name__ == "__main__":
    main()
