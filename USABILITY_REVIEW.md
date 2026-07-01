# Coach Fred — deep usability review (Plan Session 1)

**Method.** Instrumented walkthrough of `index.html` (v19) in Chromium at a
phone viewport (390 × 844, touch), driving the real UI and measuring taps,
scroll depth, control counts and element geometry — plus a full code read.
Numbers below are measured, not estimated. Raw data: appendix at the bottom.

**Headline.** The app's core job — *set rounds, round length, rest, go* — is
buried 1.24 screens deep in the Setup sheet, behind 25 interactive controls
that a new user must scroll past. Meanwhile the first-run experience
front-loads a 12-step, 435-word tutorial before the user has thrown a punch,
and the most likely first-run failure (silence) has a rescue path that takes
3 taps down an undiscoverable route. None of this needs new features to fix —
it needs the timer promoted to the front and everything else demoted behind it.

---

## 1. Journey walkthroughs

### J1 — First open → first completed round

| Step | What happens | Cost |
|---|---|---|
| Open app | 12-step tutorial auto-opens | 12 taps to read through (435 words), or 1 tap Skip |
| Land on main screen | Idle hint: "Tap start…" | Good: Start is obvious |
| Tap Start | 10s prep, then round 1 | 1 tap |
| **Failure path** | Phone on mute / volume down → **silence**, numbers flash | Nothing on screen indicates audio state |
| Rescue | gear → Settings tab → scroll → Test voice | 3 taps down a path nothing points to; the mute-switch tip is *itself* hidden behind a "?" popper |

- **Friction: the tour is a gate, not a guide.** 12 steps / 435 words / 12
  taps before the first punch. Steps 6–10 describe screens the user hasn't
  needed yet. Nothing in the tour plays audio, so the #1 failure mode
  (silence) is untouched by all 435 words.
- **The tour leaves a landmine:** it ends with Setup's third tab active, and
  the sheet **reopens on the last-viewed tab** (measured: `pane-more`). A new
  user's first real gear-tap after the tour lands on Settings — voice speed
  and themes — not Workout. Disorienting at the exact moment they're trying
  to find the timer.
- The default cold-open session is 6 × 3:00, Level "Build up" — 23 minutes.
  Reasonable for a club boxer; heavy for the "downloaded this at lunch"
  first-timer. Worth pairing the audio check with a "first session?" nudge to
  the Beginner preset.

### J2 — "I just want 5 × 2:00 with 0:30 rest" *(the founder's headline case)*

| Step | Cost |
|---|---|
| Tap gear | 1 tap (may land on wrong tab — see J1) |
| Scroll to Rounds | **814 px of scroll = 1.24 screens**, past Quick start (10 chips), Structure, Level, Stance — **25 interactive controls** before the first timer control |
| Set 5 rounds | slider drag |
| Set 2:00 | slider drag — **18.4 px per 15s stop** on a 350 px track, under the 26 px thumb; hitting exactly 2:00 is a precision task |
| Set 0:30 rest | slider drag, same problem |
| Close | 1 tap |
| Confirm it took | **The idle screen shows only `RND 01//06` + clock** — no rest, level or format anywhere. To re-check, reopen Setup. |

This journey is the app's reason to exist and it is the worst-served: ~6
interactions, three of which are precision drags, below a screen-and-a-quarter
of unrelated controls. **Every structural recommendation in §3 flows from
fixing this journey.**

### J3 — Load a preset and go (Quick start)

| Step | Cost |
|---|---|
| gear → tap "Club bag" | 2 taps |
| Feedback | chip highlights; **sheet stays open, no toast, no summary change visible** (measured: no status element exists) |
| Close, Start | 2 more taps |

4 taps, one of which produces near-invisible feedback. Users who miss the
chip highlight can't tell whether the preset loaded — and since the timer
sliders are below the fold, they can't see the values change either. Also:
any later slider touch silently clears the preset highlight (`touchWorkout`),
which is correct behaviour but invisible when it happens off-screen.

