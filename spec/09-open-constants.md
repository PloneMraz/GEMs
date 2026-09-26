# 09 — Open constants

Every value this specification cannot yet derive is left marked rather than
filled with a guess. A specification that invents its own constants trades
honesty for the appearance of completeness.

Two kinds of blank, and they are not the same:

- `⟦CTRL⟧` — **not ours to fill.** A decision belonging to whoever operates the
  body. Filling it here would be the body overruling its operator.
- `⟦IMPL⟧` — **not yet derivable.** A value that depends on choices not made, or
  on measurements not taken.

## ⟦CTRL⟧ — operator decisions

| Value | Where | Bounded by |
|---|---|---|
| Operating endurance | [03.8](03-energy.md#38-hard-constraints) | The ceiling `t_max` in [02.3](02-structure-and-motion.md#23-the-endurance-ceiling) |
| Protection level and coverage | [02.4](02-structure-and-motion.md#24-protection) | The mass loop; each kilogram costs `γ` kg |
| Supercapacitor fitted or not | [03.1](03-energy.md#31-source) | Determines whether peak power is actuator-limited or source-limited |
| Sleep depth and schedule | [03.3](03-energy.md#33-tiered-sleep) | Depth against wake latency |
| Charging method and timing | [03.5](03-energy.md#35-dock) | — |
| Area allocated to each shell layer | [04.5](04-shell.md#45-the-three-layer-division) | The same `m_ext` budget as armour |
| Compute split, body against external | [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) | Two hard ends; the middle is adjustable |
| Use made of spatial RF sensing | [01](01-architecture.md), [05.3](05-sensing.md#53-channels) | Capability retained in full at the hardware level |
| Log signing period, synchronisation frequency, flag tolerances | [06.7](06-audit-surface.md#67-hard-constraints) | — |
| Acceptable state loss when a body is lost | [01](01-architecture.md) | — |

## ⟦IMPL⟧ — not yet derivable

| Value | Where | Why not filled |
|---|---|---|
| `f_str`, `f_act` — structural and actuator mass fractions | [02.2](02-structure-and-motion.md#22-the-four-coefficients) | Depend on material and gearing choices not yet made. Ranges are narrow enough that no conclusion changes sign |
| Fixed non-scaling mass (compute, sensors, hands, skin, harness) | [02.5](02-structure-and-motion.md#25-mass-envelope) | Depends on component selection |
| Areal density of the sense-and-heal and variable-stiffness layers | [04.5](04-shell.md#45-the-three-layer-division) | No reliable published figure found. The constraint is firm even though the number is not |
| Fire layer temperature and duration | [04.4](04-shell.md#44-fire-resistance) | Must anchor to an existing firefighting-garment standard, not be derived here |
| RAM retention and root-of-trust clock power | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | Depends on the parts chosen. Immaterial against self-discharge |
| Full-CSI spatial sensing power | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | The one floor term that matters; depends on implementation |
| Merkle batch period for log signing | [06.4](06-audit-surface.md#64-audit-log) | Trades trace granularity against signing load |
| Exact self-discharge rate | [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) | Depends on the chemistry chosen. **The order of magnitude and the dominant term are established**, which is what the sleep ceiling needs |

## What is deliberately *not* here

Some things are absent because they belong to no one in this repository:

| Absent | Whose |
|---|---|
| Any specification of the controller | Not this repository |
| The standard judging a body's conduct | A third party: the deploying or certifying party |
| Conformance test procedures | [`protocol/`](../protocol/) — v0.1 draft |

## Reading this chapter

A blank here is not an oversight and not a placeholder waiting for a plausible
number. Where the specification could establish the *shape* of a constraint
without its exact value, it did so and said which is which — the sleep ceiling
in [03.6](03-energy.md#36-quiescent-power-and-the-sleep-ceiling) is the clearest
example: the precise self-discharge figure is open, but knowing *which term
dominates* was enough to close the question that mattered.
