# CAD skeleton

The parametric CAD skeleton of the GEMs body — plan [M-1](../../../plan/PLAN.md#m--mechanical) — generated from the declared kinematic configuration, in FreeCAD.

| File | Contents |
|---|---|
| [`generate_skeleton.py`](generate_skeleton.py) | The generator, and the audit that holds the CAD to the URDF |
| `gems-skeleton.step` | Generated output — 37 joint frames and 17 segment envelopes, in millimetres. Do not hand-edit |

```bash
python3 hardware/mechanical/skeleton/generate_skeleton.py                       # build, audit, write gems-skeleton.step
python3 hardware/mechanical/skeleton/generate_skeleton.py --check               # build and audit, write nothing
python3 hardware/mechanical/skeleton/generate_skeleton.py --fcstd /path/x.FCStd # also save the FreeCAD document
```

Needs FreeCAD 1.1 for its console executable (`freecadcmd`, or `freecad.cmd` from the Snap package; `--freecadcmd` or `$FREECADCMD` to name another). The script runs under `python3` and runs itself again under that executable, which takes no options of its own, so the mode passes through the environment.

## One declaration, not two

The skeleton is generated from [`../../kinematics.md`](../../kinematics.md) through [`../../sim-model/generate_urdf.py`](../../sim-model/generate_urdf.py): the generator imports that script and builds from the URDF it produces. It restates no dimension, so a change to the declaration reaches the URDF and the CAD together, the same way the [URDF](../../sim-model/README.md#generated-not-written) is kept from becoming a second declaration of the kinematics.

The audit measures the CAD after FreeCAD has built it and compares it with the URDF generator's own forward kinematics in the zero pose, at 1 µm:

```
  joint frames             37         expected 37         ok
  actuated joints          31         expected 31         ok
  frames at URDF origin    True       expected True       ok
  frames on URDF axis      True       expected True       ok
  segment envelopes        17         expected 17         ok
  envelopes = URDF         True       expected True       ok
  drawn height m           1.656      expected 1.65       ok
  solids valid             True       expected True       ok
```

A mismatch exits non-zero and writes nothing. The audit was itself checked by breaking the generator on purpose — an envelope shifted by 10 µm, a joint axis turned — and each was reported.

## What is in it

**Joint frames.** One marker per URDF joint: a rod of 60 mm through the joint's zero-pose origin, along its axis, carrying the joint's name, parent link, child link, type and, for the six coupled trunk joints, the joint it follows. The joints of one multi-axis group — shoulder, hip, wrist, ankle, each trunk segment — share an origin and differ in axis.

**Segment envelopes.** The 17 drawn segments of the URDF: the same boxes and cylinders at the same places. They follow proportion, not structure ([sim-model](../../sim-model/README.md#what-is-estimated--which-is-most-of-it)): they mark where each segment's contents go, not what size those contents are. Section sizing waits for load cases and the joint modules for D-2.

## What is not in it yet

**Keep-out volumes,** the third item of M-1. Two kinds are needed: the space a joint module occupies, which waits for D-2 to say which module; and the space a segment sweeps through its travel, which can be computed from the envelopes and is the next step here.

## Reading it

- **Axes are the URDF's:** x forward, y left, z up, origin at the pelvis frame. The body faces +x, so FreeCAD's *Right* view shows its front and FreeCAD's *Front* view shows its left side.
- **A saved `.FCStd` opens with every object hidden.** It is written without a GUI, and FreeCAD keeps visibility in the part of the file only a GUI writes. Select all and press Space. The STEP file has no such state and opens shown.
- The STEP header names the author; joint and envelope names carry through as product names (`joint_l_knee`, `env_l_thigh`).
