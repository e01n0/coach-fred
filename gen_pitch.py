#!/usr/bin/env python3
"""Audit a rendered voice pack's pitch and write voice/<pack>/pitch.json.

ElevenLabs renders short isolated exclamations ("Jab!", "Slip right!")
unpredictably: some takes come back near the voice's true register, others an
octave up in an excited falsetto — a helium coach. The app can't hear that,
so this script measures every clip's median F0 (autocorrelation over voiced
frames) and ships the verdict as pitch.json:

    {"baseline": 128, "threshold": 199, "avoid": ["jab", "7", ...]}

The baseline is the median F0 of the medial "-m" takes — rendered with
sentence context, they reliably land in the voice's real register. Any clip
whose median F0 exceeds baseline * 1.55 (roughly half an octave sharp; where
"emphatic" ends and "helium" begins) is listed in "avoid". At runtime the app
swaps a flagged atom for its "-m" twin and skips flagged whole-combo takes in
favour of stitched atoms. Clips with no alternative (motivation lines) are
still listed but the app plays them regardless — fix those by re-rendering:

    python3 gen_voice.py --voice-id <id> --pack <pack> --force --only <slug,slug,...>

Run after every gen_voice.py session so the table matches the takes:

    pip install numpy imageio-ffmpeg     # once; bundles a static ffmpeg
    python3 gen_pitch.py --pack fred
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 22050
FLAG_RATIO = 1.55


def decode(ff, path):
    import numpy as np
    p = subprocess.run([ff, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32)


def median_f0(x, sr=SR):
    """Median F0 over voiced frames; None when nothing voiced (silence, noise)."""
    import numpy as np
    frame, hop = int(0.040 * sr), int(0.010 * sr)
    lag_lo, lag_hi = int(sr / 400), int(sr / 60)   # 60-400 Hz search band
    f0s = []
    rms_all = np.sqrt(np.mean(x ** 2)) if len(x) else 0
    for start in range(0, len(x) - frame, hop):
        fr = x[start:start + frame].astype(np.float64)
        if np.sqrt(np.mean(fr ** 2)) < max(0.02, 0.5 * rms_all):
            continue                                # silence / breath
        fr = fr - fr.mean()
        ac = np.correlate(fr, fr, "full")[frame - 1:]
        if ac[0] <= 0:
            continue
        ac /= ac[0]
        k = int(np.argmax(ac[lag_lo:lag_hi]))
        if ac[lag_lo + k] < 0.5:
            continue                                # unvoiced frame
        f0s.append(sr / (lag_lo + k))
    return float(np.median(f0s)) if f0s else None


def main():
    ap = argparse.ArgumentParser(description="Write pitch.json for a rendered voice pack.")
    ap.add_argument("--pack", default="fred", help="pack directory under voice/")
    args = ap.parse_args()
    try:
        import numpy  # noqa: F401
        from imageio_ffmpeg import get_ffmpeg_exe
    except ImportError:
        sys.exit("pip install numpy imageio-ffmpeg first (bundles a static ffmpeg).")
    ff = get_ffmpeg_exe()

    d = os.path.join(ROOT, "voice", args.pack)
    f0 = {}
    files = sorted(f for f in os.listdir(d) if f.endswith(".mp3"))
    for i, f in enumerate(files, 1):
        v = median_f0(decode(ff, os.path.join(d, f)))
        if v:
            f0[f[:-4]] = v
        if i % 100 == 0:
            print(f"  measured {i}/{len(files)}")

    mvals = sorted(v for k, v in f0.items() if k.endswith("-m"))
    if not mvals:
        sys.exit("No -m takes found — can't establish the voice's register.")
    baseline = mvals[len(mvals) // 2]
    threshold = baseline * FLAG_RATIO
    avoid = sorted(k for k, v in f0.items() if v > threshold)
    # Sanity gate: on a creaky/gravelly voice the tracker can't follow the
    # irregular glottal pulses and reads fry as high pitch — the "cal" pack
    # measures as 80% falsetto, which is mush, not signal. A real helium
    # problem is a minority of takes; if most clips flag, the measurement is
    # untrustworthy and shipping it would gut the pack. Refuse to write.
    if len(avoid) > 0.25 * len(f0):
        sys.exit(f"{len(avoid)}/{len(f0)} clips flagged — the pitch tracker "
                 f"can't follow this voice (gravel/fry?). Not writing pitch.json.")

    out = {"baseline": round(baseline), "threshold": round(threshold), "avoid": avoid}
    with open(os.path.join(d, "pitch.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"{len(files)} clips, register {baseline:.0f} Hz, "
          f"{len(avoid)} flagged above {threshold:.0f} Hz -> voice/{args.pack}/pitch.json")
    no_alt = [s for s in avoid if not s.startswith("seq-")
              and not s.endswith("-m") and s + "-m" not in f0]
    if no_alt:
        print("No in-register alternative (re-render these to fix):")
        print("  --only " + ",".join(no_alt))


if __name__ == "__main__":
    main()
