# Bill of materials

Every hardware item the specification and `hardware/` already name, one row
each, with a place for its part number, source and price. **A blank is a
record, not an omission**: it says the item has not been verified yet, and it
stays blank until it is.

| File | Contents |
|---|---|
| [`bom.csv`](bom.csv) | The bill of materials — 69 rows at the time of writing |
| [`check_bom.py`](check_bom.py) | Refuses half-filled rows, and summarises what is sourced and priced |

```bash
python hardware/bom/check_bom.py
```

Python 3, standard library only. This is work package B of
[`../../plan/`](../../plan/README.md#b--bill-of-materials-and-cost).

## Columns

| Column | Meaning |
|---|---|
| `id` | Stable identifier, `ABC-01`. Never reused |
| `subsystem`, `item` | What it is |
| `spec_ref` | Where the specification or `hardware/` requires it |
| `requirement` | The figure it must meet, copied from that reference |
| `qty`, `qty_basis` | How many, and why that many. An empty quantity must say why it is empty |
| `maturity` | **TM** commercially available, **LAB** demonstrated but not a product — as in [spec 00](../../spec/00-scope-and-criteria.md) |
| `level` | L0–L5, as defined in [`plan/`](../../plan/README.md#levels-of-detail) |
| `selection` | Technology or part family chosen, if any |
| `manufacturer`, `part_number` | Filled only when a specific part is **chosen**, not merely a candidate |
| `source_url` | Where the part is documented or sold |
| `unit_price`, `currency`, `price_date`, `price_url` | All four or none |
| `notes` | Candidates, conflicts, and anything a reviewer should not have to rediscover |

## Rules the check enforces

- A price needs its currency, the date it was read, and the page it was read
  from. A price without those cannot be re-checked, so it is refused.
- A part number needs a manufacturer and a source.
- A **LAB** item has no part number to give. Its row is completed by a reference
  design traced to a publication, per the plan.
- Quantities are numbers, or areas in `m2` where the item is sold by area.

## What was verified, and how

Prices were looked for on 2026-09-26. Most supplier and shop pages were
unreachable from the environment this was written in, so verification rested on
search results and on pages that could be read. On that basis:

| Row | Found | Recorded as |
|---|---|---|
| CMP-01 | Jetson T5000 module part number `900-13834-0080-000`, listed by distributors | part number and source; **price not found** — the $3,499 widely reported is the developer kit, not the module, and is kept in the notes only |
| PWR-01 | Amprius SiCore 450 Wh/kg cell page | source; **no public price** in any source found |
| ACT-* | The 88.7 Nm/kg module is CubeMars **AKH70-16**, 85 Nm peak, 879 g | named in the notes as a candidate; **price not found** |

No row carries a price yet. The summary says so rather than printing a total.

## What building the BOM turned up

Three things the selection documents did not show until every joint had its own
row.

**The actuator density has one module behind it, and it is small.** The only
module found at or above 75 Nm/kg peaks at 85 Nm. Nine of the seventeen joint
types — 16 of the 30 joints — need more, up to 230 Nm at the hip and knee. The selected density
therefore has no identified part at the torques that dominate `f_act`, and
closing that is part of decision D-2, not a detail after it.

**The reducer classes and the actuator family disagree.** `hardware/mechanical`
§2 assigns cycloidal reducers to hips and knees and harmonic drives to wrists
and neck; `hardware/electrical` §2 selects a hollow-shaft planetary module for
every joint. Both cannot hold. The rows carry both until D-2 decides.

**Ankle and waist have no reducer class.** The mechanical table covers hip,
knee, shoulder, elbow, wrist and neck, and stops there.
