# Protocols

How a body demonstrates that it satisfies the platform contract.

| Document | Version | Status |
|---|---|---|
| [Platform conformance protocol](conformance.md) | 0.1 | draft |

## What this is for

[Chapter 08](../spec/08-platform-contract.md) of the specification maps the
requirements an external processing loop places on a body onto the places this
body supplies them. That map is enough to design against and not enough to
certify with.

The conformance protocol turns it into a test: sixteen requirements, each with
the evidence that demonstrates it, and procedures for the ones a declaration
cannot settle.

## The shape of it

**Conformance is binary. The envelope is declared.**

A body either satisfies the contract or it does not — there is no partial
conformance, because a loop whose preconditions are half-met does not half-run.

Separately, every body states its own figures: mass, endurance, protection,
link, sensing configuration. Those are **declared, not graded**. The
specification sets ranges and the operator picks the point, so there is nothing
there to pass or fail.

## What it deliberately does not test

Whether the body's conduct was acceptable. The protocol establishes that
physical amplitude at human contact is **recorded**; it never establishes that
it was **appropriate**. That judgement belongs to a third party — the deploying
or certifying party — and the protocol says so rather than leaving the gap to be
discovered.
