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
