# Coach Fred — next ideas & gap analysis (post-v33)

> **Status (v35):** gaps 1, 2, 3, 5, 8, 9, 10 (rollups), 12 (partly — Bag Coach
> now records; in-timer reaction scoring still open) and 13 (reduced-motion)
> are fixed; hygiene items 24–27 shipped; ideas 1–5 (records, trend,
> milestones, bests, graduation) and 9 (Shadowbox) are in. Everything else
> below is still open.

All ten PLAN.md sessions are shipped. This is the follow-up pass: what's left
hanging in the code as of v33, and where the app can go next. Grounded in a
full code read of `index.html` (v33), `sw.js`, the voice pipeline and the two
camera pages — every gap below points at real code, not speculation.

---

## 1. Gaps and loose ends in v33

Severity: **S1** wrong/broken today · **S2** promised-but-missing or
dead-end · **S3** papercut / hygiene.

| # | Sev | Gap | Where |
|---|---|---|---|
| 1 | S1 | **Bag Coach data is siloed.** `camera-coach.html` writes its sessions to `coachfred.cc`, which `index.html` never reads — those workouts never reach Your record, the session log, or the streak. "One session, one record" (Plan Session 8) holds for Reaction but not Bag Coach. | camera-coach.html; grep `coachfred.cc` in index.html = 0 hits |
| 2 | S2 | **Everything is counted, nothing is totalled.** `deliver()` tallies punches, per-shot counts and defensive moves live; camera rounds bank thrown/guard-drops — but only per session-log entry. There is no lifetime "punches called", no favourite shot, no defensive-move total, no camera aggregates. The all-time best streak (`stats.best`) is stored and *never rendered*. | index.html:1867, 3367 |
| 3 | S2 | **Finishing the 4-week program is a dead-end.** One line of text, the Load button disables, and the pointer sits there until a manual reset. No badge, no "what next", no follow-on plan — the app's biggest commitment device just stops. | index.html:2948 |
| 4 | S2 | **Programs can only express uniform sessions.** `PLAN_SESSIONS` entries are uniform-mode cfgs and `planLoad` assumes it — a future program can never include a round-by-round session (e.g. "rounds 1–2 combos, round 3 burnout"). | index.html:2924, 2962 |
| 5 | S2 | **Round-by-round sessions log as "Custom · N rounds".** The per-round formats/focuses you carefully set are thrown away at record time, so the session log can't tell a footwork day from a body day. | index.html:2429 |
| 6 | S2 | **Session-arc drills are uniform-only.** Speed / Build-up / Recall need the whole session's arc (by design, per the code comment) — but nothing offers a "drill block" inside a custom session, and the Drill accordion simply hides in custom mode. | index.html:1027 |
| 7 | S2 | **Fresh installs aren't actually offline.** The SW precaches only the shell; all 793 voice clips (×2 packs) and the ~17 MB pose runtime are runtime-cached on first *use*. A user who installs at home and goes to a basement gym gets a silent coach. No "download everything now" control exists. | sw.js:4-13, 62 |
| 8 | S3 | **Version drift:** `APP_VERSION = "v33"` but the SW cache tag is `coachfred-v34` — the visible build tag is stale. | index.html:2521, sw.js:3 |
| 9 | S3 | **`window.__camSim` dev hook ships in production.** Harmless but should be gated behind a dev flag. | index.html:2250 |
| 10 | S3 | **Session log caps at 60 entries with no rollup** — long-term users silently lose their history; no month/week aggregate survives the cap. | index.html:2441 |
| 11 | S3 | **Themes are visual-only.** 21 fighter skins, one coach. Picking Drago or Ali changes the CSS vars and nothing else — no voice, no catchphrase, not even a themed motivation line. The multi-pack voice plumbing is already there. | index.html:1361, 1554 |
| 12 | S3 | **Reaction time is measured only on the standalone page.** "Best slip" in Your record depends entirely on `reaction-drill.html`; the in-timer Reaction round type calls shots but measures nothing. | index.html:2071, 3376 |
| 13 | S3 | Accessibility: no `prefers-reduced-motion` handling; no screen-reader pass has been done on the sheet/accordion structure. | global |
| 14 | S3 | From WORKOUT_SETUP_REVIEW: EMOM/Pyramid/Burnout/Footwork still live a double life as Quick-start chips *and* Round-type options (finding 6) — mitigated by the confirmation bar, not resolved. | index.html:1017, 1039 |

---

## 2. New feature ideas

Grouped by theme; **effort** is relative to past sessions (S = a quick-wins
bundle, M = one session, L = multi-session or new asset spend).

### A. Progress & motivation (cheapest wins — the data already exists)

