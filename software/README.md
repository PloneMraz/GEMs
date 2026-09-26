# Software

Code executed on the edge AI module under a general-purpose operating system,
as [spec 07.1](../spec/07-firmware-and-software.md#71-the-division) defines
software: processing of what the hardware acquires. Its tasks are firm, soft or
non-real-time; nothing hard real-time runs here.

| Module | What it is | Status |
|---|---|---|
| [`audit_log.py`](audit_log.py) | The audit log of [spec 06.4](../spec/06-audit-surface.md#64-audit-log): record schema, hash chain, per-batch Merkle root, and the verifier an assessor runs | ✅ reference implementation |
| Feature extraction and compression | The ≥2:1 the link requires ([spec 05.4](../spec/05-sensing.md#54-aggregate-rate-against-the-link)) | 🔜 *waiting update* |
| Sensor fusion | Multi-rate, on a shared time base | 🔜 *waiting update* |
| Link management | Graceful degradation before dropped streams | 🔜 *waiting update* |

Python 3, standard library only.

```bash
python -m unittest discover -s software -v
```

The agency-tagging reference model moved to
[`../firmware/reference/`](../firmware/reference/): tagging is a hard real-time
firmware task (spec 07.3 g7), so its golden model lives with the firmware it
specifies.

## The audit log

The log's record schema uses the vocabulary of the RSIL contract it carries
evidence for — an *emission* is an output event, and the *anchored* tier holds
each emission's anchored context (spec 08.2). Those are field names of the
contract, not names for components; the component is the audit log.

Protocol requirements **C-4**, **C-6**, **C-9** and **C-12** are verified by
evidence class **T** — an assessor reads the log and checks a property. That
needs a defined format and a reader, or the class is unusable. This module is
both.

**The write path refuses what the specification forbids.** An emission without
anchored context, an emission still marked `UNCLASSIFIED`, a contact event with
no measured amplitude, a sequence number that skips — each raises rather than
being written. The error message names the clause.

**The verifier checks the same rules independently**, because a record can reach
an assessor without having passed this write path — from a different
implementation, or a broken one, or a hostile one. It reports findings rather
than raising: `GAP`, `NO_CONTEXT`, `UNCLASSIFIED`, `NO_AMPLITUDE`,
`ROOT_MISMATCH`, `BATCH_INCOMPLETE`, `BAD_SIGNATURE`.

### Two structural choices worth naming

**Hash chain at full rate, signature once per batch.** A secure element signs
tens to hundreds of times per second; the loop runs at 500 Hz across tens of
channels. Chaining is cheap and continuous, signing is not, so the chain carries
ordering and tamper-evidence while a Merkle root per window carries the
signature. The batch period is the implementer's trade between trace granularity
and signing load.

**An odd Merkle node is promoted, not duplicated.** Duplicating the last node
would let two distinct batches produce one root — so a batch could be rewritten
under a signature that still verifies. There is a test for this.

### What it does not do

It does not choose a signature scheme. `sign` and `verify` are callables you
supply; the module fixes *what* is signed and *when*, never *how*. The
specification leaves the scheme open, and a reference implementation that picked
one would be inventing a constant the reasoning does not fix. The tests use HMAC
because a test needs *something*, and it is named as a test key, not a scheme.

It also does not judge. A log that verifies clean says the record holds
together — nothing about whether the body behaved acceptably. There is a test
asserting exactly that: a contact event logging 400 N for thirty seconds
verifies without a single finding. Whether that was acceptable is a third
party's question, as [protocol §10](../protocol/conformance.md) states.
