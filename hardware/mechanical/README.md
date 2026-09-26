# Mechanical

Material and mechanism selection against the specification. Every figure is
sourced; §6 lists the references.

No CAD yet. What is fixed here is what the CAD will be made of and what the
joints will be made from — the decisions that have to precede geometry.

---

## 1. Structure

| Property | 7075-T6 aluminium | Carbon fibre composite | Source |
|---|---|---|---|
| Density | **2.81 g/cm³** | **1.55 g/cm³** | [1][3] |
| Young's modulus | 71.7 GPa | — | [1] |
| Tensile strength | 572 MPa | — | [1] |
| Specific stiffness | 26 GPa·SG⁻¹ | **30+ GPa·SG⁻¹** | [2] |
| Specific tensile strength | baseline | **~3.8×** aluminium | [3] |
| Stiffness at equal weight | baseline | **~3×** aluminium | [4] |
| Reported substitution gain | — | **40% mass saved, 80% stiffer** against 7075 | [4] |

**Selection: carbon fibre composite for long members, 7075-T6 at joints and
load-introduction points.**

> **This is not a preference, it is what the mass loop leaves room for.** The
> actuator finding in [`../electrical/`](../electrical/) shows `f_act` is under
> severe pressure — nothing below 80 Nm/kg keeps it inside the assumed range. If
> actuators are going to sit at the top of their band, structure has to sit at
> the top of its own, and a 40% saving against 7075 is the difference between a
> loop that closes and one that does not.
>
> Aluminium stays where composite is poor: bolted joints, bearing seats,
> anywhere load enters a member through a small area. Composite carries length;
> metal carries concentration.

**`f_str` is not closed by this.** Material fixes the density and the modulus;
the mass fraction depends on section sizing, safety factor and joint design,
none of which exist yet. [Spec
02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients) leaves it
at 0.25–0.35 and it stays there — but the choice above is what makes the lower
end reachable rather than aspirational.

## 2. Reducers, by joint class

| Class | Mechanism | Why |
|---|---|---|
| **Hip, knee** | Cycloidal / RV | ~85% efficiency, and many pins share the load so it absorbs the shock that footfall delivers and that strain-wave gears are damaged by [5][6] |
| **Shoulder, elbow** | QDD planetary, 6:1–15:1 | Backdrivable — see below |
| **Wrist, neck** | Harmonic | Smallest and lightest at high ratio, best precision, and these joints see no shock [5][6] |

**The arms are the interesting case, and the specification decides it.**
Harmonic drives are the industry standard for robot arms [6] and are lighter
than cycloidal at the same ratio — but at high ratio they are effectively
non-backdrivable. A stalled arm cannot yield: contact force becomes whatever the
controller commands, with nothing mechanical setting a ceiling.

[Spec 01](../../spec/01-architecture.md#application-frame) puts safe human
contact in the core group. QDD at 6:1–15:1 keeps the arm backdrivable, which
makes compliance a property of the mechanism rather than a promise made by
software that can fail. The cost is torque density, and §1 of the electrical
selection shows there is very little of that to spare — so this is a real trade
made deliberately, not a free choice.

Cycloidal reducers are heavier and bulkier with more parts [5], which is
acceptable in the legs and not in the wrists.

## 3. Protection

The group 5 standard requires handgun rounds, blades and everyday impact
together, and bullets and blades defeat armour by different mechanisms — a blade
tip passes between soft fibres where a bullet does not. A single body facing
both needs a layered package.

| Layer | Areal density | Source |
|---|---|---|
| Ballistic, NIJ IIIA, soft UHMWPE/aramid | **3.8–5.6 kg/m²** | [7][8] |
| Stab, NIJ 0115 level 1, spike | **~3.2 kg/m²** standalone | [9] |
| **Integrated multi-threat package** | **~6–9 kg/m²** | [10] |

Against 1.8 m² of skin area, at the coverage bands of [spec
02.4](../../spec/02-structure-and-motion.md#24-protection): **5.4 kg** at 50%
coverage and 6 kg/m², up to **13.0 kg** at 80% and 9 kg/m².

> Armour is non-scaling mass. It enters `m_ext` and is multiplied by `γ`, so at
> γ = 4.5 the difference between 50% and 80% coverage is ~3 kg of armour and
> **~14 kg of body**. With `f_act` already under pressure, coverage is the
> cheapest place to buy margin back — and the most visible thing to lose.

## 4. Shell layers

[Spec 04.5](../../spec/04-shell.md#45-the-three-layer-division) divides the shell
into three layers that cannot substitute for one another: sense-and-heal,
variable stiffness, and load-and-fire. All three are non-scaling mass competing
with armour inside the same 15–25 kg budget.

Areal densities for the first two remain `⟦IMPL⟧` — no reliable published figure
was found, and inventing one would put a number into the mass budget that
nothing supports.

## 5. Open

| `⟦IMPL⟧` | Depends on |
|---|---|
| Section sizing and safety factor | Load cases, which need a gait and a fall model |
| Joint range of motion, per joint | Mechanism layout |
| Bearing selection and preload | Joint loads |
| Areal density of the sense-and-heal and variable-stiffness layers | Materials not yet characterised at this scale |
| Fire layer temperature and duration | Must anchor to a firefighting-garment standard |

## 6. References

| # | Source |
|---|---|
| 1 | [7075 aluminium alloy](https://en.wikipedia.org/wiki/7075_aluminium_alloy) |
| 2 | [Aluminium vs carbon fibre: mechanical properties and applications](https://www.weerg.com/guides/which-is-stronger-aluminium-or-carbon-fibre) |
| 3 | [DragonPlate — carbon fiber vs aluminum](https://dragonplate.com/carbon-fiber-vs-aluminum) |
| 4 | [Carbon fiber rod vs aluminum: stiffness and weight](https://www.cnccarbonfiber.com/knowledge/carbon-fiber-rod-vs-aluminum.html) |
| 5 | [Cycloidal vs harmonic vs traction drive: robot joint comparison](https://imsystems.nl/cycloidal-vs-harmonic-vs-traction-drive/) |
| 6 | [Cycloidal reducer vs harmonic drive](https://github.com/SigGearDrive/SigGear-product-docs/blob/main/Comparisons/cycloidal-vs-harmonic-drive.md) |
| 7 | [Guardian Gear NIJ IIIA UHMWPE soft armour panel](https://bulletproofzone.com/products/guardian-gear-nij-level-iiia-handgun-rated-soft-armor) |
| 8 | [US Armor — body armor guide, NIJ levels](https://usarmor.com/body-armor-guide/) |
| 9 | [NIJ Standard 0115.00 — stab resistance of personal body armor](https://ballistics.com.au/wp-content/uploads/2020/05/NIJ_Standard_0115-00.pdf) |
| 10 | [Threat assessment and performance evaluation of multi-threat body armour](https://biokinetics.com/wp-content/uploads/2024/04/Anctil-et-al-2003-Threat-Assessment-and-Perf-Eval-of-Multi-Threat-Body-Amrour-AVT-HFM.pdf) |
