# Plan — from specification to a complete design

What remains between this repository and a GEMs body that is **fully written down**: every part identified, every circuit drawn to the last passive, every line of firmware and software written, and all of it exercised in simulation.

| Document | Contents |
|---|---|
| This file | Definition of done, the levels of detail, the open decisions, and the work packages for industrial and expressive design, mechanical, electrical, simulation and costing |
| [`firmware.md`](firmware.md) | Firmware work, module by module, down to the task |
| [`software.md`](software.md) | Software work, module by module, down to the task |

---

## 1. What "done" means here

GEMs is specified at the ceiling of current science and technology, not at the level of a budget. **The target is a complete design, not a built body.** A design is complete when a competent team with funding could procure, fabricate and assemble it without making a design decision of their own.

Physical validation is out of reach and is not claimed. Verification is by simulation — mechanical, electrical, thermal, and the full body in a physics engine — and every simulated result says it is simulated, as [protocol §4](../protocol/conformance.md) already requires.

### Levels of detail

Every item in this plan is tracked against the same ladder.

| Level | Name | An item is at this level when |
|---|---|---|
| **L0** | Specified | The envelope it must meet is stated in `spec/` |
| **L1** | Architected | Its role, interfaces and budgets (mass, power, data, time) are fixed |
| **L2** | Selected | The technology or part family is chosen, with a source |
| **L3** | Identified | A manufacturer part number — or, for custom parts, a drawing number — exists, with quantity, source, and price or "quote only" |
| **L4** | Designed | Schematic and layout to every passive, CAD to every fastener, or source code that builds |
| **L5** | Verified in simulation | A simulation exercises it against its L0 envelope and the result is recorded |

**Done is L5 everywhere it can be reached, and an honest L4 everywhere else.**

### Where L3 cannot be reached

The specification admits laboratory technology where the physics exists but the product does not (see [spec 00](../spec/00-scope-and-criteria.md)). For items marked **LAB** there is no part number to identify. Their L3 is a *reference design traced to a cited publication*, and their L4 is our own design of whatever surrounds them — readout, drive electronics, mounting — drawn to the same standard as everything else. The plan marks these rows so that they cannot be mistaken for purchasable items.

---

## 2. Where the repository stands

| Subsystem | Level reached | Evidence |
|---|---|---|
| Envelopes, mass–energy loop | L0–L1 | `spec/`, `scripts/gems_budget.py --check` |
| Kinematics, 31 core DOF; mechanical range-of-motion targets | L1 | `hardware/kinematics.md` |
| Actuators, cells, compute, bus, materials | **L2** | `hardware/electrical/`, `hardware/mechanical/` |
| Audit log, agency tagging | **L4** in reference form | `reference/`, 36 tests |
| Firmware | L1 | `firmware/ARCHITECTURE.md` |
| Kinematic simulation model | L4 for kinematics only | `hardware/sim-model/` — inertias estimated |
| Everything else | L0 | — |

No item is at L3. The engineering BOM exists — [`hardware/bom/`](../hardware/bom/), 206 part numbers in a multi-level structure, with MBOM routings and an SBOM — with one selected manufacturer part and one verified price (the AKH70-16, [`avl.csv`](../hardware/bom/avl.csv)).

---

## 3. Decisions that block everything else

These are ordered: each one is needed before the work packages that depend on it can move past L2. None can be settled by arithmetic alone.

