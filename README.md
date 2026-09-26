# GEMs — GYNOID ENTITY MODELS

Open-source designs of a physical robot body.

**Documentation:** https://plonemraz.github.io/vault/gems/

GEMs specifies a ~1.75 m humanoid body whose purpose is to acquire physical
experience on behalf of a controller that does not live entirely on it. It is a
**platform specification**: it declares capability envelopes and the trade-offs
between them, and deliberately leaves the operating point to whoever runs the
body.

---

> [!IMPORTANT]
> **This is a paper design. Nothing here has been built.**
>
> The plain reason is money. There is no funding behind this work and no budget
> to buy parts with — the actuator modules §2.6 calls for, a pack of cells, a
> multi-threat armour layup, thirty joints' worth of anything, are simply beyond
> what one person can pay for. So nothing has been procured, nothing has been
> assembled, and no figure in this repository has been measured on hardware.
> What exists is a specification, a conformance protocol, executable models, and
> a component selection drawn from published sources.
>
> Every number below is therefore a **derivation or a citation, never a
> measurement**. The models check their own arithmetic and hold the
> specification to it; what they cannot do is check either against a physical
> body. No amount of internal consistency substitutes for that, and the figures
> should be read as what a body of this description would require — not as what
> one has been observed to do.

---

## Design envelopes

GEMs does not publish one configuration. Structure, actuation and energy sit on
a single coupled loop — armour raises mass, mass raises actuator demand, demand
raises battery mass, battery mass raises mass again — so fixing any one figure
fixes the rest. What the specification publishes is the **envelope and the
trade-off**, not a chosen point on it.

| Property | Declared envelope |
|---|---|
| Height | ~1.75 m |
| Mass | **70–160 kg**, depending on endurance and armour coverage |
| Free-running endurance | Hours, under a **hard ceiling** — past it no convergent design exists at any price |
| Deep-sleep endurance | **~years**, bounded by battery self-discharge rather than by standby electronics |
| Protection | Handgun-calibre ballistic + stab + everyday impact, as one multi-layer package |
| Actuation | 3–5 kW/kg, ~30–36 Nm/kg. Peak power is limited by **the source, not the actuators** |
| Uplink | mmWave, up to ~8 Gbps, ~1 ms PHY latency at short range |
| Sensing | **16–67 Gbps** raw aggregate; ≥2:1 on-body compression is mandatory, ~8:1 realistic |
| Compute | Split between body and external system. Balance loop ≥500 Hz and reflex ≤10 ms **must** be on-body |
| Audit surface | Signed sensor–actuator trace; a readable trace remains emittable at floor power while the body sleeps |

Every figure above is reproducible — `python scripts/gems_budget.py --check`
recomputes them against the chapters that state them.

> [!NOTE]
> Several of these envelopes are bounded by something other than the obvious
> candidate. Peak power is capped by the battery rather than the actuators;
> sleep duration is capped by cell chemistry rather than by the standby circuit;
> tactile fidelity is capped by link bandwidth and fabrication density rather
> than by ambition. The specification states which constraint actually binds in
> each case.

---

## What is where

This repository holds the source: hardware designs, the firmware and software
that run on them, and the specifications they implement. Issues, pull requests
and releases belong here.

