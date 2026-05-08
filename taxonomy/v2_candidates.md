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

## How to update

When v2 is cut: bump `taxonomy/v1.json` to `v2.json`, do not edit v1 in
place. Re-run the flagging pipeline on the existing eval set under v2 and
diff the results — beats that change tags between v1 and v2 are the
high-signal cases worth understanding.