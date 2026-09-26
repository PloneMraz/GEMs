# Firmware work

Module by module, from [`../firmware/ARCHITECTURE.md`](../firmware/ARCHITECTURE.md)
down to the task. Levels L0–L5 are defined in [`README.md`](README.md#levels-of-detail).

**What can start now.** Algorithms, state machines, protocol logic and their
tests do not depend on a processor. They are written against a thin hardware
abstraction and run on the host in software-in-the-loop (V-5). Only drivers,
board support and timing measurements wait for D-3.

**Scope.** Firmware as [spec 07.1](../spec/07-firmware-and-software.md#71-the-division)
defines it: code on the embedded devices, including every hard real-time task.
Capture drivers on the application processor are software and are listed in
[`software.md`](software.md#s-9--capture-on-the-application-processor).

**One rule carried from the architecture.** Every module that carries a deadline
reports its misses. Each task below that implements a timed loop includes the
deadline monitor for it; it is not a separate task that can be skipped.

---

## F-0 — Platform

| Task | To | Waits for |
|---|---|---|
| Hardware abstraction layer: the interface every module is written against, with a host implementation for simulation | L4 | — |
| Board support package for the real-time processor | L4 | D-3 |
| RTOS configuration: task set, priorities, stack budgets, the scheduling analysis that shows every deadline is met on paper | L4 | D-3 |
| Deadline monitor and miss reporting, shared by every timed module | L4 | — |
| Watchdogs: per task and per board | L4 | D-3 |
| Build system, host and target, reproducible | L4 | — |
| Bootloader and signed update, with rollback | L4 | D-7 |

## F-1 — Sensor drivers

| Task | To | Waits for |
|---|---|---|
| Timestamp at source for every channel | L4 | F-2 |
| IMU driver, per IMU fitted | L4 | E-6 |
| Joint encoder readout, absolute and incremental | L4 | E-3 |
| Joint torque sensing | L4 | E-3 |
| Tactile readout control — scan scheduling, event thresholds | L4 | E-7 — **LAB** |
| Per-channel health: dropout, saturation, stuck value | L4 | — |

## F-2 — Time base

| Task | To | Waits for |
|---|---|---|
| EtherCAT distributed-clock configuration and drift compensation | L4 | E-5 |
| Bridging the EtherCAT clock to CAN FD nodes and to the Jetson | L4 | E-1 |
| Skew measurement and reporting against the permitted skew (`⟦IMPL⟧`) | L5 | V-6 |
| **Closes C-15** in simulated form once V-6 runs it | L5 | V-6 |

## F-3 — Actuator drivers (joint drive firmware)

Runs on each joint drive board. If D-2 chooses procured modules, most of this
is replaced by the module's own firmware and shrinks to integration.

| Task | To | Waits for |
|---|---|---|
| Field-oriented current control, at the kHz-class rate (`⟦IMPL⟧`) | L4 | D-2 |
| Velocity and position loops, and impedance mode for compliant contact | L4 | D-2 |
| Commutation and encoder calibration | L4 | D-2 |
| Protections: overcurrent, overtemperature, overvoltage on regeneration, stall | L4 | E-3 |
| Joint lock actuation and state (spec 03.2 measure 4) | L4 | M-3 |
| EtherCAT slave application: process data, state machine | L4 | E-3 |
| Telemetry for the full-tier log: commanded and measured current, position, velocity, torque, temperature | L4 | — |

## F-4 — State estimator

| Task | To | Waits for |
|---|---|---|
| Floating-base state estimation from IMU, joint kinematics and contact, at 1 kHz | L4 | — |
| Contact detection per foot and per hand | L4 | — |
| Covariance reporting, so that a degraded estimate says it is degraded | L4 | — |
| Verified against the physics model's ground truth | L5 | V-5 |

## F-5 — Balance controller

| Task | To | Waits for |
|---|---|---|
| Balance at ≥ 500 Hz: centre-of-mass and ZMP regulation, whole-body torque distribution within joint limits | L4 | — |
| Step recovery | L4 | — |
| Motion intent interface from software — intent, not commands (architecture §4) | L4 | — |
| Priority over the reflex path where they contend (architecture §3) | L4 | — |
| Verified in simulation — standing, pushed, stepping (V-3) | L5 | V-1 |
| **Closes C-13** in simulated form when run on the emulated target (V-6) | L5 | V-6 |

## F-6 — Reflex path

| Task | To | Waits for |
|---|---|---|
| Stage pipeline with the budget of architecture §2 — acquisition 1.0, agency tagging 0.5, state assembly 2.0, reflex decision 1.0, command 4.0, log 0.05 ms | L4 | — |
| Per-stage timing instrumentation, so the split can be measured and moved | L4 | — |
| Loadable reflex set: format, signing, loading at runtime | L4 | D-7 |
| Reflex decision: lookup against the loaded reflex set | L4 | — |
| Anchored context written for every reflex (spec 07.4 guarantee 3) | L4 | F-10 |
| **Closes C-14** in simulated form when measured end to end on V-6 | L5 | V-6 |

## F-7 — Agency tagging

| Task | To | Waits for |
|---|---|---|
| Port the efference-copy gate of [`firmware/reference/agency.py`](../firmware/reference/agency.py) to firmware, where commanded and measured values meet | L4 | — |
| Cross-check the port against the Python reference on the same recorded data | L5 | — |

## F-8 — Safe-state supervisor

| Task | To | Waits for |
|---|---|---|
| Fault taxonomy and the response to each | L4 | — |
| Fall detection early enough to act on | L4 | F-4 |
| Controlled descent to a supported posture — must beat the fall | L4 | F-5 |
| Power-loss behaviour: what the supercapacitor tier holds up, and for how long | L4 | E-2 |
| **Closes C-16** in simulated form (V-4) | L5 | V-1 |

## F-9 — Power state machine and BMS

| Task | To | Waits for |
|---|---|---|
| The four state levels of spec 03.4, and every transition with its wake latency | L4 | — |
| Tiered sleep with the always-on wake-up circuit on the always-on rail | L4 | E-4 |
| Battery management: cell monitoring, balancing, state of charge and health, protection | L4 | D-5 |
| Pre-charge and contactor sequencing | L4 | E-2 |
| Dock detection and charge control | L4 | E-2 |
| State-dependent gating (spec 03.2 measure 1) — which actuators and channels run | L4 | — |

## F-10 — Log writer

| Task | To | Waits for |
|---|---|---|
| Port the record format and hash chain of [`software/audit_log.py`](../software/audit_log.py) to firmware at loop rate | L4 | — |
| Batch signing through the secure element; batch period from measured signing throughput | L4 | D-7 |
| Storage layout on the log device, and behaviour when it fills — never trimmed during a link outage (architecture §5) | L4 | E-5 |
| Byte-for-byte verification against the Python verifier | L5 | — |

## F-11 — Attestation agent

| Task | To | Waits for |
|---|---|---|
| Tier 1: measured boot and per-node signatures | L4 | D-7 |
| Tier 2: physical fingerprint baselines at commissioning, and drift checks | L4 | F-1 |
| Tier 3: active challenge — commanded motion checked against encoder, IMU and vision agreement | L4 | F-3, F-4 |
| **Closes C-11** in simulated form for tiers 2 and 3 | L5 | V-5 |

## F-12 — Low-power beacon

| Task | To | Waits for |
|---|---|---|
| Signed summary format at quiescent power | L4 | — |
| Duty cycle against the floor-power budget of spec 03.6 | L4 | D-7 |
| Radio driver | L4 | E-8 |

## F-13 — Shell controllers

| Task | To | Waits for |
|---|---|---|
| Variable-stiffness field control, millisecond class | L4 | E-10 — **LAB** |
| Electrochromic colour control, second class | L4 | E-10 — **LAB** |

## F-14 — Link firmware

| Task | To | Waits for |
|---|---|---|
| mmWave radio bring-up and beam tracking interface | L4 | E-8 |
| Fallback link handover | L4 | E-8 |
| Local-core behaviour on link loss — maintain, preserve, continue, attempt; never decide (spec 07.5) | L4 | — |

## F-15 — Expressive actuators

| Task | To | Waits for |
|---|---|---|
| Facial action-unit control: per-unit position and speed within the ranges of ID-6, and blending of simultaneous units | L4 | ID-6 — **LAB** |
| Eye and pupil actuation, coordinated with neck gaze | L4 | ID-6 |
| Expression requests arrive as intent from software, like motion (architecture §4); firmware bounds range and rate, it does not choose | L4 | — |
