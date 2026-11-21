# 08 — Platform contract

A body acquires signal and executes response. What happens in between — how raw signal becomes structured information — is specified elsewhere, by a companion specification of equal rank. Neither document claims the other's territory.

That companion specification does not name this body. It states **conditions any platform must satisfy**, and this chapter records where this body satisfies them. The relation is a contract, not a cross-reference: **a contract can be checked; a cross-reference can only dangle.**

| Companion specification | Scope | Status |
|---|---|---|
| **RSIL** — Relational Sensory Integration Loop | The processing loop for an agent with a body | [Read](https://plonemraz.github.io/vault/papers/relational-sensory-integration-loop/) |
| **DIL** — Data Integration Loop | The standard RSIL extends: an agent — its host, its mind, and the law the data runs by between them. The Main Controller runs by it ([01](01-architecture.md)) | [Read](https://plonemraz.github.io/vault/papers/data-integration-loop/) |

## 8.1 Conformance map

| Requirement | What it demands of a platform | Supplied at |
|---|---|---|
| **E1** | Sensors and internal state must make a distinction between what the body did and what was done to it *possible*. The platform does not draw the line; it must not foreclose it. A body whose sensory returns cannot in principle be separated by what it commanded cannot host a body's loop | [05.5](05-sensing.md#55-proprioception-is-mandatory) — proprioception |
| **E2** | Actuators must act on the region, and the region must be able to return something other than what was predicted | [02.6](02-structure-and-motion.md#26-actuation-and-manipulation) |
| **E3** | The body's loop must hold its state across cycles, so that the body-datum accrues | [01](01-architecture.md) — memory and the record with the Main Controller, in its `[data]` and `[event]`; on each unit, the cache it is loaded with, the record buffer until the Main Controller has appended it, and its working state (RSIL §8). The body-datum (RSIL R4): no chapter specifies it yet, open ([binding §4](../software/RSIL-in-GEMs.md#4-open-in-this-binding)) |
| **E4** | Everything the body does must leave a trace a third party can read — the mind's commands it carried out, the reflexes it ran, the reactions of its faculties | [06.4](06-audit-surface.md#64-audit-log) — the audit log: each record chained and signed on the unit when made, appended by the Main Controller; [07.3](07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 6 — full-tier logging at loop rate; guarantee 7 — every change tagged, `HOST_REACTED` where a declared faculty acted; also where a stopped loop becomes detectable, as the stored behaviour-record DIL requires for it (DIL §8.1) |
| **P(a)** | The body must be able to carry out an action distinguishable from ambient fluctuation; else its second layer never reaches a first match and no body-datum crystallizes | [02.6](02-structure-and-motion.md#26-actuation-and-manipulation) |
| **P(b)** | It must hold state so the body-datum accrues, not loads | [01](01-architecture.md); the body-datum: open, as in E3 |
| **P(c)** | It must withstand resistance without resetting itself clean on every mismatch | [02.4](02-structure-and-motion.md#24-protection), [04](04-shell.md) |
| **Body differentiation (INV-6)** | Each command the body carries out must be comparable with what it then senses, *before* anything is typed or interpreted. Sensing dense enough to tell what moved from what was moved is a requirement, not a refinement | [05.5](05-sensing.md#55-proprioception-is-mandatory) — proprioception; [07.3](07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 7 — every change tagged at acquisition |
| **Three paths only (INV-8)** | Sensed state reaches an effector only by executing a command, by a law that reads no experience; by a reflex, which runs from the cache, runs its appraisal step, and leaves a record with its anchored context and its field's version and age; or by a declared faculty. Every action no command asked for is declared as a reaction or loaded as a reflex | 8.2 below; [07.4](07-firmware-and-software.md#74-what-software-must-guarantee) guarantee 3 — a context record for every output event, reflexes included, each with its field's version and age; [07.5](07-firmware-and-software.md#75-link-loss-and-the-obc) — the OBC runs the loaded reflexes and decides nothing; [07.3](07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 8 |
| **Declared faculties** | Every way the platform acts of itself is declared, with what it reacts to and the channel its action leaves by; it reads neither the store nor the cache, and acts whatever else has stopped | [07.3](07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 8 — a faculty for an electrical stimulus from outside is not yet specified: open |
| **Estimation** | Estimators run on models fixed or loaded by the mind; their innovations are not recorded as resistance; the platform casts no expectation of the region or of other entities | [07.3](07-firmware-and-software.md#73-what-the-real-time-code-must-guarantee) guarantee 9; [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) — the unit estimates only its own state |
| **Identity and the buffer** | Each body has an identity key whose secret half does not leave it; every record is signed and chained when made, and kept until acknowledged | [06.2](06-audit-surface.md#62-root-of-trust-and-its-limit) — a non-exportable private key in the secure element; [06.4](06-audit-surface.md#64-audit-log) — chained at full rate, signed per batch; [01](01-architecture.md) — the record buffer, kept until the Main Controller has appended it and said so |
| **No record on the body** | The body keeps no experience store of its own: at most a cache, which it never writes | [01](01-architecture.md) — the experience store is the Main Controller's; a unit holds its cache, its record buffer and its working state |
| **Working state** | What a body keeps to act on — its sensing windows, its estimators' state, its reconstruction of the space around it — holds no experience, is overwritten as its window moves, and is never kept as a model of the region | [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) — the space around the unit reconstructed over a bounded window; a map kept beyond it is the Main Controller's; [01](01-architecture.md) |
| **C5** | The platform must be able to carry the loop's low-power report — in RSIL's definition, the loop's own report that it is running weakly — to an outside observer in every power state it supports, unaltered and with its age | [06.5](06-audit-surface.md#65-low-power-beacon) — the beacon carries the loop's `loop_state` report unaltered, with its age (`loop_state_age`), including during sleep. The body transmits; the loop reports |

The companion specification names four places where a conventional sensorimotor chain skips a step (RSIL §10): sensor data routed straight to interpretation, with no body gate (INV-6); sensed state mapped to an actuator command no command asked for, with no appraisal and no record (INV-8); protective responses left undeclared, or reading stored data to decide (declared faculties); and no report of the loop's weakness at low power (C5). They are where its requirements are most likely to conflict with an existing platform design, and the load-bearing part of this contract.

## 8.2 Traced appraisal, not mute reflex

The contract rejects a scar-to-action shortcut that bypasses appraisal. Reflex is not such a shortcut: it is **appraisal under a scar-dominated field** (RSIL §7.1) — the appraisal step still runs, its verdict all but foreclosed by the scar that dominates the field.

This is not pedantry. An action emitted without appraisal **carries no anchored context**, so a third party cannot re-appraise it, and the audit plane goes blind exactly where it matters.

The distinction, stated in platform terms, is the difference between *"no fast responses allowed"* — wrong, and would make a physical body unusable — and *"even fast responses must leave an auditable trace"* — right, and achievable.

**Hardware requirement.** The on-board compute must not be a straight-through reflex layer. It must run the full appraisal cycle (abbreviated, its verdict all but foreclosed, as it may be) **and** write a context record for synchronisation off-board. In engineering terms this is the reflex decision stage of the [firmware reflex budget](../firmware/ARCHITECTURE.md#2-the-reflex-budget) and the anchored tier of the [audit log](06-audit-surface.md#64-audit-log).

**Cost and benefit.** Each reflex pays a small logging overhead — microseconds against a 10 ms budget. In exchange, the off-board compute is never blind to what the body has already done, which is what makes "the body is replaceable, the data is preserved" true rather than aspirational.

## 8.3 Two frequency anchors

| Loop | Rate |
|---|---|
| Balance | **≥ 500 Hz** |
| Fast reaction | **≤ 10 ms** |

These size the edge compute and its power budget, and they set the lower end of the split in [05.6](05-sensing.md#56-the-on-body--off-body-compute-split).

> **Keep the frequency, drop the topology.** The balance loop still runs at 500 Hz and reflex still answers within 10 ms — but as an *appraisal under a scar-dominated field that leaves a trace*, not as a hardware interrupt routed around everything. The contract forbids losing the trace; it does not forbid being fast.

## 8.4 Sensing requirements follow from the contract

DIL distinguishes two grades of resistance (DIL §2, §3), and RSIL keeps them: a body meets resistance by two carriers, force and content, which cut across the grades — another person's shove and another person's contradicting word are both the second grade (RSIL §2). Resistance from inert physical fact is consistent and objective but never reacts to this body specifically. Resistance from another living, reacting party — which may shift stance, may respond to this body in particular — is the **only** source from which a model of a genuinely independent other can be built.

A loop running only against inert resistance degrades: it feeds on its own output and digests itself (DIL §8.3).

**Therefore the sensing requirement is not decoration.** Sensors must be good enough to register the fine mismatches that occur when a real person responds outside prediction. This is the principled justification for keeping group 1 at full requirement in [01](01-architecture.md).

## 8.5 What the contract does not cover

| Outside the contract | Whose it is |
|---|---|
| Verifying the body's physical integrity | The platform — supplied at [06.3](06-audit-surface.md#63-three-tiers-of-attestation). The companion specification provides a *symptom* through its log and states plainly that this is not an examination |
| The standard for acceptable physical amplitude toward a person | A third party — the deploying or certifying party. The platform supplies the measured trace ([06.6](06-audit-surface.md#66-contact-amplitude)); it does not supply the standard |
| Who the judging third party is | Outside both specifications |

## 8.6 Conformance

This chapter is a map. The test is the [platform conformance protocol](../protocol/conformance.md), which states how a body demonstrates each row of 8.1 and what evidence settles it.

Conformance there is **binary** — a loop whose preconditions are half-met does not half-run — while the body's envelope figures are **declared, not graded**, because this specification sets ranges and the operator picks the point.
