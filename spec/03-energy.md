# 03 — Energy

Every trade in this specification is ultimately a division of a kilowatt-hour
budget. This chapter states the budget, the measures that stretch it, and the
ceilings that cannot be stretched.

## 3.1 Source

Solid-state cells, declared in two configurations:

| Configuration | Density | Trade |
|---|---|---|
| **Durable** | **~400–500 Wh/kg** | Good cycle life, good thermal safety — suits a body in human contact. **Recommended as the design target** |
| **Ceiling** | **~700–1100 Wh/kg** (solid-state Li-S) | Maximum endurance. **Cycle-life debt: presently ~100 cycles** — the pack becomes a consumable |

*Sourced, for positioning the three maturity tiers:*

- Commercial Li-ion today: ~250–260 Wh/kg at cell level
- Semi-solid already shipping in vehicles: ~300–350 Wh/kg
- Expected solid-state packs: 300–500+ Wh/kg; demonstrated cells at 600 Wh/kg
- Li-S: ~2600 Wh/kg theoretical; lab results 743 Wh/kg (6 mg/cm² cathode
  loading) to 1100 Wh/kg (18 mg/cm²); record cell 695 Wh/kg but **under 100
  cycles**, against >1000 for Li-ion

**Hot-swap under 2 minutes** — the pack is a replaceable module.

