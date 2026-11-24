# 09 — Open constants

Every value this specification cannot yet derive is left marked rather than filled with a guess. A specification that invents its own constants trades honesty for the appearance of completeness.

Two kinds of blank, and they are not the same:

- `⟦CTRL⟧` — **not ours to fill.** A decision belonging to whoever operates the body. Filling it here would be the body overruling its operator.
- `⟦IMPL⟧` — **not yet derivable.** A value that depends on choices not made, or on measurements not taken.

## ⟦CTRL⟧ — operator decisions

| Value | Where | Bounded by |
|---|---|---|
| Operating endurance | [03.8](03-energy.md#38-hard-constraints) | The ceiling `t_max` in [02.3](02-structure-and-motion.md#23-the-endurance-ceiling) |
| Protection level and coverage | [02.4](02-structure-and-motion.md#24-protection) | The mass loop; each kilogram costs `γ` kg |
| Supercapacitor fitted or not | [03.1](03-energy.md#31-source) | Determines whether peak power is actuator-limited or source-limited |
| Sleep depth and schedule | [03.3](03-energy.md#33-tiered-sleep) | Depth against wake latency |
| Charging method and timing | [03.5](03-energy.md#35-dock) | — |
| Compute split, body against external | [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) | Two hard ends; the middle is adjustable |
| Use made of spatial RF sensing | [01](01-architecture.md), [05.3](05-sensing.md#53-channels) | Capability retained in full at the hardware level |
| Log signing period, synchronisation frequency, flag tolerances | [06.7](06-audit-surface.md#67-hard-constraints) | — |
| Acceptable state loss when a body is lost | [01](01-architecture.md) | — |

## ⟦IMPL⟧ — not yet derivable

| Value | Where | Why not filled |
|---|---|---|
| `f_str`, `f_act` — structural and actuator mass fractions | [02.2](02-structure-and-motion.md#22-the-four-coefficients) | Depend on material and gearing choices not yet made. Ranges are narrow enough that no conclusion changes sign |
| Fixed non-scaling mass (compute, sensors, hands, shell, harness) | [02.5](02-structure-and-motion.md#25-mass-envelope) | Depends on component selection |
| Ventilation: the fans, their power and noise, the filter media and their replacement interval, duct areas, the flow of each zone, protection against water | [04.8](04-shell.md#48-ventilation-and-surface-temperature) | A thermal network at 35 °C (plan M-11), bought fans and filters; noise and water for discussion (2026-11-24) |
| Areal density of the foam padding and the tactile skin | [04.5](04-shell.md#45-the-three-layer-division) | The foam's thickness waits for plan M-8; the fall protectors are read, 1.10 kg as a set (2026-11-23); the skin's vendor states no mass. The textile's is read (0.20 kg/m²); the armour shell's is held at 7.5 kg/m², against 7.22 for the hybrid as data sheets give it |
| Fire: the temperature reaching the armour shell's face through the textile, against its UHMWPE's ≤ 70 °C | [04.4](04-shell.md#44-fire-resistance) | The textile's data sheet gives no heat-transfer figure; the armour shell has no fire standard of its own (2026-11-22). Fires as a mission, and NFPA 1970, are on the upgrade path with group 3 since 2026-11-24 ([04.7](04-shell.md#civil-rescue-in-fires-and-water)) |
| RAM retention and root-of-trust clock power | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | Depends on the parts chosen. Immaterial against self-discharge |
| Full-CSI spatial sensing power | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | The one floor term that matters; depends on implementation |
| Merkle batch period for log signing | [06.4](06-audit-surface.md#64-audit-log) | Trades trace granularity against signing load |
| Durable-tier cycle life, discharge rate and pack abuse test | [03.1](03-energy.md#31-source) | Set when the cell is chosen (plan D-5). The density, `e`, is the one figure the mass loop needs, and it is established |
| What must survive the pack's removal in service | [03.1](03-energy.md#31-source) | The always-on rail sits in the power assembly as the bill of materials stands; depends on the power architecture (plan E-2, E-4) |
| Heartbeat threshold that triggers the OBC | [07.5](07-firmware-and-software.md#75-link-loss-and-the-obc) | Depends on the link and on how long the Real-time Control Layer can hold without new setpoints |
| Motion envelope: walking's cadence and step-length ranges, the rest after running, the durations of stairs and held postures, the disturbance on stairs, fall height | [02.6](02-structure-and-motion.md#motion-envelope) | Wait for sources, simulation and the modules' thermal data (plan D-2). Which motions are declared is the author's choice, row by row; running and balance recovery were declared on 2026-11-22, walking's top speed, 1.0 m/s, on 2026-11-23, its sustained speed, 0.5 m/s, and 10 min at the top on 2026-11-24, and what a fall must protect, provisionally, the same day (spec 04.1) |
| Exact self-discharge rate | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | Depends on the chemistry chosen. **The order of magnitude and the dominant term are established**, which is what the sleep ceiling needs |

## What is deliberately *not* here

Some things are absent because they belong to no one in this repository:

| Absent | Whose |
|---|---|
| Any specification of the controller | Not this repository |
| The standard judging a body's conduct | A third party: the deploying or certifying party |
| Conformance test procedures | [`protocol/`](../protocol/) — v0.1 draft |

## Reading this chapter

A blank here is not an oversight and not a placeholder waiting for a plausible number. Where the specification could establish the *shape* of a constraint without its exact value, it did so and said which is which — the sleep ceiling in [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) is the clearest example: the precise self-discharge figure is open, but knowing *which term dominates* was enough to close the question that mattered.
