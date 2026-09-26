# Glossary

Technical terms in this repository follow standard usage in robotics, embedded
systems and systems engineering. Where the repository once used a term of its
own, this page says what the standard term is and whether the repository has
changed over to it.

## Standard terms as used here

| Term | Meaning here | Standard source |
|---|---|---|
| **Firmware** | Code running directly on a microcontroller, bare metal or under an RTOS — joint drive boards, the battery management board, the secure element, the beacon radio, and the real-time controller if D-3 makes it a microcontroller | ISO/IEC 12207: "a combination of a hardware device and computer instructions or computer data that reside as read-only software on the hardware device"; vocabulary per ISO/IEC/IEEE 24765 |
| **Software** | Code running under an operating system on an embedded computer — Linux, with or without a real-time kernel — device drivers included | General usage; drawing the line at the processor is this repository's application of the firmware definition above |
| **Hard real-time** | A task whose deadline miss is a failure and may cause harm; its worst case must be bounded by construction | Real-time systems literature (Kopetz; Buttazzo) |
| **Firm real-time** | A task whose late result has no value and is discarded, without harm | same |
| **Soft real-time** | A task whose late result has reduced value | same |
| **Non-real-time** | A task with no deadline | same |
| **Deadline**, **deadline miss** | The time by which a task must complete, and the event of it not doing so | same |
| **RTOS** | Real-time operating system: one whose scheduling bounds worst-case response | same |
| **PREEMPT_RT** | The real-time preemption patch set for the Linux kernel, which bounds scheduling latency closely enough for many real-time control loops; the bound is established by measurement | Reghenzani et al., "The Real-Time Linux Kernel: A Survey on PREEMPT_RT", ACM Computing Surveys |
| **`SCHED_FIFO`** | Linux fixed-priority real-time scheduling policy | Linux kernel documentation |
| **`SCHED_DEADLINE`** | Linux earliest-deadline-first scheduling with a constant bandwidth server; each task declares runtime, deadline and period, and deadlines hold only while total utilisation stays within the cores available | [Linux kernel documentation](https://docs.kernel.org/scheduler/sched-deadline.html) |
| **Reference model** | An executable specification that a port is checked against; it runs on no target. Here: [`reference/`](../reference/) | General usage ("golden model") |
| **EBOM**, **MBOM**, **SBOM** | Engineering, manufacturing and software bills of materials | see [`hardware/bom/`](../hardware/bom/README.md) |
| **TM**, **LAB** | Commercially available; demonstrated in the laboratory but not scaled | [00](00-scope-and-criteria.md) |
| **`⟦IMPL⟧`**, **`⟦CTRL⟧`** | Left open until parts are chosen; left to the operator | [09](09-open-constants.md) |

## Where each vocabulary belongs

Two vocabularies meet in this repository, and each has a place.

**RSIL and DIL terms are kept, in the contract layer.** They name concepts of
the companion specifications, not components, and renaming them would break the
correspondence with those papers. Their place is where the contract is stated
and tested — [spec 08](08-platform-contract.md), [`protocol/`](../protocol/) —
and the field names of the audit-log record schema, which carries the
contract's evidence. Verified against the RSIL text: *appraisal*, *scar*,
*appraisal under a scar-dominated field*, *anchored context*, *emission*,
*trace*, *agency* (`AgencyTag`, `SELF_CAUSED`), *caused-by-me*, *region*,
*resistance*, *reflex*, and the requirement labels INV-6, INV-8, C5, E1–E4.

**Everywhere else, engineering terms.** Where an engineering item realises a
contract term, it takes the engineering name and cites the contract term once:
"reflex decision (RSIL INV-8: appraisal under a scar-dominated field)".

## Terms changed to standard usage

| Was | Now | Why |
|---|---|---|
| Firmware "owns time", software "owns meaning"; "anything with a deadline is firmware" | Firmware runs directly on a microcontroller, software under an operating system; hard, firm, soft and non-real-time by the consequence of a late result, held in `realtime_config/`; every hard real-time task runs on a platform whose worst-case latency is bounded — by construction on a microcontroller, by measurement under a real-time Linux policy | The old rule merged two independent classifications. It made a camera driver on the application processor "firmware", and it placed agency tagging on both sides of the line at once. A first correction tied hard real-time to firmware; that still bound one axis to the other, and was relaxed to a rule on the platform |
| Emission log (the component) | **Audit log**; `AuditLog` in code | *Emission* stays as the contract's word for an output event, and *anchored* as the name of the tier that holds its anchored context (`Tier.ANCHORED`, matching spec 06.4) |
| Low-power trace (the component), trace emitter, trace radio | **Low-power beacon**, beacon radio | *Low-power trace* stays as the name of RSIL C5, which the beacon satisfies |
| Floor power | **Quiescent power** | Also avoids a clash with RSIL's unrelated *floor-tag* |
| Vigilance circuit, vigilance rail | **Always-on wake-up circuit**, always-on rail | Not an RSIL term |
| On-body / off-body seat | **On-board / off-board compute** | "One intelligence, two seats" stays as the name of the architectural principle in [spec 01](01-architecture.md), where it is defined; "seat" is not an RSIL term |
| Pre-closed appraisal | **Reflex decision** in engineering text; **appraisal under a scar-dominated field** (RSIL §9.7) in the contract | "Pre-closed" was this repository's paraphrase, not RSIL's wording |
| Appraisal, integration (reflex stages) | Reflex decision, state assembly | |
| Agency classification | **Agency tagging**, a firmware task | *Agency* itself is the contract's term and stays |

## Open question found in the review

**RSIL C5 and the low-power beacon may not mean the same thing.** RSIL defines
C5 as "self-reports low power: the system emits a trace of *the loop is running
weakly*", and states that C5 is not a criterion for detecting a dead loop.
Spec 06.5 meets C5 with a radio beacon that keeps transmitting a signed "alive"
summary at low electrical power while the body sleeps — closer to a liveness
heartbeat, which is what RSIL says C5 is not. Whether the beacon should also
carry a loop-weakness signal, or whether the mapping in spec 08.1 should be
restated, is a decision for the specification's author; nothing has been
changed on this point.
