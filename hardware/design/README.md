# Design

How the body looks, and how it can show things — work package ID of
[`plan/`](../../plan/README.md#id--industrial-and-expressive-design).

| Path | Contents | Plan | Status |
|---|---|---|---|
| [`concept/`](concept/) | The author's concept art: the original visual idea of the body | input to ID-1 | ✅ two images |
| `industrial/` | Industrial design: form, proportion, class-A surfaces, colour–material–finish, human-contact surfaces, renders | ID-1 to ID-4, ID-7 | 🔜 |
| `expression/` | Expressive capability: face geometry, the FACS action units to be actuated, range and speed per unit, gaze, the evaluation protocol | ID-5, ID-6, ID-8 | 🔜 |

**Industrial design** here means the discipline that decides how a manufactured
physical product looks and is handled — form, proportion, surfaces, colour,
material and finish, fit to the human body. **Expression** is the separate
discipline of what the body can show through movement: face, eyes, posture.
The two share one surface and are kept in one parent directory, but apart, so
that "how it looks" is never confused with "what it can express".

Neither specifies *when* or *why* the body expresses anything. That belongs to
the controller, which this repository does not specify
([README](../../README.md#scope-boundary)).

Concept art and renders are documents under `CC-BY-4.0`; surface CAD, once it
exists, is a hardware design under `CERN-OHL-S-2.0` ([LICENSE.md](../../LICENSE.md)).
