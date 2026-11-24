#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
The joint modules in CAD, and where they sit: plan M-1 and M-2, first pass.

    python3 hardware/mechanical/modules/generate_modules.py            # build, audit, write the STEP files and layout.csv
    python3 hardware/mechanical/modules/generate_modules.py --check    # build and audit, write nothing
    python3 hardware/mechanical/modules/generate_modules.py --mesh DIR # also write one STL per module part and layout.json

MODULES are the nine modules spec 02.6 declares, drawn from their makers'
installation drawings. A figure marked M is read off the drawing, where it is
printed; one marked S is scaled from the drawing, where it is not, and is
illustration. SEmotor's sheet prints the envelope only.

LAYOUT is a first layout, not a design: each module lies on its joint's own
axis line and slides along it until it clears its neighbours, with 3 mm between
them. No linkage, no belt, no structure. What it is for is the clash report:
which modules fit the segment envelopes, and how far each joint turns alone
before two modules touch.

The geometry is built by FreeCAD (1.1); run under python3, the script runs
itself again under FreeCAD's console executable, as ../skeleton does.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
for p in ("hardware/sim-model", "hardware/electrical", "hardware/mechanical/skeleton"):
    sys.path.insert(0, str(REPO / p))

import actuator_sizing as asz  # noqa: E402
import generate_skeleton as gs  # noqa: E402
import generate_urdf as gu  # noqa: E402

GAP = 3.0                 # mm between neighbouring modules, a choice
ENV_MODE, ENV_OUT, ENV_MESH = "GEMS_MODULES_MODE", "GEMS_MODULES_OUT", "GEMS_MODULES_MESH"
STEP_MODULES, STEP_LAYOUT, CSV_LAYOUT = "gems-modules.step", "gems-module-layout.step", "layout.csv"

