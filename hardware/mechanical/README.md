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

> **This is not a preference, it is what the mass loop leaves room for.** The actuator finding in [`../electrical/`](../electrical/) shows `f_act` is under severe pressure — with the knee sized to running, 80 Nm/kg for every joint puts it outside the assumed range, and only the denser leg modules declared since 2026-11-23 bring it back ([spec 02.6](../../spec/02-structure-and-motion.md#what-the-two-figures-give)). If actuators are going to sit at the top of their band, structure has to sit at the top of its own, and a 40% saving against 7075 is the difference between a loop that closes and one that does not.
>
> Aluminium stays where composite is poor: bolted joints, bearing seats, anywhere load enters a member through a small area. Composite carries length; metal carries concentration.

**`f_str` is not closed by this.** Material fixes the density and the modulus; the mass fraction depends on section sizing, safety factor and joint design, none of which exist yet. [Spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients) leaves it at 0.25–0.35 and it stays there — but the choice above is what makes the lower end reachable rather than aspirational.

## 2. Reducers, by joint class

| Class | Mechanism | Why |
|---|---|---|
| **Hip, knee** | Cycloidal / RV or planetary — not strain-wave | Footfall delivers shock, and strain-wave gears are damaged by it [5][6]. Cycloidal shares the load across many pins at ~85% efficiency [5]; planetary is not ruled out by that reason, and three of the four bought candidates found at the legs' torque and speed are planetary ([electrical §6d](../electrical/README.md#6d-actuator-candidates--d-2-2026-11-22)) |
| **Shoulder, elbow** | QDD planetary, 6:1–15:1; up to 18:1 at shoulder yaw and elbow | Backdrivable — see below |
| **Wrist, neck** | Harmonic | Smallest and lightest at high ratio, best precision, and these joints see no shock [5][6] |

**The arms are the interesting case, and the specification decides it.** Harmonic drives are the industry standard for robot arms [6] and are lighter than cycloidal at the same ratio — but at high ratio they are effectively non-backdrivable. A stalled arm cannot yield: contact force becomes whatever the controller commands, with nothing mechanical setting a ceiling.

[Spec 01](../../spec/01-architecture.md#application-frame) puts safe human contact in the core group. QDD at 6:1–15:1 keeps the arm backdrivable, which makes compliance a property of the mechanism rather than a promise made by software that can fail. The cost is torque density, and §1 of the electrical selection shows there is very little of that to spare — so this is a real trade made deliberately, not a free choice.

**Shoulder yaw and elbow, up to 18:1, since 2026-11-24 (Plone).** The lightest bought module whose sheet holds the static lift there is the EC-A8116-P1-18. Its rotor inertia seen at the output is 0.061 kg·m², below the 0.070 of the shoulder's EC-A10020-P1-12 at 12:1; the friction a person would push against is not published for either ([electrical §6k](../electrical/README.md#6k-static-holds--d-2-2026-11-24)). The shoulder's other axes keep 6:1–15:1.

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

**The armour is the shell** (2026-11-22, [spec 04.2](../../spec/04-shell.md#42-armour-shell)): a hybrid laminate moulded per body segment in one part — UHMWPE plies for the handgun level, 5.80 kg/m² [24], with aramid spike plies, 1.42 kg/m² [16] — carrying the protection and the body's form. That is 7.22 kg/m² before finish and curvature; the mass loop keeps 7.5 kg/m². The bought hard plate above is heavier because it also stops special threats. The aramid plies lie on the outer face and the UHMWPE behind them, as the hybrid studies read find best against ballistic impact [30][31][32]; whether that order holds spike level 1 is for the moulder to test [33][34]. Para-aramid keeps its strength to 250 °C in short peaks [28]; UHMWPE is recommended for continuous use at 70 °C or lower [29], and is the layer's thermal limit.

Against 1.6 m² of skin area at 1.65 m, at the coverage bands of [spec 02.4](../../spec/02-structure-and-motion.md#24-protection): **4.8 kg** at 50% coverage and 6 kg/m², up to **11.5 kg** at 80% and 9 kg/m².

> Armour is non-scaling mass. It enters `m_ext` and is multiplied by `γ`, so at γ = 2.2 the difference between 50% and 80% coverage is ~3 kg of armour and **~6 kg of body**. With `f_act` already under pressure, coverage is the cheapest place to buy margin back — and the most visible thing to lose.

## 4. Shell layers

[Spec 04](../../spec/04-shell.md) sets the shell at three layers, inside out: impact padding, the armour shell of §3, and an outer layer of tactile skin under textile. All three are non-scaling mass: the armour shell is the armour term of `m_ext`; the padding, the skin and the textile sit in its fixed mass, 15–25 kg.

| Layer | Bought candidate | Areal density |
|---|---|---|
| Impact padding, where a fall lands | Certified protectors (2026-11-23): D3O Diablo L2 at knees, elbows, shoulders and hips, EN 1621-1 Level 2, 9.5 mm [35]; D3O BP4 L1 at the back, EN 1621-2 Level 1, 16 mm [37]; alternate Ghost L2, 11 mm [36]. Placed where a humanoid's falls do damage [23] | **1.10 kg** as a set, ~0.36 m²; 1.26 kg with the alternate |
| Impact padding, pinch points and heat break | Rogers PORON XRD, foam [14]; Figure 03 and 1X NEO use multi-density foam and a polymer lattice [11][12][13] | 0.14–0.40 kg/m² per mm, typical; thickness `⟦IMPL⟧` |
| Armour shell | Hybrid laminate, UHMWPE (Sinofibra SJ100-240H [24]) with aramid spike plies, moulded to the GEMs drawing | 7.5 kg/m² in the loop; 7.22 from the data sheets |
| Tactile skin | Ensuring Technology HexSkin [20] | `⟦IMPL⟧` — not stated by the vendor |
| Textile | Aramid outer-shell fabric, TenCate Nomex Advance Truecolor AV 9400 [27], EN ISO 15025 compliant, certified to EN 469; the requirement is EN ISO 15025 since 2026-11-24, NFPA 1970 (2025) [19] moving with group 3 of spec 01 to the upgrade path | **0.20 kg/m²** |

What the laboratory can do and the market cannot — self-healing skin, variable stiffness, electrochromic colour, whole-body touch at the density of spec 05.2, responsive padding [23] — is on the upgrade path of [spec 04.7](../../spec/04-shell.md#47-upgrade-path), with no place reserved for it.

## 5. Open

| `⟦IMPL⟧` | Depends on |
|---|---|
| Section sizing and safety factor | Load cases, which need a gait and a fall model |
| Joint range of motion, per joint | Mechanism layout |
| Bearing selection and preload | Joint loads |
| Areal density of the foam padding and the tactile skin | Foam thickness and coverage (plan M-8); the skin vendor's data |
| Whether EN 1621, a 50 J test on a 5 kg striker [38][39], stands for a fall of the body | A fall model and the fall height of spec 02.6 row 8 (plan M-8) |
| Whether the limb protectors can lie on modules at up to 100 °C | Their data sheets state no upper service temperature [35][36]; the motors' cooling (plan M-11) |
| Armour shell: the hybrid's areal density as moulded, with finish and curvature; the use-temperature limit of SJ100-240H itself (≤ 70 °C is Dyneema's [29]); spike level 1 with the aramid plies on the outer face | A moulder's data and test (plan M-7) |
| Padding thickness that keeps the armour shell below 70 °C over hot modules | The module temperatures of [electrical §6e](../electrical/README.md), up to 100 °C; plan M-8 |
| Heat reaching the armour shell's face, through the textile in a fire and through the outer aramid plies | No heat-transfer or conductivity figure on the data sheets read [27][28] |
| Ventilation (spec 04.8): louvred slots through the armour shell, shrouds at the hot modules, ducts along the spine, local loops at knees and ankles; the fans and their power, inside 57 dB(A) at 1 m; the filter layer on every slot, about 16 × 10 cm at each end of the main path, and its maintenance; protection against water | A thermal network at 35 °C, bought fans and filters (plan M-11); the modules' mounting faces; water, for discussion |

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
| 28 | [Teijin Aramid — Twaron, *A unique combination of properties*](https://product.teijinaramid.com/twaron-brochure/a-unique-combination-of-properties), brochure page as read 2026-11-23: no melting point, decomposes above 500 °C; short peaks below 250 °C and long-term exposure below 100 °C to keep strength; low heat conductivity |
| 29 | [Dyneema SK, crimped staple — technical data sheet](https://www.minifibers.com/files/TD/PI-TDS_Dyneema-SK-Crimped-Staple.pdf), as distributed by MiniFibers, undated; Dyneema a trademark of Avient Protective Materials: melts at 144–152 °C, decomposes above 300 °C; recommended continuous use 70 °C or lower |
| 30 | Ralph, Baker, Archer, McIlhagger, [*Optimization of soft armor: the response of homogenous and hybrid multi-ply para-aramid and ultra-high molecular weight polyethylene fabrics under ballistic impact*](https://doi.org/10.1177/00405175231194365), Textile Research Journal 93(23–24), 5168–5186, 2023, CC BY: specific energy absorbed higher with UHMWPE at the rear, at 340 m/s; less pronounced or absent at 620 m/s |
| 31 | Li, Xue, Sun, Gu, [*Ballistic penetration damages of hybrid plain-woven laminates with carbon, Kevlar and UHMWPE fibers in different stacking sequences*](https://doi.org/10.1016/j.dt.2022.07.006), Defence Technology 26 (2023) 23–38, CC BY: epoxy laminates, 1.1 g FSP; Kevlar in front of UHMWPE, EV50 +7.07% and specific energy +13.65% over all-Kevlar; UHMWPE in front, +1.91% and +3.55% |
| 32 | Liu et al., [*Effect of stacking sequence of the hybrid composite armor on ballistic performance and damage mechanism*](https://doi.org/10.1515/epoly-2025-0035), e-Polymers 25 (2025) 20250035, open access: carbon/aramid/UHMWPE on TPU, hot-pressed to 120 °C; aramid facing, UHMWPE at the rear (K3C6K12U6) best against a 4 g steel sphere at 615 m/s |
| 33 | Milliken & Company, [US 7,958,812 B2](https://patents.google.com/patent/US7958812), *Flexible spike and ballistic resistant panel*, granted 2011-06-14: stiff resin-impregnated aramid layers in front of spike-resistant textile; the reverse order "reduces the spike penetration resistant performance significantly" |
| 34 | Horsfall, Watson, Champion (Cranfield University), *Optimizing the stacking sequence in dual-purpose body armours*, paper for the 27th International Symposium on Ballistics; the copy read is dated 2013-08-29: a metal plate in a 20-layer Kevlar 49 pack resists a knife best in the middle, least at the rear; against handguns it helps only at the front |
| 35 | [D3O — Diablo L2 limb protectors, product data sheet](https://d3o.com/media/3635/d3o-diablo-l2-limb-protectors-data-sheet.pdf), © 2024 Design Blue Limited: elbow/knee 227 × 144 mm, 106 g; shoulder 195 × 144 mm, 95 g; hip 178 × 130 mm, 75 g; compact elbow/knee 194 × 115 mm, 73 g; 9.5 mm; passes EN 1621-1 Level 2; typical values |
| 36 | [D3O — Ghost L2 limb protectors, product data sheet](https://d3o.com/media/2549/d3o-ghost-l2-limb-protectors-data-sheet.pdf), © 2024 Design Blue Limited: knee/elbow 240 × 147 mm, 120 g; shoulder/hip 193 × 154 mm, 110 g; 11 mm; exceeds EN 1621-1:2012 Level 2; typical values |
| 37 | [D3O — BP4 L1 back protection, product data sheet](https://www.d3o.com/media/2789/d3o-bp4-l1-data-sheet.pdf), © 2024 Design Blue Limited: five sizes, 311 × 190 mm, 167 g to 540 × 272 mm, 384 g; size M 496 × 259 mm, 336 g, torso length 44–48 cm; 16 mm; exceeds EN 1621-2:2014 Level 1; typical values |
| 38 | [SATRA — EN 1621, motorcyclists' protective clothing against mechanical impact](https://www.satra.com/ppe/EN1621.php), as read 2026-11-23: EN 1621-1, mean maximum transmitted force below 35 kN, no single value over 50 kN; EN 1621-2, below 18 kN, none over 24 kN; optional tests at +40 °C and −10 °C |
| 39 | [Wikipedia — Motorcycle armor](https://en.wikipedia.org/w/index.php?title=Motorcycle_armor&oldid=1371968356), revision 1371968356, as read 2026-11-23: EN 1621-1, 5 kg mass, 40 × 30 mm striking face, 50 mm-radius dome, at most 50 J; Level 1 mean under 35 kN, no single result over 50 kN; Level 2 under 20 kN; EN 1621-2 Level 1 under 18 kN, none over 24 kN, Level 2 under 9 kN, none over 12 kN. A secondary source: the standard's text was not read |
| 40 | Chiang F. (UL Taiwan), [*IEC 62368-1 Technical Brief: Touch Temperature Limits*](https://japan.ul.com/wp-content/uploads/sites/27/2014/06/1_techbrief_touchtemp.pdf), 2010-10-22: TS1 limits abridged from table 42 of the first edition, after ISO 13732-1:2006 — over 1 min 48 °C metal and plastic; 10 s–1 min 51 and 60 °C; 1–10 s 60 and 77 °C; under 1 s 70 and 94 °C; TS2 10 K higher; conduction only, not convection or radiation |
| 41 | Unitree Robotics, *G1 User Manual* V1.6, 2026-08-12, and the G1 product data sheet, as supplied by the author on 2026-11-24: "a localized forced air-cooling system" (p. 4), "Cooling System: Local air cooling"; run at 0–40 °C, not waterproof, not dustproof (pp. 11, 26); intake and exhaust of the cooling fan checked before use (pp. 26–27); 35 kg, about 2 h |
| 42 | [EPFL — safety pictograms](https://www.epfl.ch/campus/security-safety/en/lab-safety/useful-documents/pictograms), as read 2026-11-24: ISO 7010 W017, Hot Surface |
| 43 | de Dear R.J., Arens E., Hui Z., Oguro M., *Convective and radiative heat transfer coefficients for individual human body segments*, Int. J. Biometeorology 40 (1997) 141–156, abstract as read through [Europe PMC](https://europepmc.org/article/MED/9195861) 2026-11-23: whole-body radiation 4.5 W/m²K, natural convection 3.4 (standing), forced h_c = 10.3·v^0.6 |
| 44 | Incropera et al., *Fundamentals of Heat and Mass Transfer*, 6th ed., 2007, Table 1.1, as reproduced in a [course handout](https://pages.mtu.edu/~fmorriso/cm3120/typical_values_heat_transfer_coefficient.pdf): free convection, gases 2–25 W/m²K; forced, gases 25–250, liquids 100–20,000 |
| 45 | Delta Electronics, [*Specification for approval, DC fan FFB0948VH-F00*](https://www.delta-fan.com/Download/Spec/FFB0948VH-F00.pdf), sample issue 2009-04-23: 48 V (28–53 V), 0.17 A, 8.16 W, 3700 rpm, 2.321 m³/min = 81.97 CFM at zero static pressure, 8.11 mmH₂O at zero flow, 48.2 dB(A) at 1 m, 128 g, −10 to +60 °C, 70,000 h at 40 °C |
| 46 | Emcel Filters, [*UL94 V-0 recognised air filters*](https://www.emcelfilters.co.uk/wp-content/uploads/2016/11/UL-Flame-Retardant-Filter.pdf), © 2011: polyurethane open-cell foam, 6 mm 20, 5 mm 30 and 5 mm 45 PPI; 65% arrestance (EU2) at 1 m/s; pressure drop against face velocity in a chart, about 12 Pa at 1 m/s for 5 mm 45 PPI; replace at a rise of 65 Pa |