### J4 — Drill one combo

| Step | Cost |
|---|---|
| gear → scroll 1.24 screens → Round format select | "Drill (one combo on repeat)" is the **6th of 6 options** in a `<select>` |
| Pick the combo | a flat native select with **135 unlabelled-by-group options** |
| Set the beat | 3–30s slider: 28 stops on 350 px = **12.5 px per stop**, the worst slider in the app |
| Close, Start | 2 taps |

Discoverability is the real failure: someone whose goal is "groove my
1-2-3-slip" will never think to look under *Round format*. Intent-first
naming ("Drill a combo") beats format-first.

**Confirmed bug — Custom rounds:** the per-round Format select offers Drill,
but the round card renders no combo picker (measured: card selects are Work /
Rest / Combos / Format / Shot focus only). `drillCombo()` then silently falls
back to a random combo — the round *looks* configured and does the wrong thing.

### J5 — Check what I did last week

gear → Settings tab → "Session log" accordion → open. 3 taps, findable, and
the post-session summary deep-links to it (`sumLog`). **This journey is fine.**
Only note: the log lives under a tab named "Settings", which is the last place
users look for their history — see terminology, §5.

---

## 2. Ranked findings

Severity: **S1** can block or end a first session · **S2** causes confusion /
abandonment · **S3** papercut. Each finding maps to the plan session that fixes it.

| # | Sev | Finding | Evidence | Fix in |
|---|---|---|---|---|
| 1 | S1 | Silent first session has no on-ramp rescue: no audio check, rescue is 3 undiscoverable taps, tips hidden in poppers | J1 | S3 |
| 2 | S1 | 12-step / 435-word tutorial gates the first punch | J1 | S3 |
| 3 | S1→S2 | Timer controls (rounds/length/rest) buried 1.24 screens deep behind 25 controls | J2 | **S2** |
| 4 | S2 | Duration sliders: 18.4 px (work/rest) and 12.5 px (drill) per stop, under a 26 px thumb — precision drags for exact values | J2, J4 | S2 |
| 5 | S2 | Idle screen shows no session config beyond round count + clock; changes made in Setup can't be confirmed at a glance | J2 | S2 |
| 6 | S2 | Quick start gives near-zero feedback and doesn't offer to start | J3 | S2 |
| 7 | S2 | Custom-round Drill format silently drills a random combo (no picker) | J4, code `drillCombo()` | S5 |
| 8 | S2 | Setup reopens on the last-viewed tab, incl. the tab the tour abandoned it on | measured | S2 |
| 9 | S2 | Difficulty is spread over 7 interacting dials (Level, pace, movement mix, body shots, fatigue, format, focus) with no visible hierarchy — evidenced by **8 help poppers** in one pane needed to explain it | pane inventory | S2 |
| 10 | S2 | Drill mode undiscoverable: intent hidden as the last option of a format select | J4 | S5 |
| 11 | S3 | Drill combo picker: flat 135-option native select | J4 | S5 |
| 12 | S3 | "Uniform" / "Structure" / Setup-vs-Settings naming (full pass in §5) | — | S2 |
| 13 | S3 | Voice speed displays 1.25× as neutral default | code | S2 |
| 14 | S3 | Beginner preset calls numbers a beginner doesn't know (`callStyle:"numbers"`) | code | S2 |
| 15 | S3 | `user-scalable=no, maximum-scale=1` blocks zoom (WCAG 1.4.4) | measured meta | S2 |
| 16 | S3 | Help "?" buttons are 18 × 18 px — below WCAG 2.2's 24 px minimum and far under the 44 px HIG target; sheet close "×" hit area 26 × 30 px | CSS + measured | S2 |
| 17 | S3 | Uniform + EMOM: "Combos for all rounds" field hidden but still applied | code `syncFormatUI` | S2 |
| 18 | S3 | Skipping a round in its last seconds credits nothing to stats | code `onRoundComplete` | S2 |
| 19 | S3 | `cfg.prep` (Get ready) has no UI; presets silently reset it to 10s | code | S2 |
| 20 | S3 | Decorative HUD text ("SYS//RDY 0x1A") on the default theme reads as system status to a first-timer | screenshot | S2 (copy tweak) |

