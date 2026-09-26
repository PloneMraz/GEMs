# Real-time configuration

The timing policy of the body, kept apart from the code that follows it: which
tasks exist, which layer each runs in, at what rate, by what deadline, and what
happens if it is late.

| File | Contents |
|---|---|
| [`tasks.csv`](tasks.csv) | One row per task or pipeline stage: layer, processor, rate, deadline, stage budget, deadline class |
| [`check_timing.py`](check_timing.py) | Holds the table to the specification and to the firmware architecture |

```bash
python realtime/check_timing.py
```

## Two axes, never merged

| Axis | Question | Values | Column |
|---|---|---|---|
| **Layer** | What is it, and where does it run? | `FIRMWARE`, `SOFTWARE` — hardware is the physical design under `hardware/` | `layer` |
| **Deadline class** | What happens if it is late? | `DEADLINE_HARD` — a failure, may cause harm; `DEADLINE_FIRM` — the result is discarded; `DEADLINE_SOFT` — the result is degraded; `DEADLINE_NONE` | `deadline_class` |

Definitions and sources are in the [glossary](../spec/glossary.md). The class
names carry the `DEADLINE_` prefix so that "hard", "firm" and "soft" can never
be read as hardware, firmware and software.

The one rule that joins the axes, from
[spec 07.1](../spec/07-firmware-and-software.md#71-the-division): **every
`DEADLINE_HARD` task is `FIRMWARE`**.

## What the check enforces

1. Every `DEADLINE_HARD` task is `FIRMWARE`.
2. A periodic task's deadline equals its period, and a pipeline's stage budgets
   add up to its deadline, margin included.
3. Spec 07.2's loops, rates and classes, and the reflex and balance budgets in
   [`firmware/ARCHITECTURE.md`](../firmware/ARCHITECTURE.md) §2 and §3, are the
   figures in the table.

## What is not here yet

Only the tasks the specification classifies are listed. The power-state machine,
attestation agent, beacon and log synchronisation's upstream writer have
deadlines the specification has not yet classed; they join the table when it
does, rather than being classed here by guess. Scheduling policy for a specific
RTOS — priorities, stacks, cores — waits for the processor (plan D-3, F-0).
