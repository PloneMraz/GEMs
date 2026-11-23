# CAD skeleton

The parametric CAD skeleton of the GEMs body — plan [M-1](../../../plan/PLAN.md#m--mechanical) — generated from the declared kinematic configuration, in FreeCAD.

| File | Contents |
|---|---|
| [`generate_skeleton.py`](generate_skeleton.py) | The generator, and the audit that holds the CAD to the URDF |
| `gems-skeleton.step` | Generated output — 37 joint frames, 17 segment envelopes, 16 swept keep-out volumes and 5 joint-module keep-outs, in millimetres. Do not hand-edit |

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
  faces FreeCAD Front -Y   True       expected True       ok
  left side toward +X      True       expected True       ok
  swept keep-outs          16         expected 16         ok
  keep-outs valid          True       expected True       ok
  poses checked            282        expected 282        ok
  points outside keep-out  0          expected 0          ok
  module keep-outs         5          expected 5          ok
  modules on joint axis    True       expected True       ok
  modules = spec 02.6      True       expected True       ok
  STEP faces Front -Y      True       expected True       ok
```

The last line reads the written STEP file back, because what leaves the generator is the file, not the document. A mismatch exits non-zero and leaves no file behind. The audit was itself checked by breaking the generator on purpose — an envelope shifted by 10 µm, a joint axis turned, the turn of the next section left out of the document and then out of the file — and each was reported.

The keep-outs are checked by posing each segment at every combination of each joint's lower, middle and upper travel — 3 poses for a one-joint segment, 27 for a three-joint one, 282 in all — and testing that up to 150 points of its surface lie inside its keep-out. That is a sample, not a proof: the containment rests on how the volume is built (below), and the sample catches a build that went wrong. Breaking the generator by leaving the travel out of the sweep was reported, 1536 points outside.

The module keep-outs are checked for their centre on the joint's origin and their axis on the joint's, at 1 µm, and for the datasheet's radius and volume; and each names the module that `hardware/electrical/actuator_sizing.py` declares at that joint, at its sheet's size, so the skeleton cannot keep an old module when spec 02.6 changes. A module moved 10 µm off its joint's origin was reported; a knee keep-out 1 mm too wide, or naming the knee's former module, fails the last check (its logic tried outside FreeCAD).

## Two frames, one rotation

The URDF follows the robotics convention: x forward, y left, z up. CAD and modelling tools look at a body from the other side: FreeCAD's *Front* view, like Blender's, looks from −Y, so a body built in URDF axes shows its left side there.

Every marker and envelope is therefore built in URDF axes inside one container, `GEMs_skeleton`, turned −90° about z. In the document and in the STEP file the body faces −Y, its left side toward +X, and FreeCAD's *Front* view shows its front. **That turn is the only difference between the CAD frame and the URDF frame:** geometry taken from the CAD back to the URDF — the visual meshes of plan ID-7 — is turned +90° about z. The audit measures inside the container against the URDF, and checks the turn separately.

FreeCAD 1.1 drops an `App::Part`'s placement when it writes STEP, so the generator writes the STEP from the shapes with the turn already applied, flat, each under its own name.

## What is in it

**Joint frames.** One marker per URDF joint: a rod of 60 mm through the joint's zero-pose origin, along its axis, carrying the joint's name, parent link, child link, type and, for the six coupled trunk joints, the joint it follows. The joints of one multi-axis group — shoulder, hip, wrist, ankle, each trunk segment — share an origin and differ in axis.

**Segment envelopes.** The 17 drawn segments of the URDF: the same boxes and cylinders at the same places. They follow proportion, not structure ([sim-model](../../sim-model/README.md#what-is-estimated--which-is-most-of-it)): they mark where each segment's contents go, not what size those contents are. Section sizing waits for load cases and the joint modules for D-2.

**Swept keep-out volumes,** one for each segment but the pelvis (`keepout_l_thigh` and so on, in the group `KeepOutSwept`): the space the segment's envelope can occupy as the joints between it and its parent segment turn through their mechanical travel, the `<limit>` of the URDF. The parent and everything above it stay in the zero pose, so a keep-out is the reach of one segment relative to the one it hangs from — the thigh's is the hip's three axes, the foot's the ankle's two — not of a whole limb.

Each is built joint by joint, from the joint nearest the segment out to its parent — the order in which the joints' turns compose: the envelope's points are taken about the joint's axis, the rectangle that bounds them in radius and height is revolved through the angle the shape already spans plus the joint's travel, and the next joint revolves the result. The volume therefore contains the true sweep and is larger than it — 1 mm and 0.5° of margin on top — never smaller. How much larger shows in the numbers: the thigh's is 434 L, the upper arm's 185 L, because three axes revolving a bounding sector each time compound. It is the space no other part may enter, not the space the segment fills.

**Joint-module keep-outs** at both hip pitch joints, both knees and trunk pitch (`module_l_knee` and so on, in the group `KeepOutModule`), for the modules [spec 02.6](../../../spec/02-structure-and-motion.md#the-basis-matters-as-much-as-the-number) declares there since 2026-11-23 ([electrical §6f](../../electrical/README.md#6f-modules-declared-at-the-joint--d-2-2026-11-23)), none yet procured: SEmotor SETZ90CI-1FG at hip pitch, Φ99 × 76.5 mm; ENCOS EC-A13715-P1-12.67 at the knee, Φ170 × 73 mm; SEmotor SETZ70CI-1HA at trunk pitch, Φ78 × 85 mm. Each is a cylinder of the datasheet's outer diameter and thickness, on the joint's axis and centred on its origin. Earlier that day all five were the ENCOS EC-A10020-P2-24, Φ124 × 85 mm. That is the module's own volume, not its place: where along the axis it sits, whether it turns its joint directly or through a linkage, and how the modules of one multi-axis group clear one another are layout (plan M-2). A module keep-out overlaps the envelopes and the swept keep-outs around it, as the hardware will.

## What is not in it yet

**Module keep-outs for the other 26 actuated joints.** Their modules are declared (spec 02.6); their keep-outs are not yet built.

## Reading it

- **Views:** *Front* shows the body's front, *Right* its left side, *Top* looks down on the head. The origin is the pelvis frame of the URDF.
- **A saved `.FCStd` opens with every object hidden.** It is written without a GUI, and FreeCAD keeps visibility in the part of the file only a GUI writes. Select all and press Space. The STEP file has no such state and opens shown.
- The STEP header names the author; joint, envelope and keep-out names carry through as product names (`joint_l_knee`, `env_l_thigh`, `keepout_l_thigh`).
- The keep-outs enclose the envelopes, so hide them, or make them transparent, to see the body.
