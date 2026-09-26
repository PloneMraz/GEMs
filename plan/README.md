# Plan — from specification to a complete design

What remains between this repository and a GEMs body that is **fully written
down**: every part identified, every circuit drawn to the last passive, every
line of firmware and software written, and all of it exercised in simulation.

| Document | Contents |
|---|---|
| This file | Definition of done, the levels of detail, the open decisions, and the work packages for mechanical, electrical, simulation and costing |
| [`firmware.md`](firmware.md) | Firmware work, module by module, down to the task |
| [`software.md`](software.md) | Software work, module by module, down to the task |

---

## 1. What "done" means here

GEMs is specified at the ceiling of current science and technology, not at the
level of a budget. **The target is a complete design, not a built body.** A
design is complete when a competent team with funding could procure, fabricate
and assemble it without making a design decision of their own.

Physical validation is out of reach and is not claimed. Verification is by
simulation — mechanical, electrical, thermal, and the full body in a physics
engine — and every simulated result says it is simulated, as
[protocol §4](../protocol/conformance.md) already requires.

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

The specification admits laboratory technology where the physics exists but
the product does not (see [spec 00](../spec/00-scope-and-criteria.md)). For
items marked **LAB** there is no part number to identify. Their L3 is a
*reference design traced to a cited publication*, and their L4 is our own
design of whatever surrounds them — readout, drive electronics, mounting —
drawn to the same standard as everything else. The plan marks these rows so
that they cannot be mistaken for purchasable items.

---

## 2. Where the repository stands

| Subsystem | Level reached | Evidence |
|---|---|---|
| Envelopes, mass–energy loop | L0–L1 | `spec/`, `scripts/gems_budget.py --check` |
| Kinematics, 30 core DOF | L1 | `hardware/kinematics.md` |
| Actuators, cells, compute, bus, materials | **L2** | `hardware/electrical/`, `hardware/mechanical/` |
| Emission log, agency classification | **L4** in reference form | `software/`, 30 tests |
| Firmware | L1 | `firmware/ARCHITECTURE.md` |
| Kinematic simulation model | L4 for kinematics only | `hardware/sim-model/` — inertias estimated |
| Everything else | L0 | — |

No item is at L3. The bill of materials exists — [`hardware/bom/`](../hardware/bom/),
one row per item the specification names — but no row carries a verified price
yet.

---

## 3. Decisions that block everything else

These are ordered: each one is needed before the work packages that depend on
it can move past L2. None can be settled by arithmetic alone.

