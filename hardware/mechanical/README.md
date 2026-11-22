# Mechanical

Material and mechanism selection against the specification. Every figure is sourced; §6 lists the references.

What is fixed here is what the CAD will be made of and what the joints will be made from — the decisions that have to precede geometry. The CAD itself begins with the skeleton of plan M-1 in [`skeleton/`](skeleton/): joint frames and segment envelopes generated from the kinematics, in FreeCAD, audited against the URDF. No part is drawn yet.

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

**Selection: carbon fibre composite for long members, 7075-T6 at joints and load-introduction points.**

> **This is not a preference, it is what the mass loop leaves room for.** The actuator finding in [`../electrical/`](../electrical/) shows `f_act` is under severe pressure — nothing below 80 Nm/kg keeps it inside the assumed range. If actuators are going to sit at the top of their band, structure has to sit at the top of its own, and a 40% saving against 7075 is the difference between a loop that closes and one that does not.
>
> Aluminium stays where composite is poor: bolted joints, bearing seats, anywhere load enters a member through a small area. Composite carries length; metal carries concentration.

**`f_str` is not closed by this.** Material fixes the density and the modulus; the mass fraction depends on section sizing, safety factor and joint design, none of which exist yet. [Spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients) leaves it at 0.25–0.35 and it stays there — but the choice above is what makes the lower end reachable rather than aspirational.

## 2. Reducers, by joint class

| Class | Mechanism | Why |
|---|---|---|
| **Hip, knee** | Cycloidal / RV or planetary — not strain-wave | Footfall delivers shock, and strain-wave gears are damaged by it [5][6]. Cycloidal shares the load across many pins at ~85% efficiency [5]; planetary is not ruled out by that reason, and three of the four bought candidates found at the legs' torque and speed are planetary ([electrical §6d](../electrical/README.md#6d-actuator-candidates--d-2-2026-11-22)) |
| **Shoulder, elbow** | QDD planetary, 6:1–15:1 | Backdrivable — see below |
| **Wrist, neck** | Harmonic | Smallest and lightest at high ratio, best precision, and these joints see no shock [5][6] |

**The arms are the interesting case, and the specification decides it.** Harmonic drives are the industry standard for robot arms [6] and are lighter than cycloidal at the same ratio — but at high ratio they are effectively non-backdrivable. A stalled arm cannot yield: contact force becomes whatever the controller commands, with nothing mechanical setting a ceiling.

