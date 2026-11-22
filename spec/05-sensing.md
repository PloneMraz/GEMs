# 05 — Sensing

This is the primary axis: the body exists to acquire physical experience. Quantifying it forces a question that a single multiplier cannot answer.

## 5.1 "× human" is not one number — it is five axes

"As sensitive as human skin, times N" decomposes into five independent quantities, and they do not all move together:

| Axis | Human | Can it exceed human |
|---|---|---|
| **Point density** | ~241 mechanoreceptors/cm² at the fingertip *(sourced)* | **No** — see below |
| **Sensitivity threshold** | — | **Yes**, substantially |
| **Temporal bandwidth** | Pacinian corpuscles to ~500 Hz | **Yes** — piezoelectric sensors reach tens of kHz ⇒ **20–100×** |
| **Dynamic range** | finite, saturates early | **Yes** |
| **Simultaneous modalities** | pressure, vibration, temperature, pain | **Yes** — the self-healing skin on the upgrade path ([04.7](04-shell.md#47-upgrade-path)) also senses pH |

**Density is blocked twice, independently:**

1. **Fabrication.** The densest published e-skin array reaches **~347 elements/cm²** *(sourced)* — roughly **level with human skin**, not above it. A 100× density means 24,100/cm², about **69× beyond anything yet built**.
2. **Bandwidth.** Even if it could be built: 24,100/cm² over 1.6 m² is **386 million points**. At 1 kHz and 12 bits that is **~4,600 Gbps of tactile data alone** — **580×** the 8 Gbps link of [01](01-architecture.md). No compression ratio rescues that.

**Declared tactile capability:** density **level with human skin** in the fine regions (hands, face), thinning across the torso; **20–100× human in temporal bandwidth**; above human in sensitivity threshold, dynamic range, and number of simultaneously measured quantities.

**What the baseline meets of it** ([04.3](04-shell.md#43-outer-layer-tactile-skin-and-textile), [04.6](04-shell.md#46-touch-at-the-hands-and-face), 2026-11-22): contact force over the body, from a bought large-area skin at ~2.8 points/cm² and 60 Hz; three-axis force at the hands, from bought modules at ~2–4.5 points/cm². The declaration stays the requirement. The density and rate below are not met by anything on sale: the hands are **OPEN** against them, and the rest of the body and the face are `UPG`.

## 5.2 Tactile layout

Uniform whole-body density is wasteful — human skin is not uniform either.

| Region | Area | Density | Points |
|---|---|---|---|
| Fine — hands, face | ~500 cm² | ~300/cm² *(near the fabrication ceiling)* | ~150,000 |
| Ordinary — remainder | ~15,500 cm² | ~20/cm² | ~310,000 |
| **Total** | 1.6 m² | — | **~460,000** |

At 1 kHz and 12 bits: **5.5 Gbps** raw — two thirds of the link, from one channel. This is the requirement; the baseline's skin, ~43,000 points at 60 Hz, sends a small fraction of it. (1.8 m², ~500,000 points and 6.0 Gbps until the height came to 1.65 m on 2026-09-26.)

## 5.3 Channels

| Channel | Anchor configuration | Raw rate | Note |
|---|---|---|---|
| Stereo vision | 2 × 4K, 30 fps, 12 bit | **5.97 Gbps** | Optical zoom, multispectral, thermal IR retained |
| Thermal IR | 640×480, 30 fps, 16 bit | 0.15 Gbps | |
| LiDAR / depth | 300k points/s | 0.04 Gbps | |
| Microphone array | 16 ch, 48 kHz, 24 bit | 0.02 Gbps | High-sensitivity, directional |
| Proprioception | 41 joints × 4 channels + IMU, 1 kHz | 0.006 Gbps | Joint count declared at [`hardware/kinematics.md`](../hardware/kinematics.md). Cheapest channel, and the one that **must not be cut** — see 5.5 |
| SDR / multi-band RF | 2 ch × 56 MHz I/Q, 16 bit | **3.58 Gbps** | |
| Spatial RF sensing | Wi-Fi / mmWave CSI | modest | Retained at full hardware capability; use is `⟦CTRL⟧` |
| Olfaction (e-nose) | — | negligible | **5–30 ppb** achieved per compound *(sourced)*; 5–10 s response |
| Taste (lab-on-chip) | — | negligible | Slow, batch-wise |
| Trajectory prediction | ~1.5 s horizon | — | Computer vision plus human trajectory prediction. **TM**. The prediction is an expectation of another entity and runs on the Main Controller; the unit supplies the detections (RSIL §6) |
| Voice and ultrasound | — | — | Synthesis plus ultrasonic emission. **TM** |
| Biological response | pupil, expression | — | Micro facial actuators and microfluidics. **TM/LAB** |
| Cardiac co-regulation | vibration, warmth, rhythm | — | **Optional module, not always-on.** Instrumented per [06.6](06-audit-surface.md#66-contact-amplitude) |

> **On olfaction.** Parts-per-billion thresholds **are** achieved. What has to be reduced is not sensitivity but **sensitivity × breadth of compounds × speed simultaneously**: a sensor reaching 5 ppb for one compound takes 5–10 seconds, and no array reaches ppb across hundreds of compounds in real time.

## 5.4 Aggregate rate against the link

| Configuration | Vision | Tactile | SDR | **Total** | Minimum compression |
|---|---|---|---|---|---|
| **A — conservative** (4K30, 460k points) | 5.97 | 5.52 | 3.58 | **15.1 Gbps** | **2 : 1** |
| **B — moderate** (8K60, 1M points, 4-ch SDR) | 47.8 | 12.0 | 7.17 | **67.2 Gbps** | **8 : 1** |
| **C — 100× density** | 47.8 | 5,206 | 7.17 | **5,261 Gbps** | 658 : 1 — *excluded* |

Available link: **8 Gbps**.

> The on-board / off-board split of [01](01-architecture.md) is not a design preference. **It falls short by 2× in the most conservative configuration and by 8× in a sensible one.** On-body processing is arithmetic, not taste.

## 5.5 Proprioception is mandatory

Joint encoders, IMU and force/torque sensing, dense enough to distinguish **"I just moved"** from **"something moved me"**.

This is the cheapest channel on the list and the one that cannot be omitted. Two separate requirements land on it:

- **Experience.** A touch from another person must be cleanly separable from the body's own motion, or the experience being acquired is corrupted at source.
- **The platform contract.** An external processing loop requires that every change be classified as self-caused or not *before* it is interpreted — see [08](08-platform-contract.md). Without adequate proprioceptive hardware that requirement cannot be enforced, and every layer above it reads wrong.

The same hardware serves a third purpose in [06.3](06-audit-surface.md#63-three-tiers-of-attestation).

## 5.6 The on-body / off-body compute split

What is split here is **processing, not decision**. Deciding is the Main Controller's, off the body ([01](01-architecture.md)); the dial sets how much of the processing — compression, feature extraction, fusion — runs on the unit.

The split is a dial with **two hard ends and a soft middle**.

**Lower end — what must be on the body:**

| Constraint | Figure |
|---|---|
| Minimum compression | **2 : 1 → 8 : 1** (5.4) |
| Balance loop | **≥ 500 Hz** |
| Fast reaction loop | **≤ 10 ms** |
| Context record for every output event (RSIL INV-8: anchored context on every emission) | per event ([08.2](08-platform-contract.md#82-traced-appraisal-not-mute-reflex)) |

Link round-trip is ~1 ms at ideal short range, but at kilometre range with beam tracking it cannot be relied on for ≤10 ms. **Balance and reflex are therefore on-body — not because the design prefers it, but because there is no alternative.**

**Upper end — what must not be on the body:**

| Constraint | Content |
|---|---|
| Losing a unit loses its state | Its own state and its unsynchronised record, never memory; the more processing on the unit, the more of that there is ([01](01-architecture.md)) |
| Power | Edge compute draws on the same `p` (W/kg) that enters the convergence condition `Σf < 1` |
| Heat | A sealed body in human contact dissipates worse than a rack |
| Memory and world model | Off-body by architectural definition, not by capacity |

> **Edge compute is not "add as much as you like, it only costs battery." It eats into the convergence condition of the whole body**, and [02.3](02-structure-and-motion.md#23-the-endurance-ceiling) shows `γ` inflating non-linearly near the ceiling.
>
> The middle — feature extraction, compression, detection, reconstruction of the space around the body — is `⟦CTRL⟧`, and **should be adjustable per mission** rather than a compile-time constant. Predicting and tracking other agents is not in the middle: a tracker predicts where another entity will be, which is an expectation, and expectations are the Main Controller's (RSIL §6; 2026-11-19). The unit estimates only its own state.

**Spatial data is the unit’s to acquire; the map is not (2026-11-20).** The unit senses the space around it and reconstructs it over a bounded window — depth from the stereo pair, points from the LiDAR, occupancy around the body and within reach of its hands — and returns it, whole or in features, to the Main Controller. A map kept beyond the window — built up across visits, corrected by loop closure, used to recognize a place — is part of the world model, built on the Main Controller from what the units return (RSIL §8.6). The same reconstruction serves the unit’s own execution: the ground a foot lands on, the space a hand reaches through. Whether the body goes around a thing or touches it is behaviour, and behaviour is the Main Controller’s: it travels with the command, and the unit carries it out ([binding §2.4](../software/RSIL-in-GEMs.md#24-execution--rsil-75)). Wi-Fi and mmWave sensing (5.3) add the presence and motion of people; the geometry does not rest on them ([binding §2.9](../software/RSIL-in-GEMs.md#29-what-does-not-run-on-a-unit)).

**Operating point: `⟦CTRL⟧`.**
