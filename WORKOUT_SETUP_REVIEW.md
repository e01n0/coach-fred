# Workout setup review — new-user walkthrough (v32)

**Method.** Fresh-profile walkthrough of `index.html` (v32, post-overhaul) in
Chromium at a phone viewport (390 × 844, touch), driving the real UI and
measuring geometry, plus a code read. Focus: setting up **each kind of
workout** as a first-timer, the **Round by round** editor specifically, and
the question **"should workout setup and settings be separated?"**

**Headline.** The Session-2 overhaul landed: timer-first pane, 3-step tour,
idle summary line, preset confirmation with Start now. The remaining pain is
concentrated in one place, and it's exactly the one reported: **"Round by
round" throws away every piece of context the rest of the pane worked to
build** — the toggle you tapped teleports 1,100 px away, the timer and total
disappear, and the cards that replace them show numbers unrelated to what you
just set. Second-order: the Workout pane now hosts **five overlapping "what
kind of workout" systems** (timer+mode, Quick start, Round type, Drill a
combo, 4-week program) with formats like EMOM appearing in two of them, which
is the real source of the "lost in the settings" feeling — more than the
setup/settings co-location.

---

## 1. What the overhaul fixed (verified working — don't regress)

| Previous finding | Now |
|---|---|
| 12-step / 435-word tour gate | 3 steps, ~122 words, sheet closed after |
| Timer buried 1.24 screens deep | Steppers at very top, total time readout, tap-to-type works |
| Idle screen showed nothing | `3 × 2:00 · 1:00 REST · BEGINNER` summary line |
| Quick start had no feedback | Chip highlight + sticky "Tabata loaded — 8 × 20/10 · START NOW" bar (5 s) |
| Custom-round Drill silently random | Per-round "Combo to drill" picker renders and persists |
| Setup reopened on last tab | Always lands on Workout |
| Drill picker 135 flat options | Grouped into 5 optgroups |

Default session is now 3 × 2:00 Beginner — right-sized for a first-timer.

---

## 2. The complaint, measured: "Round by round loses context"

Tapping **Round by round** (fresh profile, after setting a uniform timer):

| What happens | Measured |
|---|---|
| The toggle you just tapped moves | from y ≈ 353 to y ≈ **1,470** — pushed below the round cards; finding it again to switch back is a scroll hunt |
| The timer block + total time vanish | `uniformBox` hidden; **no total-session readout exists anywhere in custom mode** |
| Cards show unrelated values | Uniform was 2 × 1:00 / 0:30; cards appear as 3 × 3:00 / 1:00 (the separate, stale `cfg.program`) |
| One round card | **363 px tall, 11 controls** (label, ↑ ↓ ×, Work/Rest steppers, Combos, Round type, Shot focus) |
| 3 rounds | 1,109 px of cards; pane 2,205 px = 3.2 screens |
| 8 rounds | 2,974 px of cards; pane **6.7 screens**; the viewport shows ~1.3 cards, and the top card's name is off-screen so you can't tell which round you're editing |
| Idle summary degrades | `3 rounds · round by round` — no times, no total |

So the user's mental model is destroyed twice: once on entry (my numbers
changed and my anchor moved), and continuously while editing (no overview —
editing round 6 while remembering what round 2 was is impossible).

**Adjacent traps found while in custom mode:**

- **Drill a combo is a silent no-op in custom mode.** The accordion stays
  visible, settable, and shows its "BUILD UP" badge — but `buildSchedule()`
  ignores `cfg.format` on the custom branch (per-round formats only). The UI
  claims a drill session it will never run.
- **Tapping any Quick start chip while in custom silently flips you back to
  uniform** (every preset carries `mode:"uniform"`). Your cards survive but
  vanish from view; they resurface — stale — next time you tap Round by round.
- **No duplicate-round control.** Cards offer ↑ ↓ × only, so "6 rounds the
  same, round 4 different" means hand-configuring 6 × 11 controls. Add round
  always appends a 3:00/1:00 default, not a copy of the last round.

