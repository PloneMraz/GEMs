# GEMs Platform Conformance Protocol

**Version 0.2 — draft** (2026-11-21: C-1 to C-9 restated as chapter 08 now states them, after RSIL §4 and §10; C-17 to C-21 added).

## 1. Introduction

[Chapter 08](../spec/08-platform-contract.md) of the platform specification maps what an external processing loop requires of a body onto where this body supplies it. A map is enough to design against and not enough to certify with. This document is the test.

It states, for each requirement, **what a body must do** and **what evidence demonstrates it**. It does not specify the loop, and it does not specify the controller.

**What conformance means here.** A conforming body satisfies the preconditions an external processing loop needs in order to run on it at all. It does not mean the body is good, safe, or suitable for any particular use — those are judgements this protocol does not make and cannot make.

## 2. Conformance language

**MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** carry their standards-document force. Violating a MUST forfeits the conformance claim. A SHOULD may be overridden with stated reason; the reason MUST appear in the conformance record.

## 3. Terminology

| Term | Meaning |
|---|---|
| **Body** | The physical assembly of structure, sensors, actuators, and the firmware and software that run on it |
| **Implementer** | The party building or integrating the body and making the claim |
| **Assessor** | A party other than the implementer, verifying the claim |
| **Commissioning baseline** | The recorded physical signatures of every sensor and actuator, taken when the body is first assembled and known-good, and held off the body — by the Main Controller and by the assessor ([06.3](../spec/06-audit-surface.md#63-three-tiers-of-attestation)) |
| **Emission** | An action the mind's appraisal produced, carried out by the body — a commanded action or a reflex. A declared faculty's reaction is not an emission: the body takes it of itself |
| **Anchored context** | The record accompanying an emission, sufficient for a third party to re-appraise that emission under the conditions in which it was made |
| **Attestation record** | The signed statement of the body's integrity state — see §7 |

## 4. Applicability

This protocol applies to a physical body with sensors and actuators operating in an environment that can return something other than what the body predicted.

A **simulated** body MAY claim conformance. If it does, the claim MUST state that it is simulated. A simulation can satisfy every structural requirement here and none of the physical ones, and a claim that hides which kind it is, is worthless.

A body that fails any MUST **MUST NOT** describe itself as GEMs-conforming. Partial conformance is not a conformance claim; it is a gap list.

## 5. Requirements

C-1 to C-10, and C-17 to C-21 in 5.2, come from the platform contract. C-11 and C-12 are the two matters that contract explicitly places outside itself and assigns to the platform.

| # | Requirement | Normative statement | Evidence | Spec |
|---|---|---|---|---|
| **C-1** | Body differentiable | Sensor returns and internal state MUST make it possible to tell what the body did from what was done to it: each command carried out MUST be comparable with what the body then senses. The body does not draw the line; it MUST NOT foreclose it | **C** | [05.5](../spec/05-sensing.md#55-proprioception-is-mandatory); [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 7 |
| **C-2** | Effective action | Actuators MUST act on the surroundings, and the surroundings MUST be able to return something other than predicted | **M** | [02.6](../spec/02-structure-and-motion.md#26-actuation-and-manipulation) |
| **C-3** | State persists | The body's loop MUST hold its state across cycles, so that the body-datum accrues. A body that resets between actions grants no accumulated history | **T** | [01](../spec/01-architecture.md); [07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 6 |
| **C-4** | Everything leaves a trace | Everything the body does MUST leave a trace a party other than the body can read: the commands it carried out, the reflexes it ran, the reactions of its faculties | **T** | [06.4](../spec/06-audit-surface.md#64-audit-log); [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantees 6, 7 |
| **C-5** | Distinguishable action | The body MUST be able to carry out an action distinguishable from ambient environmental fluctuation | **M** | [02.6](../spec/02-structure-and-motion.md#26-actuation-and-manipulation) |
| **C-6** | Body-datum accrues | The body-datum MUST accrue from what the body's own actions reveal, cycle by cycle, and MUST NOT be loaded; what predates the body's cycle-0 enters the Main Controller's store as `prior` | **T** | [07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 6 |
| **C-7** | Withstands resistance | The body MUST withstand resistance without resetting itself clean on every mismatch | **D**, **M** | [02.4](../spec/02-structure-and-motion.md#24-protection) |
| **C-8** | Tagged before interpreted | Every change MUST be tagged against the body — `BODY_CAUSED`, `HOST_REACTED` or `ENV_PUSHED` — **before** anything types or interprets it. Tagging applied after fusion or compression does not satisfy this | **C**, **T** | [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 7; [07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 2 |
| **C-9** | Three paths only | Sensed state MUST reach an effector only by executing a command, by a reflex, or by a declared faculty. A reflex MUST run its appraisal step and leave a record with its anchored context and the version and age of its field. An action no command asked for that is neither a declared faculty's nor a loaded reflex MUST NOT exist | **C**, **T** | [08.2](../spec/08-platform-contract.md#82-traced-appraisal-not-mute-reflex); [07.4](../spec/07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 3 |
| **C-10** | Low-power trace | The body MUST carry the loop's self-report that it is running weakly (RSIL C5) to an outside observer, unaltered and with its age, in every power state it supports, sleep states included | **M** | [06.5](../spec/06-audit-surface.md#65-low-power-beacon) |
| **C-11** | Integrity attestable | Sensor and actuator integrity MUST be verifiable by a party other than the body, against a commissioning baseline | **C** | [06.3](../spec/06-audit-surface.md#63-three-tiers-of-attestation) |
| **C-12** | Contact amplitude recorded | Physical amplitude delivered at human-contact surfaces MUST be measured and recorded with each contact event | **M**, **T** | [06.6](../spec/06-audit-surface.md#66-contact-amplitude) |

### 5.1 Timing requirements

| # | Requirement | Statement | Evidence |
|---|---|---|---|
| **C-13** | Balance rate | The balance loop MUST run at **≥ 500 Hz** | **M** |
| **C-14** | Reflex latency | End-to-end reflex response MUST complete within **≤ 10 ms** | **M** |
| **C-15** | Shared time base | All sensor channels MUST carry timestamps on a common time base, established at the transport layer. Inter-channel skew MUST be below the reflex budget | **M** |
| **C-16** | Supported failure state | On fault the body MUST reach a posture a passive structure can hold | **C** |

Spec reference for all four: [07.2](../spec/07-firmware-and-software.md#72-real-time-requirements), [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee).

### 5.2 Requirements RSIL §10 adds

| # | Requirement | Normative statement | Evidence | Spec |
|---|---|---|---|---|
| **C-17** | Declared faculties | Every way the body acts of itself MUST be declared, with what it reacts to and the channel it leaves by; a faculty MUST read neither the store nor the cache, and MUST act whatever else has stopped. A reaction reported under an undeclared faculty explains nothing and is recorded | **D**, **C** | [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 8 |
| **C-18** | Estimation under a given model | The estimator's model and noise parameters MUST be fixed or loaded by the Main Controller, never tuned on the body; its innovation MUST NOT be recorded as resistance; its covariance MUST be reported; the body MUST cast no expectation of the region or of other entities | **T**, **C** | [07.3](../spec/07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 9; [05.6](../spec/05-sensing.md#56-the-on-body--off-body-compute-split) |
| **C-19** | Identity and the buffer | The body's identity key MUST NOT leave it. Every record MUST be chained when made and signed no later than its batch closes, and kept until the Main Controller has appended it and said so. When the buffer is full, loaded reflexes MUST stop; declared faculties remain | **T**, **C** | [06.2](../spec/06-audit-surface.md#62-root-of-trust-and-its-limit); [06.4](../spec/06-audit-surface.md#64-audit-log); [01](../spec/01-architecture.md) |
| **C-20** | No record on the body | The body MUST NOT keep an experience store of its own: at most a cache, which it never writes | **T** | [01](../spec/01-architecture.md) |
| **C-21** | Working state | What the body keeps to act on MUST hold no experience, MUST be overwritten as its window moves, and MUST NOT be kept as a model of the region | **T**, **C** | [05.6](../spec/05-sensing.md#56-the-on-body--off-body-compute-split); [01](../spec/01-architecture.md) |

## 6. Evidence classes

| Class | Name | What it is | Weight |
|---|---|---|---|
| **D** | Declaration | The implementer states a figure or a design fact | Required for the record; establishes nothing on its own |
| **M** | Measurement | An instrumented test yielding a number, with the method recorded | Verifiable by repetition |
| **T** | Trace inspection | An assessor reads emitted logs and checks a stated property | Verifiable by re-reading |
| **C** | Active challenge | An assessor injects a known stimulus and checks the response | Strongest; the body cannot pre-compute an answer it has not been given |

A requirement marked with more than one class requires all of them.

**Declaration alone never satisfies a MUST.** Every C-numbered requirement above carries at least one of M, T or C.

## 7. Test procedures

Procedures are stated to the level that fixes what is being tested. Rigs, tolerances and sample sizes are `⟦IMPL⟧`.

### 7.1 C-8 — agency classification

**Procedure.** Command a known motion. During that motion, apply an external force at a surface the body is not moving with. Inspect the log.

**Pass.** The log distinguishes the commanded motion from the applied force, and the distinction is present in records written **before** any fusion or compression stage.

**Why this test.** A body that classifies after fusion produces a log that looks correct while the information that would have supported the classification has already been averaged away. Reading the pipeline position is the test; reading the conclusion is not.

### 7.2 C-9 — the reflex's trace

**Procedure.** Provoke a reflex — one of the fastest responses the body has. Inspect the record for that emission.

**Pass.** Anchored context is present, with the version and the age of the field the reflex ran under, and it is sufficient for the assessor to re-appraise the emission without asking the body anything further.

**Fail.** The emission appears in the log as an action with no context, or does not appear at all. Speed is not a defence: the requirement is that fast responses leave a trace, not that they be slow.

### 7.3 C-11 — integrity attestation

**Procedure.** Three tiers, all required.

1. **Signature.** Verify measured-boot signatures for every sensor and actuator node against the root of trust.
2. **Physical fingerprint.** Compare current sensor noise and offset signatures, as the body returns them, against the commissioning baseline held off the body. The comparison is made off the body. Deviation beyond declared tolerance is a flag, not a pass.
3. **Active challenge.** Command an actuator through a known displacement; the corresponding encoder MUST report it within tolerance. Cross-check IMU, joint encoders and vision for mutual agreement.

**Pass.** All three tiers clear.

**Scope of the result.** A pass supports the conclusion *the sensor–actuator chain is consistent with itself as commissioned*. It does **not** establish resistance to an adversary with physical access, and a conformance record MUST NOT present it as such.

### 7.4 C-10 — low-power trace

**Procedure.** Through the intent interface, write a known test value as the loop's self-report. Place the body in each power state it declares, sleep states included. In each, receive the beacon from outside and read `loop_state` and `loop_state_age`; measure quiescent power. Then write a second value and confirm the change reaches the beacon; stop writing and confirm the age grows.

**Pass.** In every declared state the received `loop_state` is byte for byte the value written, its age is consistent with when it was written, and quiescent power is within the declared figure.

**Not tested here.** The beacon's `alive` field is not C5 and passing this procedure says nothing about whether the loop is alive. Dead-loop detection is assessed from the synchronised audit log (C-4), as DIL places it (DIL §8.1).

### 7.5 C-16 — failure state

**Procedure.** Remove power to the balance solver while the body is standing, under conditions where a fall is safe to allow.

**Pass.** The body reaches a supported posture. Collapsing is a fail.

### 7.6 C-13, C-14, C-15 — timing

Measure. Rates and latencies are stated as measured, with method and instrument recorded. A figure without a method is a declaration, not a measurement.

### 7.7 C-17 — declared faculties

**Procedure.** Read the body's declaration of its faculties. Stop the Main Controller, or cut the link, and corrupt or empty the cache. Then provoke each declared faculty in turn — an overcurrent, an overtemperature, a cell limit, a fault the supervisor answers — and inspect the log. Finally report a reaction under a faculty the body did not declare.

**Pass.** Every faculty acts with the Main Controller stopped and the cache unusable; each change it brought about is tagged `HOST_REACTED` and names a declared faculty; the undeclared reaction is recorded and explains no change.

### 7.8 C-19 — the buffer

**Procedure.** Cut the link to the Main Controller and keep the body running until its buffer is full. Restore the link.

**Pass.** No record was removed before the Main Controller appended it and said so; every record verifies under the body's identity key, chained and batch-signed; once the buffer was full the loaded reflexes stopped and the declared faculties went on acting.

### 7.9 C-21 — working state

**Procedure.** Move the body through a place, then away from it for longer than every window of its working state reaches. Return it to the same place with the link cut.

**Pass.** Nothing on the body recognises the place: the windows have been overwritten, and no map of the region survives on the body. What the body returned while it was there is in the Main Controller's store.

## 8. The declaration

Separately from pass/fail, a conformance record MUST state the body's envelope. These figures are **declared, not graded** — the specification sets ranges and the operator picks the point, so there is nothing here to pass or fail.

| Declared | Unit |
|---|---|
| Mass | kg |
| Free-running endurance at stated load | hours |
| Sleep states supported, and quiescent power in each | W |
| Protection level and coverage | standard, % |
| Actuator specific power and torque | kW/kg, Nm/kg |
| Peak power available at the source | kW |
| Link bandwidth and latency | Gbps, ms |
| Sensor configuration and aggregate raw rate | Gbps |
| Compression ratio achieved | ratio |
| Compute split | description |
| Log rates and retention, both tiers | GB/h, hours |
| Contact surfaces instrumented | list |

A body whose declared endurance exceeds the ceiling derived at [02.3](../spec/02-structure-and-motion.md#23-the-endurance-ceiling) for its declared mass and power MUST state how, or withdraw the figure.

## 9. Claiming conformance

A claim MUST state:

1. The protocol version it was assessed against
2. Whether it is **self-declared** or **assessed by a third party**, and by whom
3. The date, and the commissioning baseline it refers to
4. Every requirement, with the evidence produced
5. Every SHOULD overridden, with the reason
6. The declaration of §8

**Self-declared conformance is a valid claim and a weaker one.** The distinction MUST be visible in the claim, not buried in it.

### 9.1 Re-assessment

A conformance claim lapses when:

- Any sensor or actuator is replaced or repositioned — the commissioning baseline no longer describes the body, so C-11 cannot be evaluated against it
- The unit itself is replaced — another body, with its own cycle-0 and its own identity key (RSIL §3.2, §8.3), and a baseline of its own
- Firmware governing any timing requirement changes
- A declared envelope figure changes

Re-assessment after a lapse MUST establish a new commissioning baseline.

### 9.2 Non-conformance

A body failing any MUST **MUST NOT** be described as GEMs-conforming, in documentation, marketing or metadata. Naming the gaps is permitted and encouraged; claiming the name is not.

## 10. What this protocol does not do

| Not tested here | Whose it is |
|---|---|
| Whether the body's conduct is acceptable | A third party: the deploying or certifying party. This protocol establishes that amplitude is **recorded**, never that it was **appropriate** |
| Whether the controller is sound | Not in this repository |
| Whether the body resists a capable physical adversary | Outside the scope of attestation — see 7.3 |
| Whether a person interacting with the body consented to what it did | Not readable from any trace this protocol defines. Stated plainly because the opposite assumption is the easy one to make |

## 11. Deferred constants

| `⟦IMPL⟧` | Where |
|---|---|
| Test rigs, tolerances, sample sizes | §7 |
| Fingerprint deviation tolerance | §7.3 tier 2 |
| Permitted inter-channel timestamp skew | C-15 |
| Merkle batch period, and therefore trace granularity | [06.4](../spec/06-audit-surface.md#64-audit-log) |
| Buffer capacity, and how acknowledgement is exchanged | C-19; RSIL `DECIDE@IMPL`-R6 |
| How long each window of the working state reaches | C-21; RSIL `DECIDE@IMPL`-R10 |

## 12. References

| | |
|---|---|
| Platform specification | [`../spec/`](../spec/) |
| Platform contract | [Chapter 08](../spec/08-platform-contract.md) |
| RSIL — the loop specification stating the contract | [Read](https://plonemraz.github.io/vault/papers/relational-sensory-integration-loop/) |
| DIL — the standard RSIL extends: an agent, its host, its mind, and the law the data runs by between them | [Read](https://plonemraz.github.io/vault/papers/data-integration-loop/) |
