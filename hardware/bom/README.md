# Bills of materials

The three bills of materials of the GEMs reference design, in the form hardware
teams use:

- **EBOM** — engineering BOM: the product as designed, a multi-level structure.
- **MBOM** — manufacturing BOM: the same parts regrouped into routings — build
  operations at work centres — plus the consumables the design never shows.
- **SBOM** — software BOM, in two senses the industry uses side by side:
  software images carried as virtual part numbers in the EBOM, so a shipped body
  records what it runs; and a machine-readable component inventory in
  CycloneDX, for supply-chain security.

**To read them, open [`EBOM.md`](EBOM.md) and [`MBOM.md`](MBOM.md).** The CSV
and JSON files are the data; those pages are generated from them.

| File | Contents | Kept by |
|---|---|---|
| [`parts.csv`](parts.csv) | Item master — one row per internal part number, software and consumables included | generated |
| [`ebom.csv`](ebom.csv) | Product structure — parent, find number, child, quantity | generated |
| [`mbom.csv`](mbom.csv) | Routings — assembly, operation, work centre, what each operation consumes | generated |
| [`sbom.cdx.json`](sbom.cdx.json) | Software components, hashes, licences and dependencies, CycloneDX 1.7 | generated |
| [`avl.csv`](avl.csv) | Approved manufacturer list — manufacturer, part number, source, price, date | **by hand** |
| [`EBOM.md`](EBOM.md), [`MBOM.md`](MBOM.md) | Readable views, with mass roll-up and sourcing status | generated |
| [`build_bom.py`](build_bom.py) | Generates all of the above from one definition, and checks them against each other | — |

```bash
python hardware/bom/build_bom.py            # regenerate
python hardware/bom/build_bom.py --check    # verify only; non-zero on any error
```

