# GEMs — GYNOID ENTITY MODELS

Open-source designs for building a physical robot body.

**Documentation:** https://plonemraz.github.io/vault/gems/

GEMs specifies a ~1.75 m humanoid body whose purpose is to acquire physical
experience on behalf of a controller that does not live entirely on it. It is a
**platform specification**: it declares capability envelopes and the trade-offs
between them, and deliberately leaves the operating point to whoever runs the
body.

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

| Path | Contents | Status |
|---|---|---|
| [`spec/`](spec/) | Platform specification — the capability envelopes and their derivations | ✅ ten chapters |
| [`protocol/`](protocol/) | Platform conformance protocol — how a body demonstrates it satisfies the contract | ✅ v0.1 draft |
| `firmware/` | Device-level and real-time code on the body: sensor and actuator drivers, balance loop, reflex path, energy state machine, secure boot and attestation, low-power trace emission | 🔜 *waiting update* |
| `software/` | Processing of the information and data the hardware acquires: feature extraction and compression, sensor fusion, self-caused/external classification, logging and synchronisation, link management | 🔜 *waiting update* |
| `mechanical/` | Structural CAD, armour layup, joint assemblies | 🔜 *waiting update* |
| `electrical/` | Power distribution, bus topology, sensor harness | 🔜 *waiting update* |
| `sim-model/` | Simulation model | 🔜 *waiting update* |

---

## Roadmap

| Status | Item |
|---|---|
| ✅ | Capability envelopes derived and internally consistent |
| ✅ | Platform contract mapped — every external requirement has a named home in the design |
| ✅ | Audit surface specified: attestation, emission log, low-power trace |
| ✅ | Licensing settled |
| ✅ | Platform specification published in this repository |
| ✅ | Conformance protocol (v0.1 draft) |
| 🔜 | Firmware specification |
| 🔜 | Software specification |
| 🔜 | Mechanical CAD |
| 🔜 | Electrical schematics |
| 🔜 | Simulation model |

---

## Related specifications

GEMs answers *what the body consists of and what it can do*. It is deliberately
silent on how the signal that body acquires becomes structured information —
that belongs to a separate, co-ranked specification.

| Specification | Scope | Status |
|---|---|---|
| **RSIL** — Relational Sensory Integration Loop | The information-processing loop between a body's sensors and its responses | 🔜 *waiting update* |
| **DIL** — Data Integration Loop | The same relational structure for an agent with no body at all | [doi.org/10.6084/m9.figshare.32728983](https://doi.org/10.6084/m9.figshare.32728983) |

Neither document claims the other's territory. The relation is complementary
scopes, not upper and lower tiers.

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

The [platform specification](spec/) is published here in ten chapters, and the
[conformance protocol](protocol/) in draft. Hardware designs, firmware and
software are not published yet.
