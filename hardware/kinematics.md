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
| **Waist** | **2** | yaw, pitch |
| **Neck** | **2** | yaw, pitch |
| **Core total** | **30** | |
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

Budgets elsewhere in this repository use **40 DOF**. That is this
configuration's **core 30 plus minimum hands (2 × 5)** — the low end, chosen so
that budgets derived from it are not flattered.

| Configuration | Logged joints | Full-tier log rate |
|---|---|---|
| Core only | 30 | 240 kB/s · 1.9 Mbps · 0.86 GB/h |
| **Core + minimum hands** | **40** | **320 kB/s · 2.6 Mbps · 1.15 GB/h** |
| Core + anthropomorphic hands | 72 | 576 kB/s · 4.6 Mbps · 2.07 GB/h |

Even the largest configuration is **0.06%** of the 8 Gbps link. Joint count is
not a bandwidth problem; it is a mass and reliability problem.

### 1.4 Not counted as joints

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
| 40 logged joints | Full-tier log rate, [spec 06.4](../spec/06-audit-surface.md#64-emission-log) |
| 40 joints × 4 channels | Proprioception channel, [spec 05.3](../spec/05-sensing.md#53-channels) |
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
| Joint range of motion, per joint | Mechanical design |
| Reducer ratio, per joint | Actuator selection |
| Segment mass distribution | Structural design |
| Hand configuration fitted | `⟦CTRL⟧` — see 1.2 |
