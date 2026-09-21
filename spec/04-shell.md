# 04 — Shell

The shell is not one material. Quantifying it forces a division into **three
layers that cannot substitute for one another**, and all three compete for the
same mass budget.

## 4.1 Programmable stiffness

| Mechanism | Modulus range | Speed | Maturity |
|---|---|---|---|
| **Magnetorheological** — fluid or elastomer | **2–30×** at ~1000 mT | **milliseconds** | **LAB/TM** |
| **Electrorheological** | **~16×** (stiffness 64 → 1065 mN·mm⁻¹, >1500% variation) | **tens of ms** | **LAB** |
| **Jamming** (granular or layer) | large, up to ~two orders | tens to hundreds of ms | **LAB** |
| **Shape-memory polymer** (thermal) | large | **seconds to minutes** | **TM** |
| **Piezoelectric / magnetostrictive** | small amplitude | **sub-millisecond** | **TM** |

*Sourced.*

> This is the difference in kind from programmable matter: a real material
> changes **stiffness within a finite range**. It does not change state of
> matter.
>
> **A constraint that comes attached:** magnetorheological operation needs
> ~1000 mT. Generating that across a large volume requires heavy coils, draws
> power and makes heat. Therefore **variable stiffness is a local capability,
> not a whole-body one.** Where to place it is `⟦CTRL⟧`; placing it everywhere
> puts the mass loop of [02](02-structure-and-motion.md) outside convergence.

## 4.2 Self-healing

Graphene–PEDOT:PSS polymer: heals in **seconds**, stretches to ~**600%**, and
senses pressure, temperature and pH. **LAB**, published 2025. *Sourced.*

This layer is **both skin and sensor** — it feeds directly into
[05](05-sensing.md) rather than merely covering the body.

## 4.3 Colour and texture

| Axis | Reality | Maturity |
|---|---|---|
| **Colour** — electrochromic | **~1–5 seconds** typical; best large-area ~0.8 s to colour, 4.2 s to bleach. **Slows as area grows** | **LAB/TM** *(sourced)* |
| **Texture** | Limited — surface microstructure only, no rearrangement of matter | **LAB in part** |

> **Three response classes, and they must not be merged.** Stiffness changes in
> **milliseconds**; colour changes in **seconds**; shape changes through
> mechanical folding. A specification that folds all three into "morphing"
> promises a speed only one of them delivers.

**Volume-preserving morphing** is reduced to predefined folding and jointed
mechanisms; solid matter does not rearrange on demand. **Mass-changing morphing
is not achievable** and is not specified.

## 4.4 Fire resistance

A civil-fire-resistant outer layer, for limited duration. The specific
temperature and duration are `⟦IMPL⟧` — they must anchor to an existing
firefighting-garment standard rather than being derived here.

The architectural constraint is firm: the fire layer is **outermost and
sacrificial**. It must not be the layer carrying sensors, because sensors do not
survive the temperatures this layer exists to take.

## 4.5 The three-layer division

| Layer | Function | Cannot also |
|---|---|---|
| **Sense-and-heal** | E-skin plus self-healing polymer; soft, 600% stretch | carry structural load, or survive high heat |
| **Variable stiffness** | MR/ER/jamming, local | self-heal; requires a magnetic or electric field |
| **Load and fire** | Group 5 protection ([02.4](02-structure-and-motion.md#24-protection)) plus a sacrificial fire layer | sense, or change stiffness |

> **This connects straight back to the mass loop.** All three layers are
> **non-scaling mass** — they enter `m_ext` and are **multiplied by `γ`**. They
> compete directly with armour inside the same 15–25 kg budget declared in
> [02.5](02-structure-and-motion.md#25-mass-envelope).
>
> Areal densities for the sense-and-heal and variable-stiffness layers are
> `⟦IMPL⟧` — no reliable figure was found. **But the constraint is already firm:
> every kilogram of smart skin is a kilogram of armour given up, multiplied by
> `γ`.** Full-body e-skin *and* full-body armour *and* full-body variable
> stiffness are three things that do not coexist.

**Operating point: `⟦CTRL⟧`.** This chapter supplies amplitudes, speeds, and
three layers that cannot cover for each other. Allocating area between them is
the controller's decision.
