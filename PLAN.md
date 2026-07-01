# Coach Fred — improvement plan

A session-by-session plan covering the full review: new-user usability, training
modes, new features, and camera integration. Each session is a self-contained,
shippable increment on the single-file / offline / no-build architecture —
nothing here requires abandoning it.

**Organizing principle (from the founder):** the first thing a user wants to do
is set **rounds, round length, and rest**. That is the app's core job. Today
those three sliders sit *fourth* in the Workout pane, below Quick start,
Structure, and Level. Every restructure below promotes the timer to the top and
demotes coaching nuance behind it.

---

## Session 1 — Deep usability review (audit, not code)

**Goal:** a written, prioritized usability audit that fixes the information
architecture on paper before any code moves. Output: `USABILITY_REVIEW.md`.

Scope:

- **Journey walkthroughs, step by step with friction counts** (taps, reads,
  decisions) for the five core journeys:
  1. First open → first completed round (including the silent-audio failure path)
  2. "I just want 5 × 2:00 with 0:30 rest" — the founder's headline case
  3. "Load a preset and go" (Quick start)
  4. "Drill one combo" (today: find Round format → Drill → picker)
  5. "Check what I did last week" (stats/log)
- **Setup-sheet IA redesign.** Decide the target structure. Candidates to
  evaluate against the journeys:
  - **A. Timer-first Workout pane:** Rounds / Length / Rest block at the very
    top, Quick start second (presets are shortcuts that *fill* the timer),
    Level third, everything else (stance, call style, pace, fatigue, movement
    mix, body shots) inside one "Coaching" accordion.
  - **B. Separate Timer tab:** tabs become `Timer · Coaching · Combos · More`.
    Timer holds rounds/length/rest/prep + Quick start + structure. Coaching
    holds level, stance, calls.
  - **C. Main-screen editing:** tap the clock / round tag on the idle screen to
    step rounds, length and rest right there — Setup never opens for the
    common case. (Highest value, most layout work; can layer on A or B later.)
  - Recommendation going in: **A now, C as a follow-up** — A is a reorder of
    existing DOM; C is the end state the audit should spec.
- **Control-level decisions:** sliders vs steppers vs tap-to-type for
  durations; where "Structure: Uniform/Custom" lives and what it's called
  ("Same every round / Round by round"); Setup-vs-Settings naming; which help
  poppers die because the layout now explains itself.
- **Terminology pass:** every label a non-engineer boxer would rename.
- **Ranked findings list** with severity (blocks first session / causes
  abandonment / papercut), each mapped to the session below that fixes it.

**Definition of done:** review doc committed; sessions 2–4 scopes confirmed or
amended by its findings.

---

## Session 2 — Timer-first Setup restructure + quick wins

**Goal:** implement the IA chosen in Session 1. The founder's case — set
rounds, time, rest — becomes the first thing the sheet shows.

- Reorder the Workout pane per the audit (default: option A above).
- Replace the three duration sliders with **steppers + tap-to-type** (reuse the
  existing `.stepper` component from the custom-round editor).
- Add a **"Get ready" (prep) duration control** — `cfg.prep` exists with no UI.
- **Idle-screen session summary line** under the clock: *"6 × 3:00 · 1:00 rest ·
  Build up · Combos"* — tap opens Setup on the timer block.
- **Quick start becomes load-and-go:** tapping a preset closes the sheet with a
  toast ("Club bag loaded — 6 × 3:00") and an optional "Start now" action.
- Quick wins bundle:
  - Voice speed re-baselined so default displays **1.0×** (internally unchanged).
  - Rename Uniform/Custom → "Same every round / Round by round"; resolve the
    Setup/Settings tab naming clash.
  - Beginner Quick start preset sets `callStyle:"both"` (teaches the numbers).
  - Remove `user-scalable=no` / `maximum-scale=1` (accessibility).
  - Fix: in Uniform + EMOM the hidden "Combos for all rounds" field still
    applies — show it for EMOM.
  - Fix: skipping a round in its final ~2s credits nothing to stats.

---

## Session 3 — First-run flow: audio check + slim tour

**Goal:** a new user hears the coach and starts a round inside a minute.

- **"Hear the coach" check** on first-ever Start: play a clip, ask
  "Did you hear that?" — on **No**, show the mute-switch / volume / unlock tips
  that currently hide in help poppers three levels deep.
- **Cut the auto-open tutorial from 12 steps to 3** (what it is → the controls
  → the number legend 1–6/b). Full 12-step tour stays behind the `?`.
- **Contextual first-visit hints** replace tour steps 6–10: one-time callouts
  the first time the user opens Setup, Combos, and the builder.
- First-run default session review: is 6 × 3:00 the right cold-open default,
  or should first-run land on the Beginner preset until changed?

---

## Session 4 — The corner sounds like a corner (voice upgrades)

**Goal:** the coach references the session state, not just "Round start".
Requires new clips via `gen_voice.py` (see VOICE_PACKS.md).

- **Round numbers at the bell:** "Round three" … and a distinct **"Final
  round"** line.
- **Rest-end lead-in:** at ~10s left in rest — "Ten seconds… round three,
  southpaw, body focus" — orientation without looking at the screen.
- **3-2-1 count back in** at the end of rest and prep.
- **Rest coaching lines** (sparse): breathing cue after a hard round; preview
  of the next round's focus.
- **Optional bell** — one recorded bell clip under Round start/end, as a
  toggle, keeping the voice-only default if preferred.
- **Warm-up segment (toggle):** 2–3 min opener of relaxed shadowbox/footwork
  calls before round 1.

---

## Session 5 — Modes I: Drill a combo, properly

**Goal:** "work one combo and build it up" becomes a first-class flow, not the
sixth row of a format `<select>`.

