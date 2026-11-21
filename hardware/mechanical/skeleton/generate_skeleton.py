#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Generate the parametric CAD skeleton of the GEMs body (plan M-1).

Source of truth: hardware/kinematics.md, as encoded in
hardware/sim-model/generate_urdf.py. This script imports that encoding and the
URDF it builds; it restates no dimension of its own, so the CAD and the URDF
cannot become two declarations of the same body.

    python3 hardware/mechanical/skeleton/generate_skeleton.py          # build, audit, write gems-skeleton.step
    python3 hardware/mechanical/skeleton/generate_skeleton.py --check  # build and audit, write nothing

The geometry is built by FreeCAD (1.1). Run under python3, the script runs
itself again under FreeCAD's console executable — `freecadcmd`, or
`freecad.cmd` for the Snap package; override with --freecadcmd or
$FREECADCMD — passing its mode through the environment, since that executable
takes no options of its own, and reports what the FreeCAD side prints.

WHAT IS IN IT
-------------
  * Joint frames: one marker per URDF joint — 37 of them, 31 actuated and 6
    coupled through <mimic> — a 60 mm rod through the joint's zero-pose
    origin along its axis, carrying the joint's name, parent, child and type.
    Joints of one multi-axis group (shoulder, hip, wrist, ankle, trunk
    segment) share an origin and differ in axis.
  * Segment envelopes: the 17 drawn segments of the URDF — the same boxes and
    cylinders, at the same places. They follow proportion, not structure
    (hardware/sim-model/README.md): they mark where a segment's contents go,
    not what size those contents are.

WHAT IS NOT YET IN IT
---------------------
  * Keep-out volumes. The space a joint module occupies waits for decision
    D-2 (which module); the space a segment sweeps through its travel is the
    next step of M-1.

THE AUDIT
---------
After the CAD is built it is measured — each marker's centre and axis, each
envelope's bounding box — and compared with the URDF's own forward kinematics
in the zero pose, at 1 µm. A mismatch exits non-zero and writes nothing.
Units: the URDF is in metres, FreeCAD in millimetres.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "hardware" / "sim-model"))

import generate_urdf as gu  # noqa: E402  (the declaration, encoded once)

# Author of the released file (workspace rule, 2026-11-03), in the STEP
# header's encoding: ISO 10303-21 strings are ASCII, wider characters \X2\.
STEP_AUTHOR = r"Hu\X2\1EF3\X0\nh Mai Ph\X2\00FA\X0\c (Plone Mraz)"

MM = 1000.0
TOL_MM = 1e-3
MARKER_LEN, MARKER_R = 60.0, 4.0
STEP_OUT = HERE / "gems-skeleton.step"
ENV_MODE, ENV_OUT, ENV_FCSTD = "GEMS_SKELETON_MODE", "GEMS_SKELETON_OUT", "GEMS_SKELETON_FCSTD"


# -- what the URDF says, in the zero pose ----------------------------------

def link_offsets(robot):
    """World position of every link frame, in metres, by summing joint
    origins down the tree (every origin carries rpy = 0)."""
    off = {robot.find("link").get("name"): (0.0, 0.0, 0.0)}
    for j in robot.findall("joint"):
        p = off[j.find("parent").get("link")]
        o = gu._xyz(j.find("origin"))
        off[j.find("child").get("link")] = tuple(a + b for a, b in zip(p, o))
    return off


def skeleton(robot):
    """Joint frames and segment envelopes to build, in millimetres."""
    off = link_offsets(robot)
    joints = []
    for j in robot.findall("joint"):
        parent, child = j.find("parent").get("link"), j.find("child").get("link")
        origin = tuple(MM * (a + b) for a, b in zip(off[parent], gu._xyz(j.find("origin"))))
        mimic = j.find("mimic")
        joints.append(dict(
            name=j.get("name"), parent=parent, child=child, type=j.get("type"),
            origin=origin, axis=tuple(float(v) for v in j.find("axis").get("xyz").split()),
            mimic=mimic.get("joint") if mimic is not None else ""))
    envelopes = []
    for link in robot.findall("link"):
        vis = link.find("visual")
        if vis is None:
            continue
        c = tuple(MM * (a + b) for a, b in zip(off[link.get("name")], gu._xyz(vis.find("origin"))))
        g = vis.find("geometry")[0]
        if g.tag == "box":
            sx, sy, sz = (MM * float(v) for v in g.get("size").split())
            envelopes.append(dict(link=link.get("name"), kind="box", centre=c, size=(sx, sy, sz)))
        else:
            envelopes.append(dict(link=link.get("name"), kind="cyl", centre=c,
                                  r=MM * float(g.get("radius")), h=MM * float(g.get("length"))))
    return joints, envelopes


