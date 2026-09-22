#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Generate a URDF for the GEMs body from the declared kinematic configuration.

Source of truth: hardware/kinematics.md. This script encodes that declaration
and nothing else — 30 core degrees of freedom, the declared segment lengths,
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
  * Joint limits are human ranges of motion, not mechanism travel.

The model is therefore good for reach, workspace, gait topology and controller
bring-up, and not good for anything that depends on true inertia — impact,
precise torque prediction, energy-per-step. Those wait for the mechanical
design, which is what §4 of the declaration lists as open.
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# -- declared in hardware/kinematics.md §2 ---------------------------------

SEG = {
    "pelvis":    dict(kind="box", w=0.30, d=0.18, h=0.16),
    "torso":     dict(kind="box", w=0.34, d=0.21, h=0.46),
    "head":      dict(kind="box", w=0.16, d=0.19, h=0.22),
    "upper_arm": dict(kind="cyl", r=0.048, h=0.32),   # declared 0.32
    "forearm":   dict(kind="cyl", r=0.040, h=0.26),   # declared 0.26
    "hand":      dict(kind="box", w=0.09, d=0.04, h=0.12),
    "thigh":     dict(kind="cyl", r=0.062, h=0.42),   # declared 0.42
    "shank":     dict(kind="cyl", r=0.050, h=0.42),   # declared 0.42
    "foot":      dict(kind="box", w=0.10, d=0.26, h=0.07),
}
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

# Human ranges of motion, radians. Mechanism travel is IMPL.
LIM = {
    "hip_roll": (-0.79, 0.52), "hip_pitch": (-2.09, 0.52), "hip_yaw": (-0.79, 0.79),
    "knee": (0.0, 2.44), "ankle_pitch": (-0.87, 0.52), "ankle_roll": (-0.35, 0.35),
    "shoulder_pitch": (-3.14, 1.05), "shoulder_roll": (-0.35, 3.14),
    "shoulder_yaw": (-1.57, 1.57), "elbow": (0.0, 2.62),
    "wrist_yaw": (-1.57, 1.57), "wrist_pitch": (-1.22, 1.22),
    "wrist_roll": (-1.57, 1.57),
    "waist_yaw": (-0.79, 0.79), "waist_pitch": (-0.52, 1.05),
    "neck_yaw": (-1.31, 1.31), "neck_pitch": (-0.70, 0.70),
}
EFFORT, VELOCITY = 200.0, 8.0


def inertia(seg, m):
    """Solid primitive. Real segments are shells; this overstates nothing
    systematically but is an estimate either way."""
    if seg["kind"] == "cyl":
        r, h = seg["r"], seg["h"]
        ix = iy = m * (3 * r * r + h * h) / 12.0
        iz = m * r * r / 2.0
    else:
        w, d, h = seg["w"], seg["d"], seg["h"]
        ix = m * (d * d + h * h) / 12.0
        iy = m * (w * w + h * h) / 12.0
        iz = m * (w * w + d * d) / 12.0
    return ix, iy, iz


def seg_length(name):
    s = SEG[name]
    return s["h"]


def add_link(robot, name, seg_name, mass):
    s = SEG[seg_name]
    link = ET.SubElement(robot, "link", name=name)
    ix, iy, iz = inertia(s, mass)
    inert = ET.SubElement(link, "inertial")
    ET.SubElement(inert, "origin", xyz="0 0 %.4f" % (-s["h"] / 2.0), rpy="0 0 0")
    ET.SubElement(inert, "mass", value="%.4f" % mass)
    ET.SubElement(inert, "inertia", ixx="%.6f" % ix, iyy="%.6f" % iy,
                  izz="%.6f" % iz, ixy="0", ixz="0", iyz="0")
    for tag in ("visual", "collision"):
        el = ET.SubElement(link, tag)
        ET.SubElement(el, "origin", xyz="0 0 %.4f" % (-s["h"] / 2.0), rpy="0 0 0")
        geo = ET.SubElement(el, "geometry")
        if s["kind"] == "cyl":
            ET.SubElement(geo, "cylinder", radius="%.4f" % s["r"], length="%.4f" % s["h"])
        else:
            ET.SubElement(geo, "box", size="%.4f %.4f %.4f" % (s["w"], s["d"], s["h"]))
    return link


def add_joint(robot, name, parent, child, xyz, axis, kind="revolute"):
    j = ET.SubElement(robot, "joint", name=name, type=kind)
    ET.SubElement(j, "parent", link=parent)
    ET.SubElement(j, "child", link=child)
    ET.SubElement(j, "origin", xyz=xyz, rpy="0 0 0")
    ET.SubElement(j, "axis", xyz=axis)
    base = name.split("_", 1)[1] if name[:2] in ("l_", "r_") else name
    lo, hi = LIM[base]
    ET.SubElement(j, "limit", lower="%.4f" % lo, upper="%.4f" % hi,
                  effort="%.1f" % EFFORT, velocity="%.1f" % VELOCITY)
    return j


X, Y, Z = "1 0 0", "0 1 0", "0 0 1"


