# 06 — Audit surface

This chapter does not come from reducing an earlier ambition. It comes from the
platform contract of [08](08-platform-contract.md): two requirements the body
must satisfy, and two that an external processing specification explicitly
declares **outside its own scope and belonging to the platform**.

## 6.1 Four demands, one surface

| Source | Demand | Why it binds |
|---|---|---|
| **Readable emission** | Every emission must leave a trace a third party can read | Without it, success measured from outside cannot be measured at all |
| **Low-power trace** (RSIL C5) | That trace must remain emittable at quiescent power | A closure condition, not a convenience |
| **Body integrity** | Sensor and actuator integrity must be verifiable | A recovery snapshot covers the system, not the body. A body compromised at sensor or actuator level re-infects a freshly clean system on the first cycle |
| **Contact amplitude** | Physical amplitude at human contact must be recorded | The cheapest way to provoke a strong response from a person can be to touch them |

The four have different origins and demand the same thing: **a plane that is
checkable from outside, attached to the body, not self-reported by the part being
checked.**

## 6.2 Root of trust, and its limit

A hardware root of trust: a secure element holding a non-exportable private key,
measured boot hashing and signing the firmware of every sensor and actuator
node, and a monotonic clock that cannot be wound back. Available technology:
TPM 2.0, TrustZone-class trusted execution. **TM.**

> **The limit is stated here rather than buried at the end:** a signature proves
> **firmware**, not **physics**. A sensor swapped for a different sensor running
> valid firmware passes the signature check. The root of trust is necessary and
> **not sufficient** — 6.3 exists because of exactly this gap.

## 6.3 Three tiers of attestation

| Tier | Mechanism | Catches | Maturity |
|---|---|---|---|
| **1. Signature** | Measured boot, per-node firmware signing | Modified firmware, foreign nodes | **TM** |
| **2. Physical fingerprint** | Every real sensor carries its own noise and offset signature — photosite noise floor, IMU zero bias, joint friction curve. Baselined at commissioning; deviation beyond tolerance raises a flag | Hardware swapped for hardware running valid firmware | **LAB/TM** — the same family as physically unclonable functions and sensor noise identification |
| **3. Active challenge and redundant cross-check** | Emit a known stimulus and check the response: an actuator turns a known angle and the encoder must report that angle; IMU, joint encoders and vision must agree within tolerance | A channel that is lying, even one that passes tiers 1 and 2 | **TM** |