The documentation pages are built and published from
[plonemraz.github.io](https://github.com/PloneMraz/plonemraz.github.io) so that
they share the site's navigation and theme. GitHub Pages is intentionally
disabled on this repository — `/vault/gems/` is served by the main site.

Earlier speculative material about GEMs lives under
[/vault/fiction/](https://plonemraz.github.io/vault/fiction/) and is not part of
this repository.

---

## Repository layout

One directory per group, and the body's three design disciplines nest under
`hardware/` rather than sitting at the root beside it.

| Path | Contents | Status |
|---|---|---|
| [`spec/`](spec/) | Platform specification — the capability envelopes and their derivations | ✅ ten chapters |
| [`plan/`](plan/) | What remains between the specification and a complete design: definition of done, open decisions, work packages, and the firmware and software work down to the task | ✅ v1 |
| [`protocol/`](protocol/) | Platform conformance protocol, and an assessment of this repository's simulated body against it | ✅ v0.1 draft + record |
| [`hardware/`](hardware/) | The body itself | ◐ kinematics declared |
| [`hardware/mechanical/`](hardware/mechanical/) | Material and mechanism selection, sourced; CAD to follow | ◐ selection done |
| [`hardware/electrical/`](hardware/electrical/) | Actuator, power, compute and bus selection, sourced, with joint-by-joint sizing | ◐ selection done |
| [`hardware/sim-model/`](hardware/sim-model/) | URDF generated from the kinematics, audited against it | ✅ |
| [`hardware/bom/`](hardware/bom/) | Bill of materials, one row per item the specification names; blanks mark what is not yet verified | ◐ none priced |
| [`firmware/`](firmware/) | Device-level and real-time code: drivers, balance loop, reflex path, energy state machine, secure boot and attestation, low-power trace emission | ◐ architecture; source awaits a target |
| [`software/`](software/) | Processing of what the hardware acquires: feature extraction and compression, sensor fusion, self-caused/external classification, logging and synchronisation, link management | ◐ emission log implemented |
| [`scripts/`](scripts/) | The coupled mass–energy–power loop, executable; checks the figures in `spec/` | ✅ |

Directories marked 🔜 do not exist yet. They are named in advance so that the
place a file belongs is never in question at the moment it is added.

**Firmware and software sit at the root rather than under one heading**, because
they are different disciplines under one specification chapter: firmware owns
deadlines, software owns meaning, and the line between them is load-bearing
enough to show in the layout.


---

## Roadmap

| Status | Item |
|---|---|
| ✅ | Capability envelopes derived and internally consistent |
| ✅ | Platform contract mapped — every external requirement has a named home in the design |
| ✅ | Audit surface specified: attestation, emission log, low-power trace |
| ✅ | Licensing settled |
| ✅ | Budget model, and a check that holds `spec/` to its own arithmetic |
| ✅ | Platform specification published in this repository |
| ✅ | Conformance protocol (v0.1 draft) |
| ✅ | Firmware architecture and the reflex budget split across stages |
| ✅ | Emission log: format, hash chain, batch signing, verifier |
| ✅ | Agency classification by efference copy, with protocol §7.1 run against it |
| ✅ | Conformance assessment of the simulated body — **9 of 16 unmet, and named** |
| ✅ | Kinematic configuration — DOF, arrangement, reach |
| ✅ | Simulation model — 30 DOF URDF, generated from the kinematics and audited against it |
| 🔜 | Firmware source (awaits a target board) |
| 🔜 | Feature extraction, fusion, link management |
| ✅ | Component selection, sourced — actuators, power, compute, bus, materials, reducers |
| ✅ | Actuator torque density reconciled with `f_act` — 75–90 Nm/kg peak over module mass, and the basis now declared |
| ✅ | Work plan to a complete design — decisions, packages, firmware and software task lists ([`plan/`](plan/)) |
| ◐ | Bill of materials — 69 rows from the specification, sources and prices filled only where verified ([`hardware/bom/`](hardware/bom/)) |
| 🔜 | Mechanical CAD |
| 🔜 | Electrical schematics |

---

## Related specifications

GEMs answers *what the body consists of and what it can do*. It is deliberately
silent on how the signal that body acquires becomes structured information —
that belongs to a separate, co-ranked specification.

| Specification | Scope | Status |
|---|---|---|
| **RSIL** — Relational Sensory Integration Loop | The information-processing loop between a body's sensors and its responses | [Read](https://plonemraz.github.io/vault/papers/relational-sensory-integration-loop/) |
| **DIL** — Data Integration Loop | The same relational structure for an agent with no body at all | [Read](https://plonemraz.github.io/vault/papers/data-integration-loop/) |

Neither document claims the other's territory. The relation is complementary
scopes, not upper and lower tiers.

> Both links go to the author's site, which carries the full PDF of each. DOIs
> for these papers are being reissued on a new platform; until they are, cite
> the site copy.

---

## Scope boundary

One division runs through everything here: **the body grants capability and
declares what it costs; the controller decides what to do with it.** Nothing is
cut at the level of the body for reasons that belong to whoever operates it, and
where a value is left blank, the blank is deliberate — it marks a decision that
is not the body's to make.

This repository is the body's side of that division, and only that side. It
covers hardware, the firmware that runs it, the software that turns what the
hardware acquires into information, and the protocols that carry signal between
them. **The controller is not specified here** — not its design, not its
reasoning, not how it will behave. It is addressed in the written introduction,
not in this source tree.

Two conditions hold across everything in this repository. Nothing may call for
physics that does not exist — laboratory work that is expensive, unscaled or not
yet on the market is allowed; invented physics is not. And every capability has
to earn its place by serving what the body is for: gathering physical
experience. Each mechanism carries a mark saying how far it stands from
something that can actually be built.

---

## License

Three licenses, one per kind of work. Full routing in [LICENSE.md](LICENSE.md).

| What | License |
|---|---|
| Hardware designs | [CERN-OHL-S-2.0](LICENSES/CERN-OHL-S-2.0.txt) — strongly reciprocal |
| Firmware and software | [Apache-2.0](LICENSES/Apache-2.0.txt) |
| Specifications and documentation | [CC-BY-4.0](LICENSES/CC-BY-4.0.txt) |

Hardware is reciprocal so that derivative designs stay open; software and
documents are permissive so that the rest of the ecosystem can actually use
them.

---

## Status

The [platform specification](spec/) is published here in ten chapters, the
[conformance protocol](protocol/) in draft, and the parts of the stack that do
not need a target board — the [budget model](scripts/), the
[emission log](software/) and the [simulation model](hardware/sim-model/) — are
implemented and tested. Component selection is sourced and recorded; mechanical
CAD and electrical schematics are not drawn.

**No part of this has been built or physically validated**, and the reason is
the one at the top of this file: there is no money to buy the parts with. The
work is complete as a paper design and untested as a body.
