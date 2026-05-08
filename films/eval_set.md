# Eval Set v1

Fifteen films chosen because I know their emotional arc from memory and can
defend each call. These are the ground-truth corpus for v1: every taxonomy
decision and matching algorithm gets stress-tested here first.

| # | Film | Year | One-line emotional arc | Endpoint |
|---|------|------|------------------------|----------|
| 1 | The Dark Knight | 2008 | ... | ... |
| 2 | Interstellar | 2014 | ... | ... |
| 3 | Stranger Things S1 | 2016 | ... | ... |
| 4 | Stranger Things S3 | 2019 | ... | ... |
| 5 | Harry Potter and the Prisoner of Azkaban | 2004 | ... | ... |
| 6 | How to Train Your Dragon 2 | 2014 | ... | ... |
| 7 | Avengers: Infinity War | 2018 | ... | ... |
| 8 | Avengers: Endgame | 2019 | ... | ... |
| 9 | Thor: Ragnarok | 2017 | ... | ... |
| 10 | Zindagi Na Milegi Dobara | 2011 | ... | ... |
| 11 | Spider-Man: Into the Spider-Verse | 2018 | ... | ... |
| 12 | Ford v Ferrari | 2019 | ... | ... |
| 13 | The Greatest Showman | 2017 | ... | ... |
| 14 | Bajrangi Bhaijaan | 2015 | ... | ... |
| 15 | Andhadhun | 2018 | ... | ... |

## Why these fifteen

Heroic-arc heavy by design — that's what I watch — but deliberately includes
breakers: Andhadhun for ambiguous endings and dark register, The Greatest
Showman for music as emotional engine and a flawed protagonist arc, Ford v
Ferrari for bittersweet anti-cathartic victory, three Indian films (ZNMD,
Bajrangi, Andhadhun) for non-Western narrative shapes covering three different
registers (road-trip self-actualization, cross-border tenderness, morally
ambiguous thriller), and Into the Spider-Verse / Ragnarok for tonal range
beyond the Nolan-Marvel default.

## Known v1 gaps

The eval set has two acknowledged gaps that v1 will not handle well. Documented
here so the limitation is honest rather than discovered later.

- **Yearning-driven romance as primary engine.** No film in the set has
  romantic yearning as its dominant emotional register. Greatest Showman has
  a romance subplot but it isn't the engine. Films like La La Land or Titanic
  would test the `Warmth.Yearning` tag at full intensity. v1.x candidate.
- **Non-linear narrative / unreliable narrator.** Every film in the set
  follows a roughly linear emotional progression that maps cleanly to
  narrative percentage. Andhadhun's twists give partial coverage but the
  film is still chronologically forward. Films like Memento, Arrival, or
  Eternal Sunshine would force a real data model decision: do we tag
  emotional beats by story chronology or audience-experience chronology?
  Deferred to v2.

## Format

Each row will eventually contain:

- **One-line emotional arc** — the felt journey of the film in one sentence,
  using vocabulary from `taxonomy/v1.json`. Plain language, written from
  memory, no plot summary.
- **Endpoint** — one or two (rarely three or four) tag IDs from the taxonomy
  describing where the final 5–10% of the film lands the viewer. This is the
  field the matching algorithm will check most heavily, so it has to be
  honest.