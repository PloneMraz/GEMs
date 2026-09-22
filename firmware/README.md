# Firmware

Device-level and real-time code on the body. What [spec
07](../spec/07-firmware-and-software.md) calls the layer that owns *time*: if
missing a deadline breaks the body rather than degrading an answer, it belongs
here.

| Document | Contents | Status |
|---|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Modules, ownership of each deadline, the reflex budget split across stages, and the firmware/software interface | ✅ |
| Source | — | 🔜 *waiting a target* |

## Why there is no source yet

Firmware is written against a processor, a bus and a set of drivers. None of
those are chosen — `mechanical/` and `electrical/` do not exist yet, and the
specification's
`⟦IMPL⟧` constants that firmware would encode (joint current loop rate, permitted
timestamp skew, thermal envelope) depend on parts not selected.

Source written before that would be inventing the target, which is the one thing
this repository does not do. What *can* be written without a target is the
architecture: which module owns which deadline, how the 10 ms reflex budget is
divided, and what crosses the line into software. That is
[`ARCHITECTURE.md`](ARCHITECTURE.md).

## What must be decided before source

| Decision | Blocks |
|---|---|
| Processor and RTOS, or bare metal | Everything |
| Bus topology and bandwidth | Timestamp skew budget, loop rates |
| Actuator driver interface | Current loop, joint telemetry format |
| Secure element part | Attestation agent, signing throughput |
| Low-power radio part | Trace emitter duty cycle |

Each of these is an `⟦IMPL⟧` in [spec
09](../spec/09-open-constants.md) — open because it depends on choices not yet
made, not because it was overlooked.