---

## 3. The IA decision — where do rounds / time / rest live?

Candidates evaluated against J2/J3 (full option descriptions in PLAN.md):

**A. Timer-first Workout pane** — move the timer block (Rounds · Round length
· Rest · Get ready, as steppers) to the very top of the Workout pane; Quick
start second; Level third; stance + all Coach-calls dials collapse into one
"Coaching" accordion.
- J2 becomes: gear → set → close (0 scroll, 0 precision drags).
- J3 improves for free: preset chips sit directly *below* the timer values
  they change, so loading a preset visibly updates them.
- Cost: a DOM reorder plus the stepper component that already exists
  (`.stepper` in the custom-round editor). No new architecture.

**B. Separate Timer tab** (`Timer · Coaching · Combos · More`).
- Also fixes J2, but 4 tabs are cramped at 390 px, presets straddle the
  Timer/Coaching split awkwardly, and it *adds* a navigation decision for the
  most common journey rather than removing one.

**C. Main-screen editing** — tap the clock / summary line on the idle screen
to step rounds, length and rest without opening Setup at all.
- The best end state for J2 (0 taps into Setup) and it makes the idle screen
  self-describing. But it's new UI on the most sensitive screen and interacts
  with start/pause states.

**Decision: A in Session 2, with C specced as the follow-up.** Concretely for
Session 2:

1. Workout pane order: **Timer block → Quick start → Level → "Coaching"
   accordion** (stance, call style, pace, fatigue, movement mix, body shots)
   → Structure ("Round by round") entry → Round format.
2. Timer block uses steppers (15s steps, hold-to-repeat) + tap-the-value to
   type. Includes the currently UI-less **Get ready** duration.
3. **Idle-screen summary line** under the clock — `5 × 2:00 · 0:30 rest ·
   Build up` — tap opens Setup on the Workout tab (this also resolves finding
   8: opening via the summary line always lands on Workout; the plain gear
   can keep last-tab behaviour for power users).
4. Quick start chips: tapping one updates the timer block in view **and**
   shows a one-line confirmation with a "Start now" action.