| # | Decision | Blocks | Status |
|---|---|---|---|
| **D-1** | **Knee torque requirement.** The sizing script assumes knee = hip pitch, flagged there as an assumption, not a source | Actuator sizing, `f_act`, the mass loop | open — check against published gait data |
| **D-2** | **Actuators: procure modules or design them.** An 88.7 Nm/kg module exists commercially, but it peaks at 85 Nm and 16 of the 30 joints need more ([`hardware/bom/`](../hardware/bom/README.md#what-building-the-bom-turned-up)). This decision also settles the conflict between the per-class reducers of `hardware/mechanical` and the single module family of `hardware/electrical`. Designing our own motor, reducer and drive puts every capacitor of the drive inside this repository | M-3, E-3, F-3 — the largest single block of work | open |
| **D-3** | **Real-time processor and RTOS.** The Jetson carries perception and compression; it is not a hard real-time target for the 500 Hz balance loop and the 10 ms reflex path | All firmware, E-5 | open |
| **D-4** | **High-voltage bus voltage** | Every power stage, cell count in series, harness gauge | open |
| **D-5** | **Cell and pack format** at the durable tier (400–500 Wh/kg) | Pack mechanics, BMS, thermal | open — candidates sourced in `hardware/electrical/` |
| **D-6** | **Reference hand configuration.** The declaration leaves 2×5 to 2×21 DOF open (`⟦CTRL⟧`); a complete design needs one point to draw | M-4, E-3 count, F-3 count | open — anchor figure is 40 joints, i.e. 2×5 |
| **D-7** | **Secure element and low-power trace radio** | Attestation, trace emitter, C-10, C-11 | open |
| **D-8** | **Operating point for the reference design** — endurance, armour coverage | Mass, pack size, every downstream figure | open — the conformance record uses 4 h, 65% |

D-6 and D-8 are choices of *which* point to draw, not changes to the
specification: the specification keeps its ranges, and a reference design
declares the one it drew.

---

## 4. Work packages

Every package lists its tasks, the level it takes its subject to, and what it
waits for. IDs are stable so that commits and issues can name them.

### M — Mechanical

| ID | Task | To | Waits for |
|---|---|---|---|
| M-1 | Parametric CAD skeleton generated from `kinematics.md`, the same way the URDF is — joint frames, segment envelopes, keep-out volumes | L4 | — |
| M-2 | Packaging study: where the pack, compute, drives, radios and sensors sit, checked against segment envelopes and the centre of mass | L1 | D-4, D-5 |
| M-3 | Joint modules per class — hip/knee (cycloidal), shoulder/elbow (QDD planetary), wrist/neck (harmonic): bearings, seals, encoder mounts, joint locks (spec 03.2 measure 4), series-elastic elements (measure 5) | L4 | D-1, D-2 |
| M-4 | Hands at the reference configuration | L4 | D-6 |
| M-5 | Structure per segment — composite tubes, 7075 load-introduction fittings, fastener schedule | L4 | M-2, M-3 |
| M-6 | Structural FEA per segment against peak joint loads and a fall case | L5 | M-5 |
| M-7 | Protection layer — integrated multi-threat package, panel layout at the declared coverage | L4 | D-8 |
| M-8 | Shell, three layers (spec 04.5): sense-and-heal, variable stiffness, load-and-fire | L4 | M-7 — **LAB** for the first two |
| M-9 | Head and sensor mounting — stereo baseline, thermal, LiDAR, microphone array geometry | L4 | E-6 |
| M-10 | Dock — seat form, charging contacts, alignment | L4 | E-2 |
| M-11 | Thermal design — conduction paths, compute and drive cooling, sealed-body dissipation | L5 | M-2, E-3, E-5 |
| M-12 | Mass properties exported from CAD into the simulation model, replacing the estimated inertias | L5 | M-5 |

### E — Electrical

| ID | Task | To | Waits for |
|---|---|---|---|
| E-1 | System block diagram: every board, every bus, every power rail, every connector | L1 | D-3, D-4 |
| E-2 | Power: pack, BMS, pre-charge and contactor, fusing, supercapacitor tier (spec 03.2 measure 3), regeneration path, dock charger interface | L4 | D-4, D-5 |
| E-3 | Joint drive board: inverter, gate driver, phase current sensing, encoder interface, EtherCAT slave controller, temperature sensing, brake and lock driver | L4 | D-2, D-4 |
| E-4 | Power distribution and conversion: HV to logic rails, isolated domains, the always-on vigilance rail at floor power (spec 03.6) | L4 | E-2 |
| E-5 | Compute boards: Jetson carrier, real-time controller board, EtherCAT master interface, storage for the emission log | L4 | D-3 |
| E-6 | Sensor front-ends: camera links, thermal, LiDAR, microphone array, SDR, IMUs, e-nose | L4 | E-5 |
| E-7 | Tactile skin readout for ~500,000 taxels (spec 05.2): multiplexing, ADCs, local event compression | L4 | **LAB** |
| E-8 | Radios: mmWave uplink, fallback link, low-power trace radio | L4 | D-7 |
| E-9 | Root of trust: secure element per node or per bus segment | L4 | D-7 |
| E-10 | Shell drivers: magnetorheological coils or electrorheological high-voltage supply, electrochromic drivers | L4 | M-8 — **LAB** |
| E-11 | Contact-amplitude instrumentation (spec 06.6) | L4 | E-7 |
| E-12 | Harness: every cable, gauge, connector, length, routed through the CAD | L4 | M-5, E-1 |
| E-13 | Circuit simulation: power stages, gate drive, current sensing, rail sequencing, in SPICE | L5 | E-2 … E-4 |
| E-14 | Power and energy budget rebuilt from part datasheets, checked against spec 02 and 03 | L5 | E-2 … E-10 |

### F — Firmware

See [`firmware.md`](firmware.md). Waits for D-3 to reach L4; the parts that do
not depend on a target — algorithms, state machines, protocols — can be written
now and run in simulation.

### S — Software

See [`software.md`](software.md). Needs no hardware decision and can proceed now.

### V — Simulation and verification

| ID | Task | To | Waits for |
|---|---|---|---|
| V-1 | Full-body physics model with actuator models (torque–speed, current limits, reducer efficiency, backlash) | L5 | M-12, D-2 |
| V-2 | Battery and power model: state of charge, voltage sag at peak draw, the 5C peak of spec 02.7 | L5 | E-2 |
| V-3 | Balance and gait in simulation at ≥ 500 Hz, driven by the firmware's own controller code | L5 | F-5 |
| V-4 | Fall and supported failure state (C-16) | L5 | F-8 |
| V-5 | Software-in-the-loop: firmware built for the host, stepping against the physics model | L5 | F-0 |
| V-6 | Emulated target: firmware built for the real processor, run in an instruction-set emulator against the physics model | L5 | D-3 |
| V-7 | Sensor simulation: rendered cameras, depth, IMU noise, tactile contact, for the software pipeline | L5 | S-1 |
| V-8 | Link simulation: bandwidth, latency, outage, for link management | L5 | S-5 |
| V-9 | Conformance re-assessment: rerun `protocol/assess.py` with each simulated result, and state which rows moved and why | L5 | all |

### B — Bill of materials and cost

| ID | Task | To | Waits for |
|---|---|---|---|
| B-1 | BOM format: part, manufacturer, part number, quantity, source link, unit price, currency, date priced, maturity — ✅ [`hardware/bom/`](../hardware/bom/) | — | — |
| B-2 | Price what is already selected at L2 — actuator modules, cells, compute, EtherCAT and CAN FD parts, materials | L3 | B-1 |
| B-3 | Extend the BOM as each work package reaches L3 | L3 | each package |
| B-4 | Cost roll-up by subsystem, with "quote only" and **LAB** rows counted separately rather than guessed | L3 | B-3 |

Prices are recorded with the date they were read and the page they were read
from. A price that could not be found is left empty and says so.

---

## 5. Order of work

Nothing here waits for money. What waits is decisions.

1. **D-1**, the knee torque, first — it is the one open figure that could stop
   the mass loop from converging, and it is cheap to settle.
2. **D-2 to D-5**, with **B-2** alongside, because pricing the candidates is
   part of choosing between them.
3. **S** work in parallel from now: it needs no hardware.
4. **M-1**, **E-1**, and the target-independent parts of **F**, once D-3 and D-4
   are settled.
5. Detailed design — M-3 to M-11, E-2 to E-12, F source against the target.
6. Verification — V-1 to V-9 — as each piece reaches L4, not at the end.
