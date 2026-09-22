# GEMs platform specification

This is the body's side of GEMs: what it consists of, what it can do, and what
each capability costs. It does not specify the controller that operates the body
(see [Scope boundary](../README.md#scope-boundary)).

The specification declares **envelopes and trade-offs**, never a chosen
operating point. Structure, actuation and energy sit on one coupled loop, so
fixing any single figure fixes the rest; the point on that curve is chosen by
whoever runs the body, not here.

## Chapters

| # | Chapter | Site group | Contents |
|---|---|---|---|
| 00 | [Scope and acceptance criteria](00-scope-and-criteria.md) | overview | What must be true of anything in this specification, and the notation |
| 01 | [Architecture](01-architecture.md) | overview | The invariant pillar, and the application frame it serves |
| 02 | [Structure and motion](02-structure-and-motion.md) | hardware | Mass loop, convergence condition, protection, reach and payload, peak power |
| 03 | [Energy](03-energy.md) | hardware | Sources, the six levers, state levels, docking, floor power and sleep ceiling |
| 04 | [Shell](04-shell.md) | hardware | Programmable stiffness, self-healing, colour, and the three-layer division |
| 05 | [Sensing](05-sensing.md) | hardware | Per-channel envelopes, aggregate rate, and the on-body/off-body compute split |
| 06 | [Audit surface](06-audit-surface.md) | hardware | Attestation, emission log, low-power trace, contact amplitude |
| 07 | [Firmware and software](07-firmware-and-software.md) | software | What runs on the body: responsibilities, rates, guarantees, and link-loss behaviour |
| 08 | [Platform contract](08-platform-contract.md) | protocols | What an external processing loop requires of a body, and where this body supplies it |
| 09 | [Open constants](09-open-constants.md) | resources | Values deliberately left unfilled, and why |

## Reading order

Chapters 00 and 01 set the terms; read them first. Chapters 02, 03 and 05 are
mutually dependent — mass determines power, power determines endurance,
endurance determines mass — and each states where it hands off to the others.
Chapter 07 states what the on-body stack must do; chapter 08 is the one to read
if you are checking this body against an external specification rather than
building it.

> [!NOTE]
> **Nothing specified here has been built.** The project is unfunded; every
> figure in these chapters is derived or cited, none is measured on hardware.
> See the [repository README](../README.md) for what that does and does not
> mean.

## Status

All ten chapters are written. Every capability cluster is closed: no chapter is
still at the level of a sketch.

What is not here yet is the conformance protocol that turns chapter 08 from a
map into a test — that lives in [`../protocol/`](../protocol/) and is
🔜 *waiting update*.
