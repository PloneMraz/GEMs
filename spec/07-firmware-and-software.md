# 07 — Firmware and software

What runs on the body. This chapter states responsibilities, rates and
guarantees; it does not specify an implementation.

It does not describe the controller. The stack here executes, processes and
records — it does not decide. Where the line between them is not obvious, 9.5
draws it.

## 7.1 The division

Two classifications apply to every piece of code on the body, and they are
independent. Terms follow standard usage; see the [glossary](glossary.md).

**Where it runs — firmware or software.** Firmware is software resident in the
non-volatile memory of an embedded device and executed by it: in the wording of
ISO/IEC 12207, the combination of a hardware device and the instructions and data
that reside on it as read-only software. Here that means code running directly
on a microcontroller, bare metal or under an RTOS. Software is code running under
an operating system on an embedded computer — Linux, with or without a real-time
kernel — including the device drivers that run there.

| Layer | Runs on | Contents |
|---|---|---|
| **Firmware** | Joint drive boards, the battery management board, the secure element, the beacon radio | Current and position loops, battery management, secure boot and attestation, low-power beacon |
| **Software** | The edge AI module, under Linux | Camera, LiDAR, audio and SDR drivers and capture, feature extraction and compression, sensor fusion, predictive modelling, log assembly and synchronisation, link management |
| **Either, by decision D-3** | The real-time controller: a microcontroller under an RTOS, or an embedded computer under Linux with a real-time kernel | State estimation, balance loop, reflex path including agency tagging, safety supervisor, power-state machine, full-tier log writing at loop rate |

