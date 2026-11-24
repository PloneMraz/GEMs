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

  * Swept keep-out volumes: for each of the 16 segments other than the
    pelvis, the space it can occupy as the joints between it and its parent
    segment turn through their mechanical travel (<limit>), with the parent
    and everything above it held in the zero pose. Built by revolving, joint
    by joint from the one nearest the segment out to the parent, the
    rectangle that bounds the shape's projection on a plane through the
    joint's axis — so each volume contains the true sweep and can exceed it,
    never fall short of it.
  * Joint-module keep-outs at hip pitch, knee and trunk pitch, for the
    modules spec 02.6 declares there (2026-11-23, hardware/electrical/README.md
    §6f): a cylinder of the datasheet's outer diameter and thickness, on the joint's axis, centred on its origin. Where
    along the axis the module sits, and how the modules of one multi-axis
    group clear one another, is layout (plan M-2), not set here.

WHAT IS NOT YET IN IT
---------------------
  * Module keep-outs for the other 26 actuated joints: their modules are
    declared (spec 02.6), their keep-outs not yet built.

TWO FRAMES, ONE ROTATION
------------------------
Every marker and envelope is built in the URDF's frame — x forward, y left,
z up — inside one container, `GEMs_skeleton`, whose placement turns it -90°
about z. In the document and the STEP file the body therefore faces -Y, the
direction FreeCAD's Front view (and Blender's) looks from, with its left side
toward +X. That rotation is the only difference between the CAD frame and the
URDF frame; geometry taken back to the URDF is turned +90° about z.

THE AUDIT
---------
After the CAD is built it is measured — each marker's centre and axis, each
envelope's bounding box, in the container's frame — and compared with the
URDF's own forward kinematics in the zero pose, at 1 µm; the container's
rotation is checked by where the toes end up in the document. Each keep-out is
checked by posing its segment at every combination of each joint's lower,
middle and upper travel and testing that the segment's surface points lie
inside it. Each module keep-out is checked for its centre on the joint's
origin, its axis on the joint's, and its radius and volume against the
datasheet's figures. A mismatch exits non-zero and writes nothing. Units: the
URDF is in metres, FreeCAD in millimetres.
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
sys.path.insert(0, str(REPO / "hardware" / "electrical"))
import actuator_sizing as asz  # noqa: E402  (the modules spec 02.6 declares)

# Author of the released file (workspace rule, 2026-11-03), in the STEP
# header's encoding: ISO 10303-21 strings are ASCII, wider characters \X2\.
STEP_AUTHOR = r"Hu\X2\1EF3\X0\nh Mai Ph\X2\00FA\X0\c (Plone Mraz)"

MM = 1000.0
TOL_MM = 1e-3
CAD_TURN_DEG = -90.0      # about z: URDF +x (forward) to CAD -Y (FreeCAD's Front)
MARKER_LEN, MARKER_R = 60.0, 4.0
STEP_OUT = HERE / "gems-skeleton.step"
ENV_MODE, ENV_OUT, ENV_FCSTD = "GEMS_SKELETON_MODE", "GEMS_SKELETON_OUT", "GEMS_SKELETON_FCSTD"

# The module spec 02.6 declares at the joint, and its envelope: (module, outer
# diameter mm, thickness mm), from the maker's sheet (hardware/electrical/
# README.md §6f, §6g, §6j): ENCOS motor data manual V3.13, "电机尺寸(外径×厚度)" 170×73;
# SEmotor SETZ70/90 sheets, "外形尺寸" φ99*76.5 and φ78*85. Not yet procured:
# rank 1 in hardware/bom/avl.csv. The same rows as JOINT_MODULE of
# hardware/electrical/actuator_sizing.py; the audit checks they agree.
HIP_PITCH = ("SEmotor SETZ90CI-1FG", 99.0, 76.5)
KNEE = ("ENCOS EC-A13715-P1-12.67", 170.0, 73.0)
TRUNK_PITCH = ("SEmotor SETZ70CI-1HA", 78.0, 85.0)
JOINT_MODULES = {
    "l_hip_pitch": HIP_PITCH, "r_hip_pitch": HIP_PITCH,
    "l_knee": KNEE, "r_knee": KNEE,
    "trunk_pitch": TRUNK_PITCH,
}


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