# Each module along its axis, z = 0 at the rear face, output at the top.
# cap, body, boss, output: (diameter, z from, z to); flats: width across the
# cap's flats; fins: (z from, z to, count, depth); holes: (face, count,
# pitch circle, diameter, depth, first angle deg); bore: through hole.
# Every diameter and length is printed on the drawing (M) but those listed in
# "scaled" (S).
MODULES = {
    "EC-A10020-P2-24": dict(
        maker="ENCOS", source="manual V3.13 §7.1", od=124.0, length=85.0,
        cap=(100.0, 0.0, 15.5), flats=94.0, body=(124.0, 15.5, 81.5), boss=(100.0, 81.5, 83.5), output=(62.0, 83.5, 85.0),
        fins=(27.0, 71.0, 15, 1.2), bore=8.0,
        holes=[("front", 10, 116.5, 4.0, 12.0, 0.0), ("out", 6, 50.0, 5.0, 12.0, 0.0), ("out", 3, 35.0, 6.0, 5.0, 30.0), ("rear", 8, 116.5, 4.0, 10.0, 22.5)],
        scaled="fins; angles of the bolt circles"),
    "EC-A13715-P1-12.67": dict(
        maker="ENCOS", source="manual V3.13 §9.1", od=170.0, length=73.0,
        cap=(100.0, 0.0, 11.5), flats=90.0, rear=(130.0, 11.5, 14.5), body=(170.0, 14.5, 59.5), boss=(124.0, 59.5, 68.0),
        ring=(95.0, 68.0, 69.3), output=(70.0, 69.3, 73.0), fins=(32.0, 56.0, 9, 1.5), bore=0.0,
        holes=[("front", 12, 155.0, 4.0, 21.0, 15.0), ("out", 3, 57.4, 6.0, 3.7, 30.0), ("out", 3, 40.0, 5.0, 3.7, 90.0), ("rear", 20, 155.0, 4.0, 15.0, 0.0)],
        scaled="fins; angles of the bolt circles; hole depths in the output disc, cut short"),
    "EC-A8116-P1-18": dict(
        maker="ENCOS", source="manual V3.13 §7.1", od=105.0, length=57.0,
        cap=(85.0, 0.0, 2.0), flats=None, body=(105.0, 2.0, 53.5), boss=(85.0, 53.5, 55.5), output=(60.0, 55.5, 57.0),
        fins=(24.0, 36.0, 5, 1.5), bore=0.0,
        holes=[("front", 8, 97.0, 4.0, 5.5, 22.5), ("out", 6, 50.0, 4.0, 8.5, 15.0), ("rear", 8, 97.0, 4.0, 17.5, 22.5)],
        scaled="fins; angles of the bolt circles"),
    "EC-A10020-P1-12": dict(
        maker="ENCOS", source="manual V3.13 §8.1", od=124.0, length=60.0,
        cap=(80.0, 0.0, 9.5), flats=72.0, body=(124.0, 9.5, 53.0), boss=(86.0, 53.0, 59.0), output=(47.0, 59.0, 60.0),
        fins=(23.0, 49.0, 9, 1.3), bore=0.0,
        holes=[("front", 12, 116.0, 4.0, 10.0, 15.0), ("out", 3, 38.0, 4.0, 10.0, 10.0), ("rear", 12, 116.0, 4.0, 10.0, 7.09)],
        scaled="fins; angles of the bolt circles; the output's 38 mm pitch circle"),
    "EC-A4315-P2-36": dict(
        maker="ENCOS", source="manual V3.13 §3.1", od=56.0, length=69.5,
        cap=None, flats=None, body=(56.0, 0.0, 64.5), waist=(54.5, 20.0, 47.0), boss=None, output=(35.0, 64.5, 69.5),
        fins=None, bore=0.0,
        holes=[("front", 6, 49.0, 3.0, 10.0, 60.0), ("out", 6, 26.0, 3.0, 10.0, 0.0), ("out", 3, 26.0, 4.0, 3.0, 30.0)],
        scaled="the waist's ends; angles of the bolt circles"),
    "EC-A6416-P2-25": dict(
        maker="ENCOS", source="manual V3.13 §5.1", od=88.0, length=67.5,
        cap=(70.8, 0.0, 11.5), flats=68.0, body=(88.0, 11.5, 58.5), boss=(68.0, 58.5, 63.5), output=(45.0, 63.5, 67.5),
        fins=(27.0, 51.0, 10, 1.2), bore=0.0,
        holes=[("front", 8, 80.0, 4.0, 7.5, 22.5), ("out", 6, 35.0, 4.0, 8.0, 0.0), ("rear", 8, 80.0, 4.0, 22.0, 22.5)],
        scaled="fins; angles of the output's holes"),
    "EC-A3814-H14-107": dict(
        maker="ENCOS", source="manual V3.13 §1.1 (harmonic)", od=53.0, length=78.5,
        cap=None, flats=None, body=(53.0, 0.0, 75.5), boss=None, output=(33.0, 75.5, 78.5),
        fins=(28.0, 49.0, 8, 1.0), bore=8.0,
        holes=[("front", 8, 47.0, 3.0, 12.5, 0.0), ("out", 6, 17.0, 4.0, 23.45, 30.0), ("out", 6, 24.0, 4.0, 4.3, 0.0)],
        scaled="fins"),
    "RMD-X12-P20-320": dict(
        maker="MyActuator", source="XV4 sheet 2026-04-16", od=124.0, length=85.0,
        cap=(47.0, 0.0, 4.5), flats=None, body=(124.0, 4.5, 69.5), boss=(109.0, 69.5, 82.0), output=(85.0, 82.0, 85.0),
        fins=None, slots=(14, 4.0, 1.5, 22.0, 69.5), bore=12.6,
        holes=[("front", 16, 116.5, 4.0, 8.0, 0.0), ("out", 12, 72.0, 5.0, 9.0, 0.0)],
        scaled="the rear hub's 47 mm; the side slots"),
    "SEAF70A16NG02": dict(
        maker="SEmotor", source="SETZ70 sheet", od=78.0, length=65.0,
        cap=None, flats=None, body=(78.0, 0.0, 61.0), boss=None, output=(50.0, 61.0, 65.0),
        fins=None, bore=0.0, holes=[], scaled="everything but the envelope, 78 x 65 mm"),
}

# Where each module's centre lies, in its joint's axis line: offset along the
# joint axis from the joint origin, mm; the direction its output faces along the
# axis (+1, -1); the URDF link its housing is fixed to; and, for a trunk axis
# spread over three coupled segments, the segment joint it drives. Left side;
# the right is its mirror. "why" is the reason for the place.
L = lambda n: MODULES[asz.JOINT_MODULE[n]]["length"] / 2.0
R = lambda n: MODULES[asz.JOINT_MODULE[n]]["od"] / 2.0