The real-time controller's code is firmware or software according to which
processor D-3 selects ([plan](../plan/README.md#3-decisions-that-block-everything-else)).
Its deadlines do not change with the choice; only the evidence that they are met
does.

**How late it may be — the real-time class.** A task's class is set by the
consequence of missing its deadline, as the real-time systems literature defines
it:

| Class | A late result | Here |
|---|---|---|
| **Hard real-time** | is a failure — it may cause harm | Current loops, balance, reflex path, agency tagging, safety supervisor |
| **Firm real-time** | has no value and is discarded, without harm | Per-frame capture and encoding |
| **Soft real-time** | has reduced value | Sensor fusion, link management |
| **Non-real-time** | is merely late | Log synchronisation after an outage, commissioning tools |

**The rule that joins them: every hard real-time task runs on a platform whose
worst-case latency is bounded.** The two axes stay independent — the rule
constrains the platform, not the layer — and the bound is established one of two
ways, recorded per task in [`realtime_config/`](../realtime_config/):

| Platform | How the bound is established |
|---|---|
| Microcontroller, bare metal or RTOS | **By construction**: fixed-priority or interrupt scheduling with a schedulability analysis of every task set |
| Linux with a real-time kernel (PREEMPT_RT), tasks under `SCHED_FIFO` or `SCHED_DEADLINE` on isolated cores | **By configuration and measurement**: latency measured under worst-case load and recorded as evidence. `SCHED_DEADLINE` guarantees deadlines only while total utilisation stays within the cores available, so the evidence must include the utilisation budget |

A Linux task without a real-time kernel and a real-time scheduling policy has no
bounded worst case, and cannot carry a hard real-time task.

## 7.2 Real-time requirements

| Loop | Rate | Class | Consequence of missing it |
|---|---|---|---|
| Joint current control | `⟦IMPL⟧`, typically kHz-class | hard | Actuator instability |
| Proprioceptive sampling | **1 kHz** | hard | Agency tagging degrades; see 7.3 |
| Balance | **≥ 500 Hz** | hard | The body falls |
| Reflex, end to end | **≤ 10 ms** | hard | The reaction is not a reaction |

Every task's layer, rate, deadline, stage budget and deadline class is held in
[`realtime_config/tasks.csv`](../realtime_config/tasks.csv), and its platform and
scheduling policy in [`realtime_config/scheduler.csv`](../realtime_config/scheduler.csv);
`python realtime_config/check_timing.py` checks both against this section.

**Multi-stream timestamping.** Every sensor channel MUST carry timestamps on a
common time base, established at the transport layer rather than inferred later.
Channels arrive at rates differing by three orders of magnitude
([05](05-sensing.md)); without a shared clock, fusing them produces confident
nonsense. The permitted skew between channels is `⟦IMPL⟧` and is bounded above
by the reflex budget: skew that approaches 10 ms has already broken the reflex
path.

> Link round-trip is ~1 ms at ideal short range but cannot be relied on for
> ≤10 ms at kilometre range. The two rates above are therefore **on-body by
> necessity**, as [05.6](05-sensing.md#56-the-on-body--off-body-compute-split)
> establishes. They are not a partitioning preference.

## 7.3 What the real-time code must guarantee

These bind the firmware and the real-time controller together — whichever layer
decision D-3 places the controller in.

| # | Guarantee | Note |
|---|---|---|
| 1 | **Determinism within the budgets of 7.2** | Watchdogs and deadline-miss reporting on every hard real-time task |
| 2 | **A supported failure state** | On fault the body must reach a posture a passive structure can hold — the same requirement sleep places on posture ([03.3](03-energy.md#33-tiered-sleep)). Collapsing is not a failure state; it is a second failure |
| 3 | **Power-state transitions** | The four levels of [03.4](03-energy.md#34-four-state-levels), including wake latency appropriate to the level left |
| 4 | **Measured boot and attestation** | Every sensor and actuator node under the root of trust ([06.2](06-audit-surface.md#62-root-of-trust-and-its-limit)) |
| 5 | **Beacon transmission at quiescent power** | Survives sleep levels 2 and 4 ([06.5](06-audit-surface.md#65-low-power-beacon)) |
| 6 | **Full-tier logging at loop rate** | Hash-chained, not signed per record ([06.4](06-audit-surface.md#64-audit-log)) |
| 7 | **Agency tagging at acquisition** | Every change tagged self-caused or external where the commanded and measured values meet, within the 0.5 ms stage of the reflex budget ([firmware architecture §2](../firmware/ARCHITECTURE.md#2-the-reflex-budget)) |

> Guarantee 2 deserves emphasis because it is easy to specify as an
> afterthought. A body that loses power or loses its balance solver while
> standing is a falling mass of 70–160 kg
> ([02.5](02-structure-and-motion.md#25-mass-envelope)) that may be in contact
> with a person. The failure state is a design requirement of the same rank as
> the loops themselves.

## 7.4 What software must guarantee

| # | Guarantee | Source |
|---|---|---|
| 1 | **Compression of at least 2:1, realistically 8:1** | [05.4](05-sensing.md#54-aggregate-rate-against-the-link) — below this the link cannot carry the body's own senses |
| 2 | **Agency tag carried to interpretation** | Nothing interprets an untagged change, and no stage strips the tag that firmware attached (7.3 guarantee 7; [08.1](08-platform-contract.md#81-conformance-map)) |
| 3 | **A context record for every output event** | Including reflexes — RSIL INV-8: anchored context on every emission. A fast action that leaves no context record is what the contract forbids ([08.2](08-platform-contract.md#82-traced-appraisal-not-mute-reflex)) |
| 4 | **Log assembly and synchronisation** | Two tiers, Merkle-batched signing ([06.4](06-audit-surface.md#64-audit-log)) |
| 5 | **Graceful link degradation** | Reduced fidelity before dropped streams; the body should lose resolution, not lose senses |

**On guarantee 2.** Agency tagging is done **in firmware, at acquisition**
(7.3 guarantee 7), not as a later correction in software. Once a stream has been fused, filtered or compressed
without the self-caused/external distinction attached, the distinction cannot be
recovered downstream — the information that would have carried it has already
been averaged away.

**On guarantee 3.** The cost is a compact context record per output event,
microseconds against a 10 ms budget. This is what makes *the body is
replaceable, the data is preserved* true rather than aspirational: the off-board
compute is never blind to what the body has already done.

## 7.5 Link loss and the local core

A local core is mandatory ([01](01-architecture.md)). On link loss it MUST:

| | Behaviour |
|---|---|
| **Maintain** | Balance, posture, and a supported state if it cannot maintain those |
| **Preserve** | State and log. Nothing acquired during the outage may be discarded to save space before it is synchronised |
| **Continue** | Logging, at both tiers, so that the outage is itself auditable |
| **Attempt** | Link re-establishment |

**What the local core does not do: decide.** It runs pre-loaded reflexes and
preserves what it holds. It is not a reduced controller and must not be
specified as one, because a body that substitutes its own judgement during an
outage produces actions no one can attribute afterwards — the precise failure the
audit surface exists to prevent.

> The boundary is architectural, not cautious. Reflexes are loadable; the
> interpretation of priorities in an unforeseen situation is not a reflex, and
> nothing in this repository claims to supply it.

## 7.6 Resource budget

| Resource | Figure | Binds against |
|---|---|---|
| Compute power | Draws on the same `p` (W/kg) that enters `Σf < 1` | [02.1](02-structure-and-motion.md#21-the-mass-loop) — edge compute eats the convergence condition, not merely the battery |
| Thermal | A sealed body in human contact dissipates worse than a rack | `⟦IMPL⟧` |
| Log storage | **1.15 GB/hour** full tier; ~1700 hours on a 2 TB device | [06.4](06-audit-surface.md#64-audit-log) |
| Link share, full-tier log | **0.03%** of 8 Gbps | [06.4](06-audit-surface.md#64-audit-log) |

## 7.7 Open constants

| Value | Why not filled |
|---|---|
| Joint current loop rate | Depends on actuator and driver selection |
| Permitted inter-channel timestamp skew | Bounded above by the reflex budget; the working figure depends on the transport |
| Thermal envelope for edge compute | Depends on packaging |
| Split of processing between body and external system | `⟦CTRL⟧` within the two hard ends of [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) |

**Operating point: `⟦CTRL⟧`.**
