# 02 — Structure and motion

Structure, actuation and energy are one coupled loop. They cannot be specified separately, and cutting the loop anywhere leaves the other ends meaningless.

> Every figure in this chapter is reproducible: `python3 scripts/gems_budget.py --check` recomputes them and confirms each one still appears here. See [`scripts/`](../scripts/).

## 2.1 The mass loop

Body mass divides into two kinds:

- **Scaling mass** — structure, actuators, battery. The heavier the body, the more of each it needs, because they exist to carry and move that very mass.
- **Non-scaling mass** — armour, compute, sensors, hands, shell, harness. These are placed on the body from outside; their size is set by the mission, not by the body's mass.

With `m` the total mass and `m_ext` the non-scaling part:

```
m  =  f_str·m  +  f_act·m  +  f_bat·m  +  m_ext

     f_bat = p·t / e
     p = specific power in motion (W/kg)
     t = required free-running endurance (hours)
     e = battery energy density (Wh/kg)
```

Solving:

```
m  =  m_ext / (1 − Σf)      where  Σf = f_str + f_act + p·t/e
γ  =  1 / (1 − Σf)          — the growth factor
```

**Convergence condition: `Σf < 1`.**

This is a structural statement, not a design point. If the three scaling terms sum to the whole body, nothing is left for armour, sensors or hands — and **no mass satisfies the system, at any price**. Such a design is not heavy; it does not exist.

`γ` reads directly as **the mass price of each kilogram of function**: adding 1 kg of armour costs not 1 kg but `γ` kg of body.

## 2.2 The four coefficients