def layout_rules():
    return {
        "hip_pitch": (0.0, "out", "hip_roll_link", "centred on the hip"),
        "hip_roll": (-(R("hip_pitch") + GAP + L("hip_roll")), 1, "pelvis", "behind the hip pitch module"),
        "hip_yaw": (-(R("hip_pitch") + GAP + L("hip_yaw")), -1, "hip_pitch_link", "below it, in the thigh"),
        "knee": (0.0, "out", "thigh", "centred on the knee"),
        "ankle_pitch": (0.0, "out", "shank", "centred on the ankle"),
        "ankle_roll": (-(R("ankle_pitch") + GAP + L("ankle_roll")), 1, "ankle_pitch_link", "behind the ankle pitch module"),
        "shoulder_roll": (0.0, 1, "shoulder_pitch_link", "centred on the shoulder"),
        "shoulder_pitch": (-(R("shoulder_roll") + GAP + L("shoulder_pitch")), "out", "torso", "inboard, in the torso"),
        "shoulder_yaw": (-(R("shoulder_roll") + GAP + L("shoulder_yaw")), -1, "shoulder_roll_link", "below it, in the upper arm"),
        "elbow": (0.0, "out", "upper_arm", "centred on the elbow"),
        "wrist_pitch": (0.0, "out", "wrist_yaw_link", "centred on the wrist"),
        "wrist_yaw": (R("wrist_pitch") + GAP + L("wrist_yaw"), -1, "forearm", "above it, in the forearm"),
        "wrist_roll": (R("wrist_pitch") + GAP + L("wrist_roll"), -1, "wrist_pitch_link", "in front of the wrist pitch module"),
        "trunk_pitch": (0.0, 1, "trunk_yaw_link", "on the lowest segment's axis"),
        "trunk_yaw": (0.0, 1, "spine_thoracic", "on the upper segment's axis"),
        "trunk_roll": (0.0, 1, "spine_lumbar", "on the middle segment's axis"),
        "neck_pitch": (0.0, 1, "neck_yaw_link", "centred on the neck"),
        "neck_yaw": (-(R("neck_pitch") + GAP + L("neck_yaw")), 1, "torso", "below it, in the torso"),
    }


DRIVES = {"trunk_roll": "trunk_roll_2", "trunk_yaw": "trunk_yaw_3"}      # the coupled segment joint the module sits on


def place():
    """31 modules: name, module, centre (mm, URDF frame), output direction
    (unit vector), housing link, joint axis line."""
    robot = gu.build(asz.REF_MASS)
    joints = {j["name"]: j for j in gs.skeleton(robot)[0]}
    rows = []
    for base, (off, face, link, why) in layout_rules().items():
        sided = ("l_" + base) in joints
        for side in (("l_", "r_") if sided else ("",)):
            name = side + base
            j = joints[DRIVES.get(base, name)]
            a, sgn = j["axis"], 1.0
            o = off
            if side == "r_" and a[1]:             # axes along y mirror
                sgn = -1.0
                o = -off
            out = (1.0 if side != "r_" else -1.0) if face == "out" else float(face)
            if face == "out" and not sided:
                out = 1.0
            c = tuple(p + o * v for p, v in zip(j["origin"], a))
            d = tuple(out * v for v in a)
            rows.append(dict(name=name, joint=j["name"], module=asz.JOINT_MODULE[base], centre=c, out=d,
                             link=(side + link) if (side + link) in {x["child"] for x in joints.values()} | {"pelvis"} else link,
                             origin=j["origin"], axis=a, why=why))
    return robot, joints, rows


# -- clashes, in plain Python ------------------------------------------------

def _rot(axis, ang):
    x, y, z = axis
    c, s = math.cos(ang), math.sin(ang)
    t = 1 - c
    return ((t * x * x + c, t * x * y - s * z, t * x * z + s * y),
            (t * x * y + s * z, t * y * y + c, t * y * z - s * x),
            (t * x * z - s * y, t * y * z + s * x, t * z * z + c))


