# 04 — Shell

The shell is set at what robotics can build today (2026-11-22): every layer is bought, or is integration GEMs designs and a bought service makes ([`CLAUDE.md`](../CLAUDE.md) §2). It has **three layers**, inside out — impact padding, an armour shell, and an outer layer of tactile skin under textile — and all three enter the same mass loop as everything else on the body. What is demonstrated only in the laboratory is not in it: it waits on the [upgrade path](#47-upgrade-path), which replaces a layer outright when the technology can meet it, and the baseline reserves no place for it.

Sources are numbered as in [`hardware/mechanical`](../hardware/mechanical/README.md#6-references).

## 4.1 Impact padding

The innermost layer: foam or a polymer lattice over the hardware, at pinch points and where a fall lands — row 8 of the [motion envelope](02-structure-and-motion.md#motion-envelope) sizes it. Shipping humanoids do the same: Figure 03 places multi-density foam at pinch points under a soft textile cover [11]; 1X NEO wraps its hardware in a custom 3D lattice polymer [12]; a Figure patent describes a multi-layered covering with energy-absorbing material — polyethylene, EVA and polyurethane foams among others — under a textile [13]. **TM.**

A bought candidate, Rogers PORON XRD, comes in five densities, specific gravity 0.14–0.40 — **0.14–0.40 kg/m² per millimetre** of thickness [14]. The figures are typical values, and the data sheet says it should not be used to create a specification. Thickness, and therefore areal density, is `⟦IMPL⟧` until plan M-8 sets it.

The padding also stands between the armour shell and anything hot: the shell's use-temperature limit is `⟦IMPL⟧` until read from the moulder's data sheet, and it must be checked against the module temperatures of [electrical §6e](../hardware/electrical/README.md), up to 100 °C in the thermal test read there.

## 4.2 Armour shell

Armour and shell are **one layer** (2026-11-22): a composite of ultra-high-molecular-weight polyethylene (UHMWPE), moulded per body segment, which carries the group 5 protection of [02.4](02-structure-and-motion.md#24-protection) — NIJ HG2, the level NIJ 0123.00 names in place of IIIA [17], with NIJ 0115.00 spike level 1 — and gives the body its form under the textile. UHMWPE is chosen for mobility and mass. **TM** as a material and a process; the moulding is GEMs' drawing, made by an armour manufacturer (plan M-7).

| | Figure | Source |
|---|---|---|
| Bought hard plate, 100% polyethylene, NIJ IIIA stand-alone, multi-curve, 8.9 mm | **7.2–9.1 kg/m²**, computed from the listed sizes and weights; a lower bound, since the shooter's-cut plates are smaller than their bounding rectangle | [15] |
| Bought soft multi-threat package, aramid and laminate, IIIA + spike 3, 10.4 mm | **7.03 kg/m²** | [16] |
| The mass loop | **7.5 kg/m²**, held (2026-11-22); optimistic against the hard plates above until a moulder's figure is in hand | [02.4](02-structure-and-motion.md#24-protection) |

A moulded shell of GEMs' own form is **tested to** the standard, not certified: NIJ keeps a list of compliant armour models [18], and a body's own panel set will not be one of them.

## 4.3 Outer layer: tactile skin and textile

**Tactile skin.** A large-area tactile skin lies on the armour shell, under the textile, over the body outside the hands and face. A bought candidate, Ensuring Technology's HexSkin [20]: up to 1.23 m² and 34,300 sensing points per cluster — **~2.8 points/cm²** — at **60 Hz**, normal force 0–50 N per point, under 1% of full scale, 1.75 mm thick, biaxially stretchable, with edge computing and CAN FD out. Two clusters cover the ~1.55 m² ordinary region of [05.2](05-sensing.md#52-tactile-layout), ~43,000 points. That meets what [06.6](06-audit-surface.md#66-contact-amplitude) asks — contact force and duration over every human-contact surface — and falls short of the density and rate of 05.2, which stay the requirement and go to the [upgrade path](#47-upgrade-path). The vendor states no mass, no price and no date of sale: mass is `⟦IMPL⟧`, and the part is a candidate.

The skin lies under the textile and on the hard shell because the alternatives each lose something: over a rigid panel it would be the outermost layer and the first thing struck, cut or burned; under one, a rigid panel would spread a touch before it reached the skin, and how finely the touch could still be located has not been checked.

**Textile.** The outermost layer is textile, removable, over the whole body. At the joints the armour shell stops and the textile carries on over the padding, as a Figure patent places "a different textile" between the moving parts of joints so that motion is not restricted [13]; whether the skin, which stretches, crosses the joints too is for plan M-8. The colour is fixed — dyed or printed. The fabric's flame resistance is set by 4.4.

## 4.4 Fire resistance

The body takes **limited heat, and does not fight fire directly at this level** (2026-11-22). Group 3 of [01](01-architecture.md) keeps house fires, with the body wearing an outer protective garment over the shell and calling for support; fighting fire directly is on the [upgrade path](#47-upgrade-path).

| Layer | Anchor | Status |
|---|---|---|
| Outer textile | **NFPA 1970 (2025)**, the standard for structural firefighting ensembles. Its flame resistance test admits an average char length of no more than 100 mm, an average afterflame of no more than 2.0 s, and no melting or dripping [19] | The requirement. No fabric data sheet has been read yet |
| Armour shell | A standard for a rigid layer is to be discussed: NFPA 1970 tests garment materials, not a moulded shell | **OPEN** |
| Tactile skin | Shielded by the textile | — |

Temperatures and durations beyond what the standard sets stay `⟦IMPL⟧`, anchored to the standard rather than derived here.

## 4.5 The three-layer division

| Layer | Function | Maturity | Areal density |
|---|---|---|---|
| **Impact padding** | Pinch points, falls; heat break between the shell and the modules | TM | 0.14–0.40 kg/m² per mm [14]; thickness `⟦IMPL⟧` |
| **Armour shell** | Group 5 protection and the body's form | TM | 7.5 kg/m² in the loop; 7.2–9.1 for bought hard plates [15] |
| **Outer layer** | Contact force over the body; textile cover and colour; the fire anchor | TM | Skin and textile `⟦IMPL⟧` |

> **This connects straight back to the mass loop.** All three layers are **non-scaling mass**: they enter `m_ext` and are **multiplied by `γ`**. The armour shell is the armour term of [02.5](02-structure-and-motion.md#25-mass-envelope), 7.8 kg at 65% coverage. The padding, the tactile skin and the textile sit in its fixed mass, 15–25 kg, `⟦IMPL⟧`, where "shell" stands. Each of their kilograms costs `γ` kg of body, as the armour's does.

## 4.6 Touch at the hands and face

**Hands.** Bought three-axis taxel modules, with the hand chosen under D-6. XELA's uSkin [21]: a curved fingertip, uSCu, of 30 taxels at ~6.5 mm, 71 Hz, screwed to the finger; flat patches, uSPa44, 16 taxels at 4.7 mm, 133 Hz; uSPa46, 24 taxels at 7.25 mm, 83 Hz — **~2–4.5 points/cm²**. The fine region of [05.2](05-sensing.md#52-tactile-layout) asks ~300/cm² at 1 kHz: **OPEN** against it. Ensuring Technology claims 361 sensels per cm² at 1000 Hz for its Tacta hand sensor in a press release [22]; with a data sheet it would close the gap.

**Face.** On the [upgrade path](#47-upgrade-path).

The hands carry their sensors at the surface, where the rule of 4.3 — sensors under the textile — cannot hold. That is a gap of this baseline, recorded here.

## 4.7 Upgrade path

What follows is `UPG`: on the upgrade path, not in the baseline. An upgrade is not a module added to or taken off the body; it is a later revision that replaces a layer outright when the technology can meet it.

> **Upgrading a LAB layer means running the loop of [02](02-structure-and-motion.md) again with the components current at the time — shell layer, pack and actuators together — because science and engineering do not advance one point at a time. If the loop closes, the upgrade is a new operating point; if it does not, the shortfall is paid in operating time or load margin — `⟦CTRL⟧`. The baseline reserves no place for any layer.**

### Self-healing skin

Graphene–PEDOT:PSS polymer: heals in **seconds**, stretches to ~**600%**, and senses pressure, temperature and pH. **LAB**, published 2025. *Sourced.* It would be skin and sensor at once, feeding [05](05-sensing.md) directly.

### Programmable stiffness

| Mechanism | Modulus range | Speed | Maturity |
|---|---|---|---|
| **Magnetorheological** — fluid or elastomer | **2–30×** at ~1000 mT | **milliseconds** | **LAB/TM** |
| **Electrorheological** | **~16×** (stiffness 64 → 1065 mN·mm⁻¹, >1500% variation) | **tens of ms** | **LAB** |
| **Jamming** (granular or layer) | large, up to ~two orders | tens to hundreds of ms | **LAB** |
| **Shape-memory polymer** (thermal) | large | **seconds to minutes** | **TM** |
| **Piezoelectric / magnetostrictive** | small amplitude | **sub-millisecond** | **TM** |

*Sourced.* A real material changes **stiffness within a finite range**; it does not change state of matter. Magnetorheological operation needs ~1000 mT, and generating that across a large volume takes heavy coils, power and heat: **variable stiffness is a local capability, not a whole-body one.**

### Colour

| Axis | Reality | Maturity |
|---|---|---|
| **Colour** — electrochromic | **~1–5 seconds** typical; best large-area ~0.8 s to colour, 4.2 s to bleach. **Slows as area grows** | **LAB/TM** *(sourced)* |
| **Texture** | Limited — surface microstructure only, no rearrangement of matter | **LAB in part** |

> **Three response classes, and they must not be merged.** Stiffness changes in **milliseconds**; colour changes in **seconds**; shape changes through mechanical folding. A specification that folds all three into "morphing" promises a speed only one of them delivers.

**Volume-preserving morphing** is reduced to predefined folding and jointed mechanisms; solid matter does not rearrange on demand. **Mass-changing morphing is not achievable** and is not specified.

### Whole-body touch at the density of 05.2

The layout of [05.2](05-sensing.md#52-tactile-layout) — ~300/cm² at the hands and face, ~20/cm² elsewhere, 1 kHz, ~460,000 points — and the readout it needs (plan E-7). Nothing on sale reaches it: the tactile skin of 4.3 has about a seventh of the density at a seventeenth of the rate.

### Responsive padding

A non-Newtonian, fluid-based material that stays compliant in ordinary interaction and stiffens under impact; on a 42 kg humanoid it let the robot take repeated falls, from 3 m among them, without damage [23]. **LAB**, 2026; the abstract gives no thickness or mass.

### Fighting fire directly

A shell that takes a fire itself, rather than through an outer garment (4.4).

**Operating point: `⟦CTRL⟧`.** The baseline sets the layers; armour coverage and level, and the operating point an upgrade lands on, are the operator's.
