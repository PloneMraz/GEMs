#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
Generate the engineering BOM of the GEMs reference design, and check it.

    python hardware/bom/build_bom.py            # write parts.csv, ebom.csv, EBOM.md
    python hardware/bom/build_bom.py --check    # verify, write nothing

Three files carry the BOM, in the form hardware teams use:

  parts.csv   item master — one row per internal part number    GENERATED
  ebom.csv    product structure — parent, find number, child, qty GENERATED
  avl.csv     approved manufacturer list — who makes a part, at    HAND-KEPT
              what price, read from which page on which date

The structure is generated from the declared kinematics and the joint torque
table in hardware/electrical/actuator_sizing.py, so that a change to the joint
list cannot leave the BOM behind. Sourcing and prices are facts about the world,
not about the design, so they are kept by hand in avl.csv and never generated.

A blank is a record: it says a value has not been verified. The check refuses
half-claims — a price without its date and page, a selected part without a
manufacturer part number — because a number nobody can trace is worse than a
blank.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "electrical"))
from actuator_sizing import REF_MASS, torque_table  # noqa: E402

PART_FIELDS = ["part_number", "rev", "description", "category", "make_buy",
               "uom", "unit_mass_kg", "mass_basis", "maturity", "design_level",
               "lifecycle", "spec_ref", "requirement", "notes"]
EBOM_FIELDS = ["parent", "find_no", "child", "qty", "qty_basis", "ref_des",
               "notes"]
AVL_FIELDS = ["part_number", "rank", "status", "manufacturer", "mpn",
              "supplier", "supplier_pn", "source_url", "unit_price", "currency",
              "price_qty", "price_date", "price_url", "notes"]

CATEGORIES = {"ASSY", "MFG", "OTS", "PCBA", "CABLE", "MATL", "SW", "CONS"}
MATURITY = {"TM", "LAB"}
STATUS = {"SELECTED", "CANDIDATE"}

# Declared density at the reference operating point: f_act = 0.30 needs the
# top of the 75-90 Nm/kg band (spec 02.6). Used only for mass estimates.
MODULE_NM_PER_KG = 88.7
PACK_KWH, CELLS_KG = 10.36, 23.0          # gems_budget at the declared point
ARMOUR_M2, ARMOUR_KG_M2 = 1.17, 7.5       # 65% of 1.8 m2, mid-band areal density
BODY_MASS_BUDGET = 129.5

# -- joint table: stable index -> part-number block. Never renumber. -------
#    idx, joint, reducer class, placement
JOINTS = [
    (1, "hip_pitch", "cycloidal", "leg"), (2, "hip_roll", "cycloidal", "leg"),
    (3, "hip_yaw", "cycloidal", "leg"), (4, "knee", "cycloidal", "leg"),
    (5, "ankle_pitch", "unassigned", "leg"), (6, "ankle_roll", "unassigned", "leg"),
    (7, "trunk_pitch", "unassigned", "torso"), (8, "trunk_yaw", "unassigned", "torso"),
    (9, "shoulder_pitch", "planetary", "arm"), (10, "shoulder_roll", "planetary", "arm"),
    (11, "shoulder_yaw", "planetary", "arm"), (12, "elbow", "planetary", "arm"),
    (13, "wrist_yaw", "harmonic", "arm"), (14, "wrist_pitch", "harmonic", "arm"),
    (15, "wrist_roll", "harmonic", "arm"), (16, "neck_yaw", "harmonic", "neck"),
    (17, "neck_pitch", "harmonic", "neck"),
    (18, "trunk_roll", "unassigned", "torso"),     # lateral bend, D-9
]
MODULE_CHILDREN = [
    # offset, description, category, make/buy, spec_ref
    (1, "Motor, frameless BLDC", "OTS", "BUY", "hardware/electrical 2"),
    (2, "Reducer", "OTS", "BUY", "hardware/mechanical 2"),
    (3, "Output bearing", "OTS", "BUY", "hardware/mechanical 5"),
    (4, "Absolute encoder, motor side", "OTS", "BUY", "spec 05.3 proprioception"),
    (5, "Absolute encoder, output side", "OTS", "BUY", "spec 05.3 proprioception"),
    (6, "Joint torque sensor", "OTS", "BUY", "spec 05.3; spec 06.6"),
    (7, "Joint drive PCBA", "PCBA", "MAKE", "plan E-3"),
    (8, "Housing, 7075-T6", "MFG", "MAKE", "hardware/mechanical 1"),
    (9, "Fastener set", "OTS", "BUY", "plan M-3"),
]

# Software carried as virtual part numbers: each image is a child of the board
# it is programmed into, so a shipped body records which image it carries.
SOFTWARE = [
    # pn, description, parent boards, spec_ref
    ("GEM-40010", "Firmware image, joint drive", "joint drive PCBAs", "plan F-3"),
    ("GEM-40020", "Firmware image, real-time controller", "GEM-13230", "plan F-0 to F-11"),
    ("GEM-40030", "Firmware image, battery management", "GEM-13120", "plan F-9"),
    ("GEM-40040", "Firmware image, beacon radio", "GEM-13330", "plan F-12"),
    ("GEM-40050", "Firmware image, secure element", "GEM-13350", "plan F-11"),
    ("GEM-40060", "Firmware image, tactile readout", "GEM-18080", "plan F-1"),
    ("GEM-40070", "Firmware image, shell field driver", "GEM-18090", "plan F-13"),
    ("GEM-40080", "OS image, edge AI module", "GEM-13200", "spec 07.1"),
    ("GEM-40090", "GEMs software stack, edge AI module", "GEM-13200", "plan S-0 to S-9"),
]

