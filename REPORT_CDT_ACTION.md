# STAGE 2 (exotic): can a NON-LOCAL action/measure term select the flat joint 3-manifold?

Second stage of the frontier sequence (surgical -> exotic -> 3+1D). Preregistered in
PREREG_CDT_ACTION.md (committed BEFORE the scan). Runner: cdt_frontier3_run.py (cdt_frontier2_run.py
core VERBATIM + two non-local terms; detailed balance + manifold preservation verified in --selftest
by brute force over all 5 move types). STAGE 1 (REPORT_CDT_TOPOLOGY.md) localized the 2+1D d_H-d_s
wall to "dimension + causal-ensemble diffusion geometry" and showed the flat joint 3-manifold EXISTS
in the ensemble but is ENTROPICALLY UNSELECTED. This stage asks the last in-2+1D question: can a
genuinely NON-LOCAL term -- one that sees GLOBAL structure, which no per-simplex/per-vertex term can
-- re-weight the measure to SELECT that flat 3-manifold, pulling BOTH d_H and d_s onto benchmark on a
UNIFORM profile?

## Verdict

**No. The wall survives the non-local probe. Neither non-local term -- alone, combined, or stacked on
the local levers -- selects the flat joint 3-manifold; every configuration slides along the SAME
d_H-d_s anticorrelation and no configuration meets the joint gate. The escape is DIMENSIONAL (3+1D),
now on even stronger evidence: we can independently control the two GLOBAL knobs the flat manifold
needs (a uniform volume profile AND a hub-free degree distribution) and still cannot make d_H and d_s
land on benchmark together.**

The two terms and what they proved:
- **NL-P** (non-local profile-uniformity, lam_p * sum_t (n(t)-nbar)^2, non-separable across the
  foliation): a POWERFUL, working lever -- it drives the spatial-volume profile to near-perfect
  uniformity (CV 0.25 -> 0.01) and even DE-CONDENSES the k22 lever that collapses on its own -- but it
  is **ORTHOGONAL to the wall**: on the (already-extended) baseline it moves d_s and d_H by nothing
  (3.30->3.42, ratio 0.707->0.712). The wall does not live in the volume profile. (H_null confirmed.)
