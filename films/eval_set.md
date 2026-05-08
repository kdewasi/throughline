# Eval Set v1

Fifteen films chosen because I know their emotional arc from memory and can
defend each call. These are the ground-truth corpus for v1: every taxonomy
decision and matching algorithm gets stress-tested here first.

| # | Film | Year | One-line emotional arc | Endpoint |
|---|------|------|------------------------|----------|
| 1 | The Dark Knight | 2008 | Quiet foreboding in the opening heist escalates into mounting dread as Gotham's order frays; breaks at Rachel's death into grief and moral compromise; Batman holds his conviction through the ferry dilemma and the final pursuit; lands on his choice to take the fall — muted vindication wrapped in sacrifice and melancholy. | `Moral_weight.Sacrifice`, `Triumph.Vindication`, `Grief.Melancholy` |
| 2 | Interstellar | 2014 | A dusty, suffocating melancholy on a dying Earth gives way to the sheer, awe-inspiring scale of leaving our solar system; the emotional floor drops out entirely on Miller's planet with the visceral, gut-punch realization of decades lost to a ticking clock; the film climbs into an absolute sensory and emotional crescendo inside the tesseract, where a massive, booming orchestral score collides with the intimate desperation of a father reaching through the physical architecture of time; lands on a beautifully heavy, bittersweet reunion holding victory and lifelong grief at once, before fading out to the quiet, lonely hope of Brand standing under a new sun. | `Triumph.Victory`, `Grief.Bereavement`, `Warmth.Tenderness`, `Joy.Hope` |
| 3 | Stranger Things S1 | 2016 | Childhood camaraderie biking home through Hawkins gives way to foreboding as Will vanishes; the false body in the quarry breaks the town into bereavement and visceral dread; the floor drops out as Joyce and Hopper enter the toxic Upside Down and El is pushed past her limits; the school showdown lands at confrontation and pressure under flickering lights; resolves into a quiet, nostalgic Christmas tableau — until Will coughs up the slug and foreboding returns. | `Warmth.Nostalgia`, `Dread.Foreboding` |
| 4 | Stranger Things S3 | 2019 | Neon summer delight and Starcourt-bright camaraderie open the season at full saturation; the floor cracks open with Billy possessed in the basement, signaling the threat is already inside; the Meat Flayer attack bites El and strips her powers exactly when stakes go vertical; the climax splits between mall and Russian base in kinetic chase and cathartic charge; lands on El reading Hopper's letter as the Byers drive out of Hawkins — bereavement carried in tenderness, the season's bright nostalgia now turned bittersweet. | `Grief.Bereavement`, `Warmth.Tenderness` |
| 5 | Harry Potter and the Prisoner of Azkaban | 2004 | The Knight Bus's mystery breaks into the train's creeping foreboding as a Dementor reaches in; the pub overhear about Sirius and the Potters shatters Harry into loss of innocence; the lakeside Dementor's Kiss collapses him into existential dread and helpless grief; the time-turner doubles back and Harry's enormous Patronus answers across the lake in self-actualizing release; lands on the joyful, freeze-frame exhilaration of the Firebolt at full speed. | `Joy.Exhilaration` |
| 6 | How to Train Your Dragon 2 | 2014 | Free flight over Berk opens in exhilaration and discovery; Hiccup's reunion with his lost mother in the dragon sanctuary turns the film into awe and tenderness; Stoick taking the plasma blast for Hiccup breaks everything into bereavement and loss of innocence as Hiccup's belief that every dragon can be saved breaks with his father; the final Alpha showdown rises into confrontation and victory; lands on Hiccup stepping up as chief beside Toothless, self-actualization carried by the camaraderie of his people. | `Triumph.Self_actualization`, `Warmth.Camaraderie` |
| 7 | Avengers: Infinity War | 2018 | Thanos opens by tearing through the Asgardian ship — stakes and bereavement land in the first ten minutes and never lift; Vormir folds the film into sacrifice and existential dread as Gamora dies; the Snap drops the floor into existential dread and planetary bereavement; the Wakanda and Titan stands hold at pressure and confrontation as the line refuses to break; lands on heroes blowing into dust and Thanos peacefully watching the sun rise — bereavement under visceral dread. | `Grief.Bereavement`, `Dread.Visceral` |
| 8 | Avengers: Endgame | 2019 | A grieving five-year-jump world opens in melancholy and bereavement that nobody can move past; Scott Lang's return turns the film into hope and discovery as the heist becomes possible; Vormir collapses into bereavement and sacrifice as Natasha jumps for her family's future; the portals open to Silvestri's score and the unified charge lifts into cathartic confrontation; lands on Tony's quiet funeral bleeding into Steve's long-delayed dance with Peggy — bereavement softened by nostalgia. | `Grief.Bereavement`, `Warmth.Nostalgia` |
| 9 | Thor: Ragnarok | 2017 | Thor's banter with Surtur and the fake-Odin Asgard set a new colorful, comic register from the first frame; the gladiator-arena Hulk reunion punctures tension into pure humor; Hela cornering Thor and slicing out his eye drops the film into pressure and stakes; the Sakaar escape into the Bifrost-bridge battle set to *Immigrant Song* climbs into cathartic exhilaration; lands on Asgard destroyed but its people looking toward Earth in hopeful camaraderie. | `Joy.Hope`, `Warmth.Camaraderie` |
| 10 | Zindagi Na Milegi Dobara | 2011 | Old friends reunite for a sun-drenched bachelor trip carrying camaraderie threaded with quiet regret over their unexamined lives; Imraan meeting his real father turns the trip into loss of innocence and yearning; Arjun hurling Kabir's phone from the moving car explodes into confrontation and surfaced regret; Pamplona's running of the bulls climbs into exhilaration and cathartic release; lands on Laila and Arjun's sunlit wedding — camaraderie now unburdened, dancing into delight. | `Warmth.Camaraderie`, `Joy.Delight` |
| 11 | Spider-Man: Into the Spider-Verse | 2018 | Miles in a stressful new school and the bite in the underground subway open in discovery and pressure; watching his Peter Parker die at Kingpin's hand turns the film into bereavement and stakes; the Prowler's mask coming off Uncle Aaron drops everything into grief and guilt; the leap-of-faith jump and multidimensional collider fight lift into self-actualization and confrontation; lands on Miles on his bed with a quiet smile — hope and earned victory. | `Joy.Hope`, `Triumph.Victory` |
| 12 | Ford v Ferrari | 2019 | Shelby quietly retired by his heart and Ken hot-headed and broke open the film in melancholy and camaraderie; the first successful GT40 test drive turns into discovery and exhilaration as the machine clicks; brake failure during night testing drops into visceral dread and pressure; the final laps at Le Mans climb into kinetic chase and victory; lands on Shelby driving alone after Ken's senseless death — bereavement carried in tenderness. | `Grief.Bereavement`, `Warmth.Tenderness` |
| 13 | The Greatest Showman | 2017 | Wide-eyed rooftop dreams and the museum risk open in hope and discovery; Jenny Lind singing "Never Enough" turns the film into awe and yearning toward high-society acceptance; the mob burning the circus drops into melancholy and existential dread as Barnum loses everything; rebuilding under the tent and the joyous final ensemble number lifts into cathartic camaraderie; lands on Barnum handing over the hat to watch his daughters grow — tenderness in self-actualization. | `Warmth.Tenderness`, `Triumph.Self_actualization` |
| 14 | Bajrangi Bhaijaan | 2015 | A mute girl separated from her mother begins silently following a jovial stranger — tenderness threaded with mystery from the first scene; the discovery that she is from Pakistan turns the film into confrontation and conviction; Pawan beaten in the Pakistani jail drops into visceral suffering held by sacrificial conviction; the border-fence crowd surges in cathartic suspense; lands on Munni finding her voice and the final tearful embrace — hope earned in tenderness. | `Joy.Hope`, `Warmth.Tenderness` |
| 15 | Andhadhun | 2018 | Akash faking his blindness for cheap rent opens in humor threaded with mystery; silently witnessing the body disposal while still playing the piano turns the film into suspense and stakes; Simi forcing the poison into his eyes drops everything into visceral dread and loss of innocence as the lie becomes real; the organ-harvester escape and final car chase compress into kinetic dread; lands in Europe on the cane flicking the can — mystery and unresolved guilt, trust withheld from the viewer. | `Wonder.Mystery`, `Moral_weight.Guilt` |

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
  Eternal Sunshine would force a real data model decision: tag emotional
  beats by story chronology or audience-experience chronology. Deferred to
  v2.

Two additional gaps surfaced from the eval-set labeling itself, in the
taxonomy rather than the corpus. See `taxonomy/v2_candidates.md`.

## Format

Each row contains:

- **One-line emotional arc** — the felt journey of the film in one sentence,
  using vocabulary from `taxonomy/v1.json`. Plain language, written from
  memory, no plot summary.
- **Endpoint** — one or more tag IDs from the taxonomy describing where the
  final 5–10% of the film lands the viewer. The matching algorithm checks
  this most heavily, so it has to be honest. Layered endings get layered
  endpoints — Endgame, Interstellar, and Dark Knight all have 3–4 tags
  because their endings genuinely hold multiple feelings simultaneously.