def expected(robot):
    """What the audit compares against, computed by the URDF generator's own
    forward kinematics and extents — a second path to the same numbers."""
    origins = {j.get("name"): tuple(MM * v for v in gu.point_at(robot, {}, j.find("child").get("link"), (0, 0, 0)))
               for j in robot.findall("joint")}
    axes = {j.get("name"): tuple(float(v) for v in j.find("axis").get("xyz").split())
            for j in robot.findall("joint")}
    ext = {k: [(MM * lo, MM * hi) for lo, hi in v] for k, v in gu.geometry_extents(robot).items()}
    actuated = sum(1 for j in robot.findall("joint") if j.find("mimic") is None)
    return origins, axes, ext, actuated


# -- the FreeCAD side --------------------------------------------------------

def set_step_header(path):
    """Name the file and its author in the STEP header. FreeCAD writes the
    placeholders 'Open CASCADE Shape Model' and 'Author'."""
    p = pathlib.Path(path)
    text = p.read_text(encoding="ascii")
    head, sep, body = text.partition("ENDSEC;")
    head = head.replace("FILE_NAME('Open CASCADE Shape Model'", "FILE_NAME('gems-skeleton'", 1)
    head = head.replace("('Author')", "('%s')" % STEP_AUTHOR, 1)
    if STEP_AUTHOR not in head:
        raise RuntimeError("STEP header not in the expected form; author not set")
    p.write_text(head + sep + body, encoding="ascii", newline="")


def build_and_audit(mode, out, fcstd):
    import FreeCAD as App
    import Part
    import Import
    V = App.Vector

    robot = gu.build(96.2)
    joints, envelopes = skeleton(robot)
    origins, axes, ext, actuated = expected(robot)

    doc = App.newDocument("gems_skeleton")
    g_frames = doc.addObject("App::DocumentObjectGroup", "JointFrames")
    g_env = doc.addObject("App::DocumentObjectGroup", "SegmentEnvelopes")

    markers = []
    for j in joints:
        o, a = V(*j["origin"]), V(*j["axis"])
        shape = Part.makeCylinder(MARKER_R, MARKER_LEN, o - a * (MARKER_LEN / 2), a)
        obj = doc.addObject("Part::Feature", "joint_" + j["name"])
        obj.Shape = shape
        for prop, val in (("Joint", j["name"]), ("ParentLink", j["parent"]),
                          ("ChildLink", j["child"]), ("JointType", j["type"]),
                          ("Mimic", j["mimic"])):
            obj.addProperty("App::PropertyString", prop, "GEMs")
            setattr(obj, prop, val)
        g_frames.addObject(obj)
        markers.append((j["name"], obj))

    bodies = []
    for e in envelopes:
        c = V(*e["centre"])
        if e["kind"] == "box":
            sx, sy, sz = e["size"]
            shape = Part.makeBox(sx, sy, sz, c - V(sx / 2, sy / 2, sz / 2))
        else:
            shape = Part.makeCylinder(e["r"], e["h"], c - V(0, 0, e["h"] / 2), V(0, 0, 1))
        obj = doc.addObject("Part::Feature", "env_" + e["link"])
        obj.Shape = shape
        obj.addProperty("App::PropertyString", "Link", "GEMs")
        obj.Link = e["link"]
        g_env.addObject(obj)
        bodies.append((e["link"], obj))
    doc.recompute()

    # measure what was built, compare with the URDF
    checks = []
    bad_origin = bad_axis = 0
    for name, obj in markers:
        bb = obj.Shape.BoundBox
        got = (bb.Center.x, bb.Center.y, bb.Center.z)
        if max(abs(g - w) for g, w in zip(got, origins[name])) > TOL_MM:
            bad_origin += 1
        cyl = [f for f in obj.Shape.Faces if isinstance(f.Surface, Part.Cylinder)][0]
        ax = cyl.Surface.Axis
        if abs(abs(ax.dot(V(*axes[name]))) - 1.0) > 1e-9:
            bad_axis += 1
    bad_env = 0
    for link, obj in bodies:
        bb = obj.Shape.BoundBox
        got = [(bb.XMin, bb.XMax), (bb.YMin, bb.YMax), (bb.ZMin, bb.ZMax)]
        if any(abs(g - w) > TOL_MM for gp, wp in zip(got, ext[link]) for g, w in zip(gp, wp)):
            bad_env += 1
    n_act = sum(1 for _, o in markers if not o.Mimic)
    z_lo = min(o.Shape.BoundBox.ZMin for _, o in bodies)
    z_hi = max(o.Shape.BoundBox.ZMax for _, o in bodies)
    drawn = (z_hi - z_lo) / MM
    checks = [
        ("joint frames", len(markers), len(origins), len(markers) == len(origins) == 37),
        ("actuated joints", n_act, actuated, n_act == actuated == 31),
        ("frames at URDF origin", bad_origin == 0, True, bad_origin == 0),
        ("frames on URDF axis", bad_axis == 0, True, bad_axis == 0),
        ("segment envelopes", len(bodies), len(ext), len(bodies) == len(ext) == 17),
        ("envelopes = URDF", bad_env == 0, True, bad_env == 0),
        ("drawn height m", round(drawn, 3), gu.DECLARED_HEIGHT,
         abs(drawn - gu.DECLARED_HEIGHT) < 0.02),
        ("solids valid", all(o.Shape.isValid() for _, o in markers + bodies), True,
         all(o.Shape.isValid() for _, o in markers + bodies)),
    ]
    ok = True
    print("gems-skeleton — CAD skeleton, generated from hardware/kinematics.md via generate_urdf.py")
    print("=" * 72)
    for name, got, want, passed in checks:
        print("  %-24s %-10s expected %-10s %s" % (name, got, want, "ok" if passed else "MISMATCH"))
        ok = ok and passed
    if ok and mode == "write":
        Import.export([o for _, o in markers] + [o for _, o in bodies], out)
        set_step_header(out)
        print("Wrote %s — %d joint frames, %d segment envelopes." % (out, len(markers), len(bodies)))
        if fcstd:
            doc.saveAs(fcstd)
            print("Saved %s" % fcstd)
    print("SKELETON_AUDIT %s" % ("PASS" if ok else "FAIL"))


