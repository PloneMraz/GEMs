# Electrical

Component selection against the specification. Every figure below is sourced;
§7 lists the references.

| File | Contents |
|---|---|
| [`actuator_sizing.py`](actuator_sizing.py) | Sizes every joint from its peak torque and reports the resulting `f_act` |

---

## 1. The actuator finding — raised, and resolved

> **Resolved by option A on 2026-09-22.** The specification now declares
> **75–90 Nm/kg peak, on a peak-torque-over-module-mass basis**, and states the
> basis explicitly. `spec/` and this document agree again; the record below is
> kept because the reasoning is what justifies a figure at the top of the
> commercial band.

Sizing the declared 30 joints against published torque densities did not
reproduce the actuator mass fraction the specification assumed. Tool output as
run on 2026-09-22, before the correction:

```
Nm/kg    mass kg    f_act    source
  22.0      155.2     1.19   integrated state of the art, whole-actuator
  33.0      103.5     0.80   the figure spec 02.6 uses
  36.0       94.8     0.73   top of the range spec 02.6 declares
  52.0       65.7     0.51   commercial QDD module, 8:1 planetary
  88.7       38.5     0.30   commercial hollow-shaft planetary module, peak
```

[Spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients)
assumes `f_act` between **0.25 and 0.35**. [Spec
02.6](../../spec/02-structure-and-motion.md#26-actuation-and-manipulation)
declared, at that time, actuator specific torque of **30–36 Nm/kg**, and sized
its own worked example at 33.

**Those two figures were not compatible.** At 33 Nm/kg the actuators weigh 80%
of the body, `Σf` exceeds 1 before a single cell of battery is fitted, and the
coupled loop does not converge at any endurance — not at four hours, not at two.

Both figures in that paragraph have since been corrected; they are quoted here
as they stood when the contradiction was found.

### It is not the arms

Halving the per-arm payload from 30 kg to 15 kg takes the total from 3414 Nm to
3000 Nm: `f_act` falls from 0.80 to 0.70. The legs carry 1905 Nm of the total,
and leg torque is set by body mass, not by what the hands hold.

### A lighter body is worse, not better

| Body | Total torque | `f_act` at 33 Nm/kg |
|---|---|---|
| 70 kg | 2396 Nm | **1.04** |
| 90 kg | 2735 Nm | 0.92 |
| 110 kg | 3075 Nm | 0.85 |
| 130 kg | 3414 Nm | 0.80 |

Leg and waist torque scale with mass; wrist, neck and arm torques do not. Shed
mass and the fixed torques dominate a smaller budget. **There is no lighter
version of this body that closes at 33 Nm/kg.**

### What does close

The lowest density that puts `f_act` inside the assumed range is **75 Nm/kg**,
and only the best commercially claimed module reaches it. At a mainstream QDD
module's 52 Nm/kg, `f_act` = 0.51 and the loop is already marginal:

| `f_act` | 2 h | 4 h |
|---|---|---|
| 0.30 — assumed | γ = 3.2 | γ = 4.5 |
| 0.51 — at 52 Nm/kg | γ = 9.9 | γ = 81.8 |
| 0.80 — at 33 Nm/kg | **diverges** | **diverges** |

This was a decision for the author, not something to be silently patched. The
options as put are kept at §6, with the one taken marked.

---

## 2. Actuators

**Selection: quasi-direct drive, hollow-shaft planetary, at the top of the
commercial torque-density band.** Nothing lower closes the mass loop.

| Property | Figure | Source |
|---|---|---|
| Commercial QDD module, 8:1 planetary | **52 Nm/kg**, 9 arcmin backlash | CubeMars AKE80-8 [1] |
| Commercial hollow-shaft planetary | **88.7 Nm/kg** peak, 85 Nm, 879 g | CubeMars [1] |
| Highest commercial claim, series | up to **36 Nm/kg** | ZHR-H series [3] |
| Integrated SOTA, whole-actuator | **18–22 Nm/kg** — axial flux, cycloidal QDD, hybrid housing, hollow titanium shaft, phase-change cooling | [3] |
| Design floor for hip and knee | **> 30 Nm/kg** peak | [3] |
| Industrial servo, for contrast | 5–10 Nm/kg | [3] |
| QDD reduction ratios | **6:1 to 15:1**, against 50:1–120:1 industrial | [2] |
| QDD mass saving | **40–60%** against high-ratio gearboxes | [2] |

> **The two families of number.** A module advertised at 88.7 Nm/kg quotes peak
> torque over motor-plus-gearbox mass; an integrated figure of 18–22 Nm/kg
> counts housing, cooling and wiring as well. They differ by a factor of four
> and both are honest. The sizing script prints both so the gap cannot be
> read past.

**Why QDD and not harmonic drive.** [Spec
01](../../spec/01-architecture.md#application-frame) puts safe human contact at
the core of the application frame. High-ratio harmonic drives are effectively
non-backdrivable: a stalled arm cannot yield, so contact force is whatever the
controller commands and nothing mechanical limits it. QDD at 6:1–15:1 stays
backdrivable, which makes compliance a property of the mechanism rather than a
promise made by software. That is a specification-driven reason, not a
preference.

## 3. Power

| Property | Figure | Source |
|---|---|---|
| Silicon-anode cell, commercially available | **450 Wh/kg**, 1150 Wh/L | Amprius [4] |
| Solid-state pouch, stack level | **465 Wh/kg**, 1400 Wh/L | SOLiTHOR [5] |
| Semi-solid pouch, validated | ~347 Wh/kg | [6] |
| All-solid-state pouch for robots | mass production targeted 2027, robots first | Samsung SDI [6] |
| Rate capability demonstrated | 80% retention after 400 cycles at 4C | QuantumScape [6] |

> **The durable tier of [spec 03.1](../../spec/03-energy.md#31-source) is now
> real.** It declares 400–500 Wh/kg, and 450–465 Wh/kg cells are commercially
> available or at validated stack level. The ceiling tier at 700–1100 Wh/kg
> remains laboratory-only, exactly as the specification states.
>
> **The rate trade the specification asserts is confirmed.** The literature
> frames it as a straight choice between high C-rate and high energy density
> [7], which is the mechanism behind
> [spec 02.7](../../spec/02-structure-and-motion.md#27-peak-power-is-limited-by-the-source-not-the-actuators):
> choosing the ceiling pack widens the peak-power shortfall rather than closing
> it.

## 4. Compute

| Property | Figure | Source |
|---|---|---|
| Edge module | NVIDIA Jetson AGX Thor | [8] |
| AI throughput | up to 2070 FP4 TFLOPS, 7.5× AGX Orin | [8][9] |
| Power | **40–130 W**, 3.5× the efficiency of AGX Orin | [8][9] |
| Memory | 128 GB | [9] |
| Interconnect | PCIe Gen 5, Blackwell architecture | [9] |

**Against the specification.** At 130 W on a 130 kg body this is **1 W/kg** —
between 4% and 10% of the 10–25 W/kg motion budget of
[spec 02.2](../../spec/02-structure-and-motion.md#22-the-four-coefficients). Edge
compute is affordable in the power budget; what it is not is free, and
[spec 05.6](../../spec/05-sensing.md#56-the-on-body--off-body-compute-split)
states why that matters.

The compression duty is **≥2:1 and realistically 8:1** of 15.8 Gbps raw
([spec 05.4](../../spec/05-sensing.md#54-aggregate-rate-against-the-link)) — about
2 GB/s of sensor data processed in real time. Whether this part meets it is a
measurement, not a datasheet reading, and it stays open until measured.

## 5. Bus

**Selection: EtherCAT for the joint chain, CAN FD for distributed sensing.**

| Property | Figure | Source |
|---|---|---|
| EtherCAT in humanoids | 1 kHz (RoboSimian, Hydra, ARMAR-6) | [10] |
| | 2 kHz (Atlas, LOLA) | [10] |
| | **4 kHz** dual-channel (TOCABI) | [10] |
| CAN FD | 64-byte data field, faster data phase, CAN arbitration retained | [11] |
| Common practice | hybrid: EtherCAT for high-performance joints, CAN FD for distributed controllers | [11] |

> Boston Dynamics moved from CAN in Petman to EtherCAT in Atlas [10]. The
> balance loop needs **≥500 Hz**
> ([spec 07.2](../../spec/07-firmware-and-software.md#72-real-time-requirements))
> and joint current loops need kHz-class service; EtherCAT at a demonstrated
> 2–4 kHz clears both with margin, and CAN FD does not.
>
> **This also bears on the timestamp requirement.** EtherCAT distributed clocks
> give the shared time base
> [spec 07.2](../../spec/07-firmware-and-software.md#72-real-time-requirements)
> demands, rather than leaving skew to be inferred later.

## 6. The decision

The finding of §1 had no technical answer — three options, trading against each
other. They are kept here because a design that does not record what it turned
down cannot explain itself later.

| Option | What it costs | |
|---|---|---|
| **A — Raise the declared torque density to ≥75 Nm/kg** | Commits the design to the top of the commercial market. Part availability narrows sharply and there is no margin left to trade away | **✅ taken** |
| **B — Accept a higher `f_act`** | At 52 Nm/kg, `f_act` = 0.51: γ = 9.9 at two hours and 81.8 at four. Endurance collapses below two hours and the mass envelope of spec 02.5 becomes wrong | rejected |
| **C — Reduce what the body must do** | Lower peak torque means less payload, gentler gait, less dynamic recovery. The legs dominate, so this means a body that walks rather than one that catches itself | rejected |

### What option A committed the design to

**75–90 Nm/kg peak, over module mass.** Only a handful of commercial modules
reach it — the hollow-shaft planetary at 88.7 Nm/kg is at the very top of what
is claimed, and a mainstream 52 Nm/kg module does not qualify. Supply is thin
and will stay thin.

**The specification now states the basis**, which is the part that actually
prevents a repeat. The original error was not only a wrong number: 30–36 Nm/kg
is a reasonable figure *on the integrated basis*, and it was being used as if it
were peak-over-module. A density with no basis attached is a number waiting to
be misread.

**The two bands are now one constraint.** 75–90 Nm/kg maps onto `f_act`
0.29–0.35, each derivable from the other, and `scripts/gems_budget.py --check`
holds them together — including the actuator-mass column, which it did not
cover before and which is exactly where this drift hid.

## 6a. Trunk lateral-bend torque — research, 2026-09-26

Decision D-9 added a lateral-bend axis to the trunk
([kinematics §1.4](../kinematics.md#14-the-trunk-is-a-spine-not-a-waist)). It
has no torque figure yet. Two things were found, and one was not.

**What the trunk figures already in the table rest on.** Nothing. The waist
rows — trunk pitch 1.54 Nm/kg (200 Nm at 130 kg) and trunk yaw 0.77 Nm/kg — have
no source in §7; they were assumed when the table was written. The source found
for lateral bend below covers all three axes, so it can replace both.

**Human trunk torque per kilogram, all three axes — Pan et al. 2025 [14]
(full text in [`sources/`](sources/)).** 122 asymptomatic adults, 61 male
(24.5 ± 2.3 y, 73.4 ± 15.0 kg, 175.6 ± 6.8 cm) and 61 female; Bionix Sim3 Pro
dynamometer; median peak torque, normalised to body weight:

| Axis | Isometric, male | Isometric, female | Isokinetic 15°/s, male | Isokinetic 15°/s, female |
|---|---|---|---|---|
| Extension (trunk pitch) | **1.74 Nm/kg** | 1.63 | 0.69 | 1.40 |
| Flexion | 1.15 | 1.05 | 0.58 | 0.93 |
| **Lateral bending, left / right (trunk roll)** | **0.95 / 0.91** | 1.00 / 0.86 | 0.47 / 0.46 | 0.88 / 0.78 |
| Axial rotation, left / right (trunk yaw) | **0.74 / 0.64** | 0.66 / 0.66 | 0.35 / 0.40 | 0.43 / 0.53 |

Sex differences vanish once normalised (P > 0.05), so the male isometric
column is used as the figure. The isokinetic values are lower because the
device's slow constant-velocity protocol is not a peak-effort condition; they
are not a dynamic peak. Lateral bending is **0.55 × extension**.

**Cross-check, two engineered waists and one robot URDF:**

| Source | Roll : pitch | Note |
|---|---|---|
| 3-DOF coupled tendon-driven humanoid waist, *Advanced Robotics* 2023 [15] | 0.50 | Designed pitch : roll : yaw = 4 : 2 : 1, realised as 87.0 / 53.0 / 22.2 Nm static. Abstract only; robot mass not obtained |
| Flexinoid tensegrity spine, *Scientific Reports* 2025 [18] | — | No torque figures for pitch or roll; actuators are 1.89 N·m servos with elastic assistance. Its value is as a mechanism reference — see kinematics §1.4 |
| Unitree G1 URDF, 29-DOF [16] | 1.0 | waist_roll = waist_pitch = 35 Nm, waist_yaw 88 Nm, robot 35.1 kg. An outlier: G1's pitch and roll travel only ±30°, both sized far below its yaw |

Human strength and a waist engineered to match human balance agree at
**about 0.5–0.55**. The G1 ratio is set by its small-travel design, not by need.

**Options, not yet adopted** — the sizing table still carries 30 joints. At the
130 kg point:

| | Pitch | Roll | Yaw | Σ torque | `f_act` at 75 | at 80 | at 88.7 | Density for `f_act` ≤ 0.35 |
|---|---|---|---|---|---|---|---|---|
| Today, no roll | 200 | — | 100 | 3414 Nm | 0.350 | 0.328 | 0.296 | 75.0 |
| **A** — add roll at 0.95 Nm/kg, keep the assumed pitch and yaw | 200 | 124 | 100 | 3537 Nm | 0.363 | 0.340 | 0.307 | **77.7** |
| **B** — all three trunk axes from [14]: 1.74 / 0.95 / 0.74 Nm/kg | 226 | 124 | 96 | 3560 Nm | 0.365 | 0.342 | 0.309 | **78.2** |

Either option moves the floor of the declared density band (spec 02.6) from
75 to about 78 Nm/kg; B also replaces two unsourced constants with sourced
ones. Both are specification changes and wait for the author.

**What was not found:** a dynamic lateral trunk moment during the motions the
axis is for — twisting to protect the body in a fall, righting from the ground.
Isometric strength is a floor on capability, not a peak dynamic demand.
Asymmetric-lifting biomechanics report lateral bending moments at L5/S1 rising
with task asymmetry [17], but no peak figure was obtained.

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

Joint torque requirements used by the sizing script: ankle peak 1.4 Nm/kg at
push-off and 2.5–3.5 W/kg push-off power from normative gait data; hip
100–150 Nm peak for a 70 kg humanoid during stair climbing and squat rise,
scaled by mass [12][13]. Knee is assumed equal to hip pitch — **an assumption,
not a source**, and the one figure in the table that most deserves checking
against a real gait dataset.

| # | Source |
|---|---|
| 12 | [Human-Level Actuation for Humanoids](https://arxiv.org/html/2511.06796) |
| 13 | [Selection guide for humanoid robot knee and hip joint motors](https://www.cubemars.com/how-to-choose-hip-and-knee-joint-motors-for-humanoid-robots.html) |
| 14 | Pan F., Cheng J., Kong C., Wang W., Lu S., [Sex-specific characteristics of the trunk muscle behaviors in an asymptomatic adult cohort](https://doi.org/10.1186/s40001-025-02742-w), *European Journal of Medical Research* 30:471, 2025 — [`sources/pan-2025-…pdf`](sources/pan-2025-trunk-torque-eur-j-med-res-30-471.pdf) |
| 15 | [A 3-DOF coupled tendon-driven humanoid waist](https://www.tandfonline.com/doi/abs/10.1080/01691864.2023.2289134), *Advanced Robotics* 37(23), 2023 |
| 16 | [Unitree G1 description, `g1_29dof.urdf`](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description) — joint `<limit effort>` values read on 2026-09-26 |
| 17 | [The effects of lifting speed on the peak external forward bending, lateral bending, and twisting spine moments](https://www.tandfonline.com/doi/abs/10.1080/001401399185838), *Ergonomics* 42(1) |
| 18 | Ali A. R., Abdullah H. S., [Development of a compliant spine mechanism for enhanced humanoid robotics locomotion](https://doi.org/10.1038/s41598-025-32165-w), *Scientific Reports* 15:44646, 2025 — [`sources/ali-2025-…pdf`](sources/ali-2025-flexinoid-tensegrity-spine-sci-rep-15-44646.pdf) |
