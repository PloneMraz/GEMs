#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Actuator sizing for the declared kinematic configuration.

Sizes every joint from its peak torque requirement, sums the actuator mass, and
reports the resulting `f_act` against the range spec 02.2 assumes.

    python hardware/electrical/actuator_sizing.py
    python hardware/electrical/actuator_sizing.py --mass 95

Torque requirements are scaled from published gait and task data; see
hardware/electrical/README.md for each source. Torque densities are published
figures for real actuator modules, and they differ by a factor of four
depending on whether the number counts the motor or the whole actuator — which
is the point of the table this prints.
"""

from __future__ import annotations

import argparse
import sys

G = 9.81
REF_MASS = 130.0          # the 4-hour operating point of spec 02.5
REACH = 0.70              # hardware/kinematics.md §2
FOREARM_REACH = 0.38      # elbow to grip centre

# Per-joint peak torque. Leg and trunk figures scale with body mass; arm
# figures scale with the payload the arm is required to hold at reach.
# Sources are listed per row in README.md.
JOINTS = [
    # (name, count, basis, value)
    ("hip_pitch",      2, "per_kg", 1.77),   # 230 Nm at 130 kg, scaled from 100-150 Nm at 70 kg
    ("hip_roll",       2, "per_kg", 1.23),
    ("hip_yaw",        2, "per_kg", 0.62),
    ("knee",           2, "per_kg", 1.77),
    ("ankle_pitch",    2, "per_kg", 1.40),   # sourced: 1.4 Nm/kg at push-off
    ("ankle_roll",     2, "per_kg", 0.54),
    ("trunk_pitch",    1, "per_kg", 1.54),
    ("trunk_yaw",      1, "per_kg", 0.77),
    # trunk_roll (lateral bend, kinematics §1.4, D-9) is not yet sized.
    # Candidate from README §6a: 0.6 x trunk_pitch = 0.92 Nm/kg (120 Nm at
    # 130 kg), which moves the density floor of spec 02.6 from 75 to ~78
    # Nm/kg. Adopting it is the author's call; the constant is not in the
    # table until then.
    ("shoulder_pitch", 2, "payload", (30.0, REACH)),
    ("shoulder_roll",  2, "payload", (22.0, REACH)),
    ("shoulder_yaw",   2, "fixed",   60.0),
    ("elbow",          2, "payload", (30.0, FOREARM_REACH)),
    ("wrist_yaw",      2, "fixed",   20.0),
    ("wrist_pitch",    2, "fixed",   20.0),
    ("wrist_roll",     2, "fixed",   20.0),
    ("neck_yaw",       1, "fixed",   15.0),
    ("neck_pitch",     1, "fixed",   15.0),
]

# Published torque densities, peak torque per actuator kilogram.
DENSITIES = [
    (22.0,  "integrated state of the art, whole-actuator"),
    (33.0,  "what spec 02.6 used before 2026-09-22"),
    (36.0,  "top of the superseded range"),
    (52.0,  "commercial QDD module, 8:1 planetary"),
    (75.0,  "floor of the band spec 02.6 now declares"),
    (88.7,  "commercial hollow-shaft planetary module, peak"),
]


def torque_table(body_mass):
    rows = []
    for name, n, basis, val in JOINTS:
        if basis == "per_kg":
            t = val * body_mass
        elif basis == "payload":
            load, reach = val
            t = load * G * reach
        else:
            t = val
        rows.append((name, n, t, n * t))
    return rows


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
    print("spec 02.2 assumes f_act in %.2f-%.2f." % (band_lo, band_hi))
    if not ok_any:
        print("NO published density puts f_act inside that range.")
        return 1
    need = total_nm / (band_hi * a.mass)
    print("The lowest density that fits is %.0f Nm/kg." % need)
    print("spec 02.6 declares 75-90 Nm/kg peak over module mass, which is why.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