Python 3, standard library only. This is work package B of
[`plan/`](../../plan/README.md#b--bill-of-materials-and-cost).

---

## Why this shape

A flat list of what the specification names is a requirements list, not a BOM.
Industry practice, and the open humanoid projects that publish theirs, converge
on a few features, and each one is here for a reason.

| Practice | Here | Why |
|---|---|---|
| **Multi-level, indented structure** with parent–child relations [1][2][3] | Body → assemblies (head, neck, torso, arms, hands, legs, shell, harness) → joint modules and sub-assemblies → components | A change to one sub-assembly touches only its branch, and a part used in several places — a joint module in both arms — is defined once |
| **EBOM distinct from MBOM** [4][5] | This is the EBOM: organised as the product is designed. The MBOM — assembly order, tooling, process steps — follows the CAD | Nothing has been assembled; an MBOM now would be invented |
| **Stable, non-intelligent internal part numbers** [1][6] | `GEM-nnnnn`, revision `A`. Numbers are allocated in blocks for readability only and carry no meaning to be parsed | The internal number is the key everything else references; it must survive a change of supplier |
| **Manufacturer part numbers and alternates in an AVL**, not in the structure [1][6] | `avl.csv`, one row per manufacturer candidate, ranked, `SELECTED` or `CANDIDATE` | Sourcing changes without the design changing |
| **Procurement type, lifecycle, unit of measure** [1] | `make_buy`, `lifecycle`, `uom` | |
| **Manufactured, off-the-shelf and electrical kept apart** [7] | `category`: ASSY, MFG, OTS, PCBA, CABLE, MATL | They are sourced, costed and reviewed differently |
| **Mass per line** [8] | `unit_mass_kg` with its basis, rolled up in `EBOM.md` | On this body, mass is the governing variable: every kilogram costs γ kilograms (spec 02.1) |
| **PCBA BOMs with reference designators, footprint, value, DNP** [9][10] | Each PCBA is a part here; its own BOM comes from its schematic and joins this structure then | "Down to each capacitor" lives in those PCBA BOMs, and they cannot exist before the schematics |
| **MBOM derived from the EBOM and validated back against it** [11][12] | Every EBOM line is consumed by exactly one operation of its parent's routing, with the same quantity; the check fails otherwise | An MBOM that drifts from the EBOM builds a different product from the one designed |
| **Consumables, tooling and packaging in the MBOM only** [11][12] | Category `CONS`: threadlocker, reducer grease, thermal interface material, adhesive, cable ties, packaging | They are needed to build the body and are not part of its design |
| **Software as virtual part numbers** | Category `SW`: each firmware image is a child of the board it is programmed into; the edge module's OS and software stack are children of the compute assembly | A body leaves the line with a recorded software configuration, and an update is a revision |
| **SBOM in a standard format** [13][14] | CycloneDX 1.7, validated against the official schema. SPDX (ISO/IEC 5962:2021) is the other accepted format | The EU Cyber Resilience Act requires a machine-readable SBOM for products with digital elements from 11 December 2027 [15]; CISA published updated minimum elements in 2026 [14] |
| **Generated from one source** [8] | Structure generated from the kinematics and the torque table of `hardware/electrical/actuator_sizing.py` | A joint added to the declaration appears in the BOM, or the check fails |

## Columns

**`parts.csv`** — `part_number`, `rev`, `description`, `category`, `make_buy`,
`uom` (EA, SET, M2), `unit_mass_kg` and `mass_basis`, `maturity` (TM or LAB, as
in [spec 00](../../spec/00-scope-and-criteria.md)), `design_level` (L0–L5, as in
[`plan/`](../../plan/README.md#levels-of-detail)), `lifecycle` (all `CONCEPT`
until a design is released), `spec_ref`, `requirement`, `notes`.

**`ebom.csv`** — `parent`, `find_no` (10, 20, 30… per parent), `child`, `qty`,
`qty_basis` (required when `qty` is empty), `ref_des` (for PCBA lines, once they
exist), `notes`.

**`avl.csv`** — `part_number`, `rank`, `status`, `manufacturer`, `mpn`,
`supplier`, `supplier_pn`, `source_url`, `unit_price`, `currency`, `price_qty`
(the order quantity the price is for), `price_date`, `price_url`, `notes`.

## Rules the check enforces

- Every part is used by an assembly, every line points at a part, and the
  structure has no cycles.
- An empty quantity carries a basis saying why it is empty.
- A price carries all of its currency, order quantity, date and page. A price
  that cannot be re-checked is refused.
- A `SELECTED` AVL entry carries a manufacturer, a manufacturer part number and
  a source.
- A **LAB** part carries no manufacturer part number: none exists to give.
- The generated files match what the generator produces now.

## MBOM

Routings are generated for every assembly and every PCBA that carries software.
Leaf parts — machined, composite and bought-in — have no routing here; theirs
is fabrication to drawing, and belongs with the drawing.

| Work centre | Covers |
|---|---|
| `WC-EMS` | PCB assembly at an external contract manufacturer, to each board's own PCBA BOM |
| `WC-PROG` | Programming every firmware image and installing the edge module's images |
| `WC-CELL` | Cell stack assembly at an external specialist |
| `WC-HARN` | Harness manufacture, external |
| `WC-JNT` | Joint module assembly — housing, bearing, motor, reducer, encoders, torque sensor, drive board, fasteners |
| `WC-SUB`, `WC-INT` | Sub-assembly and final integration |
| `WC-CAL` | Calibration and end-of-line test: commutation and encoders, torque sensors, whole-body kinematics, power states, stand and balance, supported failure state |
| `WC-COM` | Commissioning the audit surface: root-of-trust keys and measured-boot baseline (spec 06.2), physical-fingerprint baselines for attestation tier 2 (spec 06.3) |
| `WC-PACK` | Packaging |

Commissioning is a work centre of its own because the specification makes it
one: attestation tier 2 compares a body against the fingerprint taken here, so a
body that skips it cannot be attested later.

Consumable quantities are "as consumed" and set by work instructions, which do
not exist yet. Cycle times and labour are not estimated.

## SBOM

`sbom.cdx.json` lists the software that exists in this repository: each module
with its SHA-256, licence, supplier and the modules it imports, and the Python
interpreter they all run on. There are no third-party packages. Its version
field is a content hash, so a changed file is a changed version, and the check
fails until the SBOM is regenerated. The timestamp is set at generation and is
the one field the check ignores.

The firmware images and the edge module's OS image are in the EBOM as virtual
parts but **not** in the SBOM, because none of them has been built. They join it
when they exist — with the RTOS, the EtherCAT master stack and the operating
system distribution as the third-party components they will bring, each with its
licence to be checked against this repository's.

## Where it stands

The summary at the top of [`EBOM.md`](EBOM.md) is the current count. At the time
of writing: 281 part numbers, including 9 software images and 6 consumables; 472
operations across 57 routings; one selected manufacturer part (the Jetson T5000
module), candidates for nine parts, **no verified price**, and a mass roll-up of
70.3 kg out of the 129.5 kg budget — the rest is blank rather than guessed.

Prices were looked for on 2026-09-26. Most supplier pages were unreachable from
the environment this was written in, so the AVL rests on search results and on
the pages that could be read, and each entry's notes say which.

## What building it turned up

**The actuator density has one module behind it, and it is small.** The only
module found at or above 75 Nm/kg peaks at 85 Nm. Nine of the seventeen joint
types — 16 of the 30 joints — need more, up to 230 Nm at the hip and knee.

**The reducer classes and the actuator family disagree.** `hardware/mechanical`
§2 assigns cycloidal reducers to hips and knees and harmonic drives to wrists
and neck; `hardware/electrical` §2 selects a hollow-shaft planetary module for
every joint. The reducer rows carry the conflict until D-2 decides.

**Ankle and waist have no reducer class.** The mechanical table stops at hip,
knee, shoulder, elbow, wrist and neck.

## References

| # | Source |
|---|---|
| 1 | [Cofactr — the definitive guide to bills of materials](https://www.cofactr.com/articles/the-definitive-guide-to-bill-of-materials-boms) |
| 2 | [OpenBOM — product structures, indented BOM, multi-level BOMs](https://www.openbom.com/blog/product-structures-indented-bom-multi-level-boms-and-parent-child-relationships) |
| 3 | [Arena — multi-level BOMs](https://www.arenasolutions.com/resources/articles/multi-level-bom/) |
| 4 | [PTC — eBOM vs mBOM vs sBOM](https://www.ptc.com/en/blogs/plm/ebom-vs-mbom-vs-sbom) |
| 5 | [Duro — EBOM vs MBOM](https://durolabs.co/blog/ebom-vs-mbom/) |
| 6 | [OpenBOM — part numbers and revisions](https://www.openbom.com/blog/bom-management-best-practices-and-use-revisions-in-part-numbers) |
| 7 | [OpenArm](https://github.com/enactic/OpenArm) — BOM split into manufactured, off-the-shelf and electrical; PCBA BOM with designator, footprint, value, manufacturer part, supplier part |
| 8 | [umanoide](https://github.com/AlessioPagliai/umanoide) — humanoid BOM generated by script, with supplier, link, mass and notes per row |
| 9 | [Anzer — electronic design BOM for PCB assembly](https://www.anzer-usa.com/resources/electronic-design-bom/) |
| 10 | [PCBSync — IPC-2588, BOM data in IPC-2581](https://pcbsync.com/ipc-2588/) |
| 11 | [OpenBOM — manufacturing BOM and BOM restructuring](https://www.openbom.com/blog/manufacturing-bill-of-materials-from-bom-restructure-to-supply-chain-intelligence) |
| 12 | [Leo AI — EBOM to MBOM transformation](https://www.getleo.ai/blog/ebom-to-mbom-transformation-handoff) |
| 13 | [CycloneDX 1.7 JSON reference](https://cyclonedx.org/docs/1.7/json/) |
| 14 | [RunSafe — CISA 2026 SBOM minimum elements mapped to CycloneDX and SPDX](https://runsafesecurity.com/blog/sbom-minimum-elements-cyclonedx-spdx/) |
| 15 | [Anchore — EU CRA SBOM requirements](https://anchore.com/sbom/eu-cra/) |
