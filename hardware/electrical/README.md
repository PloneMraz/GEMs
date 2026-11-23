# Electrical

Component selection against the specification. Every figure below is sourced; §7 lists the references.

| File | Contents |
|---|---|
| [`actuator_sizing.py`](actuator_sizing.py) | Sizes every joint from its peak torque and reports the resulting `f_act` |

---

## 1. The actuator finding — raised, and resolved

> **Resolved by option A on 2026-09-22.** The specification then declared **75–90 Nm/kg peak, on a peak-torque-over-module-mass basis**, and states the basis explicitly. **Revised 2026-09-26 to 80–90 Nm/kg** when the trunk was re-sized from measured human strength and gained a lateral-bend axis (§6a). **The arm payload came down to 15 kg the same day (§6b)**, which took `f_act` at 80 Nm/kg from 0.34 to 0.30; the floor stayed at 80. `spec/` and this document agree again; the record below is kept because the reasoning is what justifies a figure at the top of the commercial band. Note that the §1 tables below were computed with the whole of `f_act` treated as scaling with body mass; §6b explains why only the leg and trunk part does.

Sizing the declared 30 joints against published torque densities did not reproduce the actuator mass fraction the specification assumed. Tool output as run on 2026-09-22, before the correction:

```
Nm/kg    mass kg    f_act    source
  22.0      155.2     1.19   integrated state of the art, whole-actuator
  33.0      103.5     0.80   the figure spec 02.6 uses
  36.0       94.8     0.73   top of the range spec 02.6 declares
  52.0       65.7     0.51   commercial QDD module, 8:1 planetary
  88.7       38.5     0.30   commercial hollow-shaft planetary module, peak
```

[Spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients) assumes `f_act` between **0.25 and 0.35**. [Spec 02.6](../../spec/02-structure-and-motion.md#26-actuation-and-manipulation) declared, at that time, actuator specific torque of **30–36 Nm/kg**, and sized its own worked example at 33.

**Those two figures were not compatible.** At 33 Nm/kg the actuators weigh 80% of the body, `Σf` exceeds 1 before a single cell of battery is fitted, and the coupled loop does not converge at any endurance — not at four hours, not at two.

Both figures in that paragraph have since been corrected; they are quoted here as they stood when the contradiction was found.

### It is not the arms

Halving the per-arm payload from 30 kg to 15 kg takes the total from 3414 Nm to 3000 Nm: `f_act` falls from 0.80 to 0.70. The legs carry 1905 Nm of the total, and leg torque is set by body mass, not by what the hands hold.

### A lighter body is worse, not better

| Body | Total torque | `f_act` at 33 Nm/kg |
|---|---|---|
| 70 kg | 2396 Nm | **1.04** |
| 90 kg | 2735 Nm | 0.92 |
| 110 kg | 3075 Nm | 0.85 |
| 130 kg | 3414 Nm | 0.80 |

Leg and waist torque scale with mass; wrist, neck and arm torques do not. Shed mass and the fixed torques dominate a smaller budget. **There is no lighter version of this body that closes at 33 Nm/kg.**

### What does close

The lowest density that puts `f_act` inside the assumed range is **75 Nm/kg**, and only the best commercially claimed module reaches it. At a mainstream QDD module's 52 Nm/kg, `f_act` = 0.51 and the loop is already marginal:

| `f_act` | 2 h | 4 h |
|---|---|---|
| 0.30 — assumed | γ = 3.2 | γ = 4.5 |
| 0.51 — at 52 Nm/kg | γ = 9.9 | γ = 81.8 |
| 0.80 — at 33 Nm/kg | **diverges** | **diverges** |

This was a decision for the author, not something to be silently patched. The options as put are kept at §6, with the one taken marked.

---

## 2. Actuators

**Selection: quasi-direct drive, hollow-shaft planetary, at the top of the commercial torque-density band.** Nothing lower closes the mass loop.

| Property | Figure | Source |
|---|---|---|
| Commercial QDD module, 8:1 planetary | **52 Nm/kg**, 9 arcmin backlash | CubeMars AKE80-8 [1] |
| Commercial hollow-shaft planetary, 16:1 | **88.7 Nm/kg** peak — 78 Nm peak, 26 Nm rated, 879 g; 78 / 0.879 = 88.7. The 85 Nm quoted here until 2026-09-26 was the end of the torque curve, see §6b | CubeMars AKH70-16 [1][22] |
| The same motor at 48:1 | **159 Nm/kg** peak — 222 Nm peak, 74 Nm rated, 1396 g, three-stage planetary; output ±5 rad/s against ±13 rad/s at 16:1 [23] | CubeMars AKH70-48 [26], search excerpts; page not readable from here |
| Highest commercial claim, series | up to **36 Nm/kg** | ZHR-H series [3] |
| Integrated SOTA, whole-actuator | **18–22 Nm/kg** — axial flux, cycloidal QDD, hybrid housing, hollow titanium shaft, phase-change cooling | [3] |
| Design floor for hip and knee | **> 30 Nm/kg** peak | [3] |
| Industrial servo, for contrast | 5–10 Nm/kg | [3] |
| QDD reduction ratios | **6:1 to 15:1**, against 50:1–120:1 industrial | [2] |
| QDD mass saving | **40–60%** against high-ratio gearboxes | [2] |

> **The two families of number.** A module advertised at 88.7 Nm/kg quotes peak torque over motor-plus-gearbox mass; an integrated figure of 18–22 Nm/kg counts housing, cooling and wiring as well. They differ by a factor of four and both are honest. The sizing script prints both so the gap cannot be read past.

**Why QDD and not harmonic drive.** [Spec 01](../../spec/01-architecture.md#application-frame) puts safe human contact at the core of the application frame. High-ratio harmonic drives are effectively non-backdrivable: a stalled arm cannot yield, so contact force is whatever the controller commands and nothing mechanical limits it. QDD at 6:1–15:1 stays backdrivable, which makes compliance a property of the mechanism rather than a promise made by software. That is a specification-driven reason, not a preference.

## 3. Power

| Property | Figure | Source |
|---|---|---|
| Silicon-anode cell, commercially available | **450 Wh/kg**, 1150 Wh/L | Amprius [4] |
| Solid-state pouch, stack level | **465 Wh/kg**, 1400 Wh/L | SOLiTHOR [5] |
| Semi-solid pouch, validated | ~347 Wh/kg | [6] |
| All-solid-state pouch for robots | mass production targeted 2027, robots first | Samsung SDI [6] |
| Rate capability demonstrated | 80% retention after 400 cycles at 4C | QuantumScape [6] |

> **The durable tier's density can be bought; its preferred chemistry cannot yet.** [Spec 03.1](../../spec/03-energy.md#31-source) declares 400–500 Wh/kg, solid-state preferred but not required (Plone, 2026-11-05). At 450 Wh/kg the cell on sale is silicon-anode with a liquid electrolyte (Amprius [4]); solid-state at that density is at validated stack level, not a product (SOLiTHOR [5]), and Samsung SDI targets mass production in 2027 [6]. So under present technology the tier is filled by silicon-anode, and the pack carries the safety a solid electrolyte would. Neither the Amprius cell's cycle life nor an abuse-test result is in hand: its row in the AVL leaves them blank. The ceiling tier at 700–1100 Wh/kg remains laboratory-only, exactly as the specification states.
>
> **The rate trade the specification asserts is confirmed.** The literature frames it as a straight choice between high C-rate and high energy density [7], which is the mechanism behind [spec 02.7](../../spec/02-structure-and-motion.md#27-peak-power-is-limited-by-the-source-not-the-actuators): choosing the ceiling pack widens the peak-power shortfall rather than closing it.

## 4. Compute

| Property | Figure | Source |
|---|---|---|
| Edge module | NVIDIA Jetson AGX Thor | [8] |
| AI throughput | up to 2070 FP4 TFLOPS, 7.5× AGX Orin | [8][9] |
| Power | **40–130 W**, 3.5× the efficiency of AGX Orin | [8][9] |
| Memory | 128 GB | [9] |
| Interconnect | PCIe Gen 5, Blackwell architecture | [9] |

**Against the specification.** At 130 W on a 130 kg body this is **1 W/kg** — between 4% and 10% of the 10–25 W/kg motion budget of [spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients). Edge compute is affordable in the power budget; what it is not is free, and [spec 05.6](../../spec/05-sensing.md#56-the-on-body--off-body-compute-split) states why that matters.

The compression duty is **≥2:1 and realistically 8:1** of 15.8 Gbps raw ([spec 05.4](../../spec/05-sensing.md#54-aggregate-rate-against-the-link)) — about 2 GB/s of sensor data processed in real time. Whether this part meets it is a measurement, not a datasheet reading, and it stays open until measured.

## 5. Bus

**Selection: EtherCAT for the joint chain, CAN FD for distributed sensing.**

| Property | Figure | Source |
|---|---|---|
| EtherCAT in humanoids | 1 kHz (RoboSimian, Hydra, ARMAR-6) | [10] |
| | 2 kHz (Atlas, LOLA) | [10] |
| | **4 kHz** dual-channel (TOCABI) | [10] |
| CAN FD | 64-byte data field, faster data phase, CAN arbitration retained | [11] |
| Common practice | hybrid: EtherCAT for high-performance joints, CAN FD for distributed controllers | [11] |

> Boston Dynamics moved from CAN in Petman to EtherCAT in Atlas [10]. The balance loop needs **≥500 Hz** ([spec 07.2](../../spec/07-firmware-and-software.md#72-real-time-requirements)) and joint current loops need kHz-class service; EtherCAT at a demonstrated 2–4 kHz clears both with margin, and CAN FD does not.
>
> **This also bears on the timestamp requirement.** EtherCAT distributed clocks give the shared time base [spec 07.2](../../spec/07-firmware-and-software.md#72-real-time-requirements) demands, rather than leaving skew to be inferred later.

## 6. The decision

The finding of §1 had no technical answer — three options, trading against each other. They are kept here because a design that does not record what it turned down cannot explain itself later.

| Option | What it costs | |
|---|---|---|
| **A — Raise the declared torque density to ≥75 Nm/kg** | Commits the design to the top of the commercial market. Part availability narrows sharply and there is no margin left to trade away | **✅ taken** |
| **B — Accept a higher `f_act`** | At 52 Nm/kg, `f_act` = 0.51: γ = 9.9 at two hours and 81.8 at four. Endurance collapses below two hours and the mass envelope of spec 02.5 becomes wrong | rejected |
| **C — Reduce what the body must do** | Lower peak torque means less payload, gentler gait, less dynamic recovery. The legs dominate, so this means a body that walks rather than one that catches itself | rejected on 2026-09-22 — **reopened and taken in part on 2026-09-26** for the arms only, see §6b: the 30 kg payload it was weighed against was a stress test, not the specification's group 2 capability |

### What option A committed the design to

**75–90 Nm/kg peak, over module mass — 80–90 since 2026-09-26.** Only a handful of commercial modules reach it — the hollow-shaft planetary at 88.7 Nm/kg is at the very top of what is claimed, and a mainstream 52 Nm/kg module does not qualify. Supply is thin and will stay thin.

**The specification now states the basis**, which is the part that actually prevents a repeat. The original error was not only a wrong number: 30–36 Nm/kg is a reasonable figure *on the integrated basis*, and it was being used as if it were peak-over-module. A density with no basis attached is a number waiting to be misread.

**The two bands are now one constraint.** 80–90 Nm/kg maps onto `f_act` 0.30–0.34, each derivable from the other, and `scripts/gems_budget.py --check` holds them together — including the actuator-mass column, which it did not cover before and which is exactly where this drift hid.

## 6a. Trunk lateral-bend torque — research, 2026-09-26

Decision D-9 added a lateral-bend axis to the trunk ([kinematics §1.4](../kinematics.md#14-the-trunk-is-a-spine-not-a-waist)). It has no torque figure yet. Two things were found, and one was not.

**What the trunk figures already in the table rest on.** Nothing. The waist rows — trunk pitch 1.54 Nm/kg (200 Nm at 130 kg) and trunk yaw 0.77 Nm/kg — had no source in §7; they were assumed when the table was written. The source found for lateral bend below covers all three axes, and has replaced both.

**Human trunk torque per kilogram, all three axes — Pan et al. 2025 [14] (open access at the DOI; its licence is CC BY-NC-ND, so it is cited, not vendored).** 122 asymptomatic adults, 61 male (24.5 ± 2.3 y, 73.4 ± 15.0 kg, 175.6 ± 6.8 cm) and 61 female; Bionix Sim3 Pro dynamometer; median peak torque, normalised to body weight:

| Axis | Isometric, male | Isometric, female | Isokinetic 15°/s, male | Isokinetic 15°/s, female |
|---|---|---|---|---|
| Extension (trunk pitch) | **1.74 Nm/kg** | 1.63 | 0.69 | 1.40 |
| Flexion | 1.15 | 1.05 | 0.58 | 0.93 |
| **Lateral bending, left / right (trunk roll)** | **0.95 / 0.91** | 1.00 / 0.86 | 0.47 / 0.46 | 0.88 / 0.78 |
| Axial rotation, left / right (trunk yaw) | **0.74 / 0.64** | 0.66 / 0.66 | 0.35 / 0.40 | 0.43 / 0.53 |

Sex differences vanish once normalised (P > 0.05), so the male isometric column is used as the figure. The isokinetic values are lower because the device's slow constant-velocity protocol is not a peak-effort condition; they are not a dynamic peak. Lateral bending is **0.55 × extension**.

**Cross-check, two engineered waists and one robot URDF:**

| Source | Roll : pitch | Note |
|---|---|---|
| 3-DOF coupled tendon-driven humanoid waist, *Advanced Robotics* 2023 [15]; full specification repeated in the same group's 2025 paper [19] | 0.50 | Designed pitch : roll : yaw = 4 : 2 : 1, realised as 87.0 / 53.0 / 22.2 Nm static from three RMD X8 Pro actuators of 13.0 Nm nominal each. ROM pitch −30…60°, roll ±30°, yaw ±90°. Sized for a torso surrogate of **10 kg at 0.2 m** — a ~20 Nm gravitational moment — so the absolute figures are for a light upper body; only the ratio transfers |
| Flexinoid tensegrity spine, *Scientific Reports* 2025 [18] | — | No torque figures for pitch or roll; actuators are 1.89 N·m servos with elastic assistance. Its value is as a mechanism reference — see kinematics §1.4 |
| Unitree G1 URDF, 29-DOF [16] | 1.0 | waist_roll = waist_pitch = 35 Nm, waist_yaw 88 Nm, robot 35.1 kg. An outlier: G1's pitch and roll travel only ±30°, both sized far below its yaw |

Human strength and a waist engineered to match human balance agree at **about 0.5–0.55**. The G1 ratio is set by its small-travel design, not by need.

**Decision, 2026-09-26: option B, floor 80.** All three trunk axes take the male isometric figures of [14]; the declared density floor of spec 02.6 moves from 75 to 80 Nm/kg — 80 rather than the computed 78 so that the next figure sized does not break the band again, and because 80 is the density the shoulder-torque table of spec 02.6 already used. The band narrows to 80–90: the design stands 10 Nm/kg, not 15, below the top of the commercial market. The options as they were weighed, at the 130 kg point:

| | Pitch | Roll | Yaw | Σ torque | `f_act` at 75 | at 80 | at 88.7 | Density for `f_act` ≤ 0.35 |
|---|---|---|---|---|---|---|---|---|
| Today, no roll | 200 | — | 100 | 3414 Nm | 0.350 | 0.328 | 0.296 | 75.0 |
| **A** — add roll at 0.95 Nm/kg, keep the assumed pitch and yaw | 200 | 124 | 100 | 3537 Nm | 0.363 | 0.340 | 0.307 | **77.7** |
| **B** — all three trunk axes from [14]: 1.74 / 0.95 / 0.74 Nm/kg | 226 | 124 | 96 | 3560 Nm | 0.365 | 0.342 | 0.309 | **78.2** |

Either option moves the floor of the declared density band (spec 02.6) from 75 to about 78 Nm/kg; B also replaces two unsourced constants with sourced ones. B was taken.

**What was not found:** a dynamic lateral trunk moment during the motions the axis is for — twisting to protect the body in a fall, righting from the ground. Isometric strength is a floor on capability, not a peak dynamic demand. Asymmetric-lifting biomechanics report lateral bending moments at L5/S1 rising with task asymmetry [17], but no peak figure was obtained.

## 6b. Arm payload and the two parts of `f_act` — 2026-09-26

**What was found.** The shoulder rows were sized for 30 kg in one hand at 0.70 m, the fingertip, and shoulder roll for 22 kg at the same lever, with the arm's own weight left out. 30 kg one-handed with the arm straight out is above what a strong human does; it was a stress test that had drifted into the table, and spec 02.6 described it only as "loads in the tens of kilograms at short to medium reach". The lever was also wrong in kind: a held object's weight acts at the grip centre, about 0.06 m beyond the wrist, not at the fingertip.

**Decision: 15 kg in one hand, arm straight and horizontal, load at the grip centre; shoulder roll 11 kg in the same posture abducted.** Sized at the grip centre — 0.64 m from the shoulder, 0.32 m from the elbow ([kinematics §2](../kinematics.md#2-reach-and-segment-lengths)) — with the arm's own weight added: the joint modules distal to each joint, weighed at the floor density from their own torque in the same table, plus allowances of 0.8 kg upper-arm structure, 0.6 kg forearm structure and 0.6 kg hand that are `⟦IMPL⟧` until CAD exists.

| Joint | Before | Payload now | Self-weight | Peak now |
|---|---|---|---|---|
| Shoulder pitch | 206 Nm | 94 | 15 | **109 Nm** |
| Shoulder roll | 151 Nm | 69 | 15 | **84 Nm** |
| Elbow | 112 Nm | 47 | 5 | **52 Nm** |

The total falls from 3560 to **3112 Nm**; `f_act` at 80 Nm/kg from 0.34 to **0.30**; the arithmetic would now allow a floor of 68 Nm/kg. **The floor stays at 80**: the margin is kept for D-1 on the knee, for a dynamic trunk figure above the isometric one, and for the continuous-torque question below.

**The two parts of `f_act`.** The finding of §1 that "a lighter body is worse" and its option C were argued with the whole actuator mass treated as a fraction of the body. It is not. Leg and trunk torque scales with body mass — 18.09 Nm per kilogram of body, 2352 Nm at 130 kg — so those actuators are a true fraction, `f_act_s` = 0.226 at 80 Nm/kg. Arm, wrist and neck torque is fixed by payload and geometry — 760 Nm, **9.5 kg** of actuator at 80 Nm/kg — and is non-scaling mass, which belongs in `m_ext` of the loop beside armour and sensors. `scripts/gems_budget.py` now takes the torque density and carries the split; with it the 4-hour point comes out at 129.3 kg and γ = 3.38, where the lumped model said 129.5 kg and γ = 4.5. The body mass is the same because the fixed part was hiding inside the 0.30; the growth factor is lower because the arms do not grow with the armour. Consequences, at the same operating point and 15 kg payload:

| Change | Body | Hip pitch | `f_act` |
|---|---|---|---|
| Reference of that morning, 4 h, 65% armour, 450 Wh/kg, 1.75 m | 129 kg | 227 Nm | 0.30 |
| Pack at 900 Wh/kg | 99 kg | 175 Nm | 0.32 |
| No armour, skin only | 99 kg | 175 Nm | 0.32 |
| Both | 76 kg | 134 Nm | 0.35 |
| **D-8 as decided that evening: 2 h with a dock, 65% armour, 1.65 m** | **96 kg** | **170 Nm** | **0.32** |

A lighter body lowers every leg and trunk module's torque and the peak power the pack must supply, and raises `f_act` slightly because the fixed part is divided by less body. At 30 kg payload the last row would be 0.39, outside the band: the payload decision is what lets the body get lighter. No row brings the hip under the 78 Nm of the one qualifying module, so D-2 is not settled by mass.

**Where the ceiling is, on three bases.** The density band is at the top of the market, and the market is not the ceiling:

| Tier | Figure | Basis |
|---|---|---|
| Physics | Torque is rotor volume × air-gap shear stress, and shear stress in electric machinery runs from a few kPa in small machines to about 100 kPa in very large, well-cooled ones [20]. A joint-sized motor sits at the low end; the reducer multiplies torque at the cost of its own mass | Bound, not a figure |
| Laboratory | **64.2 Nm/kg** peak — cycloidal quasi-direct drive, 89.9 Nm peak, 37.5 Nm continuous, Zhu et al. 2024 [21]; 1.40 kg by division, the paper's own mass figure not read | Peak over module mass |
| Market | **78 Nm peak, 26 Nm rated, 879 g** in the one module found at or above the floor, CubeMars AKH70-16 [22]: 78 / 0.879 = 88.7 Nm/kg, the figure the band's top rests on | Peak over module mass, as claimed |

The laboratory record is below the market claim, which is the usual sign that the two are not on the same basis: the laboratory figure is a full module with its housing, the market figure a compact planetary module at 16:1 whose 879 g the datasheet does not break down. **Resolved 2026-09-26 by the author from the specification summary of the CubeMars page**: peak torque is **78 Nm**, not the 85 Nm the search excerpts and reseller listings carried, and 78 / 0.879 = 88.74 Nm/kg exactly. The three figures are consistent, and the module is 7 Nm smaller than this document assumed until then — hip yaw, at 81 Nm, and shoulder roll, at 84 Nm, moved above it. The page's torque–speed curve at 48 VDC runs to 85 Nm, which is where the 85 figure came from; at that end the module turns at about 53 rpm and puts out about 470 W, so its **peak specific power is about 0.53 kW/kg**, against the 3–5 kW/kg spec 02.6 declares — an open finding for spec 02.7, where the actuator side of the peak-power comparison rests on that band. The module's interface is dual CAN, not EtherCAT. Price on the page: USD 598.90, recorded in the AVL as the first verified price.

**From the manufacturer's documents, read 2026-09-26** (supplied by the author; copyrighted, so cited and not vendored — [23][24][25]):

| Item | Figure | Source |
|---|---|---|
| Torque coefficient at the output, AKH70-16 | 2.8334 Nm/A; force-control ranges ±13 rad/s, ±110 Nm | [23] §4.2 |
| Torque coefficient at the output, AKH70-48 | 8.8123 Nm/A; ranges ±5 rad/s, ±280 Nm | [23] §4.2 |
| Drive board for both, AK70-4820-2D-A3 | 48 V rated, 18–52 V; **20 A rms rated, 60 A peak**; CAN 1 Mbps; −20…65 °C ambient, 100 °C board limit; 21-bit inner and 15-bit outer encoder; ≤1 W standby | [24] §1.1 |
| Envelope | Ø90 × 60.5 mm, Ø42 output boss, Ø7 through bore; housing mount 12 × M3 on Ø81; output face 6 × M4, 8 × M2.5, 4 × Ø3 dowels | [25] |
| AKH70-48 specification table, as far as the page shows it | 48:1, 21 pole pairs; **74 Nm rated at 28 rpm and 6 A DC** (≈ 217 W mechanical); back-drive torque 2.22 Nm; backlash 12 arcmin; NTC temperature sensor (MF51B103F3950); bearing ratings C 5680 N, C₀ 8680 N; 65 dB at 65 cm; 1396 g. The peak-torque, inertia, motor-constant and time-constant cells were blank in the copy read | [26], screenshot supplied by the author |
| Peak torque duration, thermal time constant | **not stated in any of the three documents, nor on the page.** A search engine's generated answer offering "under 0.5 s", "0.5–2 s" and "over 2 s" phases was seen and is not evidence: no CubeMars document read here gives those figures | — |

So 78 Nm at 2.83 Nm/A is 27.5 A, inside the board's 60 A peak, and the manual's ±110 Nm command range is the drive's limit, not the motor's rating. The thermal question of the previous paragraph stays open: the documents give rated and peak, not how long peak may be held.

**Torque density is a ratio choice.** The AKH70-48 is the same motor and drive behind a three-stage 48:1 reducer: 222 Nm peak, 74 Nm rated, 1396 g, **159 Nm/kg** [26] — 1.8 times the density this document called the top of the market, bought with output speed: ±5 rad/s against ±13 rad/s. Against the 130 kg table of that morning, at 48:1 every leg and trunk joint was covered except hip pitch and knee at 230 Nm (short by 8) and trunk pitch at 226 (short by 4); at the 96 kg reference point of D-8, decided that evening, every joint is covered, hip pitch and knee at 170 Nm with 29 kg of carry capacity to spare. What is not known is whether ~5 rad/s at the output is enough for gait and for catching a fall; that is the measurement D-2 now turns on, and the sizing table gains a speed column when it exists.

**Load cases and carry capacity.** Decision D-11 of the same day limits the declared loads to static objects and puts a held load onto the leg and trunk rows ([spec 02.6](../../spec/02-structure-and-motion.md#load-cases)). The sizing script prints the case table and the mass the legs can carry against this module's 222 Nm peak and 74 Nm rated torque; at the old 4-hour point the body alone exceeded the peak, at the 2-hour, 1.65 m reference point of D-8 29 kg is left for the hands.

**In-house design is not an option.** By the author's rule of 2026-09-26, revised 2026-11-05 ([`CLAUDE.md`](../../CLAUDE.md) §2), GEMs designs the system and buys its components: no part that performs a function the market sells — an actuator, a reducer, a drive board — may be proposed as something to build rather than buy. The "design them" branch of D-2 is withdrawn; what remains is which bought module, at which ratio, and how several combine.

**The continuous-torque gap.** Every figure in the sizing table is a peak, and the density band is peak over module mass. The rated figures are 26 of 78 Nm for the market module and 37.5 of 89.9 Nm for the laboratory one — about a third. A joint that must hold its peak for longer than the module's thermal time constant is sized by the rated figure, at roughly three times the mass. Which joints those are — the trunk holding a lift, the shoulder holding the declared 15 kg — is not decided here, and is the third reason the floor stays at 80 rather than falling to 68.

## 6c. Knee torque — D-1, 2026-11-21

**What was assumed.** The sizing table set the knee equal to hip pitch, 1.77 Nm per kilogram of body — 170 Nm at the 96 kg reference point — with no source of its own.

**What the gait data say.** Peak internal knee extension moment in healthy adults, normalised by body mass, as tabulated from the primary studies by Zhang et al. [27]:

| Task | Peak extension moment | Studies | Highest |
|---|---|---|---|
| Level walking | 0.13–0.95 Nm/kg, first stance peak | 11 | 0.95 |
| Stair ascent | 0.45–1.41 Nm/kg | 7 | 1.41 — McFadyen and Winter, 3 subjects, 22 cm riser |
| Stair descent | 0.37–1.62 Nm/kg, second stance peak | 7 | 1.62 — the same study; 1.35 at a 17 cm riser (Riener et al., 10 subjects) |
| Rising from a seat | 0.62–2.19 Nm/kg | 9 | 2.19 from one subject (Wu et al.); the other eight 0.62–1.29, and 1.14 is the highest from more than one subject |
| Running — not declared when this was checked; listed in the [motion envelope](../../spec/02-structure-and-motion.md#motion-envelope) on 2026-11-22, figures open | 1.16–2.57 Nm/kg | 5 | — |

**What it settles.** 1.77 Nm/kg covers every walking, stair and seat figure in the review but the single-subject 2.19: 9% above the highest stair figure, and 56% above the highest sit-to-stand figure measured on more than one subject. Rising from a seat is a declared task — the dock is a seat (DK-2). The figure stands, now with a source; nothing in the mass loop changes.

**What it does not settle.** No figure was obtained for rising from a deep squat or from the floor — which the knee's declared range ([kinematics §1.5](../kinematics.md#15-range-of-motion-mechanism-not-biology): 140° human, 200° mechanical) and recovery from a fall imply — nor for landing from a step or a drop; both are dynamic events. The figures are human, produced by human movement strategies, and a body that moves differently loads its knee differently. Those are why the 80 Nm/kg floor keeps its margin (§6b).

**Against human strength.** Šarabon et al. [28] pooled 411 studies of maximal isometric knee extension: adult men 2.92–3.45 Nm/kg at mid-range knee angle, adult women 2.08–2.74, older men 1.74–2.16 (pooled 95% confidence intervals). At 1.77 the knee has the strength of an older man: enough for the declared tasks, not a young adult's reserve.

**Two misreadings in [12].** Its walking knee moment, "0.46–1.27 Nm/kg", is Zhang et al.'s peak-to-peak range of the moment over the gait cycle, not a peak. Its knee extension moment of "3.0–3.4 Nm/kg … during the lift phase" of floor-to-waist lifting cites Šarabon et al., whose figures are maximal isometric strength, not a moment measured while lifting. Neither figure is used here. The hip row, which cites [12] and [13] together, was re-traced on 2026-11-22: neither carries its 100–150 Nm (§6d).

## 6d. Actuator candidates — D-2, 2026-11-22

**What D-2 turns on.** At the 96.2 kg reference point the AVL's module, CubeMars AKH70-48, covers every leg and trunk torque, but its output runs to about 5 rad/s (§6b). Torque does not settle D-2; speed does.

**What speed the knee needs.** Normative data from 36 healthy adults (Mentiplay et al. 2018, tabulated by Banky et al. [29]): mean peak knee angular velocity in swing is 219 °/s (3.8 rad/s) at 0.40–0.59 m/s and 384 °/s (6.7 rad/s) at 1.40–1.60 m/s, with ±1.96 SD at the faster speed spanning 294–474 °/s (5.1–8.3 rad/s); ankle dorsiflexion in swing reaches 214 °/s (3.7 rad/s) at that speed. The hip is slower: 2.3 rad/s, with a 97 Nm (1.3 Nm/kg) peak, for a 75 kg human walking at 1.6 m/s (Yu et al. [30], citing their own source). The knee sets the speed. Its two demands do not coincide — peak torque in stance at low speed, peak speed in swing at low torque — so a module must reach both corners of its torque–speed curve, not both at once. A simulated Unitree G1 reaches 16.6 rad/s at knee and hip pitch in fast walking [31]; the G1 is a 1.3 m robot, whose shorter leg turns faster at the same walking speed, so the figure bounds nothing for GEMs and is kept as a robot's reference only.

**Walking's top speed is declared at 1.0 m/s (2026-11-23).** The [motion envelope](../../spec/02-structure-and-motion.md#motion-envelope) of spec 02.6 lists walking as a region of cadence and step length, with running beside it; when this section was written every figure was open (2026-11-22), and the knee's speed requirement was part of D-2. At 1.0 m/s the simulated robot of §6e asked the knee for 6.7–6.9 rad/s. For human walking: 6.7 rad/s mean and 8.3 rad/s at the upper bound for ordinary walking at 1.4–1.6 m/s, 3.8 rad/s for a slow 0.5 m/s.

**The AVL's module does not reach it.** AKH70-48 at ±5 rad/s is below the mean knee swing speed of ordinary walking, in the lower tail of its spread. AKH70-16 has the speed, ±13 rad/s, and 78 of the 170 Nm.

**Candidates for hip pitch, knee and trunk pitch (170, 170 and 167 Nm).** Found through an open actuator dataset [32] — 565 module variants, a secondary source with one maintainer — and each figure below read from the manufacturer's datasheet as the dataset copies it:

| Module | Reducer | Peak / rated torque | Output speed | Mass | Nm/kg | Bus | Supply | Source |
|---|---|---|---|---|---|---|---|---|
| CubeMars AKE90-8 | planetary 8:1, quasi-direct drive | 170 / 55 Nm at 120 rpm | 210 rpm no-load = 22.0 rad/s | 1400 g | 121 | CAN | 48 V | [33] |
| MyActuator RMD-X12-P20-320 | planetary 20:1 | 320 / 85 Nm at 100 rpm | 125 rpm no-load = 13.1 rad/s | 2.4 kg | 133 | EtherCAT, CAN, RS-485 | 48 V | [34] |
| ENCOS EC-A10020-P2-24 | planetary 24:1 | 330 / 100 Nm at 115 rpm | 123 rpm peak = 12.9 rad/s | 2172–2211 g | 149–152 | CAN (CAN FD) | 48 V | [35] §7.2 |
| PHYBOT PhyArc 102 | cycloidal 25:1 | 244 / 60 Nm at 100 rpm | 124.2 rpm no-load = 13.0 rad/s | 1.0 kg | 244 | Ethernet and CAN FD, own protocol | 72 V (24–72 V) | [36] |
| CubeMars AKH70-48, the AVL's, for contrast | planetary 48:1 | 222 / 74 Nm at 28 rpm | ±5 rad/s command range | 1396 g | 159 | CAN | 48 V | [23][26] |

The speeds are on the basis each datasheet gives — no-load, peak, or command range — and are not one basis.

**What the table says.**
- Every candidate is above the 80 Nm/kg floor, so none strains the mass loop. At 1.77 Nm per kilogram of body and load, the capacity left for a load is 0 kg for AKE90-8 (170 Nm is the knee's figure exactly), about 42 kg for PhyArc 102, and 85–90 kg for the X12 and the ENCOS module.
- Rated torque is 25–33% of peak in every row, so the continuous-torque gap of §6b stands. ENCOS is the one manufacturer found that publishes temperature-rise curves ([35] §8.5 for its P1-12, §7.5–7.6 for the P2-24; read in §6e), the kind of data that gap needs.
- The reducer conflict D-2 names can be settled by a bought module either way. `hardware/mechanical` §2 asked for cycloidal reducers at hip and knee — revised on 2026-11-22 to cycloidal or planetary, not strain-wave, since its reason rules out strain-wave gears only — and cycloidal modules are on sale — PhyArc here, LeadShine's HRV2 at 120–160 Nm in the dataset with no speed given; MyActuator's own cycloidal line, CEM, stops at 45 Nm [37]. The planetary rows are what the electrical selection assumed. Only the 8:1 row keeps the backdrivability that §2 argues for the arms; the others are 20:1 to 25:1.
- Only MyActuator offers EtherCAT on the module; the others need the CAN-to-EtherCAT bridge of plan E-5. PhyArc wants 72 V and the rest 48 V, which ties the choice to D-4.

**Not yet done.** No price or availability outside China has been read for any of the four. The other joint classes — hip roll 118, ankle pitch 134, the arm joints at 50–104, the wrists at 20 and the neck at 15 Nm — are not yet matched. Peak duration is known for none but ENCOS's curves, and whether the dataset's copies of the datasheets are current is not checked. No row enters the AVL until the author picks the direction.

**Two open points of D-1, re-checked.** No figure was found for the knee moment of rising from a deep squat or the floor; it stays open. The hip row's 100–150 Nm at 70 kg is not in [12], whose hip figures are 0.5–1.0 Nm/kg in walking, nor in [13], which is qualitative and cites a 53 Nm module as its example: the 1.77 Nm/kg it scales to stands as an assumption, above the 1.3 Nm/kg of [30].

## 6e. Running and balance recovery — D-2, 2026-11-22

**Why these two.** The [motion envelope](../../spec/02-structure-and-motion.md#motion-envelope) of spec 02.6 lists running (row 5) and balance recovery (row 7) beside walking, and names them as the rows most likely to size the leg modules. This section gathers the figures for both; it declares none of them.

**Running: what the human knee and hip do.** Computed here from the public dataset of Fukuchi et al. [41] — treadmill running at 2.5, 3.5 and 4.5 m/s, 39 participants, 70.5 ± 8.9 kg, 175.8 ± 7.1 cm. Its processed curves are each participant's average over more than 30 cycles, at 101 points of the gait cycle; flexion is the angle about Z, moments are internal and per kilogram. The cycle time, which the processed curves do not carry, was taken from the treadmill's vertical force two independent ways: foot strikes at 20 N, the paper's threshold, after a 10 Hz low-pass and with 50 ms below threshold required; and the force's autocorrelation. A trial was kept only when the two agreed within 5%; 19 of 101 were not. The cadence of the trials kept, 80.5, 87.0 and 94.1 strides per minute for participants 1–28, is within 3% of the paper's own (80.8, 85.7, 91.7, as read through a summary of its Table 4). The moments of participants 36–39 are in a unit that is neither Nm/kg nor Nm and were left out.

| Speed | Trials | Cycle | Knee peak angular velocity | Hip peak angular velocity | Knee peak extension moment | Hip peak moment | Knee range |
|---|---|---|---|---|---|---|---|
| 2.5 m/s | 28 | 0.75 s | 10.9 ± 0.9 rad/s, highest 12.6 | 5.3 ± 0.7, highest 7.4 | 2.79 Nm/kg, highest 3.50 | 1.12, highest 1.46 | 84° |
| 3.5 m/s | 32 | 0.70 s | 12.7 ± 1.1, highest 15.8 | 7.3 ± 0.9, highest 10.1 | 3.08, highest 4.06 | 1.52, highest 2.03 | 97° |
| 4.5 m/s | 22 | 0.65 s | 14.1 ± 1.2, highest 16.6 | 9.4 ± 1.0, highest 11.6 | 3.28, highest 4.17 | 1.84, highest 2.38 | 106° |

Peaks taken from cycle-averaged curves are lower than the peaks of single cycles, so these are, if anything, low.

Schache et al. [39], overground at four speeds, 8 participants, 73.0 ± 8.6 kg, Table 1:

| Speed | Knee extension, midstance | Hip extension, initial stance | Hip flexion, initial swing | Ankle plantarflexion, midstance |
|---|---|---|---|---|
| 3.50 m/s | 3.12 Nm/kg | 2.02 | 1.09 | 2.94 |
| 5.02 m/s | 3.52 | 2.95 | 1.69 | 3.55 |
| 6.97 m/s | 3.59 | 3.18 | 2.59 | 3.77 |
| 8.95 m/s | 3.55 | 4.09 | 4.30 | 4.00 |

The two studies agree at the knee — 3.08 and 3.12 Nm/kg at 3.5 m/s, different people, different laboratories — and not at the hip, 1.52 against 2.02. The cycle averaging above, and treadmill against track, are two differences between them; which accounts for the gap was not checked. Above 5 m/s the knee's stance moment levels off while the hip's swing moments keep rising [39].

**What running asks of a GEMs module, at the 96.2 kg reference point.** The knee's stance moment is 268 Nm at 2.5 m/s and 296–300 Nm at 3.5 m/s, against 170 Nm at 1.77 Nm/kg — the figure the legs are sized to, set for walking, stairs and rising from a seat (§6c). Against the candidates of §6d:

- ENCOS EC-A10020-P2-24 (330 Nm, 12.9 rad/s peak) and RMD-X12-P20-320 (320 Nm, 13.1 rad/s no-load) carry the torque of running to about 3.5 m/s. Their speed covers the human knee's mean at 2.5 m/s, 10.9 rad/s, at 84% of the figure each datasheet gives, and does not cover 3.5 m/s. Those figures are peak or no-load, not speed under the load of a stride.
- AKE90-8 has the speed, 22.0 rad/s, and 170 Nm, which is walking's figure, not running's. PhyArc 102, at 244 Nm and 13.0 rad/s no-load at 72 V, falls short of running's torque.
- No candidate found covers both the torque and the speed of the human knee at 3.5 m/s.

The figures are human, and a human runner flexes the knee 84–106° in swing, which is what sets its speed. A robot can run with a straighter leg; Oli, walking at 0.5–1.25 m/s in the simulation below, used 13–42° of knee range. No figure for a running robot's knee speed was obtained.

**How long running can last.** A peak says what a joint does once; for how long it can keep doing it depends on its RMS torque over the stride against its continuous rating, since a motor heats with the square of its current. From the same dataset [41], participants 1–35, one leg, sagittal plane:

| Speed | Knee RMS moment (peak) | Hip RMS (peak) | Ankle RMS (peak) | Mean positive power, both legs | Mean absolute power, both legs |
|---|---|---|---|---|---|
| 2.5 m/s | 0.96 Nm/kg (2.81) | 0.56 (1.11) | 0.77 (2.07) | 3.9 W/kg | 8.2 W/kg |
| 3.5 m/s | 1.04 (3.12) | 0.78 (1.48) | 0.80 (2.28) | 5.6 | 11.8 |
| 4.5 m/s | 1.09 (3.31) | 0.99 (1.75) | 0.79 (2.35) | 7.9 | 16.4 |

At the 96.2 kg reference point and 2.5 m/s:
- **Heat sets the ceiling.** The knee's RMS is 92 Nm, against the continuous rating of ENCOS EC-A10020-P2-24, 100 Nm, and of RMD-X12-P20-320, 85 Nm [35][34] — at or over it, and the ratings are the datasheets' conditions, not a sealed body's (plan M-11). How long either module can hold it is read from a temperature-rise curve; for the P2-24 those are in [35] §7.5–7.6, read below.
- **Energy does not.** The legs' mechanical power is 375 W positive and 790 W in absolute value, of the order of 1 kW drawn. A human stores part of each stride in tendons, which a body without series-elastic elements does not, so the absolute figure is the closer of the two. Against the 3.9 kWh pack, a minute of running is small and an hour about a quarter of it; against the 12 kW the pack delivers at 3C ([spec 02.7](../../spec/02-structure-and-motion.md#27-peak-power-is-limited-by-the-source-not-the-actuators)), the draw is small.
- **The ankle is sized below running.** Its running peak, 2.07 Nm/kg, is 199 Nm, against the 134 Nm it is sized to at push-off in walking; Schache et al. give 2.94 Nm/kg at 3.5 m/s [39].

**Decided 2026-11-22 (Plone):** running is declared to 2.5 m/s, to keep pace with a person or leave a hazard, for 60 s at that speed and then a rest whose length waits for the thermal data; faster running is `OPEN` with its requirement; the disturbance balance recovery must withstand is a sudden change of the body's velocity of 1.0 m/s forward or backward or 0.5 m/s sideways, standing or walking ([spec 02.6](../../spec/02-structure-and-motion.md#motion-envelope)).

**Balance recovery: human.** Pijnappels et al. [40] tripped 12 young adults walking at 1.61 m/s. The recovery step was slower in time, not faster: swing 0.67 s against 0.44 s in normal walking, stride 1.83 m against 1.66 m (Table 1). The paper gives no joint angular velocity. Joint moments attributed to this paper by a search excerpt are not in it and are not used. No human figure for joint speed in a recovery step was found.

**Balance recovery: a robot.** LimX's published Oli policy [38] was run in MuJoCo, 1 ms step, on the serial-joint model of its description at commit 4c0a3c7 (52.55 kg), with its walking controller's observation, history, 100 Hz policy and 1 kHz PD reproduced from humanoid-rl-deploy-python at 592e6f0, and its torque limits; the heading was held by a yaw command, as an operator holds it. Its training configuration at humanoid-rl-isaaclab b5e8323 commands 1.0 m/s forward at most and pushes the base by setting its velocity, up to ±1.0 m/s forward and ±0.5 m/s sideways. A push of that kind was applied, and the leg peaks compared over the 2 s before and after it:

| Condition | Push | Knee | Hip pitch | Ankle pitch | Knee torque | Recovered |
|---|---|---|---|---|---|---|
| Walking 0.5 m/s, no push | — | 3.8 rad/s | — | — | 60 Nm | — |
| Walking 1.0 m/s, no push | — | 6.7–6.9 | 2.4–2.6 | 3.4–3.6 | 87–90 | — |
| Walking, command 1.39 m/s (reached 1.25) | — | 9.4–9.5 | 3.9 | 4.0 | 106 | — |
| Standing | 1.0 m/s forward | 4.8 | 3.6 | 4.8 | 73 | yes |
| Standing | 1.5 m/s forward | 6.0 | 4.6 | 7.0 | 85 | yes |
| Standing | 1.0 m/s backward | 9.4 | 4.0 | 9.1 | 133, the limit | yes |
| Standing | 1.5 m/s backward | 12.4 | 5.3 | 11.1 | 133, the limit | yes |
| Standing | 0.5 m/s to the left | 4.3 | 1.5 | 2.9 | 93 | yes |
| Standing | 0.5 m/s to the right | 0.3 | 0.2 | 0.4 | 35 | yes |
| Walking 1.0 m/s | 1.0 or 1.5 m/s forward or back, 0.5 m/s to either side | 7.2–8.2 | 2.8–4.3 | 3.3–7.2 | 94–133 | yes, all six |

A backward push from standing asked the knee for more speed than walking at 1.0 m/s did — 9.4 rad/s at the training range's edge, 12.4 rad/s beyond it — and ran its torque into the limit, so what the policy would have used without the limit is not known: 133 Nm on 52.55 kg is 2.5 Nm/kg, which at 96.2 kg is 243 Nm. Pushes while walking raised the knee's peak by 7–22% over walking alone. The hip roll joint also reached its limit.

**What this measurement is not.** It is a simulation without a motor model — no speed limit, no torque–speed curve — with ideal serial ankles in place of Oli's push-rod linkage; the full model with the linkage could not be run correctly here. LimX's own files disagree on the knee's speed limit: 5 rad/s in the URDF, 12 rad/s in the training configuration. The gait it produced is asymmetric — the two knees differ, and a push to one side drew far less response than a push to the other — for a reason not found. Oli is 52.55 kg against GEMs' 96.2 kg at the same height, so angular speeds carry over and torques do not. The figures are a robot's in simulation, not a measurement on hardware. The analysis scripts are not in this repository yet.

**What it says for D-2.**
- Balance recovery may set the knee's speed rather than walking does: in the robot, 9–12 rad/s after a backward push from standing, against 7 rad/s walking at 1.0 m/s. The disturbance GEMs must withstand (row 7) decides which.
- Running roughly doubles the knee's torque over the figure the legs are sized to, 3.1 Nm/kg against 1.77 at 3.5 m/s, and asks 11–13 rad/s of it if it runs as a human does. That changes the mass loop, not only the module.
- No bought module found meets human-like running at 3.5 m/s at both corners. ENCOS and X12 are at the edge of both at 2.5 m/s. Under [`CLAUDE.md`](../../CLAUDE.md) §2, a running speed no module meets is `OPEN` with its requirement, not a module designed here.
- Together, rows 5 and 7 ask the knee module for at least 270 Nm peak, at least 11 rad/s at about 50 Nm (12 with margin) and 92 Nm RMS for 60 s, and the ankle for about 200 Nm.

**Against the datasheets.** ENCOS EC-A10020-P2-24, measured tables at 48 V [35] §7.2–7.6:
- **Speed under load: met.** It turns at 123.6 rpm, 12.9 rad/s, at 52.6 Nm, and holds 122.9 rpm to 112 Nm; it falls to 105 rpm at 123 Nm and 55 rpm at 132.5 Nm. The swing's 11–12 rad/s at about 50 Nm is covered.
- **Peak torque: claimed, not measured.** The stall table ends at 242 Nm, at 99.6 A phase current; the 330 Nm of the parameter table is at 140 A and is not among the measured rows. Running's 268 Nm stance peak lies between the two.
- **Duration: not met.** From 30 °C to 100 °C under a constant load at 57.5 rpm, 6.0 rad/s — near the knee's mean speed in running at 2.5 m/s, 5.2 rad/s, computed from [41] — the module takes 5′19″ at 60 Nm, 1′54″ at 70 Nm, 56″ at 80 Nm and 46″ at 85 Nm (§7.6). The knee's 92 Nm RMS is beyond the last row, so it reaches 100 °C in under 46 s, short of the 60 s row 5 declares. 60 s needs somewhat below 80 Nm RMS, which at 0.96 Nm/kg is a body under about 83 kg. At stall, with no speed, the same module takes 12′00″ at 90 Nm and 4′14″ at 100 Nm (§7.5): its rated 100 Nm is not a torque it holds for minutes. 100 °C is the test's end point, not a winding limit the manual states; the tests start at 30 °C, which a motor that has been walking is above; ambient and mounting are not stated.

RMD-X12-P20-320 [34] gives a stall table only — 150, 200, 250 and 300 Nm raise its temperature 13, 5, 7 and 43 °C in 10, 8, 7 and 3 s, not a monotonic series — and no load–speed or sustained data; its insulation is class F. Whether it holds 92 Nm for 60 s cannot be judged from it.

**The mass loop with running's figures — computed, not applied.** With the knee at 2.79 Nm/kg and ankle pitch at 2.07 in place of 1.77 and 1.40, `scripts/gems_budget.py` still converges, Sf 0.615 to 0.657, but the body goes from 96.2 to 108.0 kg: actuators 31.0 to 38.2 kg, `f_act` 0.32 to 0.35, the top of [spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients)'s band, γ 2.60 to 2.92, pack 3.85 to 4.32 kWh, endurance ceiling 10.7 to 9.7 h. At 108 kg the knee asks 301 Nm peak and 104 Nm RMS, so the loop feeds back into the module it was meant to size. The loop weighs actuators at the declared 80 Nm/kg ([spec 02.6](../../spec/02-structure-and-motion.md#26-actuation-and-manipulation)), while the candidates are 133–152 Nm/kg; the mass it adds is the declared basis's, not the candidates'. The sizing table is unchanged until the author decides.

## 7. References

| # | Source |
|---|---|
| 1 | [CubeMars — humanoid robot motors](https://www.cubemars.com/categorys/humanoid-robot-motor) |
| 2 | [Quasi-Direct Drive Joints: The Engineering Sweet Spot for Humanoid Robots](https://zanerobotics.substack.com/p/quasi-direct-drive-joints-the-engineering) |
| 3 | [Humanoid Robot Actuator Torque Density (Nm/kg): 2026 Engineering Guide](https://robotics.zhinno.com/blog/humanoid-robot-actuator-torque-density.html) |
| 4 | [Amprius Technologies — product catalogue](https://amprius.com/documents/Amprius_Product_Catalog.pdf) |
| 5 | [SOLiTHOR — energy density milestone](https://www.solithor.com/en/news/1259/press-releases/solithor-achieves-key-energy-density-milestone-while-further-validating-alternative-pathway-to-manufacture-scalable-solid-state-batteries) |
| 6 | [Solid-State Batteries 2026: How the Technology Is Finally Reaching Commercial Use](https://to7motor.com/solid-state-batteries-2026-commercial-reality) |
| 7 | [High C-Rate or High Energy Density? Robot Battery Insights](https://www.grepow.com/blog/high-c-rate-vs-high-energy-density-robot-battery-insights-wrc-2026.html) |
| 8 | [NVIDIA Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/) |
| 9 | [Jetson module comparison, Orin to AGX Thor](https://www.forecr.io/blogs/embedded-systems/nvidia-jetson-comparison) |
| 10 | [An EtherCAT-Based Real-Time Control System Architecture for Humanoid Robots](https://mediatum.ub.tum.de/doc/1394924/0185778354196.pdf) |
| 11 | [CAN vs EtherCAT vs RS-485 vs UART for robot motors and actuators](https://openelab.io/blogs/learn/can-vs-ethercat-vs-rs-485-vs-uart-for-robot-motors-and-actuators) |

Joint torque requirements used by the sizing script: ankle peak 1.4 Nm/kg at push-off and 2.5–3.5 W/kg push-off power from normative gait data; hip 100–150 Nm peak for a 70 kg humanoid during stair climbing and squat rise, scaled by mass — a figure attributed here to [12][13], which on re-reading neither gives (§6d): it stands as an assumption, above the 1.3 Nm/kg a walking human's hip reaches [30]. Knee was assumed equal to hip pitch; on 2026-11-21 that figure was checked against published gait data (D-1) and stands for the declared tasks — walking, stairs, rising from a seat — with what it does not cover stated in [§6c](#6c-knee-torque--d-1-2026-11-21) [27][28].

| # | Source |
|---|---|
| 12 | [Human-Level Actuation for Humanoids](https://arxiv.org/html/2511.06796) |
| 13 | [Selection guide for humanoid robot knee and hip joint motors](https://www.cubemars.com/how-to-choose-hip-and-knee-joint-motors-for-humanoid-robots.html) |
| 14 | Pan F., Cheng J., Kong C., Wang W., Lu S., [Sex-specific characteristics of the trunk muscle behaviors in an asymptomatic adult cohort](https://doi.org/10.1186/s40001-025-02742-w), *European Journal of Medical Research* 30:471, 2025 — open access, CC BY-NC-ND 4.0; not vendored |
| 15 | [A 3-DOF coupled tendon-driven humanoid waist](https://www.tandfonline.com/doi/abs/10.1080/01691864.2023.2289134), *Advanced Robotics* 37(23), 2023 |
| 16 | [Unitree G1 description, `g1_29dof.urdf`](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description) — joint `<limit effort>` values read on 2026-09-26 |
| 17 | [The effects of lifting speed on the peak external forward bending, lateral bending, and twisting spine moments](https://www.tandfonline.com/doi/abs/10.1080/001401399185838), *Ergonomics* 42(1) |
| 19 | Wang Y., Chen P., Togo S., Yokoi H., Jiang Y., [A novel gravity compensation mechanism for orthogonal DoFs with coupled springs](https://doi.org/10.1016/j.mechmachtheory.2025.106220), *Mechanism and Machine Theory* 216:106220, 2025 — open access, CC BY-NC 4.0; not vendored. Table 1 restates the waist of [15]; §3.1 reports the wire-slack accuracy loss under load |
| 18 | Ali A. R., Abdullah H. S., [Development of a compliant spine mechanism for enhanced humanoid robotics locomotion](https://doi.org/10.1038/s41598-025-32165-w), *Scientific Reports* 15:44646, 2025 — open access, CC BY 4.0; copy in [`sources/`](sources/ali-2025-flexinoid-tensegrity-spine-sci-rep-15-44646.pdf) |
| 20 | MIT course notes, *Electric Machines: Electromagnetic Forces* — the shear-stress range and torque ∝ rotor volume × shear stress; quoted from search excerpts, the [copy found](https://www.scribd.com/document/62980862/MIT-Electric-Machines) was not readable from this environment |
| 21 | Zhu A., Tanaka Y., Rafeedi F., Hong D., [Cycloidal Quasi-Direct Drive Actuator Designs with Learning-based Torque Estimation for Legged Robotics](https://arxiv.org/abs/2410.16591), arXiv:2410.16591, 2024 — torque density up to 64.2 Nm/kg, 37.5 Nm continuous, 89.9 Nm peak; figures from the abstract as excerpted by search, the page not readable from this environment |
| 23 | CubeMars, *AK Series Product Manual V3.2.0 for AK 3.0 Robotic Actuator*, 2026-01-17 — §4.2 motor parameter table (KV, torque coefficient, speed and torque ranges), fault codes, CAN protocol; copyrighted, not vendored |
| 24 | CubeMars, *AK70-4820-2D-A3 Driver Manual V1.0.0*, 2026-04-29 — §1.1 driver specifications; copyrighted, not vendored |
| 25 | CubeMars, *AKH70-16 V1.0 KV41 Hollow Shaft Planetary Actuator 2D Drawing*, 2026-05-19 — proprietary, not vendored |
| 26 | [CubeMars AKH70-48 V1.0 KV41 hollow-shaft planetary actuator](https://www.cubemars.com/product/akh70-48-v-1-0-kv41-hollow-shaft-planetary-actuator.html) — 222 Nm peak, 74 Nm rated, 1396 g, 159 Nm/kg, 48:1 three-stage; from search excerpts of the page and reseller listings, the page not readable from this environment |
| 22 | [CubeMars AKH70-16 V1.0 KV41 hollow-shaft planetary actuator](https://www.cubemars.com/product/akh70-16-v-1-0-kv41-hollow-shaft-planetary-actuator.html) — Φ90 × 60.5 mm, 879 g, 7 mm bore, 26 Nm rated, **78 Nm peak**, 105 rpm no-load, 16:1, dual 21-bit encoders; from the specification summary of the product page as read by the author on 2026-09-26, the page itself not readable from this environment. Search excerpts and reseller listings quote 85 Nm peak; the 78 Nm figure is the one consistent with 879 g and 88.74 Nm/kg |
| 27 | Zhang L., Liu G., Han B., Wang Z., Yan Y., Ma J., Wei P., [Knee Joint Biomechanics in Physiological Conditions and How Pathologies Can Affect It: A Systematic Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7160724/), *Applied Bionics and Biomechanics* 2020:7451683 — knee moment tables for walking, running, stairs and sit-to-stand |
| 28 | Šarabon N., Kozinc Ž., Perman M., [Establishing Reference Values for Isometric Knee Extension and Flexion Strength](https://doi.org/10.3389/fphys.2021.767941), *Frontiers in Physiology*, 2021 — meta-analysis, 411 studies, 13,893 participants |
| 29 | Banky M., Clark R.A., Mentiplay B.F., Olver J.H., Williams G., [Clinical spasticity assessment using the Modified Tardieu Scale does not reflect joint angular velocity or range of motion during walking](https://doi.org/10.2340/16501977-2777), *Journal of Rehabilitation Medicine* 53(1):jrm00137, 2021 — Table II, normative peak joint angular velocities by walking speed from Mentiplay et al., [Lower limb angular velocity during walking at various speeds](https://doi.org/10.1016/j.gaitpost.2018.06.162), *Gait & Posture*, 2018 |
| 30 | Yu S., Huang T.-H., Yang X., et al., [Quasi-Direct Drive Actuation for a Lightweight Hip Exoskeleton with High Backdrivability and High Bandwidth](https://arxiv.org/abs/2004.00467), 2020 — §I, hip peak torque and speed for a 75 kg human at 1.6 m/s, citing its reference [27] |
| 31 | Huang X., Dong J., Zhao H., [Task-Oriented Co-Design and Optimization of Geared Actuators for Robotic Applications](https://arxiv.org/abs/2609.22795), 2026 — §II-A, knee and hip-pitch torque–speed points of a simulated Unitree G1; a robot, not a human |
| 32 | [Dynamic Robot Joint Actuator Comparison](https://zj-motor.github.io/dynamic-robot-joint-actuators/), open dataset, [repository](https://github.com/zj-motor/dynamic-robot-joint-actuators) at commit b568703 (2026-08-04) — 565 variants with copies of manufacturers' datasheets; secondary, used to find candidates, not as their figures' source |
| 33 | CubeMars product datasheet, AKE90-8 page — the copy in [32], `datasheets/25_酷德Cubemars.pdf` |
| 34 | MyActuator, XV4 planetary module datasheet, 2026-04-16, RMD-X12-P20-320 table — the copy in [32], `datasheets/12_脉塔_XV4行星模组_260416.pdf` |
| 35 | ENCOS (Nanjing), motor data manual V3.13, §7 EC-A10020-P2-24 and §8 EC-A10020-P1-12 — the copy in [32], `datasheets/20_因克斯_ENCOS电机数据手册_V3.13.pdf` |
| 36 | PHYBOT, PhyArc series parameter sheet — the copy in [32], `datasheets/5_动易_PhyArc模组.png` |
| 37 | MyActuator, CEM cycloidal module datasheet, 2025-09-28 — the copy in [32], `datasheets/12_脉塔_CEM摆线模组_250928.pdf` |
| 38 | LimX Dynamics, Oli (HU_D04): [humanoid-description](https://github.com/limxdynamics/humanoid-description) at 4c0a3c7, [humanoid-rl-deploy-python](https://github.com/limxdynamics/humanoid-rl-deploy-python) at 592e6f0, [humanoid-rl-isaaclab](https://github.com/limxdynamics/humanoid-rl-isaaclab) at b5e8323 — Apache-2.0; model, published walking policy, training configuration; simulated here, not vendored |
| 39 | Schache A.G., Blanch P.D., Dorn T.W., Brown N.A.T., Rosemond D., Pandy M.G., [Effect of running speed on lower limb joint kinetics](https://doi.org/10.1249/MSS.0b013e3182084929), *Medicine & Science in Sports & Exercise* 43(7):1260–1271, 2011 — Table 1; copyrighted, not vendored |
| 40 | Pijnappels M., Bobbert M.F., van Dieën J.H., [Contribution of the support limb in control of angular momentum after tripping](https://doi.org/10.1016/j.jbiomech.2004.02.038), *Journal of Biomechanics* 37:1811–1818, 2004 — Table 1; not vendored |
| 41 | Fukuchi R.K., Fukuchi C.A., Duarte M., [A public dataset of running biomechanics and the effects of running speed on lower extremity kinematics and kinetics](https://doi.org/10.7717/peerj.3298), *PeerJ* 5:e3298, 2017; data [10.6084/m9.figshare.4543435](https://doi.org/10.6084/m9.figshare.4543435), version 5, CC BY 4.0 — processed and force files, checked against their MD5; not vendored |
