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
| `f_act` — actuators | ~0.25–0.36 | Derived, not assumed: the mass of the module bought for each joint of the declared kinematics, in two parts — see below and [2.6](#26-actuation-and-manipulation) |
| `p` — specific power | **~10–25 W/kg** in motion | *Sourced* — commercial humanoids draw 300–1500 W walking; a 2.3 kWh pack supporting ~2 h of dynamic work implies ~1.1 kW continuous. Armoured bodies sit in the upper half |
| `e` — battery density | **450** (durable) / **900** (ceiling) Wh/kg | [03](03-energy.md) |

`f_str` is left open because it depends on material choices not yet made; its range is narrow enough that no conclusion below changes sign.

`f_act` is **no longer an assumption**. It follows from the declared joint count and the module bought for each joint — since 2026-11-23; a declared torque density before — and 2.6 shows the derivation. It is listed as a coefficient because the loop consumes it as one, not because it is free. Its band was ~0.25–0.35 until 2026-11-24, carried from the working draft with no source; the modules that hold a static load ([2.6](#static-holds)) took the derived figure to 0.351, and the author raised the band's top to 0.36. The band is a bound this design set itself; what must hold is `Σf < 1`, 0.62 at the reference point.

**It has two parts, and the loop treats them differently.** Leg and trunk torque scales with body mass, so their actuators are a true fraction of the body: `f_act_s` = **0.232** at the reference point — 24.8 kg of bought leg and trunk modules on a 107.0 kg body — and this is the part that enters `Σf`. Arm, wrist and neck torque is fixed by payload and geometry, not by body mass, so their actuators are non-scaling mass — **12.8 kg** of bought modules — and enter `m_ext` beside armour and sensors, where `γ` multiplies them. The `f_act` of the table is the sum of both over the body, 0.35 at the 2-hour point. Modules come in steps, so the leg and trunk modules are a fixed fraction of the body only while the set of modules stays the same — up to 108.8 kg for the set of 2.6 — and the loop's treatment of them as a fraction is a first approximation away from the reference point. Treating the whole of it as scaling, as this section did before 2026-09-26, overstated `γ` and made a lighter body look worse than it is.

## 2.3 The endurance ceiling

Setting `Σf = 1` and solving for `t`:

```
t_max  =  (1 − f_str − f_act) · e / p
```

Here `f_act` is the scaling part of 2.2, `f_act_s` = 0.232 for the bought modules; the fixed part sits in `m_ext` and does not bound `t`. At `f_str` = 0.30:

| | `p`=10 | `p`=15 | `p`=20 | `p`=25 W/kg |
|---|---|---|---|---|
| **e = 450** Wh/kg | 21.1 h | 14.0 h | **10.5 h** | 8.4 h |
| **e = 900** Wh/kg | 42.1 h | 28.1 h | **21.1 h** | 16.9 h |

And `γ` inflates sharply on approach (`e`=450):

| `p` \ `t` | 2 h | 4 h | 6 h | 8 h | 10 h |
|---|---|---|---|---|---|
| 10 W/kg | 2.4 | 2.6 | 3.0 | 3.4 | 4.1 |
| 15 W/kg | 2.5 | 3.0 | 3.7 | 5.0 | 7.4 |
| **20 W/kg** | 2.6 | 3.4 | 5.0 | 8.9 | **41.9** |
| 25 W/kg | 2.8 | 4.1 | 7.4 | 41.9 | *diverges* |

> **Read this correctly.** It does not say the body runs for 10 hours. It says that at `p`=20 W/kg on a durable-grade pack, **no free-running body beyond 10.5 hours exists** — and that from about 8 hours the price is already steep, since γ=8.9 means each kilogram of armour costs 8.9 kg of body, and at 10 hours γ=41.9.
>
> Endurance remains `⟦CTRL⟧`. What this ceiling adds is a bound the controller cannot choose past, because on the far side there is no expensive design — there is no design.

## 2.4 Protection

The group 5 standard is one material level covering handgun rounds, knives and everyday impact together. Bullets and blades defeat armour by different mechanisms — a blade tip passes between soft fibres where a bullet does not — so a single body facing both needs a multi-layer package.

| Layer | Areal density | Note |
|---|---|---|
| Ballistic, NIJ HG2, formerly IIIA (soft UHMWPE/aramid) | **3.8–5.6 kg/m²** | lightest ~3.76; typical ~4.9; aramid hybrid ~5.6 |
| Stab, NIJ 0115.00 spike level 1 | **1.42 kg/m²** standalone | a bought soft aramid panel; ~3.2 kg/m² until 2026-11-22, from no traceable source ([mechanical §3](../hardware/mechanical/README.md#3-protection)) |
| **Integrated multi-threat package** | **~6–9 kg/m²** | cheaper than adding two layers, dearer than one |

The reference design moulds the armour as the shell itself ([04.2](04-shell.md#42-armour-shell)): UHMWPE plies for the handgun level, 5.80 kg/m², with aramid spike plies, 1.42 kg/m², co-moulded — 7.22 kg/m² before finish and curvature, against the 7.5 kg/m² the loop holds.

*Sourced.* Against a skin area of ~1.6 m² for a 1.65 m body (1.8 m² at the 1.75 m declared until 2026-09-26, scaled by the square of height):

| Coverage | Area | @6 kg/m² | @9 kg/m² |
|---|---|---|---|
| 50% — torso and head | 0.80 m² | 4.8 kg | 7.2 kg |
| 65% — plus outer limbs | 1.04 m² | 6.2 kg | 9.4 kg |
| 80% — near full body | 1.28 m² | 7.7 kg | 11.5 kg |

> Armour is non-scaling mass, so it enters `m_ext` and is multiplied by `γ`. At γ=2.6, the reference point, choosing 80% coverage over 50% adds ~3 kg of armour — and **~8 kg of body**. Coverage and level are under discussion (D-8): the reference design keeps 65% until that is settled. This is where the trade bites hardest, and it is `⟦CTRL⟧`.
>
> Rifle-rated protection (NIJ III/IV, rifle levels RF in NIJ 0123.00) is achievable but adds substantially more mass. The anchor level proposed here is handgun plus blade plus everyday impact; anything above is `⟦CTRL⟧`.

## 2.5 Mass envelope

`m = γ · m_ext`, with `m_ext` = armour (5–13 kg) plus fixed mass — compute, sensors, hands, shell (padding, tactile skin, textile; [04.5](04-shell.md#45-the-three-layer-division)), harness: **15–25 kg**, `⟦IMPL⟧` — plus the arm, wrist and neck actuators of 2.2, 12.8 kg of bought modules, which do not scale with the body. The reference point holds the fixed mass at 20 kg. Built up from the EBOM on 2026-11-23, the parts with a figure come to 8.5–12.1 kg of it, the impact protectors of [04.1](04-shell.md#41-impact-padding) and the fans of [04.8](04-shell.md#48-ventilation-and-surface-temperature) among them, while the harness, the foam padding, the tactile skin and the compute's cooling have none, so whether 20 kg is enough is not shown. Across the band, the body is 98–118 kg on bought modules ([BOM](../hardware/bom/README.md#the-fixed-mass-bottom-up-2026-11-23)).

| Operating point | γ | Body mass |
|---|---|---|
| **2 h, durable pack — the reference design, with a dock (D-8)** | 2.6 | **86–134 kg** |
| 4 h, durable pack | 3.4 | **113–175 kg** |
| 8 h, ceiling pack | 3.4 | **113–175 kg** |
| 6 h, durable pack | 5.0 | 163–252 kg — *outside the sensible region* |

**Independent cross-check.** A real 1.2 m, 35 kg, 25-DOF humanoid scaled by mass ratio `(1.65/1.2)³ = 2.60` gives **~91 kg** for a 1.65 m body of the same architecture, before armour. That figure lands inside the 86–134 kg band at the 2-hour mark, below the reference design's 107 kg. Two independent derivations — one from the coupled loop, one from geometric scaling of a machine that exists — agree to an order of magnitude.

## 2.6 Actuation and manipulation

| Property | Envelope | Maturity |
|---|---|---|
| Specific power | **3–5 kW/kg** | **TM** |
| Specific torque | **declared at the joint**: the bought module of each joint, peak over module mass — see below | **TM**: every figure a maker's sheet; none tested here |
| Efficiency | 75–82% | **TM** |
| Response | milliseconds | **TM** |
| Joints | precision bearings with harmonic, cycloidal or planetary reducers ([mechanical §2](../hardware/mechanical/README.md#2-reducers-by-joint-class)) | **TM** |
| Balance | IMU with ZMP control and reaction wheels | **TM** |
| Adhesion | gecko-type dry adhesive, moderate load | **LAB** |

### The basis matters as much as the number

Torque density is quoted on two incompatible bases, differing by a factor of four. **Peak torque over actuator module mass** — motor, gearbox and housing — is what module datasheets give, and what this specification declares. **Total integrated actuator mass**, counting cooling and wiring, yields 18–22 Nm/kg for the state of the art. A figure carried across from one basis to the other will size a body that cannot be built.

**Since 2026-11-23 the specification declares the module at each joint, not a torque density** (D-2). Each joint carries the lightest bought module that passes the rank-1 rule of [electrical §6f](../hardware/electrical/README.md#6f-modules-declared-at-the-joint--d-2-2026-11-23) — its maker's sheet gives the peak torque and how long it is held, a continuous torque, the speed at 48 V, the mass and the size — and that meets its joint at the reference point: the peak torque below, the reducer class of [mechanical §2](../hardware/mechanical/README.md#2-reducers-by-joint-class), the speed running asks of the knee, hip pitch and ankle pitch, and, where a figure exists, the RMS torque of running for 60 s (row 5 of the motion envelope; [electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)) and the RMS torque of walking against the continuous torque, since walking is held ([electrical §6g](../hardware/electrical/README.md#6g-walking-rms-and-the-frontal-plane--d-2-2026-11-23), 2026-11-23) — for the legs, the larger of people's walking and the simulated robot's since 2026-11-24 ([electrical §6j](../hardware/electrical/README.md#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)) — and, at the arms and trunk pitch, the 10 s static lift of [Static holds](#static-holds) below (2026-11-24; [electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)). At the 107.0 kg reference point:

| Joint | Torque | Module | Peak / continuous | Speed at 48 V | Mass |
|---|---|---|---|---|---|
| Hip pitch ×2 | 189 Nm; RMS 60 Nm running, 88 walking | ENCOS EC-A10020-P2-24 | 330 / 100 Nm, 79 Nm for 60 s | 123 rpm | 2.211 kg |
| Hip roll ×2 | 185 Nm; RMS 70 Nm running, 85 walking | ENCOS EC-A10020-P2-24 | 330 / 100 Nm, 79 Nm for 60 s | 123 rpm | 2.211 kg |
| Hip yaw ×2 | 66 Nm; RMS 12 running, 20 walking | ENCOS EC-A4315-P2-36 | 75 / 25 Nm, 28 Nm for 60 s | 117 rpm | 0.485 kg |
| Knee ×2 | 299 Nm; RMS 103 Nm running, 79 walking | ENCOS EC-A13715-P1-12.67 | 320 / 110 Nm, 150 Nm for 60 s | 135 rpm | 2.695 kg |
| Ankle pitch ×2 | 221 Nm; RMS 82 Nm running, 81 walking | MyActuator RMD-X12-P20-320 | 320 / 85 Nm | 125 rpm | 2.40 kg |
| Ankle roll ×2 | 58 Nm; RMS 9 running, 20 walking | ENCOS EC-A4315-P2-36 | 75 / 25 Nm, 28 Nm for 60 s | 117 rpm | 0.485 kg |
| Trunk pitch | 186 Nm; RMS 14 walking; 105 Nm for 10 s | ENCOS EC-A10020-P2-24 | 330 / 100 Nm, 105 Nm for 192 s at stall | 123 rpm | 2.211 kg |
| Trunk roll | 102 Nm; RMS 16 walking | SEmotor SEAF70A16NG02 | 104 / 16 Nm | 175 rpm | 0.80 kg |
| Trunk yaw | 79 Nm; RMS 24 walking | ENCOS EC-A6416-P2-25 | 120 / 40 Nm | 120 rpm | 0.805 kg |
| Shoulder pitch, roll ×2 | 108, 84 Nm; 51 Nm for 10 s | ENCOS EC-A10020-P1-12 | 150 / 50 Nm, 51 Nm for 979 s at stall | 140 rpm | 1.373 kg |
| Shoulder yaw ×2 | 60 Nm, for 10 s | ENCOS EC-A8116-P1-18 | 130 / 40 Nm, 60 Nm for 15 s at stall | 140 rpm | 0.961 kg |
| Elbow ×2 | 51 Nm, for 10 s | ENCOS EC-A8116-P1-18 | 130 / 40 Nm, 51 Nm for 83 s at stall | 140 rpm | 0.961 kg |
| Wrist ×6, neck ×2 | 20, 15 Nm | ENCOS EC-A3814-H14-107 | 60 / 20 Nm | 52 rpm | 0.434 kg |

Peak over module mass is then derived, not declared: **97 Nm/kg for legs and trunk, 59 Nm/kg for arms, wrists and neck**, on 24.8 and 12.8 kg of modules. Both are below the 133 and 80 Nm/kg declared earlier on 2026-11-23, before the modules were picked, because modules come in steps and a joint carries the next one up: shoulder yaw asks 60 Nm of a 130 Nm module, a wrist 20 Nm of 60. Torque density is not a ceiling of the motor either: the same motor sold at 48:1 claims 159 Nm/kg at about half the speed ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)), so a density figure without its ratio, like one without its basis, is a number waiting to be misread. The set holds up to 108.8 kg of body, where trunk roll's 16 Nm continuous meets its walking RMS, with its 104 Nm peak at 109.5 kg. The modules are chosen from their sheets, not tested; the sheets' conditions are a bench's, not those of a body under its shell ([plan M-11](../plan/PLAN.md)). One pick still rests on a peak the sheet holds for 1 s or less: trunk roll's SEmotor, 104 Nm against 16 continuous. Until 2026-11-24 two more did, the elbow's and trunk pitch's, and changed when the static holds were declared ([Static holds](#static-holds)).

### What the two figures give

The declared kinematics need **3162 Nm** summed across 31 joints at the 107.0 kg reference point ([joint-by-joint sizing](../hardware/electrical/)); 2404 Nm of it scales with body mass and 758 Nm does not. The knee and ankle pitch are sized to running at 2.5 m/s since 2026-11-23, 2.79 and 2.07 Nm/kg (row 5 of the motion envelope below); the three trunk axes from measured human trunk strength per kilogram ([electrical §6a](../hardware/electrical/README.md#6a-trunk-lateral-bend-torque--research-2026-09-26)), the arms from the declared payload below ([electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26)). With the arms, wrists and neck on their bought modules, divide the legs and trunk:

| Legs and trunk | Actuator mass | `f_act` |
|---|---|---|
| 80 Nm/kg | 42.9 kg | 0.40 |
| 133 Nm/kg | 30.9 kg | 0.29 |
| 150 Nm/kg | 28.8 kg | 0.27 |
| the bought modules, 97 Nm/kg | 37.6 kg | **0.35** |

**The modules and the `f_act` band of 2.2 are the same constraint seen twice.** At 80 Nm/kg the legs and trunk would put `f_act` at 0.40, outside the band; the bought modules put it at 0.351, inside, near its top of 0.36. The arithmetic alone would allow a leg and trunk density near 94 Nm/kg, where `f_act` touches 0.36; the bought modules give 97. Until 2026-11-23 the densities were declared — a single band of 80–90 Nm/kg for every joint, from the 16:1 modules the sizing began with, then 133 for legs and trunk and 80 for the rest — and the loop weighed each joint as if a module came in every size at that density; with the bought modules the 82.3 kg of that declaration became 98.2 kg ([electrical §6f](../hardware/electrical/README.md#6f-modules-declared-at-the-joint--d-2-2026-11-23)), 105.6 kg when walking's RMS and the hip's frontal plane entered the check ([electrical §6g](../hardware/electrical/README.md#6g-walking-rms-and-the-frontal-plane--d-2-2026-11-23)), and 107.0 kg with the static holds ([electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)). Below the band the actuators eat the mass budget and the loop stops converging. The figures cannot drift apart, because each is derivable from the other and `scripts/gems_budget.py --check` holds them together.

### Arm torque

**Declared group 2 capability:** daily manipulation and moderate precision, with **15 kg in one hand, arm straight and horizontal, load at the grip centre** — the posture of maximum gravitational moment. Shoulder roll carries the same posture abducted, at 11 kg. Decided 2026-09-26; the reasoning is at [electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26).

The lever is to the grip centre, not the fingertip: 0.61 m from the shoulder and 0.31 m from the elbow ([`hardware/kinematics.md`](../hardware/kinematics.md#2-reach-and-segment-lengths)). The arm's own weight is added — its bought joint modules, above, plus structure and hand allowances that are `⟦IMPL⟧` until CAD exists:

| Joint | Payload | Self-weight | Peak |
|---|---|---|---|
| Shoulder pitch | 90 | 19 | **108 Nm** |
| Shoulder roll | 66 | 19 | **84 Nm** |
| Elbow | 46 | 6 | **51 Nm** |

For the lever alone, `τ = M·g·L`, with the corresponding actuator mass at 80 Nm/kg, a single module's density, not the bought arm modules' 58:

| Load | 0.40 m | 0.55 m | 0.61 m, grip at full reach |
|---|---|---|---|
| 5 kg | 20 Nm (0.25 kg) | 27 Nm (0.34 kg) | 30 Nm (0.37 kg) |
| 15 kg | 59 Nm (0.74 kg) | 81 Nm (1.01 kg) | 90 Nm (1.12 kg) |
| 30 kg | 118 Nm (1.47 kg) | 162 Nm (2.02 kg) | 180 Nm (2.24 kg) |
| 50 kg | 196 Nm (2.45 kg) | 270 Nm (3.37 kg) | 299 Nm (3.74 kg) |

### Load cases

**Decided 2026-09-26: the declared loads are static objects.** Lifting, carrying or dragging a person is outside group 2 — it needs dynamic factors no source gives and a responsibility no paper design can carry. Safe contact with people (group 4 of [01](01-architecture.md#application-frame)) is not a load case and stays core: touching, steadying and walking beside are in; lifting is out.

Each case is a mass, how many hands hold it, the horizontal lever from the shoulder and elbow axes to its centre of mass, and a status. A load held close to the body is carried by the legs and trunk, so its mass is added to every per-kilogram row of theirs — the rule the sizing lacked until this date. Arm self-weight is included. At the 107.0 kg reference point:

| Case | kg | Shoulder | Elbow | Hip | Trunk pitch | Status |
|---|---|---|---|---|---|---|
| One hand, arm straight and horizontal | 15 | 108 | 51 | 216 | 212 | decided, D-10 |
| Bag hanging from one hand, arm down | 20 | 19 | 6 | 225 | 221 | proposed |
| Object hugged to the chest, two hands | 20 | 48 | 25 | 225 | 221 | proposed |
| Light object to a high shelf, one hand | 5 | 48 | 21 | 198 | 195 | proposed |
| Stairs with a load held close, two hands | 20 | 33 | 16 | 225 | 221 | proposed |

Two things the table says. The arm cases are cheap: the horizontal arm sets the shoulder and nothing else comes near it. The leg cases are where the mass goes: 20 kg held close costs the hip 35 Nm, whatever the hands do. The bag hanging straight down costs the shoulder nothing and is a bearing case — the shoulder's EC-A10020-P1-12 is rated 2.63 kN axial and radial, 13 times that bag.

**Carry capacity** follows: a stand-up or a step asks hip pitch and knee for 1.77 Nm/kg of body and load — running's 2.79 sizes the knee, not what it lifts — so a module's torque is reached at `(body + load) = torque / 1.77`. Against the bought modules — the lower of the two is the knee's EC-A13715-P1-12.67, 320 Nm peak — the 2-hour body at 107 kg carries **74 kg** in one stand-up or step, and a 4-hour body at 140 kg carries **41 kg** on the same modules; the hands take what the arms are sized for, 15 kg in one. The 4-hour figure is a first approximation: run on bought modules at 4 hours, the loop takes heavier ones at the hip, knee, ankle pitch and trunk, and the body is 133.3 kg ([electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)). Earlier on 2026-11-23 the figure was against the RMD-X12-P20-320's 320 Nm, 98 kg at 82 kg; before that against the AKH70-48's 222 Nm, and the 4-hour body carried nothing. Every kilogram off the body is a kilogram onto the hands, which is why D-8 and the load cases are one decision, and why the reference design moved to 2 hours. At the hip module's 100 Nm continuous torque no body in 2.5 climbs stairs with a load for long; how long its peak may be held is the open question of [electrical §6b](../hardware/electrical/README.md#6b-arm-payload-and-the-two-parts-of-f_act--2026-09-26). `scripts/gems_budget.py` prints both figures for any point.

**A single joint is not the binding constraint, but the arms are the lever on `f_act`.** The legs and trunk carry 2404 Nm of the 3162 and scale with the body, so they set the absolute torque each module must deliver and the peak power of 2.7, not the fraction. The arms, wrists and neck are the fixed 758 Nm, and the fixed part is what moves `f_act` when the body gets lighter — halving the payload from the 30 kg this table once declared took `f_act` at 80 Nm/kg from 0.34 to 0.30 at the old 130 kg point, and the move to the 96 kg reference point took it to 0.32: a lighter body, and a larger share of it in the arms. Declaring the legs and trunk at 133 Nm/kg, with the knee and ankle sized to running, took it to 0.27 at 82 kg; the bought modules, the same day, to 0.33 at 98.2 kg, and walking's RMS with the hip's frontal plane to 0.35 at 105.6 kg (2026-11-23); it is 0.351 at 107.0 kg with the static holds (2026-11-24).

### Static holds

**Decided 2026-11-24 (Plone): a load is held as briefly as possible, at three levels, and the body works low in two postures.** Holding torque with the joint still is the case that heats a motor most, so the controller passes through the hard postures instead of standing in them.

| Level | Posture | Held for |
|---|---|---|
| Pass through | 15 kg in one hand at full reach, arm horizontal (11 kg abducted) | **2 s at most**, then the load is drawn in close to the body |
| Pick up, set down | the load close to the body; the trunk leaning at most 30° with 15 kg in the hands, and lower than that by the knees | **10 s at most** |
| Hold | hugged, carried, standing at work | no declared limit; measured temperature ends it, as any sustained mode. With 20 kg hugged upright the stall tables hold the elbow (25.4 Nm) 8 min or more, shoulder pitch (48 Nm) 19, trunk pitch (59 Nm) 22 |
| Squat to work | both feet flat, the trunk leaning at most 30° with no load, at most 10° with 20 kg hugged | as long as the situation asks and the motors allow; **at least 5 min with no load, 30 s with 20 kg** |
| Kneel to work | **on one knee, always preferred**: the rear knee and toes on the ground, the front foot flat. Both knees only where one is not possible | no declared limit; with a load of up to 20 kg no joint asks more than about 40 Nm |

**The situation sets how long** (Plone, 2026-11-24): the controller chooses the posture by the time it expects to need — a squat for the short, one knee for the long — and measured temperature ends it, early enough that the motors can still stand the body up; that reserve has no figure yet. It rises from one knee with the rear toes pushing until it is up.

The 2 s, 10 s, 5 min and 30 s are design choices with no source. The 10 s is checked at the elbow (51 Nm), shoulder pitch (51 Nm), shoulder yaw (60 Nm) and trunk pitch (105 Nm) against each module's stall table, and it took the EC-A8116-P1-18 to the elbow and shoulder yaw and the EC-A10020-P2-24 to trunk pitch ([electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)). The squat is checked at the knee, hip pitch and trunk pitch; the knee's module does not change. The kneel and the rise are computed, not checked by the script ([electrical §6l](../hardware/electrical/README.md#6l-squatting-and-kneeling--d-2-2026-11-24)): rising from one knee asks the knees about 110 Nm and the front hip 112 with no load, about 137 and 143 with 20 kg, if the rear toes push; without them the front knee asks about 300 of its 320. **Not shown:** the 2 s at full reach, since the shoulder's table ends at 61.5 Nm against 108 and 84; the trunk's figure, which takes the lowest of the three pitch axes and a human's mass fractions; and the hold under the shell, since the tables are a bench's, from 30 °C. No row above is marked sustainable except the elbow's 25 Nm, 0.4 Nm below what 20 kg hugged asks of it.

### Motion envelope

**Listed 2026-11-22 (Plone); rows 5 and 7 and the duration column decided the same day, walking's top speed and row 8's protection, provisionally, on 2026-11-23, walking's sustained speed and its time at the top on 2026-11-24, the rest open.** What the body must be able to do, motion by motion. The hardware is sized for the heaviest row, so each motion has a row of its own — declared, open or excluded — and none is out merely because no one wrote it down. Running had no row until this date: the knee's 1.77 Nm/kg was checked against the tasks then declared, and running was outside them by omission, not by decision ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)). How a motion is carried out — which cadence and step length, which recovery strategy — is the controller's choice; a row states what the hardware must let the controller choose.

| # | Motion | Kind | Flight phase | Where | Declared | Duration | What it sizes | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Walking, over a region of cadence and step length | commanded | no | everywhere, under the cap of the space | **top speed 1.0 m/s** (speed = cadence × step length), **0.5 m/s sustained**; cadence and step-length ranges open | **0.5 m/s for the operating endurance** ([2.3](#23-the-endurance-ceiling)); **1.0 m/s for up to 10 min** at a time. Both rest on the cooling of plan M-11, and were set on the simulated robot's gait: on it, on the makers' benches, without the shell, the left hip roll and knee sit at their modules' estimated sustained heat at 0.5 m/s, and hip pitch reaches 100 °C in about 16–19 min at 1.0 ([electrical §6h](../hardware/electrical/README.md#6h-walking-heat-by-speed-and-the-hip-roll-lever--m-11-2026-11-24)) | Its four corners, each something different: fast cadence with long steps the peak joint speed — the knee's, and with it D-2; slow cadence with long steps torque at deep flexion and balance at the ankle; fast cadence with short steps joint acceleration and loop latency; slow cadence with short steps none of the peaks. At 1.0 m/s the simulated robot's knee peaked at 6.7–6.9 rad/s ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)). Held, the heat of the hip: hip pitch and the knee fall with speed, hip roll hardly does, since most of its torque holds the body over the stance leg ([electrical §6h](../hardware/electrical/README.md#6h-walking-heat-by-speed-and-the-hip-roll-lever--m-11-2026-11-24)) — on the simulated robot's gait. A human-like gait is asked of the controller since 2026-11-24 (plan F-5); on it the hips and knees give off less than their makers' benches carry away, and the ankle pitch walks at 96% of its module's rated torque ([electrical §6j](../hardware/electrical/README.md#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)) | top speed decided 2026-11-23; the sustained speed and the 10 min at the top decided 2026-11-24, provisional until M-11; cadence and step length open |
| 2 | Walking backward and sideways, turning in place | commanded | no | everywhere | speed in each direction, turning rate: open | short | hip roll and yaw, ankle roll | listed, figures open |
| 3 | Stairs and slopes | commanded | no | stairs, ramps | riser height, slope, speed: open | open — sustained when climbing several floors, set by its purpose | knee and hip torque in flexion, covered for stairs by the 1.77 Nm/kg the hip is sized to and the knee's 2.79 ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)); held for long, the knee's continuous rating; with a load, the load case above | torque covered; geometry, speed and duration open |
| 4 | Squatting, kneeling, rising from a seat and from the floor | commanded | no | everywhere | **kneeling on one knee by preference** (2026-11-24); squat depth: open | momentary for rising; **a squat held at least 5 min with no load and 30 s with 20 kg, a kneel with no declared limit** ([Static holds](#static-holds), 2026-11-24), the situation choosing within it | knee torque at deep flexion, range of motion; held, the stall rating | rising from a seat covered ([electrical §6c](../hardware/electrical/README.md#6c-knee-torque--d-1-2026-11-21)); the holds decided 2026-11-24 and the rise from one knee computed as a static ([electrical §6l](../hardware/electrical/README.md#6l-squatting-and-kneeling--d-2-2026-11-24)); the rise's dynamics, from a deep squat and the floor, and squat depth open |
| 5 | Running | commanded | yes | open space only | **up to 2.5 m/s**, to keep pace with a person or leave a hazard | **60 s at 2.5 m/s, then a rest before the next run**; the rest open until the module's thermal data | the knee: 2.79 Nm/kg in stance, 299 Nm at the 107.0 kg reference point, the figure it is sized to since 2026-11-23; 10.9 rad/s mean in swing (12.6 the highest runner), at a swing torque of 0.53 Nm/kg or less; 0.96 Nm/kg RMS over the stride, 103 Nm, against what the module holds for 60 s. The ankle: 2.07 Nm/kg, 221 Nm, the figure it is sized to since the same date. The hip in the frontal plane: 1.73 Nm/kg peak, 185 Nm, and 0.65 Nm/kg RMS, the figures hip roll is sized to since the same date Landing impact on joints and reducers. Power about 1 kW, which the pack does not limit ([2.7](#27-peak-power-is-limited-by-the-source-not-the-actuators)) — all from [electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22) | decided 2026-11-22: speed, purpose and duration; rest open |
| 5a | Running faster than 2.5 m/s | commanded | yes | open space only | `OPEN` | — | the knee at 3.5 m/s: 3.1 Nm/kg, about 300 Nm, and 12.7 rad/s mean ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)) — no bought module found meets both ([`CLAUDE.md`](../CLAUDE.md) §2) | `OPEN` |
| 6 | Jumping | commanded | yes | open space only | height, distance: open | momentary | peak power, which the battery limits without a supercapacitor ([2.7](#27-peak-power-is-limited-by-the-source-not-the-actuators)); landing impact | listed, figures open |
| 7 | Balance recovery — after a push or a stumble, by a recovery step | reflex | possible | wherever the body is | **a sudden change of the body's velocity of 1.0 m/s forward or backward, or 0.5 m/s sideways, standing or during rows 1 and 2**; stronger goes to row 8; on stairs open. The figure is a robot's training range ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)), not drawn from a study of the disturbances people cause | momentary | the swing speed and torque of a recovery step: in a simulated robot, the backward push from standing asked the knee for 9.4 rad/s, more than walking at 1.0 m/s did, and ran its torque into the limit — 2.5 Nm/kg, 268 Nm at the reference point, within the knee's 299 | decided 2026-11-22, its source a robot's; on stairs open |
| 8 | Controlled fall, when recovery fails | reflex | — | wherever the body is | **what must be protected: knees, elbows, shoulders, hips and back, each by a protector certified to EN 1621-1 Level 2, or EN 1621-2 Level 1 at the back** ([04.1](04-shell.md#41-impact-padding)), held until a fall model sizes the protection; fall height open | momentary | the impact padding and the armour shell ([04.1](04-shell.md#41-impact-padding), [2.4](#24-protection)), shock at the joints, and the rise from the floor that follows (row 4) | protection held provisionally (2026-11-23), fall height open |
| — | Other demanding motions | — | — | — | — | — | — | open: not yet listed |

**Commanded and reflex are different kinds.** Rows 1–6 are motions the Main Controller chooses: each can be capped, confined to a space and refused. Rows 7 and 8 are not chosen. The body must be able to do them during any commanded row, whenever a disturbance arrives, so they lie over the rest of the table rather than beside it.

**A space sets a cap, not a size.** Near people, on stairs and in open space the controller holds the body below the envelope; the hardware is sized for the whole envelope and the reflex rows.

**A duration is a requirement, and temperature enforces it.** A row's duration is what the body must be able to sustain, and the module is chosen to meet it. What ends a sustained mode in service is the measured temperature of its motors, not a clock: the controller ends it there and records it. Peak torque says what a joint can do once; RMS torque over the motion, against the continuous rating in a body under its shell, says for how long ([electrical §6e](../hardware/electrical/README.md#6e-running-and-balance-recovery--d-2-2026-11-22)).

**What rows 5 and 7 ask of the knee module.** Since 2026-11-23 the knee and ankle pitch are sized to row 5, 2.79 and 2.07 Nm/kg, and the mass loop of 2.1 has been run with them on the bought modules of 2.6: at the 107.0 kg reference point the knee asks **299 Nm peak** in stance, at least 11 rad/s at about 50 Nm in swing (12 with margin), and **103 Nm RMS for 60 s**; the ankle **221 Nm** peak and 82 Nm RMS. Row 7's 268 Nm lies within the knee's figure. On the maker's bench the knee's ENCOS EC-A13715-P1-12.67 heats from 30 to 100 °C at 6.2 rad/s in 7′21″ at 90 Nm and 5′01″ at 100 Nm, and holds 150 Nm for 60 s ([electrical §6f](../hardware/electrical/README.md#6f-modules-declared-at-the-joint--d-2-2026-11-23)), so row 5's 60 s is met there with room; the EC-A10020-P2-24, the knee's module until the same day, holds about 79 Nm for 60 s and would not have met it at this mass. At the ankle the RMD-X12-P20-320's sheet gives no time under load, so its 85 Nm continuous torque stands against the 82 Nm RMS: that check is weaker than the knee's. A body under its shell is not the maker's bench (plan M-11), and the tests start at 30 °C, which a motor that has been walking is above.

## 2.7 Peak power is limited by the source, not the actuators

Actuators and pack both scale with the body, so both operating points of 2.5 have to be priced separately:

| Operating point | Body | Actuators accept | Pack | @3C | @5C | @10C |
|---|---|---|---|---|---|---|
| **2 h, durable — reference** | ~107 kg | **113–188 kW** | 4.3 kWh | 13 kW | 21 kW | 43 kW |
| 4 h, durable | ~140 kg | **136–226 kW** | 11.2 kWh | 34 kW | 56 kW | 112 kW |

**The source falls short in every cell — by up to 14×.** The actuators' 3–5 kW/kg ceiling is not reachable from the battery at the reference point, and high-energy-density chemistries generally trade away C-rate, so choosing the ceiling-grade pack widens the gap rather than closing it.

Even the most favourable corner — the larger pack at 10C against the low end of the actuator band — falls short, 112 kW against 136, and the band's top is 226 kW. Everywhere else the margin is wider. The 4-hour row scales the reference point's modules linearly; on bought modules at 4 hours the body is 133.3 kg ([electrical §6k](../hardware/electrical/README.md#6k-static-holds--d-2-2026-11-24)).

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
