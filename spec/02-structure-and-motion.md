# 02 — Structure and motion

Structure, actuation and energy are one coupled loop. They cannot be specified
separately, and cutting the loop anywhere leaves the other ends meaningless.

> Every figure in this chapter is reproducible:
> `python scripts/gems_budget.py --check` recomputes them and confirms each one
> still appears here. See [`scripts/`](../scripts/).

## 2.1 The mass loop

Body mass divides into two kinds:

- **Scaling mass** — structure, actuators, battery. The heavier the body, the
  more of each it needs, because they exist to carry and move that very mass.
- **Non-scaling mass** — armour, compute, sensors, hands, skin, harness. These
  are placed on the body from outside; their size is set by the mission, not by
  the body's mass.

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

This is a structural statement, not a design point. If the three scaling terms
sum to the whole body, nothing is left for armour, sensors or hands — and **no
mass satisfies the system, at any price**. Such a design is not heavy; it does
not exist.

`γ` reads directly as **the mass price of each kilogram of function**: adding
1 kg of armour costs not 1 kg but `γ` kg of body.

## 2.2 The four coefficients

| Coefficient | Range | Status |
|---|---|---|
| `f_str` — structure | ~0.25–0.35 | `⟦IMPL⟧` — material and safety factor |
| `f_act` — actuators | ~0.25–0.35 | Derived, not assumed: the summed joint torque of the declared kinematics divided by actuator torque density. See [2.6](#26-actuation-and-manipulation) |
| `p` — specific power | **~10–25 W/kg** in motion | *Sourced* — commercial humanoids draw 300–1500 W walking; a 2.3 kWh pack supporting ~2 h of dynamic work implies ~1.1 kW continuous. Armoured bodies sit in the upper half |
| `e` — battery density | **450** (durable) / **900** (ceiling) Wh/kg | [03](03-energy.md) |

`f_str` is left open because it depends on material choices not yet made; its
range is narrow enough that no conclusion below changes sign.

`f_act` is **no longer an assumption**. It follows from the declared joint count
and the declared torque density, and 2.6 shows the derivation. It is listed as a
coefficient because the loop consumes it as one, not because it is free.

## 2.3 The endurance ceiling

Setting `Σf = 1` and solving for `t`:

```
t_max  =  (1 − f_str − f_act) · e / p
```

At `f_str + f_act = 0.60`:

| | `p`=10 | `p`=15 | `p`=20 | `p`=25 W/kg |
|---|---|---|---|---|
| **e = 450** Wh/kg | 18.0 h | 12.0 h | **9.0 h** | 7.2 h |
| **e = 900** Wh/kg | 36.0 h | 24.0 h | **18.0 h** | 14.4 h |

And `γ` inflates sharply on approach (`e`=450):

| `p` \ `t` | 2 h | 4 h | 6 h | 8 h | 10 h |
|---|---|---|---|---|---|
| 10 W/kg | 2.8 | 3.2 | 3.7 | 4.5 | 5.6 |
| 15 W/kg | 3.0 | 3.7 | 5.0 | 7.5 | 15.0 |
| **20 W/kg** | 3.2 | 4.5 | 7.5 | **22.5** | *diverges* |
| 25 W/kg | 3.5 | 5.6 | 15.0 | *diverges* | *diverges* |

> **Read this correctly.** It does not say the body runs for 9 hours. It says
> that at `p`=20 W/kg on a durable-grade pack, **no free-running body beyond
> 9 hours exists** — and that from about 6 hours the price is already
> meaningless, since γ=7.5 means each kilogram of armour costs 7.5 kg of body.
>
> Endurance remains `⟦CTRL⟧`. What this ceiling adds is a bound the controller
> cannot choose past, because on the far side there is no expensive design —
> there is no design.

## 2.4 Protection

The group 5 standard is one material level covering handgun rounds, knives and
everyday impact together. Bullets and blades defeat armour by different
mechanisms — a blade tip passes between soft fibres where a bullet does not — so
a single body facing both needs a multi-layer package.

| Layer | Areal density | Note |
|---|---|---|
| Ballistic, NIJ IIIA (soft UHMWPE/aramid) | **3.8–5.6 kg/m²** | lightest ~3.76; typical ~4.9; aramid hybrid ~5.6 |
| Stab, NIJ 0115 level 1 (spike) | **~3.2 kg/m²** standalone | |
| **Integrated multi-threat package** | **~6–9 kg/m²** | cheaper than adding two layers, dearer than one |

*Sourced.* Against a skin area of ~1.8 m² for a 1.75 m body:

| Coverage | Area | @6 kg/m² | @9 kg/m² |
|---|---|---|---|
| 50% — torso and head | 0.90 m² | 5.4 kg | 8.1 kg |
| 65% — plus outer limbs | 1.17 m² | 7.0 kg | 10.5 kg |
| 80% — near full body | 1.44 m² | 8.6 kg | 13.0 kg |

> Armour is non-scaling mass, so it enters `m_ext` and is multiplied by `γ`. At
> γ=4.5, choosing 80% coverage over 50% adds ~3 kg of armour — and **~14 kg of
> body**. This is where the trade bites hardest, and it is `⟦CTRL⟧`.
>
> Rifle-rated protection (NIJ III/IV) is achievable but adds substantially more
> mass. The anchor level proposed here is handgun plus blade plus everyday
> impact; anything above is `⟦CTRL⟧`.

## 2.5 Mass envelope

`m = γ · m_ext`, with `m_ext` = armour (5–13 kg) plus fixed mass — compute,
sensors, hands, skin, harness: **15–25 kg**, `⟦IMPL⟧`.

| Operating point | γ | Body mass |
|---|---|---|
| 2 h, durable pack | 3.2 | **70–114 kg** |
| 4 h, durable pack | 4.5 | **99–160 kg** |
| 8 h, ceiling pack | 4.5 | **99–160 kg** |
| 6 h, durable pack | 7.5 | 165–266 kg — *outside the sensible region* |

**Independent cross-check.** A real 1.2 m, 35 kg, 25-DOF humanoid scaled by mass
ratio `(1.75/1.2)³ = 3.10` gives **~109 kg** for a 1.75 m body of the same
architecture, before armour. That figure lands in the middle of the 99–160 kg
band at the 4-hour mark. Two independent derivations — one from the coupled
loop, one from geometric scaling of a machine that exists — agree to an order of
magnitude.

## 2.6 Actuation and manipulation

| Property | Envelope | Maturity |
|---|---|---|
| Specific power | **3–5 kW/kg** | **TM** |
| Specific torque | **75–90 Nm/kg peak** — see below | **TM**, top of the commercial band |
| Efficiency | 75–82% | **TM** |
| Response | milliseconds | **TM** |
| Joints | precision bearings with harmonic or cycloidal reducers | **TM** |
| Balance | IMU with ZMP control and reaction wheels | **TM** |
| Adhesion | gecko-type dry adhesive, moderate load | **LAB** |

### The basis matters as much as the number

Torque density is quoted on two incompatible bases, differing by a factor of
four. **Peak torque over actuator module mass** — motor, gearbox and housing —
is what module datasheets give, and what this specification declares. **Total
integrated actuator mass**, counting cooling and wiring, yields 18–22 Nm/kg for
the state of the art. A figure carried across from one basis to the other will
size a body that cannot be built.

**This specification declares peak-over-module, and 75–90 Nm/kg is the top of
what is commercially claimed.** The cost of standing there is real: part
availability narrows to a handful of modules, and there is no margin to trade
away later.

### Why 75 is the floor

The declared kinematics need **3414 Nm** summed across the 30 joints sized so
far — trunk lateral bend, the 31st, awaits a torque figure
([kinematics §1.4](../hardware/kinematics.md#14-the-trunk-is-a-spine-not-a-waist)) — at the 130 kg
operating point ([joint-by-joint sizing](../hardware/electrical/)). Divide:

| Density | Actuator mass | `f_act` |
|---|---|---|
| 75 Nm/kg | 45.5 kg | **0.35** |
| 80 Nm/kg | 42.7 kg | 0.33 |
| 90 Nm/kg | 37.9 kg | **0.29** |

**The declared band and the `f_act` band of 2.2 are the same constraint seen
twice.** 75–90 Nm/kg maps onto `f_act` 0.29–0.35; below 75 the actuators eat
the mass budget and the loop stops converging. The two figures cannot drift
apart, because each is derivable from the other and
`scripts/gems_budget.py --check` holds them together.

### Shoulder torque

`τ = M·g·L`, with the corresponding actuator mass at 80 Nm/kg. Full reach for
this body is **0.70 m**, declared at
[`hardware/kinematics.md`](../hardware/kinematics.md):

| Load | reach 0.40 m | reach 0.55 m | reach 0.70 m |
|---|---|---|---|
| 5 kg | 20 Nm (0.25 kg) | 27 Nm (0.34 kg) | 34 Nm (0.43 kg) |
| 15 kg | 59 Nm (0.74 kg) | 81 Nm (1.01 kg) | 103 Nm (1.29 kg) |
| 30 kg | 118 Nm (1.47 kg) | 162 Nm (2.02 kg) | 206 Nm (2.58 kg) |
| 50 kg | 196 Nm (2.45 kg) | 270 Nm (3.37 kg) | 343 Nm (4.29 kg) |

**A single joint is not the binding constraint.** Even 50 kg at full reach needs
only ~4.3 kg of shoulder actuator. What binds is the **sum across all the
joints**, and the legs carry 1905 Nm of the 3414 — which is why arm payload is a
poor lever on total actuator mass.

**Declared group 2 capability:** daily manipulation and moderate precision, with
per-arm loads in the tens of kilograms at short to medium reach.

## 2.7 Peak power is limited by the source, not the actuators

Actuators and pack both scale with the body, so both operating points of 2.5
have to be priced separately:

| Operating point | Body | Actuators accept | Pack | @3C | @5C | @10C |
|---|---|---|---|---|---|---|
| 2 h, durable | ~93 kg | **83–139 kW** | 3.7 kWh | 11 kW | 19 kW | 37 kW |
| 4 h, durable | ~130 kg | **117–194 kW** | 10.4 kWh | 31 kW | 52 kW | 104 kW |

**The source falls short in every cell — by between 1.1× and 12.5×.** The
actuators' 3–5 kW/kg ceiling is not reachable from the battery at any point on
this table, and high-energy-density chemistries generally trade away C-rate, so
choosing the ceiling-grade pack widens the gap rather than closing it.

Only the most favourable corner — the larger pack at 10C against the low end of
the actuator band — comes close, at 1.1×. Everywhere else the margin is wide.

> Supercapacitors are listed as an option in [03](03-energy.md). These figures
> say it more precisely: **without them, the body's peak power is set by the
> battery, not by the actuators**, and every claim about fast reflex, catching
> and jumping falls in the source-limited region. A supercapacitor does not
> change total energy; it changes instantaneous power available. Fitting one
> remains `⟦CTRL⟧`, but the trade is now quantified.

## 2.8 Hard constraints

Three axes draw on one budget and **cannot all be maximised**:

| Axis | Increasing it |
|---|---|
| **Protection** (coverage × level) | raises `m_ext`, multiplied by `γ` |
| **Free-running endurance** | raises `f_bat` → `γ` inflates non-linearly → divergence at `t_max` |
| **Stature** (height) | mass by the cube, armour area by the square |

**Choose two; pay on the third.** A body is not free to weigh whatever it likes:
the coupled loop converges only in a narrow region, and the energy measures of
[03](03-energy.md) are what widen that region, by lowering effective `p`.

**Operating point: `⟦CTRL⟧`.**