# Manufacturing-only items: in the MBOM, never in the EBOM.
CONSUMABLES = [
    ("GEM-50010", "Threadlocker, medium strength", "ML"),
    ("GEM-50020", "Reducer grease", "G"),
    ("GEM-50030", "Thermal interface material", "G"),
    ("GEM-50040", "Adhesive, shell layer bonding", "ML"),
    ("GEM-50050", "Cable ties and heat-shrink", "SET"),
    ("GEM-50060", "Shipping crate and packaging", "SET"),
]


def module_pn(idx):
    return "GEM-2%02d00" % idx


class Bom:
    def __init__(self):
        self.parts = {}
        self.lines = []
        self._find = defaultdict(int)

    def part(self, pn, desc, cat, mb, uom="EA", mass="", basis="", mat="TM",
             level="L0", ref="", req="", notes=""):
        assert pn not in self.parts, pn
        self.parts[pn] = dict(part_number=pn, rev="A", description=desc,
                              category=cat, make_buy=mb, uom=uom,
                              unit_mass_kg=mass, mass_basis=basis, maturity=mat,
                              design_level=level, lifecycle="CONCEPT",
                              spec_ref=ref, requirement=req, notes=notes)
        return pn

    def use(self, parent, child, qty="1", basis="", ref_des="", notes=""):
        self._find[parent] += 10
        self.lines.append(dict(parent=parent, find_no=str(self._find[parent]),
                               child=child, qty=qty, qty_basis=basis,
                               ref_des=ref_des, notes=notes))