def segment_chains(robot, joints):
    """For each drawn segment, the joints between it and the drawn segment above
    it, the one nearest the segment first, each with its mechanical travel in degrees."""
    import math
    drawn = {l.get("name") for l in robot.findall("link") if l.find("visual") is not None}
    by_child = {j["child"]: j for j in joints}
    limits = {j.get("name"): (float(j.find("limit").get("lower")), float(j.find("limit").get("upper")))
              for j in robot.findall("joint")}
    chains = {}
    for seg in sorted(drawn):
        chain, link = [], seg
        while link in by_child:
            j = by_child[link]
            lo, hi = limits[j["name"]]
            chain.append(dict(j, lo=math.degrees(lo), hi=math.degrees(hi)))
            link = j["parent"]
            if link in drawn:
                break
        if chain:
            chains[seg] = chain
    return chains


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

SWEEP_TESS_MM = 0.5        # tessellation tolerance when reading a shape's points
SWEEP_MARGIN_MM = 1.0      # added to the bounding rectangle, covering the tessellation chord
SWEEP_MARGIN_DEG = 0.5     # added at both ends of each angular span
SWEEP_EDGE_STEP_MM = 2.0   # spacing of the points sampled along every edge


def sweep_about(shape, origin, axis, lo_deg, hi_deg):
    """A solid containing `shape` turned about the line (origin, axis) through
    every angle in [lo_deg, hi_deg]: the bounding rectangle of the shape's
    projection on a plane through the axis, revolved over the shape's own
    angular extent widened by the travel."""
    import math
    import FreeCAD as App
    import Part
    V = App.Vector
    o, a = V(*origin), V(*axis).normalize()
    ref = V(1, 0, 0) if abs(a.x) < 0.9 else V(0, 1, 0)
    u = a.cross(ref).normalize()
    v = a.cross(u)
    # Points of the surface: a tessellation (of a copy — a triangulation left on
    # the shape itself widens its bounding box) and every edge sampled densely,
    # straight ones included: a mesh of a planar face holds only its corners, and
    # angles between two corners would otherwise read as empty.
    pts = shape.copy().tessellate(SWEEP_TESS_MM)[0] + [x.Point for x in shape.Vertexes]
    for edge in shape.Edges:
        pts += edge.discretize(Distance=SWEEP_EDGE_STEP_MM)
    rs, zs, phis = [], [], []
    for p in pts:
        d = p - o
        z = d.dot(a)
        w = d - a * z
        r = w.Length
        rs.append(r)
        zs.append(z)
        if r > 1e-6:
            phis.append(math.degrees(math.atan2(w.dot(v), w.dot(u))) % 360.0)
    phis.sort()
    if phis:
        gaps = [(phis[(i + 1) % len(phis)] - phis[i]) % 360.0 for i in range(len(phis))]
        if len(phis) == 1:
            gaps = [360.0]
        k = max(range(len(gaps)), key=gaps.__getitem__)
        start, own = phis[(k + 1) % len(phis)], 360.0 - gaps[k]
    else:
        start, own = 0.0, 0.0
    span = own + (hi_deg - lo_deg) + 2 * SWEEP_MARGIN_DEG
    first = start + lo_deg - SWEEP_MARGIN_DEG
    z0, z1 = min(zs) - SWEEP_MARGIN_MM, max(zs) + SWEEP_MARGIN_MM
    # The farthest point from the axis lies on the surface; the nearest need not
    # (an axis through the solid's interior), so it is measured on the solid.
    axis_edge = Part.LineSegment(o + a * (z0 - 1.0), o + a * (z1 + 1.0)).toShape()
    near = shape.distToShape(axis_edge)[0]
    r0 = max(0.0, near - SWEEP_MARGIN_MM)
    r1 = max(rs) + SWEEP_MARGIN_MM
    if near < 1e-6:
        # every angle is occupied only if the axis runs through the solid's
        # interior; an axis lying in one of its faces (a knee axis across the top
        # of the shank) touches it without surrounding anything
        inner = [e.valueAt((e.FirstParameter + e.LastParameter) / 2)
                 for e in axis_edge.common(shape).Edges if e.Length > 1e-6]
        if any(shape.isInside(p, 1e-7, False) for p in inner):
            span = 360.0
    # The revolved rectangle is an annular sector. It is built from cylinder
    # primitives in a frame where the axis is +Z and the sector starts at +X,
    # then placed rigidly: exact cylinders keep bounding boxes and inside
    # tests tight.
    full = span >= 360.0
    ang = 360.0 if full else span
    h = z1 - z0
    sector = Part.makeCylinder(r1, h, V(0, 0, z0), V(0, 0, 1), ang)
    if r0 > 0.0:
        sector = sector.cut(Part.makeCylinder(r0, h, V(0, 0, z0), V(0, 0, 1), ang))
    m = App.Matrix(u.x, v.x, a.x, o.x,
                   u.y, v.y, a.y, o.y,
                   u.z, v.z, a.z, o.z,
                   0, 0, 0, 1)
    sector.transformShape(m)          # rigid: transformGeometry would turn it into B-splines
    if not full:
        sector.rotate(o, a, first)
    return sector


