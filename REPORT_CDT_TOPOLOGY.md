# STAGE 1 (surgical): break the sphere assumption -- causal CDT on T^2 x S^1

First stage of the topology frontier. Preregistered in PREREG_CDT_TOPOLOGY.md (committed BEFORE any
torus study state). Runner: cdt_torus_run.py (cdt_causal_run.py core VERBATIM + torus seed + chi=0
census). The S^2 x S^1 program (REPORT_CDT_HUB.md) closed the joint (d_H AND d_s) 3-manifold by the
per-slice Euler identity F = 2V - 4. STAGE 1 asked: does making each slice a 2-TORUS (chi=0), which
dissolves F=2V-4, open the joint pass -- or does an analogous obstruction reappear?

## Verdict

**The wall reappears at chi=0. Breaking F = 2V - 4 does NOT open the joint (d_H AND d_s) 3-manifold.
The obstruction is DEEPER than the sphere assumption -- it has a topology-independent algebraic root
and an entropic (diffusion-geometry) root, and neither depends on the slice being a sphere.**

Two independent results, one analytical (load-bearing, exact at every V,T) and one empirical:

### 1. The locking identity's DIFFERENTIAL is topology-independent (the escape move stays impossible)

For a closed orientable slice of genus g, chi = 2 - 2g and (closed surface, 2E=3F) F = 2V - 2 chi.
The foliation counting is unchanged (one (3,1) per lower-slice spatial triangle, one (1,3) per
upper-slice spatial triangle), so over the T periodic slabs:

    N31 = N13 = 2 N0 - 2 chi T ,    N22 = N3 - 4 N0 + 4 chi T ,    f22 = 1 - 4 (N0 - chi T) / N3 .

Sphere (chi=2): N22 = N3 - 4 N0 + 8 T (campaign 7). **Torus (chi=0): N22 = N3 - 4 N0.** The +8T offset
generalizes to +4 chi T and vanishes. BUT differentiate at fixed (N3, T): dN22 = -4 dN0 + 4 T dchi, and
chi is a topological invariant of the fixed slice topology, so dchi = 0 under every foliation-preserving
move. Hence **dN22 = -4 dN0 for EVERY genus** -- the differential lock is topology-INDEPENDENT. Changing
the slice topology moves only the CONSTANT term; it does not dissolve the lock. So "add spatial vertices
without removing (2,2) tets" is STILL combinatorially impossible on the torus, and the single-locked-DOF
structure (N0 and f22 are one degree of freedom) that roots the campaign 5-7 wall survives intact.
Verified EXACT to the integer on seed / grown / thermalized torus states, and every move preserves it
(dN22 = dN3 - 4 dN0 checked for 2-3/3-2/2-6/6-2/4-4 in --selftest). Corollary: the move weights are
UNCHANGED (2-3:+1, 3-2:-1, else 0), so the entire Metropolis core / detailed balance is reused verbatim.

This is the load-bearing result: it is exact and topological, holds at every V and T, and shows the
"different spatial topology" escape named in REPORT_CDT_HUB.md does not work for the reason hoped (it
was expected to dissolve the identity; instead it only relocates the constant).

### 2. The causal ensemble still forms hubs and fails the joint gate (empirical)

Construction validated (--selftest, all passed): T^2 x S^1 with foliation-preserving typed tets, five
Pachner moves, link census bad=0 = disk everywhere, slices verified ORIENTABLE chi=0 tori (not Klein
bottles), the identity above exact, and detailed balance via exact move round-trips -- all as the S^2
runner, re-verified for the torus. An EXACT flat T^2 x S^1 calibrant (identical flat slices stacked by
prisms) is census-clean with uniform degree 14 (sd 0) and reproduces the Kuhn T^3 benchmark:
d_s(8-24)=3.10+-0.21, d_H(2-6)=2.43 vs Kuhn 3.13+-0.18 / 2.47. So the flat joint 3-manifold EXISTS in
this ensemble -- it is literally the benchmark's own geometry -- and the estimators see it correctly.