def build():
    b = Bom()
    torque = {name: t for name, _, t, _ in torque_table(REF_MASS)}
    for pn, d, _, ref in SOFTWARE:
        b.part(pn, d, "SW", "MAKE", uom="EA", level="L0", ref=ref,
               notes="Virtual part: version recorded at programming. Nothing built yet.")
    for pn, d, uom in CONSUMABLES:
        b.part(pn, d, "CONS", "BUY", uom=uom, level="L0", ref="MBOM only")

    # -- joint modules: one part number per joint type, shared left/right --
    for idx, name, red, _ in JOINTS:
        nm = torque.get(name)
        pn = module_pn(idx)
        if nm is None:                    # declared, not yet sized
            b.part(pn, "Joint module, %s" % name.replace("_", " "), "ASSY", "MAKE",
                   level="L1", ref="hardware/kinematics.md 1.4",
                   req="torque not yet sized (D-9); >=75 Nm/kg over module mass",
                   notes="Trunk lateral bend, added by D-9. No torque source yet.")
        else:
            b.part(pn, "Joint module, %s" % name.replace("_", " "), "ASSY", "MAKE",
                   mass="%.3f" % (nm / MODULE_NM_PER_KG),
                   basis="estimate: %.0f Nm peak / %.1f Nm/kg" % (nm, MODULE_NM_PER_KG),
                   level="L2", ref="spec 02.6; hardware/kinematics.md 1",
                   req="%.0f Nm peak; >=75 Nm/kg over module mass" % nm,
                   notes="D-2 open: procure as one module or build from the children below."
                   + ("" if nm <= 85 else " No module found at this torque and density."))
        for off, desc, cat, mb, ref in MODULE_CHILDREN:
            cpn = "GEM-2%02d%02d" % (idx, off)
            d = desc
            n = ""
            if off == 2:
                d = "Reducer, %s" % red if red != "unassigned" else "Reducer"
                n = ("class per hardware/mechanical 2" if red != "unassigned" else
                     "no class assigned in hardware/mechanical 2")
                if red != "planetary":
                    n += "; conflicts with the planetary module family of hardware/electrical 2"
            if off == 7:
                n = "PCBA BOM is generated from its schematic (plan E-3); none exists yet"
            b.part(cpn, "%s, %s" % (d, name.replace("_", " ")), cat, mb,
                   uom="SET" if off == 9 else "EA",
                   level="L1" if off in (2, 7) else "L0", ref=ref, notes=n)
            b.use(pn, cpn)
            if off == 7:
                b.use(cpn, "GEM-40010")

    # -- structure and sub-assemblies --------------------------------------
    S = lambda pn, d: b.part(pn, d, "MFG", "MAKE", level="L2",
                             ref="hardware/mechanical 1",
                             req="CFRP long members, 7075-T6 at joints",
                             notes="Section sizing IMPL; structure allowance 38.8 kg in total")

    top = b.part("GEM-10000", "GEMs body, reference design A (4 h, 65% armour coverage)",
                 "ASSY", "MAKE", level="L1", ref="spec 02.5; protocol/conformance-record.md",
                 req="%.1f kg derived body mass" % BODY_MASS_BUDGET)

    head = b.part("GEM-11000", "Head assembly", "ASSY", "MAKE", level="L1", ref="plan M-9")
    b.use(top, head)
    b.use(head, S("GEM-11010", "Head structure"))
    for pn, d, q, ref, req, mat in [
        ("GEM-11020", "Camera module, 4K 30 fps 12 bit", "2", "spec 05.3", "stereo pair; optical zoom, multispectral", "TM"),
        ("GEM-11030", "Thermal IR camera, 640x480 30 fps 16 bit", "1", "spec 05.3", "", "TM"),
        ("GEM-11040", "LiDAR / depth sensor, 300k points/s", "1", "spec 05.3", "", "TM"),
        ("GEM-11050", "Microphone, array element", "16", "spec 05.3", "16 ch, 48 kHz, 24 bit", "TM"),
        ("GEM-11060", "Electronic nose", "1", "spec 05.3", "5-30 ppb per compound, 5-10 s", "TM"),
        ("GEM-11070", "Taste analyser, lab-on-chip", "1", "spec 05.3", "batch-wise", "LAB"),
        ("GEM-11080", "Speaker and ultrasonic emitter", "1", "spec 05.3", "", "TM"),
        ("GEM-11090", "Micro facial and pupil actuator set", "1", "spec 05.3; kinematics 1.6", "", "LAB"),
    ]:
        b.use(head, b.part(pn, d, "OTS" if mat == "TM" else "MFG",
                           "BUY" if mat == "TM" else "MAKE", uom="SET" if pn == "GEM-11090" else "EA",
                           mat=mat, level="L1", ref=ref, req=req), q)
    b.use(head, b.part("GEM-11100", "Head sensor hub PCBA", "PCBA", "MAKE", level="L0",
                       ref="plan E-6", notes="PCBA BOM from schematic; none exists yet"))

    neck = b.part("GEM-12000", "Neck assembly", "ASSY", "MAKE", level="L1", ref="hardware/kinematics.md 1")
    b.use(top, neck)
    b.use(neck, module_pn(16))
    b.use(neck, module_pn(17))

    torso = b.part("GEM-13000", "Torso assembly", "ASSY", "MAKE", level="L1", ref="plan M-2")
    b.use(top, torso)
    b.use(torso, S("GEM-13010", "Pelvis structure"))
    b.use(torso, S("GEM-13020", "Torso structure, upper thorax"))
    b.use(torso, S("GEM-13021", "Spine segment structure, lumbar"))
    b.use(torso, S("GEM-13022", "Spine segment structure, lower thoracic"))
    b.use(torso, b.part("GEM-13023", "Spine coupling mechanism, three axes over three segments",
                        "MFG", "MAKE", uom="SET", level="L1",
                        ref="hardware/kinematics.md 1.4; plan D-9",
                        notes="Gearing, cable or elastic continuum element: IMPL"))
    b.use(torso, module_pn(8))
    b.use(torso, module_pn(7))
    b.use(torso, module_pn(18))
    b.use(torso, b.part("GEM-13030", "IMU, torso", "OTS", "BUY", level="L1",
                        ref="spec 05.3", req="1 kHz"), "", "count IMPL; at least 1")

    power = b.part("GEM-13100", "Power assembly", "ASSY", "MAKE", level="L1", ref="plan E-2")
    b.use(torso, power)
    stack = b.part("GEM-13110", "Cell stack", "ASSY", "MAKE", mass="%.1f" % CELLS_KG,
                   basis="cells only: %.2f kWh at 450 Wh/kg (gems_budget)" % PACK_KWH,
                   level="L2", ref="spec 03.1; hardware/electrical 3", req="400-500 Wh/kg")
    b.use(power, stack)
    b.use(stack, b.part("GEM-13111", "Cell, durable tier", "OTS", "BUY", level="L2",
                        ref="spec 03.1; hardware/electrical 3", req="400-500 Wh/kg",
                        notes="D-5 open"),
          "", "%.2f kWh / per-cell energy of the part chosen" % PACK_KWH)
    for pn, d, cat, ref, req in [
        ("GEM-13120", "Battery management PCBA", "PCBA", "plan E-2", "monitoring, balancing, protection"),
        ("GEM-13130", "Pack enclosure", "MFG", "plan M-2", ""),
        ("GEM-13140", "Supercapacitor bank", "OTS", "spec 03.2 measure 3", "burst power"),
        ("GEM-13150", "Pre-charge, contactor and fuse set", "OTS", "plan E-2", "bus voltage D-4"),
        ("GEM-13160", "Power distribution and DC-DC PCBA", "PCBA", "plan E-4", "HV to logic rails"),
        ("GEM-13170", "Always-on rail PCBA", "PCBA", "spec 03.6", "tens of microwatts"),
    ]:
        b.use(power, b.part(pn, d, cat, "MAKE" if cat != "OTS" else "BUY",
                            uom="SET" if pn == "GEM-13150" else "EA", level="L1",
                            ref=ref, req=req))

    compute = b.part("GEM-13200", "Compute assembly", "ASSY", "MAKE", level="L1", ref="plan E-5")
    b.use(torso, compute)
    for pn, d, cat, lvl, ref, req, n in [
        ("GEM-13210", "Edge AI module", "OTS", "L2", "hardware/electrical 4", "40-130 W, 128 GB", ""),
        ("GEM-13220", "Edge module carrier PCBA", "PCBA", "L1", "plan E-5", "", ""),
        ("GEM-13230", "Real-time controller PCBA, EtherCAT master", "PCBA", "L0", "spec 07.2; firmware/README",
         "balance 500 Hz, reflex 10 ms", "D-3 open: processor not chosen; not the edge module"),
        ("GEM-13240", "Audit log storage, 2 TB", "OTS", "L1", "spec 07.6", "~1700 h full tier", ""),
        ("GEM-13250", "SDR front-end, 2 ch x 56 MHz", "OTS", "L1", "spec 05.3", "16 bit I/Q", ""),
    ]:
        b.use(compute, b.part(pn, d, cat, "BUY" if cat == "OTS" else "MAKE", level=lvl,
                              ref=ref, req=req, notes=n))

    comms = b.part("GEM-13300", "Communications assembly", "ASSY", "MAKE", level="L1", ref="spec 01 Link")
    b.use(torso, comms)
    for pn, d, ref, req, lvl, n in [
        ("GEM-13310", "mmWave uplink radio, 60 GHz", "spec 01 Link", "~8 Gbps, ~1 ms PHY", "L1", ""),
        ("GEM-13320", "Fallback link module, LEO / cellular", "spec 01 Link", "", "L1", ""),
        ("GEM-13330", "Low-power beacon radio", "spec 06.5", "quiescent power; RSIL C5", "L0", "D-7 open"),
        ("GEM-13340", "Spatial RF sensing front-end", "spec 05.3", "Wi-Fi / mmWave CSI", "L1", ""),
    ]:
        b.use(comms, b.part(pn, d, "OTS", "BUY", level=lvl, ref=ref, req=req, notes=n))
    b.use(comms, b.part("GEM-13350", "Secure element", "OTS", "BUY", level="L0",
                        ref="spec 06.2; spec 06.3", notes="D-7 open"),
          "", "per node or per bus segment, IMPL")
    b.use(torso, b.part("GEM-13400", "Cardiac co-regulation module", "OTS", "BUY", level="L1",
                        ref="spec 05.3", req="vibration, warmth, rhythm; optional"),
          "1", "optional, not always-on")

    for side, arm_pn, leg_pn, hand_pn in (("left", "GEM-14000", "GEM-16000", "GEM-14900"),
                                          ("right", "GEM-15000", "GEM-17000", "GEM-15900")):
        arm = b.part(arm_pn, "Arm assembly, %s" % side, "ASSY", "MAKE", level="L1",
                     ref="hardware/kinematics.md 1")
        b.use(top, arm)
        o = 0 if side == "left" else 1000
        for idx in (9, 10, 11):
            b.use(arm, module_pn(idx))
        b.use(arm, S("GEM-%d" % (14010 + o), "Upper arm structure, %s" % side))
        b.use(arm, module_pn(12))
        b.use(arm, S("GEM-%d" % (14020 + o), "Forearm structure, %s" % side))
        for idx in (13, 14, 15):
            b.use(arm, module_pn(idx))
        hand = b.part(hand_pn, "Hand assembly, %s, 5 DOF" % side, "ASSY", "MAKE", level="L1",
                      ref="hardware/kinematics.md 1.2", notes="minimum configuration, D-6")
        b.use(arm, hand)
        b.use(hand, S("GEM-%d" % (14910 + o), "Hand structure, %s" % side))
        b.use(hand, b.part("GEM-%d" % (14920 + o), "Finger actuator, %s" % side, "OTS", "BUY",
                           level="L0", ref="hardware/kinematics.md 1.2",
                           notes="torque not derived"), "5")

        leg = b.part(leg_pn, "Leg assembly, %s" % side, "ASSY", "MAKE", level="L1",
                     ref="hardware/kinematics.md 1")
        b.use(top, leg)
        for idx in (2, 1, 3):
            b.use(leg, module_pn(idx))
        b.use(leg, S("GEM-%d" % (16010 + o), "Thigh structure, %s" % side))
        b.use(leg, module_pn(4))
        b.use(leg, S("GEM-%d" % (16020 + o), "Shank structure, %s" % side))
        b.use(leg, module_pn(5))
        b.use(leg, module_pn(6))
        b.use(leg, S("GEM-%d" % (16030 + o), "Foot structure, %s" % side))
        b.use(leg, b.part("GEM-%d" % (16040 + o), "Foot contact sensing, %s" % side, "OTS", "BUY",
                          level="L0", ref="spec 06.6; plan F-4"))

    shell = b.part("GEM-18000", "Shell and protection assembly", "ASSY", "MAKE", level="L1",
                   ref="spec 04.5; spec 02.4")
    b.use(top, shell)
    b.use(shell, b.part("GEM-18010", "Armour panel, integrated multi-threat", "MATL", "BUY",
                        uom="M2", mass="%.1f" % ARMOUR_KG_M2,
                        basis="per m2, mid-band of 6-9 kg/m2", level="L2",
                        ref="spec 02.4; hardware/mechanical 3",
                        req="NIJ IIIA + NIJ 0115 level 1"),
          "%.2f" % ARMOUR_M2, "65% of 1.8 m2")
    for pn, d, q, basis, mat, ref, req in [
        ("GEM-18020", "Sense-and-heal layer, e-skin and self-healing polymer", "1.80", "skin area", "LAB", "spec 04.5", "600% stretch"),
        ("GEM-18030", "Variable-stiffness layer, MR / ER / jamming", "", "coverage IMPL", "LAB", "spec 04.1", "2-30x modulus, ms"),
        ("GEM-18040", "Fire layer, sacrificial", "", "coverage IMPL", "TM", "spec 04.4", "standard to be anchored"),
        ("GEM-18050", "Electrochromic colour layer", "", "coverage IMPL", "LAB", "spec 04.3", "~1-5 s"),
    ]:
        b.use(shell, b.part(pn, d, "MATL", "MAKE" if mat == "LAB" else "BUY", uom="M2", mat=mat,
                            level="L2", ref=ref, req=req), q, basis)
    b.use(shell, b.part("GEM-18060", "Tactile taxel, fine region (hands, face)", "MFG", "MAKE",
                        mat="LAB", level="L1", ref="spec 05.2", req="~300/cm2"),
          "150000", "~500 cm2 at ~300/cm2")
    b.use(shell, b.part("GEM-18070", "Tactile taxel, ordinary region", "MFG", "MAKE",
                        mat="LAB", level="L1", ref="spec 05.2", req="~20/cm2"),
          "350000", "~17,500 cm2 at ~20/cm2")
    b.use(shell, b.part("GEM-18080", "Tactile readout PCBA", "PCBA", "MAKE", mat="LAB",
                        level="L0", ref="plan E-7", notes="PCBA BOM from schematic; none exists yet"),
          "", "count IMPL")
    b.use(shell, b.part("GEM-18090", "Shell field driver PCBA (MR coils / ER HV / electrochromic)",
                        "PCBA", "MAKE", mat="LAB", level="L0", ref="plan E-10"), "", "count IMPL")

    harness = b.part("GEM-19000", "Harness assembly", "ASSY", "MAKE", level="L0", ref="plan E-12")
    b.use(top, harness)
    for pn, d in [("GEM-19010", "EtherCAT joint chain cable set"),
                  ("GEM-19020", "CAN FD sensing bus cable set"),
                  ("GEM-19030", "HV power distribution cable set"),
                  ("GEM-19040", "Sensor link cable set (camera, LiDAR, audio)")]:
        b.use(harness, b.part(pn, d, "CABLE", "MAKE", uom="SET", level="L0",
                              ref="hardware/electrical 5"))

    dock = b.part("GEM-30000", "Dock, seat form, with charging contacts", "ASSY", "MAKE",
                  level="L1", ref="spec 03.5", notes="Ground equipment; not part of the body")
    b.use(dock, S("GEM-30010", "Dock structure"))
    b.use(dock, b.part("GEM-30020", "Charging contact set", "OTS", "BUY", uom="SET",
                       level="L1", ref="spec 03.5"))
    b.use(dock, b.part("GEM-30030", "Dock charger PCBA", "PCBA", "MAKE", level="L0",
                       ref="plan E-2", notes="PCBA BOM from schematic; none exists yet"))

    for pn, _, parents, _ in SOFTWARE:
        if parents.startswith("GEM-"):
            b.use(parents, pn)

    # structural fasteners per assembly, drawn from the CAD once it exists
    for pn, p in list(b.parts.items()):
        if p["category"] == "ASSY" and not pn.startswith("GEM-2") and pn != "GEM-13110":
            fpn = pn[:-2] + "99"
            b.use(pn, b.part(fpn, "Fastener set, %s" % p["description"].split(",")[0].lower(),
                             "OTS", "BUY", uom="SET", level="L0", ref="plan M-5",
                             notes="Contents from the CAD (plan M-1, M-5)"))
    return b, top, dock


