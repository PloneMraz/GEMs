# RSIL in GEMs — the binding

How the operating mechanism of [RSIL](../ref/RSIL.md) is realised by the algorithms a GEMs unit runs: which algorithm carries which construct, where it runs, which plan task owns it, and what rule RSIL lays on it. RSIL §10.1 asks every platform for such a document; this is GEMs’s.

**How to read it.** This document is not normative. RSIL is the law, and the specification chapters are what GEMs requires of itself; where this binding differs from either, they govern and the difference is a defect here. Nothing in it has been built: every algorithm named is a candidate or a planned module, and where a choice waits for a decision (D-2 actuator modules, D-3 the real-time computer, D-7 the secure element), it is left waiting. The rule of [`CLAUDE.md`](../CLAUDE.md) §2 holds for software as for hardware: what the market offers — a fieldbus master, a driver, a middleware, a filter — is chosen, not written; what GEMs writes is the integration.

---

## 1. The two ends

| End | Runs | Here |
|---|---|---|
| **The controller** (RSIL §2) | DIL’s loop: the one mind, the one self, the experience store and its black box | The **Main Controller**, on the IPC, off the body ([spec 01](../spec/01-architecture.md)); its loop is `dil-core` |
| **A body** (RSIL §2) | RSIL’s loop: intake, body differentiation, channels, the body-datum; execution; the cached reflexes; declared faculties; the record buffer; the loop’s working state | Each **unit** — GEMs01, GEMs02 — on its own processors |

