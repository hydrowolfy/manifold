# Preregistration: WPP reconciliation experiment

**Charge.** Run this program's referee suite on actual Wolfram Physics Project rule evolutions.
The WPP claims emergent geometry certified by ball-growth dimension (V_r ~ r^d, log-differences);
this program's 2D/3D refereeing showed that observable false-positives on non-manifold structure
(sponges, crumples). Question: do the WPP's own flagship geometry rules pass manifold-grade
certification, and what does their causal DAG look like against the Kleitman-Rothschild crumple
discriminator?

**Rules under test (exact, from the WPP registry; init {{1,1,1},{1,1,1}} as documented):**
- R1 = wm7714 (flagship "knits a grid", claimed dimension 2):
  {{x,y,y},{z,x,w}} -> {{y,n,y},{y,z,n},{w,n,n}}   (n fresh)
- R2 = wm8619 (claimed sphere-like closed surface):
  {{x,y,y},{x,z,w}} -> {{w,n,n},{n,z,y},{x,y,n}}   (n fresh)
- C1 = tree rule {{x,y}} -> {{x,y},{y,z}} (documented; known non-geometric, exponential growth)
  as the negative calibration control.

**Updating scheme.** Random sequential (pick a uniformly random match, apply). The WPP registry
itself displays "Random evolutions" for these rules as a legitimate ordering; random updating is
the ensemble-like (and harder) test. Event DAG recorded: event -> events that produced its
consumed edges.

**Observables (the referee suite):**
1. d_H from ball growth on the skeleton graph (pairs within each relation), fit window r=2-8.
2. d_s from random-walk return probability (peak of running d_s, sigma<=40).
3. Diameter growth vs N (extended d-dim: ~N^(1/d); crumple: ~log N).
4. p_max (max degree) scaling (singular-vertex condensation guard).
5. LINK CENSUS (the certificate the WPP methodology never runs): fraction of vertices whose
   skeleton-link is a single cycle = closed-2-manifold local certificate (boundary vertices have
   path links; report both).
6. Causal DAG longest-chain height vs event count E (physical d+1 spacetime: height ~ E^(1/(1+d));
   Kleitman-Rothschild generic poset: height ~ 3 layers / ~log).

**Ladder.** N (vertices) checkpoints ~ 1k, 2k, 4k, 8k, 16k; seeds 1-3 per rule (random updating
makes runs distinct; the deterministic tree control needs one run).

**Preregistered predictions:**
- R1: d_H -> 2, d_s -> 2, diameter ~ N^(1/2). Link census: interior fraction high, boundary
  (path-link) fraction nonzero forever (it grows an open triangular patch, not a closed surface).
- R2: if the "sphere" claim is manifold-grade, link-cycle fraction -> 1 with isolated cusp
  failures at most o(1); d_H = d_s = 2; diameter ~ N^(1/2). A persistent O(1) FRACTION of bad
  links = the claim is a picture, not a manifold.
- C1: d_s/d_H diverge (tree), link fraction ~0 - suite must scream non-geometric.
- Headline: the WPP's showcased emergent geometry lives at d=2 and is produced by near-
  deterministic "knitting" rules. Prediction: the certificates pass or fail on the d=2 rules as
  stated above, and NOTHING in the documented registry provides a d=3 analogue - consistent with
  this program's finding that 3D extended geometry is exactly where generic local rewriting
  crumples and a causal scaffold must be paid for.

**Falsifier for our own thesis.** If randomized-updating evolution of a documented WPP rule
produces a growing structure with d_s = d_H = 3 jointly, N^(1/3) diameter growth, and a clean
3-manifold link census - our crumpling claim for frame-free local rewriting is wrong and must be
retracted.

**Committed before any run.** Analysis code: tooling/wpp_reconciliation/wpp_referee.py, with
selftests on a torus grid (must read d~2, links all cycles), a binary tree (must fail), and a
random cubic graph (log diameter) before touching WPP rules.

*(Post-hoc note, recorded honestly: the R1 d->2 prediction as written did not condition on the
updating order; the result falsified it for random updating. See RESULTS.)*
