# Prompt v3 candidates

Findings that the v2 prompt produces but the eval harness or manual review
identifies as wrong. Each candidate lists what's broken, what evidence
supports the finding, and how v3 should address it.

## How this list works

Each entry tracks one specific prompt-iteration candidate. When v3 ships, the
candidates it addresses are marked **closed** and the file evolves into a v4
candidates list. Candidates that don't get into v3 stay open.

---

## 1. Dominant register doesn't reflect beat tagging

**Status:** Open. Will be addressed in v3.

**Surfaced by:** Automated eval harness, rule
`dominant_register_represented`. Both v2 runs of Dark Knight failed this
rule:

- Run 1 (2026-05-11): claimed `dread` as dominant register; `dread.*` tags
  appeared in only 18% of beat tags (threshold: 30%).
- Run 2 (2026-05-13): claimed `dread` as dominant register; `dread.*` tags
  appeared in 27% of beat tags. Closer to threshold but still failing.

Same prompt, two runs, same failure mode. This is not sampling noise — it
is a structural issue with how v2 instructs the model.

**Diagnosis:** The v2 prompt asks Claude to pick a dominant register as an
*independent* judgment from beat tagging. So Claude tags the beats based
on what individual scenes feel like, then independently picks a register
based on overall vibe or atmosphere. The two answers aren't required to
agree, and they don't.

Worse, Claude leans toward atmospheric reads when picking the register
(Dark Knight *feels* oppressive and grim throughout, so → `dread`), even
when its own tagging puts the structural emotional weight elsewhere
(most of Dark Knight's beats use `moral_weight.*` and `tension.*`).

**v3 proposal — Flavor B (soft procedural rule with escape hatch):**

Update the "Dominant register" section of the prompt to read:

> *The `dominant_register` field should usually be the most-frequent
> superior emotion across your beat tags. If you choose a different
> register, write a brief explanation in the justification of your
> endpoint beat noting why beat-tag frequency doesn't reflect the film's
> actual background register. Default to matching the most-frequent
> superior; deviate only when atmosphere genuinely diverges from
> structural weight.*

Adding an explicit example would help: tell Claude that for Dark Knight
the dominant register should be `moral_weight` or `tension` (whichever
the model tags most), not `dread`.

**v4 candidate (deferred):** Remove `dominant_register` from the Claude-
produced output entirely. Make it a *computed property* on the Trajectory
model — derived in code from beat-tag frequencies. This eliminates the
"Claude's self-assessment disagrees with its own tagging" bug category
permanently. Out of scope for v3 because it's a schema and pipeline
change, not a prompt change; logged here as the architectural endgame.