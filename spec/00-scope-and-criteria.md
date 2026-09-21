# 00 — Scope and acceptance criteria

## What this specification is

GEMs specifies a ~1.75 m humanoid body built to acquire physical experience on
behalf of a controller that does not live entirely on it.

It specifies **the range of what the body can do and what each capability
costs**. It does not set the operating point. Wherever a value is marked
`⟦CTRL⟧`, the blank is deliberate: it marks a decision that is not the body's to
make.

## Two acceptance criteria

Everything in this specification has to pass both.

**1 — The physical ceiling.** No mechanism may call for physics that does not
exist. Laboratory work that is expensive, unscaled, or not yet on the market is
allowed. Invented physics is not. The target is the maximum that is actually
achievable, reaching or slightly exceeding the near term.

**2 — Service to experience.** Every capability has to earn its place by
serving what the body is for: acquiring physical experience as a human body
does, plus selected capabilities a human body does not have. Anything that bends
toward purely industrial, combat or surveillance use is reduced to the
experience-serving level.

## The division of authority

**The body grants capability and declares what it costs. The controller decides
what to do with it.**

Nothing is cut at the level of the body for reasons that belong to whoever
operates it — not ethics, not duty cycle, not acceptable risk. Those are
decisions made by the controller, and this specification records them as blanks
rather than filling them in.

This is not a disclaimer. It is a structural commitment: a body that silently
withheld capability would make the controller's decisions unauditable, because
nobody downstream could tell a choice from a limit.

## Notation

| Mark | Meaning |
|---|---|
| **TM** | Commercially available |
| **LAB** | Demonstrated in the laboratory, not yet scaled |
| `⟦CTRL⟧` | A value belonging to the controller's judgement — deliberately blank |
| `⟦IMPL⟧` | A constant not yet derivable — decided at implementation, not invented here |

A figure written as a range is a range, not an average. Where a figure is
sourced from published work it is marked as such; where it is derived inside this
specification, the derivation is shown.

**No constant is invented to look complete.** A specification that fills in its
own underived numbers trades honesty for the appearance of finish. Chapter 09
lists every value left open and says why.

## Out of scope

| Not specified here | Where it belongs |
|---|---|
| The controller — its design, its reasoning, how it will behave | Not in this repository |
| How acquired signal becomes structured information | A companion loop specification — see [08](08-platform-contract.md) |
| The standard against which a body's conduct is judged | A third party: the deploying or certifying party |
| Earlier speculative material about GEMs | [/vault/fiction/](https://plonemraz.github.io/vault/fiction/) |
