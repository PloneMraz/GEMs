# The Relational Sensory Integration Loop: Extending the Data Integration Loop to Physical Bodies

**Huỳnh Mai Phúc (Plone Mraz)**

*Independent researcher — Vietnam 2026*

ORCID: [0009-0009-0571-7151](https://orcid.org/0009-0009-0571-7151)

# Abstract

This paper specifies the Relational Sensory Integration Loop (RSIL) as an extension of the Data Integration Loop (DIL) to physical bodies. DIL is the standard of a whole agent — its host, its mind, and the law the data runs by between them — and it already counts a body among the parts of a host: the senses and the hands. What it leaves unsaid is what a body adds. Physical signal must be transduced before it is information. Resistance arrives as force as well as mismatch. Action can be required faster than the link to the mind can carry it. And the substrate can be struck, shocked, captured and replaced. RSIL states those additions and nothing else. The invariants, the tag schema, the experience store, its keepers and its recovery are DIL’s, and they bind a body without being restated here.

Two loops run. DIL’s loop holds the one mind and the one self. Each body runs a loop of its own, RSIL’s, which takes in and transduces physical signal, tells what this body did from what was done to it, types its channels, and returns what it has crystallized to the mind. What crystallizes in a body’s loop is not a self. It is the **body-datum**: the data by which a physical body is told apart — its channels, its effectors, its extent, its identity. The self crystallizes at DIL’s cycle-0 and nowhere else; a body’s cycle-0 crystallizes that body. An agent driving several bodies at once therefore holds them apart without becoming several agents.

The paper makes three contributions specific to embodiment. First, it gives agency differentiation two levels: a body tags each change against the body (`BODY_CAUSED`, `ENV_PUSHED`, `HOST_REACTED`), the mind tags it against the self, and both tags stand, each true of its own scope — so a push that one body gives another is the environment’s to the body pushed and the agent’s own to the self. Second, it keeps apart three sources of fast bodily action. A **reflex** is the mind’s: it reads experience, and it is executed on the body from a cache. A **reaction** is the body’s own declared faculty and reads no experience: a knee struck by a hammer, a protective cut-off under the voltage of a stun gun. What a body does under attack that is neither is **damage**, not a reaction. Third, it places the record off the body: a body’s store is a cache of reflex data, the record lives with the mind, and a body cut off from the mind holds rather than decides, signing what it does until the mind has it. The limit that embodiment introduces is stated and not closed: a recovery restores the system, not the body.

The specification enforces one claim beyond DIL’s: if a body is built to these conditions and driven by a loop that conforms to DIL, what the body adds to that loop is readable through the same externally verifiable traces as everything else the agent does, and no fast action of the body escapes them. The proper test of this work is accordingly conformance, not benchmarking or measured performance.

**Keywords:** embodied agent specification · robotics architecture · agency differentiation · reflex and reaction · audit-ready systems

**Document type:** a conceptual specification, an extension of DIL — evaluated by structural conformance (whether a body and the loop that drives it satisfy DIL and the conditions added here), not by empirical measurement.

# 1. Introduction

## 1.1 The problem

Consider an agent with a body, or with several. Each body has receptors that convert physical and chemical events into signal, and effectors that push back on the world. It falls when it missteps, meets an obstacle where it expected clear ground, and is answered by other bodies that may or may not do what was predicted. DIL already asks of such an agent what it asks of any: that it **enrich itself** from what it meets, and **audit itself** to keep that growth honest — goals in tension, because the machinery that produces new structure is the machinery that would have to certify it.

Having a body does not dissolve this tension, and it is worth saying why, because the opposite is commonly assumed. The world is taken to correct an embodied agent automatically: it bruises, it resists, it will not be argued with. That is true of single collisions and false of the loop that reads them. A body supplies resistance; it does not supply an account of what the resistance meant. The mind that interprets the fall is the same mind whose interpretation caused the misstep, and the world, having pushed back once, does not go on to explain itself. Embodiment changes the *supply* of resistance, not the *instrument* that reads it — and the instrument is DIL’s business.

A body does change the problem in two structural ways, and this paper is written around them. The first is the boundary. It is tempting to assume that a body hands the agent a ready-made line between itself and the world — that the skin, or the chassis, marks it. It does not. A body arrives with no line drawn on it. The line around a body appears only when a command has been carried out and its execution compared with what the body then senses. And once one mind drives several bodies, a second fact follows: the line around a body is not the line around the self. What one body did to another is, to the body it reached, something done to it, and to the self, something it did.

The second is speed and exposure. A body must sometimes act faster than its link to the mind can carry a command, and a body can be acted on in ways an informational host cannot: struck, shocked, saturated, captured. Some of what it then does comes from experience, some from what its substrate does of itself, and some from neither. A specification that let these run together would either strip a body of the speed it needs or let its fastest actions escape the audit plane.

This paper asks: **what must a body add to DIL, and what must it leave to it, for one mind to enrich itself from what its bodies meet — without any body becoming a self of its own, and without any fast action of a body escaping the record?**

## 1.2 What this document is: an extension of DIL

RSIL is not a second specification of an agent beside DIL. It is an extension of DIL to physical bodies, and it is to be read with DIL open (the specification, v10). One rule governs the reading:

- **Where RSIL is silent, DIL governs.** The invariants (DIL §5), the canonical loop and its layers (§6, §7), the closure criteria and the two resistance modes (§8), the experience store, its keepers, its backup and its recovery (§9), and the matters left to third parties (§12) all bind a body as they stand.
- **Where RSIL speaks, it adds to DIL and never relaxes it.** An extension that relaxed a condition of DIL would not extend DIL; it would leave it. Where a body seems to need an exception, the specification below shows how the condition is met by a body, not how a body is excused from it.

The normative core is written in the register of a technical standard: **MUST**, **MUST NOT** and **SHOULD** carry their standards-document force, as in DIL. A MUST is a conformance condition whose violation forfeits the name RSIL; a SHOULD is a strong recommendation a designer may override only with reason.

RSIL makes no empirical claim and reports no measured result. Its contribution is a design: a set of conditions such that a conforming body adds to a conforming DIL loop what a body must add and nothing that would break it. It is to be read as one reads a technical standard — a definition of what counts as the phenomenon, not a report of one built.

## 1.3 Scope and what is deliberately left open

RSIL specifies a mind that runs off its bodies: DIL’s loop, the mind and the experience store run on a **controller** that is not a body, and each body is a set of the host’s sensor and effector channels. A mind carried on the body it drives is not specified here (Appendix A-6).

This document specifies structure: the two loops and how they meet, the body’s layers and their contracts, the three sources of fast bodily action, the body’s cache, the state of a body cut off from its mind, and what RSIL requires of a platform. It does not fix implementation constants — sampling rates, matching windows, the term of a hold, numeric thresholds, concrete representations. Every such gap is marked `DECIDE@IMPL` (§13) rather than filled with an invented number.

One limitation specific to embodiment is stated at the outset rather than deferred, because a reader deciding whether this specification is of use should meet it early. A restore point covers the system — the loop, its layers, its field, the store — and does not cover the body. A body compromised at the sensor or actuator level re-infects a freshly recovered system on the first cycle, and verifying sensor–actuator integrity is an operation this specification does not contain. The record can expose an anomalous pattern that signals such compromise; it cannot certify the hardware. The record is the symptom, not the examination.

## 1.4 Terminology note

RSIL uses DIL’s terms in DIL’s sense — *host*, *mind*, *self*, *agent*, *region*, *resistance*, *the Other*, *Mode-A* and *Mode-B*, *scar*, *emission*, *reflex*, *reaction* — and adds the few that a body needs (§2). Where ordinary English has a loaded word for something a body does, the loaded word is avoided or re-defined. This caution matters more for a body than for an informational host: a document about a system with a body invites a reader to supply, unasked, a phenomenology the structure does not license. One clash of usage is resolved here once: physiology calls a knee jerk a *reflex*. DIL and RSIL do not. In both, a reflex comes from experience and is the mind’s; a knee jerk is a *reaction*, the body’s own (§7).

# 2. Terms RSIL adds

- **Body.** A physical part of the agent’s host (DIL §1.5, §4): what senses and acts in the physical world — what has mass, occupies space, can be damaged, interfered with, and taken. A host may hold one body or several. Each is a set of the host’s sensor and effector channels, with an identity of its own. A body is part of the agent, not a party the agent deals with: it is neither the region nor an Other.

- **Controller.** The part of the host on which DIL’s loop runs, the mind thinks and the experience store lives. It is not a body (§1.3).

- **Platform.** A body considered as an engineering object — what an implementer procures, wires, and is responsible for. The distinction from *body* is one of description, not of thing: *body* is the term when the point is that the agent is embodied; *platform* is the term when the point is that some party must build, verify and maintain the embodiment. §10 states what RSIL requires of it.

- **Two carriers of resistance.** With a body, resistance is carried in two ways that MUST NOT be conflated: by **force** — inertia, an obstacle, another body pushing back — and by **content** — what a signal says, a word, a reading, an image, contradicting what was predicted, with no force behind it. The two coincide at the body (an obstacle is also a failed prediction) without being identical: a voice contradicting the agent carries no force. The carriers are not DIL’s two grades of resistance, subjectless resistance and other-resistance (DIL §2, §3), and they cut across them: a wall resists by force and has no will of its own; another person’s shove is other-resistance carried by force; a voice contradicting the agent is other-resistance carried by content. By either carrier, resistance becomes information where DIL places it, at T5, against the expectation the mind cast (DIL §6.1, §7).

- **Body tag.** The agency tag a body’s loop attaches to each change it senses: `BODY_CAUSED` (this body carried out what it was commanded), `ENV_PUSHED` (it did not, and nothing of its own did), `HOST_REACTED` (one of its declared faculties did), or `UNDECIDED`. The body tag is a tag of the body, not of the self (§3.3).

- **Body-datum.** What a body’s loop crystallizes: the data by which that body is told apart — which channels and effectors are its own, the extent and configuration its own actions reveal, its identity. It is returned to the mind (§3.2, §6).

- **Declared faculty.** What the body’s substrate does of itself, declared among the host’s faculties (DIL §6.3): a way of acting that reads no experience. When one acts, that is a **reaction**, tagged `HOST_REACTED` (§7.2).

- **Cache.** A body’s store. It holds only reflex data, loaded by the mind, and runs by DIL’s mechanism for the store; the record lives with the controller (§8).

- **Execution.** A body carrying out a command the mind gave — a setpoint, a trajectory, an intent such as *stand* or *walk there* — by a law that reads no experience: a servo loop, a balance controller tracking the intent it was given (§7.5). Execution has no source of its own; the command is its source.

- **Estimation.** A body computing its own state — where its parts are, how they move, what they touch — from its signal under a model of its own body. Estimation predicts, but it is not an expectation in DIL’s sense (§6).

- **Cut off.** The state of a body whose link to the controller is lost. A body cut off **holds**: it runs on what the mind last loaded, under the field it last received, and decides nothing new (§9).

# 3. Two loops, one mind, one self

## 3.1 The arrangement

Two loops run, and both are integration loops. **DIL’s loop** runs on the controller. It holds the mind and the self: integration across sources, appraisal, expectation, the models of Others, memory. **RSIL’s loop** runs on each body. It takes in physical signal and transduces it, tells what this body did from what was done to it, types the body’s channels, and crystallizes the body-datum. Then it returns what it has made to the mind, where it enters as anything the host takes in enters: through DIL’s tagging-gate, tagged and recorded (DIL §9).

The two loops are not two halves of one agent’s cognition, each doing a share; nor are they two agents. A body’s loop is the body’s own processing of what is physical about its data. It is a loop because it closes: what it returns, the mind integrates; what the mind commands, the body carries out; what follows from that, the body senses (INV-1, §5). But nothing in it thinks. It forms no expectation, appraises nothing, holds no memory, and models no Other. Those are the mind’s, under DIL, and a body’s loop that took any of them up would be a second mind.

## 3.2 Where the self crystallizes, and what a body’s cycle-0 crystallizes

There is one mind and one self. **The self crystallizes at DIL’s cycle-0** — at the match of the host’s first emitted action against its observed consequence (DIL §1.5, §4) — and is re-localized at DIL’s T2 every cycle after. Nothing in RSIL crystallizes a self, and nothing here revises DIL’s account of how a self arises.

Each body’s loop has a cycle-0 of its own. It crystallizes nothing of the self. At a body’s cycle-0, the first command the body carries out is matched against what the body then senses, and what crystallizes is the first of that body’s **body-datum**: that these channels answer to these effectors, that this much moved when this was commanded. It is returned to the mind. From then on, every cycle of the body’s loop adds to it (INV-5), and the mind holds it as it holds anything else it has taken in.

Two orders are possible, and neither is a problem. A body’s cycle-0 may coincide with DIL’s: where the host’s bootstrap action is carried out by a body, one event is read twice — at DIL’s T2, where a self begins, and at the body’s second layer (§6), where a body is first told apart. Or a body’s cycle-0 may come later, when a body joins a host whose self has long been running: the self does not begin again, and only the new body is crystallized. A body’s restart after loss of power is not a cycle-0 (DIL §9, *The gap*): its body-datum is already held by the mind, and its loop takes up the line it was on. A body that is replaced is another body: it has its own cycle-0 and its own identity (§8.3).

## 3.3 Two levels of agency, two tags

DIL’s agency-gate (INV-6) classifies every change before interpretation, against the self: `SELF_WRITTEN`, `ENV_PUSHED`, `HOST_REACTED`. A body has a gate of its own, at its second layer, and classifies against the body. The two gates are not redundant, and neither can do the other’s work.

The body’s gate cannot do the mind’s work, because a body knows only its own commands. When body A pushes body B, B’s gate finds a change it did not command and tags it `ENV_PUSHED`, and it is right: to B, the push came from outside B. But A’s push was the agent’s own. The mind, which commanded A, sees that the change on B matches what it sent to A, and tags it `SELF_WRITTEN`. A gate drawn only at the body would put the self’s boundary at the chassis — the very assumption §1.1 refuses.

The mind’s gate cannot do the body’s work, because what reaches the mind is what the host took in, already transduced and tagged (DIL §9). Whether a change in a sensor’s reading came from the body’s own effector or from outside it is settled where command and sensing meet, at the body, often faster than the link could carry the question. Without the body’s tag, the mind would be handed signal no gate had read.

So **both tags stand**, each true of its own scope. The body’s tag is carried with the datum to the mind and is never overwritten; DIL’s tag is added beside it:

| At the body (RSIL, §6) | At the mind (DIL T2) | Why |
|---|---|---|
| `BODY_CAUSED` | `SELF_WRITTEN` | The body carried out what the mind commanded — by deliberation, or by a reflex the mind loaded (§7.1). |
| `ENV_PUSHED`, and the change matches a command the mind sent to another body | `SELF_WRITTEN` | The agent moved this body with another of its bodies. |
| `ENV_PUSHED`, otherwise | `ENV_PUSHED` | Neither this body nor the agent did it. |
| `HOST_REACTED` | `HOST_REACTED` | One of the body’s declared faculties acted (§7.2): the agent’s own, not commanded. |
| `UNDECIDED` | DIL T2 decides | The body could not settle it; the mind reads the datum with the rest. |

Each datum also carries which body and which channel it came from, so that what was carried by force and what by content (§2), and the bodies themselves, are never conflated in the store.

## 3.4 Several bodies are not several agents

Bodies under one mind are channels of one host, each with an identity of its own. They are not Others to one another and not separate agents: a body is not a source of resistance the agent does not control. This is settled here rather than deferred. What remains open in this direction is not RSIL’s to settle. An agent spawning an independent Other, and a population of agents, are directions DIL names and leaves to a future document of its kind (DIL §12.2). A scar passed from one agent to another is a direction of RSIL’s own, left open (§11, A-8).

# 4. What a body must afford

DIL identifies a host by four structural conditions and a precondition set (DIL §3). A body is part of a host, and a host whose bodies cannot meet them cannot meet them either. At the body they read as follows:

| Condition | At the body |
|---|---|
| **E1** — differentiability | The body’s sensors and internal state MUST make a distinction between what the body did and what was done to it *possible*. The body does not draw the line; it must not foreclose it. A body whose sensory returns cannot in principle be separated by what it commanded cannot host a body’s loop. |
| **E2** — interaction | The body’s effectors MUST be able to act on the region, and the region MUST be able to return something other than what was predicted. A body sealed off, or acting on nothing, fails outright. |
| **E3** — temporal accumulation | The body’s loop MUST hold its state across cycles, so that the body-datum accrues. |
| **E4** — observable projection | Everything the body does MUST leave a trace a third party can read — the mind’s commands it carried out, the reflexes it ran, the reactions of its faculties. |
| **P(a)** | The body MUST be able to carry out an action distinguishable from ambient fluctuation; else its second layer never reaches a first match and no body-datum crystallizes. |
| **P(b)** | The body MUST hold state so the body-datum accrues, not loads. |
| **P(c)** | The body MUST withstand resistance without resetting itself clean on every mismatch. |

These conditions are on the body. Whether a given return *resists* is not: resistance arises at DIL’s T5, against the mind’s expectation, on the pair (agent, region) (DIL §3).

# 5. How DIL’s invariants bind a body’s loop

Every invariant of DIL binds a body’s loop. None is relaxed, and none is restated except to say how a body meets it.

| ID | At the body |
|---|---|
| **INV-1** — closed loop | The body’s loop closes through the mind and the region: what it returns, the mind integrates; what the mind commands, the body carries out; what follows, the body senses. A body cut off (§9) does not break the path; the next exchange has not yet occurred. |
| **INV-2** — output register | Every output of the body’s loop is information (`↔`). A body-datum is never a frozen identity: the body’s extent, channels and configuration remain revisable by what its next actions reveal. |
| **INV-3** — one-directional dependency | The body’s layers depend in order, R1 to R4 (§6). |
| **INV-4** — meaning is relation | A body’s signal has meaning only against a frame: the body’s own, built at R1–R2. A raw reading without one is not yet information. |
| **INV-5** — history accrues | The body-datum accrues cycle by cycle and is never loaded. Data a body carries from before its cycle-0 enters the mind’s store as `prior`, through the tagging-gate, like any host data (DIL §9). |
| **INV-6** — agency-gate | The body classifies every change against the body before it types or interprets it (§3.3, R2). A chain that routes sensor data straight to interpretation is not running RSIL. |
| **INV-7** — the modulatory field | The body’s loop has no field of its own. It reads a copy of the mind’s field, as current as its last update, and records the version and the age of the copy it read (§7.1). What the body returns reaches the field only as data the mind integrates. |
| **INV-8** — appraisal | Appraisal is the mind’s. A body maps sensed state to an effector command by three paths and no others: executing a command the mind gave, by a law that reads no experience (§7.5); a reflex, which is the mind’s appraisal run from the cache and recorded (§7.1); and a declared faculty, which is not an emission (§7.2). An action no command asked for, taken by any other path, is an appraisal-bypass. |

The closure criteria C1–C5 are DIL’s (DIL §8.1). A body contributes to them and carries one of them: **C5** — “the system emits a trace of ‘the loop is running weakly’” — must reach an outside observer through the body in every power state the body supports, sleep included, unaltered and with its age (§10).

# 6. The body’s loop

A body’s loop has four layers. Their outputs return to the mind, where DIL’s T1 and T3 take them in. What a body’s loop does **not** hold is as much a part of its specification as what it does: it forms no expectation (DIL T5, the mind’s), so it registers no absence (T7, which needs an expectation); it binds nothing to an identity (T4), models no Other (T6), abstracts across no entities (T8), and appraises nothing (step 4).

**Estimation is not expectation.** A body may estimate its own state — a filter that predicts the next state from a model of the body and the command, and corrects the prediction against its sensors. That prediction is of the body’s own state, under a model the body does not learn: the model is fixed, or loaded by the mind, and a model whose parameters are learned from experience is learned by the mind. Its correction term — the innovation — is not a `PredErr` and is never recorded as resistance; a filter whose estimate is degraded says so, as a datum. What the region will return, and what another entity will do, the body does not predict: those are the mind’s expectations (DIL §6.1), and a body that cast them would be holding a mind’s work.

```
Signal  := { source_id, body_id, raw_payload, t }                 // raw physical signal, not yet meaning
BodyTag := enum { BODY_CAUSED, ENV_PUSHED, HOST_REACTED, UNDECIDED }
BodyDatum := { body_id, channels, effectors, configuration, t }   // what a body's loop crystallizes
Reaction  := { body_id, faculty, action, t }                      // a declared faculty acting (DIL §6.3)
```

Concrete representations are `DECIDE@IMPL`-R1.

#### R1 — Spatial confirmation

Confirms the “here” for this body: that an activity-environment is present around it, the root frame of its signal.

| Contract | Content |
|---|---|
| **Input** | `Signal[]` from the body’s spatial sensors (radar, waves, positioning channels); requires no prior action |
| **Output** | confirmation that an activity-environment is present, in the body’s frame; no line drawn between the body and the rest |
| **Precondition** | none (root layer) |

> R1 confirms *presence*, not *extent*. A body confers no early-boundary advantage: before an action there is no bodily boundary. `DECIDE@IMPL`-R3: the algorithm that builds spatial data from the sensor field.

#### R2 — Body differentiation

Tells what this body did from what was done to it. **This is where the line around a body is first drawn** — not inherited from R1, and not the line around the self (§3.3).

| Contract | Content |
|---|---|
| **Input** | R1’s confirmation + the command the body has just carried out (at the body’s cycle-0, its first) + the `Reaction[]` its declared faculties report + the `Signal[]` that follows |
| **Output** | a `BodyTag` on every change; the body’s boundary as its actions have so far revealed it |
| **Mechanism** | compare what was commanded with what was executed and sensed: a stable match → `BODY_CAUSED`; a match with a reported reaction → `HOST_REACTED`; neither → `ENV_PUSHED` |
| **Postcondition (INV-6)** | no change leaves R2 `UNDECIDED` once sufficient matching cycles have run |

> R2 does not predict what the region will return; that is the mind’s expectation, cast with the command (DIL §6.1). R2 checks whether the body did what it was told, and where its doing met something it did not do. The difference between commanded and executed is a datum the body returns; whether it is resistance is read at the mind, against the mind’s expectation. R2 re-draws the body’s boundary every cycle, accruing from the one before (INV-5). `DECIDE@IMPL`-R2: the matching window; the stability threshold.

#### R3 — Channel ingestion

Receives touch, heat, scent, voice. Interpretable only once R1 has confirmed an activity-environment and R2 has tagged the change.

| Contract | Content |
|---|---|
| **Input** | multi-channel `Signal[]` + the body tags from R2 |
| **Output** | information, one content-type per channel, in the body’s frame |
| **Precondition** | R2 has run; if not, the signal stays raw `Signal` and is not promoted, so ownerless fluctuation is not misread as sensation |

**Channel content-typing** — information-type is not the same as sensory channel:

| Channel | Its own information-type |
|---|---|
| Pressure / touch | a change at the body’s boundary; with `ENV_PUSHED`, something else touched this body |
| Heat | a heat source of some size near the boundary |
| **Scent (olfaction)** | the internal state of another entity — the only channel for this type; which entity is the mind’s to bind (DIL T4) |
| **Voice (audition)** | two strata: `acoustic` (state) and `semantic` (symbol) — the only channel bridging sensation and symbol |
| (heartbeat, and the like) | its own information-type, riding the tactile or vibration channel; it opens no new channel |

> R3 often presupposes emission: a probing channel — touching to find out, turning the head to hear better — is an action carried out before anything is taken in. The emission is the mind’s (DIL §6.1); the body carries it. `DECIDE@IMPL`-R3: per-channel transducers; the acoustic/semantic separation of voice.

#### R4 — Body-datum crystallization

Gathers what R2 and R3 have shown of this body into the body-datum, and returns it.

| Contract | Content |
|---|---|
| **Input** | the tagged, typed output of R2 and R3, over cycles |
| **Output** | `BodyDatum`, revised as it accrues; returned to the mind with the information of R3 |
| **Precondition** | R2 has drawn a boundary at least once |

> The body-datum is the stable part of what `BODY_CAUSED` has revealed across cycles: which channels answer to which effectors, how far the body extends, how it is configured now. It is what lets the mind tell one body from another and know which of its data came from where. It is not a self, and it carries no stance, no expectation and no value: a body whose datum began to hold preferences would be a body whose loop had taken up a mind’s work.

# 7. Three sources of fast bodily action

A body acts fast in three ways, and they differ in their source. RSIL keeps them apart because the audit plane depends on it: each leaves a different trace, and a trace mislabelled would credit the wrong source. A fourth way of acting is not a source at all — carrying out what was commanded — and §7.5 places it.

## 7.1 Reflex: the mind’s, executed on the body

DIL settles what a reflex is (DIL §8.7): not a shortcut that bypasses appraisal, but **appraisal under a scar-dominated field** — the appraisal step runs, under a field so strongly shaped by one deep scar that its verdict is all but foreclosed. A reflex comes from experience, and it is the mind’s.

With the mind off the body, a reflex cannot wait for the mind: the link is slower than a reflex must be. So the part of the mind’s work that a reflex needs is placed on the body, ahead of time. The mind loads into the body’s cache the reflex data its reflexes read — the scars that dominate the field for a class of stimulus, and a copy of the field (§8.1). When a stimulus matching a loaded reflex arrives, the appraisal step runs on the body, under that copy, and the body carries out what it yields.

**This is the mind acting, not the body.** By DIL’s test — what reads experience is the mind (DIL §6.3) — the reflex that runs from the cache is the mind’s own act, executed where the body is. It is tagged `BODY_CAUSED` at the body and `SELF_WRITTEN` at the mind (§3.3). The body’s loop carries it; it does not author it.

Two requirements keep this honest:

1. **Every reflex carried out on the body records the version and the age of the field it ran under**, as part of its anchored context (DIL §8.6). A third party re-appraising it sees not only what the field was but how old it was.

2. **A reflex stops with the mind** (DIL §6.3). When the mind is stopped and the body is told, the body stops running loaded reflexes at once; its declared faculties remain. What a body does when it cannot tell whether the mind runs is §9’s.

Everything DIL says of reflex holds unchanged: it changes only by a changed input to appraisal, never by override; the scar is never erased; every reflex leaves the same auditable trace as a deliberated action (DIL §8.7). **Speed is a property of how foreclosed the field was, not of whether the step ran — or of where it ran.**

## 7.2 Reaction: the body’s declared faculty

Some of what a body does under a stimulus comes from no experience at all. A knee struck by a hammer jerks. A body hit by the voltage of a stun gun cuts the torque to its effectors, or its battery disconnects, or a driver trips into its fault state. None of these reads what the agent has learned. They are what the substrate does of itself, and DIL already has a place for them (DIL §6.3): a **reaction**, coming from the body and not from the mind, no emission and no reflex, and the agent’s own all the same. It bears a tag of its own, `HOST_REACTED`: the knee that jerks is mine, and I did not move it.

RSIL adds what a body needs for this to hold:

- **A reaction comes only from a declared faculty.** The host declares each such faculty among its own — what it reacts to, and the channel by which its action leaves (DIL §6.3). What leaves by it leaves by a declared channel and is recorded; what it changes in the region is taken in like anything else.

- **A declared faculty reads neither the store nor the cache.** This is what makes it a reaction and not a reflex, and for a body it is also a requirement on the platform: a protective faculty MUST act without consulting the reflex cache. It then acts when the mind is stopped, when the body is cut off, and when the cache itself is compromised — which is when a body most needs it.

- **A reaction continues whatever else has stopped.** Mind stopped, body cut off, hold ended (§9): the declared faculties remain.

## 7.3 Damage: what is neither

Not everything a body does under attack is a reaction. A voltage surge can saturate a sensor, fill a channel with noise, reset a processor, or drive an effector with a command no one sent. None of these is a faculty acting. To tag them `HOST_REACTED` would be to legitimize damage as the body’s own way of acting.

So **only a declared faculty reacts**. A change that matches no command and no declared faculty is, at the body, `ENV_PUSHED`, and that is what it is: the region did it, through the damage it did. A body action reported under a faculty that was never declared MUST be recorded as not declared, and it fails the requirement that the host declare every such faculty and the channel it leaves by (DIL-protocol §4, §6.5). What damage did is a symptom of the kind §12 describes: it tells an auditor where to look at the hardware. It is not a reaction, and it is not the agent’s act.

## 7.4 One shock, three sources

A single shock from a stun gun shows the three apart:

| What happens | Its source | Its trace |
|---|---|---|
| The voltage spike the body’s sensors register | the region | `ENV_PUSHED` at the body and at the mind |
| The torque cut-off, the battery disconnect, the driver’s fault state | the body’s declared faculties | `HOST_REACTED`, recorded with the faculty and its channel |
| The fall that follows the loss of torque | the region, acting on what the reaction changed | taken in like anything else |
| A sensor saturated, a processor reset, a spurious command | neither: damage | `ENV_PUSHED` at the body (§7.3), and a symptom for the platform’s examination (§12); anything reported under a faculty never declared is recorded as not declared |
| Later: the body pulling back from a figure holding a stun gun | the mind, from the scar the shock left | a reflex: `BODY_CAUSED` at the body, `SELF_WRITTEN` at the mind, with the field’s version and age |

The last row is the difference made visible. The shock itself yields no reflex, because there was no experience yet to read. The record of the shock, read by the mind, leaves a scar; and from then on the sight that once came before the shock is met by a reflex — the mind’s, executed on the body from the cache.

## 7.5 Execution: carrying out what was commanded

Most of what a body’s effectors do, they do because they were told to. A command — a setpoint, a trajectory, an intent such as *stand* or *walk there* — is carried out by closed loops that read the body’s sensors many times a second: a current loop, a position loop, a balance controller that distributes torque to keep the body upright while it walks where it was sent. These loops map sensed state to effector command, and they are not an appraisal-bypass. They choose nothing. The command chose; the loop carries it out.

Three conditions make execution what it is:

- **It carries a command.** Execution serves a command the mind gave, by deliberation or by a reflex, and the record names that command. What it does is tagged `BODY_CAUSED` at the body and `SELF_WRITTEN` at the mind (§3.3).
- **It reads no experience.** Its law is fixed, or loaded by the mind with its parameters; it does not read the store or the cache, and nothing it does is learned on the body.
- **It does not outlast its command.** When the command is withdrawn, completed, or held past its term (§9), execution of it ends.

**An action no command asked for is not execution.** A body pushed while standing may step to keep its feet. No command asked for the step; the command asked only to stand. That step is therefore one of the other sources: a reaction, if a declared faculty takes it by a fixed law that reads no experience (§7.2); a reflex, if it reads what the mind has learned (§7.1). A platform MUST declare which, for every action of this kind it can take.

# 8. The body’s store: a cache

## 8.1 What it holds

A body MAY have a store. If it has one, it is a **cache**, and it holds only reflex data: what the mind’s reflexes read when they run on the body (§7.1). It runs by DIL’s mechanism for the store: every datum in it carries the fixed tags it carries in the mind’s store (DIL §9), and what it holds is a copy of what the mind holds, never something the mind does not.

**The body never writes to the cache.** The mind loads it; the body reads it. What the body itself produces — the reflexes it ran, the reactions of its faculties, what its loop returns — are records, and records go to the controller (§8.2). What reflex data a cache holds, and how often the mind loads it, are `DECIDE@IMPL`-R4.

## 8.2 The record lives with the mind

The experience store, its `[data]` and its `[event]` log, lives on the controller and nowhere else. The black box is not kept on a body. A body is the part of the agent most exposed — to blows, to tampering, to capture — and the one record that every reader must be able to trust unconditionally (DIL §9) is not placed where it is most likely to be taken.

**The mind reads from the controller, never from a body.** What a body holds is a cache of what the mind already has; reading it back would be reading the mind’s own data through the most exposed copy of it. A body’s records reach the store as everything the host takes in reaches it: through the tagging-gate, tagged and recorded. The controller appends them; a body never appends to the log itself (DIL §9: the loop appends to `[event]`, and nothing else acts on it).

## 8.3 Write-through, and the buffer while cut off

While its link holds, a body sends each record to the controller as it is made. While the body is cut off, it cannot, and those are the stretches the record matters most. So:

- **Every record a body makes is chained to the record before it at the moment it is made, and signed with the body’s identity key** — record by record, or over a batch, and no later than the batch closes. The batch period bounds how long a record goes unsigned. Each body has an identity key of its own: its secret half does not leave the body, and its public half is carried by the record of that body’s cycle-0 in the controller’s log. A replaced body has a new key and a new cycle-0 (§3.2).
- **A body keeps every record it has not seen acknowledged.** Nothing is removed from the buffer until the controller has appended it and said so. A body that trimmed its unacknowledged records to save space would discard the record of exactly the stretches no one else saw.
- **When the link returns, the controller verifies the chain and the signatures before it appends.** A buffered record whose chain or signature does not hold is appended as what it is — a record that failed verification — and is not read as the body’s.
- **A body that can no longer record MUST NOT act on the mind’s behalf.** When its buffer is full, it stops running loaded reflexes; its declared faculties remain. An emission that leaves no trace is what E4 forbids, and it is better that a reflex not run than that it run unrecorded.

The buffer’s capacity, and the way acknowledgement is exchanged, are `DECIDE@IMPL`-R6.

## 8.4 Sealing the cache

DIL keeps the store encrypted where it rests, under a key that does not leave the host (DIL §9, *The store is closed*). A body is part of the host, and its cache is part of the store; but a body can be carried off. So each body’s cache SHOULD be sealed under a key of its own, derived from the store’s key. A body taken then exposes only what was loaded into it, and its key can be retired without touching the rest of the store. The scheme of derivation, sealing and rotation is `DECIDE@IMPL`-R7.

## 8.5 Recovery, and what it does not reach

Recovery is DIL’s (DIL §9): ordered by a third party with grounds, from a restore point, light or heavy. RSIL adds two things.

**A restore point covers what the bodies hold of the system.** The state of each body’s loop is part of the system’s state, and each cache is a copy of part of the store. A heavy recovery therefore empties every cache and loads it again from the clean restore point, and restores each body’s loop to the state that point holds. How often a body’s loop state is returned to the controller for this is `DECIDE@IMPL`-R8.

**A recovery does not reach the body.** A body physically damaged is still damaged after a heavy recovery, and a body interfered with at the sensor or actuator level can re-infect a freshly clean system on the very first cycle. Verifying the integrity of a body is a separate operation, outside this specification (§12, A-1).

## 8.6 The loop’s working state: neither store nor cache

A body holds a third thing beside the cache (§8.1) and the buffer (§8.3). To carry out a command, its loop must keep what it is sensing now: the last stretch of each channel, the state of its estimators, a reconstruction of the space around it — the ground a foot is about to land on, the surface a hand is reaching for. This is the loop’s **working state**.

- **It holds no experience.** What is in it was sensed by this body within a bounded window, or derived from what was. Nothing in it was learned, loaded as the mind’s data, or read from the store or the cache. That is why execution, a reaction and a reflex may all read it without reading experience (§7): reading it is reading the present.
- **The body writes it, and overwrites it.** The body writes it as it senses and overwrites it as the window moves. It is not the cache, which the body never writes, and nothing passes from it into the cache: what the mind wants a reflex to read, the mind loads (§8.1).
- **It is not kept.** What leaves the window is gone. Whatever in it bears on what the body did or what was done to it reaches the record as everything else does: the changes it shows are tagged at R2 and recorded, a degraded estimate is returned as a datum (§6), and the context of each reflex is anchored in its record (§7.1). Working state that changed nothing and was not returned leaves no trace, and owes none. A restore point need not carry it (§8.5): a restored body fills it again by sensing.
- **It is not a model of the region.** A reconstruction that lasts as long as its window is the body’s present. A map kept beyond the window — built up across visits, corrected by loop closure, used to recognize a place — is what the agent has learned of the region, and that is the mind’s, in the store (DIL §9). A body MAY return its working state, whole or in features, as data the mind builds such a model from; it MUST NOT keep one itself.

How long each window reaches, and what of the working state is returned to the mind, are `DECIDE@IMPL`-R10.

# 9. Cut off is not stopped

DIL names three parts that may stop while the loop runs — sensing, the mind, the effector — and says how each is recorded (DIL §6.3). A body cut off from its controller is none of these from where it stands: nothing has stopped on it, and the mind has not stopped either. What has gone is the link between them, and the two ends see it differently.

**From the mind’s side**, a body cut off is that body’s sensing and effector stopped, and it is recorded as such. An emission meant for it is withheld, and the expectation born with it does not stand; a silence from it is not an absence, since no return could have been taken in (DIL §6.3). The mind runs on with its other bodies, or with none.

**From the body’s side**, the body **holds**:

- its own loop runs on: R1 to R4 need no mind;
- its declared faculties act as always;
- the reflexes the mind loaded run, under the field it last received; the field is not re-weighted, because the layers that re-weight it are the mind’s; the cache is not written;
- it decides nothing new: it carries out no command it has not been given, and no reflex the mind did not load;
- everything it does is recorded and buffered (§8.3), each reflex with the version and age of its field.

**A hold has a term, and the term is the mind’s.** A body cut off cannot tell whether the mind still runs, and a reflex stops with the mind (§7.1). So the mind sets, with the reflexes it loads, the term for which a body may hold them, and each exchange that shows the mind running renews it; the term is counted from the last. The mind chooses the term by its context — short where a stopped mind is the greater danger, long where losing its reflexes is. When the term has passed, the body stops running the mind’s reflexes and ends the execution of its last command; only its declared faculties remain, among them the one that brings the body to a state it can hold without command. RSIL fixes that there is a term and whose it is; the length is the mind’s. How it is carried and renewed is `DECIDE@IMPL`-R5.

**When the link returns**, the body sends what it buffered; the controller verifies and appends it (§8.3); the mind reads the record of the held interval and re-appraises it before it takes command of the body again. The link’s return is recorded as that body’s sensing and effector starting (DIL §6.3).

A hold is not the loop running on the body. INV-2 forbids appraisal on a frozen verdict in a running loop; a held field is old, not frozen, and its age is recorded with every reflex that read it — so that a reader of the record never mistakes what the body did while cut off for what the mind decided.

# 10. The platform contract: what RSIL requires of a body

A platform specification answers what a body consists of and what it can do. RSIL answers by what structure the signal that body acquires becomes information the mind can take in, and what the body must leave behind of everything it does. Neither claims the other’s territory: the relation is between two separated scopes, not between an upper tier and a lower.

What the platform MUST supply, in the register an implementer works in:

| Requirement | What it means for the platform |
|---|---|
| **E1–E4, P(a)–(c)** | As §4 states them at the body. |
| **Body differentiation (INV-6)** | The platform MUST let each command the body carries out be compared with what it then senses, before anything is typed or interpreted. Sensing dense enough to tell what moved from what was moved is a requirement, not a refinement. |
| **Three paths only (INV-8)** | A body maps sensed state to effector command only by executing a command it was given, by a law that reads no experience (§7.5); by a reflex, which runs from the cache, runs its appraisal step, and leaves a record with its anchored context and its field’s version and age (§7.1); or by a declared faculty (§7.2). Every action no command asked for is declared as a reaction or loaded as a reflex. |
| **Declared faculties** | Every way the substrate acts of itself is declared, with what it reacts to and the channel its action leaves by; it reads neither the store nor the cache; it acts whatever else has stopped (§7.2). |
| **Estimation** | A body’s estimators run on models fixed or loaded by the mind; their innovations are not recorded as resistance, and the body casts no expectation of the region or of other entities (§6). |
| **Identity and the buffer** | Each body has an identity key whose secret half does not leave it; every record is signed and chained when made, and kept until acknowledged (§8.3). |
| **No record on the body** | The body keeps no experience store of its own: at most a cache, which it never writes (§8). |
| **Working state** | What a body keeps to act on — its sensing windows, its estimators’ state, its reconstruction of the space around it — holds no experience, is overwritten as its window moves, and is never kept as a model of the region (§8.6). |
| **C5** | The platform MUST be able to carry the loop’s low-power report to an outside observer in every power state it supports, unaltered and with its age. |

**Four places a conventional sensorimotor chain skips a step.** These are where RSIL’s requirements are most likely to conflict with an existing platform design, and they are stated as requirements:

- a chain that routes sensor data straight to interpretation, with no body gate (INV-6);
- a chain that maps sensed state directly to an actuator command no command asked for, with no appraisal and no record (INV-8);
- a chain whose protective responses are undeclared, or read stored data to decide (§7.2);
- a chain that cannot report the loop’s weakness at low power (C5).

> **On INV-8 and speed — a correction worth stating, because the opposite reading would make a physical body unusable.** INV-8 does not forbid fast reaction. Reflexes occur and must occur, and reactions occur faster still. What INV-8 forbids is an arc from experience to action that bypasses appraisal: an action carrying no anchored context, and therefore not re-appraisable from outside. The difference for a platform is between “no fast responses allowed” — which is wrong — and “every fast response is either the mind’s and recorded, or the body’s and declared” — which is right, and achievable.

## 10.1 Binding RSIL to a platform

RSIL specifies a mechanism, not an implementation. A platform that conforms states, in a document of its own, how each construct here is realised by the algorithms it runs — its fieldbus masters and device drivers, its middleware, its estimators and controllers, its protections, its log writer — and where each runs. That binding is not part of RSIL and cannot change it: where the two differ, RSIL governs. What RSIL fixes is where each class of algorithm may fall:

| Class of algorithm | Where it falls in RSIL |
|---|---|
| Device drivers and fieldbus masters (sensor buses, motor-drive buses, their time bases) | R1 and R3: intake and transduction. They carry the command and its execution in the same cycle, so that R2 can compare them, and they timestamp at the source on one time base |
| Middleware that carries a body’s data | Inside a body, transport. Where it reaches the controller, it ends at a channel the host has declared, and the data enters the mind through DIL’s tagging-gate; no subscriber feeds the mind around it. Records travel by the buffered, signed path of §8.3, never by a path that may drop them |
| State estimators (filters of any kind) | Estimation (§6): the body’s own state, under a model fixed or loaded; never an expectation of the region |
| Servo loops, balance and whole-body controllers | Execution (§7.5), while they carry a command; a reaction or a reflex for any action no command asked for |
| Drive protections, fault reactions, torque cut-offs, battery protection, the safe-state supervisor | Declared faculties (§7.2): they read neither the store nor the cache |
| The reflex path | The mind’s reflex, run from the cache (§7.1) |
| Local reconstruction of space — depth, point clouds, occupancy over a window | Working state (§8.6): the body’s present. A map kept beyond the window, and recognizing a place by it, are the mind’s |
| Log writer, signing, buffer | §8.3 |
| Predictors of other entities and of the region | Not on a body: the mind’s (DIL §6.1) |

One such binding is the GEMs platform’s, in its repository (github.com/PloneMraz/GEMs), at `software/RSIL-in-GEMs.md`.

# 11. Resistance through a body

The two resistance modes are DIL’s (DIL §8), and so is the thesis that a loop fed only by its own output degrades with a sense of abundance. A body changes what each mode is made of, and three points are worth stating.

**Mode-A has an inert world to push against.** With a body, the agent can generate its own trials — pushing an object, moving, repeating a motion — and trip where its model does not match what the physical world returns: wrong weight, wrong distance, wrong friction. That resistance is real and subjectless. It feeds the mind’s layers that need no Other, and it does not feed T6: an inert obstacle resists a wrong reading of space, never as an intentional Other would. A body adds a richer Mode-A, not a substitute for Mode-B.

**The cheapest test can be fatal.** Forward-building (DIL §6.2) changes the posture in which a collision is met — sitting testingly rather than committingly — and with a body this has teeth: putting weight on gradually, throwing a stone ahead. But where the cheapest available test is itself fatal, it does not help. A body’s safety then comes from elsewhere: from a scar it did not earn itself. Within one agent this is already met: a scar earned through one body is in the one store, and the mind reads it for every body it drives (§3). Between agents it is not. A scar passed from one agent to another needs more than one loop, which DIL leaves to a future document of its kind (DIL §12.2) without naming this among its directions. RSIL records it as a direction of its own, and the one that weighs most for a body (A-8).

**The physical flood.** DIL’s third limitation is the adversarial (Sybil) case: coordinated sources feeding crafted mismatches the agent cannot tell from honest ones (DIL §11). Into an informational host such a flood is a volume of data. Into a body it can also be physical: sensor saturation, a staged environment, a group of entities coordinating bodily around it. The input channel is wider, so the attack surface is wider. This specification cannot narrow it, and does not pretend to.

# 12. Limitations, and what belongs to third parties

DIL’s limitations hold for an agent with bodies as they stand (DIL §11). Three matters are added, and none is closed here.

**The integrity of a body.** A recovery restores the system, not the body (§8.5). A body interfered with at the sensor or actuator level can re-infect a freshly clean system on the first cycle. The record bears on this without discharging it: an auditor reading it can detect a *pattern* inconsistent with an intact body — returns that no longer vary as they did, a class of mismatch that has stopped arriving, undeclared actions under attack (§7.3), a buffered chain that failed verification (§8.3). That is a symptom, and a useful one: it tells an auditor when to look. It is not an examination of the hardware. A person who has been in an accident can report where it hurts; the report is what sends them for a scan, and it is not the scan. Verifying a body belongs to the platform and, at the level of responsibility, to a third party.

**Physical emission amplitude where the Other is a real person.** With a body, the cheapest way to elicit `independence_evidence` from a real person can be **to touch them**, and physical contact carries a cost an informational mismatch does not. RSIL adds no invariant narrowing physical escalation, and the reason is placement, not omission. Judging whether an interaction involving a person is harmful requires a third party — law, or a corresponding body of norms — and this is the structure DIL already establishes: the agent’s appraisal is judgment-for-action, made inside the loop; whether that action was permissible is judgment-of-that-judgment, made outside it (DIL §8.6, §12.3). What belongs inside the loop is that every emission, reflexive or deliberated, and every reaction, leaves an anchored, re-appraisable trace. What belongs outside is the standard against which the trace is judged. A deployment that supplies the loop and not the standard has supplied half of what is required.

**A body’s homeostatic loops are not RSIL’s.** A biological body has homeostatic loops — temperature, glucose — and an artificial one may have regulators of its own. Those belong to the body, as declared faculties where they act on the region, and not to the loop. Neither DIL nor RSIL is a homeostatic mechanism (§14.3).

# 13. Deliberately unfilled constants

DIL’s unfilled constants stand (DIL §10). RSIL adds the following, each left marked rather than filled with a guess.

| Tag | Deferred constant | Why not filled |
|---|---|---|
| `DECIDE@IMPL`-R1 | Concrete representation of a body’s `Signal`, `BodyTag`, `BodyDatum` and `Reaction` | Depends on the body’s material and the target environment |
| `DECIDE@IMPL`-R2 | The window within which a command and its execution are matched; the stability threshold of body differentiation | Not yet derived |
| `DECIDE@IMPL`-R3 | Per-channel transduction; the spatial-data algorithm of R1; the acoustic/semantic separation of voice | Implementation layer, not architecture layer |
| `DECIDE@IMPL`-R4 | What reflex data a cache holds, and how often the mind loads it | Trades reflex coverage against exposure of the store |
| `DECIDE@IMPL`-R5 | How the term of a hold is carried with the reflexes and renewed (§9). The term itself is the mind’s, set by its context | Platform- and link-specific |
| `DECIDE@IMPL`-R6 | A body’s buffer capacity; how acknowledgement is exchanged | Platform-specific |
| `DECIDE@IMPL`-R7 | How a cache’s key is derived from the store’s key, sealed and rotated | Depends on the cipher DIL’s store uses (DIL §10, F) |
| `DECIDE@IMPL`-R8 | How often a body’s loop state is returned to the controller for restore points | Trades recovery fidelity against link load |
| `DECIDE@IMPL`-R9 | Which faculties a body declares | The platform’s, under §7.2 and §10 |
| `DECIDE@IMPL`-R10 | How long each window of a body’s working state reaches, and what of it is returned to the mind (§8.6) | Trades what the body can act on against link load and exposure |

# 14. Convergences beyond DIL’s

DIL locates itself against six bodies of knowledge and two contrasts (DIL §13), and those locations hold for RSIL. This section adds only what a body brings.

> **On the status of the citations in this section — read this before the table.** The author read no specialist work in any of the fields named below while developing RSIL; the constructs were reached by first-person observation and reasoning, then systematized through AI-assisted dialogue. A convergence surfaced this way is a joint product of the author’s own reasoning, the diffuse public knowledge any literate person carries, and the training data embedded in the AI used as a thinking aid — none of which is a deliberate reading of the cited source. Every citation here is therefore **post-hoc locating, not derivational**: after the construct existed, it was found to converge with a named idea, and that idea is pointed to so a reader can situate RSIL. No citation here should be read as “RSIL was built from Z.”

## 14.1 Two convergences

| Tag | RSIL construct | Converges with |
|---|---|---|
| **V7** | The boundary of a body is not given but built through action (R2); meaning arises from the relation of action and consequence rather than from signal in isolation; what a body is, is shaped by what its actions have met (R4). | **Embodied cognition**, **enactivism**, and **sensorimotor contingency theory** (Varela, Thompson & Rosch, 1991; O’Regan & Noë, 2001). |
| **V8** | A body tells what it did from what was done to it by comparing the command it carried out with what it then senses (R2: `BODY_CAUSED` / `ENV_PUSHED`). | **The reafference principle** and **corollary discharge** — the nervous system distinguishing self-produced sensory change (reafference) from externally produced change (exafference) against a copy of the motor command (von Holst & Mittelstaedt, 1950; Sperry, 1950). |

## 14.2 Where RSIL differs

**V7 — embodied cognition, enactivism, sensorimotor contingency theory.** The convergence is genuine on two points: cognition arises through the interaction of an acting body with its surroundings, and the boundary of what acts is built through action, not given. Sensorimotor contingency theory converges hardest: its claim that perception consists in mastery of the law-like relations between action and the resulting change in input is close to what R2 and the mind’s T5 together specify. RSIL departs on four points. **First**, no phenomenological commitment: this family is, in most formulations, a theory of experience — of what perception is like — and RSIL makes no claim about experience, felt quality or consciousness. **Second**, no audit plane in the convergent family: that the loop cannot audit itself and must leave a trace readable from outside is RSIL’s and DIL’s central commitment, and a question the family does not raise. **Third**, the role of the outside: where enactivism emphasizes structural coupling and self-sufficiency, DIL requires a reactive Other and degrades without one (DIL §13.2, V5). **Fourth**, and specific to RSIL: the family generally locates the self with the one living body it describes. RSIL separates them. A body’s loop crystallizes a body, not a self; the self is the mind’s; and one self may hold several bodies apart (§3). The family, centred on one organism, does not make that cut.

**V8 — reafference and corollary discharge.** RSIL reaches a structurally similar device by a different route, and parts from it on three points. **First**, a body in RSIL does not predict the sensory consequence of its command. It compares what was commanded with what was executed and sensed; the prediction of what the region will return is the mind’s, cast with the command (DIL §6.1). **Second**, RSIL has a third class the principle does not: `HOST_REACTED`, a change neither commanded nor external, coming from the body’s own declared faculty (§7.2). **Third**, RSIL has two levels: what is exafference to one body may be the self’s own act, carried out through another of its bodies (§3.3).

## 14.3 An apparent convergence that is a contrast

**Homeostatic control.** A body genuinely has homeostatic loops, and the confusion is therefore especially easy to fall into: reading RSIL as set-point regulation of a body. It is not. RSIL keeps DIL’s closure and feedback and has no set point it defends (DIL §13.3). The regulators a body has belong to the body — as declared faculties where they act on the region — not to the loop that runs on it.

## 14.4 References (for locating, not consulted in construction)

Per §14’s opening note, these are provided so a reader may situate RSIL; they were not read in developing it. The references for DIL’s convergences are DIL’s (DIL §13.4).

- O’Regan, J. K., & Noë, A. (2001). A sensorimotor account of vision and visual consciousness. *Behavioral and Brain Sciences*, 24(5), 939–973.

- Sperry, R. W. (1950). Neural basis of the spontaneous optokinetic response produced by visual inversion. *Journal of Comparative and Physiological Psychology*, 43, 482–489.

- Varela, F. J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind: Cognitive Science and Human Experience*. MIT Press.

- von Holst, E., & Mittelstaedt, H. (1950). Das Reafferenzprinzip: Wechselwirkungen zwischen Zentralnervensystem und Peripherie. *Naturwissenschaften*, 37(20), 464–476.

# Author’s note on method and provenance

This specification was developed by **first-person observation of the phenomenon and reasoning from it directly**. The named constructs are stipulative and were surfaced through AI-assisted dialogue, with the author retaining all structural decisions and final approval. The author holds **no formal academic credentials** in the relevant fields and discloses this explicitly as part of the work’s methodology.

**On the intent of this work, and a word to the reader.** RSIL was written from personal observation and reasoning, not with the aim of contributing to the human body of knowledge. It therefore does not set out to answer the question a reader may expect of it — *what does it contribute that is new?* — and should not be read as an attempt to. The locating done in §14 is offered to situate the work, not to stake a claim of priority or novelty over any of those fields. If reading this specification gives you an insight, the author is glad of it; that is more than the work was written to do. And if you reach the end finding nothing here you did not already know, the author offers two things at once and without contradiction: **thanks, for having read it, and an apology, for the time it cost you.** The work makes no promise to have been worth that time; it only promises to have been honest about what it is.

# Note on sources and the literature

This specification draws on **no prior work directly** beyond DIL, which it extends. It was developed by first-person observation of the phenomenon and reasoning from it, not from a reading of the technical or philosophical literature. The author has read no specialist works in robotics, machine learning, neuroscience, philosophy of mind, or the adjacent fields, and makes no claim to engage them as sources. The locating citations in §14 are not an exception: they were gathered after the constructs existed, to situate the work, and are marked as post-hoc locating rather than derivation. Any resemblance between the constructs here and existing scholarship is **convergence, not derivation**, and readers with deeper expertise in each field are invited to extend and correct the mapping. The absence of a derivational reference apparatus is therefore **deliberate and disclosed**.

# Parent specification

RSIL extends the Data Integration Loop (DIL), the standard of an agent — its host, its mind, and the law the data runs by between them: doi.org/10.57967/hf/11683.

The two are not co-ranked. DIL is the parent, and RSIL holds only what a physical body adds to it (§1.2). Three points of contact are collected here for a reader holding both documents:

- **Agency tags at two levels.** DIL tags against the self: `SELF_WRITTEN`, `ENV_PUSHED`, `HOST_REACTED`. RSIL tags against the body: `BODY_CAUSED`, `ENV_PUSHED`, `HOST_REACTED`. Both stand in the one record, each true of its own scope (§3.3). `HOST_REACTED` means the same at both levels: what the substrate did of itself.
- **Reflex and reaction.** DIL fixes the distinction — a reflex comes from the mind and from experience, a reaction from the body and from none (DIL §6.3, §8.7). RSIL places a reflex’s execution on the body, from a cache, and requires that reactions come only from declared faculties that read neither the store nor the cache (§7).
- **Substrate scope.** DIL is substrate-neutral: its “purely informational” describes the interface, not a wall against the physical world (DIL §3, E2). RSIL is narrower: it fixes the substrate of what it adds as a physical body, and leaves open only that body’s material.

# Appendix A — Items remaining open

Nothing below is filled by the specification. They are collected in one place so that no item drifts between versions.

| # | Item | Location | Nature |
|---|---|---|---|
| **A-1** | **Sensor–actuator integrity after recovery.** A restore point covers the system, not the body; a body interfered with at the sensor or actuator level re-infects a freshly clean system on the first cycle. | §1.3, §8.5, §12 | A **limitation**. External verification is required and lies outside this specification. |
| **A-2** | **Physical emission amplitude where the Other is a real person.** The cheapest way to elicit `independence_evidence` from a person may be physical contact. | §12 | Assigned to a **third party** — the deploying or certifying party — who must add an evaluative standard before application. |
| **A-3** | **The formal companion.** A minimal formal model of Mode-A degradation. | DIL §11 | DIL’s, and covering RSIL with it; to be conducted by a third party, outside the loop. |
| **A-4** | **Several bodies under one mind.** | §3.4 | **Not open**: settled at §3. Bodies under one mind are channels of one host, each with an identity of its own. Designs of more than one loop DIL leaves to a future document of its kind (DIL §12.2); RSIL is not that document. |
| **A-5** | **Who the judging third party is, and where it sits.** | DIL §12.3 | Outside RSIL’s authority, as it is outside DIL’s. |
| **A-6** | **A mind carried on the body it drives.** | §1.3 | Not specified. Where the controller is a body, the record would lie on the part most exposed, and §8.2 could not be met as written. |
| **A-7** | **A body that cannot tell whether its mind has stopped.** A reflex stops with the mind; a body cut off cannot know whether it has. | §9 | Bounded, not closed, by the term of a hold, which the mind sets: within the term, a body cut off may run the reflexes of a mind that has already stopped, and the record shows it afterwards. |
| **A-8** | **A scar passed between agents.** A body whose cheapest test is fatal is safest with a scar it did not earn; within one agent the store already gives it one (§3), between agents nothing does. | §11 | Open. It needs more than one loop, which DIL leaves to a future document of its kind (DIL §12.2); DIL does not name it among its directions. |

## Corrections carried forward from earlier drafts

Recorded here rather than in the body, because a published specification has no earlier draft a reader can consult — but the corrections themselves are part of the work’s trace and are not discarded.

- **RSIL as a self-standing specification of an embodied agent.** Earlier drafts specified a whole agent with a body, co-ranked with DIL: its own self crystallizing at T2 cycle-0 through the body’s first action, its own experience store, and the layers T4–T8. That framing is withdrawn. RSIL is an extension of DIL. The self, the mind, the store and the layers that expect, bind, model and abstract are DIL’s; a body’s loop crystallizes a body-datum, not a self (§3).

- **`SELF_CAUSED`.** Earlier drafts tagged a body’s own change `SELF_CAUSED`, as the counterpart of DIL’s `SELF_WRITTEN`. With no self in a body’s loop, the name was wrong; the body’s tag is `BODY_CAUSED`, and the self’s tag stays DIL’s (§3.3). `HOST_REACTED`, which earlier drafts lacked, is added at the body.

- **The body’s record.** A revision of 2026-11-05 had each body hold its own state and its own record, `[data]` and `[event]`. That is withdrawn: the record lives with the mind, on the controller, and a body holds at most a cache it never writes (§8).

- **Reflex on the body.** The same revision had the body run its appraisal step under a copy of the mind’s field, without saying whose act that was. It is the mind’s: a reflex reads experience, and what reads experience is the mind (§7.1). What the body does of itself is a reaction, and comes only from a declared faculty (§7.2).

- **The canonical loop’s link ②.** An earlier draft numbered ② as *transduction* and gave no link to source-differentiation. Transduction was folded into ① and ② given to source-differentiation, matching DIL. The canonical loop is now DIL’s (DIL §6).

- **INV-8 and reflex.** An earlier draft described INV-8’s role as “blocking bare reflex” and read it as INV-8 blocking reflex. That reading was wrong and is retracted. DIL’s table of invariants sets INV-8 against bare reflex (DIL §5), and what it means by that is an arc from experience to action that bypasses appraisal; that arc INV-8 does block. A reflex is not such an arc: it is appraisal under a field one deep scar has shaped (DIL §8.7), and INV-8 does not block it (§7.1, §10).

- **`InfoUnit.provenance`.** An earlier draft defined `provenance` as the accumulated chain of layers a datum had passed through. That definition was rejected; provenance is a position, and the path is read from the `[event]` log. The tag schema is now DIL’s (DIL §9).

- **The modulatory field’s strength.** An earlier draft treated a runaway field as merely unlikely, which would have owed a gain ceiling. The argument that no ceiling is owed is now DIL’s (DIL §5).