**Peak-burst supercapacitor: optional.** Fitted when the mission needs sudden
high-power motion (catching, jumping, fast reflex); omitted when lightness
matters more. Its role is millisecond-scale discharge without sagging the pack.
See [02.7](02-structure-and-motion.md#27-peak-power-is-limited-by-the-source-not-the-actuators)
for why this option decides more than its name suggests.

## 3.2 Six energy measures

| # | Measure | Mechanism | Effect |
|---|---|---|---|
| 1 | **State-dependent gating** | Actuators tense only when needed; full-rate sensing only on attended channels; edge compute clocks down when still | **Strongest.** Draw varies ~1:8 between idle and peak |
| 2 | **Regeneration on deceleration** | Recover on limb lowering and braking | up to **~30%** *(sourced)* |
| 3 | **Source tiering** | Main pack for motion, supercapacitor for bursts, trickle charge underneath | Each tier does what it is good at |
| 4 | **Mechanical joint locks** | Latch joints when holding a pose; actuators release | Removes the cost of standing still |
| 5 | **Actuator operating point** | Series-elastic elements store and return gait energy | Cuts the static-hold penalty |
| 6 | **Tiered sleep with delegated watch** | See 3.3 | The only measure that attacks **total scheduled energy** |

## 3.3 Tiered sleep

The body drops to quiescent power on a cycle: actuators off with the body resting on
a mechanical support, full-rate sensing off, heavy compute off. A very
low-power always-on wake-up circuit and wake-on-event remain.

**Delegated watch.** While the body sleeps, the **off-board compute of the
controller stays awake**, observing through other sources — environmental
devices, other units, signal networks. The body sleeps **without the system going
blind.** This is an architectural advantage biology does not have, and it is
available only because of the on-board / off-board split of [01](01-architecture.md).

| # | Constraint | Content |
|---|---|---|
| 1 | **Depth against wake latency** | Deeper sleep, slower waking: tens of ms (light) to seconds (deep). Multiple levels are offered; which one is `⟦CTRL⟧` |
| 2 | **Sleep posture is a physical constraint** | Switching actuators fully off requires a passive structure to carry gravity. Deep sleep needs support — it is not available while standing unaided |
| 3 | **Quiescent power is above zero** | The always-on wake-up circuit still draws. Sleep is very long but not indefinite. See 3.6 for what actually bounds it |
| 4 | **It cuts the integral, not the peak** | This measure reduces total energy over a scheduled cycle, not instantaneous power |

## 3.4 Four state levels

| Level | Source | Actuators | Sensing | Character |
|---|---|---|---|---|
| **1. Active** | Battery | Running | Full, under gating | All six measures apply |
| **2. Free sleep** | Battery (floor) | Off, body resting | Always-on wake-up circuit only | Maximum saving; the off-board compute watches |
| **3. Rest-and-charge** | **External** | Light support | **Spatial sensing retained** | **Resting without going blind, charging without going dead** |
| **4. Deep sleep on dock** | External | Off | Minimal | Fast full charge plus maximum rest; suits standby units |

> **Level 3 is the state characteristic of this architecture.** On external
> power, the constraint "switch things off to save the battery" disappears —
> nothing is drawing from the pack. The body recovers energy *while maintaining
> observational presence*. Organisms cannot do this.
>
> Even where power is free, the dock should still carry most of the body's
> weight — not for the electricity, but for **heat** (actuators holding a pose
> get hot) and **mechanical wear**.

## 3.5 Dock

| Form | Role | Gravity path | Trade |
|---|---|---|---|
| **Seat or couch** *(default)* | Active unit resting and charging | Supported from below, in compression | Low centre of mass, natural posture, good sightlines, fast to rise |
| **Load-bearing hanger** | Standby unit in storage | Suspended from above, in tension | Less floor area, more units stored; smaller charging contact, poorer sightlines |

Both charging methods are provided:

- **Wireless** — slow or maintenance charging across long rests. Convenient, no
  connector wear. *Limits: lower efficiency than contacts, and heat at the
  interface at high power.*
- **Wired contacts** — fast charging when turnaround matters.

Which method is used when: `⟦CTRL⟧`.

## 3.6 Quiescent power and the sleep ceiling

Components of quiescent power:

| Component | Power | Note |
|---|---|---|
| Sub-GHz wake-up receiver | **3–30 µW** | *Sourced* — published designs from 305 nW to ~6 µW; Wi-Fi-based variants ~30 mW |
| RAM retention and the root-of-trust monotonic clock | ~10–50 µW | `⟦IMPL⟧` |
| Low-power beacon ([06.5](06-audit-surface.md#65-low-power-beacon)) | **< 1 mW** | |
| Spatial sensing, passive mode | **~18 µW** | *Sourced* |
| Spatial sensing, full CSI, duty-cycled | **~50–200 mW** | `⟦IMPL⟧` — the expensive term |

**But the always-on wake-up circuit is not the dominant term.** Cell self-discharge runs
**1–3% per month** *(sourced; automotive standards require under 2%/month, and
solid-state is expected to be lower but has yet to demonstrate it)*. On the
10.4 kWh pack of the 4-hour reference body
([02.7](02-structure-and-motion.md#27-peak-power-is-limited-by-the-source-not-the-actuators)):

| Self-discharge | Equivalent power |
|---|---|
| 1%/month | **144 mW** |
| 2%/month | **289 mW** |
| 3%/month | **433 mW** |

A deep-sleeping always-on wake-up circuit costs **tens of µW** — about **four orders of
magnitude below self-discharge**.

Sleep duration at 2%/month, linear approximation:

| Mode | Total floor | Duration |
|---|---|---|
| Deep — wake-up receiver and retention only | ~290 mW *(over 99% of it self-discharge)* | **~4.1 years** |
| Plus passive spatial sensing | ~307 mW | ~3.9 years |
| Plus full-CSI spatial sensing | ~490 mW | **~2.4 years** |

> **Deep-sleep duration does not depend on pack size.** Energy and drain scale
> together, so a 4 kWh pack and a 20 kWh pack both reach ~4.1 years at 2%/month.
> A larger pack buys sleep duration only once there is a **fixed** load beside
> self-discharge: with full-CSI sensing running, 4 kWh gives ~1.5 years where
> 10.4 kWh gives ~2.4.

> **Two design consequences.**
>
> **(1)** Optimising the always-on wake-up circuit below ~10 mW is wasted effort — it
> disappears beneath self-discharge. The only term worth optimising is full-rate
> spatial sensing, because it alone is the same order as the chemistry.
>
> **(2)** What bounds sleep is **not the standby electronics — it is the cell
> chemistry.** A deep-sleeping body runs its pack down in a few years even if
> the always-on wake-up circuit drew nothing at all.
>
> The bound disappears at levels 3 and 4, where the dock both carries the body
> and offsets self-discharge.

## 3.7 Environmental harvesting — add-on

Peak solar irradiance is ~1000 W/m². The effective collecting area of a ~1.75 m
body is ~0.5–0.7 m²; good cell efficiency is 20–25% — giving a maximum harvest
of **~100–175 W**.

Against that, a humanoid in motion draws **hundreds to over 1000 W**. Solar
**extends standby; it does not run a working body.** It counts toward waiting
time and toward charging at rest, never toward the operating budget.

## 3.8 Hard constraints

**No configuration yields unlimited energy in free-running mode.** This is
battery physics and it is not negotiable — it is only widened by the six
measures and by charging infrastructure.

"Unlimited" is reached only at levels 3 and 4, on external power, where the
ceiling is the external supply rather than the pack.

This is the honest substitute for an inexhaustible source: **not an infinite
supply, but a finite budget plus an infrastructure that makes it sufficient.**

**Operating endurance: `⟦CTRL⟧`.** No figure is set here. The designer supplies
the range and the trade; the controller picks the point — a large pack for long
outings, a light one for short work, more or less sleep as context demands —
within the ceiling derived in [02.3](02-structure-and-motion.md#23-the-endurance-ceiling).