# -- manufacturing BOM ------------------------------------------------------

MBOM_FIELDS = ["assembly", "op_no", "work_center", "operation", "consumes",
               "qty", "uom", "qty_basis", "notes"]
WORK_CENTERS = {
    "WC-EMS": "PCB assembly, external contract manufacturer",
    "WC-PROG": "Device programming",
    "WC-CELL": "Cell stack assembly, external specialist",
    "WC-HARN": "Harness manufacture, external",
    "WC-JNT": "Joint module assembly",
    "WC-SUB": "Sub-assembly",
    "WC-INT": "Final integration",
    "WC-CAL": "Calibration and end-of-line test",
    "WC-COM": "Commissioning: root of trust and attestation baselines",
    "WC-PACK": "Packaging",
}
AS_CONSUMED = "as consumed; figure set by the work instruction"


def build_mbom(b, roots):
    """Routings: the EBOM regrouped into build operations, plus the
    manufacturing-only items the EBOM never carries. Every EBOM line is
    consumed by exactly one operation of its parent's routing."""
    children = defaultdict(list)
    for l in b.lines:
        children[l["parent"]].append(l)
    ops = []

    def op(asm, wc, text, consumes="", qty="", basis="", notes=""):
        n = 10 * (1 + sum(o["assembly"] == asm for o in ops))
        uom = b.parts[consumes]["uom"] if consumes else ""
        ops.append(dict(assembly=asm, op_no=str(n), work_center=wc, operation=text,
                        consumes=consumes, qty=qty, uom=uom, qty_basis=basis, notes=notes))

    def line(asm, off_desc):
        for l in children[asm]:
            if b.parts[l["child"]]["description"].startswith(off_desc):
                return l
        raise KeyError((asm, off_desc))

    for asm in sorted(children):
        p = b.parts[asm]
        if asm.startswith("GEM-2") and p["category"] == "ASSY":          # joint module
            name = p["description"].split(", ", 1)[1]
            steps = [("Housing", "Prepare housing", None),
                     ("Output bearing", "Press in output bearing", None),
                     ("Motor", "Install motor stator and rotor", None),
                     ("Reducer", "Install reducer; grease per work instruction", "GEM-50020"),
                     ("Absolute encoder, motor side", "Install motor-side encoder", None),
                     ("Absolute encoder, output side", "Install output-side encoder", None),
                     ("Joint torque sensor", "Install joint torque sensor", None),
                     ("Joint drive PCBA", "Mount drive PCBA; thermal interface to housing", "GEM-50030"),
                     ("Fastener set", "Fasten and torque to drawing", "GEM-50010")]
            for key, text, cons in steps:
                l = line(asm, key)
                op(asm, "WC-JNT", text, l["child"], l["qty"], l["qty_basis"])
                if cons:
                    op(asm, "WC-JNT", "(consumable) %s" % b.parts[cons]["description"],
                       cons, "", AS_CONSUMED)
            op(asm, "WC-CAL", "Commutation offset and encoder calibration, %s" % name)
            op(asm, "WC-CAL", "Joint torque sensor calibration")
            op(asm, "WC-CAL", "End-of-line test: peak torque, backdrive, thermal")
            continue
        if p["category"] == "PCBA":
            op(asm, "WC-EMS", "Assemble board to its PCBA BOM (from schematic)")
            for l in children[asm]:
                op(asm, "WC-PROG", "Program %s" % b.parts[l["child"]]["description"].lower(),
                   l["child"], l["qty"], l["qty_basis"])
            op(asm, "WC-CAL", "Board-level functional test")
            continue
        if asm == "GEM-13110":
            for l in children[asm]:
                op(asm, "WC-CELL", "Build cell stack", l["child"], l["qty"], l["qty_basis"])
            op(asm, "WC-CAL", "Cell matching and stack acceptance test")
            continue
        wc = {"GEM-10000": "WC-INT", "GEM-19000": "WC-HARN"}.get(asm, "WC-SUB")
        for l in children[asm]:
            c = b.parts[l["child"]]
            if c["category"] == "SW":
                op(asm, "WC-PROG", "Install %s" % c["description"].lower(),
                   l["child"], l["qty"], l["qty_basis"])
            elif c["uom"] == "M2":
                op(asm, wc, "Apply %s" % c["description"].lower(), l["child"], l["qty"],
                   l["qty_basis"])
            elif c["description"].startswith("Fastener set"):
                op(asm, wc, "Fasten and torque to drawing", l["child"], l["qty"], l["qty_basis"])
            else:
                op(asm, wc, "Install %s" % c["description"][0].lower() + c["description"][1:],
                   l["child"], l["qty"], l["qty_basis"])
        if asm == "GEM-18000":
            op(asm, wc, "(consumable) %s" % b.parts["GEM-50040"]["description"],
               "GEM-50040", "", AS_CONSUMED)
        if asm == "GEM-19000":
            op(asm, wc, "(consumable) %s" % b.parts["GEM-50050"]["description"],
               "GEM-50050", "", AS_CONSUMED)
        if wc == "WC-SUB" or asm == "GEM-10000":
            op(asm, wc, "(consumable) %s" % b.parts["GEM-50010"]["description"],
               "GEM-50010", "", AS_CONSUMED)
        if asm == "GEM-10000":
            op(asm, "WC-COM", "Provision root-of-trust keys; record measured-boot baseline (spec 06.2)")
            op(asm, "WC-COM", "Baseline physical fingerprints for attestation tier 2 (spec 06.3)")
            op(asm, "WC-CAL", "Whole-body calibration: IMU, joint zero offsets, kinematics")
            op(asm, "WC-CAL", "End-of-line test: power states (spec 03.4), stand and balance, supported failure state (spec 07.3)")
    for r in roots:
        op(r, "WC-PACK", "Pack for shipment", "GEM-50060", "1")
    return ops


