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

## Round formats
**Setup → Workout → Round format** changes what the corner calls during work:

- **Combos** *(default)* — combinations from your ticked pool
- **Pyramid** — climb the punch count 1→6 and back down, a classic bag ladder
- **Burnout** — non-stop 1-2 punch-out; speed and volume over power
- **Footwork** — real called footwork drills (pivots, shuffles, in-and-out,
  circling, L-step, cut-the-angle), which flip left/right on southpaw rounds
- **EMOM** — every minute on the minute: one combo at the top, rest the rest

In **Custom rounds** each round can use a different format.

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
  **Movement mix → Heavy**.

## Your record
Coach Fred keeps a tally on your device — rounds, sessions, minutes on the bag
and your current day streak. See it under **Setup → Settings → Your record**; it
rides along in your **.coach** backup.

## Sounds
Coach Fred is **voice-only** — no bell, no clapper. The coach speaks every cue:
**“Round start”** (with your stance) to open a round, **“Rest”** between rounds,
and a **“ten seconds”** call with a shout of motivation in the final stretch. Turn
the ten-second call off under **Setup → More**.

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
- iOS only speaks after you tap Start, and the silent switch must be off.
- "Add to Home Screen" in Safari for fullscreen app behaviour.
- Offline support and install require the page to be served over HTTPS or
  `localhost` (not opened as a `file://` URL).
