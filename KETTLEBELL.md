# Kettlebell rounds — feature proposal

Bring strength & conditioning into the corner: the coach calls kettlebell
stations the same way he calls combos, so a bag session and a bell session live
in one app, one timer, one record.

## Why kettlebells, and what the sources say

Kettlebell work is the standard S&C companion to boxing: ballistic hip-hinge
movements mimic the ground-up power transfer of a punch, and round-based bell
circuits condition you to recover inside a one-minute rest — exactly the
fight-shaped intervals Coach Fred already runs.

Sourced structures worth shipping as-is:

- **FightCamp (Coach PJ) — top 5 KB exercises for fighters:** swings (10–20),
  squat jumps (10–20), rotational swings (10–20), halos (5–10 each side),
  wrist rolls (10–20). Recommended as a circuit or a finisher after bag work.
- **FightCamp — Shanie Smash's 4-round circuit:** 4 rounds of
  swings ×25 → goblet squats ×20 → clean & press ×10/side →
  single-leg deadlift ×10/side → plank drag ×5/side.
- **Kettlebell EMOM convention:** work 30–45s at the top of each minute, rest
  the remainder, 10–30 minutes total — identical to the app's existing EMOM
  format, just with a bell in your hands.
- **Knockout Coaching:** round-based KB conditioning built around boxing's
  3:00 work / 1:00 rest cadence, training recovery inside the rest.
- **General guidance (FightCamp, ExpertBoxing, RDX):** 2–3 KB sessions a week,
  technique before load.