def check_mbom(b, ops):
    errs = []
    ebom = defaultdict(list)
    for l in b.lines:
        ebom[l["parent"]].append((l["child"], l["qty"]))
    mbom = defaultdict(list)
    for o in ops:
        if o["work_center"] not in WORK_CENTERS:
            errs.append("mbom: %s op %s: unknown work centre" % (o["assembly"], o["op_no"]))
        if o["consumes"] and o["consumes"] not in b.parts:
            errs.append("mbom: %s consumes unknown part %s" % (o["assembly"], o["consumes"]))
        elif o["consumes"] and b.parts[o["consumes"]]["category"] != "CONS":
            mbom[o["assembly"]].append((o["consumes"], o["qty"]))
    for asm in set(ebom) | set(mbom):
        if sorted(ebom[asm]) != sorted(mbom[asm]):
            errs.append("mbom: %s does not consume exactly its EBOM lines" % asm)
    return errs


# -- software BOM -------------------------------------------------------------

REPO = HERE.parent.parent
# Two roles, kept apart. Reference implementations are the specifications the
# on-body code is checked against. Design tools produce and check the design;
# they are never part of the body, so CycloneDX scope "excluded" marks them.
REFERENCE, TOOL = "reference-implementation", "design-tool"
SBOM_SOURCES = [
    # path, CycloneDX type, role, description, depends on
    ("reference/audit_log.py", "library", REFERENCE, "Audit log: format, hash chain, Merkle batches, verifier", []),
    ("reference/agency.py", "library", REFERENCE, "Agency tagging by efference copy; golden model for the firmware port", ["reference/audit_log.py"]),
    ("hardware/electrical/actuator_sizing.py", "application", TOOL, "Joint torque table and actuator sizing", []),
    ("scripts/gems_budget.py", "application", TOOL, "Mass-energy-power budget model and spec check", ["hardware/electrical/actuator_sizing.py"]),
    ("protocol/assess.py", "application", TOOL, "Conformance assessment of the simulated body", ["reference/audit_log.py", "reference/agency.py", "scripts/gems_budget.py"]),
    ("hardware/sim-model/generate_urdf.py", "application", TOOL, "URDF generator and audit", []),
    ("hardware/bom/build_bom.py", "application", TOOL, "EBOM, MBOM and SBOM generator and check", ["hardware/electrical/actuator_sizing.py"]),
    ("realtime_config/check_timing.py", "application", TOOL, "Timing table check against the specification and the firmware architecture", []),
]