[Spec 01](../../spec/01-architecture.md#application-frame) puts safe human contact in the core group. QDD at 6:1–15:1 keeps the arm backdrivable, which makes compliance a property of the mechanism rather than a promise made by software that can fail. The cost is torque density, and §1 of the electrical selection shows there is very little of that to spare — so this is a real trade made deliberately, not a free choice.

Cycloidal reducers are heavier and bulkier with more parts [5], which is acceptable in the legs and not in the wrists.

**Hip and knee revised 2026-11-22 (Plone).** The row read *Cycloidal / RV* alone, but its reason rules out strain-wave gears, not planetary ones. Between cycloidal and planetary the choice is made per module under D-2, on torque, speed, mass and what the datasheet says about shock, not on the reducer type.

## 3. Protection

The group 5 standard requires handgun rounds, blades and everyday impact together, and bullets and blades defeat armour by different mechanisms — a blade tip passes between soft fibres where a bullet does not. A single body facing both needs a layered package.

| Layer | Areal density | Source |
|---|---|---|
| Ballistic, NIJ HG2 (formerly IIIA), soft UHMWPE/aramid | **3.8–5.6 kg/m²** | [7][8] |
| Stab, NIJ 0115.00 spike level 1, soft aramid | **1.42 kg/m²**, 2.0 mm; spike level 3 2.83 kg/m² | [16] |
| **Integrated multi-threat package** | **~6–9 kg/m²** | [10] |
| Soft multi-threat package, IIIA + spike 3 | **7.03 kg/m²**, 10.4 mm | [16] |
| Hard plate, 100% polyethylene, IIIA and special threats stand-alone, multi-curve | **7.2–9.1 kg/m²**, 8.9 mm, computed from listed sizes and weights; a lower bound | [15] |
| UHMWPE cross-ply for pressed hard plates (SJ100-240H), IIIA, 24 plies | **5.80 kg/m²**; pressed at 125–135 °C, 8–15 MPa; the vendor's own laboratory | [24] |
| UHMWPE cross-ply for soft armour (SJ400-130S), IIIA, 22–25 plies | **2.90–3.25 kg/m²**; the vendor's own laboratory | [25] |

The handgun levels were renamed when NIJ Standard 0101.07 moved its levels into NIJ Standard 0123.00: Level II is now HG1 and Level IIIA HG2 [17][18]. The spike row read ~3.2 kg/m² until 2026-11-22, citing the standard itself [9], which sets the test and gives no areal density; the figure now comes from a bought panel's specification.

**The armour is the shell** (2026-11-22, [spec 04.2](../../spec/04-shell.md#42-armour-shell)): a hybrid laminate moulded per body segment in one part — UHMWPE plies for the handgun level, 5.80 kg/m² [24], with aramid spike plies, 1.42 kg/m² [16] — carrying the protection and the body's form. That is 7.22 kg/m² before finish and curvature; the mass loop keeps 7.5 kg/m². The bought hard plate above is heavier because it also stops special threats.

Against 1.6 m² of skin area at 1.65 m, at the coverage bands of [spec 02.4](../../spec/02-structure-and-motion.md#24-protection): **4.8 kg** at 50% coverage and 6 kg/m², up to **11.5 kg** at 80% and 9 kg/m².

> Armour is non-scaling mass. It enters `m_ext` and is multiplied by `γ`, so at γ = 2.6 the difference between 50% and 80% coverage is ~3 kg of armour and **~7 kg of body**. With `f_act` already under pressure, coverage is the cheapest place to buy margin back — and the most visible thing to lose.

## 4. Shell layers

[Spec 04](../../spec/04-shell.md) sets the shell at three layers, inside out: impact padding, the armour shell of §3, and an outer layer of tactile skin under textile. All three are non-scaling mass: the armour shell is the armour term of `m_ext`; the padding, the skin and the textile sit in its fixed mass, 15–25 kg.

| Layer | Bought candidate | Areal density |
|---|---|---|
| Impact padding | Rogers PORON XRD, foam [14]; Figure 03 and 1X NEO use multi-density foam and a polymer lattice [11][12][13] | 0.14–0.40 kg/m² per mm, typical; thickness `⟦IMPL⟧` |
| Armour shell | Hybrid laminate, UHMWPE (Sinofibra SJ100-240H [24]) with aramid spike plies, moulded to the GEMs drawing | 7.5 kg/m² in the loop; 7.22 from the data sheets |
| Tactile skin | Ensuring Technology HexSkin [20] | `⟦IMPL⟧` — not stated by the vendor |
| Textile | Aramid outer-shell fabric, TenCate Nomex Advance Truecolor AV 9400 [27], certified to EN 469; the requirement is NFPA 1970 (2025) [19] | **0.20 kg/m²** |

What the laboratory can do and the market cannot — self-healing skin, variable stiffness, electrochromic colour, whole-body touch at the density of spec 05.2, responsive padding [23] — is on the upgrade path of [spec 04.7](../../spec/04-shell.md#47-upgrade-path), with no place reserved for it.

## 5. Open

| `⟦IMPL⟧` | Depends on |
|---|---|
| Section sizing and safety factor | Load cases, which need a gait and a fall model |
| Joint range of motion, per joint | Mechanism layout |
| Bearing selection and preload | Joint loads |
| Areal density of the padding and the tactile skin | Padding thickness (plan M-8); the skin vendor's data |
| Armour shell: the hybrid's areal density as moulded, with finish and curvature, and its use-temperature limit | A moulder's data; the limit is checked against the module temperatures of [electrical §6e](../electrical/README.md) |
| Textile: NFPA 1970 certification | The candidate fabric holds EN 469 [27] |
| Fire standard for the armour shell | **OPEN** — NFPA 1970 tests garment materials, not a moulded shell ([spec 04.4](../../spec/04-shell.md#44-fire-resistance)) |

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
| 11 | [Figure AI — Introducing Figure 03](https://www.figure.ai/news/introducing-figure-03), 2025-10-09: multi-density foam at pinch points, soft textiles, washable covers removable without tools |
| 12 | [1X — NEO](https://www.1x.tech/neo): "custom 3D lattice polymer" around the hardware, a machine-washable nylon suit |
| 13 | Figure AI Inc., US 12,611,766 B2, *Humanoid robot with advanced kinematics*, granted 2026-04-28; description as published in [US 2026/0077482 A1](https://patents.google.com/patent/US20260077482A1/en): multi-layered exterior covering with energy-absorbing material under a textile; "a different textile" between the moving parts of joints |
| 14 | Rogers Corporation, *PORON XRD Extreme Impact Protection — Physical Properties*, data sheet as distributed by Seal & Design; typical values |
| 15 | [Point Blank — Speed Plates, hard armor plate](https://cdn.shopify.com/s/files/1/0402/4713/2328/files/speed-plates-2024.pdf), 2024: 100% polyethylene, IIIA stand-alone, 0.35 in, sizes and weights |
| 16 | [Safariland — technical specifications MT01-IIIA, PS-1.0, PS-3.0](https://www.copquest.com/body-armor-spec-sheets/Prism-Product-Specs.pdf), catalogue pages 26–30 (2016): areal density and thickness, NIJ 0101.06 and 0115.00 |
| 17 | [NIJ Standard 0123.00 — ballistic protection levels and test threats](https://nij.ojp.gov/topics/equipment-and-technology/specification-nij-ballistic-protection-levels-and-associated-test-threats-nij-standard-012300): Level IIIA renamed HG2 |
| 18 | [NIJ Standard 0101.07 — ballistic resistance of body armor](https://nij.ojp.gov/topics/equipment-and-technology/ballistic-resistance-body-armor-nij-standard-010107), 2025-12-01; the 0101.06 compliant products list kept through at least 2029 |
| 19 | [NFPA 1970, 2025 edition, TIA 25-5](https://docinfofiles.nfpa.org/files/AboutTheCodes/1970/TIA_1970_25_5.pdf): flame resistance — average char length ≤ 100 mm, average afterflame ≤ 2.0 s, no melting or dripping |
| 20 | [Ensuring Technology — HexSkin](https://www.ensuringtech.com/en/product/#hexskin), product page as captured 2026-11-22: 1.23 m² and 34,300 points per cluster, 60 Hz, 0–50 N per point, 1.75 mm, CAN FD |
| 21 | [XELA Robotics](https://www.xelarobotics.com/) — uSkin spec sheets uSPa44 (2024-10-23), uSCu (2024-10-23), uSPa46 / XR1946 (2025-07-23) |
| 22 | [Ensuring Technology — CES 2026 press release](https://finance.yahoo.com/news/fingertips-full-body-coverage-ensuring-090900110.html), 2026-01-09: Tacta, 361 sensels per cm² at 1000 Hz; the vendor's claim |
| 23 | Wang et al., [*Soft Responsive Materials Enhance Humanoid Safety*](https://arxiv.org/abs/2601.02857), arXiv:2601.02857, 2026-01-06 |
| 24 | Sinofibra Advanced Materials, LOONG-FLEX SJ100-240H, UHMWPE UD for hard armour, product data sheet v2.1, 2026-01-18 ([sinofibra.com](https://www.sinofibra.com)): 240 g/m² per 4-ply sheet; IIIA at 24 plies, 5.80 kg/m²; press 125–135 °C, 8–15 MPa; typical values, the vendor's laboratory |
| 25 | Sinofibra Advanced Materials, LOONG-FLEX SJ400-130S, UHMWPE UD for soft armour, product data sheet v2.1, 2026-01-18: IIIA at 22–25 plies, 2.90–3.25 kg/m² |
| 26 | FIBER-LINE, *Nomex meta-aramid* fibre data sheet (2016): no melting point; 0.4% shrinkage in dry air at 177 °C for 30 min; specific gravity 1.38 |
| 27 | TenCate Protective Fabrics, *Nomex Advance Truecolor AV 9400*, technical data Q1-2025: 200 g/m², Nomex/Kevlar/anti-static; EN ISO 15025 compliant; ISO 17493 at 180 °C ≤ 2%; certified EN 469 and EN 1149-5; indicative values |
