# Recorded voice packs (ElevenLabs)

Coach Fred is voice-only. Out of the box every cue is spoken by the browser's
built-in text-to-speech, which on many devices sounds robotic. A **voice pack**
replaces that with **pre-rendered ElevenLabs audio** — a genuinely human corner
man — while keeping the app fully offline and self-contained (it just ships some
extra audio files). No API key is ever stored in the app, and nothing changes
until you generate and commit a pack.

## How it works

The coach only ever says a **finite set of short phrases** — each punch, each
movement, each bell cue and each motivation line. They're listed in
[`voice/phrases.json`](voice/phrases.json) (~103 clips). `gen_voice.py` renders
one MP3 per phrase with ElevenLabs into `voice/<pack>/`, plus a `manifest.json`
of what's present.

At runtime, when you choose a recorded voice in the app, it plays those clips in
sequence: combos play word-by-word (`jab! · cross! · hook!` — staccato, which
suits a boxing corner), and the longer lines play as whole, natural phrases.
**Any clip that's missing falls the whole phrase back to TTS**, so a partial
pack works fine and the voice stays consistent within a phrase.

## Generate a pack

1. Get an [ElevenLabs](https://elevenlabs.io) API key and pick a voice — choose
   a **punchy, energetic** one; it's a fight corner, not an audiobook. Note its
   **voice id**.

2. Render the clips:

   ```bash
   export ELEVENLABS_API_KEY=sk_...

   # Recommended first pass — the spoken lines where robotic TTS grates most
   # (round intros, "rest", "ten seconds" + all the motivation lines). ~51 clips.
   python3 gen_voice.py --voice-id <VOICE_ID> --styles cue,line,test

   # Or the full vocabulary, including every combo word (~103 clips):
   python3 gen_voice.py --voice-id <VOICE_ID>
   ```

   Already-rendered clips are skipped, so re-running is cheap; `--force`
   re-renders. Tune delivery with `--stability`, `--similarity`, `--style`.

3. In the app: **Setup → Settings → Coach voice → “★ Coach Fred — recorded
   (ElevenLabs)”**, then **Test voice**.

4. **Commit `voice/<pack>/`** so it deploys with the static site:

   ```bash
   git add voice/fred && git commit -m "Add ElevenLabs voice pack"
   ```

## Offline

The service worker caches each clip the first time it plays (stale-while-
revalidate), so after one online run-through the recorded coach works offline
like the rest of the app.

## Adding more packs (e.g. per-fighter voices)

`--pack <id>` writes to `voice/<id>/`. To expose a new pack in the picker, add an
entry to `VOICE_PACKS` in `index.html`:

```js
const VOICE_PACKS = [
  { id:"fred",  label:"Coach Fred — recorded (ElevenLabs)" },
  { id:"rocky", label:"Rocky — recorded (ElevenLabs)" },
];
```

## Costs & licensing

Clips are generated against **your** ElevenLabs account and count toward your
character quota. Make sure your plan's licensing permits redistributing the
rendered audio in a deployed app, and don't commit your API key.