But the causal measure does not select it. Primary config V=6000, T=12, k0=2, k22=0 (matched to the
campaign-7 sphere baseline), thermalized to a stable plateau (f22, CV, both dims flat over sweeps
262->1700), seed-averaged (6-8 estimator seeds):

Benchmark (matched flat T^3, N0~1000): **d_H(2-6) = 2.47 , d_s(8-24) = 3.13 +- 0.18.**

| config              | f22   | d_s(8-24)     | d_s(16-48)    | d_H(2-6)      | dH ratio | CV    | deg mean/sd/max | G1 | G2 dH>=.90 | G3 |ds-b|<=.20 | G4 no-cond | joint |
|---------------------|-------|---------------|---------------|---------------|----------|-------|-----------------|----|------------|----------------|-----------|-------|
| flat calibrant (ref)| 0.333 | 3.10 +- 0.21  | 2.86 +- 0.35  | 2.43 +- 0.00  | 0.98     | ~0.00 | 14.0 / 0.0 / 14 | P  | PASS       | PASS           | PASS      | exists* |
| **k22=0 (equilib.)**| 0.404 | 3.48 +- 0.31  | 2.31 +- 0.61  | 1.68 +- 0.04  | **0.68** | 0.10  | 15.4 / 11.0 /79 | P  | **FAIL**   | **FAIL(+0.35)**| PASS      | **NO**  |
| k22=1.0 (lever)     | 0.180 | 3.27 +- 0.23  | 2.49 +- 0.38  | 1.93 +- 0.11  | 0.78     | 0.22^ | 11.8 /11.8 /118 | P  | FAIL       | PASS(+0.14)    | FAIL^cond | NO    |

*the flat calibrant is a static exact configuration, not a state the causal dynamics reaches.
^CV rose 0.10 -> 0.22 with profile min/max spreading 124/176 -> 148/302: the k22 d_H gain rides
 CONDENSATION, not equilibrium (LESSONS 6, 14) -- the same disqualifier found on the sphere.

Reading it:
- **The equilibrium baseline (k22=0) sits in the sphere's exact failing corner.** Compare the S^2
  baseline (REPORT_CDT_HUB sigma=0): f22 0.38, d_s 3.23, d_H 1.71 (ratio 0.69), CV 0.31, deg 14.6/10.2/84.
  The torus: f22 0.40, d_s 3.48, d_H 1.68 (ratio 0.68), CV 0.10, deg 15.4/11.0/79. **Essentially identical**
  -- heavy-tailed hubs (deg_max 79 vs the flat 14), d_H saturated low, d_s high. The torus forms hubs
  even though the uniform degree-6 flat slice is admissible (6 chi = 0) and IS the benchmark. Hub
  formation is entropic (many hubbed triangulations, one flat one), and it happens regardless of topology.
- **The k22 lever reproduces the anticorrelation.** k22: 0 -> 1.0 drives f22 0.40 -> 0.18, d_s DOWN
  (3.48 -> 3.27, onto benchmark) and d_H UP (1.68 -> 1.93) -- opposite directions, the campaign-5/6/7
  d_H-d_s tradeoff again -- while CV rises 0.10 -> 0.22 (condensation). Where d_s reaches benchmark d_H
  is still 0.78, on a condensing (non-3-manifold) profile. The two benchmark crossings are separated
  along the lever, exactly as on the sphere. **No accessible config passes G2 and G3 together.**

Prereg decision-rule landing: **rule 2 -- H_wall SUPPORTED, H_topo refuted.** The registered prior
(H_wall likelier, because the differential lock survives) held.

## Mechanism (why the torus does not help)

The campaign 5-7 wall had two roots and STAGE 1 shows both are topology-independent:
1. ALGEBRAIC: spatial-vertex density N0 and the (2,2) fraction f22 are ONE locked DOF (dN22 = -4 dN0).
   This is the differential of the Euler identity and is chi-independent -- proven above. Changing the
   slice genus cannot give N0 and f22 as two independent knobs.