| Coefficient | Range | Status |
|---|---|---|
| `f_str` — structure | ~0.25–0.35 | `⟦IMPL⟧` — material and safety factor |
| `f_act` — actuators | ~0.25–0.35 | Derived, not assumed: the summed joint torque of the declared kinematics divided by actuator torque density, in two parts — see below and [2.6](#26-actuation-and-manipulation) |
| `p` — specific power | **~10–25 W/kg** in motion | *Sourced* — commercial humanoids draw 300–1500 W walking; a 2.3 kWh pack supporting ~2 h of dynamic work implies ~1.1 kW continuous. Armoured bodies sit in the upper half |
| `e` — battery density | **450** (durable) / **900** (ceiling) Wh/kg | [03](03-energy.md) |

`f_str` is left open because it depends on material choices not yet made; its range is narrow enough that no conclusion below changes sign.

`f_act` is **no longer an assumption**. It follows from the declared joint count and the declared torque density, and 2.6 shows the derivation. It is listed as a coefficient because the loop consumes it as one, not because it is free.

**It has two parts, and the loop treats them differently.** Leg and trunk torque scales with body mass, so their actuators are a true fraction of the body: `f_act_s` = **0.226** at 80 Nm/kg, and this is the part that enters `Σf`. Arm, wrist and neck torque is fixed by payload and geometry, not by body mass, so their actuators are non-scaling mass — **9.2 kg** at 80 Nm/kg — and enter `m_ext` beside armour and sensors, where `γ` multiplies them. The `f_act` of the table is the sum of both over the body, 0.32 at the 2-hour point. Treating the whole of it as scaling, as this section did before 2026-09-26, overstated `γ` and made a lighter body look worse than it is.

## 2.3 The endurance ceiling

Setting `Σf = 1` and solving for `t`:

```
t_max  =  (1 − f_str − f_act) · e / p
```

Here `f_act` is the scaling part of 2.2, `f_act_s` = 0.226 at 80 Nm/kg; the fixed part sits in `m_ext` and does not bound `t`. At `f_str` = 0.30:

| | `p`=10 | `p`=15 | `p`=20 | `p`=25 W/kg |
|---|---|---|---|---|
| **e = 450** Wh/kg | 21.3 h | 14.2 h | **10.7 h** | 8.5 h |
| **e = 900** Wh/kg | 42.6 h | 28.4 h | **21.3 h** | 17.1 h |

And `γ` inflates sharply on approach (`e`=450):

| `p` \ `t` | 2 h | 4 h | 6 h | 8 h | 10 h |
|---|---|---|---|---|---|
| 10 W/kg | 2.3 | 2.6 | 2.9 | 3.4 | 4.0 |
| 15 W/kg | 2.5 | 2.9 | 3.7 | 4.8 | 7.1 |
| **20 W/kg** | 2.6 | 3.4 | 4.8 | **8.5** | 34.0 |
| 25 W/kg | 2.8 | 4.0 | 7.1 | 34.0 | *diverges* |

> **Read this correctly.** It does not say the body runs for 10 hours. It says that at `p`=20 W/kg on a durable-grade pack, **no free-running body beyond 10.7 hours exists** — and that from about 8 hours the price is already meaningless, since γ=8.5 means each kilogram of armour costs 8.5 kg of body.
>
> Endurance remains `⟦CTRL⟧`. What this ceiling adds is a bound the controller cannot choose past, because on the far side there is no expensive design — there is no design.

## 2.4 Protection

The group 5 standard is one material level covering handgun rounds, knives and everyday impact together. Bullets and blades defeat armour by different mechanisms — a blade tip passes between soft fibres where a bullet does not — so a single body facing both needs a multi-layer package.

| Layer | Areal density | Note |
|---|---|---|
| Ballistic, NIJ HG2, formerly IIIA (soft UHMWPE/aramid) | **3.8–5.6 kg/m²** | lightest ~3.76; typical ~4.9; aramid hybrid ~5.6 |
| Stab, NIJ 0115.00 spike level 1 | **1.42 kg/m²** standalone | a bought soft aramid panel; ~3.2 kg/m² until 2026-11-22, from no traceable source ([mechanical §3](../hardware/mechanical/README.md#3-protection)) |
| **Integrated multi-threat package** | **~6–9 kg/m²** | cheaper than adding two layers, dearer than one |

The reference design moulds the armour as the shell itself, in UHMWPE composite ([04.2](04-shell.md#42-armour-shell)); bought hard polyethylene plates of the handgun level come to 7.2–9.1 kg/m², so the 7.5 kg/m² the loop holds is at the optimistic end.

*Sourced.* Against a skin area of ~1.6 m² for a 1.65 m body (1.8 m² at the 1.75 m declared until 2026-09-26, scaled by the square of height):

| Coverage | Area | @6 kg/m² | @9 kg/m² |
|---|---|---|---|
| 50% — torso and head | 0.80 m² | 4.8 kg | 7.2 kg |
| 65% — plus outer limbs | 1.04 m² | 6.2 kg | 9.4 kg |
| 80% — near full body | 1.28 m² | 7.7 kg | 11.5 kg |

> Armour is non-scaling mass, so it enters `m_ext` and is multiplied by `γ`. At γ=2.6, the reference point, choosing 80% coverage over 50% adds ~3 kg of armour — and **~7 kg of body**. Coverage and level are under discussion (D-8): the reference design keeps 65% until that is settled. This is where the trade bites hardest, and it is `⟦CTRL⟧`.
>
> Rifle-rated protection (NIJ III/IV, rifle levels RF in NIJ 0123.00) is achievable but adds substantially more mass. The anchor level proposed here is handgun plus blade plus everyday impact; anything above is `⟦CTRL⟧`.

## 2.5 Mass envelope

`m = γ · m_ext`, with `m_ext` = armour (5–13 kg) plus fixed mass — compute, sensors, hands, shell (padding, tactile skin, textile; [04.5](04-shell.md#45-the-three-layer-division)), harness: **15–25 kg**, `⟦IMPL⟧` — plus the arm, wrist and neck actuators of 2.2, 9.2 kg at 80 Nm/kg, which do not scale with the body.

| Operating point | γ | Body mass |
|---|---|---|
| **2 h, durable pack — the reference design, with a dock (D-8)** | 2.6 | **76–123 kg** |
| 4 h, durable pack | 3.4 | **99–160 kg** |
| 8 h, ceiling pack | 3.4 | **99–160 kg** |
| 6 h, durable pack | 4.8 | 141–228 kg — *outside the sensible region* |

**Independent cross-check.** A real 1.2 m, 35 kg, 25-DOF humanoid scaled by mass ratio `(1.65/1.2)³ = 2.60` gives **~91 kg** for a 1.65 m body of the same architecture, before armour. That figure lands inside the 76–123 kg band at the 2-hour mark, beside the reference design's 96 kg. Two independent derivations — one from the coupled loop, one from geometric scaling of a machine that exists — agree to an order of magnitude.

## 2.6 Actuation and manipulation

| Property | Envelope | Maturity |
|---|---|---|
| Specific power | **3–5 kW/kg** | **TM** |
| Specific torque | **80–90 Nm/kg peak** — see below | **TM**, at a 16:1 reduction; the same motor at 48:1 is sold at 159 Nm/kg — see below |
| Efficiency | 75–82% | **TM** |
| Response | milliseconds | **TM** |
| Joints | precision bearings with harmonic, cycloidal or planetary reducers ([mechanical §2](../hardware/mechanical/README.md#2-reducers-by-joint-class)) | **TM** |
| Balance | IMU with ZMP control and reaction wheels | **TM** |
| Adhesion | gecko-type dry adhesive, moderate load | **LAB** |

### The basis matters as much as the number

Torque density is quoted on two incompatible bases, differing by a factor of four. **Peak torque over actuator module mass** — motor, gearbox and housing — is what module datasheets give, and what this specification declares. **Total integrated actuator mass**, counting cooling and wiring, yields 18–22 Nm/kg for the state of the art. A figure carried across from one basis to the other will size a body that cannot be built.

**This specification declares peak-over-module, at the reduction ratio of the modules it was derived from — about 16:1, ~100 rpm no-load.** Torque density is not a ceiling of the motor: the same motor sold at 48:1 claims 159 Nm/kg at about half the speed ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)). What the ratio trades is output speed, so a density figure without its ratio, like one without its basis, is a number waiting to be misread. The cost of standing at 80–90 is still real: part availability narrows to a handful of modules, and the joints that need more torque than those modules give must take a higher ratio and lose speed, which the sizing here does not yet check.

### Why 80 is the floor

The declared kinematics need **2475 Nm** summed across 31 joints at the 96 kg reference point ([joint-by-joint sizing](../hardware/electrical/)); 1737 Nm of it scales with body mass and 738 Nm does not. The three trunk axes are sized from measured human trunk strength per kilogram ([electrical §6a](../hardware/electrical/README.md#6a-trunk-lateral-bend-torque--research-2026-09-26)), the arms from the declared payload below ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)). Divide:

| Density | Actuator mass | `f_act` |
|---|---|---|
| 80 Nm/kg | 30.9 kg | **0.32** |
| 85 Nm/kg | 29.1 kg | 0.30 |
| 90 Nm/kg | 27.5 kg | **0.29** |

**The declared band and the `f_act` band of 2.2 are the same constraint seen twice.** 80–90 Nm/kg maps onto `f_act` 0.29–0.32. The arithmetic alone would allow a floor near 74 Nm/kg, where `f_act` touches 0.35; the declared floor was kept at 80 when the arm payload came down on 2026-09-26, as margin — for decision D-1 on the knee, for a dynamic trunk figure above the isometric one, and for the continuous-torque question electrical §6b leaves open. Below the floor the actuators eat the mass budget and the loop stops converging. The two figures cannot drift apart, because each is derivable from the other and `scripts/gems_budget.py --check` holds them together.

### Arm torque

**Declared group 2 capability:** daily manipulation and moderate precision, with **15 kg in one hand, arm straight and horizontal, load at the grip centre** — the posture of maximum gravitational moment. Shoulder roll carries the same posture abducted, at 11 kg. Decided 2026-09-26; the reasoning is at [electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26).

The lever is to the grip centre, not the fingertip: 0.61 m from the shoulder and 0.31 m from the elbow ([`hardware/kinematics.md`](../hardware/kinematics.md#2-reach-and-segment-lengths)). The arm's own weight is added — its joint modules weighed at 80 Nm/kg from their own torque, plus structure and hand allowances that are `⟦IMPL⟧` until CAD exists:

| Joint | Payload | Self-weight | Peak |
|---|---|---|---|
| Shoulder pitch | 90 | 14 | **104 Nm** |
| Shoulder roll | 66 | 14 | **80 Nm** |
| Elbow | 46 | 4 | **50 Nm** |

For the lever alone, `τ = M·g·L`, with the corresponding actuator mass at 80 Nm/kg:

| Load | 0.40 m | 0.55 m | 0.61 m, grip at full reach |
|---|---|---|---|
| 5 kg | 20 Nm (0.25 kg) | 27 Nm (0.34 kg) | 30 Nm (0.37 kg) |
| 15 kg | 59 Nm (0.74 kg) | 81 Nm (1.01 kg) | 90 Nm (1.12 kg) |
| 30 kg | 118 Nm (1.47 kg) | 162 Nm (2.02 kg) | 180 Nm (2.24 kg) |
| 50 kg | 196 Nm (2.45 kg) | 270 Nm (3.37 kg) | 299 Nm (3.74 kg) |

### Load cases

**Decided 2026-09-26: the declared loads are static objects.** Lifting, carrying or dragging a person is outside group 2 — it needs dynamic factors no source gives and a responsibility no paper design can carry. Safe contact with people (group 4 of [01](01-architecture.md#application-frame)) is not a load case and stays core: touching, steadying and walking beside are in; lifting is out.

Each case is a mass, how many hands hold it, the horizontal lever from the shoulder and elbow axes to its centre of mass, and a status. A load held close to the body is carried by the legs and trunk, so its mass is added to every per-kilogram row of theirs — the rule the sizing lacked until this date. Arm self-weight is included. At the 96 kg reference point:

| Case | kg | Shoulder | Elbow | Hip | Trunk pitch | Status |
|---|---|---|---|---|---|---|
| One hand, arm straight and horizontal | 15 | 104 | 50 | 196 | 193 | decided, D-10 |
| Bag hanging from one hand, arm down | 20 | 14 | 4 | 205 | 202 | proposed |
| Object hugged to the chest, two hands | 20 | 44 | 24 | 205 | 202 | proposed |
| Light object to a high shelf, one hand | 5 | 44 | 20 | 179 | 176 | proposed |
| Stairs with a load held close, two hands | 20 | 29 | 14 | 205 | 202 | proposed |

Two things the table says. The arm cases are cheap: the horizontal arm sets the shoulder and nothing else comes near it. The leg cases are where the mass goes: 20 kg held close costs the hip 35 Nm, whatever the hands do. The bag hanging straight down costs the shoulder nothing and is a bearing case — the AKH70-48 output bearing is rated 8680 N static, 18 times that bag.

**Carry capacity** follows: the leg joint with the largest per-kilogram demand (hip pitch and knee, 1.77 Nm/kg) reaches a module's torque at `(body + load) = torque / 1.77`. Against the AKH70-48's 222 Nm peak, the 2-hour body at 96 kg carries **29 kg** in one stand-up or step, while a 4-hour body at 125 kg carries **0 kg** — itself and nothing else. Every kilogram off the body is a kilogram onto the hands, which is why D-8 and the load cases are one decision, and why the reference design moved to 2 hours. At the module's 74 Nm rated torque no body in 2.5 climbs stairs with a load for long; how long its peak may be held is the open question of [electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26). `scripts/gems_budget.py` prints both figures for any point.

**A single joint is not the binding constraint, but the arms are the lever on `f_act`.** The legs and trunk carry 1737 Nm of the 2475 and scale with the body, so they set the absolute torque each module must deliver and the peak power of 2.7, not the fraction. The arms, wrists and neck are the fixed 738 Nm, and the fixed part is what moves `f_act` when the body gets lighter — halving the payload from the 30 kg this table once declared took `f_act` at 80 Nm/kg from 0.34 to 0.30 at the old 130 kg point, and the move to the 96 kg reference point took it to 0.32: a lighter body, and a larger share of it in the arms.

### Motion envelope

**Listed 2026-11-22 (Plone); rows 5 and 7 and the duration column decided the same day, the rest open.** What the body must be able to do, motion by motion. The hardware is sized for the heaviest row, so each motion has a row of its own — declared, open or excluded — and none is out merely because no one wrote it down. Running had no row until this date: the knee's 1.77 Nm/kg was checked against the tasks then declared, and running was outside them by omission, not by decision ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)). How a motion is carried out — which cadence and step length, which recovery strategy — is the controller's choice; a row states what the hardware must let the controller choose.

| # | Motion | Kind | Flight phase | Where | Declared | Duration | What it sizes | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Walking, over a region of cadence and step length | commanded | no | everywhere, under the cap of the space | cadence range, step-length range and top speed (speed = cadence × step length) open; 1.0 m/s proposed as the top speed, not decided | sustained: the operating endurance ([2.3](#23-the-endurance-ceiling)) | Its four corners, each something different: fast cadence with long steps the peak joint speed — the knee's, and with it D-2; slow cadence with long steps torque at deep flexion and balance at the ankle; fast cadence with short steps joint acceleration and loop latency; slow cadence with short steps none of the peaks | listed, figures open |
| 2 | Walking backward and sideways, turning in place | commanded | no | everywhere | speed in each direction, turning rate: open | short | hip roll and yaw, ankle roll | listed, figures open |
| 3 | Stairs and slopes | commanded | no | stairs, ramps | riser height, slope, speed: open | open — sustained when climbing several floors, set by its purpose | knee and hip torque in flexion, covered for stairs by the 1.77 Nm/kg the legs are sized to ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)); held for long, the knee's continuous rating; with a load, the load case above | torque covered; geometry, speed and duration open |
| 4 | Squatting, kneeling, rising from a seat and from the floor | commanded | no | everywhere | squat depth, kneeling posture: open | momentary for rising; open for a squat or a kneel held to work, which holds torque with the joint still — the case that heats a motor most | knee torque at deep flexion, range of motion; held, the stall rating | rising from a seat covered ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)); deep squat, kneeling, the floor and the hold open |
| 5 | Running | commanded | yes | open space only | **up to 2.5 m/s**, to keep pace with a person or leave a hazard | **60 s at 2.5 m/s, then a rest before the next run**; the rest open until the module's thermal data | the knee: 2.79 Nm/kg in stance, 268 Nm at the 96 kg reference point; 10.9 rad/s mean in swing (12.6 the highest runner), at a swing torque of 0.53 Nm/kg or less; 0.96 Nm/kg RMS over the stride, 92 Nm, against the module's continuous rating. The ankle: 2.07 Nm/kg, 199 Nm, against the 134 Nm it is sized to. Landing impact on joints and reducers. Power about 1 kW, which the pack does not limit ([2.7](#27-peak-power-is-limited-by-the-source-not-the-actuators)) — all from [electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22) | decided 2026-11-22: speed, purpose and duration; rest open |
| 5a | Running faster than 2.5 m/s | commanded | yes | open space only | `OPEN` | — | the knee at 3.5 m/s: 3.1 Nm/kg, about 300 Nm, and 12.7 rad/s mean ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)) — no bought module found meets both ([`CLAUDE.md`](../CLAUDE.md) §2) | `OPEN` |
| 6 | Jumping | commanded | yes | open space only | height, distance: open | momentary | peak power, which the battery limits without a supercapacitor ([2.7](#27-peak-power-is-limited-by-the-source-not-the-actuators)); landing impact | listed, figures open |
| 7 | Balance recovery — after a push or a stumble, by a recovery step | reflex | possible | wherever the body is | **a sudden change of the body's velocity of 1.0 m/s forward or backward, or 0.5 m/s sideways, standing or during rows 1 and 2**; stronger goes to row 8; on stairs open. The figure is a robot's training range ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)), not drawn from a study of the disturbances people cause | momentary | the swing speed and torque of a recovery step: in a simulated robot, the backward push from standing asked the knee for 9.4 rad/s, more than walking at 1.0 m/s did, and ran its torque into the limit — 2.5 Nm/kg, 243 Nm at the reference point | decided 2026-11-22, its source a robot's; on stairs open |
| 8 | Controlled fall, when recovery fails | reflex | — | wherever the body is | fall height, what must be protected: open | momentary | the impact padding and the armour shell ([04.1](04-shell.md#41-impact-padding), [2.4](#24-protection)), shock at the joints, and the rise from the floor that follows (row 4) | listed, figures open |
| — | Other demanding motions | — | — | — | — | — | — | open: not yet listed |

**Commanded and reflex are different kinds.** Rows 1–6 are motions the Main Controller chooses: each can be capped, confined to a space and refused. Rows 7 and 8 are not chosen. The body must be able to do them during any commanded row, whenever a disturbance arrives, so they lie over the rest of the table rather than beside it.

**A space sets a cap, not a size.** Near people, on stairs and in open space the controller holds the body below the envelope; the hardware is sized for the whole envelope and the reflex rows.

**A duration is a requirement, and temperature enforces it.** A row's duration is what the body must be able to sustain, and the module is chosen to meet it. What ends a sustained mode in service is the measured temperature of its motors, not a clock: the controller ends it there and records it. Peak torque says what a joint can do once; RMS torque over the motion, against the continuous rating in a sealed body, says for how long ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)).

**What rows 5 and 7 ask of the knee module.** At least 270 Nm peak in stance; at least 11 rad/s at about 50 Nm in swing, 12 with margin; 92 Nm RMS for 60 s. The ankle: about 200 Nm peak. The figure the legs are sized to, 1.77 Nm/kg, is below these, and the mass loop of 2.1 has not yet been run with them (plan D-2).

## 2.7 Peak power is limited by the source, not the actuators

Actuators and pack both scale with the body, so both operating points of 2.5 have to be priced separately:

| Operating point | Body | Actuators accept | Pack | @3C | @5C | @10C |
|---|---|---|---|---|---|---|
| **2 h, durable — reference** | ~96 kg | **93–155 kW** | 3.9 kWh | 12 kW | 19 kW | 38 kW |
| 4 h, durable | ~125 kg | **112–188 kW** | 10.0 kWh | 30 kW | 50 kW | 100 kW |

**The source falls short in every cell — by between 1.1× and 13×.** The actuators' 3–5 kW/kg ceiling is not reachable from the battery at any point on this table, and high-energy-density chemistries generally trade away C-rate, so choosing the ceiling-grade pack widens the gap rather than closing it.

Only the most favourable corner — the larger pack at 10C against the low end of the actuator band — comes close, at 1.1×. Everywhere else the margin is wide.

> Supercapacitors are listed as an option in [03](03-energy.md). These figures say it more precisely: **without them, the body's peak power is set by the battery, not by the actuators**, and every claim about fast reflex, catching and jumping falls in the source-limited region. A supercapacitor does not change total energy; it changes instantaneous power available. Fitting one remains `⟦CTRL⟧`, but the trade is now quantified.

## 2.8 Hard constraints

Three axes draw on one budget and **cannot all be maximised**:

| Axis | Increasing it |
|---|---|
| **Protection** (coverage × level) | raises `m_ext`, multiplied by `γ` |
| **Free-running endurance** | raises `f_bat` → `γ` inflates non-linearly → divergence at `t_max` |
| **Stature** (height) | mass by the cube, armour area by the square |

**Choose two; pay on the third.** A body is not free to weigh whatever it likes: the coupled loop converges only in a narrow region, and the energy measures of [03](03-energy.md) are what widen that region, by lowering effective `p`.

**Operating point: `⟦CTRL⟧`.**
