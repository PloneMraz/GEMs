#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Room for the battery pack: how many catalogue pouch cells fit in each part of
the trunk, around the joint modules of layout.csv (plan M-2, D-5).

    python3 hardware/mechanical/modules/pack_fit.py            # needs numpy; a few minutes
    python3 hardware/mechanical/modules/pack_fit.py --layout   # write pack.csv: the reference pack, cell by cell

Cells are boxes at their largest printed tolerance with 0.5 mm between faces, laid
by a greedy lattice in free space 2 mm fine. Nothing is kept for walls, terminals,
cooling, compression, a crush zone or a vent, so a real pack holds less; the fill
is not optimal either, so a better lattice holds somewhat more. 4 mm is kept
from every module, 10 from hip pitch, which turns, 18 from the trunk's own,
which turn against the segment, and the circle the neck pitch module sweeps.
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
    # the neck pitch module, turning with neck yaw about the z axis
    ok &= ~((p[..., 2] > 398.0) & (np.hypot(p[..., 0], p[..., 1]) < 52.0))
    return ok


# The reference pack (spec 03.1, plan M-2, 2026-11-24): SA03 cells in two boxes, 3 mm of
# wall on every side, the back at -150 mm, the left half mirrored; how many of
# each, a choice, so that each box is filled about alike: name, zone, cells
PACK = [("upper", (-150, -20, 124, 240, 424), 38), ("lower", (-150, 40, 155, 122, 208), 24)]
WALL = 3.0


def fill(ok, dims, org=None):
    """The most cells a greedy lattice holds; with `org`, their centres and sizes."""
    best, where = 0, []
    orient = sorted(set(itertools.permutations(dims)))
    for order in itertools.product(orient, repeat=2):
        o, n, at = ok.copy(), 0, []
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
                            at.append(((x, y, z), k, dm))
                            z += k[2]
                        else:
                            z += 1
        if n > best:
            best, where = n, at
    if org is None:
        return best
    return [(tuple(org[i] + S * (p[i] + k[i] / 2) for i in range(3)), dm) for p, k, dm in where]


def layout(rows):
    out = []
    for name, (x0, x1, yh, z0, z1), n in PACK:
        ok = free(x0 + WALL, x1 - WALL, yh - WALL, z0 + WALL, z1 - WALL, rows)
        a, b, t = CELLS["SA03"][:3]
        at = fill(ok[:, ok.shape[1] // 2:, :], (a, b, t), (x0 + WALL, 0.0, z0 + WALL))
        print("%s: %d of %d cells placed" % (name, n, 2 * len(at)))
        # from the back forward, so that the room left is toward the modules
        at.sort(key=lambda c: (round(c[0][0] - c[1][0] / 2, 1), round(abs(c[0][1]), 1), c[0][2]))
        out += [(name, (c[0], s * c[1], c[2]), d) for c, d in at[:n // 2] for s in (1, -1)]
    return out


def main():
    rows = g.place()[2]
    if "--layout" in sys.argv:
        text = "box,x_mm,y_mm,z_mm,dx_mm,dy_mm,dz_mm\n" + "".join(
            "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n" % ((n,) + c + d) for n, c, d in layout(rows))
        (pathlib.Path(__file__).resolve().parent / "pack.csv").write_text(text, encoding="utf-8")
        return
    for name, x0, x1, yh, z0, z1 in ZONES:
        ok = free(x0, x1, yh, z0, z1, rows)
        cells = []
        for c, (a, b, t, wh, gm) in CELLS.items():
            n = fill(ok, (a, b, t))
            cells.append("%s: %d cells, %.2f kWh" % (c, n, n * wh / 1000))
        print("%-30s free %.1f L   %s" % (name, ok.sum() * S ** 3 / 1e6, "; ".join(cells)), flush=True)


if __name__ == "__main__":
    main()
