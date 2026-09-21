# 01 — Architecture

## The invariant pillar: one intelligence, two seats

The operating intelligence **does not reside entirely on the body**. It is
distributed across two locations:

- **On-body** — reflex loops, balance, sensor transduction and feature
  extraction. Low latency.
- **Off-body** — memory, world model, accumulated experience, long-horizon
  integration.

**One intelligence, two seats. Not two agents.**

The link carries **processed data, not raw data**. This is not a preference; it
is forced by the numbers, and [05](05-sensing.md) shows where.

### What follows

| | Consequence |
|---|---|
| (a) | The control station sits within a few kilometres, on a direct radio link |
| (b) | The uplink is a vital organ. A local core is mandatory for link loss |
| (c) | The body is replaceable — but the more compute sits on it, the more state is lost with it. The split defaults to the middle; the data-loss question is `⟦CTRL⟧` |
| (d) | Several bodies may run against one control system |

> The trade in (c) is not resolved here because it cannot be: how much state is
> acceptable to lose is a judgement about what the body is being used for.

## Application frame

The body is a general-purpose one for a single operator, working in **ordinary
social environments**, for the purpose of acquiring physical experience.

**"As human as possible" means sensory bandwidth, not appearance.** The body
should acquire every kind of physical information a human body acquires, plus
the capacity to reconfigure in ways a human body cannot.

| Group | Level |
|---|---|
| **1 — Sensing and experience acquisition** | **Primary axis.** At or above human. Only the extreme surveillance end is trimmed |
| **2 — Technical manipulation** | Daily tasks and moderate precision. Industrial force is out |
| **3 — Harsh environments** | Civil rescue only: house fires, ordinary-depth water. Vacuum, radiation, deep sea and foundry work are out |
| **4 — Interaction and presence** | **Core.** Safe human contact, social presence |
| **5 — Durability** | One material standard covering everyday physical impact: strikes, knives, vehicle contact, handgun rounds, training impact |

**Where group 1 is trimmed:** everything that enriches direct physical
experience is kept. What is reduced is the extreme through-obstacle
reconnaissance end. **One deliberate exception:** RF and Wi-Fi sensing keeps its
full capability at the hardware level. What it is used for is `⟦CTRL⟧`.

## Architectural baseline

| Property | Choice | Maturity |
|---|---|---|
| Terminal body, intelligence partly remote | Station within a few km, direct radio | **TM** |
| Replaceable body | Continuous synchronisation with real latency | **TM** |
| Fully solid-state | All-electric, no hydraulics | **TM** |
| Humanoid, ~1750 mm | Real humanoids of this size exist | **TM** |

## Link

| Property | Envelope | Maturity |
|---|---|---|
| Uplink | mmWave / 60 GHz, up to **~8 Gbps**, **~1 ms** PHY latency at ideal short range. Kilometre range needs directional antennas and beam tracking | **TM/LAB** |
| Latency tolerance | An operator adapts below **~170 ms** and can manage up to **~300 ms** | **TM** |
| Fallback | LEO satellite, 5G/6G, VLF underwater | **TM** |
| Security | End-to-end encryption and authentication | **TM** |

> **This is the architectural gate.** 8 Gbps carries many high-resolution sensor
> streams, but not the full raw sensor set at full rate simultaneously — see
> [05](05-sensing.md). That single constraint is what produces the two-seat
> architecture: the body extracts and compresses first, and the link carries what
> has already been processed.