def build(total_mass):
    masses = {k: total_mass * f for k, f in MASS_FRAC.items()}

    robot = ET.Element("robot", name="gems")
    robot.append(ET.Comment(
        " Generated by hardware/sim-model/generate_urdf.py from the declared "
        "kinematic configuration in hardware/kinematics.md. Do not hand-edit. "
        "Masses are anthropometric estimates; inertias are solid primitives; "
        "joint limits are human ranges of motion. None is derived from a "
        "mechanical design, because none exists yet. "))

    add_link(robot, "pelvis", "pelvis", masses["pelvis"])

    # waist 2 + torso
    add_link(robot, "waist_yaw_link", "pelvis", 1e-3)
    add_joint(robot, "waist_yaw", "pelvis", "waist_yaw_link", "0 0 0", Z)
    add_link(robot, "torso", "torso", masses["torso"])
    add_joint(robot, "waist_pitch", "waist_yaw_link", "torso", "0 0 0", Y)

    th = seg_length("torso")

    # neck 2 + head
    add_link(robot, "neck_yaw_link", "head", 1e-3)
    add_joint(robot, "neck_yaw", "torso", "neck_yaw_link", "0 0 %.4f" % th, Z)
    add_link(robot, "head", "head", masses["head"])
    add_joint(robot, "neck_pitch", "neck_yaw_link", "head", "0 0 0", Y)

    for side, sgn in (("l", 1.0), ("r", -1.0)):
        p = side + "_"
        sy = sgn * SHOULDER_WIDTH / 2.0

        # arm: 7 DOF
        add_link(robot, p + "shoulder_pitch_link", "upper_arm", 1e-3)
        add_joint(robot, p + "shoulder_pitch", "torso", p + "shoulder_pitch_link",
                  "0 %.4f %.4f" % (sy, th), Y)
        add_link(robot, p + "shoulder_roll_link", "upper_arm", 1e-3)
        add_joint(robot, p + "shoulder_roll", p + "shoulder_pitch_link",
                  p + "shoulder_roll_link", "0 0 0", X)
        add_link(robot, p + "upper_arm", "upper_arm", masses["upper_arm"])
        add_joint(robot, p + "shoulder_yaw", p + "shoulder_roll_link",
                  p + "upper_arm", "0 0 0", Z)
        add_link(robot, p + "forearm", "forearm", masses["forearm"])
        add_joint(robot, p + "elbow", p + "upper_arm", p + "forearm",
                  "0 0 %.4f" % -seg_length("upper_arm"), Y)
        add_link(robot, p + "wrist_yaw_link", "hand", 1e-3)
        add_joint(robot, p + "wrist_yaw", p + "forearm", p + "wrist_yaw_link",
                  "0 0 %.4f" % -seg_length("forearm"), Z)
        add_link(robot, p + "wrist_pitch_link", "hand", 1e-3)
        add_joint(robot, p + "wrist_pitch", p + "wrist_yaw_link",
                  p + "wrist_pitch_link", "0 0 0", Y)
        add_link(robot, p + "hand", "hand", masses["hand"])
        add_joint(robot, p + "wrist_roll", p + "wrist_pitch_link", p + "hand",
                  "0 0 0", X)

        # leg: 6 DOF
        hy = sgn * HIP_WIDTH / 2.0
        add_link(robot, p + "hip_roll_link", "thigh", 1e-3)
        add_joint(robot, p + "hip_roll", "pelvis", p + "hip_roll_link",
                  "0 %.4f %.4f" % (hy, -seg_length("pelvis")), X)
        add_link(robot, p + "hip_pitch_link", "thigh", 1e-3)
        add_joint(robot, p + "hip_pitch", p + "hip_roll_link",
                  p + "hip_pitch_link", "0 0 0", Y)
        add_link(robot, p + "thigh", "thigh", masses["thigh"])
        add_joint(robot, p + "hip_yaw", p + "hip_pitch_link", p + "thigh",
                  "0 0 0", Z)
        add_link(robot, p + "shank", "shank", masses["shank"])
        add_joint(robot, p + "knee", p + "thigh", p + "shank",
                  "0 0 %.4f" % -seg_length("thigh"), Y)
        add_link(robot, p + "ankle_pitch_link", "foot", 1e-3)
        add_joint(robot, p + "ankle_pitch", p + "shank", p + "ankle_pitch_link",
                  "0 0 %.4f" % -seg_length("shank"), Y)
        add_link(robot, p + "foot", "foot", masses["foot"])
        add_joint(robot, p + "ankle_roll", p + "ankle_pitch_link", p + "foot",
                  "0 0 0", X)

    return robot


def audit(robot, total_mass):
    """Check the model against the declaration it was generated from."""
    joints = robot.findall("joint")
    dof = [j for j in joints if j.get("type") in ("revolute", "continuous",
                                                  "prismatic")]
    mass = sum(float(m.get("value"))
               for m in robot.iter("mass"))
    reach = (seg_length("upper_arm") + seg_length("forearm")
             + seg_length("hand"))
    height = (seg_length("foot") + seg_length("shank") + seg_length("thigh")
              + seg_length("pelvis") + seg_length("torso") + seg_length("head"))

    checks = [
        ("core DOF", len(dof), 30, len(dof) == 30),
        ("total mass kg", round(mass, 1), total_mass,
         abs(mass - total_mass) < 0.5),
        ("reach m", round(reach, 3), DECLARED_REACH,
         abs(reach - DECLARED_REACH) < 0.005),
        ("standing height m", round(height, 3), DECLARED_HEIGHT,
         abs(height - DECLARED_HEIGHT) < 0.02),
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