- **Fix the existing gap:** Custom-rounds Drill format has no combo picker —
  it silently drills a random combo (`drillCombo()` fallback). Add a per-round
  picker.
- **Ladder / Builder mode:** pick a target combo; the session constructs it —
  first two tokens → add a token per rung → full combo → full combo + layered
  defence/counter (reuse the phase-family grammar) → final rung mixes it into
  normal calling. Reuses `progressFactor()` and the drill beat.
- **Surface it as an intent:** a "Drill a combo" entry at the top of Quick
  start (or on the main screen), with combo picker + rounds count.
- **Speed ladder option:** same combo, shrinking call interval per rung
  (8s → 6s → 4s → burnout).
- **A/B drill:** two combos, alternating or randomly interleaved.

---

## Session 6 — Modes II + personal workouts

- **Save my workout:** name and save the current timer + coaching config as a
  chip in the Quick start grid; rides in the `.coach` backup; shareable like
  `.combo` files.
- **Shot focus in Uniform mode** (today it's Custom-rounds-only) — one
  "Focus" select in the uniform box covers "today is body-shot day".
- **Quiet / freestyle round type:** bell, ten-second warning, sparse
  motivation only — no combo calls.
- **Recall / memory mode:** early rounds call the full sequence, later rounds
  call only the combo *name*; you produce the sequence. (Camera-verifiable in
  Session 9.)
- **Post-session shot breakdown** on the summary card, computed from the
  tokens actually called: "~140 punches called · 38 jabs · 12 slips".
- **Weekly goal** alongside the day streak ("12 rounds this week: 8/12") —
  streaks punish rest days; weekly targets don't.

---

## Session 7 — Audio-only reaction + polish

- **Reaction calls without the camera:** random single calls ("slip!",
  "roll!", "2!") at unpredictable intervals with a pace dial — the reaction
  drill concept for everyone, offline, no camera.
- **Tap-to-hear in the combo library:** tap a row to play its call (clips are
  already cached) — browse by ear + doubles as an audio check.
- **`navigator.vibrate` round cues** on Android (training with music over the
  coach).
- **Landscape / prop-up layout** pass for the clock-dominant main screen.

---

## Session 8 — Camera I: the camera serves the caller

**Goal:** camera stops being a lab demo two pages away; sessions get measured.
Uses only shipped detectors (pose, guard, punch-thrown, bag-contact optical
flow) — no ML training.

- **Camera-scored rounds:** a "Use camera" toggle in the main timer (side-on,
  like Bag Coach). Per round: punches thrown / landed, guard drops, balance
  flags → into the session summary and "Your record".
- **Duty-cycling:** camera runs only during work segments (battery/heat);
  rest screen shows the round's numbers ("42 landed — beat it").
- **One session, one record:** Bag Coach and Reaction sessions land in the
  same history/stats/streak as timer sessions.
- **Beat-your-best for Reaction:** persist best/median reaction times into
  `stats` and the `.coach` backup; coach calls out a new best.

---

## Session 9 — Camera II: live cues + verified drilling

- **Live "hands up" cue** in main sessions using recorded clips (guard drop
  between combos → "hands up"; repeated overreach → "don't reach"), throttled
  to 1–2 per round.
- **Rep-gated ladder mode:** in the Session-5 Builder mode, advance rungs on
  N *landed* reps (bag-contact counting) instead of the clock — "ten more
  clean ones and we add the slip."
- **Verified defensive beats:** front-on placement, head-sway detector
  confirms the called slip direction; scores the Defence focus.
- **Reaction as a round type** in Custom rounds / a Quick start preset
  ("Fight IQ"), with the coach announcing the placement flip during rest.
- **Placement wizard:** one visual screen (top-down diagram + the live
  SIDE-ON badge) replacing the prose + confirm() gate; promote the camera
  entry out of Experimental once device-tested (iOS installed-PWA
  `getUserMedia` check first, per CAMERA_COACH.md).

---

## Session 10 — Program ("career mode") + second voice

- **Multi-week program:** a C25K-style plan (e.g. 4-week beginner → club
  fighter) that suggests the next session from history — "Week 2, day 3:
  4 × 2:00, body focus." Builds on stats, history, Build level, and
  Save-my-workout.
- **Second voice pack** via the existing multi-pack infrastructure
  (`gen_voice.py`, manifest, `#sVoice`): a contrasting personality; voice
  select appears in Settings once ≥2 packs exist.

---

## Long-term (separate track, per CAMERA_COACH.md backlog)

- **Punch-type classifier** (BoxingVI pretrain → self-recorded fine-tune,
  keypoint-based, TF.js/ONNX Web) — replaces the `classifyPunch()` heuristic.
- Then **combo verification**: corner calls "1-2-3", classifier confirms the
  sequence, coach reacts ("you dropped the hook"); per-combo accuracy in the
  summary. Interim step that needs no classifier: **count verification**
  (called 3, saw 2).
- **Adaptive calling from measured output:** pace responds to what was
  actually thrown, not just the clock.
- **Recall mode, camera-verified** (Sessions 6 + 9 converge).

---

## Sequencing rationale

| Order | Why it's early |
|---|---|
| Usability audit → timer-first restructure | The founder's stated #1 pain; everything else lands in a better-shaped app |
| Audio check + slim tour | Kills the most likely first-run failure (silence) |
| Voice upgrades | Cheap (clips only), transforms perceived quality |
| Drill-a-combo | The most-requested mode gap; camera later multiplies it |
| Camera I before Camera II | Scoring needs no new clips or UX invention; cues and gating build on it |
| Career mode last | Biggest scope; depends on saved workouts, breakdowns, and history being solid |

Each session ends with: manual test on a phone-sized viewport, bump
`APP_VERSION`, update the service-worker cache list if any new files, commit,
push.