def _mul(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def _about(p, o, axis, ang):
    d = _mul(_rot(axis, ang), tuple(a - b for a, b in zip(p, o)))
    return tuple(a + b for a, b in zip(d, o))


def _points(c, d, r, h, n=36, m=7):
    ref = (1.0, 0, 0) if abs(d[0]) < 0.9 else (0, 1.0, 0)
    u = (d[1] * ref[2] - d[2] * ref[1], d[2] * ref[0] - d[0] * ref[2], d[0] * ref[1] - d[1] * ref[0])
    k = math.sqrt(sum(x * x for x in u))
    u = tuple(x / k for x in u)
    v = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    pts = []
    for i in range(m):
        z = -h / 2 + h * i / (m - 1)
        for rr in ((r,) if 0 < i < m - 1 else (r, r * 0.75, r * 0.5, r * 0.25, 0.0)):
            for q in range(n if rr else 1):
                a = 2 * math.pi * q / n
                pts.append(tuple(c[k] + d[k] * z + rr * (math.cos(a) * u[k] + math.sin(a) * v[k]) for k in range(3)))
    return pts


def _inside(p, c, d, r, h, tol=0.5):
    w = tuple(a - b for a, b in zip(p, c))
    z = sum(a * b for a, b in zip(w, d))
    if abs(z) > h / 2 - tol:
        return False
    return sum(x * x for x in w) - z * z < (r - tol) ** 2


def overlap(a, b):
    """True when the envelopes of two posed modules overlap by more than 0.5 mm."""
    for p, q in ((a, b), (b, a)):
        ca, da, ra, ha = p
        cb, db, rb, hb = q
        if sum((x - y) ** 2 for x, y in zip(ca, cb)) > (math.hypot(ra, ha / 2) + math.hypot(rb, hb / 2)) ** 2:
            return False
        if any(_inside(x, cb, db, rb, hb) for x in _points(ca, da, ra, ha)):
            return True
    return False


def below(joints, joint):
    """Links that move when `joint` (and the joints coupled to it) turns."""
    kids = {}
    for j in joints.values():
        kids.setdefault(j["parent"], []).append(j["child"])
    out, todo = set(), [joints[joint]["child"]]
    while todo:
        k = todo.pop()
        out.add(k)
        todo += kids.get(k, [])
    return out


def cyl(m):
    d = MODULES[m["module"]]
    return (m["centre"], m["out"], d["od"] / 2.0, d["length"])


def travel_report(robot, joints, rows, step_deg=2.0):
    """For each joint turned alone from the zero pose, the angles within its
    mechanical travel where no two module envelopes overlap, and the pair that
    stops it. The drive modules only: no segment, no structure."""
    limits = {j.get("name"): tuple(math.degrees(float(j.find("limit").get(k))) for k in ("lower", "upper")) for j in robot.findall("joint")}
    rep = {}
    for j in joints.values():
        if j["mimic"] or j["name"].startswith("trunk"):
            continue
        moved = below(joints, j["name"])
        A = [m for m in rows if m["link"] in moved]
        B = [m for m in rows if m["link"] not in moved]
        lo, hi = limits[j["name"]]
        res = []
        for end in (lo, hi):
            ang, hit = 0.0, ""
            while abs(ang) < abs(end) - 1e-9:
                nxt = max(end, ang - step_deg) if end < 0 else min(end, ang + step_deg)
                t = math.radians(nxt)
                R_ = _rot(j["axis"], t)
                for m in A:
                    c, d, r, h = cyl(m)
                    pm = (_about(c, j["origin"], j["axis"], t), _mul(R_, d), r, h)
                    for k in B:
                        if overlap(pm, cyl(k)):
                            hit = "%s / %s" % (m["name"], k["name"])
                            break
                    if hit:
                        break
                if hit:
                    break
                ang = nxt
            res.append((ang, hit))
        rep[j["name"]] = (lo, hi, res[0], res[1])
    return rep


def protrusion(robot, rows):
    """How far each module's envelope stands out of every segment envelope of the
    zero pose: the largest distance from a point of its surface to the union
    of the segment envelopes, mm, and the point's direction."""
    env = gs.skeleton(robot)[1]
    out = {}
    for m in rows:
        worst, where = 0.0, None
        for p in _points(*cyl(m)):
            best = 1e9
            for e in env:
                d = [p[i] - e["centre"][i] for i in range(3)]
                if e["kind"] == "box":
                    g = [max(0.0, abs(d[i]) - e["size"][i] / 2) for i in range(3)]
                    v = math.sqrt(sum(x * x for x in g))
                else:
                    v = math.hypot(max(0.0, math.hypot(d[0], d[1]) - e["r"]), max(0.0, abs(d[2]) - e["h"] / 2))
                best = min(best, v)
            if best > worst:
                worst, where = best, p
        out[m["name"]] = (worst, where)
    return out


def zero_clashes(rows):
    return [(a["name"], b["name"]) for i, a in enumerate(rows) for b in rows[i + 1:] if overlap(cyl(a), cyl(b))]


def layout_csv(robot, joints, rows, rep, pro):
    f = io.StringIO()
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["joint", "module", "x_mm", "y_mm", "z_mm", "output_x", "output_y", "output_z", "housing_link", "place",
                "outside_segments_mm", "travel_lower_deg", "travel_upper_deg", "clear_lower_deg", "clear_upper_deg", "stopped_by"])
    for m in rows:
        t = rep.get(m["name"])
        w.writerow([m["name"], m["module"]] + ["%.2f" % (v + 0.0) for v in m["centre"]] + ["%d" % round(v) for v in m["out"]]
                   + [m["link"], m["why"], "%.1f" % pro[m["name"]][0]]
                   + (["%.0f" % t[0], "%.0f" % t[1], "%.0f" % t[2][0], "%.0f" % t[3][0], "; ".join(sorted({x for x in (t[2][1], t[3][1]) if x}))] if t else ["", "", "", "", "not checked: coupled trunk axes"]))
    return f.getvalue()