# -- the python3 side --------------------------------------------------------

def find_freecadcmd(given):
    for cand in (given, os.environ.get("FREECADCMD"), "freecadcmd", "FreeCADCmd", "freecad.cmd"):
        if cand and shutil.which(cand):
            return shutil.which(cand)
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="build and audit, write nothing")
    ap.add_argument("--out", default=str(STEP_OUT), help="STEP output path")
    ap.add_argument("--fcstd", default="", help="also save the FreeCAD document here")
    ap.add_argument("--freecadcmd", default=None, help="FreeCAD console executable")
    a = ap.parse_args(argv)

    exe = find_freecadcmd(a.freecadcmd)
    if not exe:
        print("No FreeCAD console executable found (freecadcmd, freecad.cmd); "
              "pass --freecadcmd or set $FREECADCMD.")
        return 2
    env = dict(os.environ)
    env[ENV_MODE] = "check" if a.check else "write"
    env[ENV_OUT] = str(pathlib.Path(a.out).resolve())
    env[ENV_FCSTD] = str(pathlib.Path(a.fcstd).resolve()) if a.fcstd else ""
    proc = subprocess.run([exe, str(pathlib.Path(__file__).resolve())], env=env,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = proc.stdout + proc.stderr
    lines = [l for l in out.splitlines()
             if l.startswith(("gems-skeleton", "=", "  ", "Wrote", "Saved", "SKELETON_AUDIT",
                              "Traceback", "  File")) or "Error" in l]
    print("\n".join(l for l in lines if not l.startswith("SKELETON_AUDIT")))
    if "SKELETON_AUDIT PASS" in out:
        if a.check:
            print("\nAudit only; nothing written.")
        return 0
    if "SKELETON_AUDIT FAIL" in out:
        print("\nThe CAD disagrees with the URDF. Fix the generator.")
        return 1
    print("\nFreeCAD did not finish the build:\n" + out[-2000:])
    return 3


if os.environ.get(ENV_MODE):          # running under FreeCAD
    try:
        build_and_audit(os.environ[ENV_MODE], os.environ.get(ENV_OUT, str(STEP_OUT)),
                        os.environ.get(ENV_FCSTD, ""))
    except Exception:
        import traceback
        traceback.print_exc()
        print("SKELETON_AUDIT ERROR")
elif __name__ == "__main__":
    sys.exit(main())