5. Help poppers in the Workout pane: target ≤ 3 remaining once layout
   explains hierarchy (Level keeps one; movement/body merge into the
   Coaching accordion's single intro note).

**Spec for C (build after A beds in):** the idle summary line becomes
tappable chips — `[5 ×] [2:00] [0:30 rest]` — each opening a thumb-reach
stepper popover. No sheet. Start button unaffected. Guard: disabled while a
session is running.

---

## 4. Control-level decisions

| Control | Today | Decision |
|---|---|---|
| Rounds (1–15) | slider | stepper |
| Round length (0:15–5:00) | slider, 18.4 px/stop | stepper, 15s steps, tap-to-type |
| Rest (0–3:00) | slider | stepper, 15s steps |
| Get ready | none | stepper (0–60s), in the timer block |
| Drill interval (3–30s) | slider, 12.5 px/stop | stepper |
| Voice speed | slider | keep slider (continuous is right), re-baseline display to 1.0× |
| Structure Uniform/Custom | seg buttons at top | rename + move below timer (§3) |
| Round format | `<select>` | keep select for now; **remove "Drill" from it** when Session 5 gives drilling its own entry point |
| Drill combo picker | flat 135-option select | group `<optgroup>` by Basics/Power/… now; searchable picker when Session 5 rebuilds the flow |
| Help "?" buttons | 18 px circle | ≥ 24 px hit area (padding, not visual size) |
| Sheet close "×" | 26×30 hit area | pad to ≥ 44 px |
| Viewport meta | `user-scalable=no` | drop `maximum-scale` / `user-scalable` (double-tap zoom suppression is already handled by `touch-action` on buttons) |

---

## 5. Terminology pass

| Today | Problem | Proposed |
|---|---|---|
| "Uniform" / "Custom rounds" | engineer-speak | **"Same every round" / "Round by round"** |
| "Structure" | vague | fold into the timer block; the seg control needs no heading once it reads "Same every round / Round by round" |
| Sheet "Setup" containing tab "Settings" | two names, nested | rename third tab **"More"** (its DOM id is already `pane-more`) |
| "Combos for all rounds" | 4 words for "pool" | **"Combo pool"** |
| "Movement mix" | movement of what? | **"Defence & movement"** |
| "Fatigue shaping" | reads clinical | **"Corner pacing"** with note "eases mid-round, pushes the final ten" |
| "Round format" | format-first | **"Round type"** |
| "Quick start" | fine | keep |
| "Call style" | fine | keep |
| "Shot focus" | fine | keep |
| Tour title "Your corner man" | fine | keep — the voice of the copy is a strength; the problem is quantity and placement, not tone |

---

## 6. What's working — don't break these

- **The voice and copy personality** ("Lace up, hands up") — distinctive,
  keep it through every rename.
- **Start / Pause / Skip / Reset** footer: correct, obvious, thumb-sized.
- **Post-session summary → log deep-link** (J5): the best journey in the app.
- **Quick start preset *content*** (ring-standard structures): right idea,
  wrong feedback.
- **Group All on/off + level badges** in the combo library.
- **Help-popper mechanism** itself (collapsed by default) — the issue is that
  the Workout pane *needs* 8 of them; the target is fewer questions, not
  fewer answers.
- Safe-storage wrapper, XSS escaping on imported combo names, schedule
  engine, clip normalisation — solid under the hood; nothing in this review
  touches the engine.

---

## 7. Acceptance criteria for Session 2 (measurable)

Re-run this audit's script after Session 2; the restructure passes when:

1. J2 = gear → 3 stepper interactions → close, with **0 px scroll** to the
   first timer control and **0 slider drags**.
2. Idle screen states rounds × length · rest (+ level), and updates within
   one frame of closing Setup.
3. Quick start tap produces visible confirmation + optional immediate start.
4. Workout pane: ≤ 3 help poppers; first screenful contains the complete
   timer block.
5. Setup opened from the summary line lands on Workout 100% of the time.
6. No slider remains whose per-stop distance is under 24 px.

---

## Appendix — raw measurements (390 × 844, v19)

```
firstRun:        tutorial auto-opens; 12 steps; 12 taps; 435 words
idleScreen:      shows "RND 01//06", clock "03:00", start hint only
setupReopensOn:  "more" (last-viewed tab persists)
timerJourney:    Rounds field 814 px from pane top; sheet viewport 659 px
                 => 1.24 screens of scroll; 25 interactive controls above;
                 work slider: 350 px track / 20 stops = 18.4 px per stop
workoutPane:     59 buttons, 13 selects, 4 sliders, 2 toggles, 8 help
                 poppers; pane 1.9 screens tall with accordions closed
quickStart:      sheet stays open; no toast/status element; chip highlight only
drillUniform:    picker appears; 135 flat options; Drill is option 6 of 6
drillCustomRound: no combo picker in round card (Work/Rest/Combos/Format/
                 Shot focus only) -> silent random-combo fallback
logJourney:      3rd tab + closed accordion; summary card deep-links (good)
a11y:            viewport blocks zoom; steel-on-canvas contrast 4.89:1 (AA
                 pass); help-btn 18x18 CSS px; sheet close hit area 26x30
audioRescue:     3 taps (gear -> Settings -> Test voice), no signposting
```

Audit script: Playwright walkthrough (kept out of the repo; results frozen
above). Screenshots captured at each journey step during the run.
