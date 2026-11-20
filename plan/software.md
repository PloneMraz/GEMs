# Software work

Module by module, from [spec 07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) and [`../software/README.md`](../software/README.md) down to the task. Levels L0–L5 are defined in [`README.md`](README.md#levels-of-detail).

**Scope.** Software as [spec 07.1](../spec/07-firmware-and-software.md#71-the-division) defines it: code on the edge AI module under Linux. Its tasks here are firm, soft or non-real-time; their classes are set in [`../realtime_config/`](../realtime_config/). The Real-time Control Layer's modules are planned in [`firmware.md`](firmware.md), whichever layer D-3 puts them in.

**Almost none of this waits for hardware.** Every module except the capture drivers of S-9 can be written and tested now against synthetic or simulated sensor data (V-7). That makes this the one package that can move to L5 before any part is chosen.

**Scope boundary kept.** Nothing here specifies the controller that operates the body. Software turns what the body acquires into information and carries it; what to do with that information is not this repository's ([README](../README.md#scope-boundary)).

---

## S-0 — Common

| Task | To | Waits for |
|---|---|---|
| Record types shared with firmware: sensor record, agency tag, telemetry, fault, intent | L4 | — |
| Intent carries the contact it allows — what may be touched, with what force, what is kept clear; where it gives none, the default the Main Controller loaded applies (binding §2.4) | L4 | — |
| The interface between the real-time code and the edge software (architecture §4), as a versioned message definition — including the loop's `loop_state` report for the beacon (spec 06.5) | L4 | — |
| Synthetic data generators per channel, for tests that do not need the full simulator | L4 | — |

## S-1 — Feature extraction and compression

Guarantee 1: **≥ 2:1, realistically 8:1**, on 15.1 Gbps raw at the conservative configuration (spec 05.4).

| Task | To | Waits for |
|---|---|---|
| Stereo vision: encoding, disparity, features; the retained multispectral and thermal paths | L4 | — |
| Stereo depth, object detection and 6-DoF pose — candidates ESS, RT-DETR, FoundationPose (binding §2.1); object models loaded by the Main Controller | L4 | — |
| Tactile: event-based compression — report change, not state — for ~460,000 taxels | L4 | — |
| SDR: decimation and channel selection | L4 | — |
| LiDAR, microphone array (beamforming), proprioception passed at full rate — it is the one channel that must not be cut (spec 05.5) | L4 | — |
| Compression ratio measured per channel and in aggregate on simulated data | L5 | V-7 |
| Compute load measured against the Jetson power envelope of `hardware/electrical/` §4 | L5 | D-3 |

## S-2 — Agency tag handling

| Task | To | Waits for |
|---|---|---|
| Reference implementation — the specification the firmware port F-7 is checked against | ✅ L4 | done — [`agency.py`](../reference/agency.py) |
| Run on simulated whole-body motion rather than synthetic returns | L5 | V-5 |
| Carry the firmware's tag through every stage and refuse untagged input (spec 07.4 guarantee 2) — enforced by the pipeline, not by convention; ROS 2 messages included (binding §2.1) | L4 | S-3 |

## S-3 — Sensor fusion

| Task | To | Waits for |
|---|---|---|
| Multi-rate fusion on the shared time base of F-2 | L4 | — |
| Carries the body tag through: a fused estimate that mixes changes of different tags says so | L4 | S-2 |
| Local reconstruction of space over a bounded window, as working state (RSIL §8.6) — candidate nvblox; no map kept beyond the window (binding §2.1) | L4 | — |
| Visual-inertial odometry of the unit’s own pose — candidate cuVSLAM, odometry only (binding §2.2) | L4 | V-5 |
| Latency and consistency verified in simulation | L5 | V-7 |

## S-4 — Log assembly and synchronisation

| Task | To | Waits for |
|---|---|---|
| Audit log: format, hash chain, Merkle batches, verifier | ✅ L4 | done — [`audit_log.py`](../reference/audit_log.py) |
| Two tiers — full and anchored — assembled from firmware records | L4 | F-10 |
| Synchronisation to the Main Controller, oldest first, nothing dropped; a record leaves the buffer only once the Main Controller has verified, appended and acknowledged it (RSIL §8.3) | L4 | S-5 |
| Storage accounting: 1.18 GB/h full tier against the log device | L4 | E-5 |

## S-5 — Link management

Guarantee 5: **reduced fidelity before dropped streams.**

| Task | To | Waits for |
|---|---|---|
| Degradation ladder: which channel loses resolution first, and the floor below which a channel is kept rather than dropped | L4 | — |
| Bandwidth estimation and the controller that walks the ladder | L4 | — |
| The IPC heartbeat, which renews the term of a hold, and passing command to the OBC and back (spec 07.5) | L4 | — |
| End-to-end encryption and authentication | L4 | D-7 |
| Verified against simulated bandwidth, latency and outage (V-8) | L5 | V-8 |

## S-6 — Self-motion model

Revised 2026-11-19. A unit casts no expectation of the region or of other entities: those are the Main Controller's (RSIL §6, DIL §6.1). Human trajectory prediction at a ~1.5 s horizon (spec 05.3, **TM**) is such an expectation, and leaves this plan: it runs on the Main Controller, which this repository does not specify. What stays is the model of the body's own execution.

| Task | To | Waits for |
|---|---|---|
| Self-motion model — what this body's own command produces, the model the agency gate compares against; fixed, or loaded by the Main Controller, never learned on the unit | L4 | S-2 |

## S-7 — Channel processing beyond vision

| Task | To | Waits for |
|---|---|---|
| Audio: localisation and separation from the 16-channel array | L4 | — |
| Olfaction: compound identification within the 5–10 s response of spec 05.3 | L4 | E-6 |
| Taste: batch analysis | L4 | **LAB** |
| Contact amplitude (spec 06.6): recorded for every contact event, enforced at write as the audit log already does | L4 | E-11 |

## S-8 — Commissioning and assessment tools

| Task | To | Waits for |
|---|---|---|
| Fingerprint baselining for attestation tier 2 | L4 | F-11 |
| Assessor tooling: extend `protocol/assess.py` as simulated evidence arrives | L5 | V-9 |

## S-9 — Capture on the application processor

Drivers are software when they run under the general-purpose OS (spec 07.1). Frame capture and encoding are firm real-time: a late frame is dropped, not used.

| Task | To | Waits for |
|---|---|---|
| Camera, thermal, LiDAR, microphone and SDR capture, delivering buffers timestamped on the shared time base of F-2 | L4 | E-6 |
| Per-channel health: dropout, saturation, stuck value | L4 | — |
