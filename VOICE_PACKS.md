# Recorded voice packs (ElevenLabs)

Coach Fred is voice-only, and the corner is a **recorded human voice** —
pre-rendered with ElevenLabs and shipped as static audio. There is **no browser
text-to-speech**: every cue is a short clip. This keeps the app fully offline and
self-contained (it just ships some audio files). No API key is ever stored in the
app; you regenerate the voice by running the script with your own key.

## How it works

The coach only ever says a **finite set of short phrases** — each punch, each
movement, each bell cue and each motivation line. They're listed in
[`voice/phrases.json`](voice/phrases.json) (~103 clips). `gen_voice.py` renders
one MP3 per phrase with ElevenLabs into `voice/<pack>/`, plus a `manifest.json`
of what's present.

At runtime the app plays those clips in sequence: combos play word-by-word
(`jab! · cross! · hook!` — staccato, which suits a boxing corner), and the longer
lines play as whole, natural phrases. The spoken vocabulary is fixed and fully
recorded, so there's no gap to cover — a clip that genuinely fails to load is
simply skipped and the round's timing carries on.

## Regenerate the voice

1. Get an [ElevenLabs](https://elevenlabs.io) API key and pick a voice — choose
   a **punchy, energetic** one; it's a fight corner, not an audiobook. Note its
   **voice id** (Voices page). A paid plan unlocks the full library and voice
   cloning, and clears the free tier's attribution/redistribution terms.

2. Render the full pack (overwriting the shipped one):

   ```bash
   export ELEVENLABS_API_KEY=sk_...
   python3 gen_voice.py --voice-id <VOICE_ID> --pack fred --force
   ```

   Tune delivery with `--stability`, `--similarity`, `--style`. (Drop `--force`
   to only fill in missing clips.)

3. In the app, hit **Test voice** (Setup → Settings) to hear it.

4. **Commit `voice/<pack>/`** so it deploys with the static site:

   ```bash
   git add voice/fred && git commit -m "Add ElevenLabs voice pack"
   ```

## Offline

The service worker caches each clip the first time it plays (stale-while-
revalidate), so after one online run-through the recorded coach works offline
like the rest of the app.

## Adding more packs (e.g. per-fighter voices)

`--pack <id>` writes to `voice/<id>/`. The app currently ships a single recorded
coach and has no voice-picker UI, but the plumbing is multi-pack aware: add an
entry to `VOICE_PACKS` in `index.html` and the app will populate a `#sVoice`
selector if one is present in the markup.

```js
const VOICE_PACKS = [
  { id:"fred",  label:"Coach Fred" },
  { id:"rocky", label:"Rocky" },
];
```

## Costs & licensing

Clips are generated against **your** ElevenLabs account and count toward your
character quota. Make sure your plan's licensing permits redistributing the
rendered audio in a deployed app, and don't commit your API key.
