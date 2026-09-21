# Scripts

| Script | What it does |
|---|---|
| [`gems_budget.py`](gems_budget.py) | The coupled mass–energy–power loop of [spec 02](../spec/02-structure-and-motion.md), executable. Prices an operating point, and checks the figures printed in the specification |

Python 3, standard library only. No installation.

## Pricing an operating point

```bash
python scripts/gems_budget.py                 # the 4-hour durable-pack point
python scripts/gems_budget.py --endurance 6   # ask what six hours costs
python scripts/gems_budget.py --json          # machine-readable
python scripts/gems_budget.py --help          # every input
```

The specification declares envelopes rather than a configuration, because
structure, actuation and energy sit on one coupled loop. This script *is* that
loop: give it a point and it returns the body mass, the growth factor, the pack
size, and which of the actuators or the source limits peak power.

It also refuses to pretend. Past the endurance ceiling it reports that the
design does not converge rather than printing a large number:

```
loop     Sf = 1.022   (converges when Sf < 1)
VERDICT  DOES NOT CONVERGE. The scaling terms consume the whole body;
         nothing is left for armour, sensors or hands. This is not an
         expensive design, it is not a design.
```

Exit status is `0` when the point converges, `2` when it does not.

## Checking the specification

```bash
python scripts/gems_budget.py --check
```

Recomputes every figure the specification quotes — endurance ceilings, growth
factors, armour masses, shoulder torques, both operating points with their pack
sizes and power bands, self-discharge, sleep durations, log rates — and confirms
each one still appears in the chapter that claims it.

Exit status is `0` when all agree, `1` otherwise.

**What a mismatch means.** Either the arithmetic drifted, or the chapter's
wording changed. The check says which figure and where; it does not guess which
of the two is wrong. Look at both.

This is the only thing in the repository that holds the specification's numbers
to account. Without it, the figures in `spec/` rest on having been calculated
carefully once.

## Scope

The model prices a **declared** point. It does not recommend one — that choice
belongs to whoever operates the body, as
[spec 00](../spec/00-scope-and-criteria.md) sets out. Nor does it invent
constants: everything it returns is derived from inputs you supply, and inputs
the specification leaves open stay open here too.
