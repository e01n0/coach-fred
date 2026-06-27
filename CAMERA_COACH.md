# Camera Coach — design notes & build backlog

Experimental visual coaching for Coach Fred: the phone camera watches you on the
bag and checks your guard, head movement, balance, punch type, and whether you
**landed** the shot — all **on-device**, no video ever leaves the phone.

Split across **two standalone pages** because the two drills need the phone in
**different places**, and mixing them in one screen confused people:

- **`camera-coach.html`** — **Bag Coach**, phone **side-on (~90°)**: Watch + Form
  check (guard, balance, punch type, contact).
- **`reaction-drill.html`** — **Reaction**, phone **front-on**: the SLIP L/R
  reaction drill.

Both are launched from the main app under **Setup → More → Experimental** and
share the same self-hosted pose runtime under `./vendor`. Kept separate from the
core on purpose: they pull a ~5 MB pose model over the network and would bloat
the offline single-file core.

> **Status legend:** ✅ working now · 🧪 placeholder/heuristic · 🔨 needs building · 🎓 needs a trained model

---

## What runs today (no training required)

| Capability | How | Status |
|---|---|---|
| Body pose (33 keypoints) | MediaPipe Tasks Vision `PoseLandmarker` (lite, GPU) | ✅ |
| Guard check (hands up?) | non-punching wrist height vs head/shoulder line | ✅ |
| Head-sway / slip detection | nose offset vs shoulder centre, calibrated neutral | ✅ |
| Reaction drill (scored) | random SLIP L/R prompt, reaction-time scoring | ✅ |
| Balance check | hip centre-of-mass over the ankle base | ✅ |
| Overreach check | arm-extension ratio (wrist↔shoulder span / shoulder width) | ✅ |
| Head-over-knee check | nose vs lead-knee on the image x-axis, normalised by torso length — flags `HEAD PAST KNEE` when the head lunges forward past the front knee | ✅ side-on, pure 2D (no depth) |
| Punch *thrown* detection | extension hysteresis (reach + elbow straightening), **gated to a ~90° side view** | ✅ |
| **Contact — "did you land it"** | **optical-flow motion spike in a marked bag ROI** | ✅ gym-proof, no audio |
| Punch *type* label (jab/cross/hook/uppercut) | geometry heuristic over wrist trajectory | 🧪 placeholder |

Mic fusion for contact was **rejected**: a real gym has 20 other bags, music and
noise — you can never isolate your own bag's thud. Contact is detected
**visually** from the bag's motion instead (the bag is large and slow vs the
glove, so it stays trackable even when fast hands motion-blur).

---

## Build backlog — the stuff we must not lose

### 1. 🎓 Punch-type classifier (replace the heuristic)
Replace `classifyPunch()` in `camera-coach.html` with a small temporal model over
the keypoint window. The function is already isolated as the integration seam.

- **Input:** sliding window of ~8–12 frames × 33 keypoints (x,y,z), body-centred &
  scale-normalised (translate to mid-hip, scale by shoulder width) so it's
  viewpoint-robust.
