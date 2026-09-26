# Kinematic configuration

The specification declares envelopes; this declares a point on them. Joint
count and reach are not capability ranges — a body has the joints it has — so
they are fixed here rather than in `spec/`.

Everything below is a **declared configuration**, not a derived constraint. A
different configuration satisfying the same envelopes is a different body, not a
wrong one.

## 1. Degrees of freedom

| Group | DOF | Arrangement |
|---|---|---|
| **Legs** | **12** | 6 × 2 — hip roll, pitch, yaw; knee; ankle pitch, roll |
| **Arms** | **14** | 7 × 2 — shoulder pitch, roll, yaw; elbow; wrist yaw, pitch, roll |
| **Trunk** | **3** | yaw, pitch, lateral bend — each spread over three coupled segments, one actuator per axis (see 1.4) |
| **Neck** | **2** | yaw, pitch |
| **Core total** | **31** | |
| **Hands** | **2 × 5 … 2 × 21** | declared separately — see 1.2 |

### 1.1 Why seven-DOF arms

Six DOF positions and orients an end effector. The seventh makes the arm
redundant: the same hand pose is reachable through a range of elbow positions,
so the arm can work around an obstacle, or around a person, without giving up
the pose it is holding.

That redundancy is not a convenience here. Group 4 of [spec
01](../spec/01-architecture.md#application-frame) puts safe human contact at the
core, and a non-redundant arm in contact with a person has exactly one way to
hold a pose — if that way is blocked, it must break contact or force through.

Reference point: a real 1.2 m humanoid ships 5-DOF arms and 25 DOF total, with
no hands. This configuration is a step up in exactly the places the application
frame asks for.

### 1.2 Hands, and why they are counted apart

A human hand carries roughly 21 DOF. Two of them would nearly double the whole
body's joint count, so hands are declared as their own tier with a range:

| Configuration | DOF per hand | Suits |
|---|---|---|
| **Minimum** | 5 | Grasp and release, coupled fingers, independent thumb |
| **Moderate** | 10–12 | Group 2 — daily manipulation and moderate precision |
| **Anthropomorphic** | up to 21 | Full human dexterity |

Which one is fitted is `⟦CTRL⟧`. The hands are the single largest lever on total
joint count, and a specification that folded them into one number would hide
that.

### 1.3 The working figure

Budgets elsewhere in this repository use **41 DOF**. That is this
configuration's **core 31 plus minimum hands (2 × 5)** — the low end, chosen so
that budgets derived from it are not flattered.

| Configuration | Logged joints | Full-tier log rate |
|---|---|---|
| Core only | 31 | 248 kB/s · 2.0 Mbps · 0.89 GB/h |
| **Core + minimum hands** | **41** | **328 kB/s · 2.6 Mbps · 1.18 GB/h** |
| Core + anthropomorphic hands | 73 | 584 kB/s · 4.7 Mbps · 2.10 GB/h |

Even the largest configuration is **0.06%** of the 8 Gbps link. Joint count is
not a bandwidth problem; it is a mass and reliability problem.

### 1.4 The trunk is a spine, not a waist

In a human the trunk does not turn at one joint. Rotation is spread over many
vertebrae, most of it through the thoracic spine; the lumbar spine barely turns
at all, its facet joints set against it
([Anatomy Standard](https://www.anatomystandard.com/biomechanics/spine/rom-of-spine.html)).
A single yaw joint at the waist turns the body exactly where a human does not,
and at large angles reads as a figure twisted at one seam.

**Decision D-9, 2026-09-26: a coupled multi-segment spine.** The trunk is three
segments — lumbar, lower thoracic, and the upper thorax that carries the
shoulders, the neck and the battery pack. Each of three axes — yaw, pitch and
lateral bend — has **one actuator**, and a coupling mechanism (gearing, cable or
an elastic continuum element; `⟦IMPL⟧`) spreads its motion over the three
segments. The motion is distributed like a spine's; the actuator count is that
of a three-axis waist.

Rejected: one actuator per segment per axis, the approach of musculoskeletal
humanoids such as Kotaro and Kenshiro. It is the most flexible, but those
designs report poor controllability and low load capacity, and nine trunk
actuators would break the actuator mass budget (`f_act`).

**An implemented precedent for the coupling.** The Flexinoid spine (Ali and
Abdullah, *Scientific Reports* 2025;
[`electrical/sources/`](electrical/sources/)) is a five-vertebra tensegrity
column — rigid struts, TPU cables, a spherical joint at each level — with pitch
and roll driven by **two actuators in the lumbar region** through tendons and
series elastic elements, the tensegrity transmitting the motion up the column.
Per vertebra 25° flexion and ±10° lateral bend, ±30° lateral bend in total;
unpowered it carries 15 kg passively. Two differences from this body: its yaw
is a separate revolute joint at the shoulder mount, where here yaw is the third
coupled axis; and its lateral range is a third of the 90° targeted here. It
shows the mechanism class works at human scale, not that these figures do.

**A caution on cable coupling, from the same literature.** The 3-DOF
tendon-driven waist of Wang et al. (*Advanced Robotics* 2023; specification
restated in *Mech. Mach. Theory* 216:106220, 2025) couples three actuators
through wires and pulleys. Under a 10 kg torso surrogate at 80°/s, wire slack
put the path **63 mm** off the unloaded reference, and the authors added a
spring gravity-compensation module to recover accuracy. For the coupling
mechanism here — still `⟦IMPL⟧` — that is evidence against plain cable
coupling at this body's trunk mass, and for either geared coupling or cable
coupling with pretension and gravity compensation. Spring compensation of
trunk pitch and roll also serves the energy measure of spec 03.2 (series
elastic elements storing what gravity would otherwise cost).

The coupling ratio between segments is `⟦IMPL⟧`. The simulation model spreads
each axis equally; the human distribution — most rotation thoracic, little
lumbar — is the reference the mechanical design should move toward. The
battery pack sits on the top segment, rigid with the shoulders, so the spine
turns beneath it.

**Lateral bend is new with this decision.** It has no torque in the sizing table
yet ([`electrical/actuator_sizing.py`](electrical/actuator_sizing.py)), so `f_act`
figures elsewhere cover 30 of the 31 core joints until it is sized.

### 1.5 Range of motion: mechanism, not biology

The body's joint limits are set by what the mechanism allows, not by human
range of motion. Wider travel gives the real-time code more ways to turn the
body before impact — the way animals twist to protect what is vulnerable — and
fewer moments of being pinned at a limit exactly when a reaction is needed.
Human range stays available as a **profile**, not as the mechanism.

| Tier | Where | Whose |
|---|---|---|
| **Mechanical travel** | URDF `<limit>` | The body's capability — declared here |
| **Soft limit** | URDF `<safety_controller>` | The operator's or controller's choice (`⟦CTRL⟧`). The model ships the human range as the default profile |

Design targets for mechanical travel, total range — decided 2026-09-26,
to be revised by simulation and, if it happens, by assembly:

| Joint | Human range (soft default) | Mechanical target |
|---|---|---|
| Shoulder pitch | 240° | **250°** |
| Shoulder roll | 200° | **220°** |
| Elbow | 150° | **200°** — 50° past straight |
| Hip pitch | 150° | **210°** — 90° of extension |
| Knee | 140° | **200°** — 60° past straight |
| Trunk yaw | 90° | **180°**, spread over three segments (60° each) |
| Trunk lateral bend | 60° | **90°** — provisional, not sourced |
| Trunk pitch | 90° | 90° — no change proposed |
| Neck | 150° yaw, 80° pitch | unchanged: radar and Wi-Fi sensing cover what is behind |
| All others | human | equal to human until the mechanical design says otherwise |

Where flexion is already bounded by segments meeting — a forearm against an
upper arm near 150° — the added travel is on the other side of straight.

**Locks are separate from limits.** A lock that holds a joint for standing
(spec 03.2, measure 4) engages at a chosen angle — the knee at 0° — and is
independent of the mechanical travel beyond it. Two conditions follow from
separating them: a lock whose release would let the joint pass straight must be
**engaged without power** (spring-applied), since a knee that can pass 0°
collapses if the lock opens on power loss; and it must carry the full static
load path.

### 1.6 Not counted as joints

Facial micro-actuators and pupil actuation ([spec
05.3](../spec/05-sensing.md#53-channels)) are not structural joints: they carry
no load, need no torque sensing, and are not logged per-joint. They are declared
with the sensing channels they serve.

## 2. Reach and segment lengths

For a ~1.75 m body, taken from ordinary human proportion:

| Measure | Declared |
|---|---|
| Shoulder to fingertip | **~0.70 m** |
| Shoulder to elbow | ~0.32 m |
| Elbow to wrist | ~0.26 m |
| Shoulder width | ~0.40 m |
| Hip to knee | ~0.42 m |
| Knee to ankle | ~0.42 m |

The **0.70 m** figure is the one the shoulder-torque table of [spec
02.6](../spec/02-structure-and-motion.md#26-actuation-and-manipulation) takes as
full reach. It was used there before being declared here; this document closes
that gap.

## 3. What this configuration commits elsewhere

| Declared here | Consumed by |
|---|---|
| 41 logged joints | Full-tier log rate, [spec 06.4](../spec/06-audit-surface.md#64-audit-log) |
| 41 joints × 4 channels | Proprioception channel, [spec 05.3](../spec/05-sensing.md#53-channels) |
| Joint count and gearing | `f_act`, [spec 02.2](../spec/02-structure-and-motion.md#22-the-four-coefficients) — still `⟦IMPL⟧`, because count alone does not fix mass |
| 0.70 m reach | Shoulder torque, [spec 02.6](../spec/02-structure-and-motion.md#26-actuation-and-manipulation) |
| Joint count | Module count in [firmware](../firmware/ARCHITECTURE.md) |

> **Joint count does not fix `f_act`.** More joints means more actuators, but a
> joint's actuator is sized by the torque it carries, and an ankle carries
> nothing like a wrist. The actuator mass fraction stays `⟦IMPL⟧` until parts
> are chosen; what this document fixes is how many there are, not what they
> weigh.

## 4. Open

| `⟦IMPL⟧` | Depends on |
|---|---|
| Joint range of motion, per joint — the mechanical travel actually achieved, against the targets of 1.5 | Mechanical design |
| Spine coupling mechanism and ratios | Mechanical design (D-9) |
| Trunk lateral-bend torque | Sizing, D-9 |
| Reducer ratio, per joint | Actuator selection |
| Segment mass distribution | Structural design |
| Hand configuration fitted | `⟦CTRL⟧` — see 1.2 |
