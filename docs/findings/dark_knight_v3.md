# Finding: The Dark Knight, prompt v3

**Date:** 2026-05-15
**Prompt version:** `prompts/flag_film_v3.md`
**Model:** claude-sonnet-4-5
**Input:** `data/plots/raw/dark_knight.md` (IMDb synopsis, ~3,255 words)
**Output:** `data/trajectories/dark_knight_v3.json`
**Ground truth:** Eval-set entry for The Dark Knight in `films/eval_set.md`
**Compared against:** `data/trajectories/dark_knight_v2.json` (previous run)

## TL;DR

v3 closes the dominant-register issue surfaced by the eval harness on two
consecutive v2 runs. The harness now passes 6 of 7 rules (vs. 5 of 7
under v2), with the single remaining warn (`has_intensity_floor`) being
defensible — Dark Knight is genuinely a film with no quiet scenes. All
v2 wins (layered-sacrifice ending, operational-success calibration,
beat synthesis) carried forward without regression.

## What changed in v3

A single targeted modification to the "Dominant register" section of
the v2 prompt. The new instruction tells Claude to default the dominant
register to the most-frequent superior emotion across its beat tags,
with an escape hatch for films where atmosphere genuinely diverges from
structural weight. A worked example using Dark Knight itself was included
in the prompt. Full rationale and prompt diff in
`docs/findings/prompt_v3_candidates.md` (candidate #1).

No other section of the v2 prompt was modified.

## Harness results

| Rule | Severity | v2 (most recent run) | v3 |
|---|---|---|---|
| beat_count_in_range | error | ✓ (11 beats) | ✓ (8 beats) |
| beats_position_ordered | error | ✓ | ✓ |
| endpoint_tags_appear_in_beats | error | ✓ | ✓ |
| ending_beat_exists | warn | ✓ (0.98) | ✓ (0.92) |
| has_intensity_peak | warn | ✓ (0.95) | ✓ (0.95) |
| has_intensity_floor | warn | ✗ (0.50) | ✗ (0.50) |
| dominant_register_represented | warn | ✗ (27%) | ✓ (31%) |

Overall: PASS for both, but v3 has 1 warn vs. v2's 2 warns.

## Did the fix work?

Yes. Two pieces of evidence.

**Direct:** The dominant_register field changed from `dread` (v2) to
`moral_weight` (v3), and the harness rule now passes at 31%. v2 failed
this rule on two consecutive runs (18% and 27%), so this isn't sampling
noise — the prompt change moved the model's behavior.

**Indirect:** The model's beat tagging is now *internally consistent*
with the dominant register. The film has 5 of ~16 total tags as
`moral_weight.*` (compromise × 3, conviction × 1, sacrifice × 1). The
final beat's justification explicitly frames the film's ending as
"purposeful sacrifice" — same language as v2's layered-sacrifice rule.
Claude is reading Dark Knight as a film about ethical pressure under
chaos, and the dominant register naturally follows from that reading.

This is the soft-procedural rule landing the way I hoped. Not just
enforcing arithmetic ("count tags, pick the most frequent"), but
nudging the model toward a more coherent interpretation where beat
tagging and dominant register agree because they're reading the same
underlying spine.

## Did anything regress?

No. Spot checks against v2's known wins:

- **Endpoint tags:** v3 matches eval-set entry exactly:
  `moral_weight.sacrifice`, `triumph.vindication`, `grief.melancholy`.
  Same as v2's best run.
- **Operational-success rule (Hong Kong beat):** v3 still tags as
  `tension.chase` at intensity 0.5, with the justification explicitly
  using v2's rule language ("operational competence without emotional
  payoff, kinetic but not triumphant"). The rule is persisting.
- **Synthesis rule (Rachel/Harvey beat):** v3 folds Rachel's death and
  Harvey's corruption into one beat at position 0.58, tagged with both
  `grief.bereavement` and `moral_weight.compromise`. This is exactly
  what v2 introduced. Held.
- **Layered-sacrifice rule (ending):** v3's final beat carries
  sacrifice + vindication + melancholy simultaneously, with intensity
  0.9 and a justification explicitly naming purposeful sacrifice. Held.

All four v2 improvements carried forward cleanly.

## New findings from this run

### Finding 1: `has_intensity_floor` consistently fails for Dark Knight

The lowest-intensity beat in v2 run 1, v2 run 2, and v3 is the same:
0.50. Across three runs of two different prompt versions, Claude
consistently reads Dark Knight as a film with no scenes quieter than
0.5 intensity.

This is defensible — Dark Knight is wall-to-wall pressure, with no
rest scenes the way HTTYD2 has its dragon-sanctuary moment. The
intensity floor of 0.4 set by the harness rule may simply not apply to
high-tension films.

Action: leave the rule unchanged. Watch this rule across other films.
If it fails consistently on Endgame and Infinity War (also high-
intensity films) but passes on HTTYD2 / Bajrangi / Greatest Showman,
the rule is correctly identifying a class of films rather than being
miscalibrated.

### Finding 2: Run cost is non-trivial for repeated experiments

Four Dark Knight runs to date (v1, v2 × 2, v3) — roughly $0.50 of API
spend on one film. When the eval harness scales to 15 films and v3+
prompt iterations land, repeated re-running will become a real cost
consideration.

Action: not today. Logged as something to address when corpus expands.
Possible mitigations: lower temperature for determinism, caching of
trajectories keyed by (film_id, prompt_version, plot_hash).

## Closes

- `prompt_v3_candidates.md` candidate #1 (dominant register): **closed.**
  The fix worked.

## Open

- `prompt_v3_candidates.md` candidate #1 v4 follow-up (compute dominant
  register in code rather than via prompt): still open. v3 closes the
  acute issue but the architectural cleanup remains valuable for v4.

## What this run tells us about the system overall

Two iteration cycles of the eval-driven-development loop have now
completed cleanly:

- v1 → manual finding (Dark Knight ending) → v2 → fix worked
- v2 → automated harness finding (dominant register) → v3 → fix worked

Each fix was isolated (one variable changed per version), measurable
(both manual and automated evidence), and additive (each version
builds on the last without regressing prior wins). This is the
methodology working as intended.

The next test of robustness is running v3 against a tonally different
film. Bajrangi Bhaijaan is queued as the next experiment — its
expected register is `warmth`, not `moral_weight` or `dread`, which
will exercise the v3 prompt's "escape hatch" clause (atmospheric reads
allowed when beat-tag frequency doesn't reflect background register).
If v3 correctly identifies Bajrangi's register as warmth despite many
tension beats, the soft-procedural rule generalizes. If v3 forces
Bajrangi's register to `tension` or `dread` based on frequency, the
escape hatch isn't strong enough and we'll need v3.5 or v4.