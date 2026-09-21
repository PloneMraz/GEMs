# Licensing

Copyright © 2026 Plone Mraz.

This repository holds three different kinds of work, and each is licensed under
the instrument built for it. Pick the row that matches the file you are looking
at.

| What | Where | License | SPDX |
|---|---|---|---|
| **Hardware designs** — mechanical and electrical CAD, schematics, PCB layouts, bills of materials, fabrication files | `mechanical/`, `electrical/`, `sim-model/` | [CERN Open Hardware Licence v2 — Strongly Reciprocal](LICENSES/CERN-OHL-S-2.0.txt) | `CERN-OHL-S-2.0` |
| **Software** — firmware and software source, build scripts, tooling | `firmware/`, `software/`, `scripts/` | [Apache License 2.0](LICENSES/Apache-2.0.txt) | `Apache-2.0` |
| **Documents** — specifications, protocols, documentation, this README | `spec/`, `protocol/`, `docs/`, root-level Markdown | [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt) | `CC-BY-4.0` |

Where a file's kind is not obvious from its path, the kind decides, not the
path. A schematic that happens to live next to source code is still a hardware
design.

---

## What each choice means in practice

**Hardware is strongly reciprocal.** If you build a product from these designs
and distribute it, you must make your modified designs available under the same
licence. You may sell what you build; you may not close the designs. This is the
deliberate part of the choice: a body meant to be externally verifiable does not
stay verifiable if its derivatives can be shut. It is also the restrictive part —
an integrator who needs to keep design changes proprietary cannot use this
repository's hardware.

**Software is permissive.** Apache-2.0 lets anyone use, modify and ship the
firmware and software, including in closed products, and it carries an explicit
patent grant from contributors. The reason for not matching the hardware's
reciprocity here is practical: this code has to sit alongside the existing
robotics ecosystem, most of which is Apache-2.0 or BSD, and a copyleft licence
would cut it off from exactly the projects most likely to use it.

**Documents are attribution-only.** The specifications are meant to be cited,
quoted and implemented freely, including by people building something that
competes with this. CC-BY-4.0 asks only for credit. A conformance protocol that
nobody can implement without a licence negotiation is a dead protocol.

> **The audit guarantee does not come from the licence.** Nothing here forces an
> implementer to be honest, and no licence could. What a body must do to be
> called conforming is set by the conformance protocol, not by copyright — a
> body either emits the verifiable trace the protocol requires or it does not
> conform. Copyright keeps derivative *designs* open; the protocol is what makes
> a *running body* checkable.

---

## Contributing

Contributions are accepted under the licence that already governs the file being
changed — inbound matches outbound. By opening a pull request you agree your
contribution is licensed that way.

---

## Notes

Directories listed above may not exist yet. The mapping is stated in advance so
that the licence of a file is never in question at the moment it is added.

`LICENSES/` holds the unmodified text of each licence.
