# Bill of materials

The engineering bill of materials (EBOM) of the GEMs reference design, kept in
the form hardware teams use: a multi-level product structure, an item master
with stable internal part numbers, and an approved manufacturer list that holds
sourcing and price separately from the design.

**Open [`EBOM.md`](EBOM.md) to read it.** The CSV files are the data; that page
is the indented view generated from them.

| File | Contents | Kept by |
|---|---|---|
| [`parts.csv`](parts.csv) | Item master — one row per internal part number | generated |
| [`ebom.csv`](ebom.csv) | Product structure — parent, find number, child, quantity | generated |
| [`avl.csv`](avl.csv) | Approved manufacturer list — manufacturer, part number, source, price, date | **by hand** |
| [`EBOM.md`](EBOM.md) | Indented view with mass roll-up and sourcing status | generated |
| [`build_bom.py`](build_bom.py) | Generates the structure and checks all four | — |

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

## Where it stands

The summary at the top of [`EBOM.md`](EBOM.md) is the current count. At the time
of writing: 230 part numbers, one selected manufacturer part (the Jetson T5000
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
