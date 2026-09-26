#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Generate a URDF for the GEMs body from the declared kinematic configuration.

Source of truth: hardware/kinematics.md. This script encodes that declaration
and nothing else — 31 core degrees of freedom, the declared segment lengths,
and a mass model. Change the declaration, regenerate, do not hand-edit the URDF.

    python hardware/sim-model/generate_urdf.py            # write gems.urdf
    python hardware/sim-model/generate_urdf.py --mass 95  # a lighter point
    python hardware/sim-model/generate_urdf.py --check    # validate, write nothing

WHAT IS ESTIMATED HERE, AND IT IS MOST OF IT
--------------------------------------------
No mechanical design exists yet, so nothing below is derived from one.

  * Segment masses come from anthropometric fractions for a human of the same
    height. A robot is not a human: actuators concentrate mass at the joints
    and the battery sits in the torso, so the real distribution will differ,
    and the torso fraction in particular is understated here.
  * Inertia tensors are computed from solid geometric primitives — cylinders
    for limbs, boxes for torso, pelvis, head and feet. Real segments are
    shells around voids.
  * Joint limits are targets for mechanical travel (kinematics §1.5), with the
    human range of motion as the soft limit. Neither is mechanism travel yet.

The model is therefore good for reach, workspace, gait topology and controller
bring-up, and not good for anything that depends on true inertia — impact,
precise torque prediction, energy-per-step. Those wait for the mechanical
design, which is what §4 of the declaration lists as open.
"""

from __future__ import annotations

import argparse
import math
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# -- declared in hardware/kinematics.md §2 ---------------------------------
# URDF axes: x forward, y left, z up. For boxes, w is lateral (y), d is
# fore-aft (x), h is along the segment (z). Segments hang below their joint
# unless listed in UPWARD.

SEG = {
    "pelvis":    dict(kind="box", w=0.30, d=0.18, h=0.16),
    # The trunk (0.46 m) is three coupled segments (kinematics §1.4, plan D-9):
    # lumbar, lower thoracic, and the upper thorax that carries the shoulders,
    # the neck and the battery pack.
    "spine_lumbar":   dict(kind="box", w=0.34, d=0.21, h=0.12),
    "spine_thoracic": dict(kind="box", w=0.34, d=0.21, h=0.12),
    "torso":          dict(kind="box", w=0.34, d=0.21, h=0.22),
    "head":      dict(kind="box", w=0.16, d=0.19, h=0.22),
    "upper_arm": dict(kind="cyl", r=0.048, h=0.32),   # declared 0.32
    "forearm":   dict(kind="cyl", r=0.040, h=0.26),   # declared 0.26
    "hand":      dict(kind="box", w=0.04, d=0.09, h=0.12),   # palm faces the thigh
    "thigh":     dict(kind="cyl", r=0.062, h=0.42),   # declared 0.42
    "shank":     dict(kind="cyl", r=0.050, h=0.42),   # declared 0.42
    "foot":      dict(kind="box", w=0.10, d=0.26, h=0.07),
}
UPWARD = {"spine_lumbar", "spine_thoracic", "torso", "head"}
TRUNK = ("spine_lumbar", "spine_thoracic", "torso")
TRUNK_HEIGHT = sum(SEG[k]["h"] for k in TRUNK)
SHOULDER_WIDTH = 0.40       # declared
HIP_WIDTH = 0.18
DECLARED_REACH = 0.70       # declared: shoulder to fingertip
DECLARED_HEIGHT = 1.75

# Winter's anthropometric segment mass fractions. Sum to 1.0 over the body.
MASS_FRAC = {
    "pelvis": 0.142, "torso": 0.355, "head": 0.081,
    "upper_arm": 0.028, "forearm": 0.016, "hand": 0.006,
    "thigh": 0.100, "shank": 0.0465, "foot": 0.0145,
}
PAIRED = {"upper_arm", "forearm", "hand", "thigh", "shank", "foot"}

# Two tiers of joint limit (kinematics §1.5). LIM is the human range of
# motion: written as the soft limit (<safety_controller>), a profile the
# operator may choose. MECH is the mechanical travel the design targets:
# written as <limit>, and at least as wide as LIM everywhere. Joints absent
# from MECH have mechanical travel equal to the human range until the
# mechanical design says otherwise.
# Signs are for the left side under the right-hand rule about each joint's
# axis: pitch about +y, so flexion that carries a limb forward is negative;
# roll about +x, so abduction of a left limb is positive. Right-side roll and
# yaw limits are mirrored in add_joint. Trunk limits are totals across its
# three segments.
LIM = {
    "hip_roll": (-0.52, 0.79), "hip_pitch": (-2.09, 0.52), "hip_yaw": (-0.79, 0.79),
    "knee": (0.0, 2.44), "ankle_pitch": (-0.52, 0.87), "ankle_roll": (-0.35, 0.35),
    "shoulder_pitch": (-3.14, 1.05), "shoulder_roll": (-0.35, 3.14),
    "shoulder_yaw": (-1.57, 1.57), "elbow": (-2.62, 0.0),
    "wrist_yaw": (-1.57, 1.57), "wrist_pitch": (-1.22, 1.22),
    "wrist_roll": (-1.57, 1.57),
    "trunk_yaw": (-0.79, 0.79), "trunk_pitch": (-0.52, 1.05),
    "trunk_roll": (-0.52, 0.52),
    "neck_yaw": (-1.31, 1.31), "neck_pitch": (-0.70, 0.70),
}
MECH = {
    "shoulder_pitch": (-3.14, 1.22),    # 250 deg
    "shoulder_roll": (-0.70, 3.14),     # 220 deg
    "elbow": (-2.62, 0.87),             # 200 deg: 50 deg past straight
    "hip_pitch": (-2.09, 1.57),         # 210 deg: 90 deg of extension
    "knee": (-1.05, 2.44),              # 200 deg: 60 deg past straight; lock at 0
    "trunk_yaw": (-1.57, 1.57),         # 180 deg, spread over three segments
    "trunk_roll": (-0.79, 0.79),        # 90 deg, provisional
}
SOFT_K_POSITION, SOFT_K_VELOCITY = 100.0, 1.5   # placeholders; the profile is CTRL
EFFORT, VELOCITY = 200.0, 8.0

# Display colours, RGB. Left limbs warm, right limbs cool, so the sides can be
# told apart at a glance; along each limb the shade alternates so adjacent
# segments never share a colour. Axial segments are neutral.
AXIAL_RGB = {"pelvis": (0.25, 0.25, 0.28), "spine_lumbar": (0.33, 0.36, 0.42),
             "spine_thoracic": (0.46, 0.50, 0.58), "torso": (0.40, 0.44, 0.52),
             "head": (0.80, 0.80, 0.82)}
LIMB_SHADE = {"upper_arm": 0, "forearm": 1, "hand": 2,
              "thigh": 0, "shank": 1, "foot": 2}
SIDE_RGB = {
    "l": ((0.90, 0.55, 0.20), (0.96, 0.80, 0.50), (0.65, 0.33, 0.10)),
    "r": ((0.20, 0.58, 0.75), (0.58, 0.82, 0.92), (0.10, 0.38, 0.55)),
}


def colour(link_name, seg_name):
    if seg_name in AXIAL_RGB:
        return AXIAL_RGB[seg_name]
    return SIDE_RGB[link_name[0]][LIMB_SHADE[seg_name]]


def inertia(seg, m):
    """Solid primitive. Real segments are shells; this overstates nothing
    systematically but is an estimate either way."""
    if seg["kind"] == "cyl":
        r, h = seg["r"], seg["h"]
        ix = iy = m * (3 * r * r + h * h) / 12.0
        iz = m * r * r / 2.0
    else:
        w, d, h = seg["w"], seg["d"], seg["h"]
        ix = m * (w * w + h * h) / 12.0
        iy = m * (d * d + h * h) / 12.0
        iz = m * (w * w + d * d) / 12.0
    return ix, iy, iz


def seg_length(name):
    s = SEG[name]
    return s["h"]


DUMMY_MASS = 1e-3
DUMMY_INERTIA = 1e-6


def seg_centre_z(seg_name):
    h = SEG[seg_name]["h"]
    return h / 2.0 if seg_name in UPWARD else -h / 2.0


def add_link(robot, name, seg_name, mass):
    s = SEG[seg_name]
    link = ET.SubElement(robot, "link", name=name)
    ix, iy, iz = inertia(s, mass)
    cz = "0 0 %.4f" % seg_centre_z(seg_name)
    inert = ET.SubElement(link, "inertial")
    ET.SubElement(inert, "origin", xyz=cz, rpy="0 0 0")
    ET.SubElement(inert, "mass", value="%.4f" % mass)
    ET.SubElement(inert, "inertia", ixx="%.6f" % ix, iyy="%.6f" % iy,
                  izz="%.6f" % iz, ixy="0", ixz="0", iyz="0")
    for tag in ("visual", "collision"):
        el = ET.SubElement(link, tag)
        ET.SubElement(el, "origin", xyz=cz, rpy="0 0 0")
        geo = ET.SubElement(el, "geometry")
        if s["kind"] == "cyl":
            ET.SubElement(geo, "cylinder", radius="%.4f" % s["r"], length="%.4f" % s["h"])
        else:
            ET.SubElement(geo, "box", size="%.4f %.4f %.4f" % (s["d"], s["w"], s["h"]))
        if tag == "visual":
            mat = ET.SubElement(el, "material", name=name)
            ET.SubElement(mat, "color", rgba="%.2f %.2f %.2f 1" % colour(name, seg_name))
    return link


def add_dummy(robot, name):
    """Intermediate link between two axes of one joint. It carries a gram and
    no geometry: drawing the next segment here would duplicate it."""
    link = ET.SubElement(robot, "link", name=name)
    inert = ET.SubElement(link, "inertial")
    ET.SubElement(inert, "origin", xyz="0 0 0", rpy="0 0 0")
    ET.SubElement(inert, "mass", value="%.4f" % DUMMY_MASS)
    ET.SubElement(inert, "inertia", ixx="%.6f" % DUMMY_INERTIA,
                  iyy="%.6f" % DUMMY_INERTIA, izz="%.6f" % DUMMY_INERTIA,
                  ixy="0", ixz="0", iyz="0")
    return link


def add_joint(robot, name, parent, child, xyz, axis, kind="revolute",
              limit_key=None, share=1.0, mimic=None):
    j = ET.SubElement(robot, "joint", name=name, type=kind)
    ET.SubElement(j, "parent", link=parent)
    ET.SubElement(j, "child", link=child)
    ET.SubElement(j, "origin", xyz=xyz, rpy="0 0 0")
    ET.SubElement(j, "axis", xyz=axis)
    base = limit_key or (name.split("_", 1)[1] if name[:2] in ("l_", "r_") else name)
    lo, hi = LIM[base]
    mlo, mhi = MECH.get(base, LIM[base])
    if name.startswith("r_") and axis != Y:
        lo, hi = -hi, -lo    # mirror roll and yaw across the sagittal plane
        mlo, mhi = -mhi, -mlo
    ET.SubElement(j, "limit", lower="%.4f" % (mlo * share), upper="%.4f" % (mhi * share),
                  effort="%.1f" % EFFORT, velocity="%.1f" % VELOCITY)
    ET.SubElement(j, "safety_controller", soft_lower_limit="%.4f" % (lo * share),
                  soft_upper_limit="%.4f" % (hi * share),
                  k_position="%.1f" % SOFT_K_POSITION, k_velocity="%.1f" % SOFT_K_VELOCITY)
    if mimic:
        ET.SubElement(j, "mimic", joint=mimic, multiplier="1", offset="0")
    return j


X, Y, Z = "1 0 0", "0 1 0", "0 0 1"


def build(total_mass):
    masses = {k: total_mass * f for k, f in MASS_FRAC.items()}
    trunk_mass = masses.pop("torso")
    for k in TRUNK:
        masses[k] = trunk_mass * SEG[k]["h"] / TRUNK_HEIGHT

    robot = ET.Element("robot", name="gems")
    robot.append(ET.Comment(
        " Generated by hardware/sim-model/generate_urdf.py from the declared "
        "kinematic configuration in hardware/kinematics.md. Do not hand-edit. "
        "Masses are anthropometric estimates; inertias are solid primitives; "
        "joint limits are design targets for mechanical travel, with the human "
        "range of motion as the soft limit. None is derived from a mechanical "
        "design, because none exists yet. "))

    add_link(robot, "pelvis", "pelvis", masses["pelvis"])

    # trunk: 3 axes, each spread over 3 coupled segments. The first segment's
    # joints are the actuated masters; the others follow through <mimic>.
    parent, z0 = "pelvis", 0.0
    share = 1.0 / len(TRUNK)
    for i, seg_name in enumerate(TRUNK, start=1):
        sfx = "" if i == 1 else "_%d" % i
        yaw_l, pitch_l = "trunk_yaw%s_link" % sfx, "trunk_pitch%s_link" % sfx
        add_dummy(robot, yaw_l)
        add_joint(robot, "trunk_yaw" + sfx, parent, yaw_l, "0 0 %.4f" % z0, Z,
                  limit_key="trunk_yaw", share=share, mimic=None if i == 1 else "trunk_yaw")
        add_dummy(robot, pitch_l)
        add_joint(robot, "trunk_pitch" + sfx, yaw_l, pitch_l, "0 0 0", Y,
                  limit_key="trunk_pitch", share=share, mimic=None if i == 1 else "trunk_pitch")
        add_link(robot, seg_name, seg_name, masses[seg_name])
        add_joint(robot, "trunk_roll" + sfx, pitch_l, seg_name, "0 0 0", X,
                  limit_key="trunk_roll", share=share, mimic=None if i == 1 else "trunk_roll")
        parent, z0 = seg_name, SEG[seg_name]["h"]

    th = seg_length("torso")

    # neck 2 + head
    add_dummy(robot, "neck_yaw_link")
    add_joint(robot, "neck_yaw", "torso", "neck_yaw_link", "0 0 %.4f" % th, Z)
    add_link(robot, "head", "head", masses["head"])
    add_joint(robot, "neck_pitch", "neck_yaw_link", "head", "0 0 0", Y)

    for side, sgn in (("l", 1.0), ("r", -1.0)):
        p = side + "_"
        sy = sgn * SHOULDER_WIDTH / 2.0

        # arm: 7 DOF
        add_dummy(robot, p + "shoulder_pitch_link")
        add_joint(robot, p + "shoulder_pitch", "torso", p + "shoulder_pitch_link",
                  "0 %.4f %.4f" % (sy, th), Y)
        add_dummy(robot, p + "shoulder_roll_link")
        add_joint(robot, p + "shoulder_roll", p + "shoulder_pitch_link",
                  p + "shoulder_roll_link", "0 0 0", X)
        add_link(robot, p + "upper_arm", "upper_arm", masses["upper_arm"])
        add_joint(robot, p + "shoulder_yaw", p + "shoulder_roll_link",
                  p + "upper_arm", "0 0 0", Z)
        add_link(robot, p + "forearm", "forearm", masses["forearm"])
        add_joint(robot, p + "elbow", p + "upper_arm", p + "forearm",
                  "0 0 %.4f" % -seg_length("upper_arm"), Y)
        add_dummy(robot, p + "wrist_yaw_link")
        add_joint(robot, p + "wrist_yaw", p + "forearm", p + "wrist_yaw_link",
                  "0 0 %.4f" % -seg_length("forearm"), Z)
        add_dummy(robot, p + "wrist_pitch_link")
        add_joint(robot, p + "wrist_pitch", p + "wrist_yaw_link",
                  p + "wrist_pitch_link", "0 0 0", Y)
        add_link(robot, p + "hand", "hand", masses["hand"])
        add_joint(robot, p + "wrist_roll", p + "wrist_pitch_link", p + "hand",
                  "0 0 0", X)

        # leg: 6 DOF
        hy = sgn * HIP_WIDTH / 2.0
        add_dummy(robot, p + "hip_roll_link")
        add_joint(robot, p + "hip_roll", "pelvis", p + "hip_roll_link",
                  "0 %.4f %.4f" % (hy, -seg_length("pelvis")), X)
        add_dummy(robot, p + "hip_pitch_link")
        add_joint(robot, p + "hip_pitch", p + "hip_roll_link",
                  p + "hip_pitch_link", "0 0 0", Y)
        add_link(robot, p + "thigh", "thigh", masses["thigh"])
        add_joint(robot, p + "hip_yaw", p + "hip_pitch_link", p + "thigh",
                  "0 0 0", Z)
        add_link(robot, p + "shank", "shank", masses["shank"])
        add_joint(robot, p + "knee", p + "thigh", p + "shank",
                  "0 0 %.4f" % -seg_length("thigh"), Y)
        add_dummy(robot, p + "ankle_pitch_link")
        add_joint(robot, p + "ankle_pitch", p + "shank", p + "ankle_pitch_link",
                  "0 0 %.4f" % -seg_length("shank"), Y)
        add_link(robot, p + "foot", "foot", masses["foot"])
        add_joint(robot, p + "ankle_roll", p + "ankle_pitch_link", p + "foot",
                  "0 0 0", X)

    return robot


def _xyz(el):
    return [float(v) for v in el.get("xyz").split()]


def geometry_extents(robot):
    """Axis-aligned extents of every visual in the zero pose, keyed by link.
    All joint and visual origins carry rpy="0 0 0", so a link's pose is the
    sum of the joint offsets down to it."""
    offset = {robot.find("link").get("name"): [0.0, 0.0, 0.0]}
    for j in robot.findall("joint"):
        parent = offset[j.find("parent").get("link")]
        offset[j.find("child").get("link")] = [
            a + b for a, b in zip(parent, _xyz(j.find("origin")))]
    ext = {}
    for link in robot.findall("link"):
        vis = link.find("visual")
        if vis is None:
            continue
        c = [a + b for a, b in zip(offset[link.get("name")],
                                   _xyz(vis.find("origin")))]
        g = vis.find("geometry")[0]
        if g.tag == "box":
            half = [float(v) / 2.0 for v in g.get("size").split()]
        else:
            r, h = float(g.get("radius")), float(g.get("length"))
            half = [r, r, h / 2.0]
        ext[link.get("name")] = [(ci - hi, ci + hi) for ci, hi in zip(c, half)]
    return ext


def _rot(axis, q):
    x, y, z = axis
    c, s, t = math.cos(q), math.sin(q), 1.0 - math.cos(q)
    return [[t*x*x + c,   t*x*y - s*z, t*x*z + s*y],
            [t*x*y + s*z, t*y*y + c,   t*y*z - s*x],
            [t*x*z - s*y, t*y*z + s*x, t*z*z + c]]


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def _apply(r, v):
    return [sum(r[i][k] * v[k] for k in range(3)) for i in range(3)]


def point_at(robot, q, link, local):
    """World position of a point fixed in `link`, with joints set per `q`
    (name -> angle, others at zero). The root sits at the origin."""
    pose = {robot.find("link").get("name"): ([0.0, 0.0, 0.0], _rot((0, 0, 1), 0))}
    for j in robot.findall("joint"):
        pp, pr = pose[j.find("parent").get("link")]
        o = _apply(pr, _xyz(j.find("origin")))
        axis = [float(v) for v in j.find("axis").get("xyz").split()]
        m = j.find("mimic")
        if m is not None:                 # a coupled joint follows its master
            angle = (float(m.get("multiplier")) * q.get(m.get("joint"), 0.0)
                     + float(m.get("offset")))
        else:
            angle = q.get(j.get("name"), 0.0)
        pose[j.find("child").get("link")] = (
            [a + b for a, b in zip(pp, o)], _mul(pr, _rot(axis, angle)))
    pp, pr = pose[link]
    return [a + b for a, b in zip(pp, _apply(pr, local))]


def joint_senses(robot):
    """Does each joint move the body the way its name says, on both sides?
    Each check drives one joint to the limit that should produce the motion
    and asks where a probe point ends up. The human asymmetries it checks are
    properties of the soft limits — the human profile — not of the mechanical
    travel, which is wider by design."""
    lim = {j.get("name"): (float(j.find("safety_controller").get("soft_lower_limit")),
                           float(j.find("safety_controller").get("soft_upper_limit")))
           for j in robot.findall("joint")}
    hand = (0.0, 0.0, -seg_length("hand"))
    toe = (SEG["foot"]["d"] / 2.0, 0.0, 0.0)
    ok = True
    for side, out in (("l", 1.0), ("r", -1.0)):
        p = side + "_"

        def moved(joint, bound, link, local, test):
            q = lim[p + joint][0 if bound == "lo" else 1]
            return test(point_at(robot, {p + joint: q}, link, local),
                        point_at(robot, {}, link, local))

        ok &= moved("shoulder_pitch", "lo", p + "hand", hand,
                    lambda a, z: a[2] > z[2] + 1.0)            # raises forward overhead
        ok &= point_at(robot, {p + "shoulder_pitch": -1.57},
                       p + "hand", hand)[0] > 0.5              # ... to the front
        ok &= moved("shoulder_roll", "hi" if out > 0 else "lo", p + "hand", hand,
                    lambda a, z: a[2] > z[2] + 1.0)            # abducts overhead
        ok &= out * point_at(robot, {p + "shoulder_roll": out * 1.57},
                             p + "hand", hand)[1] > 0.5        # ... outward
        ok &= moved("elbow", "lo", p + "hand", hand,
                    lambda a, z: a[0] > 0.1)                   # forearm comes forward
        ok &= moved("hip_pitch", "lo", p + "shank", (0, 0, 0),
                    lambda a, z: a[0] > 0.2
                    and a[2] > -seg_length("pelvis"))          # knee comes up to the hip
        ok &= moved("knee", "hi", p + "foot", (0, 0, 0),
                    lambda a, z: a[0] < -0.1)                  # shin folds back
        z0 = point_at(robot, {}, p + "foot", toe)[2]
        down, up = (point_at(robot, {p + "ankle_pitch": q}, p + "foot", toe)[2] - z0
                    for q in reversed(lim[p + "ankle_pitch"]))
        ok &= down < -up < 0          # toe drops further than it lifts: plantar > dorsi
        y0 = point_at(robot, {}, p + "shank", (0, 0, 0))[1]
        sway = [out * (point_at(robot, {p + "hip_roll": q}, p + "shank",
                                (0, 0, 0))[1] - y0)
                for q in lim[p + "hip_roll"]]
        ok &= max(sway) > -min(sway) > 0   # abducts outward further than it adducts
    return ok


def audit(robot, total_mass):
    """Check the model against the declaration it was generated from."""
    joints = robot.findall("joint")
    dof = [j for j in joints if j.get("type") in ("revolute", "continuous",
                                                  "prismatic")
           and j.find("mimic") is None]
    coupled = {}
    for j in joints:
        m = j.find("mimic")
        if m is not None:
            coupled.setdefault(m.get("joint"), []).append(j.get("name"))
    trunk_spread = all(len(coupled.get(a, [])) == len(TRUNK) - 1
                       for a in ("trunk_yaw", "trunk_pitch", "trunk_roll"))
    covers = all(float(j.find("limit").get("lower")) <= float(j.find("safety_controller").get("soft_lower_limit")) + 1e-9
                 and float(j.find("limit").get("upper")) >= float(j.find("safety_controller").get("soft_upper_limit")) - 1e-9
                 for j in joints)
    mass = sum(float(m.get("value"))
               for m in robot.iter("mass"))
    reach = (seg_length("upper_arm") + seg_length("forearm")
             + seg_length("hand"))
    height = (seg_length("foot") + seg_length("shank") + seg_length("thigh")
              + seg_length("pelvis") + TRUNK_HEIGHT + seg_length("head"))

    ext = geometry_extents(robot)
    drawn_height = (max(e[2][1] for e in ext.values())
                    - min(e[2][0] for e in ext.values()))
    foot = ext["l_foot"]
    foot_forward = (foot[0][1] - foot[0][0]) > (foot[1][1] - foot[1][0])
    torso_above_waist = ext["spine_lumbar"][2][0] >= -1e-9
    senses = joint_senses(robot)

    checks = [
        ("core DOF", len(dof), 31, len(dof) == 31),
        ("trunk spread 3 segs", trunk_spread, True, trunk_spread),
        ("mech covers soft", covers, True, covers),
        ("total mass kg", round(mass, 1), total_mass,
         abs(mass - total_mass) < 0.5),
        ("reach m", round(reach, 3), DECLARED_REACH,
         abs(reach - DECLARED_REACH) < 0.005),
        ("standing height m", round(height, 3), DECLARED_HEIGHT,
         abs(height - DECLARED_HEIGHT) < 0.02),
        ("drawn height m", round(drawn_height, 3), DECLARED_HEIGHT,
         abs(drawn_height - DECLARED_HEIGHT) < 0.02),
        ("drawn segments", len(ext), 17, len(ext) == 17),
        ("torso above waist", torso_above_waist, True, torso_above_waist),
        ("feet point forward", foot_forward, True, foot_forward),
        ("joints move as named", senses, True, senses),
    ]
    return checks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mass", type=float, default=130.0,
                    help="total body mass in kg (default: the 4-hour point)")
    ap.add_argument("--out", default=None, help="output path")
    ap.add_argument("--check", action="store_true",
                    help="audit against the declaration, write nothing")
    a = ap.parse_args(argv)

    robot = build(a.mass)
    checks = audit(robot, a.mass)

    print("gems.urdf — generated from hardware/kinematics.md")
    print("=" * 58)
    ok = True
    for name, got, want, passed in checks:
        print("  %-20s %-10s expected %-10s %s"
              % (name, got, want, "ok" if passed else "MISMATCH"))
        ok = ok and passed
    if not ok:
        print("\nThe model disagrees with the declaration. Fix one of them.")
        return 1
    if a.check:
        print("\nAudit only; nothing written.")
        return 0

    out = a.out or str(__import__("pathlib").Path(__file__).with_name("gems.urdf"))
    xml = minidom.parseString(ET.tostring(robot)).toprettyxml(indent="  ")
    xml = "\n".join(l for l in xml.split("\n") if l.strip())
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml + "\n")
    print("\nWrote %s — %d links, %d joints."
          % (out, len(robot.findall("link")), len(robot.findall("joint"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
