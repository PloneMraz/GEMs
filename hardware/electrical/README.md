# Electrical

Component selection against the specification. Every figure below is sourced; §7 lists the references.

| File | Contents |
|---|---|
| [`actuator_sizing.py`](actuator_sizing.py) | Sizes every joint from its peak torque and reports the resulting `f_act` |

---

## 1. The actuator finding — raised, and resolved

> **Resolved by option A on 2026-09-22.** The specification then declared **75–90 Nm/kg peak, on a peak-torque-over-module-mass basis**, and states the basis explicitly. **Revised 2026-09-26 to 80–90 Nm/kg** when the trunk was re-sized from measured human strength and gained a lateral-bend axis (§6a). **The arm payload came down to 15 kg the same day (§6b)**, which took `f_act` at 80 Nm/kg from 0.34 to 0.30; the floor stayed at 80. **Revised again 2026-11-23**, when the knee and ankle were sized to running (§6e): 133 Nm/kg for legs and trunk, the figure of RMD-X12-P20-320, and 80 for arms, wrists and neck ([spec 02.6](../../spec/02-structure-and-motion.md#the-basis-matters-as-much-as-the-number)). **Replaced the same day by a module declared at each joint** (§6f): the densities are now derived from the bought modules, 110 and 58 Nm/kg at 98.2 kg, 100 and 58 at 105.6 kg when walking's RMS and the hip's frontal plane entered the check (§6g), and 97 and 59 at 107.0 kg since static holds did (§6k). `spec/` and this document agree again; the record below is kept because the reasoning is what justifies a figure at the top of the commercial band. Note that the §1 tables below were computed with the whole of `f_act` treated as scaling with body mass; §6b explains why only the leg and trunk part does.

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

**75–90 Nm/kg peak, over module mass — 80–90 since 2026-09-26; on 2026-11-23, 133 for legs and trunk and 80 for arms, wrists and neck; since the same day no density, a bought module at each joint (§6f), which gives 110 and 58, then 100 and 58 (§6g).** Only a handful of commercial modules reach it — the hollow-shaft planetary at 88.7 Nm/kg is at the very top of what is claimed, and a mainstream 52 Nm/kg module does not qualify. Supply is thin and will stay thin.

**The specification now states the basis**, which is the part that actually prevents a repeat. The original error was not only a wrong number: 30–36 Nm/kg is a reasonable figure *on the integrated basis*, and it was being used as if it were peak-over-module. A density with no basis attached is a number waiting to be misread.

**The two bands are now one constraint.** 80–90 Nm/kg mapped onto `f_act` 0.30–0.34 then; at the densities declared on 2026-11-23 `f_act` was 0.27 at 82 kg, and with the bought modules of §6f it was 0.33 at 98.2 kg, 0.35 at 105.6 kg with §6g's checks and 0.351 at 107.0 kg with §6k's, the band's top raised to 0.36 the same day ([spec 02.6](../../spec/02-structure-and-motion.md#what-the-two-figures-give)), each derivable from the other, and `scripts/gems_budget.py --check` holds them together — including the actuator-mass column, which it did not cover before and which is exactly where this drift hid.

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

**Since 2026-11-23** a bought module is declared at each joint (§6f, spec 02.6) and the reference point is 107.0 kg (§6k), 105.6 kg before static holds entered the check (§6g), 98.2 kg before walking's RMS entered the check; earlier that day the legs and trunk were declared at 133 Nm/kg, the X12's figure, at 82.3 kg. The torques in this section are at the 96.2 kg point of its date: AKE90-8 at 121 Nm/kg falls below the declaration; ENCOS, PhyArc and the AKH70-48 are above it.

**The direction, picked 2026-11-23 (Plone), and superseded the same day by §6f,** which keeps the P2-24 only at the ankle pitch and as an alternate elsewhere. ENCOS EC-A10020-P2-24 is the main candidate for hip pitch, knee and trunk pitch, with the RMD-X12-P20-320 and PhyArc 102 as alternates, ranked in that order in the [AVL](../bom/avl.csv); the AKH70-48 rows at those three joints are dropped, since at ±5 rad/s it does not reach the knee's 6.7–6.9 rad/s in walking at 1.0 m/s. None is procured, and no price or availability outside China has been read. The three modules' keep-outs, Φ124 × 85 mm on each joint's axis, are in the [CAD skeleton](../mechanical/skeleton/) (plan M-1).

**PhyArc 102 at 48 V.** Its sheet [36] gives 72 V as the rated voltage and 24–72 V as the supply range, and every speed at the rated voltage; it has no figure at 48 V. Scaled by voltage, as a motor's no-load speed scales with its back-EMF, 124.2 rpm becomes about 83 rpm, 8.7 rad/s — an estimate, not the manufacturer's: above the knee's speed in walking at 1.0 m/s, below the 11–12 rad/s of running. On a 48 V bus it is not a knee module for running; it stays an alternate for a 72 V bus (D-4).

**The other joint classes, matched (2026-11-23).** Each joint's torque at the 82 kg point of `actuator_sizing.py`, against the reducer class of [mechanical §2](../mechanical/README.md#2-reducers-by-joint-class) — legs and trunk not strain-wave, shoulder and elbow QDD planetary 6:1–15:1, wrist and neck harmonic — at 48 V, with the knee at 11 rad/s or more for running (§6e), hip pitch at 7.4 rad/s or more (the hip's highest in running at 2.5 m/s, §6e) and ankle pitch at 3.7 rad/s or more (walking, above; no figure for running). The lightest module that meets each, among the 565 of the dataset [32], against the mass the declared density allows at that joint. ENCOS's figures were read from its manual [35]; the other makers' are the dataset's, and only SEmotor's were checked against its sheet:

| Joint | Needs | Allowed at 133 or 80 Nm/kg | Lightest ENCOS | Lightest of any maker |
|---|---|---|---|---|
| hip pitch ×2 | 145 Nm | 1.09 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | SEmotor SETZ70CI-1GA, 156 Nm, 0.90 kg |
| hip roll ×2 | 101 Nm | 0.76 kg | EC-A6416-P2-25, 120 Nm, 0.81 kg | SEmotor SEAF70A16NG02, 104 Nm, 0.80 kg |
| hip yaw ×2 | 51 Nm | 0.38 kg | EC-A4315-P2-36, 75 Nm, 0.48 kg | the same |
| knee ×2 | 229 Nm | 1.72 kg | EC-A10020-P2-24, 330 Nm, 2.19 kg | the same |
| ankle pitch ×2 | 170 Nm | 1.28 kg | EC-A10020-P2-24, 330 Nm, 2.19 kg | SEmotor SETZ70CI-1HA, 227.5 Nm, 1.05 kg |
| ankle roll ×2 | 44 Nm | 0.33 kg | EC-A4315-P2-36, 75 Nm, 0.48 kg | the same |
| trunk pitch | 143 Nm | 1.07 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | SEmotor SETZ70CI-1GA, 156 Nm, 0.90 kg |
| trunk roll | 78 Nm | 0.59 kg | EC-A6416-P2-25, 120 Nm, 0.81 kg | DAMIAO DM-J6248P-2EC, 97 Nm, 0.63 kg |
| trunk yaw | 61 Nm | 0.46 kg | EC-A4315-P2-36, 75 Nm, 0.48 kg | the same |
| shoulder pitch ×2 | 104 Nm | 1.30 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | Motorevo RR-PA-100-2012, 151 Nm, 1.26 kg |
| shoulder roll ×2 | 80 Nm | 1.00 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | HCFA Hu-GRS090N, 90 Nm, 0.93 kg |
| shoulder yaw ×2 | 60 Nm | 0.75 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | Motorevo RR-PA-100-1010, 63 Nm, 0.90 kg |
| elbow ×2 | 50 Nm | 0.62 kg | EC-A10020-P1-12, 150 Nm, 1.37 kg | SEmotor SETZ70CI-1DA, 58.5 Nm, 0.70 kg |
| wrist ×6 | 20 Nm | 0.25 kg | EC-A3814-H14-107, 60 Nm, 0.43 kg | Xynova HR100-43-20, 20 Nm, 0.24 kg |
| neck ×2 | 15 Nm | 0.19 kg | EC-A3814-H14-107, 60 Nm, 0.43 kg | Xynova HR100-43-20, 20 Nm, 0.24 kg |
| **31 joints** | | **22.5 kg** | **32.2 kg** | **23.3 kg** |

**What the match says: the declared density is a module's, not the joints'.** 133 Nm/kg is the X12's own peak over its own mass; the loop turns it into a mass at each joint as torque over density, as if a module came in every size at that density. Bought modules come in steps, and a joint's module carries the torque of the next step up: the knee's 229 Nm is carried by a 330 Nm module, so the knee is 2.19 kg where the loop allows 1.72. No ENCOS module is inside its joint's allowance at any joint. Of any maker, only SEmotor's are, at hip pitch, trunk pitch and ankle pitch — the least checked modules of the table, below — and the five smaller leg and trunk joints, hip roll and yaw, ankle roll, trunk roll and yaw, have none: their lightest modules are 5–46% over. At 80 Nm/kg the arms are inside at shoulder pitch, shoulder roll and the wrists, and over at shoulder yaw, the elbow and the neck. With bought modules in place of the declared density, and the loop run again until the modules and the body agree:

| Modules | Body | Actuators | `f_act` | Pack | Knee RMS in running |
|---|---|---|---|---|---|
| Declared densities (spec 02.6) | 82.3 kg | 22.5 kg | 0.27 | 3.29 kWh | 79 Nm |
| ENCOS at the knee, the lightest of any maker elsewhere | 83.7 kg | 23.3 kg | 0.28 | 3.35 kWh | 80 Nm |
| ENCOS P2-24 at hip pitch, knee and trunk pitch, as picked; the lightest of any maker elsewhere | 90.0 kg | 27.2 kg | 0.30 | 3.60 kWh | 86 Nm |
| ENCOS at every joint | 103.2 kg | 35.3 kg | 0.34 | 4.13 kWh | 99 Nm |

Every row converges and stays inside the `f_act` band of spec 02.2. The knee's RMS is 0.96 Nm/kg of body (§6e); ENCOS's bench takes 80 Nm from 30 to 100 °C in 56 s and 85 Nm in 46 s at 6.0 rad/s, so running's 60 s is short again in every row but the declared one: by about 4 s at 83.7 kg, by more at 90 kg, and at 103 kg far beyond the bench's last row.

**The lightest row is the least checked.** Its hip pitch, trunk pitch and ankle modules are SEmotor's SETZ70CI series, whose sheet ([32], `datasheets/24_小象SEmotor.pdf`) gives a continuous stall torque of 24 Nm against the 156 Nm peak of the -1GA and 35 Nm against 227.5 Nm for the -1HA, and limits the peak to 1 s or less (its note 3). That a 1 s peak at 15% continuous serves a hip in gait has not been checked; the dataset carries neither figure. The DAMIAO, Motorevo, HCFA and Xynova figures are the dataset's alone, and the Xynova wrist module meets 20 Nm with no margin. Only ENCOS publishes the temperature-rise curves that a duration needs.

**Closed the same day (§6f).** The author chose to declare the module at each joint rather than a density (Plone, 2026-11-23). The lightest rows of the table above did not survive their sheets: the dataset's figures are not the makers', and the makers' sheets say less than the dataset implies. §6f reads them, sets the rule a module must pass, and gives the set the loop now carries.

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

**The mass loop with running's figures — applied 2026-11-23, at the declared densities, and superseded the same day by the bought modules of §6f (98.2 kg).** With the knee at 2.79 Nm/kg and ankle pitch at 2.07, and the legs and trunk declared at 133 Nm/kg — the lower of the two modules that carry running's knee — with arms, wrists and neck at 80, the body is **82.3 kg**: actuators 22.5 kg, `f_act` 0.27, γ 2.22, pack 3.29 kWh, endurance ceiling 12.1 h. At 82.3 kg the knee asks 229 Nm peak and 79 Nm RMS, and ENCOS's bench takes 80 Nm from 30 to 100 °C at 6.0 rad/s in 56 s and 75 Nm in 78 s, so row 5's 60 s is at the edge rather than short; a sealed body is not the bench (plan M-11). What follows is the computation of 2026-11-22, kept as it was: with every joint at the then-declared 80 Nm/kg, `scripts/gems_budget.py` still converges, Sf 0.615 to 0.657, but the body goes from 96.2 to 108.0 kg: actuators 31.0 to 38.2 kg, `f_act` 0.32 to 0.35, the top of [spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients)'s band, γ 2.60 to 2.92, pack 3.85 to 4.32 kWh, endurance ceiling 10.7 to 9.7 h. At 108 kg the knee asks 301 Nm peak and 104 Nm RMS, so the loop feeds back into the module it was meant to size. The loop weighs actuators at the declared 80 Nm/kg ([spec 02.6](../../spec/02-structure-and-motion.md#26-actuation-and-manipulation)), while the candidates are 133–152 Nm/kg; the mass it adds is the declared basis's, not the candidates'. That is why the declaration was revised before the figures were applied.

## 6f. Modules declared at the joint — D-2, 2026-11-23

**Decided 2026-11-23 (Plone).** The actuator mass is declared at the joint, as the bought module that serves it, not as one torque density for a class of joints — the third of the ways §6d named for closing the gap between the declaration and the bought modules. With it, the rule below for which module the loop carries.

**The rank-1 rule.** A module is ranked first for a joint only if its maker's sheet gives all four: the peak torque and how long it is held — a stated limit, or a stall or constant-load temperature-rise table; a continuous torque; the speed at 48 V; the mass and the size. A module whose sheet lacks one of them, or whose figures come only from the dataset [32], can be an alternate, not the module the loop carries.

**Then it must meet its joint at the reference point**, as `actuator_sizing.py` checks: its peak at least the joint's torque; the reducer class of [mechanical §2](../mechanical/README.md#2-reducers-by-joint-class); at least 105 rpm at the knee, 71 at hip pitch and 35 at ankle pitch (§6e); and, at the three joints with a running figure — knee 0.96, hip pitch 0.56, ankle pitch 0.77 Nm/kg RMS (§6e) — that RMS for row 5's 60 s, against the torque the sheet's constant-load test holds for 60 s where it has one, interpolated between its rows, and against the continuous torque where it has none. The lightest module that passes is taken; between two of one mass, the higher peak.

**The sheets read**, each in full, from the dataset's `datasheets/` at commit b568703 [32]:

| Maker | Sheet | What it gives | Rule |
|---|---|---|---|
| ENCOS | `20_因克斯_ENCOS电机数据手册_V3.13.pdf` [35] | peak and rated torque, peak speed at 48 V, mass, size; for every module a stall and a constant-load temperature-rise table, 30 to 100 °C | passes |
| SEmotor | `24_小象SEmotor.pdf` | peak torque, held 1 s or less (its note 3); continuous stall torque; rated and maximum speed at 48 V; mass without leads, size; separate tables with its own drive (CI) and an Elmo drive | passes |
| MyActuator | `12_脉塔_XV4行星模组_260416.pdf` [34] | peak and rated torque, a stall temperature table, speed, mass (the X12, §6d) | passes |
| CubeMars | `25_酷德Cubemars.pdf` | peak and rated torque, no-load and rated speed, mass, size | no hold time |
| DAMIAO | `4_达妙_关节电机_20250630.pdf` | rated and peak torque, rated and no-load speed (J6248P: one figure, on a 24 V supply that takes 24–48 V), curves of efficiency and speed | no hold time |
| Motorevo | `13_泉智博_Motorevo机器人关节.pdf`, scanned | continuous and maximum output torque, mass, size, KV; "deeper parameters on request" | no output speed, no hold time |
| HCFA | `7_禾川_HuGRS模组.png` | rated and peak torque, rated and peak speed at 48 V, mass, size | no hold time |
| LeadShine | `9_雷赛_人形关节模组_202507.pdf`, scanned | rated torque, start-stop peak, rated speed at half the rated torque, 48 V | no hold time |
| Xynova | `17_曦诺未来_行星关节模组.png`, `…谐波关节模组.png` | peak and rated torque, 45 r/min no-load at 48 V, mass, size | no hold time |
| WEDALI | `16_伟达立_谐波关节模组.pdf` | rated, maximum average-load and peak torque, rated and peak speed, mass, size | no hold time |
| TC Drive | `15_同川精密_机器人关节模组_20250921 .pdf` | rated torque at 2000 rpm input, average-load and start-stop limits, peak, output speed | no hold time |
| Astrall | `18_璇玑动力_Astrall轴向磁通模组.png` | rated, maximum ±10%, no-load and rated speed, mass ±0.1 kg | no size, no hold time |
| ZDL (智动力) | `21_智动力_关节模组.docx` | rated torque, maximum acceleration torque, rated and no-load speed, size, mass; EtherCAT | no hold time |
| PHYBOT | `5_动易_PhyArc模组.png` [36] | its figures at 72 V | no speed at 48 V |

**What the sheets changed.** SEmotor's peak is a 1 s figure, and its continuous torque is 15–25% of it in the modules read here: the -1GA's 156 Nm over 24, the -1DA's 58.5 over 9. ENCOS's rated torque is not what a module holds under load: the EC-A6416-P2-25, rated 40 Nm, holds 30 Nm for 1′11″ and 35 for 34″ at 50 rpm; the EC-A10020-P2-24, rated 100, holds about 79 Nm for 60 s at 57.5 rpm. And one module read for this changes the knee: ENCOS EC-A13715-P1-12.67 — 320 Nm peak, 110 Nm rated, 135 rpm peak, 2695 g, Φ170 × 73 mm, 12.67:1 — holds 90 Nm for 7′21″, 100 for 5′01″ and 150 for 60 s at 59.5 rpm (manual §9.6), so it meets row 5's 60 s at the knee where the P2-24 does not.

**The set, at the 98.2 kg reference point** — superseded the same day by [§6g](#6g-walking-rms-and-the-frontal-plane--d-2-2026-11-23) at hip pitch, hip roll, ankle pitch and trunk yaw, and kept here as the step it was:

| Joint | Needs | Module | Peak / continuous | 60 s under load | Speed at 48 V | Mass |
|---|---|---|---|---|---|---|
| hip pitch ×2 | 174 Nm, 55 Nm RMS | SEmotor SETZ90CI-1FG | 240 / 60 Nm | — | 86.5 rpm | 1.60 kg |
| hip roll ×2 | 121 Nm | SEmotor SETZ70CI-1GA | 156 / 24 Nm | — | 116.5 rpm | 0.90 kg |
| hip yaw ×2 | 61 Nm | ENCOS EC-A4315-P2-36 | 75 / 25 Nm | 28 Nm | 117 rpm | 0.485 kg |
| knee ×2 | 274 Nm, 94 Nm RMS | ENCOS EC-A13715-P1-12.67 | 320 / 110 Nm | 150 Nm | 135 rpm | 2.695 kg |
| ankle pitch ×2 | 203 Nm, 76 Nm RMS | ENCOS EC-A10020-P2-24 | 330 / 100 Nm | 79 Nm | 123 rpm | 2.211 kg |
| ankle roll ×2 | 53 Nm | ENCOS EC-A4315-P2-36 | 75 / 25 Nm | 28 Nm | 117 rpm | 0.485 kg |
| trunk pitch | 171 Nm | SEmotor SETZ70CI-1HA | 227.5 / 35 Nm | — | 80 rpm | 1.05 kg |
| trunk roll | 93 Nm | SEmotor SEAF70A16NG02 | 104 / 16 Nm | — | 175 rpm | 0.80 kg |
| trunk yaw | 73 Nm | ENCOS EC-A4315-P2-36 | 75 / 25 Nm | 28 Nm | 117 rpm | 0.485 kg |
| shoulder pitch, roll, yaw ×2 | 108, 84, 60 Nm | ENCOS EC-A10020-P1-12 | 150 / 50 Nm | 55 Nm | 140 rpm | 1.373 kg |
| elbow ×2 | 51 Nm | SEmotor SETZ70CI-1DA | 58.5 / 9 Nm | — | 311 rpm | 0.70 kg |
| wrist ×6, neck ×2 | 20, 15 Nm | ENCOS EC-A3814-H14-107 | 60 / 20 Nm | — | 52 rpm | 0.434 kg |

The loop converged on **98.2 kg** from any start between 82 and 120 kg: modules 32.2 kg — 19.1 for legs and trunk, 13.1 for arms, wrists and neck — `f_act` 0.33, γ 2.40, pack 3.93 kWh, endurance ceiling 11.4 h. Peak over module mass comes out at 110 Nm/kg for legs and trunk and 58 for the rest, against the 133 and 80 declared earlier the same day. The set held to 101.4 kg of body, where trunk yaw's 75 Nm runs out, and ankle pitch's 60 s at 102.7 kg. Against the rows of §6d: with the continuous torque in place of the 60 s figure, the knee keeps the P2-24 and the body is 96.3 kg, but running's 60 s is short at the knee on its own bench; with the dataset's figures and no rule it was 83.7–90.0 kg.

**At the 4-hour point** the same rules take the P2-24 at hip pitch, the EC-A13715 at ankle pitch and, at the knee, the EC-A13720-P1-11.4 — 400 Nm peak, 120 Nm rated, 139 rpm peak, 3160 g, Φ170 × 84.5 mm, about 170 Nm for 60 s at 63 rpm (manual §10.6): the body is 122.7 kg, `f_act` 0.30, pack 9.8 kWh — corrected 2026-11-23: 4.91 kWh was written here, the 2-hour pack of that body, not the 4-hour one. `scripts/gems_budget.py` carries the 2-hour set's densities to every point and gives 125 kg there; spec 02.6 and 02.7 say which figure is which.

**What is not checked.**
- Static holds. The elbow's SEmotor holds 9 Nm continuously against the 51 Nm of the static payload of spec 02.6; trunk pitch's 35 Nm against a 171 Nm sized from human isometric strength; the shoulder's EC-A10020-P1-12 has a stall table that ends at 61.5 Nm for 5′18″, against 108 Nm. How long a static load is held is not declared (the motion envelope's held postures), and those picks stand on it. Declared, and both picks changed, on 2026-11-24 ([§6k](#6k-static-holds--d-2-2026-11-24)).
- RMS in walking, and at every joint other than knee, hip pitch and ankle pitch: no figure. Closed the same day by §6g.
- The sheets' conditions are a bench's: the ENCOS tests start at 30 °C and state no ambient or mounting; a sealed body is not the bench (plan M-11). SEmotor's figures are with its own drive.
- The bus: ENCOS is CAN and CAN FD, ZDL EtherCAT; the SEmotor pages read name none. The CAN-to-EtherCAT bridge of plan E-5 stands.
- Fit: the knee's module is Φ170 mm against the P2-24's 124. The skeleton's keep-outs at hip pitch, knee and trunk pitch carry the new modules ([skeleton](../mechanical/skeleton/)); where they sit along the axis is layout (plan M-2).
- Whether the dataset's copies are the makers' current sheets, price and availability outside China: not read. None is procured.

## 6g. Walking RMS and the frontal plane — D-2, 2026-11-23

**Decided 2026-11-23 (Plone).** Two checks join the module check of §6f: walking's RMS torque at every leg and trunk joint, against the module's continuous torque, since walking is held, not a 60 s burst; and the hip in the frontal plane in running, which sizes hip roll.

**Since 2026-11-24** the legs must hold people's walking as well ([§6j](#6j-walking-like-a-person--d-2-and-f-5-2026-11-24)); Oli's figures stay required, as the stress case, and serve the trunk alone.

**Why.** The joint heat of plan M-11, run on the set of §6f at 98.2 kg, compared each module's RMS in walking at 1.0 m/s with what its sheet holds continuously. Hip pitch's SEmotor SETZ90CI-1FG walked at 79–81 Nm RMS against its 60 Nm, 1.32–1.35 times; hip roll's SETZ70CI-1GA at 69–78 Nm against 24, 2.9–3.3 times. The walking figures are Oli's [38], a simulated robot with an asymmetric gait, so they were checked against people where people were measured: the running data of Fukuchi et al. [41] carry the hip's moment about all three axes, and the paper's convention puts flexion about Z, abduction and adduction about X, rotation about Y, as net internal moments per kilogram (read in full through Europe PMC, PMC5426356). At 2.5 m/s the hip's abduction moment is 0.65 Nm/kg RMS and 1.73 Nm/kg at its peak, 31 participants — 64 and 170 Nm at 98.2 kg, against the -1GA's 24 Nm continuous and 156 Nm peak. Hip roll had been sized at 1.23 Nm/kg.

**The figures**, Nm per kilogram of body, held in `actuator_sizing.py`:

| Joint | Walking 1.0 m/s, RMS (Oli, the larger side) | Running 2.5 m/s, RMS / peak (Fukuchi, axis) |
|---|---|---|
| Hip pitch | 0.824 | 0.56 / 1.11 (Z) |
| Hip roll | 0.796 | **0.65 / 1.73 (X)** |
| Hip yaw | 0.183 | 0.11 / 0.35 (Y) |
| Knee | 0.736 | 0.96 / 2.79 (Z, §6e) |
| Ankle pitch | 0.683 | 0.77 / 2.07 (Z) |
| Ankle roll | 0.183 | 0.08 / 0.22 (X) |
| Trunk pitch, roll, yaw | 0.127, 0.147, 0.224 | — |

Oli's torques are over the last 8 s of its walk at a commanded 1.0 m/s, divided by its 52.55 kg; the larger of left and right is taken, since the gait is not symmetric (the left knee 0.736, the right 0.564). The arms are left out: Oli's arm swing scales with Oli's arm, not with this body's. Running's figures are each participant's cycle-averaged curve, the method of `RUN_RMS` in §6e, which gives 2.07 at the ankle as declared. Hip roll is now sized to running's 1.73 Nm/kg peak; hip yaw's 0.35 and ankle roll's 0.22 lie below their declared 0.62 and 0.54.

**The set, at the 105.6 kg reference point** — the reference point until 2026-11-24, when [§6k](#6k-static-holds--d-2-2026-11-24) changed trunk pitch, shoulder yaw and the elbow and took it to 107.0 kg; kept here as the step it was. Four joints change from §6f:

| Joint | Needs | Module | Peak / continuous | 60 s under load | Mass |
|---|---|---|---|---|---|
| hip pitch ×2 | 187 Nm; RMS 59 running, 87 walking | ENCOS EC-A10020-P2-24 | 330 / 100 Nm | 79 Nm | 2.211 kg |
| hip roll ×2 | 183 Nm; RMS 69 running, 84 walking | ENCOS EC-A10020-P2-24 | 330 / 100 Nm | 79 Nm | 2.211 kg |
| ankle pitch ×2 | 219 Nm; RMS 81 running, 72 walking | MyActuator RMD-X12-P20-320 | 320 / 85 Nm | — | 2.40 kg |
| trunk yaw | 78 Nm; RMS 24 walking | ENCOS EC-A6416-P2-25 | 120 / 40 Nm | 31.5 Nm | 0.805 kg |

The other joints keep their modules of §6f, with their needs at 105.6 kg in spec 02.6. The RMD-X12-P20-320's size is read from its sheet's drawing, Φ124 ± 0.1 × 85 ± 0.5 mm [34]; the same sheet gives a line resistance of 0.12 Ω and a torque constant of 3.3 N·m/A, which the joint heat of plan M-11 can use. It is taken at the ankle because the P2-24's 79 Nm for 60 s falls short of running's 81 Nm RMS at this mass. The X12's sheet gives no time under load, so the check there is against its 85 Nm continuous torque, a weaker check than the P2-24 had: the rule rewards the sheet that says less.

The loop converges on **105.6 kg** from any start between 82 and 120 kg: modules 36.7 kg — 23.6 for legs and trunk, 13.1 for arms, wrists and neck — `f_act` 0.348, at the top of the 0.25–0.35 band of spec 02.2, γ 2.58, pack 4.22 kWh, endurance ceiling 10.7 h. Peak over module mass comes out at 100 Nm/kg for legs and trunk and 58 for the rest. The set holds to 108.8 kg of body, where trunk roll's 16 Nm continuous meets its walking RMS; its 104 Nm peak runs out at 109.5 kg, and ankle pitch's running RMS reaches the X12's 85 Nm at 110.4 kg.

**At the 4-hour point** the same rules give 132.7 kg, `f_act` 0.31, pack 10.6 kWh, with the EC-A13715-P1-12.67 at hip pitch, hip roll and ankle pitch, the EC-A13720-P1-11.4 at the knee, the EC-A6416-P2-25 at hip yaw, SEmotor SETZ90CI-1FG at trunk pitch and SETZ70CI-1GA at trunk roll. `scripts/gems_budget.py` carries the 2-hour set's densities to every point and gives 137 kg there.

**What it does not settle.**
- Walking's figures come from one simulated robot, not from people walking; no human walking data with the hip's three axes was read.
- ENCOS's own stall temperature-rise tables put what a module holds continuously below its rated torque: the EC-A4315-P2-36 holds 20 Nm, not its rated 25; the EC-A13715-P1-12.67 heats from 30 to 100 °C in 27′50″ at 80 Nm against its rated 110; the EC-A10020-P2-24 in 22′15″ at 80 against 100 [35]. The check uses the rated figure; at a stall these tables are the stricter.
- Heat: computed again on this set in §6h. The hip roll figure of the table above is scaled from Oli by mass alone; Oli's hips are 26 cm apart and GEMs' 18, so it is likely high (§6h).
- The rest of §6f's list stands: static holds (closed on 2026-11-24 in part, §6k), the bench's conditions, the bus, fit, the sheets' currency, price and availability.

## 6h. Walking heat by speed and the hip roll lever — M-11, 2026-11-24

*Computed on Oli's gait at 105.6 kg, the reference point of its day; §6k gives the totals at 107.0. On people's gait, the basis since 2026-11-24, see [§6j](#6j-walking-like-a-person--d-2-and-f-5-2026-11-24); this section stands as the stress case: the heat if the controller walks the way the simulated robot does.*

**Decided 2026-11-24 (Plone), on these figures:** walking is sustained at 0.5 m/s and held at its 1.0 m/s top for up to 10 min at a time (spec 02.6 row 1), both provisional until the cooling of plan M-11; the hip joints stay 0.18 m apart (kinematics §2); and the balance controller keeps hip roll's holding torque down by where it puts the centre of mass (plan F-5, `⟦CTRL⟧`).

**The joint heat.** For each ENCOS module, heat = L0(|τ|) + k·|τ·ω|, from its own tables in the manual [35]: L0, the bus input at zero speed, from the stall table, all of it heat; k from the slow-ramp table, the loss above L0 per watt of output, median over the rows at half the table's top speed or more (0.17 for the EC-A10020-P1-12, 0.23 for the EC-A6416-P2-25, 0.25 for the P2-24, 0.35 for the EC-A13715-P1-12.67). For the RMD-X12-P20-320 the sheet gives a line resistance of 0.12 Ω, Y-connected, and a torque constant of 3.3 N·m/A [34]: copper loss 1.5·R·(τ/K_t)², a floor, with the rest of the loss at its rated point (85 Nm, 100 rpm, 1000 W, 75%) as k·|τ·ω|, an estimate. SEmotor gives no resistance, efficiency or measured table, so trunk pitch, trunk roll and the elbows are not computed. The torques are Oli's [38], walking straight with the heading held, over the last 8 s, scaled from its 52.55 kg to 105.6 kg; its speeds as simulated.

**What a module holds without overheating, on its maker's bench.** No ENCOS module used here has a row marked sustainable except the EC-A4315-P2-36 (20 Nm at stall) and the EC-A3814-H14-107. A first-order model, ΔT = P·R·(1 − e^(−t/τ)) to 70 K, fitted to the two lowest rows of a table, estimates it: the EC-A4315-P2-36 at 41–43 W, between the 37.3 W its table holds and the 45.9 W it does not, which checks the method; the P2-24 at 65 W from its stall rows and 85 W from its constant-load rows; the EC-A13715-P1-12.67 at about 75 W from its stall rows (its load rows lie too far above to fit); the EC-A10020-P1-12 at about 94 W. These are estimates on a bench whose ambient and mounting the manual does not state, starting at 30 °C, without the shell. At one heat the stall rows reach 100 °C sooner than the load rows, by about 2× for the P2-24 and 10× for the EC-A6416-P2-25, so the figures carry that spread.

**By speed**, watts per joint, left and right:

| Speed | Hip pitch | Hip roll | Hip yaw | Knee | Ankle pitch (X12) | Ankle roll | All joints computed |
|---|---|---|---|---|---|---|---|
| 0.25 m/s | 25, 26 | 63, 43 | 29, 21 | 53, 33 | 16, 3 | **44**, 36 | ~0.44 kW |
| 0.5 m/s | 61, 56 | **65**, 50 | 29, 19 | **76**, 47 | 29, 14 | 31, 32 | ~0.59 kW |
| 0.75 m/s | **96, 87** | **79, 65** | 30, 24 | **112**, 59 | 53, 53 | 27, 34 | ~0.83 kW |
| 1.0 m/s | **115, 108** | **97, 76** | 40, 26 | **132, 85** | 85, 95 | 36, 34 | ~1.07 kW |

In bold, a joint at or above the low end of its module's estimated sustained heat: 65 W for the P2-24, 75 for the EC-A13715-P1-12.67, 41 for the EC-A4315-P2-36; the X12 has no such figure. 0.5 m/s is the fastest speed with every computed joint at or under it, and the left hip roll and knee are at it, with no margin; at 0.25 m/s the left ankle roll is over, since each foot stands alone longer. At 1.0 m/s, by the P2-24's constant-load rows, hip pitch reaches 100 °C in about 16 min on the left and 19 on the right, from 30 °C; the left knee in about 19 min by the EC-A13715's stall rows. The six hip modules give about 460 W at 1.0 m/s and 280 W at 0.5. Oli's gait is not symmetric, which is why left and right differ. A straight walk and the earlier one that drifted 13.6 m sideways at 1.0 m/s give the same hip roll, 85 and 84 Nm.

**Why hip roll does not fall with speed.** In single support, the rest of the body — all of it but the stance leg — hangs on the stance hip's roll axis. Logged in the simulation, its centre of mass sits 14.4 cm from that axis on average, 13.4–15.6 cm, at 0.5 and at 1.0 m/s alike: a static moment of about 61 Nm at Oli's scale, against an RMS of 41–52 Nm in the joint over single support, since the body also falls toward the stance leg. Two things set the lever: Oli's hip joints are 26 cm apart, and its whole-body centre of mass moves only about 0.8 cm toward the stance foot. GEMs' hips are 18 cm apart; with Oli's gait its lever would be about 10 cm, and its static moment some 28% smaller than Oli's scaled by mass, as §6g scales it — an estimate, not a simulation. So the walking figure §6g uses at hip roll is likely high, and it stays as the conservative figure: hip roll would still need the P2-24. Each centimetre the centre of mass moves toward the stance hip takes about 8.6 Nm off the static moment at 105.6 kg (87 kg above the stance leg, at Oli's mass fraction); what that costs in lateral motion, and what it does to the rest of the gait, needs a controller trained for this body.

**What it does not settle.**
- One simulated robot, one trained policy; no human walking data with the hip's three axes was read. Oli's policy takes only a speed command, so a gait with a different stance or weight shift could not be run.
- The benches' conditions, and the shell: the padding over the hip, knee and shoulder modules, and the protectors there, keep heat in (spec 04.1).
- The X12 has no usable temperature-rise data, so the ankle pitch's time to 100 °C is not known; SEmotor's trunk pitch, trunk roll and elbows have no heat at all, and the elbows walk at 1.00–1.02 times their 9 Nm continuous from the arm's swing, a load §6g's check leaves out.
- The cooling itself (plan M-11), which both walking figures now rest on.

## 6i. Thermal network of the ventilated body — M-11, 2026-11-24

*Run on Oli's gait at 105.6 kg — the stress case since 2026-11-24; at 107.0 kg, with trunk pitch and the arms counted, [§6k](#6k-static-holds--d-2-2026-11-24). On people's gait see [§6j](#6j-walking-like-a-person--d-2-and-f-5-2026-11-24).*

**What it answers.** The airflow of [spec 04.8](../../spec/04-shell.md#48-ventilation-and-surface-temperature), at 35 °C ambient and at 40, with the joint heat of §6h: how much air each branch needs, and how well the body must cool each module. The makers publish no resistance from winding to housing, so the network cannot predict a winding temperature. It states a requirement instead: R_req = (100 °C − T_air) / P, the resistance from the winding to the air at that module that keeps it at the bench's 100 °C end point, and sets it against the maker's bench, R_bench = 70 K / P_sus with P_sus the sustained heat of §6h, the bench taken at 30 °C.

**The paths.** The main path takes the hips, then trunk yaw, then the shoulders; each lower leg has its own loop (knee, ankle); the edge computer, 130 W, a cool branch. Air rises 15 K in a branch (10 K in the compute branch), and a module sees its zone's inlet plus half the zone's rise. The design case is the lower of two: walking at 0.5 m/s held, and 10 min at 1.0 m/s from the 0.5 m/s steady state, with the bench time constant of §6h's fits (an estimate).

| Branch | 0.5 m/s | 1.0 m/s |
|---|---|---|
| Main path: hips, trunk, shoulders | 336 W, 39 CFM | 586 W, 69 CFM |
| Left leg / right leg | 135 / 93 W, 16 / 11 CFM | 252 / 214 W, 30 / 25 CFM |
| Edge computer | 130 W, 23 CFM | 130 W, 23 CFM |
| **All** | **~89 CFM** | **~147 CFM** |

**Per module, at 35 °C**, the design resistance and how much better than its own bench the body must do:

| Module | Design R, K/W | Better than the bench by | h at the housing, at least |
|---|---|---|---|
| Hip pitch, left / right (P2-24) | 0.67 / 0.71 | **1.6× / 1.5×** | 26 / 24 W/m²K |
| Hip roll, left / right (P2-24) | 0.73 / 0.93 | **1.5× / 1.2×** | 24 / 19 W/m²K |
| Knee, left / right (EC-A13715) | 0.59 / 0.94 | **1.6×** / 1.0× | 20 / 13 W/m²K |
| Hip yaw, ankle roll (EC-A4315) | 1.5–2.3 | 0.7–1.1× | 25–39 W/m²K |
| Trunk yaw (EC-A6416) | 1.65 | 0.9× | 20 W/m²K |
| Shoulders (EC-A10020-P1-12) | 2.1–4.1 | 0.2–0.4× | 5–10 W/m²K |
| Ankle pitch (X12) | 0.60–0.68 | no bench figure | 26–29 W/m²K |

At 40 °C the largest factors — hip pitch, left hip roll, left knee — rise to 1.6–1.8×; right hip roll to 1.3×. The 10 min at 1.0 m/s sets the hips and knees, not the held 0.5 m/s. The coefficient in the last column is what the housing alone would need if all of R_req lay outside it — a floor, since the winding-to-housing resistance adds to it; it sits at the low end of forced convection in gases, 25–250 W/m²K (mechanical ref 44). **Whether air can meet the hips depends on that unpublished internal resistance**: if it is near 0.6 K/W, no flow of air reaches R_req at hip pitch, and the heat needs a conducted path into the structure as well. It is the first thing to ask of ENCOS, or to measure when a module is in hand.

**What it does not settle.** The bench's sustained heats and time constants are first-order estimates from two rows each; the bench's mounting and ambient are not stated; the pack's own heat is not known; the module fans at the shrouds are not chosen; the fans' operating points need P–Q curves that the candidate's specification does not give; the pressure drop of louvres and ducts is not known.

## 6j. Walking like a person — D-2 and F-5, 2026-11-24

**Decided 2026-11-24 (Plone).** People walking become the basis: the balance controller is asked for a gait whose RMS at each leg joint keeps within the 90th percentile of people at 1.0 m/s (plan F-5), and the leg modules must hold it. The simulated robot's gait stays as the stress case, and the modules must hold that too, since no controller yet walks this body like a person. For the trunk, where the human data stop at the pelvis, Oli's figures serve alone.

**The data.** Fukuchi, Fukuchi and Duarte's public dataset of walking [42], version 6: 51 people, 382 treadmill trials at eight speeds, 40–145% of each one's self-selected speed, the belt speed of each trial recorded in `WBDSinfo.csv`. Per trial, the cycle-averaged joint moments in Nm/kg, Cardan Z–X–Y — Z flexion and extension, X abduction and adduction, Y rotation, the hip's resolved in the pelvis — as the authors' Visual3D pipeline and script define them. Holding the rails was allowed and is recorded: 28 trials with the hands on them are left out, as are 45 where it is not recorded and 10 with values missing; 299 remain, 42 of them by 38 people at 0.9–1.1 m/s. With the unrecorded trials in, no 90th percentile at that speed moves by more than 4%. The larger side of each trial is taken, as for Oli.

| Joint | People, 0.4–0.6 m/s: mean (90th percentile) | People, 0.9–1.1 m/s: mean (90th percentile) | Oli, 1.0 m/s | Oli over the mean at 1.0 m/s |
|---|---|---|---|---|
| Hip pitch | 0.24 (0.32) | 0.33 (**0.400**) | 0.824 | 2.5× |
| Hip roll | 0.47 (0.53) | 0.48 (**0.536**) | 0.796 | 1.7× |
| Hip yaw | 0.10 (0.13) | 0.10 (**0.118**) | 0.183 | 1.9× |
| Knee | 0.25 (0.35) | 0.24 (**0.334**) | 0.736 | 3.0× |
| Ankle pitch | 0.63 (0.74) | 0.67 (**0.760**) | 0.683 | 1.0× |
| Ankle roll | 0.06 (0.10) | 0.09 (**0.124**) | 0.183 | 2.2× |

RMS, Nm/kg; the figures in bold are `WALK_RMS` in `actuator_sizing.py`, Oli's are `WALK_RMS_OLI`, and a leg module must hold the larger. The knee's 90th percentile is a little higher at 0.5 m/s than at 1.0, and neither is near its module's 110 Nm. People's hip roll is 0.47–0.48 at every speed from 0.5 to 1.2 m/s, the static moment of the body over the stance leg that §6h found in Oli. The ankle does not fall with speed either: at 0.5 m/s it is nearly what it is at 1.0.

**The set and the loop.** With both gaits required, the larger RMS at each joint, the set is that of §6g and the body **105.6 kg** (107.0 since §6k, the same day): the robot's figure is the larger at every leg joint but the ankle pitch, where people's, 80 Nm at 105.6 kg, stands against the X12's 85. The set holds to 108.8 kg, where trunk roll's 16 Nm continuous meets its walking RMS.

**What was tried.** On people's figures alone the rule of §6f takes the lighter SEmotor SETZ90CI-1FG at hip pitch and the body is 103.6 kg, 2.0 kg less (commit 4d98ce1, the same day). It was not kept: it does not hold the stress case, 85 Nm RMS against 60 continuous, which no airflow mends; a stand-up or step carries 32 kg against 75; running's RMS, 58 Nm, leaves it 3%; and its maker publishes no loss, so its heat could not be computed.

**Heat on people's gait**, per joint, the 90th percentile over the trials, at 105.6 kg: the ENCOS loss model of §6h, with the joint power of the dataset for the speed term — the hip's whole power cannot be divided among its axes and is charged to hip pitch, so hip roll and hip yaw carry their stall part only, a floor — and the X12's copper loss with its rated-point rest:

| Joint | 0.5 m/s | 1.0 m/s | Design R at 35 °C, against the bench |
|---|---|---|---|
| Hip pitch (P2-24) | 25 W | 37 W | 1.94 K/W, 0.55× |
| Hip roll (P2-24) | 43 W | 44 W | 1.39 K/W, 0.77× |
| Hip yaw (EC-A4315) | 18 W | 15 W | 3.36 K/W, 0.51× |
| Knee (EC-A13715) | 35 W | 39 W | 1.57 K/W, 0.59× |
| **Ankle pitch (X12)** | **105 W** | **114 W** | 0.51 K/W, no bench figure |
| Ankle roll (EC-A4315) | 13 W | 17 W | 3.42 K/W, 0.50× |

Below 1×, a module may be cooled less well than on its maker's bench; at 40 °C the factors are 0.55–0.85×. So the hips, knee and ankle roll ask for nothing better than their benches, where on Oli's gait hip pitch, left hip roll and left knee asked for 1.5–1.8× (§6i). **The ankle pitch is the joint to watch.** It walks at 78–80 Nm RMS, 94% of the X12's 85 Nm rated torque, at 0.5 m/s as at 1.0, and its copper loss alone is 101–106 W against 119 W at the rated torque. The sheet has no time under load, so whether 85 Nm is held is not known, and the one maker that publishes it, ENCOS, holds less than it rates (§6g). It is warmer here than on Oli's gait at 0.5 m/s, 29 W: a human gait relieves the knee and hip, not the ankle.

The network of §6i on these heats, with Oli's trunk and shoulders: about **85 CFM at 0.5 m/s and 100 at 1.0**, against 89 and 147 on Oli's gait, for which the fans are sized.

**What it does not settle.**
- The gait: a controller that walks this way on this body is plan F-5's to make. People's moments hold for a mass carried as theirs is; GEMs' modules sit heavier at the knee and ankle, which loads the swing. The dataset is barefoot, on a treadmill, and each curve is an average over cycles, slightly lower in RMS than a single one.
- The ankle pitch: the X12's time under load, its loss and its thermal resistance.
- Trunk pitch, trunk roll and the elbows: SEmotor publishes no loss. Trunk roll alone since §6k.
- The trunk and arms, still on Oli's figures or none.

## 6k. Static holds — D-2, 2026-11-24

**Decided 2026-11-24 (Plone).** A load is held as briefly as possible, at three levels ([spec 02.6](../../spec/02-structure-and-motion.md#static-holds)): at most 2 s passing through full reach, at most 10 s picking up or setting down, and no declared limit where the load is close and the torque low. The 2 s and 10 s are design choices; no source gives them. This closes what §6f left open for the arms and trunk pitch, and not for the knee (a squat or a kneel held).

**Why shortening the hold was not enough.** SEmotor's sheet gives a peak held 1 s or less and a continuous torque, and nothing between. The elbow's SETZ70CI-1DA holds 9 Nm, of which the level forearm takes 6, so about 1 kg is left; two hands hugging 20 kg ask each elbow 25. Trunk pitch's SETZ70CI-1HA holds 35 Nm, and 20 kg hugged upright asks 59. Lifts and carries last longer than 1 s, so no maker's figure covers them.

**The loads.** Arm torques are those of §6b. Trunk pitch is a gravity moment, the trunk straight and leaning as a whole with the arms hanging, at the lowest of the three pitch axes: g · sin θ · (0.536 · M · 0.3035 m + load · 0.430 m), the shares and lengths of the URDF, whose mass fractions are a human's (Winter). At 107.0 kg and 30° with 15 kg it is 117 Nm. If the coupling shared the angle equally over the three axes, the actuator would see their mean, about a third less; the coupling is `⟦IMPL⟧`, so the larger figure stands. The check is `static_holds` in `actuator_sizing.py`, and the modules' times are ENCOS's stall tables, 30 to 100 °C on the bench [35], interpolated log-log:

| Joint | Level | Torque | Module | Held on its maker's bench |
|---|---|---|---|---|
| Elbow | 10 s: 15 kg, forearm level | 51 Nm | EC-A8116-P1-18 | 83 s |
| Shoulder pitch | 10 s: 15 kg, upper arm down, forearm level | 51 Nm | EC-A10020-P1-12 | 979 s |
| Shoulder yaw | 10 s: its declared torque | 60 Nm | EC-A8116-P1-18 | 15 s |
| Trunk pitch | 10 s: 15 kg in the hands, leaning 30° | 117 Nm | EC-A10020-P2-24 | 91 s |
| Elbow | held: 20 kg hugged, two hands | 25.4 Nm | EC-A8116-P1-18 | 483 s or more; 25 Nm is marked sustainable |
| Shoulder pitch | held: 20 kg hugged, two hands | 48 Nm | EC-A10020-P1-12 | 1133 s or more |
| Trunk pitch | held: 20 kg hugged, upright | 59 Nm | EC-A10020-P2-24 | 1335 s or more |
| Shoulder pitch, roll | 2 s: full reach | 108, 84 Nm | EC-A10020-P1-12 | **not in the table**, which ends at 61.5 Nm, 5′18″ |

**The modules.** The rule of §6f, the lightest that passes, with the 10 s hold added: the EC-A8116-P1-18 at the elbow and shoulder yaw — 130 Nm peak, 40 Nm rated, 140 rpm peak, 961 g, Φ105 × 57 mm, 18:1 (manual §7.2) — and the EC-A10020-P2-24 at trunk pitch. The lighter EC-A8112-P1-18 (868 g, 90 Nm peak) has a stall table that ends at 32 Nm. At the elbow the module is heavier than the SEmotor it replaces by 0.26 kg, and at shoulder yaw lighter than the EC-A10020-P1-12 by 0.41.

**The 18:1 exception (Plone).** The arm's reducers are 6:1–15:1 so that a person can push the arm back ([mechanical §2](../mechanical/README.md#2-reducers-by-joint-class)). What a person feels of the motor is its rotor inertia times the ratio squared: 189 kg·mm² at 18:1 is 0.061 kg·m², below the 0.070 of the shoulder's EC-A10020-P1-12 (485 kg·mm² at 12:1), both from the manual. The reducer's friction, the other part, is not published for either. The exception is for these two joints.

**The loop.** It converges on **107.0 kg**: modules 37.6 kg — 24.8 for legs and trunk, 12.8 for arms, wrists and neck — `f_act` 0.351, γ 2.64, pack 4.28 kWh, endurance ceiling 10.5 h; peak over module mass 97 Nm/kg for legs and trunk, 59 for the rest. The set still holds to 108.8 kg, 1.8 kg above the reference point, where trunk roll's 16 Nm continuous meets its walking RMS. The ankle pitch walks at 81 Nm RMS and runs at 82, 96 and 97% of the X12's 85. A stand-up or step carries 74 kg. `f_act` passed the 0.35 that topped spec 02.2's band, which had no source; the author raised the top to 0.36 the same day. Without the exception at shoulder yaw the body is 108.4 kg and `f_act` 0.355; with no exception at all, the EC-A10020-P1-12 at both, 109.9 kg, and trunk roll takes the next module.

**At the 4-hour point** the same rules give 136.0 kg, `f_act` 0.32, pack 10.9 kWh, with the EC-A13720-P1-11.4 at hip pitch and knee, the EC-A13715-P1-12.67 at hip roll, ankle pitch and trunk pitch, the EC-A6416-P2-25 at hip yaw and SEmotor SETZ70CI-1GA at trunk roll. `scripts/gems_budget.py` carries the 2-hour set's densities and gives 140 kg there.

**Heat and air at 107.0 kg**, as §6j and §6i compute them, 0.5 / 1.0 m/s. On people's gait, per joint: hip pitch 25 / 37 W, hip roll 43 / 45, hip yaw 18 / 16, knee 36 / 40, ankle pitch 108 / 117, ankle roll 13 / 18; the factors against the bench 0.5–0.8× at 35 °C and up to 0.86× at 40. Trunk pitch, the elbows and shoulder yaw now have a maker's loss table: on Oli's gait trunk pitch gives off 8 / 9 W, an elbow 3 / 5 W and a shoulder yaw 1 W — small, since they carry little while walking. With them counted the body needs about **88 / 104 CFM** on people's gait, and **92 / 152 CFM** on Oli's, which the fans are sized for; the factors of §6i hold to within 0.1 at the hips and knees. The elbows, at 5.5–9.3 Nm RMS of arm swing, no longer walk at their module's continuous limit.

**What it does not settle.**
- The 2 s at full reach: no figure at 108 or 84 Nm. To ask of ENCOS, or to measure.
- The hold under the shell, and from a module already warm: the tables are a bench's, from 30 °C, its mounting and ambient not stated. A module that turns under load holds for less: at 50 Nm the EC-A10020-P1-12 goes 18′53″ standing still and 1′27″ at 63.5 rpm.
- In a stall one phase may carry more than the others; where the bench's sensor sits is not stated.
- Shoulder yaw's 60 Nm, a declared figure with no source.
- The trunk's mass fractions and the coupling's share.
- The fit: the EC-A8116-P1-18 is Φ105 mm at the elbow, against a 90 mm upper arm and a 76 mm forearm in the URDF (plan M-2).

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
| 42 | Fukuchi C.A., Fukuchi R.K., Duarte M., [A public dataset of overground and treadmill walking kinematics and kinetics in healthy individuals](https://doi.org/10.7717/peerj.4640), *PeerJ* 6:e4640, 2018 (read in full through Europe PMC, PMC5922232); data [10.6084/m9.figshare.5722711](https://doi.org/10.6084/m9.figshare.5722711) v6, CC BY 4.0: treadmill T01–T08 at 40–145% of self-selected speed; processed knt files, moments in Nm/kg, Cardan Z–X–Y (the authors' Visual3D pipeline `wbdsOvergroundDA.v3s` and script `wbdsExploratoryDA.m`) |