---

## 3. Setting up each kind of workout (new-user pass)

- **Uniform (5 × 2:00, 0:30 rest)** — *good.* Gear → 7 stepper taps → close;
  0 scroll, total updates live, idle line confirms. The Session-2 acceptance
  criteria pass.
- **Quick start preset (Tabata/HIIT/Club…)** — *good feedback*, two papercuts:
  presets also silently set Level / pace / call style (Tabata → Intermediate +
  Relentless) with nothing visible changing on screen — inconsistently
  (Pyramid/Burnout keep your Level but set pace). A first-timer who tapped
  Beginner earlier and then Tabata is now Intermediate without knowing it.
- **EMOM / Pyramid / Burnout / Footwork** — *confusing double identity.* Each
  exists **both** as a Quick start chip and as a Round type select option.
  Chip = timing + format; select = format only. A new user who wants "EMOM
  but 12 minutes" has no way to know whether to tap the chip then edit, or
  set the select — both work, differently (the chip also rewrites rest/pace).
- **Drill a combo** — *discoverable and well-explained now* (own accordion,
  state badge, grouped picker, beat notes). Two issues: turning it on makes
  Round type / Combo pool / Shot focus silently disappear (fields vanish with
  no note saying the drill replaced them), and the custom-mode no-op above.
- **Round by round** — see §2. This is the one broken flow.
- **4-week program** — loads correctly with the toast + Start now. Fine.

**Control count:** the Workout pane totals **104 interactive controls**
(2.36 screens with accordions closed). Coaching (bell, vibrate, camera, call
style, pace, corner pacing, defence, body shots, stance) is collapsed but
still adds ~30 of them to the same pane.

---

## 4. Ranked findings

Severity: S1 blocks/breaks a session · S2 confusion/abandonment · S3 papercut.

| # | Sev | Finding |
|---|---|---|
| 1 | S2 | Round-by-round entry: toggle teleports below 1,100+ px of cards; timer/total hidden; no anchor survives the switch |
| 2 | S2 | Custom program is a second, disconnected state — doesn't seed from the uniform timer you just set; stale cards resurface later |
| 3 | S2 | No session overview in custom mode: no total time, no compact structure view; 8 rounds = 6.7 screens; active card's label scrolls off |
| 4 | S2 | Drill a combo silently inert in Round-by-round mode (badge still shows) |
| 5 | S2 | Quick start chip while in custom silently flips mode to uniform |
| 6 | S2 | Five overlapping "workout kind" systems in one pane; EMOM/Pyramid/Burnout/Footwork duplicated between Quick start and Round type |
| 7 | S2 | Presets silently change Level/pace/call style, inconsistently across presets |
| 8 | S3 | No duplicate-round; Add round appends a default, not a copy of the last round |
| 9 | S3 | Idle line in custom mode drops all times (`3 rounds · round by round`) |
| 10 | S3 | Drill on: Round type / pool / focus fields vanish without explanation |
| 11 | S3 | "More" tab mixes history (Your record, Session log) with device settings (voice, theme, backup, camera) |

---

## 5. The setup-vs-settings question

**Short answer: the instinct is right, but the split that matters is not
"workout sheet vs settings sheet" — it's *today's session* vs *how the coach
behaves*, and *state that survives the mode switch* vs *state that doesn't*.**
Moving settings elsewhere without fixing §2 would leave the reported problem
intact; fixing §2 removes most of the "lost" feeling even with the current
tabs.

Recommended order:

### 5a. Fix Round by round in place (the complaint — do this first)

> **Status: shipped in v33** (same branch). All eight items below are
> implemented and verified with a fresh-profile Playwright pass: toggle
> pinned above the content (0 px movement on switch), `N rds · total`
> header, program seeds from the uniform timer until first touched
> (`cfg.progTouched`), collapsed one-line rows with single-open expansion
> (5 rounds fit one screenful), duplicate + copy-last Add round with
> generic-label renumbering, drill accordion hidden in custom mode with a
> pointer to the per-round Drill type, preset/plan toast appends
> "· same every round" when it flips the mode, idle line reads
> `5 rounds · 12:10 · round by round`.

