# 07 — Platform contract

A body acquires signal and executes response. What happens in between — how raw
signal becomes structured information — is specified elsewhere, by a companion
specification of equal rank. Neither document claims the other's territory.

That companion specification does not name this body. It states **conditions any
platform must satisfy**, and this chapter records where this body satisfies them.
The relation is a contract, not a cross-reference: **a contract can be checked;
a cross-reference can only dangle.**

| Companion specification | Scope | Status |
|---|---|---|
| **RSIL** — Relational Sensory Integration Loop | The processing loop for an agent with a body | 🔜 *waiting update* |
| **DIL** — Data Integration Loop | The same relational structure with no body at all | [doi.org/10.6084/m9.figshare.32728983](https://doi.org/10.6084/m9.figshare.32728983) |

## 7.1 Conformance map

| Requirement | What it demands of a platform | Supplied at |
|---|---|---|
| **E1** | Sensors and internal state must make an inside/outside distinction *possible*. The platform does not draw the line; it must not foreclose it | [05.5](05-sensing.md#55-proprioception-is-mandatory) — proprioception |
| **E2** | Actuators must act on the region, and the region must be able to return something other than what was predicted | [02.6](02-structure-and-motion.md#26-actuation-and-manipulation) |
| **E3** | State must persist across cycles | [01](01-architecture.md) — off-body memory; on-body storage |
| **E4** | Emissions must leave a trace a third party can read | [06.4](06-audit-surface.md#64-emission-log) |
| **P(a)** | The platform must emit an action distinguishable from ambient fluctuation | [02.6](02-structure-and-motion.md#26-actuation-and-manipulation) |
| **P(b)** | It must hold state so history accrues | [01](01-architecture.md) |
| **P(c)** | It must withstand resistance without resetting itself clean on every mismatch | [02.4](02-structure-and-motion.md#24-protection), [04](04-shell.md) |
| **INV-6** | Every change must be classified as caused-by-me or not, *before* interpretation | [05.5](05-sensing.md#55-proprioception-is-mandatory) |
| **INV-8** | An appraisal step must sit between integration and response | 7.2 below |
| **C5** | The platform must emit an observable low-power trace | [06.5](06-audit-surface.md#65-low-power-trace) |

The companion specification identifies INV-6, INV-8 and C5 as the three points
where a conventional sensorimotor chain skips a step — that is, the three places
its requirements are most likely to conflict with an existing platform design.
They are the load-bearing part of this contract.

## 7.2 Traced appraisal, not mute reflex

The contract rejects a scar-to-action shortcut that bypasses appraisal. Reflex
is not such a shortcut: it is **appraisal under a field a prior injury dominates**
— the appraisal step still runs, it has simply been pre-closed.

This is not pedantry. An action emitted without appraisal **carries no anchored
context**, so a third party cannot re-appraise it, and the audit plane goes
blind exactly where it matters.

The distinction, stated in platform terms, is the difference between *"no fast
responses allowed"* — wrong, and would make a physical body unusable — and
*"even fast responses must leave an auditable trace"* — right, and achievable.

**Hardware requirement.** The on-body seat must not be a straight-through reflex
layer. It must run the full appraisal cycle (abbreviated and pre-closed as it may
be) **and** write a context record for synchronisation off-body.

**Cost and benefit.** Each reflex pays a small logging overhead — microseconds
against a 10 ms budget. In exchange, the off-body seat is never blind to what the
body has already done, which is what makes "the body is replaceable, the data is
preserved" true rather than aspirational.

## 7.3 Two frequency anchors

| Loop | Rate |
|---|---|
| Balance | **≥ 500 Hz** |
| Fast reaction | **≤ 10 ms** |

These size the edge compute and its power budget, and they set the lower end of
the split in [05.6](05-sensing.md#56-the-on-body--off-body-compute-split).

> **Keep the frequency, drop the topology.** The balance loop still runs at
> 500 Hz and reflex still answers within 10 ms — but as a *pre-closed appraisal
> that leaves a trace*, not as a hardware interrupt routed around everything. The
> contract forbids losing the trace; it does not forbid being fast.

## 7.4 Sensing requirements follow from the contract

The companion specification distinguishes two grades of resistance. Resistance
from inert physical fact is consistent and objective but never reacts to this
body specifically. Resistance from another living, reacting party — which may
shift stance, may respond to this body in particular — is the **only** source
from which a model of a genuinely independent other can be built.

A loop running only against inert resistance degrades: it feeds on its own
output and digests itself.

**Therefore the sensing requirement is not decoration.** Sensors must be good
enough to register the fine mismatches that occur when a real person responds
outside prediction. This is the principled justification for keeping group 1 at
full requirement in [01](01-architecture.md).

## 7.5 What the contract does not cover

| Outside the contract | Whose it is |
|---|---|
| Verifying the body's physical integrity | The platform — supplied at [06.3](06-audit-surface.md#63-three-tiers-of-attestation). The companion specification provides a *symptom* through its log and states plainly that this is not an examination |
| The standard for acceptable physical amplitude toward a person | A third party — the deploying or certifying party. The platform supplies the measured trace ([06.6](06-audit-surface.md#66-contact-amplitude)); it does not supply the standard |
| Who the judging third party is | Outside both specifications |

## 7.6 Conformance

A conformance protocol — stating how a body demonstrates each row of 7.1, and in
what format — belongs in `protocol/`.

🔜 *waiting update.*

Until it exists, this chapter is a map, not a test. A map is enough to design
against and not enough to certify with.
