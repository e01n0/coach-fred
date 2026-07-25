# Coach Fred

A boxing round timer for the heavy bag that calls combinations out loud — your corner man between the bells. Single self-contained `index.html`, no build step.

> Named after Coach Fred from Cyberpunk 2077's *Beat on the Brat* boxing questline, who phones in advice while you fight.

## Deploy to Render

### Option A: Dashboard (two clicks)
1. Push this folder to a GitHub/GitLab repo.
2. Render Dashboard -> **New** -> **Static Site**.
3. Pick the repo. Set:
   - **Build Command:** *(leave blank)*
   - **Publish Directory:** `.`
4. **Create Static Site**. Done. You get a `*.onrender.com` URL.

### Option B: Blueprint (uses render.yaml)
1. Push this folder (including `render.yaml`) to a repo.
2. Render Dashboard -> **New** -> **Blueprint** -> pick the repo -> **Apply**.

### Option C: Render CLI
```bash
# one-time
brew install render            # or: npm i -g @render/cli
render login

# from this folder, after pushing to a connected repo
render deploys create <service-id>
```

## Run locally
```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Quick-start workouts
**Setup → Workout → Quick start** loads ring-standard sessions in one tap. The
structures are taken from boxing coaching sources (pro/amateur round formats,
heavy-bag interval work, FightCamp's HIIT/Tabata/EMOM guidance):

- **Beginner** — 3 × 2:00, sparse easy combos
- **Amateur** — 3 × 3:00, Olympic/amateur men's distance
- **Club bag** — 6 × 3:00, the standard heavy-bag session
- **Pro** — 12 × 3:00, championship distance
- **Tabata** — 8 × 20s/10s, **HIIT** — 10 × 40s/20s
- **EMOM** — 10 × 1:00, one combo at the top of each minute
- **Pyramid**, **Burnout**, **Footwork** — drill formats (below)
- **Shadowbox** — 4 × 2:00, no bag needed (below)
- **KB circuit** 4 × 3:00, **KB EMOM** 10 × 1:00, **Swing Tabata** 8 × 20/10 —
  kettlebell strength & conditioning (below)
- **Bag & bell** — 6 × 3:00 alternating bag round / bell round, the classic
  hybrid session, built on Round by round mode

## Round types
**Setup → Workout → Round type** changes what the corner calls during work:

- **Combos** *(default)* — combinations from your ticked pool
- **Pyramid** — climb the punch count 1→6 and back down, a classic bag ladder
- **Burnout** — non-stop 1-2 punch-out; speed and volume over power
- **Footwork** — real called footwork drills (pivots, shuffles, in-and-out,
  circling, L-step, cut-the-angle), which flip left/right on southpaw rounds
- **Shadowbox** — no bag needed: movement-first calling where footwork, feints
  and head movement carry the round, with crisp combos stitched between them
- **Kettlebell** — called strength stations (swings, goblet squats, cleans,
  rows…) on a fixed rotation: a 3:00 round works through five stations, a 1:00
  round takes one, and two-sided moves get a *"switch sides"* call at the
  halfway mark. An illustrated **Kettlebell guide** (with themable line-art
  frames and coaching cues per exercise) appears in Setup whenever a session
  has a bell round — and its cards double as the **exercise pool**: untick
  anything you can't do and the rotation skips it. During rest before a bell
  round, the screen **previews the next station's frames** so you see the
  movement before the bell. Structures are sourced from boxing S&C coaching —
  see [KETTLEBELL.md](KETTLEBELL.md)
- **EMOM** — every minute on the minute: one combo at the top, rest the rest

In **Round by round** mode each round can use a different type.

## Drill a combo
**Setup → Workout → Drill a combo** grooves one combination for the whole
session — the timer sets rounds and rest, the drill sets what gets called:

- **Build up** — starts with the combo's first two pieces and adds one each
  round, layers a slip/roll and counter onto the finished combo near the end,
  then mixes it into normal calling for the last round: can you still fire it
  when it's not the only thing coming?
- **Speed** — the full combo on a beat that tightens every round, down to 3s.
- **Repeat** — the classic steady-beat drill, one rep per call.

**Repeat** and **Speed** can alternate two combos (A/B) so you switch gears
between reps. In **Round by round** mode, a round with the **Drill** type has
its own combo picker.

## Shot focus (custom rounds)
**Setup → Workout → Round by round → Shot focus** leans the corner onto one shot
or one family of movement for that round — "rear uppercut round 1, rolls round
2" — so most of the round's combos pay off with the chosen shot or build around
the chosen movement, instead of calling evenly from the whole pool. Pick from
the punches (jab through rear uppercut, plus body shots) or a movement family
(slips, rolls, steps, pivots, guard, feints). The corner announces it at the
bell ("…rear uppercut focus") and still mixes in enough variety to breathe.
Applies on the **Combos** and **EMOM** formats; the fixed drill formats
(pyramid, burnout, footwork) ignore it.

## How the corner calls
On the default **Combos** format the caller works like a corner man, not a
shuffle:

- **Reactive calling** — calls answer the shot you just threw. A hook draws the
  slip-and-counter, a long burst draws a defensive reset, a jab draws the
  straight behind it.
- **Fatigue shaping** — on rounds long enough to have an arc (45s+), the pace
  eases through the back half, then spikes for the final push, with a spoken
  *"last ten — empty the tank"* in the closing seconds.
- **Defensive-only beats** — pure *slip · roll · reset* calls with no punch, to
  drill head movement. These come up most on the **Defence** focus and with
  **Defence & movement → Heavy**.
- **Feints** — fakes (*feint jab*, *feint cross*, *feint hook*, *feint level
  change*) sit alongside slips, rolls and footwork in the movement library and
  always draw the real shot behind them. Tick them under **Setup → Combos →
  Movement**, dial them in with **Defence & movement**, or make a round a feint round
  with **Shot focus → Feints**.

Movement is gated by the **Defence & movement** dial and your ticked moves — not by a
round's combo focus — so head movement and feints get drilled even on a Power
or Basics round, from the first round on.

## Your record
Coach Fred keeps a tally on your device — rounds, sessions, minutes on the bag,
your current and best day streaks, plus **lifetime totals** that survive the
session-log cap: punches called, your favourite shot, and what the camera has
seen. A **rounds-per-week trend strip** shows the last eight weeks at a glance,
a **Best session** line tracks your personal bests (most rounds, longest
session, most punches called), and **milestones** (first session, 100 rounds,
1,000 punches called, 7-day streak, program graduate…) light up as you earn
them — new ones are celebrated on the session summary card. See it all under
**Setup → More → Your record**; it rides along in your **.coach** backup.

A **4-week program** (Setup → Workout → 4-week program) takes you from first
bag session to club distance, three sessions a week — load the next one and
finishing it ticks it off. A **weekly goal** (rounds per week, under Your
record) tracks alongside the day streak.

When you finish a session a **summary card** sums up the work — rounds, minutes
on the bag, total sessions, your streak, and a breakdown of what the corner
called (~punches, top shot, defensive moves). Every completed session is also kept
in a **Session log** (**Setup → More → Session log**), newest first, so the
streak counter becomes a real training journal. The log lives on your device and
travels in the **.coach** backup.

## Sounds
The corner is a **recorded human voice** (pre-rendered with ElevenLabs), not
robotic text-to-speech: every cue is a short audio clip and the app plays them
back-to-back. The coach calls the card like a real corner: **“Round three”**
(**“Final round”** on the last) with your stance to open a round, **“Rest”**
between rounds, a heads-up near the end of rest (*“ten seconds — round four,
southpaw”*), a **3-2-1 count** back in, a breathing cue on longer rests, and a
**“ten seconds”** shout of motivation in the final stretch of a round (the
phrase is picked at random, so it stays fresh). An optional **bell**
(Coaching → Ring the bell) rings under the voice at the start and end of every
round; off keeps the corner voice-only. A **Warm-up round** toggle adds two
easy minutes of footwork and light shots before round one. On longer
rounds the **fatigue shaping** eases the pace through the back half, then digs in
for that last push. The clips are cached for offline use as they play — or grab them all at once
with **Take the coach offline** (Setup → More) before training somewhere with
no signal. **Coach voice** (Setup → More) picks
who works your corner — Coach Fred, or Coach Cal's gravel — and **Voice
speed** sets how fast the corner calls. See
[VOICE_PACKS.md](VOICE_PACKS.md) to regenerate the voice with your own
ElevenLabs voice.

## Install (PWA)
Coach Fred is an installable Progressive Web App. Open it in a browser and use
**Install app** (Chrome/Edge) or **Add to Home Screen** (Safari) for a
fullscreen, native-feeling app. Once loaded it works **offline** — a service
worker caches the app shell. Icons and manifest live alongside `index.html`
(`manifest.webmanifest`, `sw.js`, `icon-*.png`). The icons are generated from
the boxing-glove master `icon-source.png` by `gen_icons.py` (`pip install
Pillow`). A service worker needs HTTPS or `localhost`, both of which Render and
the local server above provide.

## Themes
Reskin the whole app from **Setup → More → Theme** (at the bottom). Twenty looks,
boxers and beyond:

- **Boxing:** Coach Fred (default), Rocky Balboa, Apollo Creed,
  Ivan Drago, Little Mac, Iron Mike, Marvin Hagler, George Foreman,
  Muhammad Ali, Manny Pacquiao, Ippo Makunouchi, King Hippo
- **Games & screen:** Cyberpunk 2077, Ryu, Scorpion, Sub-Zero, Goku,
  Vegeta, Bruce Lee, Kenshiro

Each theme uses its fighter's authentic colours: Rocky's black &amp; gold,
Apollo's Old Glory red/white/blue, Pacquiao's Philippine-flag blue/red/yellow,
Drago's Soviet red, Ali's white-with-black-trim, Goku's orange gi, Scorpion's
`#E3C519` yellow, Vegeta's Saiyan blue and Cyberpunk 2077's neon yellow-on-cyan.

The choice is saved on your device.

## Notes
- iOS only speaks after you tap Start. The coach plays through the mute
  switch by default (Setup → More → Play on silent); turning that off makes it
  duck under your music instead, but then the mute switch must be off.
- "Add to Home Screen" in Safari for fullscreen app behaviour.
- Offline support and install require the page to be served over HTTPS or
  `localhost` (not opened as a `file://` URL).