1. **Pin the context header.** Keep a compact, always-visible summary at the
   top of custom mode: `4 rounds · 15:00 total` (reuse `vTotal`). The timer
   block may hide; the *totals* must not.
2. **Move the mode toggle above the block it switches** so it never moves —
   today it sits below `uniformBox`/`customBox` and gets shoved 1,100 px down
   the moment cards render.
3. **Seed the program from the current uniform setup** on first switch (or
   whenever the program hasn't been touched): N rounds × work/rest copied
   over. The numbers a user just set must be the numbers they see.
4. **Compact round rows, expand-one-at-a-time.** Render each round as a
   one-line row — `R3 · 3:00 · 0:30 rest · Burnout` — expanding to the full
   card on tap (single-open accordion). The whole session structure becomes
   one screenful; "which round am I editing" is always answered.
5. **Add a duplicate button** per round; make **Add round copy the last
   round** instead of a fixed default.
6. **Resolve Drill × custom:** hide the Drill accordion in custom mode with a
   one-line note ("Drills are per-round here — pick Drill as a Round type"),
   or make it apply. Never show an active badge that does nothing.
7. **Preset taps while in custom** should say what they're about to do
   ("Switches to Same-every-round") on the confirmation bar — cheap honesty.
8. Idle line in custom mode: `4 rounds · 15:00 · round by round`.

### 5b. Then thin the Workout pane (the "lost in settings" feeling)

1. **One system for "what kind of workout."** Quick start chips stay the
   entry point for *sessions*; Round type stays the knob for *round content*.
   Kill the duplication by making the chips visibly set the same controls
   (the confirmation bar could name what changed: "Tabata — 8 × 0:20/0:10,
   pace Relentless"). Presets should stop silently rewriting Level/call
   style, or the bar must say so.
2. **Move the Coaching accordion out of the Workout tab.** It's persistent
   preference, not session setup — it belongs with voice/audio. Re-scope the
   tabs as **Workout · Combos · Coach & app** (or keep "More" as the name),
   and let "Your record / Session log" move to the top of that pane or,
   better, behind the stats already shown on the post-session screen.
   This takes the Workout pane from 104 controls to ~70 and makes it
   single-purpose: *what am I doing today*.
3. Only if the pane still feels crowded after 1–2, consider a fourth tab or
   a separate settings sheet — at 390 px, three tabs is already the limit,
   and every extra navigation decision costs the main journey.

---

## Appendix — raw measurements (390 × 844, v32, fresh profile)

```
tour:            3 steps, ~122 words; sheet closed after; reopen lands Workout
workout pane:    scrollHeight 1611 px = 2.36 screens; 104 controls total;
                 16 controls in first screenful (timer block complete)
segMode:         y=353 uniform → y=1470 after switching to custom
custom cards:    363 px / 11 controls each; 3 rds = 1109 px; 8 rds = 2974 px,
                 pane 6.7 screens; vTotal hidden in custom mode
uniform↔custom:  independent state; uniform 2×1:00 → custom shows 3×3:00
preset tap:      chip highlight + toast w/ START NOW (5 s); sets mode uniform
                 even from custom; Tabata sets level=intermediate silently
drill:           own accordion, badge, 5 optgroups; inert in custom mode
                 (buildSchedule custom branch reads per-round format only)
idle line:       uniform "3 × 2:00 · 1:00 REST · BEGINNER" (good)
                 custom  "3 rounds · round by round" (no times)
more pane:       record/goal/log + voice/speed/silent/test/theme/backup/camera
```

Walkthrough script: Playwright, kept out of the repo; screenshots captured at
each journey step during the run.