def pose_points(points, chain, angles):
    """The points of a segment with the joints of its chain at `angles`
    (degrees, the joint nearest the segment first): each joint turns about its zero-pose line."""
    import FreeCAD as App
    V = App.Vector
    out = []
    for p in points:
        q = V(p)
        for j, ang in zip(chain, angles):
            o = V(*j["origin"])
            q = App.Rotation(V(*j["axis"]), ang).multVec(q - o) + o
        out.append(q)
    return out


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

    robot = gu.build(asz.REF_MASS)
    joints, envelopes = skeleton(robot)
    origins, axes, ext, actuated = expected(robot)

    doc = App.newDocument("gems_skeleton")
    root = doc.addObject("App::Part", "GEMs_skeleton")
    root.Placement = App.Placement(V(0, 0, 0), App.Rotation(V(0, 0, 1), CAD_TURN_DEG))
    g_frames = doc.addObject("App::DocumentObjectGroup", "JointFrames")
    g_env = doc.addObject("App::DocumentObjectGroup", "SegmentEnvelopes")
    root.addObject(g_frames)
    root.addObject(g_env)

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

    g_keep = doc.addObject("App::DocumentObjectGroup", "KeepOutSwept")
    root.addObject(g_keep)
    chains = segment_chains(robot, joints)
    env_shape = {link: obj.Shape for link, obj in bodies}
    keepouts = []
    for seg, chain in chains.items():
        shape = env_shape[seg]
        for j in chain:                      # the joint nearest the segment first
            shape = sweep_about(shape, j["origin"], j["axis"], j["lo"], j["hi"])
        obj = doc.addObject("Part::Feature", "keepout_" + seg)
        obj.Shape = shape
        obj.addProperty("App::PropertyString", "Link", "GEMs")
        obj.Link = seg
        obj.addProperty("App::PropertyString", "Joints", "GEMs")
        obj.Joints = " ".join(j["name"] for j in chain)
        g_keep.addObject(obj)
        keepouts.append((seg, obj))

    g_mod = doc.addObject("App::DocumentObjectGroup", "KeepOutModule")
    root.addObject(g_mod)
    by_name = {j["name"]: j for j in joints}
    modules = []
    for jn, (model, od, th) in JOINT_MODULES.items():
        j = by_name[jn]
        o, a = V(*j["origin"]), V(*j["axis"]).normalize()
        shape = Part.makeCylinder(od / 2, th, o - a * (th / 2), a)
        obj = doc.addObject("Part::Feature", "module_" + jn)
        obj.Shape = shape
        for prop, val in (("Joint", jn), ("Module", model)):
            obj.addProperty("App::PropertyString", prop, "GEMs")
            setattr(obj, prop, val)
        g_mod.addObject(obj)
        modules.append((jn, obj))
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
    # the container's turn, read from where the body ends up in the document
    env = dict(bodies)
    world = lambda p: root.Placement.multVec(p)
    lf, rf = env["l_foot"].Shape.BoundBox, env["r_foot"].Shape.BoundBox
    toe = world(V(lf.XMax, lf.Center.y, lf.Center.z))
    heel = world(V(lf.XMin, lf.Center.y, lf.Center.z))
    faces_front = toe.y < heel.y - 1.0 and abs(toe.x - heel.x) < TOL_MM
    left_to_x = world(lf.Center).x > world(rf.Center).x
    z_lo = min(o.Shape.BoundBox.ZMin for _, o in bodies)
    z_hi = max(o.Shape.BoundBox.ZMax for _, o in bodies)
    drawn = (z_hi - z_lo) / MM
    # every keep-out holds its segment at each joint's lower, middle and upper travel, in every combination
    import itertools
    poses = outside = 0
    for seg, obj in keepouts:
        chain = chains[seg]
        pts = env_shape[seg].copy().tessellate(2.0)[0] + [x.Point for x in env_shape[seg].Vertexes]
        pts = pts[::max(1, len(pts) // 150)]
        levels = [(j["lo"], (j["lo"] + j["hi"]) / 2, j["hi"]) for j in chain]
        for angles in itertools.product(*levels):
            poses += 1
            for q in pose_points(pts, chain, angles):
                if not obj.Shape.isInside(q, 0.01, True):
                    outside += 1
    n_poses = sum(3 ** len(chains[seg]) for seg, _ in keepouts)
    keep_valid = all(o.Shape.isValid() and o.Shape.Volume > 0 for _, o in keepouts)
    # every module keep-out: centre on its joint's origin, axis on its joint's,
    # radius and volume those of the datasheet's cylinder
    import math
    bad_mod = 0
    for jn, obj in modules:
        _, od, th = JOINT_MODULES[jn]
        s = obj.Shape
        c = s.CenterOfMass
        cyl = [f for f in s.Faces if isinstance(f.Surface, Part.Cylinder)][0].Surface
        if (not s.isValid()
                or max(abs(g - w) for g, w in zip((c.x, c.y, c.z), origins[jn])) > TOL_MM
                or abs(abs(cyl.Axis.dot(V(*axes[jn]))) - 1.0) > 1e-9
                or abs(cyl.Radius - od / 2) > TOL_MM
                or abs(s.Volume - math.pi * (od / 2) ** 2 * th) > 1e-6 * s.Volume):
            bad_mod += 1
    # every module keep-out names the module actuator_sizing.py declares at
    # that joint, at its sheet's size
    bad_decl = 0
    for jn, (model, od, th) in JOINT_MODULES.items():
        row = asz.module(jn[2:] if jn[:2] in ("l_", "r_") else jn)
        if model != "%s %s" % row[:2] or (od, th) != tuple(float(v) for v in row[6].split(" x ")):
            bad_decl += 1
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
        ("faces FreeCAD Front -Y", faces_front, True, faces_front),
        ("left side toward +X", left_to_x, True, left_to_x),
        ("swept keep-outs", len(keepouts), 16, len(keepouts) == 16),
        ("keep-outs valid", keep_valid, True, keep_valid),
        ("poses checked", poses, n_poses, poses == n_poses > 0),
        ("points outside keep-out", outside, 0, outside == 0),
        ("module keep-outs", len(modules), len(JOINT_MODULES), len(modules) == len(JOINT_MODULES) == 5),
        ("modules on joint axis", bad_mod == 0, True, bad_mod == 0),
        ("modules = spec 02.6", bad_decl == 0, True, bad_decl == 0),
    ]
    ok = True
    print("gems-skeleton — CAD skeleton, generated from hardware/kinematics.md via generate_urdf.py")
    print("=" * 72)
    for name, got, want, passed in checks:
        print("  %-24s %-10s expected %-10s %s" % (name, got, want, "ok" if passed else "MISMATCH"))
        ok = ok and passed
    if ok and mode == "write":
        export_step(markers + bodies + keepouts + modules, root.Placement, out)
        # read the written file back: its geometry, not the document's, is what leaves
        step_front = step_faces_front(out)
        print("  %-24s %-10s expected %-10s %s" % ("STEP faces Front -Y", step_front, True,
                                                   "ok" if step_front else "MISMATCH"))
        ok = ok and step_front
        if ok:
            set_step_header(out)
            print("Wrote %s — %d joint frames, %d segment envelopes, %d swept keep-outs, %d module keep-outs."
                  % (out, len(markers), len(bodies), len(keepouts), len(modules)))
            if fcstd:
                doc.saveAs(fcstd)
                print("Saved %s" % fcstd)
        else:
            pathlib.Path(out).unlink()
    print("SKELETON_AUDIT %s" % ("PASS" if ok else "FAIL"))


def export_step(objects, placement, out):
    """Write the STEP with the container's turn applied to the geometry itself.
    Exported as an App::Part, FreeCAD 1.1 drops the container's placement, so
    the shapes are turned and written flat, from a document of their own so
    that each keeps its name."""
    import FreeCAD as App
    import Import
    m = placement.toMatrix()
    tmp = App.newDocument("gems_skeleton_export")
    try:
        flat = []
        for name, obj in objects:
            o = tmp.addObject("Part::Feature", obj.Name)
            o.Shape = obj.Shape.transformGeometry(m)
            o.Label = obj.Name
            flat.append(o)
        tmp.recompute()
        Import.export(flat, str(out))
    finally:
        App.closeDocument(tmp.Name)


def step_faces_front(path):
    """Does the written STEP put the toes of the left foot toward -Y and the
    left foot on the +X side?"""
    import FreeCAD as App
    import Import
    d = App.newDocument("gems_skeleton_readback")
    try:
        Import.insert(str(path), d.Name)
        bb = {}
        for o in d.Objects:
            if o.Label in ("env_l_foot", "env_r_foot") and hasattr(o, "Shape"):
                s = o.Shape.copy()
                s.Placement = o.getGlobalPlacement()
                bb[o.Label] = s.BoundBox
        if len(bb) != 2:
            return False
        lf, rf = bb["env_l_foot"], bb["env_r_foot"]
        return lf.YLength > lf.XLength and lf.Center.x > rf.Center.x
    finally:
        App.closeDocument(d.Name)


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
