#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Actuator sizing for the declared kinematic configuration.

Sizes every joint from its peak torque requirement, sums the actuator mass, and
reports the resulting `f_act` against the range spec 02.2 assumes.

    python hardware/electrical/actuator_sizing.py
    python hardware/electrical/actuator_sizing.py --mass 95

Torque requirements are scaled from published gait and task data; arm joints
are sized from the declared payload at the grip centre with the arm's own
weight added; see hardware/electrical/README.md for each source. Torque densities are published
figures for real actuator modules, and they differ by a factor of four
depending on whether the number counts the motor or the whole actuator — which
is the point of the table this prints.
"""

from __future__ import annotations

import argparse
import sys

G = 9.81
REF_MASS = 130.0          # the 4-hour operating point of spec 02.5
FLOOR_DENSITY = 80.0      # floor of the band spec 02.6 declares, Nm/kg

# Arm geometry, hardware/kinematics.md §2. Levers are horizontal distances from
# the joint axis with the arm held straight out, the posture of maximum
# gravitational moment.
UPPER_ARM = 0.32          # shoulder to elbow
FOREARM = 0.26            # elbow to wrist
WRIST_TO_GRIP = 0.06      # wrist to the centre of a held object, assumed ⟦IMPL⟧
SHOULDER_TO_GRIP = UPPER_ARM + FOREARM + WRIST_TO_GRIP   # 0.64 m
ELBOW_TO_GRIP = FOREARM + WRIST_TO_GRIP                  # 0.32 m

# Arm payload, decided 2026-09-26 (README §6b): 15 kg in one hand, arm
# horizontal, load at the grip centre. Shoulder roll carries the same posture
# abducted, at 11 kg.
PAYLOAD_KG = 15.0
PAYLOAD_ROLL_KG = 11.0

# Arm self-weight. Joint modules are weighed at the floor density from the
# torque this table gives them; structure and hand are allowances until CAD
# exists (⟦IMPL⟧). Positions are along the straight arm from the shoulder.
ARM_STRUCTURE = [
    # (name, mass kg, distance from shoulder m)
    ("upper arm structure", 0.8, UPPER_ARM / 2),
    ("forearm structure",   0.6, UPPER_ARM + FOREARM / 2),
    ("hand",                0.6, SHOULDER_TO_GRIP),
]
SHOULDER_YAW_POS = UPPER_ARM / 2     # yaw module sits in the upper arm
WRIST_POS = UPPER_ARM + FOREARM      # three wrist modules at the wrist

# Per-joint peak torque. Leg and trunk figures scale with body mass; arm
# figures follow from the payload and the arm's own weight; the rest are fixed.
# Sources are listed per row in README.md.
JOINTS = [
    # (name, count, basis, value)
    ("hip_pitch",      2, "per_kg", 1.77),   # 230 Nm at 130 kg, scaled from 100-150 Nm at 70 kg
    ("hip_roll",       2, "per_kg", 1.23),
    ("hip_yaw",        2, "per_kg", 0.62),
    ("knee",           2, "per_kg", 1.77),
    ("ankle_pitch",    2, "per_kg", 1.40),   # sourced: 1.4 Nm/kg at push-off
    ("ankle_roll",     2, "per_kg", 0.54),
    # Trunk: human isometric peak, normalised to body weight, male medians
    # (Pan et al. 2025, README ref 14): extension 1.74, lateral bending 0.95
    # (left, the larger side), axial rotation 0.74 Nm/kg. Adopted 2026-09-26
    # (README §6a, option B); the roll axis is decision D-9.
    ("trunk_pitch",    1, "per_kg", 1.74),   # sourced: extension
    ("trunk_roll",     1, "per_kg", 0.95),   # sourced: lateral bending
    ("trunk_yaw",      1, "per_kg", 0.74),   # sourced: axial rotation
    ("shoulder_pitch", 2, "arm",    ("shoulder", PAYLOAD_KG)),
    ("shoulder_roll",  2, "arm",    ("shoulder", PAYLOAD_ROLL_KG)),
    ("shoulder_yaw",   2, "fixed",  60.0),
    ("elbow",          2, "arm",    ("elbow", PAYLOAD_KG)),
    ("wrist_yaw",      2, "fixed",  20.0),
    ("wrist_pitch",    2, "fixed",  20.0),
    ("wrist_roll",     2, "fixed",  20.0),
    ("neck_yaw",       1, "fixed",  15.0),
    ("neck_pitch",     1, "fixed",  15.0),
]

# Published torque densities, peak torque per actuator kilogram.
DENSITIES = [
    (22.0,  "integrated state of the art, whole-actuator"),
    (33.0,  "what spec 02.6 used before 2026-09-22"),
    (36.0,  "top of the superseded range"),
    (52.0,  "commercial QDD module, 8:1 planetary"),
    (75.0,  "floor of the band before 2026-09-26"),
    (80.0,  "floor of the band spec 02.6 now declares"),
    (88.7,  "commercial hollow-shaft planetary module, peak"),
]


def _fixed(name):
    return next(v for n, _, b, v in JOINTS if n == name and b == "fixed")


def arm_torques(density=FLOOR_DENSITY):
    """Peak torque at elbow and shoulder, arm horizontal, load at grip centre.

    Returns {"elbow": (payload Nm, self-weight Nm), "shoulder": (...),
    "shoulder_roll": (...)}. Self-weight counts the joint modules distal to
    the joint, weighed at `density` from their own torque here, plus the
    structure and hand allowances of ARM_STRUCTURE.
    """
    wrist_kg = 3 * _fixed("wrist_yaw") / density
    yaw_kg = _fixed("shoulder_yaw") / density

    # elbow: everything beyond it, measured from the elbow
    e_self = wrist_kg * G * (WRIST_POS - UPPER_ARM)
    for name, m, x in ARM_STRUCTURE:
        if x > UPPER_ARM:
            e_self += m * G * (x - UPPER_ARM)
    e_pay = PAYLOAD_KG * G * ELBOW_TO_GRIP
    elbow_kg = (e_pay + e_self) / density

    # shoulder: everything beyond it, measured from the shoulder
    s_self = (yaw_kg * G * SHOULDER_YAW_POS
              + elbow_kg * G * UPPER_ARM
              + wrist_kg * G * WRIST_POS
              + sum(m * G * x for _, m, x in ARM_STRUCTURE))
    return {
        "elbow": (e_pay, e_self),
        "shoulder": (PAYLOAD_KG * G * SHOULDER_TO_GRIP, s_self),
        "shoulder_roll": (PAYLOAD_ROLL_KG * G * SHOULDER_TO_GRIP, s_self),
    }


def torque_table(body_mass, density=FLOOR_DENSITY):
    arms = arm_torques(density)
    rows = []
    for name, n, basis, val in JOINTS:
        if basis == "per_kg":
            t = val * body_mass
        elif basis == "arm":
            joint, load = val
            key = "shoulder_roll" if load == PAYLOAD_ROLL_KG and joint == "shoulder" else joint
            t = sum(arms[key])
        else:
            t = val
        rows.append((name, n, t, n * t))
    return rows


def split(body_mass=REF_MASS, density=FLOOR_DENSITY):
    """The summed torque in two parts: the part that scales with body mass,
    as Nm per kg of body, and the part that does not, in Nm.

    Legs and trunk are per-kg. Arms, wrists and neck are fixed by payload and
    geometry, so their actuator mass is non-scaling and belongs in m_ext of
    the mass loop (spec 02.1), not in f_act.
    """
    basis = {name: b for name, _, b, _ in JOINTS}
    per_kg = sum(n * v for _, n, b, v in JOINTS if b == "per_kg")
    fixed = sum(tot for name, _, _, tot in torque_table(body_mass, density)
                if basis[name] != "per_kg")
    return per_kg, fixed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--mass", type=float, default=REF_MASS,
                    help="body mass in kg (default: the 4-hour point)")
    a = ap.parse_args(argv)

    rows = torque_table(a.mass)
    total_nm = sum(r[3] for r in rows)
    n_joints = sum(r[1] for r in rows)

    print("Actuator sizing — %d joints, body mass %.0f kg" % (n_joints, a.mass))
    print("=" * 66)
    print("  %-16s %3s %10s %12s" % ("joint", "n", "peak Nm", "total Nm"))
    for name, n, t, tot in rows:
        print("  %-16s %3d %10.0f %12.0f" % (name, n, t, tot))
    print("  %-16s %3d %10s %12.0f" % ("TOTAL", n_joints, "", total_nm))

    per_kg, fixed = split(a.mass)
    print()
    print("Split: %.2f Nm per kg of body (legs, trunk) = %.0f Nm at %.0f kg;"
          % (per_kg, per_kg * a.mass, a.mass))
    print("       %.0f Nm fixed (arms, wrists, neck) -> %.1f kg of actuator at %.0f Nm/kg,"
          % (fixed, fixed / FLOOR_DENSITY, FLOOR_DENSITY))
    print("       non-scaling mass, m_ext in the loop of spec 02.1.")
    arms = arm_torques()
    print()
    print("Arm sizing: %.0f kg at the grip centre, %.2f m from the shoulder, arm horizontal"
          % (PAYLOAD_KG, SHOULDER_TO_GRIP))
    for k, label in (("shoulder", "shoulder pitch"), ("shoulder_roll", "shoulder roll (%.0f kg)" % PAYLOAD_ROLL_KG), ("elbow", "elbow")):
        pay, own = arms[k]
        print("  %-22s payload %5.1f Nm + self-weight %4.1f Nm = %5.1f Nm"
              % (label, pay, own, pay + own))

    print()
    print("Actuator mass and f_act at published torque densities")
    print("=" * 66)
    print("  %8s  %9s  %7s  %-28s" % ("Nm/kg", "mass kg", "f_act", "source"))
    band_lo, band_hi = 0.25, 0.35
    ok_any = False
    for d, label in DENSITIES:
        m = total_nm / d
        f = m / a.mass
        inrange = band_lo <= f <= band_hi
        ok_any = ok_any or inrange
        print("  %8.1f  %9.1f  %7.2f  %-28s %s"
              % (d, m, f, label, "in range" if inrange else ""))

    print()
    print("spec 02.2 assumes f_act in %.2f-%.2f (scaling part + fixed part / body)." % (band_lo, band_hi))
    if not ok_any:
        print("NO published density puts f_act inside that range.")
        return 1
    need = total_nm / (band_hi * a.mass)
    print("The arithmetic alone would allow %.0f Nm/kg." % need)
    print("spec 02.6 declares 80-90 Nm/kg peak over module mass: the floor was kept")
    print("at 80 when the arm payload came down (README §6b), as margin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