| # | Decision | Blocks | Status |
|---|---|---|---|
| **D-1** | **Knee torque requirement.** The sizing script assumes knee = hip pitch, flagged there as an assumption, not a source | Actuator sizing, `f_act`, the mass loop | **checked 2026-11-21 against published gait data: 1.77 Nm/kg stands** — it covers walking, stairs and rising from a seat; since 2026-11-23 the knee is sized to running instead, 2.79 Nm/kg (spec 02.6 row 5), and 1.77 remains hip pitch and what a stand-up asks ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)). Open within it: rising from a deep squat or the floor, and landing — no figure obtained |
| **D-2** | **Actuators: which procured modules, at which reduction ratio.** In-house design is off the table by rule ([`CLAUDE.md`](../CLAUDE.md) §2, 2026-09-26): every option must be bought. The same CubeMars motor is sold at 16:1 (78 Nm peak, 105 rpm, 88.7 Nm/kg) and 48:1 (222 Nm peak, ~48 rpm, 159 Nm/kg), so torque density is a ratio choice paid in speed, and the open question per joint is *torque × speed*, not torque alone ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)). At 48:1 only hip pitch, knee and trunk pitch fall short, by 4–8 Nm; whether ~5 rad/s at the output is enough for gait and fall recovery is unmeasured. Also settles the conflict between the per-class reducers of `hardware/mechanical` and the single module family of `hardware/electrical`, and the CAN-to-EtherCAT question of E-5 | M-3, E-3, F-3 | open — researched 2026-11-22 ([electrical §6d](../hardware/electrical/README.md#6d-actuator-candidates--d-2-2026-11-22)): the knee needs speed as well as torque, about 6.7 rad/s in the swing of ordinary walking, which the AVL's AKH70-48 does not reach; four bought candidates read from their datasheets, planetary and cycloidal. The author's to decide: the figures of the [motion envelope](../spec/02-structure-and-motion.md#motion-envelope) (listed 2026-11-22: walking over a region of cadence and step length, its top speed 1.0 m/s since 2026-11-23, running and jumping in open space only, balance recovery and a controlled fall in every mode, other demanding motions still to be listed; running and balance recovery researched in [electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22) and declared 2026-11-22: running to 2.5 m/s for 60 s, faster running `OPEN`; a push of 1.0 m/s fore and aft, 0.5 m/s sideways. With them and the modules declared 2026-11-23 ([spec 02.6](../spec/02-structure-and-motion.md#the-basis-matters-as-much-as-the-number)), the body is 107.0 kg and the knee asks 299 Nm peak, 11 rad/s at about 50 Nm and 103 Nm RMS for 60 s, the ankle 221 Nm), and the bus and supply voltage that follow. The reducer class at hip and knee is settled (2026-11-22): cycloidal or planetary, not strain-wave ([mechanical §2](../hardware/mechanical/README.md#2-reducers-by-joint-class)). The direction is picked (2026-11-23): ENCOS EC-A10020-P2-24 is the main candidate at hip pitch, knee and trunk pitch, RMD-X12-P20-320 and PhyArc 102 the alternates (PhyArc only on a 72 V bus); the other joint classes are matched but not picked. Matching every joint to a bought module put the body at 84–103 kg, not 82.3: the declared density was a module's, and bought modules come in steps ([electrical §6d](../hardware/electrical/README.md#6d-actuator-candidates--d-2-2026-11-22)). **Decided 2026-11-23 (Plone): the module is declared at each joint**, the lightest that passes the rank-1 rule — its maker's sheet gives peak and hold time, continuous torque, speed at 48 V, mass and size — and meets the joint, running's 60 s included ([electrical §6f](../hardware/electrical/README.md#6f-modules-declared-at-the-joint--d-2-2026-11-23)): 13 sheets of 11 makers read, three pass (ENCOS, SEmotor, MyActuator); the knee takes ENCOS EC-A13715-P1-12.67, which holds 150 Nm for 60 s on its maker's bench, and the body is 98.2 kg. **Added 2026-11-23 (Plone): walking's RMS and the hip's frontal plane** ([electrical §6g](../hardware/electrical/README.md#6g-walking-rms-and-the-frontal-plane--d-2-2026-11-23)): at 98.2 kg the hip's SEmotor modules walked at 1.3 and 2.9–3.3 times their continuous torque, and running asks hip roll 170 Nm against its 156 Nm peak. Walking's RMS at every leg and trunk joint is now checked against the continuous torque, and hip roll is sized to running's frontal plane, 1.73 Nm/kg; hip pitch and hip roll take the EC-A10020-P2-24, ankle pitch the RMD-X12-P20-320, trunk yaw the EC-A6416-P2-25, and the body is 105.6 kg, `f_act` 0.348. **Changed 2026-11-24 (Plone): the legs' walking figures are people's** (Fukuchi et al. 2018, the 90th percentile at 1.0 m/s; [electrical §6j](../hardware/electrical/README.md#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)), with a human-like gait asked of F-5, and the robot's gait, the stress case, required of the leg modules as well: the set and the 105.6 kg stand. On people's figures alone hip pitch would have taken the SETZ90CI-1FG, 103.6 kg (commit 4d98ce1, the same day), which does not hold the stress case and carries 32 kg in a stand-up against 75; Plone chose the P2-24. **Decided 2026-11-24 (Plone): static holds** — 2 s at most at full reach, 10 s picking up and setting down, longer only close to the body ([spec 02.6](../spec/02-structure-and-motion.md#static-holds), [electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)). SEmotor's sheet gives nothing between a 1 s peak and its continuous torque, so the elbow and shoulder yaw take the EC-A8116-P1-18, at 18:1 by exception to the arm's 6:1–15:1, and trunk pitch the EC-A10020-P2-24; the body is 107.0 kg, `f_act` 0.351, and the top of spec 02.2's band was raised from 0.35 to 0.36. The set holds to 108.8 kg. Open: SEmotor's losses at trunk roll and the X12's time under load; the shoulder's hold at 108 Nm for 2 s; a squat or a kneel held; the trunk's walking figures, still the simulated robot's; none procured |
| **D-3** | **Real-time computer, which carries the Real-time Control Layer: a microcontroller under an RTOS, or an embedded computer under Linux with a real-time kernel.** The Jetson carries perception and compression; it is not the target for the 500 Hz balance loop and the 10 ms reflex path. The choice decides whether that code is firmware or software (spec 07.1), and how its latency bound is established — by construction or by measurement | All firmware, E-5 | open |
| **D-4** | **High-voltage bus voltage** | Every power stage, cell count in series, harness gauge | open |
| **D-5** | **Cell and pack format** at the durable tier (400–500 Wh/kg). Solid-state preferred, not required ([spec 03.1](../spec/03-energy.md#31-source), 2026-11-05); on sale today only as silicon-anode. The choice fixes the tier's `⟦IMPL⟧` figures — cycle life, discharge rate, and the abuse test the pack must pass | Pack mechanics, BMS, thermal | open — candidates sourced in `hardware/electrical/` |
| **D-6** | **Reference hand configuration.** The declaration leaves 2×5 to 2×21 DOF open (`⟦CTRL⟧`); a complete design needs one point to draw | M-4, E-3 count, F-3 count | open — anchor figure is 40 joints, i.e. 2×5 |
| **D-7** | **Secure element and low-power beacon radio** | Attestation, beacon, C-10, C-11 | open |
| **D-8** | **Operating point for the reference design** — endurance, height, armour | Mass, pack size, every downstream figure | **decided 2026-09-26, in part: 2 h free-running with a dock, and 1.65 m** (was 4 h, 1.75 m). The body came to ~96 kg; on 2026-11-23, with the knee and ankle sized to running and the legs and trunk declared at 133 Nm/kg, ~82 kg; with a bought module declared at each joint, ~98 kg; since the same day, with walking's RMS and the hip's frontal plane in the module check, it was ~106 kg; since 2026-11-24, with static holds in it, it is **~107 kg**, and the legs carry 74 kg in a stand-up, limited by the knee's module ([spec 02.6](../spec/02-structure-and-motion.md#load-cases)). Open within it: armour coverage and level — the reference keeps 65% until discussed. The dock is now load-bearing for the design: package DK |
| **D-9** | **Trunk architecture** | M-5, E-3, F-5, the URDF | **decided 2026-09-26: a coupled multi-segment spine** — three segments, one actuator per axis for yaw, pitch and lateral bend ([kinematics §1.4](../hardware/kinematics.md#14-the-trunk-is-a-spine-not-a-waist)). Open within it: the coupling mechanism and ratios. All three trunk axes are sized from Pan et al. 2025 |
| **D-10** | **Arm payload** | Shoulder and elbow sizing, `f_act`, the mass loop | **decided 2026-09-26: 15 kg in one hand, arm horizontal, load at the grip centre; shoulder roll 11 kg** ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)). Replaced a 30 kg fingertip stress test. With it `f_act` splits into a scaling part (legs, trunk) and a fixed part (arms, wrists, neck) carried in `m_ext`; the density floor stays at 80 Nm/kg as margin |
| **D-11** | **Load cases** | Leg and trunk sizing, carry capacity, D-8 | **decided 2026-09-26: static objects only; lifting, carrying or dragging a person is out, contact stays in** ([spec 02.6](../spec/02-structure-and-motion.md#load-cases)). A held load adds to the leg and trunk per-kg rows. Open within it: the masses of the four proposed cases |

D-6 and D-8 are choices of *which* point to draw, not changes to the specification: the specification keeps its ranges, and a reference design declares the one it drew.

---

## 4. Work packages

Every package lists its tasks, the level it takes its subject to, and what it waits for. IDs are stable so that commits and issues can name them.

### ID — Industrial and expressive design

How the body looks, and how it can show things. Two halves that share one surface: the **form** — proportion, silhouette, colour, material and finish — and the **expressive capability** — face, gaze and posture as a set of controllable degrees of freedom with ranges and speeds.

**Scope boundary kept.** This package specifies what the body *can* express, never *when* or *why* it does. Choosing an expression is the controller's, and the controller is not specified here ([README](../README.md#scope-boundary)).

Two standard references anchor it. The **Facial Action Coding System** (Ekman and Friesen, 1978) is the vocabulary for facial movement, and robot heads have been designed around its action units [Yan et al., 2014](https://onlinelibrary.wiley.com/doi/10.1155/2014/208924). The **uncanny valley** (Mori) is the design risk: a face that nearly but not quite passes as human is received worse than one that does not try.

| ID | Task | To | Waits for |
|---|---|---|---|
| ID-1 | Design brief: proportions from `kinematics.md`, the gynoid form, the uncanny-valley position the design takes and why; starting from the author's [concept art](../hardware/design/concept/) and its tensions with the specification. One tension is already visible: the concept's slender legs against what a leg segment must hold — an actuator module at hip and knee (the AVL's CubeMars AKH70-48 is Ø90 × 81.5 mm on its vendor drawing), the armour shell (spec 02.4, 04.2) with padding beneath and tactile skin and textile above (spec 04.5); the URDF, whose radii follow proportion rather than structure, already draws the thigh at a 58 mm radius. The brief decides which gives: the form, or what is inside it | L1 | — |
| ID-2 | Form development: silhouette and proportion studies, form language, then class-A outer surfaces in CAD. Constraints: the thickness of the three shell layers (spec 04.5), armour coverage (spec 02.4), textile at the joints (spec 04.3), joint range of motion from the URDF | L4 | ID-1, M-1, D-3, D-4 |
| ID-3 | Human-contact surfaces: pinch-point elimination at every joint, contact zones for safe touch (spec 01 group 4), lift and handling points | L4 | ID-2 |
| ID-4 | Colour, material and finish by zone, within what the shell allows: a textile outer layer over the whole body, colour fixed — dyed or printed — and the fabric's flame resistance (spec 04.3, 04.4); where the concept's gloss and panel lines can and cannot carry through | L4 | ID-2, M-8 |
| ID-5 | Face: static geometry, eyes, skin; the FACS action units the face will actuate, which fixes the count of facial actuators (EBOM `GEM-11090`) | L4 | ID-1 — **LAB** |
| ID-6 | Expressive capability specification: range, speed and simultaneity per action unit; gaze from neck and eyes; posture. Colour change as a slow channel is `UPG` (spec 04.7) | L4 | ID-5 |
| ID-7 | Visual model: renders and a textured visual model for the simulator, replacing the primitives of `sim-model/`. Trunk and limbs first, from the surfaces of ID-2; face (ID-5) and hands (M-4) after them, being the finest and the least settled. The model is cut into one mesh per URDF link at the joint boundaries, each in its link's frame and reduced for display, and `generate_urdf.py` points its `<visual>` at them; `<collision>` stays primitive. A base mesh is used only under an open licence recorded beside it; meshes made from a vendor's CAD of a bought part are not published unless the vendor's terms allow it (CubeMars marks its drawings proprietary and confidential) — a bought part is drawn by its envelope | L4 | ID-2, ID-9 |
| ID-8 | Evaluation without hardware: a rendered-stimulus perception study protocol for the face and form — the protocol and stimuli are in scope, running it needs people | L5 | ID-6, ID-7 |
| ID-9 | Tooling for form and the visual model: Blender, for freeform surfaces, materials, renders and glTF / OBJ / DAE export, driven by its Python API; an MCP server for it is read and checked before use, as freecad-mcp was for FreeCAD (2026-11-21). FreeCAD stays the tool of M-1 and of every dimensioned part — ✅ 2026-11-21: Blender 5.3 with the Blender Lab MCP (add-on 1.0.0, server 1.0.2, GPL-3.0), read in full before install: no telemetry, no network beyond its socket on localhost; run over stdio, never its HTTP transport, which drops DNS-rebinding protection. Not taken: `mcp-for-blender`, which sends a usage record by default and, on opt-in, prompts and scenes for model training | — | — |

### M — Mechanical

| ID | Task | To | Waits for |
|---|---|---|---|
| M-1 | Parametric CAD skeleton generated from `kinematics.md`, the same way the URDF is — joint frames, segment envelopes, keep-out volumes. In FreeCAD (1.1), by a generator script beside `generate_urdf.py` with an audit that holds the CAD and the URDF to the same declaration — ◐ [`hardware/mechanical/skeleton/`](../hardware/mechanical/skeleton/), 2026-11-21: joint frames and segment envelopes generated and audited; 2026-11-22: swept keep-out volumes, 16, audited at 282 poses; 2026-11-23: joint-module keep-outs at hip pitch, knee and trunk pitch, audited on the joint axis and against the modules spec 02.6 declares there (ENCOS EC-A10020-P2-24 Φ124 × 85, ENCOS EC-A13715-P1-12.67 Φ170 × 73, and at trunk pitch the EC-A10020-P2-24 again since 2026-11-24); the other 26 joints' modules are declared, their keep-outs not yet built | L4 | — |
| M-2 | Packaging study: where the pack, compute, drives, radios and sensors sit, checked against segment envelopes, the outer form and the centre of mass. The hip joints stay 0.18 m apart, centre to centre (kinematics §2, 2026-11-24): hip roll's walking torque grows with the spacing ([electrical §6h](../hardware/electrical/README.md#6h-walking-heat-by-speed-and-the-hip-roll-lever--m-11-2026-11-24)), and three modules per side meet at each hip's centre. **Pack location decided: the scapular region of the upper back, on the torso frame** — see [pack location](#pack-location-decided) below | L1 | D-4, D-5, ID-2 |
| M-3 | Joint modules per class — hip/knee (cycloidal or planetary, not strain-wave), shoulder/elbow (QDD planetary), wrist/neck (harmonic): bearings, seals, encoder mounts, joint locks (spec 03.2 measure 4), series-elastic elements (measure 5) | L4 | D-1, D-2 |
| M-4 | Hands at the reference configuration | L4 | D-6 |
| M-5 | Structure per segment — composite tubes, 7075 load-introduction fittings, fastener schedule | L4 | M-2, M-3 |
| M-6 | Structural FEA per segment against peak joint loads and a fall case | L5 | M-5 |
| M-7 | Armour shell — hybrid laminate moulded per segment in one part, UHMWPE plies with co-moulded aramid spike plies, NIJ HG2 + spike level 1, tested to and not certified (spec 04.2), with the aramid plies on the outer face and the UHMWPE behind: panel layout at the declared coverage, the moulds, the moulder's areal density, the use-temperature limit of SJ100-240H itself, and a spike level 1 test in that ply order | L4 | D-8 |
| M-8 | Shell, three layers (spec 04.5) on the surfaces of ID-2: impact padding — certified protectors at knees, elbows, shoulders, hips and back, held at EN 1621-1 Level 2 and EN 1621-2 Level 1 (2026-11-23, provisional), how they are held on the body, the back protector's size, and the fall model that confirms or replaces that anchor; foam at pinch points and its thickness, kept between the armour shell and hot modules so that the shell stays below its UHMWPE's ≤ 70 °C, and whether the protectors can lie on modules at up to 100 °C, with M-11 (spec 04.1); the armour shell of M-7; the tactile skin laid on it under a removable textile cover; at the joints the shell stops and the textile carries on, and whether the skin crosses them is decided here. The armour shell has no fire standard of its own (spec 04.4) | L4 | M-7, ID-2 |
| M-9 | Head and sensor mounting — stereo baseline, thermal, LiDAR, microphone array geometry, inside the face of ID-5 | L4 | E-6, ID-5 |
| M-10 | Dock, mechanical — moved to package DK below | — | — |
| M-11 | Thermal design — forced-air ventilation to [spec 04.8](../spec/04-shell.md#48-ventilation-and-surface-temperature) (2026-11-24): one main path from the pelvis flanks along the spine to the upper back, local loops at knees and ankles, a cool branch for pack and compute, shrouds and fans at the hot modules, no liquid; ambient 20–40 °C, simulated at 30–35 °C in a thermal network that sizes the flow of each zone; contact surfaces at 48 °C, the palms and the front of the trunk at 36 °C; the fans bought, their noise discussed with the search; a bought filter layer on every slot, its pressure drop in the fan sizing, clogging seen by the firmware from fan power against module temperature, and a maintenance procedure with its replacement interval; a cold store recharged at the dock, an option. Mainly indoors; water open. Sized by the thermal network: on people's gait ([electrical §6j](../hardware/electrical/README.md#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)) ~88 CFM at 0.5 m/s and ~104 at 1.0 (at 107.0 kg, [electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)), the hips and knee within their makers' benches, the ankle pitch's X12 the hottest at 108–117 W each and 96% of its rated torque, with no bench figure; on the robot's gait, the stress case the fans are sized for ([electrical §6i](../hardware/electrical/README.md#6i-thermal-network-of-the-ventilated-body--m-11-2026-11-24)), ~92 and ~152 CFM, hip pitch, left hip roll and left knee 1.5–1.8× better than their benches. **First ask of ENCOS: the winding-to-housing thermal resistance of the P2-24 and EC-A13715**, which decides whether air alone can do it; else measure it on a module. Decided 2026-11-24: noise at most 57 dB(A) at 1 m from all the fans at full flow, and about 16 × 10 cm of filter at each pelvis flank and each exhaust, the filters at ~1 m/s. Exhaust at the upper back, over the pack — see [pack location](#pack-location-decided) below. Sized for walking at 0.5 m/s sustained and 1.0 m/s for 10 min (spec 02.6 row 1, 2026-11-24), which rest on it: on the robot's gait the joints' heat is about 1.1 kW at 1.0 m/s and 0.6 kW at 0.5, of which the six hip modules are about 470 and 290 W, the body's largest source; on people's about 0.69 and 0.56 kW, 348 and 312 W of it in the knees and ankles and 196 and 173 in the hips ([electrical §6j](../hardware/electrical/README.md#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)). The hips lie at the pelvis, away from the exhaust path ([electrical §6h](../hardware/electrical/README.md#6h-walking-heat-by-speed-and-the-hip-roll-lever--m-11-2026-11-24)) | L5 | M-2, E-3, E-5 |
| M-12 | Mass properties exported from CAD into the simulation model, replacing the estimated inertias | L5 | M-5 |

#### Pack location, decided

The author's decision, 2026-09-26: **the battery pack sits in the scapular region of the upper back, on the torso frame** — not on the arms, and not in the waist or pelvis. It frees the waist the concept art asks for ([`hardware/design/concept/`](../hardware/design/concept/)), and it places the body's largest heat source where an exhaust is easiest to design.

What the decision costs, at the declared point (URDF geometry at 1.65 m: pelvis centre ~0.94 m above the sole, scapular region ~1.30 m), and how the cost falls as cells improve — `gems_budget.py` at the D-8 point, 2 h and 65% coverage, with the bought modules of spec 02.6 (2026-11-23):

| Cell energy density | Body | Pack | Centre of mass raised by moving the pack from pelvis to upper back |
|---|---|---|---|
| 450 Wh/kg — durable tier, today | 107.0 kg | 9.5 kg, 4.3 kWh | ~3 cm |
| 550 Wh/kg | 102.7 kg | 7.5 kg | ~3 cm |
| 700 Wh/kg — low end of the ceiling tier (spec 03.1) | 98.8 kg | 5.6 kg | ~2 cm |
| 1000 Wh/kg | 94.8 kg | 3.8 kg | ~1 cm |

(At the 4 h point this section was written for, the pack was 23 kg and the shift ~6 cm; the move to 2 h on 2026-09-26 took most of the cost away.)

The pack shrinks faster than the energy it holds would suggest, because the mass loop compounds: a lighter pack makes a lighter body, which needs less pack. Two things do not improve with it. The ceiling tier trades rate for density (spec 02.7, 03.1), so the peak-power shortfall widens; and its cycle life is presently ~100 cycles. A denser cell is not free — it moves the problem.

Constraints the decision carries into the design:

| | |
|---|---|
| **Trunk load** | Pack mass high above the waist adds pitch inertia about the waist (~0.6 kg·m² at 7.3 kg, against ~3.7 kg·m² estimated for the 1.75 m torso — under +20%; ~1.8 kg·m² and +50% at the 23 kg pack of the old 4 h point). Trunk pitch, 186 Nm at the reference point, is sized with it; the pack rides the top spine segment, so the spine turns beneath it |
| **Impact protection** | A pack frame with a crush zone between the outer shell and the cells, so that an impact reaches the cells as shock within their qualified level, never as deformation or penetration — the path to thermal runaway. The upper back has the volume for that crush zone; the waist, in the concept's form, does not |
| **Falls** | The upper back is among the first regions to land in a backward fall, at speed. **Verification requirement (V-4):** the pack survives the worst-case backward fall from standing with no cell deformation and cell acceleration within the qualified shock level. The supported failure state (spec 07.3 g2) should still favour falls that spare the back |
| **Strikes** | The flank and waist are primary targets for kicks and knees; many combat rule sets forbid strikes to the spine and the back of the head. The upper back is the least-struck region of the torso |
| **Dock** | The default dock is a seat carrying the body through the pelvis (spec 03.5). A pack in the upper back is never loaded by sitting, and the charging contacts can sit in the backrest, next to the pack |
| **Cooling exhaust** | Up and out at the upper back, where warm air leaves naturally. Since 2026-11-24 ([spec 04.8](../spec/04-shell.md#48-ventilation-and-surface-temperature)): louvred openings either side of the spine near the neck, about 16 × 10 cm of filter each, turning the air rearward and down; intake at the flanks of the pelvis, just above the hips, the same size. Exhaust points away from the face and head sensors |
| **Thermal-runaway venting** | A separate path from cooling, and never toward the head. Runaway gas is directed down and away from the body |
| **Sealing and armour** | Openings in the torso break the seal and the armour; the torso is in every coverage band (spec 02.4). Baffled or labyrinth openings behind the protection layer. The body is ventilated, not sealed (2026-11-24, spec 04.8): dust is kept out by a filter layer on every slot, with periodic maintenance; protection against water is open |
| **Compute placement** | The edge module (40–130 W) is not placed upstream of the cells in the airflow — cells keep a lower temperature window than compute. Both sit in a cool branch of their own, not downstream of the hips (spec 04.8), and not behind the front of the trunk, which is held to 36 °C |

### E — Electrical

| ID | Task | To | Waits for |
|---|---|---|---|
| E-1 | System block diagram: every board, every bus, every power rail, every connector | L1 | D-3, D-4 |
| E-2 | Power: pack, BMS, pre-charge and contactor, fusing, supercapacitor tier (spec 03.2 measure 3), regeneration path, dock charger interface. The BMS and the dock charger are bought and wired to each other over CAN, the charger running under the BMS (candidates in the AVL) | L4 | D-4, D-5 |
| E-3 | Joint bus integration. The drive board is inside the bought actuator module (D-2; [`CLAUDE.md`](../CLAUDE.md) §2): what is designed here is how the modules reach the real-time computer — CAN bus segments, how many joints per segment at the balance rate, the bought CAN-to-EtherCAT bridges (none if D-2's module speaks EtherCAT), the joint torque sensors' interface, the brake and lock wiring. The bridge's latency counts in the 4.0 ms command stage of the reflex budget | L4 | D-2, D-4 |
| E-4 | Power distribution and conversion: HV to logic rails, isolated domains, the always-on rail at quiescent power (spec 03.6). Converters and regulators are bought modules; what is designed here is which rails, from which module, through which fuses and harness | L4 | E-2 |
| E-5 | Compute: Jetson carrier, real-time computer, EtherCAT master interface, storage for the audit log, and the OBC (spec 07.5) — all bought; what is designed here is their packaging, wiring and cooling in the torso | L4 | D-3 |
| E-6 | Sensor front-ends: camera links, thermal, LiDAR, microphone array, SDR, IMUs, e-nose, through bought interface boards | L4 | E-5 |
| E-7 | Tactile: the baseline's bought skin, ~43,000 points at 60 Hz with its own edge computing on CAN FD, and the hands' bought modules (spec 04.3, 04.6) — bus, power and placement. The readout for the ~460,000 taxels of spec 05.2 is `UPG`: nothing on sale was found (2026-11-05); research systems reach about 8,000 taxels. Not designed here ([`CLAUDE.md`](../CLAUDE.md) §2) | L4 | M-8, D-6 |
| E-8 | Radios: mmWave uplink, fallback link, low-power beacon radio | L4 | D-7 |
| E-9 | Root of trust: secure element per node or per bus segment | L4 | D-7 |
| E-10 | Shell drivers: magnetorheological coils or electrorheological high-voltage supply, electrochromic drivers. `UPG`: the layers they drive are on the upgrade path (spec 04.7), and the baseline has none to drive | — | `UPG` |
| E-11 | Contact-amplitude instrumentation (spec 06.6) | L4 | E-7 |
| E-12 | Harness: every cable, gauge, connector, length, routed through the CAD | L4 | M-5, E-1 |
| E-13 | Circuit simulation of the integration, from the bought parts' models: rail sequencing, inrush and pre-charge, voltage sag at peak draw, in SPICE | L5 | E-2 … E-4 |
| E-14 | Power and energy budget rebuilt from part datasheets, checked against spec 02 and 03 | L5 | E-2 … E-10 |

### F — Firmware

See [`firmware.md`](firmware.md). Waits for D-3 to reach L4; the parts that do not depend on a target — algorithms, state machines, protocols — can be written now and run in simulation.

### S — Software

See [`software.md`](software.md). Needs no hardware decision and can proceed now.

### V — Simulation and verification

| ID | Task | To | Waits for |
|---|---|---|---|
| V-1 | Full-body physics model with actuator models (torque–speed, current limits, reducer efficiency, backlash) | L5 | M-12, D-2 |
| V-2 | Battery and power model: state of charge, voltage sag at peak draw, the 5C peak of spec 02.7 | L5 | E-2 |
| V-3 | Balance and gait in simulation at ≥ 500 Hz, driven by the firmware's own controller code | L5 | F-5 |
| V-4 | Fall and supported failure state (C-16), including the backward-fall case for the pack (see [pack location](#pack-location-decided)) | L5 | F-8 |
| V-5 | Software-in-the-loop: firmware built for the host, stepping against the physics model | L5 | F-0 |
| V-6 | Emulated target: firmware built for the real processor, run in an instruction-set emulator against the physics model | L5 | D-3 |
| V-7 | Sensor simulation: rendered cameras, depth, IMU noise, tactile contact, for the software pipeline | L5 | S-1 |
| V-8 | Link simulation: bandwidth, latency, outage, for link management | L5 | S-5 |
| V-9 | Conformance re-assessment: rerun `protocol/assess.py` with each simulated result, and state which rows moved and why | L5 | all |

### DK — Dock

With the reference point at 2 h free-running (D-8), the dock is part of the design, not an accessory: the body's day is a sequence of free-running spans and dock returns, and nothing in the repository designs the dock yet. Spec [03.5](../spec/03-energy.md#35-dock) declares its forms (seat or couch by default, load-bearing hanger for storage) and both charging methods; the pack-location decision above puts the contacts in the backrest.

| ID | Task | To | Waits for |
|---|---|---|---|
| DK-1 | Requirements: charge power and time to full against the 3.3 kWh pack, how many returns a day at the declared power profile, wired and wireless roles (spec 03.5), where a body may dock, what state it holds while docked (spec 03.4 levels 3 and 4) | L1 | D-8 |
| DK-2 | Seat form: pelvis support and rise-from-seat path against the ROM tiers, backrest contacts beside the pack, alignment and self-docking tolerance, the hanger variant | L4 | DK-1, ID-2, M-2 |
| DK-3 | Dock electrical: charger, contact set and its safety (dead contacts until mated), wireless pad as the maintenance path, thermal handling of charge power, mains side | L4 | DK-1, D-4, D-5, E-2 |
| DK-4 | Dock-side control and telemetry: detection and handshake with F-9, charge control, the beacon read while docked (spec 06.5) | L4 | DK-3, F-9 |
| DK-5 | Simulated dock cycle: walk to dock, sit, charge, rise — endurance per day measured, not assumed | L5 | V-3, DK-2 |

### B — Bill of materials and cost

| ID | Task | To | Waits for |
|---|---|---|---|
| B-1 | BOM format: part, manufacturer, part number, quantity, source link, unit price, currency, date priced, maturity — ✅ [`hardware/bom/`](../hardware/bom/): EBOM, MBOM, SBOM, item master, AVL | — | — |
| B-2 | Price what is already selected at L2 — actuator modules, cells, compute, EtherCAT and CAN FD parts, materials | L3 | B-1 |
| B-3 | Extend the BOM as each work package reaches L3 | L3 | each package |
| B-4 | Cost roll-up by subsystem, with "quote only" and **LAB** rows counted separately rather than guessed | L3 | B-3 |

Prices are recorded with the date they were read and the page they were read from. A price that could not be found is left empty and says so.

---

### R — Open research

Studies the author has asked for that are not in the baseline. No decision rests on them, and nothing in the specification reserves a place for them until one is taken in.

| ID | Study | To | Waits for |
|---|---|---|---|
| R-1 | **Wheeled locomotion** (Plone, 2026-11-24): powered wheels, four under each foot, retracted into the foot and let down only for long travel on flat ground. Why: on wheels both feet stay on the ground, so the hips never carry the body in single support; standing, the simulated robot's hip roll gives 7–26 W, against 76–97 W walking at 1.0 m/s ([electrical §6h](../hardware/electrical/README.md#6h-walking-heat-by-speed-and-the-hip-roll-lever--m-11-2026-11-24)). To find: bought in-wheel motors, and a bought actuator for the retraction, inside a foot the URDF draws at 0.095 × 0.25 × 0.066 m; the mass at the foot, which raises the hip and knee torques of swing and is multiplied by `γ`; steering, braking and the stopping distance near people; contact sensing at the sole; how the body changes between rolling and walking. Wheel-legged humanoids built so far not yet read | L1 | D-2, M-2 |

## 5. Order of work

Nothing here waits for money. What waits is decisions.

1. **D-1**, the knee torque, first — it is the one open figure that could stop the mass loop from converging, and it is cheap to settle. Checked 2026-11-21: the figure stands for the declared tasks.
2. **D-2 to D-5**, with **B-2** alongside, because pricing the candidates is part of choosing between them.
3. **S** work in parallel from now: it needs no hardware. **ID-1** and **ID-5** can start now as well — the brief and the face depend on the kinematics and the specification, not on parts — and so can **M-1**, which needs only `kinematics.md`, and **ID-9**, which waits for nothing.
4. **E-1**, **ID-2**, and the target-independent parts of **F**, once D-3 and D-4 are settled. Form and packaging iterate against each other from here: neither is fixed first.
5. Detailed design — M-3 to M-11, E-2 to E-12, F source against the target.
6. Verification — V-1 to V-9 — as each piece reaches L4, not at the end.