- **Output classes (match Coach Fred's existing six shots exactly):**
  `Jab · Cross · Lead Hook · Rear Hook · Lead Uppercut · Rear Uppercut`
  (+ optional `Body` variants, + a `none` class for non-punch frames).
- **Model:** 1D-CNN / small temporal transformer on keypoints. Tiny (input is
  ~1k floats/frame, not pixels) → sub-millisecond inference, effectively free on
  top of pose. Export to **TF.js** or **ONNX Runtime Web**; lazy-load like the
  pose model.

**Training data (see datasets below).** Pretrain on BoxingVI, then **fine-tune on
a few hundred self-recorded heavy-bag clips** to close the domain gap (BoxingVI is
sparring/air-boxing from YouTube, not a fixed phone at a heavy bag). Because the
model eats *keypoints*, not pixels, the gap is far smaller than for a pixel model.

### 2. 🔨 Auto bag detection (replace tap-to-mark ROI)
Today the user taps to mark the bag ROI. Optional upgrade: a small object
detector to auto-find the bag (and reject neighbouring bags) using the Roboflow
sets below. Only worth it if tap-to-mark proves annoying in testing. Runs via
ONNX Runtime Web / TF.js — but mind the **one-heavy-model ceiling** (see Perf).

### 3. 🔨 Depth for true reach/forward-balance (optional, later)
A front camera sees lateral/vertical well but **forward lunge is depth (z)** and
monocular z is noisy. The cheaper, already-shipped answer is the **side-on view**:
with the phone at ~90° the forward axis becomes the image **x**, so forward lunge
is read in 2D with no depth model — that's exactly what the **head-over-knee**
check (`HEAD PAST KNEE` in `evaluatePunch()`) does, flagging the head drifting
past the lead knee. A monocular depth model (Depth Anything / MiDaS via
Transformers.js or ONNX Web) would only be worth it for a **front-on** reach/balance
drill, and it's **heavy (~5–15 fps)** — toggle on per-drill only, never alongside
another heavy net.

### 4. 🔨 Combo verification in the caller
Once punch-type recognition lands, close the loop with the existing combo caller:
the corner calls "jab–cross–hook", the classifier confirms the *sequence* you
actually threw (not just a count), and Coach Fred reacts ("you dropped the hook").
Feeds the planned **session history / summary card** with per-combo accuracy.

---

## Datasets (verified June 2026)

**Punch-type / action recognition (pose-based):**
- **BoxingVI** — arXiv:2511.16524 — *the one to use.* 6,915 labelled punch clips,
  the exact six classes above, **per-frame 2D pose included**, 18 athletes from 20
  YouTube sessions. PoseConv3D baseline ~87.3% on the six types.
- **BoxMAC** — arXiv:2412.18204 — multi-label boxing actions, same six punches.
- Pretrain/augment: **UCF101** (`BoxingPunchingBag`, `BoxingSpeedBag`),
  **Kinetics** (`punching bag`, `shadow boxing`), **NTU RGB+D** (skeleton `punch`).

**Bag / glove object detection (Roboflow Universe):**
- Detecting Punches in Boxing — Bag / Cross / Jab / No-Punch
- Combat Sports — `boxing-bag`, `glove-left`, `glove-right` + punch types
- Boxing Gloves Detection (1,563 imgs) · Punching bag (200 imgs)

> **License caveat:** YouTube-derived clips and Roboflow community sets vary —
> check terms before any commercial use. Sizes are modest (hundreds–~7k); fine
> for a *pose-based* classifier precisely because its input is low-dimensional.

---

## Performance — "will it work on video at speed?"

- **Compute: yes.** Pose-lite ~30 fps on a modern phone; the punch classifier runs
  on keypoints (tiny) → effectively free; bag optical-flow on a small ROI is cheap.
- **Real risk is temporal resolution, not FLOPS.** A jab is ~100–150 ms = 3–5
  frames @30 fps, and the glove blurs at peak extension. Mitigations, all in the
  prototype or planned:
  - **Capture at 60 fps** (`getUserMedia frameRate:{ideal:60}`) where available.
  - **Classify the whole trajectory window**, not one peak frame.
  - **Time contact off the bag, not the glove** — the bag stays sharp at 30 fps.
- **One-heavy-model ceiling:** pose + bag-flow + keypoint classifier all fit one
  frame budget. Adding depth or an object detector means dropping something else.

---

## Camera placement decides what you can coach

- **Phone facing you** (where it sits for the timer): great for **guard** and
  **head slips**; lateral balance OK; forward lunge is hardest (depth).
- **Phone to your side (90°):** great for **reach / overextension / forward
  balance / punch extension**; weaker on guard.

**This split is now baked into the UI:** the two placements are **separate
pages**, so the user never has to discover mid-session that a mode wants a
different camera angle. Bag Coach (`camera-coach.html`) is side-on only — punch
detection only counts when a ~90° side view is detected (shoulder span small vs
torso height), with an on-screen SIDE-ON / TURN SIDE-ON badge. Reaction
(`reaction-drill.html`) is front-on only. Detection itself is a retract→extend
hysteresis (not a single-frame delta) with joint-visibility gating, so a still
guard no longer phantom-fires punches.

---

## Code seams (in `camera-coach.html`)

- `classifyPunch(hand)` — 🧪 heuristic; **swap for the trained model**.
- `analyzeBag()` / `markBag()` — bag optical-flow contact; swap `markBag` for an
  auto-detector if desired.
- `evaluatePunch()` — combines guard/reach/balance + contact + type into a verdict;
  where combo-caller verification will hook in.
- Model + runtime are **self-hosted** under `./vendor` (MediaPipe tasks-vision
  **0.10.35** + `pose_landmarker_lite.task`, ~17 MB total) so the coach runs
  **fully offline after the first load** — the service worker runtime-caches them
  on first use (not precached on install, to avoid burdening non-camera users).
  Only the SIMD wasm variant is vendored; pre-2017 no-SIMD devices would need the
  `nosimd` files added.

## iOS / permissions
HTTPS required. Installed (home-screen) PWAs have historically been flaky with
`getUserMedia` on some iOS versions — the prototype degrades gracefully with a
clear message. **Test on a real device** before promoting out of Experimental.

## If we ever want it fully inline
Today it's a launched same-origin page. To embed inside `index.html` instead:
lazy-`import()` the MediaPipe module only when the panel opens (don't load it on
app start), self-host the model, and namespace its state so it can't touch the
timer's. Recommended only after the feature graduates from Experimental.
