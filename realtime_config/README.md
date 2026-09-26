# Real-time configuration

The timing policy of the body, kept apart from the code that follows it and
independent of where that code lives: which tasks exist, how late each may be,
and how its deadline is met.

| File | Tier | Contents |
|---|---|---|
| [`tasks.csv`](tasks.csv) | **Requirement** — set by the specification | Every task and pipeline stage: layer, processor, rate, deadline, stage budget, deadline class |
| [`scheduler.csv`](scheduler.csv) | **How it is met** — set by the hardware | Every top-level task: platform, scheduling policy, priority, `SCHED_DEADLINE` parameters, how the worst-case latency is bounded, and the evidence |
| [`check_timing.py`](check_timing.py) | — | Holds both to the specification and to the firmware architecture |

```bash
python realtime_config/check_timing.py
```

## Two axes, never merged

| Axis | Question | Values | Where |
|---|---|---|---|
| **Layer** | Where does the code run? | `FIRMWARE` — directly on a microcontroller, bare metal or RTOS; `SOFTWARE` — under an operating system; `IMPL` — the real-time controller, until decision D-3 | `tasks.csv`, `layer` |
| **Deadline class** | What happens if it is late? | `DEADLINE_HARD` — a failure, may cause harm; `DEADLINE_FIRM` — the result is discarded; `DEADLINE_SOFT` — the result is degraded; `DEADLINE_NONE` | `tasks.csv`, `deadline_class` |

Definitions and sources are in the [glossary](../spec/glossary.md). The class
names carry the `DEADLINE_` prefix so that "hard", "firm" and "soft" can never be
read as hardware, firmware and software.

## The rule, from spec 07.1

**Every `DEADLINE_HARD` task runs on a platform whose worst-case latency is
bounded.** The rule constrains the platform, not the layer:

| `platform` | Scheduling | `bound_basis` |
|---|---|---|
| `MCU_BARE_METAL`, `MCU_RTOS` | `ISR`, `RTOS_FIXED_PRIORITY` | `CONSTRUCTION` — schedulability analysis of the task set |
| `LINUX_RT` — PREEMPT_RT, isolated cores | `SCHED_FIFO` with a priority, or `SCHED_DEADLINE` with runtime ≤ deadline ≤ period | `MEASUREMENT` — latency under worst-case load, with the report named in `evidence` |
| `LINUX` — no real-time kernel | `SCHED_OTHER` | `NONE` — may carry firm, soft and non-real-time tasks only |

`SCHED_DEADLINE` meets its deadlines only while total utilisation stays within
the cores available ([kernel documentation](https://docs.kernel.org/scheduler/sched-deadline.html)),
so evidence for it must include the utilisation budget.

## What the check enforces

1. The rule above, for every `DEADLINE_HARD` task.
2. Layer and platform agree: `FIRMWARE` on a microcontroller, `SOFTWARE` under
   Linux; Linux policies only on Linux, microcontroller policies only on a
   microcontroller.
3. A periodic task's deadline equals its period; a pipeline's stage budgets add
   up to its deadline, margin included; `SCHED_DEADLINE` parameters are ordered.
4. Spec 07.2's loops, rates and classes, and the reflex and balance budgets in
   [`firmware/ARCHITECTURE.md`](../firmware/ARCHITECTURE.md) §2 and §3, are the
   figures in `tasks.csv`.

It prints which hard real-time tasks still have no established bound. Today that
is all five: the joint drive boards wait for the drive electronics (D-2), and the
real-time controller for its platform (D-3). The specification sets the
requirement; no platform, policy or priority is filled in before the hardware
that would justify it.

## What is not here yet

Only the tasks the specification classifies are listed. The power-state machine,
attestation agent, beacon and log writer have deadlines the specification has
not yet classed; they join the table when it does, rather than being classed
here by guess.