On a unit, RSIL’s parts fall on the processors of [spec 07.1](../spec/07-firmware-and-software.md#71-the-division):

| Processor | What of RSIL runs there |
|---|---|
| Joint drive boards, inside the bought actuator modules | Execution at its lowest: current, velocity and position loops (manufacturer’s firmware, configured by F-3); the module’s own protections, as declared faculties |
| Sensor nodes | Intake (R1, R3): acquisition and timestamp at source |
| Real-time computer — the Real-time Control Layer, D-3 | The fieldbus master; estimation; body differentiation (R2); balance and whole-body execution; the reflex path from the cache; the safe-state supervisor; the log writer |
| Edge AI module (Linux) — the DAQ | Intake of the heavy channels (R3): cameras, LiDAR, audio, SDR; compression; fusion; log assembly; link management |
| OBC | The hold while cut off (RSIL §9): the cached reflexes and field, under the term the Main Controller set |
| Secure element | The unit’s identity key; signing of the record buffer (RSIL §8.3) |
| BMS (bought) | A declared faculty: battery protection |

---

## 2. The algorithms, construct by construct

### 2.1 Intake and transduction — R1, R3

| Algorithm | Candidates | Runs on | Plan | Rule from RSIL |
|---|---|---|---|---|
| **EtherCAT master** | SOEM (Simple Open EtherCAT Master) or the IgH EtherCAT Master (EtherLab). IgH runs as a Linux kernel module, so it fits only if D-3 selects Linux with a real-time kernel; SOEM is a library with an OS abstraction layer and can also serve an RTOS target where a port exists. Chosen with D-3 | Real-time computer | F-2, F-3, E-5 | Each cycle carries, for every joint, the command sent (RxPDO) and the execution measured (TxPDO), so that R2 compares the two within one cycle ([07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 7). Its distributed clocks are the one time base every channel is stamped on (F-2, protocol C-15). Drive state and error reports that it carries are reports of reactions (§2.5), not sensor data |
| **CAN / CAN FD, CANopen** | CAN FD for distributed sensing ([electrical §5](../hardware/electrical/README.md#5-bus)); the actuator modules’ CAN messages through the bought CAN → EtherCAT bridge where D-2’s module does not speak EtherCAT (F-3); CANopen where a bought part speaks it — the dock charger candidate does, CiA 419 ([AVL](../hardware/bom/avl.csv), `GEM-30030`), and a drive profile such as CiA 402 if D-2’s module offers one | Sensor nodes, bridge, real-time computer | F-1, F-3, F-9 | Timestamp at source on the shared base. A CANopen emergency message, or a drive’s fault state, is a faculty reporting what it did (§2.5) |
| **Modbus, UART, SPI** | Device-level links a bought part may require — an IMU on SPI or UART, a sensor or a power part on Modbus RTU over RS-485. No part in the AVL is fixed to Modbus today; the row is the class, not a choice | Sensor nodes | F-1 | As above. Per-channel health — dropout, saturation, stuck value (F-1) — is returned as a datum. What a link carries under attack that is no faculty’s is damage, and stays `ENV_PUSHED` (RSIL §7.3) |
| **ROS 2 sensor drivers** | ROS 2 drivers for the cameras, LiDAR, microphones and SDR, on the edge module (S-9) | Edge AI module | S-9, S-0 | Linux without a real-time kernel carries firm, soft and non-real-time tasks only ([07.1](../spec/07-firmware-and-software.md#71-the-division)): no hard task runs in a ROS 2 graph there. Each message carries the record type of S-0, its body tag included, and nothing downstream accepts an untagged one ([07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 2). If a ROS 2 graph reaches the IPC, it ends at a channel the unit has declared to `dil-core` (§3), and its data enters the mind through the tagging-gate; no subscriber feeds the Main Controller around it (RSIL §10.1). Records never travel by a ROS 2 topic whose QoS may drop them: they go by the signed buffer path of §2.7 |
| **Compression and feature extraction** | Per channel (S-1) | Edge AI module | S-1 | Transduction, not interpretation: the body tag is attached before compression and survives it |
| **Sensor fusion** | Multi-rate, on the shared time base (S-3) | Edge AI module | S-3 | A fused estimate that mixes changes of different body tags says so |

### 2.2 Estimation — RSIL §6

| Algorithm | Candidates | Runs on | Plan | Rule from RSIL |
|---|---|---|---|---|
| **State estimator** — floating-base state from IMU, joint kinematics and contact, at 1 kHz | Kalman filter (KF) where the model is linear; extended (EKF) or unscented (UKF) Kalman filter for the nonlinear floating-base model with orientation. Chosen in simulation (V-5) against the 0.6 ms estimate stage of the balance loop ([`tasks.csv`](../realtime_config/tasks.csv), `balance.estimate`) | Real-time computer | F-4 | Estimation, not expectation. The model and its noise parameters are fixed, or loaded by the Main Controller; nothing tunes them on the unit from experience. The innovation is not a prediction error and is never recorded as resistance. The covariance is reported, so a degraded estimate says it is degraded (F-4) |
| **Self-motion model of the agency gate** | The execution model of [`reference/agency.py`](../reference/agency.py) (`ForwardModel`), replaced by joint dynamics when parts exist | Real-time computer | F-7 | The same rule: it says what this body’s own command produces, never what the region will return |

### 2.3 Body differentiation — R2

| Algorithm | Runs on | Plan | Rule from RSIL |
|---|---|---|---|
| **Efference-copy gate** — [`reference/agency.py`](../reference/agency.py) (`AgencyGate`) | Real-time computer, in the 0.5 ms agency stage of the reflex path ([firmware §2](../firmware/ARCHITECTURE.md#2-the-reflex-budget)) | F-7, S-2 | Each change is tagged `BODY_CAUSED` (within tolerance of the command), `HOST_REACTED` (a declared faculty acted on the joint) or `ENV_PUSHED` (neither), before anything interprets it. A reaction reported under an undeclared faculty explains nothing and is kept for the record. The Main Controller adds the self’s tag beside the body’s and never overwrites it (RSIL §3.3) |

### 2.4 Execution — RSIL §7.5

| Algorithm | Runs on | Plan | Rule from RSIL |
|---|---|---|---|
| **Current, velocity, position and impedance loops** | Joint drive boards (manufacturer’s firmware) | F-3 | Execution of the setpoints they are sent; their gains are configured, not learned |
| **Balance and whole-body control** — centre-of-mass and ZMP regulation, whole-body torque distribution within joint limits, at ≥ 500 Hz | Real-time computer | F-5 | Execution of the motion intent the edge software passes down from the Main Controller — intent, not commands ([firmware §4](../firmware/ARCHITECTURE.md#4-the-interface-to-the-edge-software)). Tagged `BODY_CAUSED`. It reads no experience, and it ends with its intent, or at the end of a hold’s term (§2.8) |
| **Expressive and shell actuators** | Real-time computer, shell controllers | F-13, F-15 | Execution of requested expressions and shell states, bounded in range and rate |
| **Step recovery** | Real-time computer | F-5 | **Not execution**: no command asks for the step. It is declared, as a faculty (`step_recovery`, a fixed law that reads no experience) or as a reflex the Main Controller loads (RSIL §7.5). **Open** in GEMs: which one is to be decided with F-5; until it is, the platform contract is not met for it |

### 2.5 Declared faculties — RSIL §7.2

Each is declared to the Main Controller as a `ReactionFaculty` of the unit (§3); each reads neither the store nor the cache, and acts whether the Main Controller runs, the link holds, or the cache is intact.

| Faculty | Realised by | Plan |
|---|---|---|
| Actuator protections — overcurrent, overtemperature, overvoltage on regeneration, stall | The bought module’s own firmware, set to this body’s values | F-3 |
| Drive fault reaction — fault state, quick stop | The module’s firmware, through its bus profile where it has one | F-3 |
| Safe torque off | An STO input, where D-2’s module or its drive chain offers one; none is fixed in the BOM today | F-8, D-2 |
| Battery protection — cell limits, disconnect | The bought BMS | F-9 |
| Safe-state supervisor — controlled descent to a supported posture | Real-time computer, a fixed law | F-8 |
| Step recovery, if declared as a faculty | Real-time computer | F-5 |

**Gap.** No faculty is yet specified for an electrical stimulus from outside — a stun gun’s voltage at the skin, the harness or the pack. RSIL §7.4 walks through what one must do; GEMs has not stated which part does it. **Open**, for spec 06 and E-2.

### 2.6 The reflex path and the cache — RSIL §7.1, §8.1

| Algorithm | Runs on | Plan | Rule from RSIL |
|---|---|---|---|
| **Reflex decision** — lookup against the loaded reflex set, in the 1.0 ms decision stage | Real-time computer; the OBC while it holds | F-6 | The Main Controller’s appraisal, run from the cache. Every reflex records its anchored context with the version and age of the field it ran under. A reflex stops with the Main Controller: when the Main Controller stops and says so, the set is unloaded |
| **The cache** — the loadable reflex set, the field copy, and the term of a hold | Real-time computer, OBC | F-6, F-14 | Loaded and signed by the Main Controller (D-7); never written by the unit. Sealed under a key of the unit’s own (RSIL §8.4; `DECIDE@IMPL`-R7, with D-7) |

### 2.7 The record buffer — RSIL §8.2–8.3

| Algorithm | Runs on | Plan | Rule from RSIL |
|---|---|---|---|
| **Log writer** — the record format and hash chain of [`reference/audit_log.py`](../reference/audit_log.py), at loop rate; a Merkle root per batch, signed by the secure element | Real-time computer, secure element | F-10 | Each record chained when made, signed no later than its batch closes |
| **Log device** — 2 TB (`GEM-13240`) | Unit | E-5 | A buffer, not the record: it keeps every record until the Main Controller has appended it and said so, and is never trimmed while records wait ([firmware §5](../firmware/ARCHITECTURE.md#5-link-loss)) |
| **Log assembly and synchronisation** — oldest first, nothing dropped | Edge AI module | S-4 | The Main Controller verifies the chain and signatures (the verifier of `audit_log.py`) before it appends; a record that fails is appended as one that failed. The Main Controller reads only what it has appended, never the unit’s device |

### 2.8 Cut off — RSIL §9

| Algorithm | Runs on | Plan | Rule from RSIL |
|---|---|---|---|
| **Heartbeat and handover** | Edge AI module, OBC | S-5, F-14 | The Main Controller loads, with the reflex set, the term for which the unit may hold it; each heartbeat renews it, counted from the last. While it runs, the OBC holds: balance and posture as execution of the last intent, the loaded reflexes, the declared faculties, the buffer; it decides nothing ([07.5](../spec/07-firmware-and-software.md#75-link-loss-and-the-obc)). When the term has passed, the reflexes stop, execution of the last intent ends, and the safe-state supervisor brings the unit to a supported posture ([07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 2) |
| **Low-power beacon** | Beacon radio | F-12 | Carries the loop’s low-power report (C5) unaltered and with its age, in every power state |

### 2.9 What does not run on a unit

**Prediction of other entities and of the region.** Human trajectory prediction at a ~1.5 s horizon (spec 05.3) is an expectation of another entity, and expectations are the mind’s (DIL §6.1; RSIL §6). It runs on the Main Controller, which this repository does not specify ([README](../README.md)); plan S-6 no longer carries it.

**Appraisal, memory, the models of Others.** Integration across sources, appraisal, expectation, the identity store and the experience store are DIL’s, on the Main Controller.

**A map of the region.** A unit reconstructs the space around it for as long as its window reaches (§2.10), and returns that reconstruction, whole or in features, as data. A map kept beyond the window — built up across visits, corrected by loop closure, used to recognize a place or to relocalize in it — is what the agent has learned of the region, and it is built on the Main Controller from what the units return (RSIL §8.6). Whether the agent then goes around a thing or reaches for it is the Main Controller’s to decide, and travels with the command.

### 2.10 Three things a unit holds — RSIL §8

| | What it holds | Written by | Read by | Where on a unit | Rule from RSIL |
|---|---|---|---|---|---|
| **The cache** (§8.1) | The loaded reflex set, the field copy, the term of a hold | The Main Controller, signed (D-7) | The reflex decision (F-6); the OBC while it holds | Real-time computer, OBC (§2.6) | Never written by the unit; sealed under a key of its own (`DECIDE@IMPL`-R7) |
| **The record buffer** (§8.3) | Every record, chained and signed, until the Main Controller has appended it and said so | The unit: the log writer (F-10), log assembly (S-4) | The Main Controller, as it appends | Log device `GEM-13240`, written through the real-time computer and the edge AI module (§2.7) | Nothing removed before acknowledgement; when it is full, loaded reflexes stop and declared faculties remain |
| **The working state** (§8.6) | The sensing windows of each channel (S-9); the state estimator’s state and covariance (F-4); the commands and reactions in flight at the agency gate (F-7); the reconstruction of the space around the unit — depth, point clouds, occupancy over a window (S-1, S-3) | The unit, overwritten as each window moves | Execution (F-3, F-5, F-15), the declared faculties, the reflexes, compression and fusion | Working memory of the real-time computer and the edge AI module; never the log device, except as records | Holds no experience. What in it changes something is tagged at R2 and recorded; nothing passes from it into the cache; no map is kept beyond its window (`DECIDE@IMPL`-R10) |

---

## 3. Where a unit meets `dil-core`

The Main Controller’s host declaration ([`dil-core`](https://github.com/PloneMraz/dil-core), `src/host/declaration.ts`) is where each unit states itself to the mind, and where RSIL’s constructs become something the mind’s law can check:

| `dil-core` | What a GEMs unit declares or sends |
|---|---|
| `HostDeclaration.channels` — `{ id, canReturn, returnsOfItself? }` | One channel per unit channel, named with the unit (`GEMs01/…`). Proprioception and touch answer the unit’s own emissions; cameras, microphones and the clock return of themselves |
| `HostDeclaration.reactions` — `ReactionFaculty { id, to, via? }` | Every faculty of §2.5, with what acts on the unit to bring it about |
| `HostDeclaration.outward` | Every way content can leave the unit: its effectors, its radios, the beacon |
| `HostCycleInput.signals`, `.changes` | What the unit returns each cycle, each change carrying its body tag and its unit |
| `HostCycleInput.reactions` — `{ faculty, action }` | What the unit’s faculties did since the last cycle, tagged `HOST_REACTED` at T2 |
| The tagging-gate (`admitArrival`) | Every arrival from a unit, buffered records included, enters through it; there is no other way in |

A unit’s cycle-0 — its first command matched against what it then senses — is recorded in the Main Controller’s log with the public half of the unit’s identity key, and from then on the unit’s records verify under it (RSIL §3.2, §8.3).

---

## 4. Open in this binding

| Item | Waits for |
|---|---|
| EtherCAT master: SOEM or IgH | D-3 |
| Bus profile of the actuator modules (EtherCAT directly, or CAN through the bridge; CiA 402 or the vendor’s own) | D-2 |
| KF, EKF or UKF for the state estimator | V-5, against the 0.6 ms stage |
| Step recovery: a declared faculty or a loaded reflex | F-5 |
| A faculty against external electrical stimulus | spec 06, E-2 |
| The body-datum (R4): no module is planned for it yet; commissioning calibration (S-8) and the physical fingerprints of attestation tier 2 (F-11) are its nearest neighbours | a plan task |
| Sealing of the cache and how the term is carried and renewed | D-7; RSIL `DECIDE@IMPL`-R5, R7 |
| The windows of the working state, and what of it is returned to the Main Controller | RSIL `DECIDE@IMPL`-R10; S-1, S-9 |
| The local reconstruction of space that execution reads — the ground for balance and stepping (F-5), the workspace for reaching: no module is planned for it, and no path from the edge AI module to the real-time computer carries it yet | a plan task; D-3 |