def build_sbom(timestamp):
    import hashlib
    import json
    comps, deps = [], []
    py = {"type": "platform", "bom-ref": "cpython", "name": "CPython",
          "version": ">=3.10", "description": "Python interpreter; standard library only, no third-party packages",
          "licenses": [{"license": {"id": "PSF-2.0"}}]}
    for path, typ, role, desc, needs in SBOM_SOURCES:
        digest = hashlib.sha256((REPO / path).read_bytes()).hexdigest()
        comps.append({
            "type": typ, "bom-ref": path, "name": path, "version": "sha256:" + digest[:12],
            "description": desc,
            "supplier": {"name": "Plone Mraz"},
            "licenses": [{"license": {"id": "Apache-2.0"}}],
            "hashes": [{"alg": "SHA-256", "content": digest}],
            "scope": "excluded" if role == TOOL else "optional",
            "properties": [{"name": "gems:role", "value": role}],
        })
        deps.append({"ref": path, "dependsOn": needs + ["cpython"]})
    comps.append(py)
    deps.append({"ref": "cpython", "dependsOn": []})
    doc = {
        "$schema": "http://cyclonedx.org/schema/bom-1.7.schema.json",
        "bomFormat": "CycloneDX", "specVersion": "1.7", "version": 1,
        "metadata": {
            "timestamp": timestamp,
            "authors": [{"name": "Plone Mraz"}],
            "component": {"type": "application", "bom-ref": "gems", "name": "GEMs repository code: reference implementations and design tools",
                          "supplier": {"name": "Plone Mraz"},
                          "licenses": [{"license": {"id": "Apache-2.0"}}]},
        },
        "components": comps,
        "dependencies": [{"ref": "gems", "dependsOn": [c[0] for c in SBOM_SOURCES]}] + deps,
    }
    return json.dumps(doc, indent=2) + "\n"


