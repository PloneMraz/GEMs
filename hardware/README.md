# Hardware

The body itself. What [spec chapters 02–06](../spec/) specify as envelopes, this
directory fixes as a design.

| Document | Contents | Status |
|---|---|---|
| [`kinematics.md`](kinematics.md) | Degrees of freedom, their arrangement, reach and segment lengths | ✅ |
| [`mechanical/`](mechanical/) | Material and mechanism selection, sourced. CAD still to come | ◐ selection done |
| [`electrical/`](electrical/) | Actuator, power, compute and bus selection, sourced, with joint-by-joint actuator sizing | ◐ selection done |
| [`sim-model/`](sim-model/) | URDF generated from the kinematics, with an audit that holds it to the declaration | ✅ |
| [`bom/`](bom/) | EBOM, MBOM and SBOM generated from the kinematics and checked against each other; approved manufacturer list with source and price where verified | ◐ 281 parts, none priced |

## Specification and design

The two are kept apart on purpose.

**The specification declares ranges**, because structure, actuation and energy
sit on one coupled loop and fixing one figure fixes the rest — so it publishes
the curve and leaves the point to whoever operates the body.

**This directory declares a point.** Joint count is not a range: a body has the
joints it has. Reach is not a range: an arm is as long as it is. Those belong
here, and they are stated as chosen, not derived.

A different configuration satisfying the same envelopes is a different body, not
a wrong one.

## What was closed here

The joint count **40** and the reach **0.70 m** were load-bearing in three
places — the proprioception channel, the full-tier log rate, and the shoulder
torque table — before any chapter declared them.
[`kinematics.md`](kinematics.md) declares them, and shows what the figure would
be under the minimum and maximum hand configurations so that the choice is
visible rather than buried.

## Why the rest waits

`hardware/mechanical/` and `hardware/electrical/` need parts: an actuator, a reducer, a structural
alloy, a bus. Choosing them is design work, and none of the specification's
`⟦IMPL⟧` constants that depend on them — actuator mass fraction, joint current
loop rate, permitted timestamp skew, thermal envelope — can be closed before
they are chosen.

[`sim-model/`](sim-model/) needed less, and is done: kinematics were declared,
so the model is generated from them with estimated masses and inertias. It is
good for reach, workspace and gait topology, and **not** good for impact or
torque prediction — those need true inertia, which needs a mechanical design.
The README there says which is which rather than leaving a user to find out.

**Why the simulation model lives under hardware rather than beside it.** It is
not a model in its own right; it is a model *of* this body, and its inertias
come from the mechanical design. Kept apart, the two drift and the simulation
quietly starts lying about the thing it claims to represent. Kept adjacent, the
coupling is visible and a change to one is an obvious prompt to check the
other.