Sources: [FightCamp top-5](https://blog.joinfightcamp.com/training/top-5-kettlebell-exercises-for-fighters/),
[Shanie Smash circuit](https://blog.joinfightcamp.com/training/shanie-smash-s-4-round-kettlebell-circuit-for-boxing-training/),
[Kettlebell EMOM guidance](https://kettlebellsworkouts.com/kettlebell-emom-workout/),
[Knockout Coaching](https://knockout-coaching.com/unlock-explosive-power-kettlebell-conditioning-for-boxers/),
[ExpertBoxing](https://expertboxing.com/kettlebell-training-for-boxing),
[RDX](https://blogs.rdxsports.com/kettlebell-training-for-boxing/).

## How it fits the app (design)

The app already has the right bones: a **round format** is just a different way
of picking what the corner calls (`FORMATS`, with `footwork` as the closest
cousin — a list of named drills called as single instructions), and **Quick
start** presets are just canned `cfg` objects (`WORKOUTS`). Kettlebell slots in
as one new format plus three presets — no new timer, no new screens.

### 1. New round format: `kettlebell`

Unlike combos (random-gap calls), a KB round is **station-based**: the work
time divides into stations and the corner announces each one at its boundary.

- At the bell: *"Round two — swings."* The station name is also the big
  on-screen call, like combos today.
- Station changes on a fixed schedule (e.g. 5 stations in a 3:00 round ≈ 36s
  each): *"Goblet squats — go."*
- One-sided exercises get a *"switch sides"* call at the station midpoint
  (clean & press, halos, single-leg deadlift).
- Everything else is reused: the 3-2-1 count back in, the ten-second shout,
  rest-breathing cues, the bell, fatigue shaping off (steady pace — form over
  frenzy).

Exercise pool (a `KB_EXERCISES` const beside `FOOT_DRILLS`, each entry
`{name, twoSided, level}`):

| Exercise | Sided | Source |
|---|---|---|
| Swings | no | FightCamp, Shanie |
| Goblet squats | no | Shanie |
| Clean and press | yes | Shanie |
| Snatch | yes | EMOM convention |
| Rotational swings | no | FightCamp |
| Halos | yes | FightCamp |
| Squat jumps | no | FightCamp |
| Single-leg deadlift | yes | Shanie |
| Rows | yes | common KB staple |
| Get-ups | yes | boxing-KB staple (slow, advanced) |

Like combos, the pool is tickable so people skip what they can't do, and
`level` gates get-ups/snatches behind intermediate+.

### 2. New Quick-start presets (`WORKOUTS`)

- **KB circuit** — 4 × 3:00 / 1:00 rest, 5 stations per round, Shanie's
  ordering (swings → goblet squats → clean & press → single-leg deadlift →
  rotational swings). `format:"kettlebell"`.
- **KB EMOM** — 10 × 1:00, one exercise called at the top of each minute,
  rotating through the pool — mirrors the existing EMOM preset exactly.
- **Swing Tabata** — 8 × 20/10, swings only, all-out — sits naturally beside
  the existing Tabata card.

### 3. Hybrid "Bag & bell" sessions — free, via round-by-round

Because `kettlebell` becomes a normal format, **Round by round** mode
immediately supports the classic hybrid session: rounds 1–2 combos, round 3
kettlebell, repeat. Worth one more Quick-start card (**Bag & bell**, 6 × 3:00
alternating) to advertise it, and it makes the FightCamp "finisher" pattern —
bag session, KB last round — a one-tap setup.

### 4. Voice: ~12 new clips per pack

The corner is pre-rendered audio only (no TTS), so each exercise name plus
*"switch sides"* needs a clip: ~12 new phrases in `voice/phrases.json`,
rendered by `gen_voice.py` for both packs (Fred + Cal, ≈24 MP3s). Slugs come
free via the existing `slugify` convention. Until a pack is re-rendered,
`speak()` silently skips missing clips and the on-screen call still shows the
station — so the feature degrades gracefully, but shipping should include the
rendered clips like every other call.

### 5. Exercise guide (pics + how-to)

A caller shouting *"snatch — go"* is useless if you've never seen one, so each
exercise ships with a visual guide:

- **Line-art SVG illustrations, not photos.** Two or three key-position frames
  per exercise (e.g. swing: hinge → hip snap → lockout), drawn as simple
  stroke figures with `stroke="currentColor"`. This matters for three reasons:
  they're ~1–2 KB each so the offline PWA stays light (photos or GIFs would
  dwarf the app shell); they inherit every one of the 20 themes automatically
  (Drago's guide is Soviet red, Cyberpunk's is neon); and self-drawn art has
  no licensing problem, unlike scraped exercise photos.
- **A guide card per exercise:** the frames, 3–4 coaching cues in the corner's
  voice ("hinge, don't squat — the bell floats, you don't lift it"), the
  common fault to avoid, and which preset it appears in.
- **Where it lives:** a guide pane inside Setup, opened from an ⓘ on each
  exercise in the tickable pool — same interaction as the existing combo
  tooltips. During a session, the **rest screen shows the next station's
  frames** so you preview the movement before the bell, not during it.
- **First-run nudge:** the first time a KB preset loads, the quick-start
  toast offers "New to the bell? Open the guide" — one tap, dismissible,
  never shown again.
- **Safety line on the guide pane:** technique before load, 2–3 bell sessions
  a week (per FightCamp/RDX guidance) — the same sourced-guidance tone the
  README uses for round structures.

A working prototype of the art style lives in
[`kettlebell-art-preview.html`](kettlebell-art-preview.html) — the swing's
three frames (hinge → snap → lockout) drawn once as `<symbol>`s and rendered
across four real theme palettes, including Apollo's light scheme.

Everything stays inline in `index.html` (SVGs are markup, so the
self-contained/no-build rule holds and `sw.js` needs no new precache entries).
If the art grows past taste, the fallback is a separate `kettlebell-guide.html`
following the `reaction-drill.html` pattern.

### 6. Record & log integration

- `FORMAT_LABEL` entry so bells ring in ("Round three — kettlebell") and the
  session log shows KB days distinctly from bag days.
- KB rounds naturally stay out of punch tallies (no punch tokens), but count
  toward rounds/minutes/streak — a bell day keeps the streak alive.
- Later: a "bell rounds" lifetime total beside punches called.

## Implementation sketch (touch points)

All in `index.html` (self-contained, no build step):

1. `FORMATS` (~line 1053): add `["kettlebell","Kettlebell round","Called strength stations — swings, cleans, squats — on a fixed rotation."]`.
2. New `KB_EXERCISES` const beside `FOOT_DRILLS` (~line 1044).
3. Caller dispatch (~line 2282, where `footwork` branches): a `kettlebell`
   branch driven by the round clock (station boundaries + midpoint
   switch-sides) instead of random-gap `deliver()` calls.
4. `WORKOUTS` (~line 1076): the three preset cards (+ optional Bag & bell).
5. Tickable pool UI: reuse the movement-checkbox pattern from Setup → Combos.
6. Guide art: one inline SVG `<symbol>` per exercise (`id="kb-swing"` …),
   referenced from the pool's ⓘ guide pane and the rest-screen preview.
7. `voice/phrases.json` + `gen_voice.py` run for both packs.
8. `FORMAT_LABEL`, session-log summary line.

## Phasing

- **Phase 1** — format + 3 presets + clips + log label. Complete feature.
- **Phase 2** — exercise guide (SVG frames, cue cards, rest-screen preview,
  first-run nudge); Bag & bell hybrid card; per-exercise tick pool with levels.
- **Phase 3** — rep-target calls ("swings — fifteen"), KB block in a future
  program (the 4-week program's S&C day), bell-rounds lifetime total.

## Open questions

- Rep-count calling (EMOM style "ten swings") vs. pure time-based stations —
  time-based is simpler and matches the app's interval DNA; proposed default.
- Should Swing Tabata allow any single exercise ("Tabata anything")? Cheap to
  add once the pool exists.
- Get-ups are slow and risky under fatigue — gate to their own long-station
  preset later rather than mixing into fast circuits.
