#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Actuator sizing for the declared kinematic configuration.

Sizes every joint from its peak torque requirement, checks the bought module
declared at each joint against it (spec 02.6, JOINT_MODULE), sums the module
masses, and reports the resulting `f_act` against the range spec 02.2 assumes.

    python3 hardware/electrical/actuator_sizing.py
    python3 hardware/electrical/actuator_sizing.py --mass 95

Torque requirements are scaled from published gait and task data; arm joints
are sized from the declared payload at the grip centre with the arm's own
weight added; see hardware/electrical/README.md for each source. Module
figures are the makers' sheets (README §6f). The published torque densities
the last table prints differ by a factor of four depending on whether the
number counts the motor or the whole actuator.
"""

from __future__ import annotations

import argparse
import functools
import sys

G = 9.81
REF_MASS = 102.3           # the reference point of D-8 (2 h, 65% armour, 1.65 m), scripts/gems_budget.py; checked there

MARGIN = 0.05              # room the module set keeps over REF_MASS before a joint fails, decided 2026-11-24 (README §6m); a choice, no source

# Bought module per joint (spec 02.6, decided 2026-11-23: the actuator mass is
# declared at the joint, not as one density). Each is the lightest module that
# passes the rank-1 rule of README §6f — the maker's sheet gives the peak torque
# and how long it holds, a continuous torque, the speed at 48 V, the mass and
# the size — and meets its joint at REF_MASS, and at REF_MASS plus MARGIN for
# the joints that scale with the body: peak torque, the reducer class of
# hardware/mechanical §2, the speed of MIN_RPM and, where a figure exists, the
# RMS torque of running in RUN_RMS and of walking in WALK_RMS. Figures are the
# sheets' (README §6f):
# (maker, model, peak Nm, continuous Nm, speed rpm at 48 V, kg, size mm, reducer, ratio)
# Continuous is the sheet's rated torque (ENCOS) or continuous stall torque
# (SEmotor); speed is ENCOS's peak speed or SEmotor's maximum speed.
MODULE_CATALOGUE = {
    "EC-A4315-P2-36":   ("ENCOS", "EC-A4315-P2-36", 75.0, 25.0, 117.0, 0.485, "56 x 69.5", "planetary", 36),
    "EC-A6416-P2-25":   ("ENCOS", "EC-A6416-P2-25", 120.0, 40.0, 120.0, 0.805, "88 x 67.5", "planetary", 25),
    "EC-A8116-P1-18":   ("ENCOS", "EC-A8116-P1-18", 130.0, 40.0, 140.0, 0.961, "105 x 57", "planetary", 18),
    "EC-A10020-P1-12":  ("ENCOS", "EC-A10020-P1-12", 150.0, 50.0, 140.0, 1.373, "124 x 60", "planetary", 12),
    "EC-A10020-P2-24":  ("ENCOS", "EC-A10020-P2-24", 330.0, 100.0, 123.0, 2.211, "124 x 85", "planetary", 24),
    "EC-A13715-P1-12.67": ("ENCOS", "EC-A13715-P1-12.67", 320.0, 110.0, 135.0, 2.695, "170 x 73", "planetary", 12.67),
    "EC-A3814-H14-107": ("ENCOS", "EC-A3814-H14-107", 60.0, 20.0, 52.0, 0.434, "53 x 78.5", "harmonic", 107),
    "SETZ70CI-1DA":     ("SEmotor", "SETZ70CI-1DA", 58.5, 9.0, 311.0, 0.70, "78 x 65", "planetary", 9),
    "SEAF70A16NG02":    ("SEmotor", "SEAF70A16NG02", 104.0, 16.0, 175.0, 0.80, "78 x 65", "planetary", 16),
    "SETZ70CI-1GA":     ("SEmotor", "SETZ70CI-1GA", 156.0, 24.0, 116.5, 0.90, "78 x 67", "planetary", 24),
    "SETZ70CI-1HA":     ("SEmotor", "SETZ70CI-1HA", 227.5, 35.0, 80.0, 1.05, "78 x 85", "planetary", 35),
    "SETZ90CI-1FG":     ("SEmotor", "SETZ90CI-1FG", 240.0, 60.0, 86.5, 1.60, "99 x 76.5", "planetary", 30),
    "RMD-X12-P20-320":  ("MyActuator", "RMD-X12-P20-320", 320.0, 85.0, 125.0, 2.40, "124 x 85", "planetary", 20),
}
# Torque held for 60 s, Nm: ENCOS's constant-load test, 30 to 100 °C at 54.5-63.5
# rpm output, interpolated between its rows (README §6f). Where a module has a
# figure here, the RUN_RMS check uses it; elsewhere the continuous torque.
HOLD_60S = {
    "EC-A4315-P2-36": 28.0, "EC-A6416-P2-25": 31.5, "EC-A10020-P1-12": 54.9,
    "EC-A10020-P2-24": 79.1, "EC-A13715-P1-12.67": 150.0,
}
JOINT_MODULE = {
    "hip_pitch": "EC-A10020-P2-24", "hip_roll": "EC-A10020-P2-24", "hip_yaw": "EC-A4315-P2-36",
    "knee": "EC-A13715-P1-12.67", "ankle_pitch": "RMD-X12-P20-320", "ankle_roll": "EC-A4315-P2-36",
    "trunk_pitch": "EC-A10020-P2-24", "trunk_roll": "SEAF70A16NG02", "trunk_yaw": "EC-A6416-P2-25",
    "shoulder_pitch": "EC-A10020-P1-12", "shoulder_roll": "EC-A10020-P1-12",
    "shoulder_yaw": "EC-A8116-P1-18", "elbow": "EC-A8116-P1-18",
    "wrist_yaw": "EC-A3814-H14-107", "wrist_pitch": "EC-A3814-H14-107", "wrist_roll": "EC-A3814-H14-107",
    "neck_yaw": "EC-A3814-H14-107", "neck_pitch": "EC-A3814-H14-107",
}
# The arm's reducer class is planetary, 6:1 to 15:1 (hardware/mechanical §2); at
# these joints up to 18:1 is allowed (Plone, 2026-11-24; README §6k).
ARM_RATIO_MAX = {"elbow": 18, "shoulder_yaw": 18}
# Time a module holds a torque standing still, 30 to 100 °C on its maker's
# bench, (Nm, s): the stall temperature-rise tables of the ENCOS manual
# (README ref 35). None in place of seconds: the row is marked sustainable.
# SEmotor and MyActuator publish no such table.
STALL_HOLD = {
    "EC-A8116-P1-18":  [(25.0, None), (30.0, 483), (35.0, 228), (40.0, 162), (50.0, 112), (60.0, 15), (70.0, 3)],
    "EC-A10020-P1-12": [(50.0, 1133), (53.0, 827), (55.0, 621), (58.0, 512), (61.5, 318)],
    "EC-A13715-P1-12.67": [(80.0, 1670), (105.0, 710), (130.0, 181), (160.0, 49), (170.0, 44), (195.0, 13)],
    "EC-A10020-P2-24": [(80.0, 1335), (86.0, 969), (90.0, 720), (96.0, 370), (100.0, 254), (110.0, 148), (122.0, 66), (127.0, 21)],
}
# Static holds, decided 2026-11-24 (Plone; spec 02.6, README §6k): a load at full
# reach is passed through, 2 s at most; picking up and setting down, 10 s at
# most; anything longer only where the module's table starts.
PASS_S, LIFT_S = 2.0, 10.0
# Trunk, straight and leaning as a whole, arms hanging: the moment at the lowest
# of the three pitch axes, the heavier case, since how the coupling shares it is
# not designed (⟦IMPL⟧). Geometry and mass fractions of the URDF (Winter's, a
# human's): the mass above the pelvis as a share of the body, its centre above
# that axis, and the shoulders above that axis, m.
UPPER_FRAC, UPPER_COM, SHOULDER_HEIGHT = 0.536, 0.2857, 0.335
LIFT_LEAN_DEG = 30.0       # trunk lean allowed with PAYLOAD_KG in the hands
HUG_KG, HUG_SHOULDER, HUG_ELBOW = 20.0, 0.30, 0.20   # LOAD_CASES, two hands
# Squatting to work, decided 2026-11-24 (Plone; README §6l): how long is the
# situation's, and what the hardware must hold at least is (load kg, trunk lean
# limit deg, seconds). Kneeling, on one knee by preference, is in README §6l.
SQUATS = [(0.0, 30.0, 300.0), (HUG_KG, 10.0, 30.0)]
# The squat: planar, both legs alike, feet flat. Lengths of the URDF and
# Winter's mass fractions; shank tilt to the ankle's 30 deg, and the centre of
# mass kept 3 cm inside the heel and 6 cm inside the toe.
THIGH, SHANK, FOOT_HALF, UPPER_ABOVE_HIP, SHOULDER_ABOVE_HIP = 0.40, 0.40, 0.125, 0.4357, 0.485
PELVIS_FRAC, THIGH_FRAC, SHANK_FRAC = 0.142, 0.100, 0.0465
# Speed a joint's module must reach, output rpm (README §6e): the knee's 11 rad/s
# in running, hip pitch's 7.4 rad/s (the hip's highest in running at 2.5 m/s),
# ankle pitch's 3.7 rad/s (walking; no running figure).
MIN_RPM = {"knee": 105.0, "hip_pitch": 71.0, "ankle_pitch": 35.0}
# The bus, decided 2026-11-24 (plan D-4; README §6n): 12 SA03 cells in series. The
# sheets give a module's speed at 48 V; it is scaled with the bus voltage, an
# estimate. Checked at the nominal voltage, reported down to the empty one.
SHEET_V, BUS_V = 48.0, (30.0, 40.8, 50.4)   # empty, nominal, full
# What else a joint's speed must reach, rpm at the output, not sized to: the
# knee's 9.4 rad/s in balance recovery and 6.9 walking at 1.0 m/s (README §6e).
OTHER_RPM = [("knee", "balance recovery", 89.8), ("knee", "walking at 1.0 m/s", 65.9)]
# RMS moment of running at 2.5 m/s, Nm per kg of body (README §6e, Fukuchi et
# al., participants 1-35, each one's cycle-averaged curve), for row 5's 60 s,
# against HOLD_60S where the module has it and its continuous torque elsewhere.
# Sagittal (Z) since 2026-11-23; hip roll and ankle roll from the frontal axis
# (X, abduction/adduction) and hip yaw from the transverse (Y), added
# 2026-11-23 (README §6g). Trunk, arms, wrists, neck: no figure.
RUN_RMS = {"hip_pitch": 0.56, "knee": 0.96, "ankle_pitch": 0.77,
           "hip_roll": 0.65, "hip_yaw": 0.11, "ankle_roll": 0.08}
# RMS torque of walking at 1.0 m/s, Nm per kg of body, against the module's
# continuous torque, since walking is held (README §6g). Legs: people walking
# on a treadmill at 0.9-1.1 m/s without holding the rails, the 90th percentile
# of the larger side (Fukuchi, Fukuchi & Duarte 2018; README §6j), adopted 2026-11-24
# with a human-like gait asked of the balance controller (plan F-5). Trunk:
# the simulated robot Oli (README §6g), since the human data stop at the
# pelvis. Arms: no figure; Oli's arm swing scales with Oli's arm.
WALK_RMS = {"hip_pitch": 0.400, "hip_roll": 0.536, "hip_yaw": 0.118, "knee": 0.334,
            "ankle_pitch": 0.760, "ankle_roll": 0.124,
            "trunk_pitch": 0.127, "trunk_roll": 0.147, "trunk_yaw": 0.224}
# The simulated robot's walking RMS, the stress case: required of the legs as
# well (Plone, 2026-11-24; README §6j), since no controller yet walks this body
# like a person, and no cooling helps a module below the torque it must hold.
WALK_RMS_OLI = {"hip_pitch": 0.824, "hip_roll": 0.796, "hip_yaw": 0.183, "knee": 0.736,
                "ankle_pitch": 0.683, "ankle_roll": 0.183}


def module(name):
    """The bought module of a joint: the catalogue row."""
    return MODULE_CATALOGUE[JOINT_MODULE[name]]

# Arm geometry, hardware/kinematics.md §2. Levers are horizontal distances from
# the joint axis with the arm held straight out, the posture of maximum
# gravitational moment.
UPPER_ARM = 0.30          # shoulder to elbow, 1.65 m body
FOREARM = 0.25            # elbow to wrist
WRIST_TO_GRIP = 0.06      # wrist to the centre of a held object, assumed ⟦IMPL⟧
SHOULDER_TO_GRIP = UPPER_ARM + FOREARM + WRIST_TO_GRIP   # 0.61 m
ELBOW_TO_GRIP = FOREARM + WRIST_TO_GRIP                  # 0.31 m

# Arm payload, decided 2026-09-26 (README §6b): 15 kg in one hand, arm
# horizontal, load at the grip centre. Shoulder roll carries the same posture
# abducted, at 11 kg.
PAYLOAD_KG = 15.0
PAYLOAD_ROLL_KG = 11.0

# Arm self-weight. Joint modules are the bought ones of JOINT_MODULE;
# structure and hand are allowances until CAD exists (⟦IMPL⟧). Positions are along the straight arm from the shoulder.
ARM_STRUCTURE = [
    # (name, mass kg, distance from shoulder m)
    ("upper arm structure", 0.8, UPPER_ARM / 2),
    ("forearm structure",   0.6, UPPER_ARM + FOREARM / 2),
    ("hand",                0.6, SHOULDER_TO_GRIP),
]
SHOULDER_YAW_POS = UPPER_ARM / 2     # yaw module sits in the upper arm
WRIST_POS = UPPER_ARM + FOREARM      # three wrist modules at the wrist

# Load cases, decided 2026-09-26 (spec 02.6, plan D-11): static objects only.
# Lifting, carrying or dragging a person is outside the declared capability;
# contact with people (spec 01 group 4) is not a load case and stays in.
# Levers are horizontal distances from the shoulder and elbow axes to the
# load's centre of mass; a load on the legs adds its mass to every per-kg
# leg and trunk row. Masses marked "proposed" await the author's figures.
LOAD_CASES = [
    # (name, mass kg, hands, lever from shoulder m, lever from elbow m, status)
    ("one hand, arm straight and horizontal",   PAYLOAD_KG, 1, SHOULDER_TO_GRIP, ELBOW_TO_GRIP, "decided D-10"),
    ("bag hanging from one hand, arm down",     20.0, 1, 0.0,  0.0,  "proposed"),
    ("object hugged to the chest, two hands",   20.0, 2, 0.30, 0.20, "proposed"),
    ("light object to a high shelf, one hand",  5.0,  1, SHOULDER_TO_GRIP, ELBOW_TO_GRIP, "proposed"),
    ("stairs with a load held close, two hands", 20.0, 2, 0.15, 0.10, "proposed"),
]

# The carry capacity is reported against the bought modules of hip pitch and
# knee, the lower of the two. Carrying is a stand-up or a step, so the demand
# is the walking and stairs figure of hip pitch and knee, not running's.
STAND_PER_KG = 1.77       # hip pitch, and the knee in walking, stairs and rising (README §6c)

# Per-joint peak torque. Leg and trunk figures scale with body mass; arm
# figures follow from the payload and the arm's own weight; the rest are fixed.
# Sources are listed per row in README.md.
JOINTS = [
    # (name, count, basis, value)
    ("hip_pitch",      2, "per_kg", 1.77),   # 100-150 Nm at 70 kg, scaled; unsourced (README §6d), above the 1.3 Nm/kg of a walking human
    ("hip_roll",       2, "per_kg", 1.73),   # running at 2.5 m/s, abduction peak (Fukuchi et al., README §6g), 2026-11-23; 1.23 before
    ("hip_yaw",        2, "per_kg", 0.62),
    ("knee",           2, "per_kg", 2.79),   # running at 2.5 m/s, stance peak (Fukuchi et al., README §6e; spec 02.6 row 5), 2026-11-23; 1.77 before, walking, stairs and rising (README §6c)
    ("ankle_pitch",    2, "per_kg", 2.07),   # running at 2.5 m/s (Fukuchi et al., README §6e), 2026-11-23; 1.40 before, push-off in walking
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
    (80.0,  "the arm floor; legs and trunk until 2026-11-23"),
    (88.7,  "commercial hollow-shaft planetary module, peak"),
    (133.0, "RMD-X12-P20-320, the leg density declared until 2026-11-23"),
    (150.0, "ENCOS EC-A10020-P2-24"),
]


def _fixed(name):
    return next(v for n, _, b, v in JOINTS if n == name and b == "fixed")


def arm_torques():
    """Peak torque at elbow and shoulder, arm horizontal, load at grip centre.

    Returns {"elbow": (payload Nm, self-weight Nm), "shoulder": (...),
    "shoulder_roll": (...)}. Self-weight counts the bought joint modules
    distal to the joint (JOINT_MODULE), plus the structure and hand
    allowances of ARM_STRUCTURE.
    """
    wrist_kg = sum(module(n)[5] for n in ("wrist_yaw", "wrist_pitch", "wrist_roll"))
    yaw_kg = module("shoulder_yaw")[5]

    # elbow: everything beyond it, measured from the elbow
    e_self = wrist_kg * G * (WRIST_POS - UPPER_ARM)
    for name, m, x in ARM_STRUCTURE:
        if x > UPPER_ARM:
            e_self += m * G * (x - UPPER_ARM)
    e_pay = PAYLOAD_KG * G * ELBOW_TO_GRIP
    elbow_kg = module("elbow")[5]

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


def torque_table(body_mass, carry_kg=0.0):
    """Peak torque per joint. `carry_kg` is a load held close to the body: it
    adds to the mass every leg and trunk row scales with, and nothing else."""
    arms = arm_torques()
    rows = []
    for name, n, basis, val in JOINTS:
        if basis == "per_kg":
            t = val * (body_mass + carry_kg)
        elif basis == "arm":
            joint, load = val
            key = "shoulder_roll" if load == PAYLOAD_ROLL_KG and joint == "shoulder" else joint
            t = sum(arms[key])
        else:
            t = val
        rows.append((name, n, t, n * t))
    return rows


def carry_capacity(body_mass):
    """Mass the legs can carry at their modules' peak and continuous torque: a
    stand-up or a step asks hip pitch and knee for STAND_PER_KG per kg of body
    and load, so a module's torque is reached at (body + carry) = torque /
    STAND_PER_KG; the lower of the two joints limits. Negative means the body
    alone exceeds it. Continuous is the figure for a load held through a slow
    climb; peak for a single stand-up or step."""
    hip, knee = module("hip_pitch"), module("knee")
    lim = hip if hip[2] <= knee[2] else knee
    peak = min(hip[2], knee[2])
    cont = min(hip[3], knee[3])
    return (peak / STAND_PER_KG - body_mass, cont / STAND_PER_KG - body_mass,
            "hip pitch (%s %s)" % lim[:2] if lim is hip else "knee (%s %s)" % lim[:2])


def load_case_table(body_mass):
    """Per load case: shoulder, elbow, hip and trunk torque, arm self-weight
    included. Hip and trunk take the load on the legs."""
    arms = arm_torques()
    s_self = arms["shoulder"][1]
    e_self = arms["elbow"][1]
    hip = next(v for n, _, b, v in JOINTS if n == "hip_pitch")
    trunk = next(v for n, _, b, v in JOINTS if n == "trunk_pitch")
    rows = []
    for name, m, hands, ls, le, status in LOAD_CASES:
        rows.append((name, m, status,
                     m / hands * G * ls + s_self,
                     m / hands * G * le + e_self,
                     hip * (body_mass + m),
                     trunk * (body_mass + m)))
    return rows


def split(body_mass=REF_MASS):
    """The summed torque in two parts: the part that scales with body mass,
    as Nm per kg of body, and the part that does not, in Nm.

    Legs and trunk are per-kg. Arms, wrists and neck are fixed by payload and
    geometry, so their actuator mass is non-scaling and belongs in m_ext of
    the mass loop (spec 02.1), not in f_act.
    """
    basis = {name: b for name, _, b, _ in JOINTS}
    per_kg = sum(n * v for _, n, b, v in JOINTS if b == "per_kg")
    fixed = sum(tot for name, _, _, tot in torque_table(body_mass)
                if basis[name] != "per_kg")
    return per_kg, fixed


def module_masses():
    """Bought module mass in two parts: legs and trunk (scales with the body
    through the module steps), arms, wrists and neck (does not)."""
    basis = {name: b for name, _, b, _ in JOINTS}
    legs = sum(n * module(name)[5] for name, n, _, _ in JOINTS if basis[name] == "per_kg")
    fixed = sum(n * module(name)[5] for name, n, _, _ in JOINTS if basis[name] != "per_kg")
    return legs, fixed


def densities(body_mass=REF_MASS):
    """Peak torque over bought module mass, legs and trunk and the rest, at
    `body_mass`: no longer declared, derived from JOINT_MODULE (spec 02.6)."""
    per_kg, fixed_nm = split(body_mass)
    legs, fixed = module_masses()
    return per_kg * body_mass / legs, fixed_nm / fixed


def module_check(body_mass):
    """Each joint's module against its joint at `body_mass`: peak, reducer
    class, speed, running RMS, walking RMS and static holds. Returns (failures, body mass up
    to which every module still meets its joint's peak and RMS)."""
    rows = {name: t for name, _, t, _ in torque_table(body_mass)}
    bad, limit = [], float("inf")
    for joint, level, what, t, need, held in static_holds(body_mass):
        if level in ("lift", "squat") and (held is None or held < need):
            bad.append("%s: %s holds %.0f Nm (%s) %s < %.0f s" % (
                joint, module(joint)[1], t, what, "no figure" if held is None else "%.0f s" % held, need))
    for name, n, basis, val in JOINTS:
        mk, model, peak, cont, rpm, kg, size, red, ratio = module(name)
        t = rows[name]
        if peak < t:
            bad.append("%s: %s peak %.0f Nm < %.0f Nm" % (name, model, peak, t))
        cls = "legs" if basis == "per_kg" else ("wrist" if name.startswith(("wrist", "neck")) else "arm")
        if cls == "legs" and red == "harmonic" or cls == "wrist" and red != "harmonic" \
                or cls == "arm" and not (red == "planetary" and 6 <= ratio <= ARM_RATIO_MAX.get(name, 15)):
            bad.append("%s: %s reducer %s %s:1 outside its class" % (name, model, red, ratio))
        if name in MIN_RPM and rpm * BUS_V[1] / SHEET_V < MIN_RPM[name]:
            bad.append("%s: %s %.0f rpm at %.1f V < %.0f rpm" % (name, model, rpm * BUS_V[1] / SHEET_V, BUS_V[1], MIN_RPM[name]))
        held = HOLD_60S.get(model, cont)
        if name in RUN_RMS and held < RUN_RMS[name] * body_mass:
            bad.append("%s: %s %s %.0f Nm < running RMS %.0f Nm"
                       % (name, model, "60 s" if model in HOLD_60S else "continuous",
                          held, RUN_RMS[name] * body_mass))
        walk = max(WALK_RMS.get(name, 0.0), WALK_RMS_OLI.get(name, 0.0))
        if cont < walk * body_mass:
            bad.append("%s: %s continuous %.0f Nm < walking RMS %.0f Nm"
                       % (name, model, cont, walk * body_mass))
        if basis == "per_kg":
            limit = min(limit, peak / val)
            if name in RUN_RMS:
                limit = min(limit, held / RUN_RMS[name])
            if walk:
                limit = min(limit, cont / walk)
    return bad, limit


def stall_hold(model, torque):
    """Seconds a module holds `torque` standing still, from STALL_HOLD,
    interpolated log-log between its rows. inf at or below a row marked
    sustainable; the lowest row's seconds below a lowest row with a time (the
    table says no more); None above the table or without one."""
    from math import exp, log
    rows = STALL_HOLD.get(model)
    if not rows or torque > rows[-1][0] + 1e-9:
        return None
    if torque <= rows[0][0]:
        return float("inf") if rows[0][1] is None else float(rows[0][1])
    for (t0, s0), (t1, s1) in zip(rows, rows[1:]):
        if t0 < torque <= t1:
            if s0 is None:         # above a sustainable row: the next row's time, a floor
                return float(s1)
            f = (log(torque) - log(t0)) / (log(t1) - log(t0))
            return exp(log(s0) + f * (log(s1) - log(s0)))


def trunk_lean(body_mass, deg, load_kg):
    """Moment at the lowest trunk pitch axis, Nm: the trunk straight and leaning
    `deg`, the arms hanging, `load_kg` in the hands."""
    from math import radians, sin
    return G * sin(radians(deg)) * (UPPER_FRAC * body_mass * UPPER_COM + load_kg * SHOULDER_HEIGHT)


@functools.lru_cache(maxsize=64)
def squat(body_mass, load_kg, lean_deg):
    """The worst knee torque of a squat, per leg, over knee bends to 135 deg,
    with the trunk lean (up to `lean_deg`) and shank tilt that make it least at
    each bend. Returns (knee Nm, hip Nm of that posture, trunk pitch Nm at
    `lean_deg`, knee bend deg)."""
    from math import cos, radians, sin
    mu, mp = UPPER_FRAC * body_mass, PELVIS_FRAC * body_mass
    mt, ms = 2 * THIGH_FRAC * body_mass, 2 * SHANK_FRAC * body_mass
    worst = (0.0, 0.0, 0)
    for bend in range(15, 136, 5):
        best = None
        for tilt in range(0, min(30, bend) + 1):
            kx = SHANK * sin(radians(tilt))
            back = radians(bend - tilt)
            hx, tx = kx - THIGH * sin(back), kx - THIGH / 2 * sin(back)
            for lean in range(-5, int(lean_deg) + 1):
                a = radians(lean)
                ux = hx + UPPER_ABOVE_HIP * sin(a)
                lx = hx + SHOULDER_ABOVE_HIP * sin(a) + HUG_SHOULDER
                above = mu + mp + load_kg + mt
                xa = (mu * ux + mp * hx + load_kg * lx + mt * tx) / above
                com = (above * xa + ms * kx / 2) / (above + ms)
                if not -FOOT_HALF + 0.03 <= com <= FOOT_HALF - 0.06:
                    continue
                knee = abs(above * G * (kx - xa) / 2)
                if best is None or knee < best[0]:
                    best = (knee, (mu * (ux - hx) + load_kg * (lx - hx)) * G / 2, bend)
        if best and best[0] > worst[0]:
            worst = best
    a = radians(lean_deg)
    trunk = G * (sin(a) * UPPER_FRAC * body_mass * UPPER_COM
                 + load_kg * (SHOULDER_HEIGHT * sin(a) + HUG_SHOULDER * cos(a)))
    return worst[0], worst[1], trunk, worst[2]


def static_holds(body_mass):
    """(joint, level, what, Nm, seconds required, seconds held). A pass-through
    above the module's table is reported, not failed: no maker's figure reaches it."""
    arms = arm_torques()
    e_self = arms["elbow"][1]
    s_self = arms["shoulder"][1]
    yaw = next(v for n, _, _, v in JOINTS if n == "shoulder_yaw")
    rows = [
        ("shoulder_pitch", "pass", "%.0f kg at full reach" % PAYLOAD_KG, sum(arms["shoulder"]), PASS_S),
        ("shoulder_roll", "pass", "%.0f kg at full reach, abducted" % PAYLOAD_ROLL_KG, sum(arms["shoulder_roll"]), PASS_S),
        ("shoulder_pitch", "lift", "%.0f kg, upper arm down, forearm level" % PAYLOAD_KG, sum(arms["elbow"]), LIFT_S),
        ("shoulder_yaw", "lift", "its declared torque", yaw, LIFT_S),
        ("elbow", "lift", "%.0f kg, forearm level" % PAYLOAD_KG, sum(arms["elbow"]), LIFT_S),
        ("trunk_pitch", "lift", "%.0f kg in the hands, leaning %.0f deg" % (PAYLOAD_KG, LIFT_LEAN_DEG),
         trunk_lean(body_mass, LIFT_LEAN_DEG, PAYLOAD_KG), LIFT_S),
        ("shoulder_pitch", "held", "%.0f kg hugged, two hands" % HUG_KG, HUG_KG / 2 * G * HUG_SHOULDER + s_self, None),
        ("elbow", "held", "%.0f kg hugged, two hands" % HUG_KG, HUG_KG / 2 * G * HUG_ELBOW + e_self, None),
        ("trunk_pitch", "held", "%.0f kg hugged, upright" % HUG_KG, HUG_KG * G * HUG_SHOULDER, None),
    ]
    for load, lean, secs in SQUATS:
        knee, hip, trunk, bend = squat(body_mass, load, lean)
        what = ("%.0f kg hugged" % load if load else "no load") + ", leaning %.0f deg at most" % lean
        rows += [("knee", "squat", what, knee, secs), ("hip_pitch", "squat", what, hip, secs),
                 ("trunk_pitch", "squat", what, trunk, secs)]
    return [(j, lv, w, t, need, stall_hold(module(j)[1], t)) for j, lv, w, t, need in rows]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--mass", type=float, default=REF_MASS,
                    help="body mass in kg (default: the D-8 reference point)")
    ap.add_argument("--carry", type=float, default=0.0,
                    help="load held close to the body, kg, added to the leg and trunk rows")
    a = ap.parse_args(argv)

    rows = torque_table(a.mass, carry_kg=a.carry)
    total_nm = sum(r[3] for r in rows)
    n_joints = sum(r[1] for r in rows)

    print("Actuator sizing — %d joints, body mass %.1f kg%s"
          % (n_joints, a.mass, ", carrying %.0f kg" % a.carry if a.carry else ""))
    print("=" * 96)
    print("  %-15s %2s %8s  %-8s %-17s %6s %5s %6s %6s %7s" % (
        "joint", "n", "peak Nm", "maker", "module", "peak", "cont", "rpm", "kg", "Nm/kg"))
    for name, n, t, tot in rows:
        mk, model, peak, cont, rpm, kg, size, red, ratio = module(name)
        print("  %-15s %2d %8.0f  %-8s %-17s %6.0f %5.0f %6.0f %6.3f %7.0f"
              % (name, n, t, mk, model, peak, cont, rpm, kg, t / kg))
    legs, fixed_kg = module_masses()
    print("  %-15s %2d %8.0f  modules %.1f kg (legs and trunk %.1f, arms, wrists, neck %.1f)"
          % ("TOTAL", n_joints, total_nm, legs + fixed_kg, legs, fixed_kg))
    bad, limit = module_check(a.mass + a.carry)
    print()
    short = a.mass == REF_MASS and not a.carry and limit < REF_MASS * (1 + MARGIN)
    if short:
        print("THE SET HOLDS ONLY TO %.1f kg, under %.0f%% over the reference, %.1f kg" % (limit, MARGIN * 100, REF_MASS * (1 + MARGIN)))
    if bad:
        print("MODULES THAT DO NOT MEET THEIR JOINT at %.1f kg:" % (a.mass + a.carry))
        for b in bad:
            print("  " + b)
    else:
        print("Every module meets its joint's peak, reducer class, speed, running and walking RMS (people's and the robot's), static holds")
        print("at %.1f kg; the set holds up to %.1f kg of body." % (a.mass + a.carry, limit))

    print()
    print("Speed on the bus (the sheet's at 48 V, scaled with the voltage, an estimate): empty %.1f, nominal %.1f, full %.1f V" % BUS_V)
    for name, what, need in [(n, "running" if n != "ankle_pitch" else "walking", v) for n, v in MIN_RPM.items()] + OTHER_RPM:
        rpm = module(name)[4]
        print("  %-12s %-20s needs %5.1f rpm: %5.1f at nominal; down to %.1f V%s"
              % (name, what, need, rpm * BUS_V[1] / SHEET_V, need / rpm * SHEET_V, "" if need / rpm * SHEET_V <= BUS_V[0] else ", above the empty pack"))
    print()
    print("Static holds (maker's stall table, 30 to 100 °C on the bench; README §6k, §6l):")
    for joint, level, what, t, need, held in static_holds(a.mass):
        print("  %-15s %-5s %-38s %5.0f Nm  %-16s %s" % (
            joint, level, what, t, module(joint)[1],
            "not in the table" if held is None else "sustainable" if held == float("inf") else "%.0f s" % held
            + (" or more" if t <= STALL_HOLD[module(joint)[1]][0 if STALL_HOLD[module(joint)[1]][0][1] else 1][0] else "")))

    per_kg, fixed = split(a.mass)
    d_legs, d_fixed = densities(a.mass)
    print()
    print("Split: %.2f Nm per kg of body (legs, trunk) = %.0f Nm at %.1f kg, on %.1f kg of modules: %.0f Nm/kg;"
          % (per_kg, per_kg * a.mass, a.mass, legs, d_legs))
    print("       %.0f Nm fixed (arms, wrists, neck), on %.1f kg of modules: %.0f Nm/kg,"
          % (fixed, fixed_kg, d_fixed))
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
    print("Load cases (static objects; people are not a load case) — Nm, arm self-weight included")
    print("=" * 66)
    print("  %-42s %5s %8s %6s %5s %6s" % ("case", "kg", "shoulder", "elbow", "hip", "trunk"))
    for name, m, status, ts, te, th, tt in load_case_table(a.mass):
        print("  %-42s %5.0f %8.0f %6.0f %5.0f %6.0f  %s" % (name, m, ts, te, th, tt, status))
    cp, cr, joint = carry_capacity(a.mass)
    print()
    print("Carry capacity of the legs against their modules, limited by %s," % joint)
    print("  at %.2f Nm/kg in a stand-up or step:" % STAND_PER_KG)
    print("  a single stand-up or step, at peak:       %s"
          % ("%.0f kg" % cp if cp >= 0 else "none — the body alone exceeds it by %.0f kg" % -cp))
    print("  a sustained climb, at continuous torque:  %s"
          % ("%.0f kg" % cr if cr >= 0 else "none — the body alone exceeds it by %.0f kg" % -cr))

    print()
    print("Actuator mass and f_act with legs and trunk at published torque densities,")
    print("arms, wrists and neck on their bought modules (%.1f kg)" % fixed_kg)
    print("=" * 66)
    print("  %8s  %9s  %7s  %-28s" % ("Nm/kg", "mass kg", "f_act", "source"))
    band_lo, band_hi = 0.25, 0.36   # for reference only since 2026-11-24 (Plone): the band has no source (spec 02.2)
    for d, label in DENSITIES + [(d_legs, "the bought modules of JOINT_MODULE")]:
        m = per_kg * a.mass / d + fixed_kg
        f = m / a.mass
        print("  %8.1f  %9.1f  %7.3f  %-28s %s"
              % (d, m, f, label, "in range" if band_lo <= f <= band_hi else ""))
    print()
    print("For reference, spec 02.2 once held f_act to %.2f-%.2f (scaling part + fixed part / body)." % (band_lo, band_hi))
    f_bought = (legs + fixed_kg) / a.mass
    print("With the bought modules f_act is %.3f%s." % (f_bought, "" if band_lo <= f_bought <= band_hi else ", outside that band, which is no longer a check"))
    return 1 if bad or short else 0


if __name__ == "__main__":
    sys.exit(main())