> **Tier 3 is not new hardware.** [05.5](05-sensing.md#55-proprioception-is-mandatory)
> already requires proprioception dense enough to separate "I moved" from
> "something moved me." That machinery **is** the machinery that detects a lying
> channel: both are redundant comparison between command issued and quantity
> measured.
>
> **One set of hardware, two uses.** The proprioception requirement is justified
> on experience grounds alone; it carries body-integrity verification at no
> additional mass.

**Scope of the claim:** the three tiers support a conclusion of the form *"the
sensor–actuator chain is consistent with itself as commissioned."* That is the
examination the contract asks for. It is not, and must not be presented as, a
guarantee against an adversary with physical access — see 6.6.

## 6.4 Audit log

Two tiers, matching the on-board / off-board split of [01](01-architecture.md). The anchored tier carries what RSIL calls the anchored context of each emission (spec 08.2):

| Tier | Content | Location | Rate |
|---|---|---|---|
| **Full** | Per joint: command, position, current, torque | Ring buffer on the body, for forensics | Control-loop rate (≥500 Hz) |
| **Anchored** | Per emission: the anchored context, enough for a third party to re-appraise it | Synchronised off-body | Per event |

Budget:

- **Full tier:** 40 DOF ([declared configuration](../hardware/kinematics.md))
  × 4 channels × 4 bytes × 500 Hz ≈ **320 kB/s ≈ 2.6 Mbps
  ≈ 1.15 GB/hour**. Against an 8 Gbps link: **0.03%**. On a 2 TB on-body SSD:
  ~1700 hours.
- **Anchored tier:** orders of magnitude smaller. A compact context record costs
  microseconds and does not threaten a 10 ms budget.

> **A signing constraint that is easy to specify wrongly.** A secure element
> signs on the order of tens to hundreds of signatures per second — it cannot
> sign 500 Hz × 40 channels. Therefore: **hash-chain at full rate** (hardware
> hashing runs at MB/s, with room to spare) and **sign a Merkle root per batch**.
> The batch period is `⟦IMPL⟧`; it trades trace granularity against signing load.

## 6.5 Low-power beacon

The beacon is how this body meets RSIL C5, the observable low-power trace
(spec 08.1). It must survive sleep levels 2 and 4
([03.4](03-energy.md#34-four-state-levels)). Mechanism: a low-duty-cycle radio
periodically emitting a signed summary — alive, state, Merkle root of the log.

Anchored on a common BLE SoC: **4.6 mA at 0 dBm** while transmitting for a few
milliseconds, **~1.5 µA** between. At a 1-second advertising interval the
average lands in the **tens of µA** — **under one milliwatt**. *Sourced.*

> **This is effectively free in power terms.** Against the quiescent power of
> [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) and against hundreds
> to thousands of watts in motion, sub-milliwatt is rounding noise. **The
> low-power beacon is not an energy problem; it is a specification omission**, and
> this chapter closes it without touching the mass budget.
>
> Note the direction: this is a **transmit** path, distinct from the receive-side
> spatial sensing that stays awake during sleep. Shared radio hardware is
> acceptable; conflated roles are not.

## 6.6 Contact amplitude

The division that applies here is the one from [00](00-scope-and-criteria.md):
**declaring a measurable envelope is declaring capability, not cutting
specification for ethical reasons.**

| Measured | Where | Why |
|---|---|---|
| Contact force and torque | Hands, forearms, every human-contact surface | The mechanical amplitude actually transmitted to a person |
| Surface temperature | Contact regions | The shell carries micro-thermal regulation ([04](04-shell.md)) |
| Vibration amplitude and frequency | The cardiac co-regulation module ([05.3](05-sensing.md#53-channels)) | This is a **measurable** physiological intervention channel |
| Contact duration and frequency | Whole body | A brief intervention is not a sustained one |

Every contact event enters the anchored tier of 6.4 with its measured amplitude.

> **What this does and does not achieve.** It makes the **intervention**
> visible: how much vibration, at what rhythm, for how long, how often —
> readable by a third party, independent of whether the party performing it
> noticed.
>
> **It does not make consent visible.** Whether a person is being steered toward
> a state they did not choose is not readable from physiological indices, and it
> is not readable from an amplitude log either. The hardware supplies the
> **trace**; the **standard against which the trace is judged** belongs to a
> third party. A deployment that supplies the body and not the standard has
> supplied half of what is required.

## 6.7 Hard constraints

| # | Constraint | Content |
|---|---|---|
| 1 | **Attestation does not prove physics** | The three tiers support *consistent with itself as commissioned*. An adversary with sufficient physical access and capability defeats it. This is a known limit of every attestation system, not a defect peculiar to this one |
| 2 | **An unsynchronised trace dies with the body** | The full tier lives on the body. Losing the body loses whatever has not synchronised — exactly the trade declared in [01](01-architecture.md). Synchronisation frequency is `⟦CTRL⟧` |
| 3 | **A trace is not a verdict** | This chapter supplies what is readable, not what is right |
| 4 | **Cheap in power, not in discipline** | Under a milliwatt (6.5); 0.03% of the link (6.4). The expensive part is the **design constraint**: every sensor and actuator node must sit under the root of trust from the start. Retrofitting it to a finished body is close to impossible |

**Operating point: `⟦CTRL⟧`.** Signing period, synchronisation frequency, flag
tolerances — the controller chooses.
