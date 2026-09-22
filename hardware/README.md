# Hardware

The body itself. What [spec chapters 02–06](../spec/) specify as envelopes, this
directory fixes as a design.

| Document | Contents | Status |
|---|---|---|
| [`kinematics.md`](kinematics.md) | Degrees of freedom, their arrangement, reach and segment lengths | ✅ |
| `mechanical/` | Structural CAD, armour layup, joint assemblies | 🔜 *needs part selection* |
| `electrical/` | Power distribution, bus topology, sensor harness | 🔜 *needs part selection* |
| `sim-model/` | URDF/MJCF simulation model | 🔜 *needs kinematics plus inertias* |

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

`mechanical/` and `electrical/` need parts: an actuator, a reducer, a structural
alloy, a bus. Choosing them is design work, and none of the specification's
`⟦IMPL⟧` constants that depend on them — actuator mass fraction, joint current
loop rate, permitted timestamp skew, thermal envelope — can be closed before
they are chosen.

`sim-model/` needs less: kinematics are now declared, and a simulation could be
built on them with estimated inertias. That is the nearest buildable piece of
hardware work, and the only one that needs no fabrication.
