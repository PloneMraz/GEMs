# Joint modules in CAD

The nine joint modules [spec 02.6](../../../spec/02-structure-and-motion.md#the-basis-matters-as-much-as-the-number) declares, drawn from their makers' installation drawings, and a first layout of all 31 on the body — plan [M-1 and M-2](../../../plan/PLAN.md#m--mechanical), 2026-11-24.

![The 31 joint modules on the segment envelopes](media/gems-modules-whole.webp)

| File | Contents |
|---|---|
| [`generate_modules.py`](generate_modules.py) | The modules' dimensions, the layout, the generator in FreeCAD, and the audit |
| `gems-modules.step` | Generated — the nine modules, each as its body, cover and output, in millimetres |
| `gems-module-layout.step` | Generated — the 31 module envelopes in place, facing FreeCAD's *Front* as the [skeleton](../skeleton/README.md#two-frames-one-rotation) does |
| [`layout.csv`](layout.csv) | Generated — where each module sits, how far it stands outside the segment envelopes, how far its joint turns before two modules touch |
| [`render_modules.py`](render_modules.py) | The Blender scene behind the files of `media/` |
| `media/` | `gems-module-layout.glb`, for a viewer on the web; a turntable in WEBM; five stills in WebP |

```bash
python3 hardware/mechanical/modules/generate_modules.py          # build, audit, write
python3 hardware/mechanical/modules/generate_modules.py --check  # build and audit, write nothing
```

Needs FreeCAD 1.1, as the skeleton does. `gems-modules.step` is a drawing of bought parts for layout, not a manufacturing file, and not the makers' own CAD, which was not obtained.

## What is read, and what is not

Diameters, lengths, bolt counts, pitch circles and thread depths are read off the installation drawings: the ENCOS manual V3.13 and MyActuator's XV4 sheet, [electrical refs 35 and 34](../../electrical/README.md#7-references). What the drawings do not print is scaled from them and is illustration: the cooling fins, the angles of the bolt circles, and what each entry of `MODULES` names under `scaled`. SEmotor's sheet prints only the envelope, Φ78 × 65 mm, so everything else of the trunk roll module is illustration. The connectors, the cables and the screws are not drawn.

**The layout is not a design.** Each module lies on its joint's own axis and slides along it until it clears its neighbours, but for hip roll, which stands above its axis and drives it by a parallelogram of rods that is not drawn. The trunk's three sit on the axes of different coupled segments. There is no rod, no bearing and no structure; what a layout this plain is good for is showing what fits.

## Wrist, hip and shoulder, 2026-11-24

The first layout of the day, every module driving its own axis directly, did not fit at three places. Each is changed (Plone):

- **Wrist.** Three Φ53 × 78.5 mm modules cannot share one point: wrist roll stood 69 mm out in front and left 6° of bend toward it. **The pitch axis is now 56 mm above the roll axis** ([kinematics §2](../../kinematics.md#2-reach-and-segment-lengths)), one diameter and the gap, so each axis carries its module, pitch and roll across the limb, yaw along it. The price is that the three axes no longer meet: the arm's inverse kinematics loses the closed form a spherical wrist gives and is solved numerically. Wrist pitch's lever to the grip grows from 60 to 116 mm: 15 kg held level asks it 18.0 Nm, hand and roll module included, within the 20 Nm it is declared at and the 7′00″ its stall table holds that for.
- **Hip roll.** Behind the hip, it stood 90 mm out of the pelvis, and the URDF's thigh, 116 mm across, would have touched it at 7° of extension, against a declared target of 90; the module check alone had said 28, because it does not move the segments. **It is now in the pelvis, above the hip pitch module**, and drives the roll axis, 136 mm below, by a parallelogram whose ratio is 1: for 185 Nm, two rods on 45 mm cranks carry about 2.1 kN each at the middle of the travel and 2.9 at 45°. The rods and rod ends are to be bought, the cranks are GEMs' own integration; none is drawn.
- **Shoulder.** The joint stood level with the base of the neck, 1.446 m up, and its modules 62 mm above the torso. Women of 1.63–1.67 m in [ANSUR II](https://www.openlab.psu.edu/ansur2/) have the acromion at 1.353 m (442 of 1986; the female file). **The shoulders are now at 1.35 m** ([kinematics §2](../../kinematics.md#2-reach-and-segment-lengths)); nothing stands above the torso or beside the head, and the wrist hangs at 0.80 m, where the same file has 0.805. Reach overhead drops by 95 mm.

The trunk's modules were rearranged to make room: pitch on the middle segment's axis, yaw and roll on the upper's.

## What it shows

In the zero pose no two modules overlap. Turned alone, **two modules stop 5 of the 31 joints** before the end of their mechanical travel, against 18 of 28 in the first layout, which did not check the trunk:

- **Hip roll** (both): inward 6°, where the two ankle modules meet, and outward 22°, where the hip pitch module meets the wrist of an arm hanging straight down. Without the arms and the other leg its whole travel is clear.
- **Shoulder roll** (both): the same wrist against the same hip, an arm hanging straight down cannot turn inward.
- **Trunk bend**: 2° for the hanging arms, and **21° without them, where hip roll meets trunk pitch** — below the 30° of the human range and the 45 that is the provisional target. This one is the layout's, and open.

Outside the segment envelopes:

| Module | Outside, mm | Against women of 1.63–1.67 m (ANSUR II, means) |
|---|---|---|
| Shoulder roll | 54, at the side | modules 504 mm across; shoulder breadth over the deltoids 452 |
| Knee, Φ170 | 41 | lower thigh 129 mm across, calf 120 |
| Ankle roll / pitch | 30 / 22 | ankle 69 mm across |
| Trunk roll | 20, in front | chest depth 249, the module's front at 120 mm from the middle |
| Elbow, Φ105 | 19 | upper arm 98 mm across, forearm 85 |
| Hip pitch | 14 | hip breadth 356; the modules 265 |
| Wrist pitch / roll, shoulder yaw | 9 / 9 / 8 | wrist 50 mm across |

Part of each figure is the URDF's, whose segments are thinner than a person's: a thigh of 116 mm where the file's circumference gives 197 at the top, a shank of 94 against 120. The widths across are circumference over π. What is wide in itself is the shoulder, the knee and the ankle.

The check turns one joint at a time, in steps of 2°, with plain cylinders for the modules and nothing else of the body — no segment, no rod, no pack — so a clear figure is not a promise. The shoulder pitch modules now stand where the battery pack is to lie, in the upper back ([plan](../../../plan/PLAN.md#pack-location-decided)): 38 mm is left behind them within the torso envelope, for M-2 to check.
