# Taxonomy v2 Candidates

Tags that the v1 eval-set labeling surfaced as missing or imprecise. The v1
taxonomy stays frozen — these are tracked here for inclusion when v2 is cut.

The discovery process matters: these gaps were not theoretical. They appeared
because real films in the eval set could not be cleanly tagged with v1
vocabulary. That is exactly the use of an eval set in taxonomy iteration.

## 1. Anger

**Surfaced by:** Interstellar — Mann's betrayal sequence (~70% mark).

**The gap:** When Mann reveals he falsified his data and tries to kill
Cooper, the dominant felt emotion includes anger — at the betrayal, at the
waste of the mission, at the cost already paid. v1 has no anger tag.

The closest v1 tags are `Tension.Confrontation` (the fight) and `Dread.Visceral`
(the violence), but neither captures *anger as a felt emotion in its own
right*. Anger is genuinely distinct from confrontation (which is about two
forces meeting) and dread (which is about anticipated bad outcomes).

**v2 proposal:** Add `Anger` as a 9th superior emotion with sub-emotions for
range. Candidate sub-emotions: `Anger.Betrayal`, `Anger.Outrage`,
`Anger.Frustration`, `Anger.Rage`. Likely also surfaces in revenge films,
political dramas, and confrontation-driven cinema not currently in the eval
set.

## 2. Moral disquiet / unreliable-narrator unease

**Surfaced by:** Andhadhun — the European coda where Akash flicks the can
with his cane (~99% mark).

**The gap:** The Andhadhun ending leaves the viewer in a register v1 cannot
name cleanly: *moral unease without resolution*. Not dread (the danger has
passed), not melancholy (it isn't sad), not guilt-as-felt-by-protagonist
(Akash seems fine). It is the *viewer's* uncertainty about whether to trust
the narrator and how to feel about what they have just been told.

For v1 the beat is tagged as `Wonder.Mystery` + `Moral_weight.Guilt`, but
neither captures the specific texture of *unreliable-narrator unease*.

**v2 proposal:** Either a new sub-emotion `Moral_weight.Disquiet` (ethical
unsettledness without clear cause), or a more substantial structural addition
like `Ambiguity` as a meta-tag flagging that a beat resists single-emotion
tagging. The latter is more honest but more complex; revisit during v2 design.
This will likely also surface in films like *No Country for Old Men*,
*Shutter Island*, *Joker*, and *Drishyam* if they enter the corpus.

## 3. Bittersweet/sacrificial endings under `grief.melancholy`

**Surfaced by:** The Dark Knight — endpoint disagreement (~99% mark). See
`docs/findings/dark_knight_v1.md`.

**The gap:** The v1 gloss for `grief.melancholy` reads "diffuse sadness."
That captures the *texture* of melancholy but not its *purposeful*
variety. Dark Knight's ending — Batman choosing to take the fall, the
sacrifice serving Gotham's hope — is felt as melancholy, but a melancholy
*with hidden meaning*, not diffuse sadness. The same applies to endings
like Logan's death, Tony Stark's funeral, or Ken Miles' final drive.

Without a clearer gloss, the LLM reads these endings as `dread.existential`
(the bleak interpretation) and the recommender will match Dark Knight
against films like *No Country for Old Men* rather than *Logan*. Those
are wildly different recommendations.

**v2 proposal:** Update the gloss for `grief.melancholy` in `taxonomy/v1.json`
to: *"Quiet sadness, often bittersweet or purposeful. Includes the heavy
peace of a chosen sacrifice and the warm-cold ache of a hard-won ending."*
This is a gloss refinement, not a new tag. The change is non-breaking for
v1; flagged films don't need re-running unless we want them to.

## 4. Operational success without emotional catharsis

**Surfaced by:** The Dark Knight — Hong Kong / Lau extraction beat (~42%
mark). See `docs/findings/dark_knight_v1.md`.

**The gap:** When the protagonist demonstrates capability or operational
success without the scene carrying an emotional payoff, the LLM reaches
for `triumph.victory` because nothing else in the Triumph branch fits.
But `triumph.victory` implies *external goal achieved at meaningful
emotional stakes* — that's not what the Lau extraction is. It's a
competence flex; the threat hasn't shifted.

This generalizes: every film with a "mission accomplished" scene that
doesn't actually move the emotional needle will hit this gap. Think any
Mission Impossible mid-film extraction, Avengers gathering the team in
Endgame's heist montage before the snap reveal, Pawan crossing the first
border without consequence in Bajrangi Bhaijaan.

**v2 proposal:** Either add a new sub-emotion `Triumph.Competence` (the
mission worked, no catharsis attached), or instruct the prompt to
downgrade `triumph.victory` intensity below 0.5 when the beat is purely
operational. The latter is cheaper (prompt-only fix) and worth trying
first; if v2 of the prompt still over-tags these beats, add the
sub-emotion in v3.

## 5. Conviction outside moral pressure

**Surfaced by:** The Dark Knight — Harvey Dent's courtroom punch (~18%
mark). See `docs/findings/dark_knight_v1.md`.

**The gap:** When a character demonstrates *standing up for what's right*
in a scene where there's no genuine ethical dilemma (the punch is
defensive, the cause is unambiguous), the LLM has nowhere clean to tag
it. `moral_weight.conviction` requires actual ethical pressure on the
soul; `joy.hope` is too soft and shifts the register away from character
toward outcome. v1 ended up with `joy.hope` for the courtroom beat,
which under-reads the scene.

This is a real category: it shows up in any film where a character takes
a public stand without facing real moral cost — Hiccup defending dragons
to the village in HTTYD, Munni's mother on the train in Bajrangi
Bhaijaan, Cap's "I can do this all day," Mia choosing the audition over
the dinner in La La Land.

**v2 proposal:** Consider a sub-emotion `Triumph.Conviction` distinct from
`Moral_weight.Conviction`. The moral-weight version is "holding the line
when it costs"; the triumph version is "standing up before the cost is
real, in a way that defines who the character is." Slight difference but
useful for both flagging precision and recommender matching.

## How to update

When v2 is cut: bump `taxonomy/v1.json` to `v2.json`, do not edit v1 in
place. Re-run the flagging pipeline on the existing eval set under v2 and
diff the results — beats that change tags between v1 and v2 are the
high-signal cases worth understanding.