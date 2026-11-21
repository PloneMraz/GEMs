# Protocols

How a body demonstrates that it satisfies the platform contract.

| Document | Version | Status |
|---|---|---|
| [Platform conformance protocol](conformance.md) | 0.2 | draft |
| [`assess.py`](assess.py) | — | runs the protocol against this repository's simulated body |
| [Conformance record](conformance-record.md) | — | generated; **the body does not conform** |

```bash
python3 protocol/assess.py            # print the assessment
python3 protocol/assess.py --record   # regenerate conformance-record.md
```

## What this is for

[Chapter 08](../spec/08-platform-contract.md) of the specification maps the requirements an external processing loop places on a body onto the places this body supplies them. That map is enough to design against and not enough to certify with.

The conformance protocol turns it into a test: twenty-one requirements, each with the evidence that demonstrates it, and procedures for the ones a declaration cannot settle.

## The shape of it

**Conformance is binary. The envelope is declared.**

A body either satisfies the contract or it does not — there is no partial conformance, because a loop whose preconditions are half-met does not half-run.

Separately, every body states its own figures: mass, endurance, protection, link, sensing configuration. Those are **declared, not graded**. The specification sets ranges and the operator picks the point, so there is nothing there to pass or fail.

## Run against itself

A protocol that has never been run on anything is the kind of unchecked assertion this repository keeps removing elsewhere. So it has been run — on the only body available, the simulated one that §4 explicitly permits a claim for.

| State | Count |
|---|---|
| MET | 2 |
| MET (simulated) | 3 |
| not implemented | 8 |
| not demonstrable without hardware | 8 |

**Sixteen of twenty-one unmet: the body does not conform**, and the record says so in its second paragraph rather than its last.

The eight executable requirements are not asserted — `assess.py` runs the procedures and reports what happened, including the pipeline-position half of §7.1 that a conclusion-only check would pass by mistake. Three of them (C-3, C-6, C-17) run the half that can run and still report unmet, because the other half needs code not yet written or a body. The thirteen others carry a stated reason instead, and the difference is visible in every row.

The value is in what the gaps turn out to be. They cluster into five groups: four are each one purchase away from being testable, and the fifth is reference code not yet written. That converts "unfunded" from a sentence in the README into a shopping list with a priority order.

## What it deliberately does not test

Whether the body's conduct was acceptable. The protocol establishes that physical amplitude at human contact is **recorded**; it never establishes that it was **appropriate**. That judgement belongs to a third party — the deploying or certifying party — and the protocol says so rather than leaving the gap to be discovered.
