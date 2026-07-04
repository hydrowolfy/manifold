# Committee verdict: is the discrete-geometry foundation viable, and how to rebuild the hierarchy

Three-member adversarial committee (run on Claude Fable 5): a quantum-gravity Theorist
(constructive/CDT), an adversarial Skeptic (numerology red-team), and a Methodologist
(experiment design). They argued the one question the whole physics hierarchy depends on. This
is the synthesis. Experiments, not this debate, settle it — the committee's job was to produce
the right experiments in the right order, with the anti-fooling guardrails baked in.

## The three positions (best point of each)
- **Theorist:** the certified Pachner 3-manifold is a genuine foundation-in-hand (a topological
  fact from an independent vertex-link-2-sphere test, not a fitted statistic). Crumpling at
  d_s~2.58 is the *known* Euclidean-DT wall; the published fix is causal slicing (CDT), which in
  3D recovers an extended phase with d_s flowing toward 3. Grounds it in Ambjorn-Jurkiewicz-Loll
  (CDT), Benedetti-Henson (spectral dimension in 3D CDT), Bombelli-Lee-Meyer-Sorkin and Surya
  (causal sets). *Concession he insists be made loudly:* CDT needs tuning to a critical region,
  so success means "the substrate supports a CDT-class geometric phase," NOT "d=3 is inevitable."
- **Skeptic:** the foundation FAILED its own bar. 2D defects rise with N (wrong sign — a
  structural obstruction, not finite-size noise); the motivating ablation was circular, which
  contaminates the program's whole evidence base; and deriving sec02-13 on top of an uncertified
  substrate is the classic fitting-power-not-explanatory-power failure. His sharpest live point:
  CDT's fix is a *global foliation* — a preferred slicing — in direct tension with the founding
  "zero coordinates / frame-free" thesis. If the foundation only works by adding the very
  structure the program exists to eliminate, the thesis is falsified even if the geometry is saved.
- **Methodologist:** turn the dispute into pre-registered GO/NO-GO experiments with a tuning-set
  vs verdict-set partition, blinded seeds, a fixed N-ladder, a mandatory null panel, and a
  one-revision stopping rule — so no failure can be rescued by a finite-size excuse or a
  post-hoc metric.

## Consensus (all three agree)
1. **Quarantine the hierarchy.** Nothing above the manifold layer (sec02-13: mechanics, EM, SR,
   QM, GR, QFT, cosmology) is supported until the foundation passes; relabel those layers
   conjectural, in writing, in the repo. Geodesics need a stable geometric phase to even be defined.
2. **The causal-slicing experiment is the last live test.** The cubic route is a certified sponge
   and the 2D route is dead, so causal-sliced dynamics on the certified Pachner 3-manifold is the
   only remaining path to a discrete 3-geometry.
3. **Pre-register, then execute**, with holdout separation enforced by a code-path audit (no
   quantity in the generator's objective or acceptance gate may appear in validation), blinded
   seeds, the full null panel, and an immutable record at tagged commits.
4. **The frame-free claim must be explicitly audited, not assumed** — the deepest live tension.

## The one live disagreement, and how it gets decided
Does causal foliation preserve "frame-free"? Theorist: a causal *order* is extra structure, not
a coordinate frame, and the project's own minor-universality theorem (3D cubic lattices are
minor-universal) *forces* dimension selection to come from the measure/dynamics rather than any
graph rule — so causal weighting is the only option, not a cheat. Skeptic: that may be precisely
the thesis being falsified. **Resolution (Methodologist's E5): decide it empirically** — try to
reconstruct the 2-cells/manifold from the *unlabeled 1-skeleton alone*. If the manifold survives
without the layer labels, the geometry is in the graph and "frame-free" stands; if it only exists
in the bookkeeping labels, the "frame-free substrate" claim is withdrawn even though the geometry
result may stand.

## Pre-registered protocol (execute in order; E4 is the cleanest falsifier)
- **E1 — Blind pipeline calibration (prerequisite).** Estimators (two d_s, two d_H) + link census
  must recover the class of blinded labeled controls (Freudenthal manifolds, grids, rewires,
  random-regular, known-crumpled) within bootstrap CIs at every N; nulls must NOT classify as
  manifolds. Fail => freeze until estimators fixed.
- **E2 — Register the 2D FAIL.** Enters the 2D route as a dead result (blocks goalpost-moving);
  resurrection needs a new pre-registration + the full battery with a negative defect-scaling
  exponent whose 95% CI excludes zero.
- **E3 — Causal coupling scan (small N).** Causal-sliced Pachner chain on the certified manifold
  over a registered coupling grid; must exhibit a window where the d_s plateau and d_H both land
  in the matched-control envelope at the same N, AND separate (non-overlapping CIs) from BOTH the
  causal-off (Euclidean) twin and the degree-preserving rewire.
- **E4 — Finite-size scaling (the verdict).** In that window, the d_s/d_H gap to matched controls
  must be non-increasing in N across >=4 sizes with the trend's 95% CI excluding "flat or
  growing," largest-N inside the control envelope, plus one never-tuned holdout observable
  agreeing. FAIL here = crumpling is intrinsic, foundation falsified with no rhetorical exit.
- **E5 — Frame-freeness audit** (only after E4 passes): reconstruct from the unlabeled 1-skeleton;
  decides the "frame-free" headline per the disagreement above.

> **E5 CORRECTED by red-team consult (redteam/CONSULT_E5_frame_freeness.md):** the 1-skeleton
> does NOT determine a 3-manifold (Dancis threshold is the 2-skeleton; K_9 alone carries 1297
> triangulations in two homeomorphism types). Replace with (A) vertex-link census on the unlabeled
> **2-skeleton** + (B) a **gauge-invariance test**: the move rule must descend to the
> isomorphism quotient and all observables factor through the forgetful map. Graph-only
> certification is valid only for flag complexes. Frame-freeness is a property of the DYNAMICS,
> not of a single configuration.

## Decision
Freeze the hierarchy above the manifold now. The foundation question reduces to a clean, pre-
registered go/no-go centered on E4. The current scheduled run (Euclidean DT at larger scale) is
useful precisely as the E3 causal-OFF null baseline. The causal-slicing construction itself (E3)
is the next human-green-lit build — the Theorist and Skeptic both flagged that a cold agent
writing new causal-dynamics code unsupervised is exactly where a confident wrong answer creeps in.

*Citations above came from the Theorist agent and are well-known works, but verify each before any
formal write-up. No numbers here are new measurements; they reference results established earlier
this cycle.*
