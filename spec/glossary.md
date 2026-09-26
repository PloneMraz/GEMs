# Glossary

Technical terms in this repository follow standard usage in robotics, embedded
systems and systems engineering. Where the repository once used a term of its
own, this page says what the standard term is and whether the repository has
changed over to it.

## Standard terms as used here

| Term | Meaning here | Standard source |
|---|---|---|
| **Firmware** | Software resident in the non-volatile memory of an embedded device and executed by it — joint drive boards, the real-time controller, the battery management board, the secure element, the trace radio | ISO/IEC 12207: "a combination of a hardware device and computer instructions or computer data that reside as read-only software on the hardware device"; vocabulary per ISO/IEC/IEEE 24765 |
| **Software** | Code executed on the application processors under a general-purpose operating system, device drivers included | General usage; drawing the line at the processor is this repository's application of the firmware definition above |
| **Hard real-time** | A task whose deadline miss is a failure and may cause harm; its worst case must be bounded by construction | Real-time systems literature (Kopetz; Buttazzo) |
| **Firm real-time** | A task whose late result has no value and is discarded, without harm | same |
| **Soft real-time** | A task whose late result has reduced value | same |
| **Non-real-time** | A task with no deadline | same |
| **Deadline**, **deadline miss** | The time by which a task must complete, and the event of it not doing so | same |
| **RTOS** | Real-time operating system: one whose scheduling bounds worst-case response | same |
| **EBOM**, **MBOM**, **SBOM** | Engineering, manufacturing and software bills of materials | see [`hardware/bom/`](../hardware/bom/README.md) |
| **TM**, **LAB** | Commercially available; demonstrated in the laboratory but not scaled | [00](00-scope-and-criteria.md) |
| **`⟦IMPL⟧`**, **`⟦CTRL⟧`** | Left open until parts are chosen; left to the operator | [09](09-open-constants.md) |

## Terms changed to standard usage

| Was | Now | Why |
|---|---|---|
| Firmware "owns time", software "owns meaning"; "anything with a deadline is firmware" | Firmware and software by where code runs; hard, firm, soft and non-real-time by the consequence of a late result; every hard real-time task is firmware | The old rule merged two independent classifications. It made a camera driver on the application processor "firmware", and it placed agency classification on both sides of the line at once |

## Repository terms still to review

These are terms the repository uses that are not standard engineering
vocabulary. Some come from the RSIL and DIL papers the repository answers to,
where they name concepts rather than components, and renaming them would break
that correspondence. None has been changed yet; each needs a decision.

| Repository term | Nearest standard term | Note |
|---|---|---|
| Emission log | Audit log; event log | Used in code (`software/audit_log.py` already says audit) and in protocol evidence classes |
| Low-power trace, trace emitter | Telemetry beacon; heartbeat | |
| Vigilance circuit | Always-on domain; wake-up circuit | |
| Floor power | Quiescent power; standby power | |
| On-body / off-body seat | On-board / off-board compute; edge / remote | "Two seats" is the architecture's own image (spec 01) |
| Agency classification, self-caused / external | Self/other discrimination by efference copy; sense of agency | Both are established terms in motor control and cognitive science; the repository's usage is close already |
| Anchored context | Provenance record; context record | |
| Traced appraisal | — | An RSIL concept, not a component; no engineering equivalent to adopt |
| Dock | Docking station; charging station | Already standard |