1. **Lifetime totals in Your record** *(S)* — aggregate the history array (and
   keep running totals so the 60-entry cap doesn't matter): total punches
   called, favourite shot, defensive moves, camera punches thrown, all-time
   best streak (already stored — gap #2). One render function, no new data.
2. **Weekly trend strip** *(S–M)* — rounds/minutes per week for the last ~8
   weeks as a tiny bar row in Your record. Needs weekly rollups that survive
   the history cap (fixes gap #10 as a side effect).
3. **Milestones** *(M)* — first session, 100 rounds, 1,000 punches called,
   10-session streak, program graduate. A dozen thresholds over the aggregates
   from idea 1, celebrated once on the summary card and listed in Your record.
   Cheap, and it gives the streak-breaker a reason to come back.
4. **Personal bests** *(S)* — longest session, most rounds in a day, best
   camera round (landed). The summary card already compares "42 landed — beat
   it" within a session; make it lifetime.

### B. Programs (the career mode has one rung)

5. **Program completion → graduation** *(S)* — fix the dead-end (gap #3):
   badge on the record, a "program graduate" summary card, and an explicit
   pointer at the next program.
6. **More programs** *(M)* — `PLAN_SESSIONS` is already data-driven; add a
   program *picker* with 2–3 more plans: an 8-week "club → pro distance"
   continuation, a 2-week defence course (movement-heavy, camera-verified
   where available), a body-work month. Content design, near-zero engine work.
7. **Build-your-own program** *(M)* — sequence saved workouts ("My workouts")
   into an N-session plan with the same pointer/tick-off mechanics. Save-my-
   workout + PLAN_SESSIONS already contain all the pieces.
8. **Custom sessions inside programs** *(M)* — lift the uniform-only
   restriction (gap #4) so future plans can include round-by-round days.

### C. Training content

9. **Shadowboxing mode** *(S–M)* — a first-class "no bag today" session:
   footwork/movement-forward calling, no burnout/EMOM assumptions, sparse
   power cues. Mostly a preset plus caller weighting — the movement grammar
   already exists. (Front-on camera could later verify slips, per Session 9
   infrastructure.)
10. **Sparring simulation rounds** *(M, needs ~a dozen new clips)* — the
    corner narrates an opponent: "he jabs — slip it, counter two", "he's
    crowding you — pivot out". Reuses `counterFor()` logic in reverse. The
    single most "corner-man" feature on this list.
11. **Rest-period tasks** *(M, needs clips)* — optional conditioning on rest:
    "ten push-ups", "shake it out, breathe". A toggle beside the warm-up one.
12. **Surprise me** *(S)* — one chip that generates a session (random valid
    structure + focus + round types, seeded away from recent history). Zero
    new engine, high replay value.
13. **Southpaw conversion / switch-hitting drill** *(S)* — `stanceMode:
    alternate` exists; wrap it in a named drill with orientation-flipped
    clips (already rendered) and a preset chip.

### D. Voice & personality

14. **Themed voice packs** *(L, real money/licensing)* — the #1 "wow" upgrade:
    Rocky or Drago working your corner. Plumbing is multi-pack ready (gap
    #11); cost is ~793 clips × pack and soundalike-rights care. A cheaper
    first step: **themed catchphrase packs** — keep the base coach, add 5–10
    theme-flavoured motivation lines mixed into `TEN_LINES`/`TANK_LINES` when
    a theme is active.
15. **More motivation variety by context** *(M, clips only)* — per-focus
    encouragement ("good body work", "nice slipping"), post-best-round praise
    with camera on, harder tank lines at Relentless pace. Same mechanism as
    Session 4, pure content.
16. **Beep/metronome mode** *(S)* — a voice-free option (bell + beeps only)
    for shared spaces and headphone-less gyms; also a graceful fallback while
    clips download (gap #7).

### E. Camera

17. **Unify Bag Coach history** *(S–M)* — read/migrate `coachfred.cc` into
    the shared record (gap #1) and retire the silo.
18. **In-timer reaction scoring** *(M)* — when the camera is on and the round
    type is Reaction, measure call→movement latency with the existing
    head-sway detector; feed `stats.reaction` from the main app too (gap #12).
19. **Count verification** *(M)* — the interim step from CAMERA_COACH.md's
    backlog that needs no classifier: corner calls 3 punches, flow/pose sees
    2, coach says "finish the combo". Per-combo accuracy lands on the summary.
20. **Punch-type classifier → combo verification** *(L)* — the existing
    long-term track; unchanged, still the right order (classifier, then
    sequence verification, then adaptive calling).

### F. Sharing & integration

21. **Share the summary card** *(M)* — render the post-session card to a
    canvas image and hand it to `navigator.share`. The card is already the
    best screen in the app; let people post it.
22. **Session log export (CSV)** *(S)* — one button next to the `.coach`
    backup for spreadsheet people.
23. **Heart-rate via Web Bluetooth** *(L, Android/desktop Chrome only)* — pair
    a chest strap, show live BPM during rounds, effort per session. Genuinely
    valuable for the HIIT/Tabata crowd, but iOS Safari has no Web Bluetooth —
    would be Android-only and should be framed as such from day one.

### G. Platform hygiene (quick-wins bundle)

24. Reconcile `APP_VERSION` with the SW cache tag — derive one from the other
    (gap #8).
25. Gate `__camSim` behind a `?dev` flag (gap #9).
26. **"Make offline now" button** in More → downloads the active voice pack
    (and optionally the pose runtime) with a progress bar (gap #7).
27. Log per-round detail for custom sessions — store the program shape in the
    history entry (gap #5).
28. `prefers-reduced-motion` + a screen-reader pass on the Setup sheet
    (gap #13).

---

## 3. Suggested sequencing (Sessions 11–14)

| Session | Scope | Why this order |
|---|---|---|
| **11 — Records & milestones** | Ideas 1, 2, 3, 4, 5 + hygiene 24, 25, 27 | Pure aggregation of data the app already collects; fixes the two motivational dead-ends (untotalled stats, program ending); no new assets |
| **12 — Programs II** | Ideas 6, 7, 8 | Turns the one-shot career mode into a system; content-heavy, engine-light |
| **13 — Corner content** | Ideas 9, 10, 12, 13, 15, 16 (one clip batch) | One ElevenLabs render session covers sparring sim + context praise + rest tasks; shadowbox/surprise/switch drills are config-only |
| **14 — Camera unification** | Ideas 17, 18, 19 + hygiene 26 | Closes the two data silos and ships count verification — the last camera step before the classifier track |

Ideas 14 (themed voices), 21–23 (sharing, CSV, heart rate) and 20
(classifier) stay on the shelf until the above land — they're the expensive
or platform-constrained ones, and nothing below depends on them.
