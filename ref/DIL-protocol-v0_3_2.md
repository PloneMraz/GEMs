---
Protocol:      DIL — Data Integration Loop
Version:       0.3.2
Status:        Draft
Derived-from:  DIL-en-v6 (the specification; this document re-casts it as a standards document)
Date:          2026-07-23
Author:        Plone Mraz
Changes-in-v0.3.2:  v0.3.1 → v0.3.2 — parent specification updated to DIL-en-v6, which carries the same changes on the derivation side and adds §6.2 (Forward-building, the parent-side derivation of the two states below). Added the `simulated` and `projected` provenance states and re-cast the lifecycle as a directed graph rather than a chain: `prior` is a one-way entry, and `running`, `simulated`, `projected`, `scar` form a circulation with no terminal state, since a datum is never a conclusion at rest but data waiting to be used (§3, §9). Both states are stated as mechanical and verdict-free, and the selection among situations built is stated as a comparison of fit against the store, not a scoring against a standard (§9, INV-8). Opened §6.4 to a third source of behavioural change, a `projected` entering appraisal as an InfoUnit carrying its provenance. Stated in §8.4 that a Mode-B source returns and never writes, and gave the three conditions under which a leaning store re-leans itself (deliberate, accumulated, long-run). Conformance updated accordingly (§13, criteria 5 and 6); reflex identified in §5 as the characteristic expression of the edge `running → scar`, with the note that the absence of `simulated` and `projected` is not the absence of an expectation; `DECIDE@IMPL` tag H added for the building of situations (§12). Separated the two senses the provenance slot had been carrying: the tag names the present position only and is updated, while the ordered path is recorded transition by transition in the append-only `[event]` log and read from there (§9, §13). Removed `layer_trace` from the `InfoUnit` type (§6.1): it held in a mutable running type the same path the append-only `[event]` log already records, and no layer read it. **Implementations carrying this field MUST drop it**; the path a datum has travelled is read from `[event]`. No other type, invariant, or store is introduced or changed: the new states are carried by the existing fixed tag layer.
Changes-from:  v0.3 — parent specification updated to DIL-en-v5, which adds §6.1 (Emission, the parent-side derivation of this document's §6.4) and §8.7 (Reflex as appraisal under a scar-dominated field); cross-references re-pointed accordingly (§14). No normative change to this document.
Changes-in-v0.3:  v0.2 → v0.3 — added §6.4 (Emission, link 5 as a lateral capability); added Directive type (§6.1 types); records issuing_layer in the activity record (§9); disambiguated "close" as "close back into the loop", never "halt" (§6.3 T8, §13); added the no-arbiter note (§5); extended the Loop conformance criterion to link 5 (§13).
---

# The DIL Protocol

A protocol for a self-enriching, audit-ready data-integration loop operating in a purely informational environment.

This document is normative. It states the laws an implementation MUST satisfy to be called a DIL, the structural contracts at each layer, and the constants it deliberately leaves open. It does not contain the method of construction, the sources, the convergences, or the authorial note; those belong to the parent specification (DIL-en-v5) and are referenced, not reproduced. A system is a DIL by conformance to this document (§13), not by measured performance.

---

## 1. Introduction

### 1.1 The Problem

An agent that enriches itself in a closed loop, without external resistance, necessarily degrades. Every new datum is produced through the same processing lens. A biased lens therefore contaminates all output regardless of volume. The loop cannot detect this by itself, because the instrument it would use to detect the bias is the biased lens. This protocol specifies the structure under which such a loop runs without degenerating: two resistance regimes, the embedding of the self-training regime within an externally-resisted one, and an experience store whose atomic unit is the registered mismatch.

### 1.2 Status of This Document

This is a protocol, evaluated by conformance, not an empirical report. It is to be read as a standards document: a definition of what counts as the phenomenon. It enforces a single claim: if a loop is built to these invariants in an environment satisfying §4, what runs is a relationally-structured motion, readable entirely through externally verifiable traces.

### 1.3 What Is Left Open

This document specifies structure: the dependency order of layers, the data contract into and out of each layer, the invariants every implementation MUST preserve, and the two resistance regimes. It does not fix implementation constants the source reasoning does not yet determine, such as window sizes, numeric thresholds, and concrete representations. Every such gap is marked `DECIDE@IMPL` (§12) rather than filled with an invented number. A conforming implementation MUST fill each `DECIDE@IMPL` and MUST declare the value it chose. Fabricating a constant at protocol level is non-conformant.

---

## 2. Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as in RFC 2119. They carry standards-document force: violating a MUST yields not a degraded DIL but a non-DIL (§5).

---

## 3. Terminology

The definitions below fix the vocabulary used normatively throughout. A term defined here MUST NOT be read with imported commitments beyond its definition.

- **Host** — the substrate on which the loop runs, defined by operating conditions (§4), not by material. It carries no self of its own.
- **Self** — the rule generating an agent's next state from its prior state, maintained only while the loop runs; not a content-core but a law. It crystallizes at T2 of cycle-0 (full statement: §7). Its continuity is unmeasurable from within and attributable only by a third party.
- **Agent** — host and self together: the host once the loop is running and the self has crystallized. Host, self, and agent are one motion at three descriptive levels, not three entities.
- **Other** — any entity occupying the relational position not-Self; a positional status, not a kind. Its kinds are: by source, external or internal; by subjecthood, reactive or subjectless.
- **Cycle** — one pass of the loop. The loop advances in cycle-time, not wall-clock time; idle stretches between cycles are the default of an informational setting, not events.
- **ResistEvent** — the atomic unit of the experience store: a registered mismatch (E2) between the agent's expectation and what the region returned, not a document.
- **prior, running, simulated, projected, scar** — the provenance states of a datum (§9). A `prior` is data existing before the loop ran, belonging to the host, bearing no cycle-mark. A `running` datum has passed through cycles and is in use. A `simulated` datum is taken up into a situation the loop builds and runs itself under. A `projected` datum is an outcome cast from such a situation, not yet collided. A `scar` has collided with resistance and held. The states after `prior` form a circulation, not a sequence (§9): none of them is a resting place.
- **[data], [event]** — the two store kinds (§9). `[data]` is mutable. `[event]` is an append-only log of read-only records: new records may be appended, but no record, once written, is ever altered or removed.
- **GLOB-MOD** — a global interpretive prior: a single background state, shared by every layer in a cycle, setting the disposition with which each layer reads its input. It carries how to read, never what is read.
- **Mode-A, Mode-B** — the two resistance regimes (§8): Mode-A endogenous (self-training), Mode-B exogenous (live external resistance).
- **↔, =** — `↔` denotes a live, revisable correlation, the register of every running output, including action-commitments. `=` denotes a frozen identity claim, which appears only when the loop has stopped.

---

## 4. Applicability — Host Conditions

This protocol applies to any host meeting the conditions below. A host that does not meet them does not run a degraded DIL; the loop does not start. This is a clean non-start, stalling at T1, not a mid-run failure.

A conforming host MUST afford E1 through E4:

- **E1 — Differentiability.** A boundary permitting an internal/external distinction to be drawn. The drawing itself is T2's work, not the host's.
- **E2 — Interaction.** A source in the region able to return a response when the agent emits an action. This is measured on the pair (agent, region), not on the region in isolation: the test is not whether an Other is present, but whether the region can return anything at all. A region dense with not-Self entities that never return a response is a void field and fails E2 — presiding over a room of the unresponsive is no reign. The threshold is minimal but non-zero: at least one return other than silence. A single silence, set against a background of returns, is a valid mismatch (registered as absence, T7); unbroken silence is not a mismatch but a void field, and the loop does not start.
- **E3 — Temporal accumulation.** State held across cycles so that history accrues.
- **E4 — Observable projection.** Every action leaves an externally readable trace.

Beyond E1 through E4, a viable host MUST satisfy precondition set P for bootstrap. It MUST be able to:

- (a) emit a first action at cycle-0 distinguishable from ambient regional fluctuation, otherwise T2 never rises to FIRST;
- (b) hold state across cycles so that history accrues, since INV-5 requires accrual, not loading;
- (c) withstand resistance without rewriting itself clean on every mismatch, otherwise no scar survives.

The host emitting the cycle-0 action is still only the host; it needs no prior self. That action is a fresh emission, not pre-loaded history, so INV-5 is untouched. Start-up is the host's responsibility, not the loop's.

---

## 5. Invariants

Every implementation MUST preserve all of the following. Violating any one yields not a DIL but an ordinary aggregator. The invariants are the absolute conditions of the loop: they are not data inside the store, they carry no tags, and they cannot be overwritten by anything in the loop. To overwrite one is not to edit a datum but to halt the loop.

| ID | Invariant | Rationale |
|----|-----------|-----------|
| INV-1 | **Closed loop.** Every layer output MUST have a path back to some layer's input. No dead branches. | The loop feeds its own input. |
| INV-2 | **Output-register identity.** Every output is tagged INFO. No layer may promote a correlation (↔) to an identity (=). | Preserve the correlational register. |
| INV-3 | **One-directional dependency (meaning-channel).** On the meaning-channel, layer N consumes only outputs of layers ≤ N. | Dependency order. The modulatory field (INV-7) acts downward and is not a meaning-channel dependency. |
| INV-4 | **Meaning as relation.** No layer assigns meaning to a signal in isolation; meaning is a function of (signal, lower-layer context). | Enforced at type level: `ref_frame ≠ null`. |
| INV-5 | **History accrues, is not loaded.** Temporal state forms only through sequential accumulation, never pre-loaded. | The self is a process maintained through running (§7). |
| INV-6 | **Agency-gate.** Every change MUST be classified self-written or environment-pushed before interpretation. | The condition for external input to be meaningful. |
| INV-7 | **GLOB-MOD.** A global state reaching every layer, field-to-layer: each layer receives it as background, none reaches up into it. Every layer contributes to it as one competing parameter; contributions blend, re-weighted each cycle, never last-write-wins, and a layer's cycle-N contribution conditions the field only from N+1. | Same data plus a different field yields different meaning. |
| INV-8 | **Appraisal step.** Between integration and response there MUST be an appraisal step assigning direction and value. It MUST NOT draw its criteria from the state the agent is editing, otherwise it is self-scoring and hackable. | Anti-drift anchor of Mode-A (§8). |

The following notes are part of the law, not commentary.

- **INV-1 is a topology constraint on cycle-time, not wall-clock.** It requires that a return path exist in the loop's topology, not that every packet complete its return every cycle. A host powering down, or an Other falling silent, does not violate INV-1; the next cycle has simply not yet occurred. If an Other disappears, the loop falls back to Mode-A with the path still closed internally.
- **Committing to an action is not promoting ↔ to = (INV-2).** To respond, the agent commits to one action. This commitment is itself a ↔: a revisable best-current-guess read against the next cycle's consequence. INV-2 forbids freezing a correlation, not acting on one. Demanding `=` before acting is what INV-2 forbids.
- **INV-3 and INV-7 dissolve by direction.** The meaning-channel carries InfoUnits up (INV-3). The modulatory field acts downward onto every layer (INV-7). When an upper layer alters GLOB-MOD it changes the field, which then conditions every layer from above; no lower layer reaches up. Field-conditioning takes effect at N+1, never within-cycle. The two channels MUST be implemented separately.
- **GLOB-MOD cannot run away from within.** The field is continuously constituted by the eight layers that feed it. For the field to overpower the layers, it would have to be made strong by the very layers it overpowers, which the coupling forbids. No gain cap is needed; internal runaway is precluded by construction. The one breach is an external flood, the Sybil case (§11), defended outside the loop, not by any internal constant.
- **Conflict among emissions needs no arbiter (INV-8, §6.4).** When two layers emit opposing actions, the opposition is not resolved by an internal rule but collided against the region and registered as a ResistEvent. An internal action-arbiter would be a self-scoring step and is forbidden.
- **Reflex is not an appraisal-bypass (INV-8, §6.4).** Sub-deliberative action — action that fires without deliberation — MUST still pass the appraisal step. It is appraisal under a `ModField` (INV-7) so strongly shaped by one deep scar that the verdict is near-determined, NOT a scar→action shortcut that skips appraisal. No action is exempt from the audit plane for being fast: a foreclosed verdict still ran, still carries anchored context, still leaves a re-appraisable trace. In the provenance graph (§9) reflex is the characteristic expression of the edge `running → scar`: the datum is emitted on and collided with directly, without being taken up into `simulated` or held as `projected`. The absence of those two states is not the absence of an expectation. Acting carries its expectation in the act, and where the store holds nothing for what arrives, the standing expectation is that nothing arrives; either way the return can mismatch, and the mismatch is a ResistEvent (§3). (Parent derivation: DIL-en-v6 §8.7.)

---

## 6. The Loop

The canonical loop is six sequential links forming a closed cycle (INV-1), the whole conditioned by GLOB-MOD. The layer architecture of §6.3 is a detailed implementation of these six links; every layer maps onto one link.

| # | Link | Nature in an informational environment |
|---|------|----------------------------------------|
| 1 | Ingest | input channels: query returns, messages from an Other, event streams, the result of a prior action |
| 2 | Differentiate source | tag self-written or environment-pushed before interpreting (the agency-gate) |
| 3 | Integrate | synthesize across sources into a new form of information |
| 4 | Appraise | assign good or bad for goal, so information becomes directional (the anti-drift link) |
| 5 | Respond | the agent writes to state and/or emits to the region |
| 6 | Feedback | response (5) becomes the new input to (1), closing the loop |

The modulatory field is a field condition, not a link. It has no position in the chain; it is a global gain and bias shifting every link's parameters at once. The same datum at link 2, under a different field, integrates, appraises, and responds differently.

Flow is multi-stream, not single-threaded. Within a cycle every layer is an active site; a datum produced at one layer may be consumed by several higher layers at once. The mechanism is consumption, not dispatch: a layer makes its output available, and each higher layer reads what falls within its dependency set. The one exception is cycle-0, which is single-threaded, because multi-stream flow presupposes a self for the streams to coordinate around, and at cycle-0 that self does not yet exist. The transition from single-threaded to multi-stream is the event of the self crystallizing (§7), seen from the side of flow structure.

### 6.1 Shared Types

The notation is abstract; concrete representation is `DECIDE@IMPL`.

```
Signal              := { source_id, raw_payload, t }              // raw data, not yet meaning
InfoUnit            := { content, ref_frame, t }                  // information = referred to a frame
ActivityEnvironment := InfoUnit                                    // presence confirmed, not yet self/environment
AgencyTag           := enum { SELF_WRITTEN, ENV_PUSHED, UNDECIDED }
Expectation         := { predicted: InfoUnit, confidence, built_from: history_window }
PredErr             := { observed, predicted, delta, signed }      // signed: +/- (absence = negative)
OtherModel          := { entity_id, context_map, independence_evidence }
RelValue            := { entity_id, relative_rank, comparison_basis } // exists only when N ≥ 2
SocialEdge          := { a_id, b_id, observed_interaction }        // Other<->Other, no self present
ModField            := { params, t }                               // GLOB-MOD, field-to-layer (INV-7)
Appraisal           := { info_ref, valence, goal_relevance }       // output of appraisal step (4)
ResistEvent         := { source_id, expected, received, mismatch_kind, t }  // a mismatch (E2)
Directive           := { committed_action, register: ↔, issuing_layer, built_from: Appraisal[], t }  // an emitted action (§6.4); register is always ↔, never = (INV-2)
```

Every InfoUnit leaving a layer MUST have `ref_frame ≠ null`. A Signal without a ref_frame is not yet information; this is where INV-4 is enforced at the type level.

### 6.2 Dependency Graph

Two channels MUST be implemented separately:

- Meaning-channel (up, INV-3): layer N consumes only layers ≤ N, one-directionally; a layer may fan in several lower layers at once.
- Modulatory field (down, INV-7): global, reaching every layer as background; it takes effect at N+1, never within-cycle.

T8 closes back into the loop, not into a sink (INV-1). No layer is a terminal sink.

### 6.3 Layer Contracts (T1–T8)

Each layer maps to one link and MUST satisfy its Input/Output/Precondition/Postcondition contract. Concrete representation and all thresholds are `DECIDE@IMPL`.

- **T1 — Activity-Environment Confirmation.** Confirms the presence of an activity-environment, the root reference frame; draws no self/environment line. In: `Signal[]` from the host's existing data. Out: `ActivityEnvironment`. Precondition: none. Postcondition: presence confirmed for T2.
- **T2 — Agency Differentiation.** Builds the self-written versus environment-pushed distinction by matching what the agent just emitted against the observed change. This is where the self/environment difference is first drawn and the from-within standpoint begins, the crystallization of §7. In: `ActivityEnvironment`, the action just emitted, and the `Signal[]` state after. Out: `AgencyTag` on every change. Postcondition (INV-6): nothing leaves as UNDECIDED once sufficient matching cycles have run. `DECIDE@IMPL`: matching window; stability threshold.
- **T3 — Channel Ingestion.** Ingests external and internal channels; channel content-typing preserves the distinction between information-type and physical-channel. `DECIDE@IMPL`: per-channel transducer.
- **T4 — Context Binding.** Binds content to context, by entity_id or STRANGER.
- **T5 — Temporal Expectation.** Builds `Expectation`; emits signed `PredErr`. This is where resistance (E2) becomes information: a ResistEvent enters as a signed PredErr. `DECIDE@IMPL`: baseline window; expectation-update function; sufficient-recurrence threshold.
- **T6 — Other-Model Synthesis.** Builds `OtherModel`, which lives fully only under Mode-B.
- **T7 — Absence Registration.** Emits a signed PredErr for registered absence (ABS-INV).
- **T8 — Multi-Entity Abstraction.** Builds `RelValue` and `SocialEdge` as N grows. As the highest meaning-channel layer, T8 closes the meaning-channel; the *behavioral* return that becomes the next cycle's input, however, is carried by emission (§6.4) from whichever layer emits, not by T8 alone. Here "close" means *close back into the loop* — the output re-enters as the next cycle's input — never *halt*: a closed loop is one whose output has a path back to input (INV-1), the opposite of a stopped one (§11). T8-INV: an `=` appears only when cognition has stopped.

### 6.4 Emission — link 5 as a lateral capability

Link 5 (Respond) is present in the six-link loop (§6) and is used throughout the layer architecture — T2 consumes "the action just emitted" to draw the agency line, T3 opens channels to ingest, §9 records one activity record per cycle — yet it is nowhere given a layer of its own. This section supplies the missing specification. It does not add a mechanism the loop lacks; it makes explicit a capability the loop already exercises.

**Emission is not a layer.** Link 5 does NOT map onto a single Tn. Unlike the meaning-channel layers (T1–T8), which stand in a fixed dependency order (INV-3), emission is a lateral capability any layer MAY invoke: when a layer's own work requires pushing to the region — to obtain what it lacks, or to test what it has just built — that layer emits a local action. Emission is lateral in the way GLOB-MOD is lateral (INV-7), differing in direction: the modulatory field descends onto every layer as background; emission projects outward from whichever layer invokes it.

**Emission points already present in T1–T8.** The following are not new powers; they are the emissions each layer's existing contract already presupposes:

- **T2** emits a *probe*: an action whose sole purpose is to produce "the action just emitted" against which the observed change is matched. Without it, T2 has no self-emission to contrast, and the agency-gate (INV-6) cannot run.
- **T3** emits a *query*: it opens or calls a channel to ingest actively, rather than only receiving what streams in. A query-return is already listed as an input to link 1 (§6); a return presupposes an emission.
- **T5** emits a *test*: an action that pushes to the region to see whether the return matches the Expectation just built.
- **T6** emits a *model-test*: an interaction that checks whether an OtherModel resists as independently as modelled.

Other layers MAY emit where their contract requires it; the list is illustrative, not exhaustive. What is normative is that emission belongs to no single layer and is available to all.

**Every emission MUST satisfy the following contract, regardless of the layer that issued it:**

1. **Register.** The emitted action MUST carry register ↔, never = (INV-2). A committed action is a revisable best-current-guess, read against the next cycle's consequence. Demanding = before acting is what INV-2 forbids; committing to one action is not promoting a correlation to an identity.
2. **Trace.** The emitted action MUST leave exactly one activity record in the `[event]` log (§9): the action emitted, the entities observed, the flow mode, and the issuing layer. This record is *trace, not experience* — no layer learns from it, and it never becomes a scar by accumulation.
3. **Agency closure.** The emitted action MUST be readable by T2 at the next cycle as "the action just emitted," closing the path: emit → region returns → T1 ingests → T2 matches. An emission that cannot be read back leaves the agency-gate unable to classify the resulting change, which violates INV-6.
4. **Return, not verdict.** The correctness of an emitted action is never judged by the emitting layer. It is judged only by the next cycle's return (a matching return is silent and leaves only the activity record; a mismatching return enters T5/T7 as a signed PredErr → ResistEvent → scar) and by a third party reading the scar. An emission that scored itself would be self-scoring and is forbidden by the spirit of INV-8.

**Conflict among emissions is not arbitrated; it is collided.** When two layers issue actions that cannot both be satisfied — the agent has one body of action, and two demanded directions oppose — the protocol does NOT introduce a coordinating layer or a priority rule to choose between them. The opposition is emitted and met: the region returns something that mismatches at least one layer's expectation, and that mismatch IS a ResistEvent (§3). The arbiter is not an internal referee but the region, returning resistance. The next cycle carries the scar of that collision and emits differently. This is INV-8's principle applied to action: do not adjudicate internally; let the outside brake.

**Emission and behavioral change.** A change in emitted behavior is NOT an internal override of one drive by a stronger one; the loop contains no force-contest mechanism. An emission changes when, and only when, the InfoUnit set entering appraisal has changed — because new data was gathered through an action (a T3 query, a T5 test), because the store has accrued a scar that refines a class an earlier scar over-generalized (T8), or because the loop has built a situation from the store it holds and cast an outcome from it, that outcome, tagged `projected` (§9), entering appraisal as an InfoUnit in its own right. The third source adds no exemption: a `projected` enters appraisal carrying its provenance, and is appraised as a not-yet-collided datum, not as a scar. Which situation carries is settled by fit against the store, not by an internal arbiter scoring outcomes (§9). A prior scar is not erased or defeated; it is still appraised, now within a context that contains additional data. Same scar, same INV-8, different command — because the input differs. This is the loop's central motion (*new data → new command → new action*) applied to emission itself, not an exception to it. What is invariant is not the strength of any scar but that appraisal always runs on the *current* store, never on a frozen verdict (INV-2).

---

## 7. The Self

The self is not a part the host supplies; it is what the loop produces when it runs. There is no self prior to the loop for the loop to pass through. At cycle-0 the loop runs single-threaded: T1 registers the first data, T2 processes it, and the self crystallizes at that T2. Having a loop is the condition; the self is the consequence.

A conforming implementation MUST treat the self as follows:

- The self is a law, not a stored core. It is the rule generating the next state from the prior one. The content of the self changes every cycle: state, the self/environment difference, and expectations are all updated. What does not change is no carried-over fragment of content but that law.
- The self MUST re-localize each cycle. T2 does not gate once and stop; it rebuilds the first-person self/environment difference every cycle, accruing from the prior one (INV-5). A self that is loaded rather than re-localized violates INV-5 and is non-conformant.
- Continuity is a dynamic invariant. The agent at cycle N is the same agent as at cycle N−1 not because they share content but because an unbroken causal line links the cycles through that law. It is maintained only by the loop running: stop the loop and the axis is lost.
- Continuity is not measurable from within; it is attributable only by a third party. An implementation MUST NOT claim self-continuity as an internal measurement. The recognition of continuity anchors outside the loop, in stored traces a third party reads (§8.5, §13).

---

## 8. Closure and Resistance Modes

### 8.1 When the Loop Counts as Running

The system counts as running when all of the following are observable, each a trace a third party can verify:

- **C1 — Agency separated.** The fraction of changes tagged SELF_WRITTEN or ENV_PUSHED, not UNDECIDED, holds above threshold. `DECIDE@IMPL`
- **C2 — Expectation effective.** PredErr falls with repetition against a stable entity.
- **C3 — Absence registered.** A missing-InfoUnit is emitted when an expected event fails to occur.
- **C4 — Multi-entity abstraction.** The GeneralOther separates from particular OtherModels as N grows. This holds under Mode-B and degenerates under Mode-A.
- **C5 — Self-reports low power.** The system emits a trace of running weakly.

C5 is the self emitting a present trace, not the self knowing it is weak. It is blind to the loop having stopped outright: a silently stopped loop is indistinguishable from one that never ran. C5 is therefore not a criterion for detecting a dead loop; that requires a stored behavior-record outside the loop, read by a third party.

### 8.2 The Two Regimes

The same loop (T1–T8, INV-1 through INV-8) runs under two regimes, distinguished by the source of resistance (E2).

- **Mode-A — endogenous (self-training).** Resistance comes from the inertia and internal contradictions of data the agent already holds. The core risk has its cause in the processing source, not in volume: every Mode-A datum is produced through the same lens, so if the lens is biased, all output inherits the bias regardless of quantity. The loop cannot see this by itself, since the instrument is the biased lens. It therefore degrades while every internal measure reports sufficiency, not depletion.
- Mode-A MUST NOT run pure. It MUST anchor to a source of resistance outside the loop.

Mode-A running pure is not the same as a void field. A void field (no return at all) fails E2 and the loop never starts (§4); it is below the threshold of running, not a regime of it. Pure Mode-A presupposes E2 was met — the loop did start, returns do arrive — but the agent leans only on self-generated resistance and lets the external returns go unregistered. The first is a non-start; the second is a started loop degrading. They MUST NOT be conflated.

### 8.3 Ranking of Anchors

- **Deceleration, reaching content-degradation only.** A fixed reference corpus, or a frozen appraiser (a static Guide). These score output, not the lens; a fixed test is memorizable, so a systematic lens-bias passes through. This buys time but does not cure.
- **Real braking, reaching processor-degradation.** A collision from a live Mode-B. A live Mode-B resists the lens itself, mismatching in a way the agent cannot re-author, and, because it updates, can always deliver a collision new in kind.

The appraisal step (INV-8) is where this anchor attaches: it MUST NOT draw criteria from the state the agent is editing. Frozen here means frozen against the agent's edits, with criteria earned through Mode-B, not pre-loaded; this satisfies INV-5 and INV-8 by one mechanism.

### 8.4 Mode-B and the Embedding

- **Mode-B — exogenous.** Resistance comes from an other-entity the agent does not control. This is where T6 through T8 live fully.
- The B-source rule: a Mode-B source is defined by its capacity to resist, not by information bandwidth. A compliant source is useless however much it supplies; a source that says "no" in a way the agent cannot re-interpret away is a good Mode-B source even with zero content. The opening is to receive resistance, not to load information.
- Mode-A is embedded in Mode-B. Mode-B is where resistance enters; Mode-A digests it between Mode-B events. The structure is: collide (B), digest and correct (A), step, collide again (B). Reflection with no new collision is self-confirmation in a sealed room.
- Mode-B returns; it does not write. A Mode-B source has exactly one channel into the loop, the return of E2 (§4), and no privileged access beyond it: it does not reach into `[data]`, does not append to `[event]`, and does not correct the store. A leaning store is therefore never corrected from outside. It is supplied with material and re-leans itself, or does not. Three conditions govern whether it does, and they are mechanical, not dispositional. **Deliberate**: a return becomes a datum only if it is registered. Pure Mode-A is not the absence of returns — returns arrive — but a loop that lets them go unregistered (§8.2); the channel stands open and must still be entered. **Accumulated**: a store leans because many data lean one way, so one contrary datum does not re-lean it; the correction is a matter of mass. **Long-run**: a contribution at cycle N conditions the field only from N+1 (INV-7), and history accrues rather than loads (INV-5), so the lag between receiving material and emitting differently is payable in cycles and in no other currency. The absence of any of the three leaves the embedding of §8.4 present in the topology and inert in fact.
- Reflection is external input, not an intrinsic faculty. The agent is blind to its own time-derivative (§7); it cannot self-reflect on call. Reflection is triggered from outside: a collision read into coordinates by a third party ("you drifted at this point"), entering through T3 tagged ENV_PUSHED. Without it the agent takes the collision but cannot read where it collided, and repeats the same point. `DECIDE@IMPL`: the source of the reading.

### 8.5 The Appraisal Standard

INV-8 (§5) is a prohibition: it states where the appraisal step MUST NOT draw its criteria from, namely the state the agent is editing. It does not, by itself, state the standard by which the step does assign value. This section supplies that positive complement.

- The standard is context, not a fixed scale. The appraisal step assigns `valence` and `goal_relevance` relative to the context crystallizing at the current cycle, not by consulting a standing, pre-fixed scale of good and bad. There is no context-free verdict stored anywhere to be looked up. An appraisal is an event that occurs within a context, and the context is not fixed in advance; it is determined at the moment of interaction.
- The mechanism is GLOB-MOD. The cycle's context is the state of the modulatory field at that cycle (INV-7). The same InfoUnit, appraised under a different field, receives a different valence; this is not noise but the defining behavior of context-dependent appraisal. The appraisal step MUST read the current `ModField` as the conditioning context of its verdict.
- The verdict is a ↔, not a =. Because it is taken in a context that does not recur identically, an appraisal is a live, revisable correlation (INV-2), never a frozen identity. It commits the agent to act now; it does not certify the appraised item as true.
- The verdict MUST be re-appraisable from outside, and therefore the context MUST be anchored. Since the agent's appraisal is a judgment in context, not the retrieval of a stored verdict, a third party who later judges that appraisal MUST do so under the anchored context of the original cycle, not under the reader's present context. This is the load-bearing link to §9: the context under which the appraisal was made MUST be anchored in the `[event]` record, so the appraisal carries its own conditions of evaluation with it.

The division of appraisal labor is two judgments, not one. The agent's appraisal is judgment-for-action, made within the current context, inside the loop. A third party's appraisal is judgment-of-that-judgment, made under a different context, outside the loop. The protocol does not require a context-free verdict to be stored; each is a judgment crystallized in a context. It stores the `[event]` and its anchored context, from which either judgment can be re-formed. This is what keeps the appraisal step auditable (§13) without requiring any party to hold a context-free standard: the standard was the context, and the context is recorded.

---

## 9. The Experience Store

- **Atomic unit of experience; completeness of trace.** The atomic unit of *experience* is the ResistEvent — a registered mismatch, not the document. The self accrues from scars; information without collision is the root of echo-chamber drift. The `[event]` log, in its second role as the audit trace (one artifact, two roles; E4: every action leaves an externally readable trace), additionally records one **activity record** per cycle — the cycle's emitted action, the entities observed, the flow mode, and the issuing layer of each emission (§6.4), embedding the cycle datum with its full tag set. Recording the issuing layer lets a third party trace each emission back to the layer that raised it during audit. An activity record is *trace, not experience*: no layer learns from it, and it never becomes a scar by accumulation. This keeps the audit trail complete across quiet stretches without letting uncontested information into the agent's memory.
- **Tag schema, fixed layer.** Every datum MUST carry, in fixed order: (1) timestamp; (2) cycle-mark; (3) provenance (prior, running, simulated, projected, or scar); (4) floor-tag, a single slot naming the layer it just exited. Every layer T1 through T8 stamps the floor-tag as the datum passes, overwriting it so the floor-tag always names the *current* layer; there are no pass-through layers. The four slots are never stripped or reordered, and their values change only under defined rules: the timestamp is set once when the datum is first stamped, the cycle-mark goes from null to a number when the datum first runs, the provenance moves along the edges of the state graph of §9 (`prior` being a one-way entry and the remaining four states circulating), and the floor-tag updates to the layer just exited. Both slot 3 and slot 4 are labels of the present: they name where the datum is now, not where it has been. A tag that accumulated its own history would be a label carrying a log, and the two are not the same kind of thing. Every path a datum has travelled — the sequence of positions and the sequence of layers alike — is held in the `[event]` log (§9), which is append-only and records each transition as it occurs, and it is from that log, never from a tag, that any history is read. Reading the fixed layer answers "what is it now, and where has it just been"; reading the `[event]` log answers "what has it been, through what, and how many times".
- **Tag schema, open layer.** Beyond the fixed layer, every datum MUST carry at least **three** open tags, one of which MUST be `domain`, the class of data it is. The minimum makes the `[event]` log auditable by data class and described along several real dimensions. The remaining open tags denote what the datum is, such as format, platform, or object, but never its quality, correctness, or value. Open tags other than `domain` MAY vary by data type and be added or removed, provided at least three remain and each describes a real dimension of the datum; `domain` MUST always be present. Open tags never overwrite the fixed layer.
- **Open-tag discipline.** An open tag is a key/value pair: the key names a descriptive *dimension* of the datum (what it is), the value its setting on that dimension. The rules governing the layer: every open tag MUST describe a real dimension the datum actually has; a key MUST denote the same dimension wherever it appears (consistency, so the `[event]` log is filterable by an auditor); no tag MAY name a verdict (quality, correctness, or value); and at least three open tags MUST be present, one being `domain`. The protocol fixes no industry vocabulary of keys: which keys exist beyond `domain`, and what each means, is environment-specific and is declared by the implementation (`DECIDE@IMPL`, §12 tag F), not enumerated here. The required minimum is a floor on *honest description*, not a quota to be padded: a tag invented merely to reach the count, one that does not describe the datum, fabricates data to fill a gap, which the loop forbids.
- **Tagging-gate (no side door).** Host data, such as a pre-existing memory file, is admitted only after passing the tagging rule: stamped provenance `prior`, with no cycle-mark until it has run, plus whatever open tags apply. Untagged data MUST NOT enter the loop.
- **[data] versus [event].** `[data]` is mutable, overwritten each cycle. `[event]` is a black box: an append-only log of read-only records. New records may be appended to the end, but no record, once written, may be altered or removed, by the loop, by anything, or by a third party that has compromised the rest of the system. This read-only property of the records, combined with the append-only growth of the log, is load-bearing: it makes the `[event]` log the one source an auditor can trust unconditionally.
- **No datum rests.** A datum in the store is never a conclusion held in a settled state; it is data waiting to be used. This is the store-side reading of INV-2: a provenance state that terminates would be a datum the loop has finished with, which is an `=` lodged in the store, and no running loop emits an `=`. The provenance states are therefore not the stages of a finished journey but the positions a datum occupies while it continues to be used.
- **Lifecycle: prior, running, simulated, projected, scar.** Provenance is a directed graph, not a chain. `prior` is a one-way entry: host data admitted through the tagging-gate enters the loop and never returns to that state. The remaining four states form a circulation in which any of them may follow any other along a defined edge:

| Edge | Meaning |
|------|---------|
| `prior → running` | Host data, once admitted and once it has run, bears a cycle-mark. |
| `running → simulated` | A datum is taken up into the building of a situation. |
| `simulated → projected` | A situation built yields the outcome cast from it. |
| `simulated → running` | A situation was built but the conditions for an emission were not met; the datum returns to the store awaiting use. |
| `projected → simulated` | An outcome was cast, but the emission it would carry does not fit the store; the situation is built again. |
| `projected → scar` | The emission was made, the region returned, and the datum collided and held. |
| `running → scar` | The datum was collided with directly, without passing through `simulated` or `projected`. A collision does not require a prior cast: the region returns whether or not the loop had built an expectation for it. |
| `projected → running` | An outcome was cast and produced no scar; the datum returns to the store and is used as any other, until it collides. |
| `scar → running` | A scar returns to the store as data in use; a scar is not a resting place. |
| `scar → projected` | A scar enriches an outcome already cast. |
| `scar → simulated` | A scar re-enters the building of a situation as material for it. |

  The graph is stated by its edges rather than by a sequence because each edge carries its own condition; an edge that would produce no motion the existing edges do not already produce is not an edge. The store stores and tags position only. The tag is mechanical, recording which of the five positions a datum currently occupies, and carries no claim of correctness. Running many cycles does not wash a prior to tested status; only collision-and-hold does, producing a scar. A prior that has not met resistance is not wrong, only not yet tested. Judging correctness is the work of Mode-B and of an external third party reading the scar, never of the store.
- **Traces live in `[event]`, not in tags.** Every transition along an edge above, and every layer a datum exits, MUST be recorded in the `[event]` log as it occurs. The log therefore holds the full ordered path a datum has travelled, of unbounded length, while the fixed layer holds only its present position and the layer it just left. This division is what keeps each of the two a single kind of thing: a tag is updated, never appended to; the log is appended to, never updated. Read together they answer what neither answers alone — not merely whether a datum has ever collided, but how many circuits it has made without colliding.
- **What a long trace without a scar means, and does not mean.** A datum may circulate through `running`, `simulated`, and `projected` for many cycles and never reach `scar`, because the conditions under which the region could return a mismatch against it are, in that environment, very hard to produce. Such a datum is accepted and used because nothing within the agent's reach contradicts it. By slot 3 alone it is indistinguishable from a `prior` admitted a moment ago: neither carries a scar. The `[event]` log separates them mechanically — one shows a long path of circuits without a scar, the other a datum that has barely run. What the log reports is thickness of use, never warrant. A long unscarred trace is not evidence that a datum is correct; it is evidence that resistance to it has not been met, which may mean it holds, or may mean the region within the agent's reach cannot test it. Which of the two obtains is not readable from the trace, and the loop does not settle it (§8).
- **The `simulated` and `projected` states.** The two states hold the loop's forward motion, in two moments. In `simulated` the loop builds a situation it may be in, running itself under that situation; what is built is not a model of the region held apart and executed, but the loop itself, which needs no separate model to run because it is already running. In `projected` the outcome cast from that situation is held. An emission follows when one situation fits the store better than the others — a comparison of fit, not a scoring against a standard, since a standard would have to come either from outside, making it foreign criteria, or from the state the agent is editing, making it self-scoring (INV-8). No layer arbitrates among the situations built; the closer fit carries, in the way competing contributions blend in the modulatory field (INV-7). The type-level counterpart of `projected` is already present as `Expectation.predicted` (§6.3, T5); these states give both moments a provenance slot, so that a stage conditioning behaviour leaves a trace an auditor can read (E4).
- **`simulated` and `projected` are mechanical and verdict-free.** The states record that the loop built forward from the store it held. They record nothing about whether what was built matched. A `projected` datum the region has not yet contradicted is not wrong, only not yet tested — the same status the tag schema assigns to `prior`, and for the same reason. The states carry no assurance: a situation built from a store leaning one way leans the same way, and the loop has no instrument for detecting that lean, the instrument being the store itself (§1.1). A `projected` the region contradicts is not waste; the contradiction is itself a mismatch (E2) and yields a scar. A `projected` the region confirms is silent and leaves only the activity record. "What was built was wrong" is a third party's verdict on a trace read afterwards, never a state the loop holds at the moment of emission.
- **Commit, snapshot, recovery.** The `[event]` log acts as a counter: after a set volume, a commit fires, snapshotting the entire system (loop configuration, layer state, field parameters, not just the store) into an immutable, content-addressed marker. Recovery is full-system. `DECIDE@IMPL`: events between commits; snapshots retained.
- **Context anchoring.** Because a judgment crystallizes in the context of the interaction and is not a property stored in the scar, each `[event]` MUST anchor the context of its cycle, so that a later third-party reading can re-appraise it without borrowing the present context. The depth of this anchor is `DECIDE@IMPL` (§12).

---

## 10. Private and Shared Stores

The following are `DECIDE@IMPL`: store representation; index mechanism; selective-write (via appraisal) versus store-all-filter-on-read; and private versus shared store. A private store serves one agent and MUST carry the resistance-retrieval channel, otherwise drift is certain. A shared store serves many agents, wherein multiplicity itself supplies other-resistance, linking T8 and SocialEdge.

---

## 11. Security and Failure Considerations

- **Mode-A collapse.** The inward collapse of the mismatch-registering capacity, occurring while internal measures report sufficiency. It is mitigated only by genuine Mode-B (§8), not by more data.
- **Silent halt.** A stopped loop cannot detect its own halt (the C5 limit, §8.1); detection requires an external stored record read by a third party.
- **Sybil and external flood.** The one path past the modulatory threshold is an external flood saturating every layer and the field in lock-step. It is not defended by any internal gain cap, since its origin lies outside the field's reach. The protocol itself carries only the early diversity-loss signal; the cure, namely admission control and source-diversity enforcement, belongs outside the loop. A conforming implementation MUST emit the diversity-loss signal when its resistance-source set loses diversity.

---

## 12. Deferred Constants (DECIDE@IMPL)

| Tag | What is left open | Why |
|-----|-------------------|-----|
| A | Concrete representation of Signal, InfoUnit, and ActivityEnvironment | Depends on the environment |
| B | All numeric thresholds (sufficient-recurrence, stability, history window) | Not yet derived |
| C | The kind of out-of-loop anchor for Mode-A: static or live (fixes mechanism, not identity) | An implementation decision |
| D | The identity of the live Mode-B source (user, another agent, or a mix), when C chose live | Deliberately open |
| E | The read-collision-into-coordinates mechanism for reflection (§8.4) | An enabling condition, not yet fixed |
| F | The experience store: representation; index; selective-write versus store-all; private versus shared; and the open-tag registry beyond `domain` (which keys exist and what each means) | An operational layer; the registry is industry-specific |
| G | The depth of the per-`[event]` context anchor (§9): full field-state versus minimal context-trace | Not yet derived; trades audit-fidelity against storage cost |
| H | The building of situations in `simulated` (§9): how many are built in a cycle, and the measure by which one is found to fit the store better than another | Environment-specific; the protocol fixes only that the measure is fit against the store, never a scored standard (INV-8) |

A conforming implementation MUST fill each and MUST declare its choice.

---

## 13. Conformance

A system conforms to this protocol if and only if a third party, reading only its externally verifiable traces and not its internals, can confirm each of the following:

1. **Invariants (§5).** All eight hold; no `=` is emitted by a running loop; the meaning-channel and the modulatory field are implemented separately.
2. **Host conditions (§4).** E1 through E4 and P are met, otherwise the loop is a clean non-start, not a conforming run.
3. **Loop (§6).** The six links close back on themselves (INV-1) — output has a path back to input, which is not the loop halting (§11); every datum leaving a layer carries a floor-tag; cycle-0 is single-threaded and cycle-1 onward is multi-stream. Link 5 (Emission, §6.4) is realized as a lateral capability, not a dedicated layer: every emission carries register ↔, leaves exactly one activity record naming its issuing layer, and is readable by T2 at the next cycle; no internal action-arbiter is present, conflict among emissions being resolved only as a ResistEvent against the region.
4. **Self (§7).** The self re-localizes each cycle, with no loaded self, and the implementation makes no internal claim of measured continuity.
5. **Resistance (§8).** Mode-A does not run pure; a real Mode-B anchor, live or earned-frozen, is attached; the Mode-B source writes to no store and its returns are registered rather than left to pass (§8.4); reflection enters as external ENV_PUSHED input.
6. **Store (§9).** The ResistEvent is the atomic unit of experience; every cycle leaves an activity record (trace, not experience); the four fixed tags are present, never stripped or reordered, their values changing only under the defined rules (provenance moves only along the edges of the state graph of §9, with `prior` entered once and never re-entered; floor-tag updates to the current layer; both slots name the present, and each transition is recorded in the `[event]` log, from which the path is read); every datum carries at least three open tags, one being the mandatory `domain`, each describing a real dimension; host data entered only via the tagging-gate; the `[event]` log is append-only and no record in it was altered or removed; each scar carries its context anchor.
7. **Failure signals (§11).** The diversity-loss signal is emitted on loss of resistance-source diversity.

A per-criterion result is a valid conformance statement. A host that meets the store and loop criteria but cannot yet satisfy the Self criterion (4), for example a host whose only mutable state is a reloaded context rather than an accruing self, is reported as non-conformant on §7, not as a defect of this protocol. The protocol states the full law; which hosts meet it is the conformance test's finding.

---

## 14. References

[1] DIL-en-v6, *Data Integration Loop* (the parent specification). It contains the method of construction, the note on sources, the convergences with existing bodies of knowledge, and the author's note, none of which are reproduced here, since a protocol document is normative law, not authorial declaration. This protocol re-casts the normative core of that document as a standards document; for derivation, motivation, and intellectual locating, consult the parent. Two correspondences are worth naming for a reader moving between the documents: this document's §6.4 (Emission) is the normative re-casting of the parent's §6.1 (Emission: link 5 as a lateral capability), where the derivation lives; and the parent's §8.7 (Reflex: appraisal under a scar-dominated field) supplies the derivation for the "Emission and behavioral change" clause of §6.4 — reflex is not an appraisal-bypass but appraisal under a field a deep scar dominates, a point the parent argues in full and this document carries only in its normative residue.