def sbom_equal(a, b_text):
    import json
    x, y = json.loads(a), json.loads(b_text)
    x["metadata"].pop("timestamp", None)
    y["metadata"].pop("timestamp", None)
    return x == y


# -- serialisation ----------------------------------------------------------

def to_csv(fields, rows):
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return s.getvalue()


def read_csv(path, fields):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != fields:
            raise SystemExit("%s: header must be %s" % (path.name, ",".join(fields)))
        return list(r)


# -- checks -------------------------------------------------------------------

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_structure(b, roots, consumed=()):
    errs = []
    children = defaultdict(list)
    for l in b.lines:
        for k in ("parent", "child"):
            if l[k] not in b.parts:
                errs.append("ebom: %s %s is not in parts" % (k, l[k]))
        children[l["parent"]].append(l)
        if l["qty"] == "" and not l["qty_basis"]:
            errs.append("ebom: %s under %s has no qty and no basis" % (l["child"], l["parent"]))
    used = {l["child"] for l in b.lines} | set(roots) | set(consumed)
    for pn, p in b.parts.items():
        if pn not in used:
            errs.append("parts: %s is not used by any assembly" % pn)
        if p["category"] not in CATEGORIES or p["maturity"] not in MATURITY:
            errs.append("parts: %s has an unknown category or maturity" % pn)
    # cycles
    state = {}

    def visit(pn):
        if state.get(pn) == 1:
            errs.append("ebom: cycle through %s" % pn)
            return
        if state.get(pn) == 2:
            return
        state[pn] = 1
        for l in children[pn]:
            visit(l["child"])
        state[pn] = 2
    for r in roots:
        visit(r)
    return errs, children


def check_avl(avl, parts):
    errs = []
    for i, a in enumerate(avl, start=2):
        w = "avl line %d (%s)" % (i, a["part_number"])
        p = parts.get(a["part_number"])
        if p is None:
            errs.append("%s: part number not in parts" % w)
            continue
        if a["status"] not in STATUS:
            errs.append("%s: status must be SELECTED or CANDIDATE" % w)
        if a["status"] == "SELECTED" and not (a["manufacturer"] and a["mpn"] and a["source_url"]):
            errs.append("%s: SELECTED needs manufacturer, mpn and source_url" % w)
        if p["maturity"] == "LAB" and a["mpn"]:
            errs.append("%s: a LAB part has no manufacturer part number" % w)
        price = [a[k] for k in ("unit_price", "currency", "price_qty", "price_date", "price_url")]
        if any(price) and not all(price):
            errs.append("%s: a price needs unit_price, currency, price_qty, price_date and price_url" % w)
        if a["price_date"] and not DATE_RE.match(a["price_date"]):
            errs.append("%s: price_date must be YYYY-MM-DD" % w)
    return errs


# -- views --------------------------------------------------------------------

def rollup(b, children, pn, qty_known=True):
    """Mass of one unit of pn: its own figure if it has one, else the sum of
    its children. Returns (kg, complete)."""
    p = b.parts[pn]
    if p["unit_mass_kg"]:
        return float(p["unit_mass_kg"]), True
    kg, complete = 0.0, bool(children[pn])
    for l in children[pn]:
        ckg, cc = rollup(b, children, l["child"])
        if l["qty"] == "":
            complete = False
            continue
        kg += ckg * float(l["qty"])
        complete = complete and cc
    return kg, complete


def indented(b, children, avl_by_pn, root):
    out = ["| Level | Find | Part number | Description | Qty | UoM | Cat | Maturity | Mass kg (unit) | AVL |",
           "|---|---|---|---|---|---|---|---|---|---|"]

    def walk(pn, level, find, qty):
        p = b.parts[pn]
        kg, ok = rollup(b, children, pn)
        mass = ("%.2f" % kg if ok else ("≥ %.2f" % kg if kg else "")) if (kg or ok) else ""
        a = avl_by_pn.get(pn, [])
        avl = ", ".join("%s %s" % (x["status"].lower(), x["mpn"] or x["manufacturer"]) for x in a)
        out.append("| %s | %s | `%s` | %s%s | %s | %s | %s | %s | %s | %s |" % (
            level, find, pn, "&nbsp;&nbsp;" * level, p["description"], qty or "—",
            p["uom"], p["category"], p["maturity"], mass, avl))
        for l in children[pn]:
            walk(l["child"], level + 1, l["find_no"], l["qty"])
    walk(root, 0, "", "1")
    return out


