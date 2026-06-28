#!/usr/bin/env python3
"""Pre-render Coach Fred's voice with ElevenLabs into a playable voice pack.

Coach Fred is voice-only and uses no browser text-to-speech: every cue is a
recorded clip. This script renders each spoken atom listed in voice/phrases.json
to an MP3 with ElevenLabs, so the app plays a genuinely human corner man. The
app loads a pack from voice/<pack>/; the spoken vocabulary is fixed and fully
recorded, so render the whole thing.

Nothing here stores a key: you bring your own ElevenLabs API key and voice, run
this once, then commit the voice/<pack>/ folder so it deploys with the static
site.

Usage
-----
    export ELEVENLABS_API_KEY=sk_...
    # render the full vocabulary (~103 clips), overwriting the shipped pack:
    python3 gen_voice.py --voice-id <ELEVENLABS_VOICE_ID> --pack fred --force

The pack id must match an entry in VOICE_PACKS in index.html (default: "fred").
Without --force, already-rendered clips are skipped so re-running resumes
cheaply. Styles (--styles): combo (punches/movements), cue (bell calls), line
(motivation), test. Pick a punchy, energetic voice — it's a boxing corner.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

API = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
ROOT = os.path.dirname(os.path.abspath(__file__))


def render(text, voice_id, model, key, stability, similarity, style_exag):
    body = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style_exag,
            "use_speaker_boost": True,
        },
    }).encode("utf-8")
    req = urllib.request.Request(
        API.format(vid=voice_id), data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser(description="Render a Coach Fred ElevenLabs voice pack.")
    ap.add_argument("--voice-id", required=True, help="ElevenLabs voice id")
    ap.add_argument("--pack", default="fred", help="output id under voice/ (match VOICE_PACKS in index.html)")
    ap.add_argument("--styles", default="combo,cue,line,test",
                    help="comma list to render: combo,cue,line,test")
    ap.add_argument("--model", default="eleven_multilingual_v2", help="ElevenLabs model id")
    ap.add_argument("--stability", type=float, default=0.45)
    ap.add_argument("--similarity", type=float, default=0.8)
    ap.add_argument("--style", type=float, default=0.0, help="style exaggeration 0..1")
    ap.add_argument("--force", action="store_true", help="re-render clips that already exist")
    ap.add_argument("--sleep", type=float, default=0.3, help="pause between calls (seconds)")
    args = ap.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY in your environment first.")

    with open(os.path.join(ROOT, "voice", "phrases.json"), encoding="utf-8") as f:
        phrases = json.load(f)

    want = {s.strip() for s in args.styles.split(",") if s.strip()}
    todo = [p for p in phrases if p["style"] in want]
    outdir = os.path.join(ROOT, "voice", args.pack)
    os.makedirs(outdir, exist_ok=True)

    print(f"{len(todo)} clips in styles {sorted(want)} -> voice/{args.pack}/")
    made = skipped = failed = 0
    for i, p in enumerate(todo, 1):
        dest = os.path.join(outdir, p["slug"] + ".mp3")
        if os.path.exists(dest) and not args.force:
            skipped += 1
            continue
        for attempt in range(4):
            try:
                audio = render(p["text"], args.voice_id, args.model, key,
                               args.stability, args.similarity, args.style)
                with open(dest, "wb") as out:
                    out.write(audio)
                made += 1
                print(f"  [{i}/{len(todo)}] {p['slug']:<28} “{p['text']}”")
                time.sleep(args.sleep)
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")[:200]
                if e.code == 429 and attempt < 3:          # rate limited — back off
                    time.sleep(2 ** attempt)
                    continue
                print(f"  ! {p['slug']}: HTTP {e.code} {msg}", file=sys.stderr)
                failed += 1
                break
            except Exception as e:                          # network blip — retry
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                print(f"  ! {p['slug']}: {e}", file=sys.stderr)
                failed += 1
                break

    # Manifest = every clip actually present in the pack dir, so the app knows
    # exactly what it can play (and what to fall back to TTS for).
    slugs = sorted(f[:-4] for f in os.listdir(outdir) if f.endswith(".mp3"))
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"voice": args.voice_id, "model": args.model, "slugs": slugs}, f, indent=2)
        f.write("\n")

    print(f"\nrendered {made}, skipped {skipped}, failed {failed}. "
          f"manifest lists {len(slugs)} clips.")
    print(f"Now pick “Coach Fred — recorded” under Setup → Settings → Coach voice, "
          f"and commit voice/{args.pack}/ to deploy it.")


if __name__ == "__main__":
    main()
