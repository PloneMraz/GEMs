# Firmware architecture

The specification states what firmware must guarantee. This document states how
the work is divided so that it can, and — the part that is genuinely new here —
**how the 10 ms reflex budget is spent**.

Nothing below fixes a part. Where a figure depends on hardware not yet chosen it
is marked `⟦IMPL⟧` and stays marked.

## 1. Modules and the deadline each owns

| Module | Owns | Deadline | Source |
|---|---|---|---|
| **Sensor drivers** | Acquisition and timestamping at source, on the embedded nodes — IMU, encoders, joint torque, tactile readout. Camera, LiDAR, audio and SDR capture run on the application processor and are software ([07.1](../spec/07-firmware-and-software.md#71-the-division)) | per-channel rate | [07.2](../spec/07-firmware-and-software.md#72-real-time-requirements) |
| **Time base** | One clock all channels share, established at transport | skew below the reflex budget | 07.2 |
| **Actuator drivers** | Current and position loops | `⟦IMPL⟧`, kHz-class | 07.2 |
| **State estimator** | Joint state, IMU fusion, contact state | 1 kHz | 07.2 |
| **Balance controller** | Posture and ZMP | **≥ 500 Hz** | 07.2 |
| **Reflex path** | Reflex decision and command | **≤ 10 ms** end to end | 07.2 |
| **Power state machine** | The four levels, and wake latency per level | transition-bounded | [03.4](../spec/03-energy.md#34-four-state-levels) |
| **Safe-state supervisor** | Reaching a supported posture on fault | must beat the fall | [07.3](../spec/07-firmware-and-software.md#73-what-firmware-must-guarantee) |
| **Attestation agent** | Measured boot, per-node signatures, challenge responses | boot and on demand | [06.3](../spec/06-audit-surface.md#63-three-tiers-of-attestation) |
| **Log writer** | Full-tier records, hash-chained at loop rate | loop rate | [06.4](../spec/06-audit-surface.md#64-audit-log) |
| **Low-power beacon** | Signed summary at quiescent power | duty-cycled | [06.5](../spec/06-audit-surface.md#65-low-power-beacon) |

**One rule across all of them.** A module that misses its deadline must say so.
A late result delivered silently is worse than a reported miss, because the
layer above cannot tell the difference between fresh and stale, and the log will
record a decision made on data that was not what it appeared to be.

## 2. The reflex budget

10 ms is the whole path — stimulus at a sensor to motion at an actuator, not
the compute portion of it. A proposed division:

| Stage | Budget | Note |
|---|---|---|
| Acquisition and timestamp | 1.0 ms | Includes transduction at the node |
| Agency tagging | 0.5 ms | Self-caused or external, before anything interprets |
| State assembly | 2.0 ms | Assembling the state the reflex decision reads |
| Reflex decision | 1.0 ms | Lookup against the loaded reflex set; not skipped (RSIL INV-8: appraisal under a scar-dominated field, [spec 08.2](../spec/08-platform-contract.md#82-traced-appraisal-not-mute-reflex)) |
| Command and actuation onset | 4.0 ms | Mechanical response begins |
| Log write | 0.05 ms | Compact context record |
| **Margin** | **1.45 ms** | Unallocated, deliberately |
| **Total** | **10.0 ms** | |

> **The log write is 0.5% of the budget.** This is the number that answers the
> objection that a context record per reflex (RSIL: traced appraisal) costs too
> much to run at reflex speed. It does
> not. What it costs is the discipline of having a place to write to, which is a
> design constraint rather than a time cost — see
> [06.7](../spec/06-audit-surface.md#67-hard-constraints).
>
> **The reflex decision stage is not optional and not zero.** It still runs,
> however little it has left to decide; that is what makes the output event
> re-appraisable from outside, which is what RSIL INV-8 asks. A
> firmware design that discovers it is over budget and reclaims this millisecond
> has stopped conforming ([protocol C-9](../protocol/conformance.md)).

The split is `⟦IMPL⟧` and will move once real parts exist. The same figures are
held, with every task's layer and deadline class, in
[`../realtime/tasks.csv`](../realtime/tasks.csv), and
`python realtime/check_timing.py` fails if the two disagree. The margin is not
spare capacity to be spent later — it absorbs the jitter that measurement will
find.

## 3. The balance loop

500 Hz is a 2 ms period. Within it:

| Stage | Budget |
|---|---|
| State estimate | 0.6 ms |
| Control solve | 0.8 ms |
| Command dispatch | 0.3 ms |
| Log write | 0.05 ms |
| Margin | 0.25 ms |

Balance and reflex share sensors and actuators but not deadlines. Where they
contend, **balance wins**: a body that reflexes correctly while falling has
failed at the thing that keeps the reflex worth having.

## 4. The interface to software

Firmware hands up, software hands down. The boundary is narrow on purpose.

| Direction | Carries | Rate |
|---|---|---|
| **Up** | Timestamped sensor records, each already carrying its agency tag | per-channel |
| **Up** | Joint telemetry for the full-tier log | loop rate |
| **Up** | Deadline-miss and fault notifications | on event |
| **Down** | Motion intent, not motion commands | on event |
| **Down** | Power state requests | on event |
| **Down** | Gating: which channels run at full rate | on event |

**Agency tagging is firmware.** It is a hard real-time stage of the reflex path,
and it needs the commanded value and the measured value in the same place at the
same time
([07.3](../spec/07-firmware-and-software.md#73-what-firmware-must-guarantee), guarantee 7):
once a stream has crossed upward without its tag, the information that would
have carried it has already been averaged away.

**Software sends intent, not commands.** The final command belongs to a hard
real-time task, so it belongs to firmware. Software that could write actuator
values directly could also miss a deadline while holding them, and nothing on the
application processor has a watchdog that bounds it.

## 5. Link loss

The local core is firmware plus the minimum software needed to keep logging. On
link loss it maintains balance, preserves state and log, continues recording at
both tiers, and attempts re-establishment.

**It does not decide.** The boundary is stated at
[07.5](../spec/07-firmware-and-software.md#75-link-loss-and-the-local-core) and
it is architectural: reflexes are loadable, and the interpretation of priorities
in an unforeseen situation is not a reflex.

A practical consequence for this layer: the log must not be trimmed to save
space during an outage. An outage is exactly when the record matters most, and a
body that discards its own unsynchronised history has made the outage
unauditable.

## 6. Open

| `⟦IMPL⟧` | Depends on |
|---|---|
| Joint current loop rate | Actuator and driver |
| Permitted inter-channel skew | Bus topology |
| Reflex stage split | Measurement on real parts |
| Thermal envelope | Packaging |
| Signing throughput, and therefore batch period | Secure element part |
