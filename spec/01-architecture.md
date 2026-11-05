# 01 — Architecture

## The invariant pillar: the controller is off the body

The operating intelligence — the **Main Controller** — sits **entirely off the body**, on an **IPC** (industrial PC) at the control station (Plone, 2026-11-05). It holds the memory, the world model and the accumulated experience, and it decides. It is an agent in its own right, connected to networks directly and acting in the digital world as well as through bodies, and it runs by DIL.

A GEMs **unit** is the Main Controller's sensors and effectors in the physical world. It runs by RSIL, which carries what physical data needs; it holds no mind and decides nothing. A connected unit declares itself to the Main Controller's host as a set of sensor and effector channels with an identity of its own — GEMs01, GEMs02 — as a left hand and a right hand, a thumb and a forefinger, are each one. DIL and RSIL share one relational structure, so the Main Controller runs them as one loop, not two.

On each unit, four tiers execute and none decides:

| Tier | What it does |
|---|---|
| **Real-time Control Layer** | The whole-body loops the link is too slow to close: state estimation, balance at ≥ 500 Hz, reflex within 10 ms, the safe-state supervisor. It executes the setpoints it is given. Runs on the real-time computer, whose processor decision D-3 chooses |
| **MCU** | The per-device loops: each joint's current and position, battery management, the secure element, the beacon |
| **DAQ** | Data acquisition: sensor front-ends, capture and timestamping at source, feature extraction and compression |
| **OBC** | The on-board computer: the kernel for a link to the IPC that lags or is lost. It holds the reflexes and field the Main Controller loads into it, and chooses only among them ([07.5](07-firmware-and-software.md#75-link-loss-and-the-obc)) |

**One source of commands at a time.** While the IPC is online the OBC stands by: powered, receiving what the Main Controller loads, with no command authority. It takes command on one of two triggers — the unit misses the IPC's heartbeat for longer than a threshold, or the Main Controller, judging the link too slow, hands command to it — and gives it back only when the Main Controller takes it back. The Real-time Control Layer runs throughout; only the source of its setpoints changes.

**What a unit holds is its own.** A unit's `[data]` is the state of that unit: what its Real-time Control Layer, MCUs and DAQ record, its calibration, the reflexes loaded into it. Without it the Main Controller could neither read the unit nor drive it. The unit's `[event]` record is signed by its own root of trust. Memory — experience, the world model, what was learned through every unit — is the Main Controller's `[data]` and stays with it. Replacing a unit is replacing a hand: the hand's own sense of where it is goes with it; the one who uses it does not change.

The link carries **processed data, not raw data**. This is not a preference; it is forced by the numbers, and [05](05-sensing.md) shows where.

### What follows

| | Consequence |
|---|---|
| (a) | The control station sits within a few kilometres, on a direct radio link |
| (b) | The uplink is a vital organ. The OBC is mandatory for when it lags or fails |
| (c) | A unit is replaceable, and replacing one loses no memory. What goes with it is its own state and whatever of its record is not yet synchronised; the more processing sits on the unit, the more of that there is. How much processing sits there is `⟦CTRL⟧`, within the two hard ends of [05.6](05-sensing.md#56-the-on-body--off-body-compute-split) |
| (d) | Several units may run against one Main Controller, as limbs of one body. Which units run, and when one takes over from another, is the Main Controller's decision: `⟦CTRL⟧` |

> The trade in (c) is the Main Controller's because it cannot be settled here: how much unit state is acceptable to lose is a judgement about what the units are being used for.

## Application frame

The body is a general-purpose one for a single operator, working in **ordinary social environments**, for the purpose of acquiring physical experience.

**"As human as possible" means sensory bandwidth, not appearance.** The body should acquire every kind of physical information a human body acquires, plus the capacity to reconfigure in ways a human body cannot.

| Group | Level |
|---|---|
| **1 — Sensing and experience acquisition** | **Primary axis.** At or above human. Only the extreme surveillance end is trimmed |
| **2 — Technical manipulation** | Daily tasks and moderate precision, on static objects. Industrial force is out; so is lifting, carrying or dragging a person ([02.6](02-structure-and-motion.md#load-cases)) |
| **3 — Harsh environments** | Civil rescue only: house fires, ordinary-depth water. Vacuum, radiation, deep sea and foundry work are out |
| **4 — Interaction and presence** | **Core.** Safe human contact, social presence |
| **5 — Durability** | One material standard covering everyday physical impact: strikes, knives, vehicle contact, handgun rounds, training impact |

**Where group 1 is trimmed:** everything that enriches direct physical experience is kept. What is reduced is the extreme through-obstacle reconnaissance end. **One deliberate exception:** RF and Wi-Fi sensing keeps its full capability at the hardware level. What it is used for is `⟦CTRL⟧`.

## Architectural baseline

| Property | Choice | Maturity |
|---|---|---|
| Terminal body, intelligence wholly remote | Main Controller on an IPC within a few km, direct radio | **TM** |
| Replaceable unit | Continuous synchronisation with real latency | **TM** |
| Fully solid-state | All-electric, no hydraulics | **TM** |
| Humanoid, ~1650 mm | Real humanoids of this size exist | **TM** |

## Link

| Property | Envelope | Maturity |
|---|---|---|
| Uplink | mmWave / 60 GHz, up to **~8 Gbps**, **~1 ms** PHY latency at ideal short range. Kilometre range needs directional antennas and beam tracking | **TM/LAB** |
| Latency tolerance | An operator adapts below **~170 ms** and can manage up to **~300 ms** | **TM** |
| Fallback | LEO satellite, 5G/6G, VLF underwater | **TM** |
| Security | End-to-end encryption and authentication | **TM** |

> **This is the architectural gate.** 8 Gbps carries many high-resolution sensor streams, but not the full raw sensor set at full rate simultaneously — see [05](05-sensing.md). That single constraint is what produces the two-seat architecture: the body extracts and compresses first, and the link carries what has already been processed.