# -- the FreeCAD side --------------------------------------------------------

def solids(name):
    """The module's solids, axis +Z, centred on its envelope's middle: dict part -> shape."""
    import FreeCAD as App
    import Part
    V = App.Vector
    d = MODULES[name]
    cy = lambda t: Part.makeCylinder(t[0] / 2.0, t[2] - t[1], V(0, 0, t[1]))
    body = cy(d["body"])
    if d.get("waist"):
        w = d["waist"]
        body = body.cut(Part.makeCylinder(d["body"][0] / 2 + 1, w[2] - w[1], V(0, 0, w[1])).cut(cy(w)))
    if d.get("rear"):
        body = body.fuse(cy(d["rear"]))
    if d.get("boss"):
        body = body.fuse(cy(d["boss"]))
    if d["fins"]:
        z0, z1, n, dep = d["fins"]
        pitch = (z1 - z0) / n
        ro = d["body"][0] / 2
        for k in range(n):
            z = z0 + pitch * (k + 0.25)
            body = body.cut(Part.makeCylinder(ro + 1, pitch * 0.5, V(0, 0, z)).cut(Part.makeCylinder(ro - dep, pitch * 0.5, V(0, 0, z))))
    if d.get("slots"):
        n, wd, dep, z0, z1 = d["slots"]
        ro = d["body"][0] / 2
        for k in range(n):
            b = Part.makeBox(dep + 1, wd, z1 - z0 - 6, V(ro - dep, -wd / 2, z0 + 3))
            b.rotate(V(0, 0, 0), V(0, 0, 1), 360.0 * k / n)
            body = body.cut(b)
    parts = {"body": body}
    if d.get("cap"):
        cap = cy(d["cap"])
        if d["flats"]:
            f = d["flats"]
            cap = cap.common(Part.makeBox(f, 400, 400, V(-f / 2, -200, -200)))
        parts["cap"] = cap
    o = cy(d["output"])
    if d.get("ring"):
        parts["body"] = parts["body"].fuse(cy(d["ring"]))
    parts["output"] = o
    top = {"front": d["body"][2], "out": d["output"][2], "rear": d["body"][1]}
    for face, n, pcd, dia, dep, a0 in d["holes"]:
        for k in range(n):
            a = math.radians(a0 + 360.0 * k / n)
            x, y = pcd / 2 * math.cos(a), pcd / 2 * math.sin(a)
            z = top[face]
            h = Part.makeCylinder(dia / 2, dep + 0.2, V(x, y, z - dep if face != "rear" else z - 0.2))
            for key in (("output", "body") if face == "out" else ("body",)):
                parts[key] = parts[key].cut(h)
    if d["bore"]:
        b = Part.makeCylinder(d["bore"] / 2, d["length"] + 2, V(0, 0, -1))
        parts = {k: s.cut(b) for k, s in parts.items()}
    for s in parts.values():
        s.translate(V(0, 0, -d["length"] / 2))
    return parts