2. ENTROPIC / DIFFUSION-GEOMETRY: at fixed counts the only freedom is the degree distribution, and the
   causal ensemble entropically fills it with hubs (short-range shortcuts) that saturate ball growth
   (d_H low) while holding the walk return down (d_s high). This is a property of the ensemble's
   diffusion geometry, not of the slice being a sphere -- so the torus hubs identically (deg_max 79).
   The admissible flat uniform slice has negligible entropic weight; the measure never sits there.

## Honest caveats

- Result 1 (the identity + its topology-independent differential) is EXACT and holds at every V, T,
  coupling, and genus. It is the load-bearing claim and needs no finite-size defense.
- Result 2 is V=6000, T=12, single MC seed (seed 0), matched to the campaign-7 baseline. The baseline
  k22=0 point is a genuine equilibrium (stable 262->1700 sweeps; k3 frozen past tune). The k22=1.0 point
  is a warm-started, still-relaxing (f22 0.21->0.18, CV rising) CONDENSING state -- reported as a lever/
  trend demonstration, NOT an equilibrium pass; its only role is to show the anticorrelation direction
  and the condensation, both of which match the sphere. A fuller seed-averaged k22 / slice-size scan at
  V=6000-24000 (uncapped box) is the natural confirmation; the sandbox verdict does not depend on it.
- Benchmark cross-validated two ways (Kuhn T^3 m=10 and the flat foliated calibrant) -- they agree, and
  both have uniform degree 14, unlike the causal state. Scoring uses seed-averaged windows (LESSONS 1-2).
- Census bad=0 in every torus snapshot: the construction never leaves T^2 x S^1; the obstruction is
  dimensional/entropic, not topological.

## What this closes, and the stage-2 / stage-3 recommendation

CLOSED by STAGE 1: the "different spatial topology" escape. Higher genus does NOT help -- the
differential lock dN22 = -4 dN0 is chi-independent (proven), so no closed-surface slice gives N0 and
f22 as two knobs, and the causal ensemble hubs regardless of genus. The surgical branch of the frontier
is closed: the 2+1D wall is a property of the dimension and the causal-ensemble diffusion geometry, not
of the spatial topology.

Does this motivate stage 2 (exotic / non-local action) or stage 3 (3+1D)? **It motivates continuing,
and it re-ranks them:**
- STAGE 3 (3+1D) is now the BEST-motivated next step. STAGE 1 localizes the obstruction to "2+1D +
  local causal measure": it is topology-independent, so the remaining escape is DIMENSIONAL. 3+1D CDT
  has a known de Sitter phase that reaches 4 in both dimensions by a different mechanism (an extended
  emergent geometry, not a hub-free reshuffle at fixed 2+1D counts). The stage-1 result -- the wall
  survives every in-2+1D lever including topology -- is exactly the evidence that says "change the
  dimension, not the slice."
- STAGE 2 (non-local action) remains worth ONE probe, but with a cautious prior. The obstruction's
  second root is diffusion geometry (hubs), and campaign 7 showed a LOCAL degree-measure term only
  reparameterizes the tradeoff. A genuinely NON-LOCAL term acting on the global connectivity / return
  probability (not a local per-vertex penalty) is the one untested lever on the entropic root. But four
  local/structural levers have now failed (aspect, k0 x k22, hub-measure, topology), so expect it to be
  hard; its value is mainly to test whether the diffusion-geometry root can be reshaped WITHIN 2+1D.

Recommendation for the handoff: **proceed to STAGE 3 (3+1D) as primary**; keep STAGE 2 (non-local
action) as a secondary in-2+1D probe. STAGE 1 is a genuine result either way -- it did not open the
joint pass, but it converted "the sphere assumption blocks it" into the stronger, exact statement that
the block is topology-independent, which is what sharpens the case for the dimensional escape.
