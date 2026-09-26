# Simulation model

A URDF of the GEMs body, generated from the declared kinematic configuration.

| File | Contents |
|---|---|
| [`generate_urdf.py`](generate_urdf.py) | The generator, and the audit that holds the model to the declaration |
| `gems.urdf` | Generated output — 38 links, 37 joints: 31 actuated, 6 coupled through `<mimic>`. Do not hand-edit |

```bash
python hardware/sim-model/generate_urdf.py            # write gems.urdf
python hardware/sim-model/generate_urdf.py --check    # audit only
python hardware/sim-model/generate_urdf.py --mass 95  # a lighter operating point
```

Python 3, standard library only.

## Generated, not written

The model is produced from [`../kinematics.md`](../kinematics.md) rather than
authored beside it. A hand-written URDF is a second declaration of the same
facts, and two declarations drift: the file says 0.70 m reach, the document says
something else, and nobody notices until a controller is tuned against the wrong
one.

The audit closes that loop. It recomputes the model's own properties and
compares them to the declaration:

```
  core DOF             31         expected 31         ok
  trunk spread 3 segs  True       expected True       ok
  mech covers soft     True       expected True       ok
  total mass kg        130.0      expected 130.0      ok
  reach m              0.7        expected 0.7        ok
  standing height m    1.75       expected 1.75       ok
  drawn height m       1.75       expected 1.75       ok
  drawn segments       17         expected 17         ok
  torso above waist    True       expected True       ok
  feet point forward   True       expected True       ok
  joints move as named True       expected True       ok
```

The first three check the structure: 31 actuated joints, each trunk axis spread
over its three segments by `<mimic>`, and mechanical travel at least as wide as
the soft limit everywhere. The next three add up declared figures. The next four
measure the geometry
actually written — the boxes and cylinders a viewer draws in the zero pose —
because a model can have every length right and still draw the torso below the
waist. The last drives each limb joint to its limits, on both sides, and checks
by forward kinematics that it moves the way its name says: the elbow brings the
hand forward, the knee folds the shin back, abduction carries a limb outward,
and the larger half of each asymmetric range points the way the human one does.
Those asymmetries are checked against the soft limits — the human profile — not
against the mechanical travel, which is wider by design.

A mismatch exits non-zero. If the declaration changes, regenerate; if the
generator disagrees with the declaration, one of them is wrong and the audit
says which figure.

## What is estimated — which is most of it

No mechanical design exists, so nothing here is derived from one.

| Quantity | Where it comes from | What that costs |
|---|---|---|
| **Segment masses** | Anthropometric fractions for a human of the same height | A robot is not a human. Actuators concentrate mass at joints and the battery sits in the torso, so the real distribution differs — the torso fraction here is understated |
| **Inertia tensors** | Solid cylinders for limbs, boxes for torso, pelvis, head, feet | Real segments are shells around voids. The tensors are the right order and the wrong number |
| **Joint limits** | Two tiers ([kinematics §1.5](../kinematics.md#15-range-of-motion-mechanism-not-biology)): `<limit>` is the mechanical-travel **target**, `<safety_controller>` the human range as the default soft profile | The travel actually achieved is `⟦IMPL⟧` until the mechanical design; the soft limits' gains are placeholders |
| **Segment radii and widths** | Proportion, not structure | Nothing has been sized to carry a load |

Segment **lengths**, **joint count** and **arrangement** are the exceptions:
those are declared, not estimated.

### What the model is therefore good for

Reach and workspace, self-collision geometry, gait topology, controller
bring-up, and anything that depends on *where the joints are*.

### What it is not good for

Impact, precise torque prediction, energy per step, or any claim about
stability margins — all of which depend on true inertia. Those wait for
`hardware/mechanical/`, and using this model for them would produce confident
numbers about a body that does not exist.

## Model notes

**Twenty-one intermediate links carry 1 g each.** URDF gives every joint a child
link, so a three-axis shoulder needs two massless links between the torso and
the upper arm, and each of the three trunk segments needs two. Some tools reject
exactly-zero mass, so they carry a gram — 21 g across the body, 0.02% of it. They carry no geometry: each segment is drawn
once, on the link that holds its mass.

**Axes follow the URDF convention** — x forward, y left, z up. The zero pose
stands upright with arms at the sides and palms facing the thighs; the torso
and head extend upward from their joints, every other segment hangs below its
own. Joint angles follow the right-hand rule about each axis, so flexion that
carries a limb forward is negative, and roll and yaw limits are mirrored
between the left and right sides.

**Colours are for telling parts apart,** not a surface finish: left limbs are
orange, right limbs blue, alternating light and dark along each limb, with the
pelvis, torso and head in greys. Shading is the viewer's, not the file's.

**The trunk is three segments with coupled joints** (kinematics §1.4, D-9).
Each axis — yaw, pitch, lateral bend — has one actuated joint at the lumbar
segment and two `<mimic>` joints above it, so a trunk command turns all three
segments together: 30° commanded is 90° at the shoulders. Simulators that ignore
`<mimic>` treat the followers as free joints and need an equality constraint
added — MuJoCo, for one, expresses coupling that way.

**The root is `pelvis`,** floating. Attach it to a world frame in whatever
simulator you use; the model does not assume one.

**Hands are one rigid link each.** The declaration puts hands at 2 × 5 to
2 × 21 DOF and leaves the choice to the operator
([kinematics §1.2](../kinematics.md)). Modelling a specific hand here would fix
a choice the declaration deliberately leaves open, so the sim carries the core
31 DOF and a hand-shaped mass.
