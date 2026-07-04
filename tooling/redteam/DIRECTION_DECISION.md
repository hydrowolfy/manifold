# Red-team direction decision: the most promising route to a frame-free discrete 3-geometry

Charge: aim at whatever is most promising. Three Fable specialists (RG/EFT physicist,
flag-complex topologist, Lakatosian analyst) each named a direction; one empirical pre-test
decided the fork. Citations are the specialists' (verified via search); re-verify before formal use.

## The convergent picture
1. **Flag complexes are the correct SUBSTRATE — for frame-freeness, not for geometry.** They are
   the unique regime where graph -> manifold is well-posed (prior E5 consult), AND there is a
   theorem-grade *frame-free growth move*: Lutz-Nevo stellar theory for flag complexes (edge
   subdivision + inverse, all intermediates flag; purely graph-level) [arXiv:1302.5197]. Every
   3-manifold has flag triangulations (barycentric subdivision is flag).
2. **Flag-ness alone does NOT decrumple — proven and now measured.** Adamaszek-Hladky: the
   face-maximal flag 3-spheres are joins of two cycles C_a * C_b with diameter 2, i.e. maximally
   crumpled [arXiv:1205.4060]. **Pre-test (this repo):** barycentrically subdividing our certified
   crumpled 3-manifolds (making them flag) left them crumpled - d_s overshot to ~4.0-4.3 and
   d_H stayed ~1.2-1.5, nowhere near 3. Confirmed: flag = substrate, not geometry.
3. **The one open, frame-free lever is FLAG-NO-SQUARE (fns).** It is the *maximal* local condition
   the Januszkiewicz-Swiatkowski no-go permits (no 6-large triangulation of S^2, so no systolic
   3-manifold) [Publ. IHES 104 (2006)]; it exists for every closed 3-manifold (Przytycki-
   Swiatkowski, flag-no-square subdivisions) [GGD 3 (2009)]; and it *kills the Adamaszek-Hladky
   crumpled extremal family* (C_a*C_b is full of empty squares). Whether a random fns 3-manifold
   is extended, crumpled, or branched-polymer is **genuinely open - no literature exists.**
4. **The physics fallback is locally-causal CDT, and the frame-free objection to it is already
   answered.** Jordan-Loll showed the global proper-time foliation is inessential: a purely LOCAL
   causality condition (edge timelike/spacelike labels) still yields the extended de Sitter phase
   in 2+1D [arXiv:1305.4582; PRD 88 044055]. The 3D CDT geometric phase (d_s -> 3) is an *extended
   region*, not a tuned point [Ambjorn-Jurkiewicz-Loll PRD 64 044011; Benedetti-Henson arXiv:0911.0401].
   Crumpling is entropic (baby-universe branching); causality forbids the branching.

## Decision (the most promising direction)
**Build the FLAG-NO-SQUARE 3-manifold Monte Carlo.** It is the only route that (a) is genuinely
open/novel - a positive result is new to the literature, not imported; (b) is cleanly frame-free
- the manifold lives in the graph's own clique complex, no foliation, no tuned lattice, satisfying
the STRONG "zero coordinates" hard core; (c) is cheap - Lutz-Nevo moves + square rejection slot
into the existing graph-only certification; (d) has content on BOTH outcomes (Lakatos): a PASS is a
progressive novel result, a FAIL is the clean diagnostic that intrinsic frame-free growth cannot
decrumple 3-geometry - which is exactly what then justifies the CDT fallback, honestly.

## Pre-registered experiment (lock before production runs)
Three arms on identical instrumentation (the existing d_s/d_H estimators + link census):
- **A (null):** existing Euclidean Pachner DT (the current scheduled run supplies this baseline).
- **B (flag):** Lutz-Nevo flag Pachner MC. Prior: crumples like A (pre-test supports this).
- **C (flag-no-square):** Lutz-Nevo moves with empty-square rejection. **The whole ballgame.**
Sizes N ~ 10^3-10^4, >=10 seeds, blinded, tuning/verdict partition enforced.
- **PASS (progressive):** a fugacity window in C where d_s and d_H drift JOINTLY toward 3 with the
  gap |d-3| shrinking monotonically over >=1 decade in N, PLUS one pre-stated novel observable
  (a curvature-fluctuation or volume-profile exponent named before the run) confirmed.
- **FAIL:** C crumples (d_s overshoot, d_H low) or locks at branched-polymer (d_s~4/3, d_H~2).
  Consequence: intrinsic frame-free growth cannot decrumple 3D; proceed to locally-causal CDT
  (Jordan-Loll) with a mandatory foliation-gauge-invariance test as ITS novel prediction.

## Open flanks flagged by the panel (do not paper over)
- fns-preserving move ergodicity / fixed-N mixing is unproven (Lutz-Nevo is proven for flag, not
  fns); the honest workaround is flag moves + square rejection, whose chain connectivity is open.
- For the CDT fallback: whether the locally-causal extended window survives N -> inf (vs shrinking
  to zero, meaning the global foliation was doing the work) is the honest open question.

## Next build (staged)
Implement the Lutz-Nevo flag edge-subdivision move + inverse at graph level; grow a certified flag
3-manifold; add empty-square rejection for the fns arm; wire the existing link census (must stay
all-2-sphere) and d_s/d_H estimators; run arms B and C. Arm C is the decisive novel experiment.

## Build status (arm B done; arm C obstacle characterized)

`tooling/flag3_manifold.py` — frame-free FLAG 3-manifold generator (Lutz-Nevo edge subdivision,
graph-only). Certified: the 16-cell seed and all grown configs pass the flag-2-sphere vertex-link
census (K4-free neighborhood + clique complex a 2-sphere). This is a genuine milestone: a
frame-free construction that produces CERTIFIED 3-manifolds via a theorem-grade move, with the
manifold living in the graph itself.

- **Arm B (plain flag), result:** certified flag 3-manifolds at N=40/80 CRUMPLE — d_s 2.27/2.47,
  d_H 0.22/0.48, empty-square count 672/1810. Confirms with the REAL Lutz-Nevo move (not merely
  barycentric subdivision) that flag alone does not decrumple. Consistent with Adamaszek-Hladky
  and the earlier pre-test.
- **Arm C (flag-no-square) obstacle, precisely located:** the minimal flag seed (16-cell) already
  has 12 empty squares, and every Lutz-Nevo subdivision INCREASES the square count, so greedy
  square-minimization stalls at the seed (cannot descend monotonically). Reaching a flag-no-square
  3-manifold requires going UPHILL in the square energy first — i.e. a Metropolis-annealed MCMC
  with the INVERSE Lutz-Nevo move (contraction) for fixed-size exploration, and/or a constructed
  fns seed. The existence/reachability of small fns 3-spheres via a square-rejecting chain is
  genuinely open (no published fns analog of Lutz-Nevo). This is the next careful build — the
  "whole ballgame" — and the one place to go slow to avoid a confident wrong answer.

### Next build (staged, precise)
1. Implement the inverse Lutz-Nevo move (contract a subdivided vertex; recognize by the local
   neighborhood condition), with certification-rejection.
2. Metropolis MCMC over flag 3-spheres with energy = empty-square count; anneal toward 0.
3. If a fns (0-square) 3-manifold is reached at usable N: measure d_s/d_H vs N (arm C = the
   decisive novel experiment); pre-register the pass gate (d_s,d_H -> 3, gap closing) before runs.
4. If fns cannot be reached / stays crumpled: that is the clean negative that licenses the
   locally-causal CDT fallback (Jordan-Loll), honestly.
