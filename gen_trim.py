#!/usr/bin/env python3
"""Cut next-word bleed off the tails of a pack's medial (-m) takes.

The -m takes are rendered with `next_text` sentence context so they carry
mid-sentence prosody — but ElevenLabs sometimes renders a truncated onset of
that next word ("one, two...") at the end of the clip. Stitched into a combo,
every word grows a ghost syllable: "three-w", "slip right-m". This script
detects and removes those tails in place.

Detection per clip (10ms RMS envelope): find the final energy blob and the
quiet gap before it. It is bleed — not part of the word — when it runs to the
end of the file AND either
  * the gap is >= 120ms (no within-word stop closure is that long; the word,
    including any final release burst, is over), or
  * the gap is >= 50ms and the blob is voiced (pitched onset of "one" —
    a word-final stop release like the b in "jab" is an unvoiced burst).
Anything ambiguous is left untouched and reported. Cuts re-encode with the
bundled libmp3lame at 128k with a 12ms fade so the new tail can't click.

Run after rendering, before gen_pitch.py:

    pip install numpy imageio-ffmpeg     # once
    python3 gen_trim.py --pack fred      # add --dry-run to preview
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 22050
WIN_S = 0.010          # envelope window
QUIET_FLOOR = 0.010    # silence threshold floor; scaled per clip in cut_point
GAP_HARD_S = 0.120     # gap this long always ends the word
GAP_SOFT_S = 0.050     # shorter gap: cut only if the tail blob is voiced
TAIL_MAX_S = 0.250     # bleed blobs are short
END_SLACK_S = 0.040    # blob must reach (nearly) the end of the file


def decode(ff, path):
    import numpy as np
    p = subprocess.run([ff, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32)


def blobs_of(env, quiet):
    """Contiguous env>quiet regions as (start, end) window indices."""
    out, i = [], 0
    while i < len(env):
        if env[i] > quiet:
            j = i
            while j < len(env) and env[j] > quiet:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def is_voiced(x):
    """Does the snippet carry a pitch (60-400 Hz autocorrelation peak)?"""
    import numpy as np
    if len(x) < int(0.030 * SR):
        return False
    fr = x.astype(np.float64) - x.mean()
    ac = np.correlate(fr, fr, "full")[len(fr) - 1:]
    if ac[0] <= 0:
        return False
    ac /= ac[0]
    lo, hi = int(SR / 400), min(int(SR / 60), len(ac) - 1)
    return bool(ac[lo:hi].max() > 0.4)


def cut_point(x):
    """Sample index to cut at, or None to leave the clip alone."""
    import numpy as np
    win = int(WIN_S * SR)
    env = np.array([np.sqrt(np.mean(x[i:i + win] ** 2))
                    for i in range(0, len(x) - win, win)])
    # The gap between word and bleed is rarely dead silence — breath and room
    # tone sit around 0.01-0.02 RMS, at a level that varies per clip — so try
    # several silence thresholds; each candidate cut is validated by the same
    # gap+voicing rules, and the earliest validated cut wins (it marks the
    # true end of the word).
    n_win = len(env)
    cands = []
    for quiet in {QUIET_FLOOR, round(0.18 * float(env.max()), 4), 0.02, 0.03}:
        bl = blobs_of(env, quiet)
        if len(bl) < 2:
            continue
        (ps, pe), (ls, le) = bl[-2], bl[-1]
        gap_s = (ls - pe) * WIN_S
        blob_s = (le - ls) * WIN_S
        if (n_win - le) * WIN_S > END_SLACK_S or blob_s > TAIL_MAX_S:
            continue
        if gap_s >= GAP_HARD_S or \
           (gap_s >= GAP_SOFT_S and is_voiced(x[ls * win:le * win])):
            cp = int((pe + max(1, int(gap_s / WIN_S / 2))) * win)
            # A word can mimic the bleed signature ("two" = t-burst, gap,
            # voiced vowel) — but cutting a word removes most of its energy,
            # while cutting real bleed removes a sliver. Guard on that.
            tot = float(np.sum(x.astype(np.float64) ** 2))
            if tot > 0 and float(np.sum(x[cp:].astype(np.float64) ** 2)) / tot <= 0.30:
                cands.append(cp)
    return max(cands) if cands else None


def main():
    ap = argparse.ArgumentParser(description="Trim next-word bleed from -m takes.")
    ap.add_argument("--pack", default="fred")
    ap.add_argument("--dry-run", action="store_true", help="report, don't rewrite")
    args = ap.parse_args()
    try:
        import numpy  # noqa: F401
        from imageio_ffmpeg import get_ffmpeg_exe
    except ImportError:
        sys.exit("pip install numpy imageio-ffmpeg first.")
    ff = get_ffmpeg_exe()

    d = os.path.join(ROOT, "voice", args.pack)
    targets = sorted(f for f in os.listdir(d) if f.endswith("-m.mp3"))
    cut = kept = 0
    for f in targets:
        path = os.path.join(d, f)
        x = decode(ff, path)
        cp = cut_point(x)
        if cp is None:
            kept += 1
            continue
        cut += 1
        print(f"  {f[:-4]:<26} {len(x)/SR*1000:4.0f}ms -> {cp/SR*1000:4.0f}ms")
        if args.dry_run:
            continue
        t = cp / SR
        tmp = path + ".tmp.mp3"
        r = subprocess.run([ff, "-v", "error", "-y", "-i", path,
                            "-t", f"{t:.3f}", "-af", f"afade=t=out:st={t-0.012:.3f}:d=0.012",
                            "-c:a", "libmp3lame", "-b:a", "128k", tmp], capture_output=True)
        if r.returncode != 0:
            print(f"  ! {f}: {r.stderr.decode()[:120]}", file=sys.stderr)
            os.path.exists(tmp) and os.remove(tmp)
            continue
        os.replace(tmp, path)
    print(f"{'would trim' if args.dry_run else 'trimmed'} {cut}, left {kept} of {len(targets)} -m clips")


if __name__ == "__main__":
    main()