def envelope(name):
    import FreeCAD as App
    import Part
    d = MODULES[name]
    return Part.makeCylinder(d["od"] / 2, d["length"], App.Vector(0, 0, -d["length"] / 2))


def placement(m):
    import FreeCAD as App
    V = App.Vector
    return App.Placement(V(*m["centre"]), App.Rotation(V(0, 0, 1), V(*m["out"])))


def set_header(path, title):
    p = pathlib.Path(path)
    t = p.read_text(encoding="ascii")
    head, sep, body = t.partition("ENDSEC;")
    head = head.replace("FILE_NAME('Open CASCADE Shape Model'", "FILE_NAME('%s'" % title, 1).replace("('Author')", "('%s')" % gs.STEP_AUTHOR, 1)
    if gs.STEP_AUTHOR not in head:
        raise RuntimeError("STEP header not in the expected form")
    p.write_text(head + sep + body, encoding="ascii", newline="")


def build(mode, out, mesh):
    import FreeCAD as App
    import Import
    import MeshPart
    V = App.Vector
    robot, joints, rows = place()
    checks = []
    ok = lambda label, got, want, good: checks.append((label, got, want, bool(good)))

    # 1. the data: modules are spec 02.6's, at their sheets' envelope
    used = {m["module"] for m in rows}
    ok("modules in use", len(used), len(MODULES), used == set(MODULES))
    size_ok = all(tuple(float(v) for v in asz.MODULE_CATALOGUE[n][6].split(" x ")) == (d["od"], d["length"]) for n, d in MODULES.items())
    ok("envelopes = spec 02.6", size_ok, True, size_ok)
    ok("modules placed", len(rows), 31, len(rows) == 31)
    off = max(math.sqrt(max(0.0, sum((c - o) ** 2 for c, o in zip(m["centre"], m["origin"])) - sum((c - o) * a for c, o, a in zip(m["centre"], m["origin"], m["axis"])) ** 2)) for m in rows)
    ok("on their joint's axis mm", round(off, 6), 0.0, off < 1e-6)
    z = zero_clashes(rows)
    ok("overlaps, zero pose", len(z), 0, not z)

    # 2. the solids, against the data
    parts = {n: solids(n) for n in sorted(MODULES)}
    vol_ok = bb_ok = valid = True
    for n, ps in parts.items():
        d = MODULES[n]
        bb = App.BoundBox()
        for s in ps.values():
            valid = valid and s.isValid() and len(s.Solids) >= 1
            bb.add(s.BoundBox)
        bb_ok = bb_ok and abs(bb.XLength - d["od"]) < 0.05 and abs(bb.ZLength - d["length"]) < 1e-3 and abs(bb.ZMin + d["length"] / 2) < 1e-3
    ok("solids valid", valid, True, valid)
    ok("solids = envelopes", bb_ok, True, bb_ok)
    # 3. mirror
    pos = {m["name"]: m for m in rows}
    mir = all(abs(pos[n]["centre"][1] + pos["r" + n[1:]]["centre"][1]) < 1e-9 and abs(pos[n]["centre"][0] - pos["r" + n[1:]]["centre"][0]) < 1e-9 for n in pos if n.startswith("l_"))
    ok("right mirrors left", mir, True, mir)

    rep = travel_report(robot, joints, rows)
    pro = protrusion(robot, rows)
    text = layout_csv(robot, joints, rows, rep, pro)
    for label, got, want, good in checks:
        print("  %-26s %-10s expected %-10s %s" % (label, got, want, "ok" if good else "MISMATCH"))
    if z:
        print("  overlapping:", z)
    short = [(n, t) for n, t in rep.items() if t[2][1] or t[3][1]]
    print("  joints whose travel two modules stop: %d of %d" % (len(short), len(rep)))
    for n, (lo, hi, a, b) in short:
        if n.startswith("r_"):
            continue
        print("    %-16s travel %4.0f..%4.0f deg, clear %4.0f..%4.0f   %s" % (n, lo, hi, a[0], b[0], "; ".join(x for x in {a[1], b[1]} if x)))
    print("  furthest outside the segment envelopes, mm:")
    for n, (v, p) in sorted(pro.items(), key=lambda x: -x[1][0]):
        if v > 0.5 and not n.startswith("r_"):
            print("    %-16s %5.1f  at (%.0f, %.0f, %.0f)" % ((n, v) + p))
    if not all(c[3] for c in checks):
        return 1
    if mode == "check":
        have = (HERE / CSV_LAYOUT)
        if not have.exists() or have.read_text(encoding="utf-8") != text:
            print("MISMATCH layout.csv is out of date — run generate_modules.py")
            return 1
        print("Checked; nothing written.")
        return 0

    doc = App.newDocument("gems_modules")
    out = pathlib.Path(out)
    turn = App.Placement(V(0, 0, 0), App.Rotation(V(0, 0, 1), gs.CAD_TURN_DEG))
    objs, x = [], 0.0
    for n in sorted(MODULES):
        x += MODULES[n]["od"] / 2 + 15
        for part, s in parts[n].items():
            o = doc.addObject("Part::Feature", (n + "_" + part).replace("-", "_").replace(".", "_"))
            t = s.copy()
            t.Placement = App.Placement(V(x, 0, 0), App.Rotation()).multiply(t.Placement)
            o.Shape = t
            o.Label = n + " " + part
            objs.append(o)
        x += MODULES[n]["od"] / 2 + 15
    Import.export(objs, str(out / STEP_MODULES))
    set_header(out / STEP_MODULES, "gems-modules")
    objs = []
    for m in rows:
        o = doc.addObject("Part::Feature", "module_" + m["name"])
        s = envelope(m["module"])
        s.Placement = turn.multiply(placement(m))
        o.Shape = s
        o.Label = "%s %s" % (m["name"], m["module"])
        objs.append(o)
    Import.export(objs, str(out / STEP_LAYOUT))
    set_header(out / STEP_LAYOUT, "gems-module-layout")
    (out / CSV_LAYOUT).write_text(text, encoding="utf-8", newline="")
    if mesh:
        md = pathlib.Path(mesh)
        md.mkdir(parents=True, exist_ok=True)
        for n, ps in parts.items():
            for part, s in ps.items():
                MeshPart.meshFromShape(Shape=s, LinearDeflection=0.12, AngularDeflection=0.35).write(str(md / ("%s__%s.stl" % (n, part))))
        segs = [dict(e, centre=list(e["centre"])) for e in gs.skeleton(robot)[1]]
        (md / "layout.json").write_text(json.dumps(dict(
            modules=[dict(name=m["name"], module=m["module"], centre=m["centre"], out=m["out"], link=m["link"]) for m in rows], segments=segs,
            outside={k: v[0] for k, v in pro.items()})), encoding="utf-8")
    for f in (STEP_MODULES, STEP_LAYOUT, CSV_LAYOUT):
        print("Wrote %s (%d bytes)" % (f, (out / f).stat().st_size))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true", help="build and audit, write nothing")
    ap.add_argument("--mesh", default="", help="also write STL meshes and layout.json to this directory")
    ap.add_argument("--freecadcmd", default=os.environ.get("FREECADCMD", ""))
    a = ap.parse_args()
    exe = a.freecadcmd or shutil.which("freecadcmd") or shutil.which("freecad.cmd")
    if not exe:
        sys.exit("FreeCAD's console executable not found; pass --freecadcmd")
    env = dict(os.environ, **{ENV_MODE: "check" if a.check else "write", ENV_OUT: str(HERE), ENV_MESH: str(pathlib.Path(a.mesh).resolve()) if a.mesh else ""})
    r = subprocess.run([exe, str(pathlib.Path(__file__).resolve())], env=env, capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith(("  ", "Wrote", "Checked", "MISMATCH", "GEMS_", "Traceback"))]
    print("\n".join(l for l in lines if not l.startswith("GEMS_")))
    rc = next((int(l.split("=")[1]) for l in lines if l.startswith("GEMS_MODULES_RC=")), 1)
    if rc:
        sys.stderr.write(r.stderr[-3000:])
    return rc


if __name__ == "__main__" and not os.environ.get(ENV_MODE):
    sys.exit(main())
elif os.environ.get(ENV_MODE):
    try:
        _rc = build(os.environ[ENV_MODE], os.environ[ENV_OUT], os.environ[ENV_MESH])
    except Exception:
        import traceback
        traceback.print_exc()
        _rc = 1
    print("GEMS_MODULES_RC=%d" % _rc)
    sys.stdout.flush()
    os._exit(_rc)