def summary(b, children, avl, top):
    kg, complete = rollup(b, children, top)
    n = len(b.parts)
    cats = defaultdict(int)
    for p in b.parts.values():
        cats[p["category"]] += 1
    lab = sum(p["maturity"] == "LAB" for p in b.parts.values())
    massed = sum(bool(p["unit_mass_kg"]) for p in b.parts.values())
    sel = {a["part_number"] for a in avl if a["status"] == "SELECTED"}
    cand = {a["part_number"] for a in avl if a["status"] == "CANDIDATE"} - sel
    priced = {a["part_number"] for a in avl if a["unit_price"]}
    return [
        "| | |", "|---|---|",
        "| Part numbers | %d (%s) |" % (n, ", ".join("%s %d" % kv for kv in sorted(cats.items()))),
        "| LAB parts — no part number exists to give | %d |" % lab,
        "| Parts with a selected manufacturer part | %d |" % len(sel),
        "| Parts with candidates only | %d |" % len(cand),
        "| Parts with a verified price | %d |" % len(priced),
        "| Parts with a mass figure | %d |" % massed,
        "| Body mass rolled up from known figures | %.1f kg of a %.1f kg budget — %s |" % (
            kg, BODY_MASS_BUDGET, "complete" if complete else "**incomplete**, blanks count as zero"),
    ]


def render_mbom(b, ops):
    md = ["# Manufacturing BOM — routings", "",
          "Generated by [`build_bom.py`](build_bom.py). Do not hand-edit; see "
          "[`README.md`](README.md#mbom). Every EBOM line is consumed by exactly one "
          "operation of its parent's routing; the check fails otherwise.", "",
          "## Work centres", "", "| Code | Work centre |", "|---|---|"]
    md += ["| `%s` | %s |" % kv for kv in WORK_CENTERS.items()]
    by = defaultdict(list)
    for o in ops:
        by[o["assembly"]].append(o)
    for asm in sorted(by):
        md += ["", "## `%s` %s" % (asm, b.parts[asm]["description"]), "",
               "| Op | Work centre | Operation | Consumes | Qty | UoM |",
               "|---|---|---|---|---|---|"]
        for o in by[asm]:
            md.append("| %s | `%s` | %s | %s | %s | %s |" % (
                o["op_no"], o["work_center"], o["operation"],
                "`%s`" % o["consumes"] if o["consumes"] else "",
                o["qty"] or ("—" if o["consumes"] else ""), o["uom"]))
    return "\n".join(md) + "\n"


def render(b, top, dock, avl, ops=()):
    errs, children = check_structure(b, [top, dock], {o["consumes"] for o in ops if o["consumes"]})
    by_pn = defaultdict(list)
    for a in avl:
        by_pn[a["part_number"]].append(a)
    md = ["# Engineering BOM — indented view", "",
          "Generated by [`build_bom.py`](build_bom.py) from `parts.csv`, `ebom.csv` and "
          "`avl.csv`. Do not hand-edit; see [`README.md`](README.md).", "",
          "## Summary", ""] + summary(b, children, avl, top) + [
          "", "## Body", ""] + indented(b, children, by_pn, top) + [
          "", "## Ground equipment", ""] + indented(b, children, by_pn, dock)
    return errs, "\n".join(md) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true", help="verify, write nothing")
    a = ap.parse_args(argv)

    from datetime import datetime, timezone
    b, top, dock = build()
    ops = build_mbom(b, [top, dock])
    parts_csv = to_csv(PART_FIELDS, list(b.parts.values()))
    ebom_csv = to_csv(EBOM_FIELDS, b.lines)
    avl = read_csv(HERE / "avl.csv", AVL_FIELDS)
    errs, md = render(b, top, dock, avl, ops)
    errs += check_avl(avl, b.parts)
    errs += check_mbom(b, ops)
    sbom = build_sbom(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    files = {"parts.csv": parts_csv, "ebom.csv": ebom_csv, "EBOM.md": md,
             "mbom.csv": to_csv(MBOM_FIELDS, ops), "MBOM.md": render_mbom(b, ops)}
    if a.check:
        for name, text in files.items():
            p = HERE / name
            if not p.exists() or p.read_text(encoding="utf-8") != text:
                errs.append("%s is out of date — run build_bom.py" % name)
        p = HERE / "sbom.cdx.json"
        if not p.exists() or not sbom_equal(p.read_text(encoding="utf-8"), sbom):
            errs.append("sbom.cdx.json is out of date — run build_bom.py")
    for e in errs:
        print("ERROR " + e)
    if errs:
        return 1
    if not a.check:
        for name, text in files.items():
            (HERE / name).write_text(text, encoding="utf-8")
        p = HERE / "sbom.cdx.json"
        if not p.exists() or not sbom_equal(p.read_text(encoding="utf-8"), sbom):
            p.write_text(sbom, encoding="utf-8")
    print("\n".join(l for l in summary(b, check_structure(b, [top, dock])[1], avl, top)
                    if l.startswith("| ") and not l.startswith("| |")))
    print("MBOM: %d operations across %d routings" % (len(ops), len({o["assembly"] for o in ops})))
    print("\n%s." % ("Checked; nothing written" if a.check else
                     "Wrote parts.csv, ebom.csv, EBOM.md, mbom.csv, MBOM.md, sbom.cdx.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
