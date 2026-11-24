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
| `media/` | `gems-module-layout.glb`, for a viewer on the web; a turntable in WEBM; four stills in WebP |

```bash
python3 hardware/mechanical/modules/generate_modules.py          # build, audit, write
python3 hardware/mechanical/modules/generate_modules.py --check  # build and audit, write nothing
```

Needs FreeCAD 1.1, as the skeleton does. `gems-modules.step` is a drawing of bought parts for layout, not a manufacturing file, and not the makers' own CAD, which was not obtained.

## What is read, and what is not

Diameters, lengths, bolt counts, pitch circles and thread depths are read off the installation drawings: the ENCOS manual V3.13 and MyActuator's XV4 sheet, [electrical refs 35 and 34](../../electrical/README.md#7-references). What the drawings do not print is scaled from them and is illustration: the cooling fins, the angles of the bolt circles, and what each entry of `MODULES` names under `scaled`. SEmotor's sheet prints only the envelope, Φ78 × 65 mm, so everything else of the trunk roll module is illustration. The connectors, the cables and the screws are not drawn.

**The layout is not a design.** Each module lies on its joint's own axis and slides along it until it clears its neighbours by 3 mm. The trunk's three sit on the axes of three different coupled segments. There is no linkage, no belt, no bearing and no structure; whether a joint is driven directly or through a linkage is M-2's to decide. What a layout this plain is good for is showing where direct drive does not fit.

## What it shows

In the zero pose no two modules overlap. Beyond that:

- **Hip roll stands out of the pelvis envelope by 65 mm behind and 62 below, 90 at its corner.** Hip pitch fills the hip's centre, so hip roll, on the axis behind it, reaches x = −150 mm on a pelvis that ends at −85.
- **Wrist roll stands 69 mm outside the hand and forearm, in front,** for the same reason, and leaves the wrist 6° of bend toward it, of a 70° range. At the wrists three modules on one point do not fit; this is the clearest case for a linkage or another module.
- **Shoulder roll stands 62 mm above the torso envelope** and shoulder pitch 50 mm, inside the space drawn for the head's sides.
- **The knee, Φ170 mm, stands 41 mm outside** a thigh of 116 mm and a shank of 94. The ankle's X12 stands 22 mm outside the shank and foot, and the roll module 28 mm above the foot and 10 behind it.
- **The elbow's EC-A8116, Φ105 mm, stands 19 mm outside** the arm, 90 mm above it and 76 mm below; shoulder yaw, the same module, 8 mm.
- **Travel.** Turned alone from the zero pose, 18 of the 28 limb and neck joints meet another module before the end of their mechanical travel, nine on each side. Hip pitch extends 28°, where the human range declared is 30; hip roll adducts 6° before the two ankles meet, which straight legs do on any body; the shoulder's extension stops at 4°, the wrist pitch module on hip roll, and an arm that hangs straight down cannot turn inward at all.

The zero pose has the arms straight down, so some of the last are the pose's; each is in `layout.csv` with the pair that meets. The check turns one joint at a time, in steps of 2°, with plain cylinders for the modules and nothing else of the body, so a clear figure is not a promise.

Until 2026-11-24 the skeleton's keep-outs held five of the 31 modules. A first place for trunk yaw, in the pelvis, stopped hip roll at 2° of abduction, and was moved to the upper segment's axis for that reason.