- **NL-D** (symmetric global degree-distribution counter-term, lam_d * sum_v (deg_v-14)^2, driving the
  FULL distribution to the flat delta -- strictly stronger than campaign 7's one-sided hub cap): it
  suppresses hubs hard (deg sd 10.1->2.7, deg max 84->24) and lifts d_H, but **REPARAMETERIZES THE
  SAME TRADEOFF** -- d_H SATURATES at ratio ~0.85 (never reaching the 0.90 gate) while d_s COLLAPSES
  through and past the benchmark (3.30->2.75). Matching the flat degree signature (every vertex deg 14)
  is NECESSARY BUT NOT SUFFICIENT for flatness: the entropically-typical uniform-degree-14 causal
  triangulation is still an irregular, walk-confining geometry, not the flat lattice. (H_reparam.)

## The scan (V=6000, T=12, k0=2; warm-started from the k0=2 equilibrium; seed-averaged, seedbase 100)

Benchmark (size-matched flat T^3, m=10, 8 seeds): **d_s(8-24)=3.135+-0.172, d_H(2-6)=2.473**.
Gate: G2 d_H ratio>=0.90 (d_H>=2.226); G3 |d_s-3.135|<=0.20 (d_s in [2.935,3.335]); G4 profile CV<=0.35
non-drifting; G1 census bad=0; G5 genuine (equilibrium, non-projector). JOINT = G1..G5.

| config                       | f22  | deg sd | deg max | prof CV | d_s(8-24)     | d_H(2-6)      | dH rat | G2 | G3 | G4 | JOINT |
|------------------------------|------|--------|---------|---------|---------------|---------------|--------|----|----|----|-------|
| flat benchmark (target)      | .333 |  0.0   |   14    | 0.00    | 3.135 +-.172  | 2.473         | 1.00   | -  | -  | -  | (goal)|
| baseline k22=0               | .395 | 10.05  |   84    | 0.25    | 3.295 +-.246  | 1.749 +-.099  | 0.707  | F  | P  | P  | NO    |
| NL-P 0.10                    | .398 | 10.46  |   79    | 0.01    | 3.423 +-.242  | 1.761 +-.102  | 0.712  | F  | P  | P  | NO    |
| NL-D 0.02                    | .433 |  5.63  |   33    | 0.27    | 2.943 +-.289  | 2.036 +-.125  | 0.823  | F  | P~ | P  | NO    |
| NL-D 0.05                    | .440 |  3.66  |   26    | 0.24    | 2.748 +-.214  | 2.112 +-.058  | 0.854  | F  | F  | P  | NO    |
| NL-D 0.10                    | .450 |  2.67  |   24    | 0.24    | 2.825 +-.305  | 2.087 +-.055  | 0.844  | F  | F  | P  | NO    |
| NL-D 0.05 + NL-P 0.10        | .422 |  3.81  |   27    | 0.04    | 2.771 +-.243  | 2.159 +-.053  | 0.873  | F  | F  | P  | NO    |
| k22 1.0 + NL-P 0.10 (sb100)  | .124 | 11.89  |  119    | 0.01    | 2.953 +-.220  | 2.166 +-.086  | 0.876  | F  | P  | P  | NO*   |
| k22 1.0 + NL-P 0.10 (sb200)  | .124 | 11.89  |  119    | 0.01    | 3.106 +-.159  | 2.030 +-.092  | 0.821  | F  | P  | P  | NO*   |
| k22 1.0 + NL-P 0.10 + sig.015| .143 |  8.03  |   49    | 0.01    | 2.240 +-.146  | 2.602 +-.204  | 1.052  | P  | F  | P  | NO    |
| k22 1.0 + NL-P 0.10 + sig.05 | .188 |  6.55  |   35    | 0.01    | 2.055 +-.087  | 2.649 +-.160  | 1.071  | P  | F  | P  | NO    |

*the k22+NL-P d_s is in G3 but is a TRANSIENT crossing (f22 still relaxing 0.40->0.12 during the k22
warm-start; LESSONS 6/14) and it fails G5 (not an equilibrium) -- and the two independent seedbases
(0.876 vs 0.821) average to d_H ratio ~0.85, i.e. it sits with the pack, 0.05 short of G2.

## Reading it: two GLOBAL knobs, one wall

STAGE 1 named the wall's two roots. STAGE 2's non-local terms give INDEPENDENT control of exactly the
two global features that distinguish the flat manifold from the causal ensemble:
1. **Profile** (NL-P): drives CV to ~0.01 -- a razor-uniform tube, matching the flat manifold's flat
   profile. It even de-condenses the k22 lever whose d_s "pass" was a collapse in c6/PROFILE (k22=1.0
   ALONE: CV -> ~1; k22=1.0 + NL-P: CV 0.01). This is a genuinely new capability. But on the wall it
   does NOTHING (baseline d_s/d_H unchanged): the volume profile is not where the wall lives.
2. **Degree distribution** (NL-D / the hub cap): drives deg toward the flat delta at 14. It lifts d_H
   but along the anticorrelation -- d_s falls in lockstep.

The decisive test stacks BOTH plus the local levers: **k22 (lower f22) + NL-P (hold the profile
uniform) + a hub cap (remove hubs)** -- FOUR couplings producing a PERFECTLY UNIFORM (CV 0.01),
census-clean, hub-suppressed 3-manifold, the closest structural match to the flat calibrant any lever
set has produced. Result: d_H sails ABOVE benchmark (ratio 1.05-1.07) while d_s COLLAPSES to ~2.0-2.2
(deficit -0.9 to -1.1). Sweeping the hub cap from 0 to 0.05, d_H rises 0.85 -> 1.07 and d_s falls
3.03 -> 2.05: the benchmark crossings pass each other with a large gap (at the sigma where d_H = 0.90,
d_s is already ~2.8, below the G3 floor). **The needle is unthreadable.**

Mechanism (why even matched profile + matched degree is not enough): the flat manifold is a REGULAR
LATTICE -- every vertex has the same neighbourhood, and the lazy walk genuinely explores 3D (d_s ~3.13)
WITHOUT hubs. The causal ensemble stripped of hubs and forced uniform-profile is still IRREGULAR at the
level of local connectivity BEYOND degree (varying clustering / ball-growth per vertex), and that
irregularity CONFINES the walk (d_s ~2.0-2.2). The residual difference between "uniform-profile,
uniform-degree causal triangulation" and "flat lattice" is exactly the diffusion-geometry regularity
that NO profile term, degree term, or hub term reaches. It is the entropic root in its sharpest form:
the flat lattice is one microstate; the uniform-degree causal states are exponentially many, and they
are walk-confining, not flat.

## Preregistered decision-rule landing

- **NL-P: H_null** (registered prediction) CONFIRMED -- orthogonal to the wall on the baseline; its real
  effect is de-condensation, which does not open the gate (d_H stays low where the profile is uniform).
- **NL-D: H_reparam** CONFIRMED -- monotone anticorrelated lever, d_H saturates below G2 while d_s
  crosses G3; the two benchmark crossings never coincide. In fact NL-D is WORSE than c7's one-sided cap
  for d_H (saturates ~0.85 vs c7's 0.91-0.93) because forcing under-connected vertices UP to degree 14
  re-adds short-range connectivity that re-saturates ball growth.
- **Combined + local levers: H_reparam** -- the strongest 4-coupling lever passes G2 only by overshoot,
  with d_s deep below G3. No (lam_p, lam_d, sigma, k22) meets G2 and G3 together.
- **G5 (anti-triviality):** never reached -- there is no joint-passing state to scrutinize; the one
  G3-passing-with-highest-d_H point (k22+NL-P) is a non-equilibrium transient (fails G5a) whose stable
  version relaxes d_s out of G3. No frozen-projector artifact arises.

Registered ESCALATION TRIGGER (WSL confirmation "only if a V=6000 point meets G1-G5 or lands within
0.05 of BOTH gates on a low-CV STABLE state"): **NOT triggered.** The only within-0.05-of-both point
(k22+NL-P) is a transient, not a stable equilibrium, and the orthogonal move to close its 0.05 G2 gap
(add hub removal) is DEMONSTRATED to crash d_s out of G3 by ~1.0. So the neighbourhood is walled, not
near-passing; larger V cannot help (d_H, d_s are V-independent functions of slice size across campaigns
5-7). The V=6000 verdict is decisive and the WSL box was not needed. (Available as optional
reconfirmation; it would only re-measure the known slow campaign-5 large-V extrapolation, which these
non-local terms do not change.)

## Honest caveats

- V=6000, T=12, single MC seed (seed 0). The load-bearing evidence is the MONOTONE anticorrelation
  across nine configurations and the large gap between the two benchmark crossings -- robust to seed and
  to the exact equilibration, exactly as in campaigns 5-7. A second MC seed / V=12000 was preregistered
  only if a pass appeared; none did.
- Estimator seed variance is real and was respected: the k22+NL-P d_H read 0.876 at seedbase 100 but
  0.821 at seedbase 200 (LESSONS 2). Both windows and both seedbases are reported; no single-seedbase
  number is load-bearing.
- The k22 combos have a long warm-start transient (LESSONS 7); the k22+NL-P point is reported as a
  de-condensation demonstration + trend, explicitly NOT an equilibrium pass (its f22 was still drifting).
  The hub-cap "nudge/needle" points re-equilibrate fast and ARE plateaus.
- Detailed balance + manifold preservation for BOTH new terms are EXACT, not statistical: the per-move
  deltas were verified against brute force over all 5 move types (2500+ moves) and shown reverse =
  -forward in --selftest; census bad=0 in every snapshot of every chain.
- Both terms are genuine measure re-weightings on the SAME S^2 x S^1 alpha=1 ensemble (proposals
  unchanged) -- they answer "does the causal measure, re-weighted non-locally, select flat", not a
  different-ensemble question.

## What this closes, and the recommendation

CLOSED: the "non-local action/measure term" escape named in REPORT_CDT_HUB / _TOPOLOGY. A non-local
profile term and a non-local degree-distribution counter-term -- the two levers that directly target
the wall's two roots, and that CAN independently reproduce the flat manifold's global profile AND its
degree delta -- do not select the flat joint 3-manifold. Combined with campaigns 5-7 and stage 1, the
2+1D d_H-d_s wall now survives: aspect ratio (c5), the whole k0 x k22 plane (c6), a one-sided hub cap
(c7), spatial topology (stage 1), AND now a non-local profile term + a non-local symmetric degree
counter-term + their stack with the local levers (stage 2). Six independent lever families, one wall.
The reason is structural and now maximally sharp: reproducing the flat manifold's profile and degree is
not enough; the walk-confining IRREGULARITY of the causal 1-skeleton (beyond profile and degree)
remains, and it is entropically overwhelming.

**Recommendation: proceed to STAGE 3 (3+1D) as the primary and now sole remaining escape.** Stage 1
localized the obstruction to dimension; stage 2 shows even a non-local re-weighting cannot reshape the
2+1D diffusion geometry into the flat one. The evidence to change the DIMENSION (not the ensemble, the
topology, or the measure) is now complete.

**Stage-3 first step (cheap, before any heavy build):** check whether 3+1D CDT has an analogous
LOCKING IDENTITY. The 2+1D wall's algebraic root is the per-slice Euler identity F=2V-2chi giving
dN22=-4dN0 (one locked DOF). In 3+1D the spatial slices are 3-manifolds and the tetrahedron types are
(4,1)/(3,2)/(2,3)/(1,4); the analogous Dehn-Sommerville / Euler relations among N_{ij}, N0, N1 should
be written down FIRST. If they leave the spatial-vertex density and the timelike-simplex fraction as
TWO INDEPENDENT DOF (no 2+1D-style single lock), that is the concrete, a-priori reason 3+1D can reach 4
in both dimensions where 2+1D cannot -- and it is checkable on paper / in a tiny seed census before
committing to the full 3+1D Metropolis. If instead an analogous lock appears, that reshapes the whole
program. Either way it is the correct, cheap gate for stage 3.

## Reproduce

    PYTHONPATH=.:tooling python3 cdt_frontier3_run.py --selftest      # DB + manifold + term-delta checks
    # benchmark:
    PYTHONPATH=.:tooling python3 remeasure.py --torus 10 --seeds 8 --dswin 8-24,16-48 --seedbase 100
    # baseline then a term point (warm-start by copying the baseline pickle to the term's tag file):
    PYTHONPATH=.:tooling python3 cdt_frontier3_run.py --chunk --k0 2 --T 12 --V 6000 --seed 0 \
      --tune 500 --sweeps 100000 --budget-s 36 --scratch s2/scratch --log s2/rec.jsonl   # x3 -> f22~0.40
    cp s2/scratch/causal_k0+2.00_T12_V6000_s0_sig0.000_ld0.0000_lp0.0000_k220.00.pkl \
       s2/scratch/causal_k0+2.00_T12_V6000_s0_sig0.000_ld0.0500_lp0.0000_k220.00.pkl
    PYTHONPATH=.:tooling python3 cdt_frontier3_run.py --chunk --k0 2 --T 12 --V 6000 --seed 0 \
      --lam-d 0.05 --tune 500 --sweeps 100000 --budget-s 36 --scratch s2/scratch --log s2/rec.jsonl  # x2
    PYTHONPATH=.:tooling python3 remeasure.py --pkl <that pkl> --seeds 8 --dswin 8-24,16-48 --seedbase 100
    # NL-P: --lam-p 0.1 ; combined nudge: --k22 1.0 --lam-p 0.1 --sigma 0.05 --D0 14
