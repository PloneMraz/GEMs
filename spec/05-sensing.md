# 05 — Sensing

This is the primary axis: the body exists to acquire physical experience.
Quantifying it forces a question that a single multiplier cannot answer.

## 5.1 "× human" is not one number — it is five axes

"As sensitive as human skin, times N" decomposes into five independent
quantities, and they do not all move together:

| Axis | Human | Can it exceed human |
|---|---|---|
| **Point density** | ~241 mechanoreceptors/cm² at the fingertip *(sourced)* | **No** — see below |
| **Sensitivity threshold** | — | **Yes**, substantially |
| **Temporal bandwidth** | Pacinian corpuscles to ~500 Hz | **Yes** — piezoelectric sensors reach tens of kHz ⇒ **20–100×** |
| **Dynamic range** | finite, saturates early | **Yes** |
| **Simultaneous modalities** | pressure, vibration, temperature, pain | **Yes** — the self-healing layer of [04.2](04-shell.md#42-self-healing) also senses pH and humidity |

**Density is blocked twice, independently:**

1. **Fabrication.** The densest published e-skin array reaches **~347
   elements/cm²** *(sourced)* — roughly **level with human skin**, not above it.
   A 100× density means 24,100/cm², about **69× beyond anything yet built**.
2. **Bandwidth.** Even if it could be built: 24,100/cm² over 1.8 m² is **434
   million points**. At 1 kHz and 12 bits that is **~5,200 Gbps of tactile data
   alone** — **650×** the 8 Gbps link of [01](01-architecture.md). No compression
   ratio rescues that.

**Declared tactile capability:** density **level with human skin** in the fine
regions (hands, face), thinning across the torso; **20–100× human in temporal
bandwidth**; above human in sensitivity threshold, dynamic range, and number of
simultaneously measured quantities.

## 5.2 Tactile layout

Uniform whole-body density is wasteful — human skin is not uniform either.

| Region | Area | Density | Points |
|---|---|---|---|
| Fine — hands, face | ~500 cm² | ~300/cm² *(near the fabrication ceiling)* | ~150,000 |
| Ordinary — remainder | ~17,500 cm² | ~20/cm² | ~350,000 |
| **Total** | 1.8 m² | — | **~500,000** |

At 1 kHz and 12 bits: **6.0 Gbps** raw — three quarters of the link, from one
channel.

## 5.3 Channels

| Channel | Anchor configuration | Raw rate | Note |
|---|---|---|---|
| Stereo vision | 2 × 4K, 30 fps, 12 bit | **5.97 Gbps** | Optical zoom, multispectral, thermal IR retained |
| Thermal IR | 640×480, 30 fps, 16 bit | 0.15 Gbps | |
| LiDAR / depth | 300k points/s | 0.04 Gbps | |
| Microphone array | 16 ch, 48 kHz, 24 bit | 0.02 Gbps | High-sensitivity, directional |
| Proprioception | 40 joints × 4 channels + IMU, 1 kHz | 0.006 Gbps | Cheapest channel, and the one that **must not be cut** — see 5.5 |
| SDR / multi-band RF | 2 ch × 56 MHz I/Q, 16 bit | **3.58 Gbps** | |
| Spatial RF sensing | Wi-Fi / mmWave CSI | modest | Retained at full hardware capability; use is `⟦CTRL⟧` |
| Olfaction (e-nose) | — | negligible | **5–30 ppb** achieved per compound *(sourced)*; 5–10 s response |
| Taste (lab-on-chip) | — | negligible | Slow, batch-wise |
| Trajectory prediction | ~1.5 s horizon | — | Computer vision plus human trajectory prediction. **TM** |
| Voice and ultrasound | — | — | Synthesis plus ultrasonic emission. **TM** |
| Biological response | pupil, expression | — | Micro facial actuators and microfluidics. **TM/LAB** |
| Cardiac co-regulation | vibration, warmth, rhythm | — | **Optional module, not always-on.** Instrumented per [06.6](06-audit-surface.md#66-contact-amplitude) |

> **On olfaction.** Parts-per-billion thresholds **are** achieved. What has to be
> reduced is not sensitivity but **sensitivity × breadth of compounds × speed
> simultaneously**: a sensor reaching 5 ppb for one compound takes 5–10 seconds,
> and no array reaches ppb across hundreds of compounds in real time.

## 5.4 Aggregate rate against the link

| Configuration | Vision | Tactile | SDR | **Total** | Minimum compression |
|---|---|---|---|---|---|
| **A — conservative** (4K30, 500k points) | 5.97 | 6.00 | 3.58 | **15.8 Gbps** | **2 : 1** |
| **B — moderate** (8K60, 1M points, 4-ch SDR) | 47.8 | 12.0 | 7.17 | **67.2 Gbps** | **8 : 1** |
| **C — 100× density** | 47.8 | 5,206 | 7.17 | **5,261 Gbps** | 658 : 1 — *excluded* |

Available link: **8 Gbps**.

> The two-seat architecture of [01](01-architecture.md) is not a design
> preference. **It falls short by 2× in the most conservative configuration and
> by 8× in a sensible one.** On-body processing is arithmetic, not taste.

## 5.5 Proprioception is mandatory

Joint encoders, IMU and force/torque sensing, dense enough to distinguish **"I
just moved"** from **"something moved me"**.

This is the cheapest channel on the list and the one that cannot be omitted.
Two separate requirements land on it:

- **Experience.** A touch from another person must be cleanly separable from the
  body's own motion, or the experience being acquired is corrupted at source.
- **The platform contract.** An external processing loop requires that every
  change be classified as self-caused or not *before* it is interpreted — see
  [07](07-platform-contract.md). Without adequate proprioceptive hardware that
  requirement cannot be enforced, and every layer above it reads wrong.

The same hardware serves a third purpose in [06.3](06-audit-surface.md#63-three-tiers-of-attestation).

## 5.6 The on-body / off-body compute split

The split is a dial with **two hard ends and a soft middle**.

**Lower end — what must be on the body:**

| Constraint | Figure |
|---|---|
| Minimum compression | **2 : 1 → 8 : 1** (5.4) |
| Balance loop | **≥ 500 Hz** |
| Fast reaction loop | **≤ 10 ms** |
| Traced appraisal on every emission | per emission ([07](07-platform-contract.md)) |

Link round-trip is ~1 ms at ideal short range, but at kilometre range with beam
tracking it cannot be relied on for ≤10 ms. **Balance and reflex are therefore
on-body — not because the design prefers it, but because there is no
alternative.**

**Upper end — what must not be on the body:**

| Constraint | Content |
|---|---|
| Losing the body loses the state | The more state on the body, the more expensive its loss ([01](01-architecture.md)) |
| Power | Edge compute draws on the same `p` (W/kg) that enters the convergence condition `Σf < 1` |
| Heat | A sealed body in human contact dissipates worse than a rack |
| Memory and world model | Off-body by architectural definition, not by capacity |

> **Edge compute is not "add as much as you like, it only costs battery." It
> eats into the convergence condition of the whole body**, and
> [02.3](02-structure-and-motion.md#23-the-endurance-ceiling) shows `γ` inflating
> non-linearly near the ceiling.
>
> The middle — feature extraction, compression, predictive modelling, tracking
> of other agents — is `⟦CTRL⟧`, and **should be adjustable per mission** rather
> than a compile-time constant.

**Operating point: `⟦CTRL⟧`.**
