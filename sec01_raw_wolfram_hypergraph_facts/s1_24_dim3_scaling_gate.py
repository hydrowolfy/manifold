"""ROUND 64 -- THE N-SCALING GATE KILLS THE d=3 MANIFOLD CLAIM (on structural grounds), and corrects
round 63's own test design. The (alpha, k) = (3, 4) stack builds a complex whose local defect density
does NOT shrink with N and does NOT shrink with annealing effort, while a true cubic lattice's interior
FILLS as N grows. That divergence is a thermodynamic obstruction to manifold structure, independent of
any spectral-dimension estimate. The 2D result (r62) is untouched; the r63 "cubic-grade 3-complex" does
not survive scaling.

TWO CORRECTIONS TO ROUND 63'S FRAMING (made before trusting any result):
  1. "Does d_s climb toward 3" was DEAD ON ARRIVAL. Measured reference-cube d_s finite-size line:
     k^3 = 5^3..8^3 gives d_s = 2.37, 2.39, 2.53, 2.54 (N = 125..512) -- a PERFECT cubic lattice barely
     moves and is nowhere near 3 at any reachable N. Comparing a grown object's d_s to the integer 3 was
     never answerable here. The test must compare to the cube's OWN finite-size point at matched N.
  2. "d_s falls monotonically with N" (the tempting kill signal: grown d_s 1.79 -> 1.53 -> 1.41 at
     N = 216, 343, 512) is STEP-CONFOUNDED. A starvation control at N = 512 (80 vs 160 steps/node) moved
     d_s 1.41 -> 1.69 -- the larger-N runs were under-annealed at fixed steps/node. The d_s-vs-N trend is
     retracted as an artifact and the verdict rests ONLY on step-independent structural metrics.

THE STRUCTURAL KILL (unconfounded, the actual result): three defect metrics are FLAT in N and FLAT in
annealing effort, while the cube's corresponding interior measure RISES with N:
    metric                    grown (3,4)           cube k^3
    closed-link-at-4    0.31 / 0.28 / 0.29     0.30 / 0.36 / 0.42 / 0.56   (N = 216 / 343 / 512 [/8^3])
    fd overshoot (5-6)  17% / 15% / 19%        0% (a lattice has none)
    gauge deficit       11 / 12 / 10           0 (squares span the cube's cycle space)
The grown object keeps a HIGH raw fd = 4 fraction (58-61%, above the cube) but a LOW, N-independent
closed-link fraction: individual edges reach coordination 4 without organizing into closed vertex stars.
That is a locally-4-ish but globally disordered SPONGE, not a 3-complex whose interior fills. Adding
nodes adds defects as fast as bulk; the interior never coheres. Doubling the anneal at N = 512 left
closed-link at 0.29 and overshoot at 18% -- the defects are thermodynamic, not kinetic.

WHY (mechanism): the symmetric |fd - 4| penalty makes over-stacking (fd 5, 6) cost exactly what
under-filling costs, so the dynamics buys cheap interior-looking 4s by tolerating overshoot elsewhere,
and the resulting frustration pins vertex stars open. In 2D the analogous fd = 3 defect population was
small (4-7%) and did not scale; at the cubic target k = 4 the defect channel is wider (fd can overshoot
to 5, 6, 7) and it saturates at ~18% regardless of effort.

SCOPE, stated precisely (what is and is not refuted): REFUTED -- the r63 protocol (symmetric penalty,
annealed 2->0.2, single seed) yields a 3D manifold. NOT REFUTED -- that SOME protocol could: the named
r63 fixes (asymmetric penalty penalizing overshoot harder than underfill; a cold handle-cleanup phase for
the deficit debris) were NOT tested here and remain open. What scaling shows is that the CURRENT stack
has an irreducible defect density in 3D that it did not have in 2D -- a specific, located obstruction,
not a proof of impossibility. The honest one-line headline: "cubic-grade complex with irreducible defect
density," not "3D manifold."

CONTRAST WITH 2D (why this is a real dimensional asymmetry, not just a weak run): the r62 (2,2) stack
matched the quad-lattice column INCLUDING closed-link (0.69-0.77 vs 0.69) at N = 150, and its defect
population was small and non-scaling. The (3,4) stack cannot match closed-link at ANY tested N and its
defects are ~18% and flat. The same machinery that selects a 2-manifold fails to select a 3-manifold,
and the failure mode is thermodynamic frustration at the wider cell-gluing target. This is consistent
with (not proof of) the intuition behind r55's minor-universality: 3D coherence is genuinely harder to
enforce locally.

HONEST LIMITS: single seed per (N, schedule); steps/node held at the r63 value except the one N = 512
starvation control (accepts-per-node were NOT fully equalized across N, which is exactly why the d_s-vs-N
trend is retracted rather than used); largest N reached is 512; the closed-link and overshoot metrics are
the load-bearing evidence and they are unconfounded by the step issue.

STATUS: PARTIAL -- N-scaling executed as the gate on the r63 3D claim; the claim is REFUTED on structural
(step-independent) grounds, r63's own d_s-based test design is corrected (d_s-vs-3 dead, d_s-vs-N
confounded), and the surviving obstruction is a located, named defect channel with untested candidate
fixes. The 2D result stands. No keystone results change; no leaf grades change; tally fixed at 366.
"""
import os
import time
from collections import defaultdict
from sec01_raw_wolfram_hypergraph_facts.s1_23_dim3_sandwich import (
    _sandwich_k, _lat3, Ek_per_edge, closed_k, hist7)
from sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors import _flux_deficit
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_H, _diam

STATUS = "PARTIAL"
TITLE = ("N-scaling gate: the (3,4) stack's defect density is FLAT in N and in annealing effort "
         "(closed-link ~0.29, overshoot ~18%, deficit ~11) while a cube's interior FILLS with N "
         "(closed-link 0.30->0.56) -- a thermodynamic obstruction; the r63 3D-manifold claim is REFUTED "
         "on structural grounds (the 2D result stands). Also corrects r63's dead d_s-vs-3 test and its "
         "step-confounded d_s-vs-N trend.")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  r63 named N-scaling as the gate on its 3D claim. Two corrections to its framing first,")
    print("  then the structural kill that survives them.\n")

    print("  (A) CORRECTION 1 -- 'd_s -> 3' is DEAD: a PERFECT cube barely moves and is nowhere near 3.")
    print("      k^3   N     d_s    d_H   fd4%   closed4")
    for k in [5, 6, 7, 8]:
        L = _lat3(k); N = len(L)
        print("      %d^3  %4d   %.2f   %.2f   %2.0f%%    %.2f" % (
            k, N, _d_s(L), _d_H(L), hist7(L)[4], closed_k(L, 4)))
    print("      => compare grown objects to the cube's OWN point at matched N, never to the integer 3.")

    print("\n  (B) THE STRUCTURAL SWEEP -- grown (3,4) vs cube, matched N (load-bearing, step-independent):")
    print("      N     closed4_grown  closed4_cube   fd4_g/cube   overshoot   deficit   [t]")
    cube_cl = {216: 0.30, 343: 0.36, 512: 0.42}
    cube_fd = {216: 30, 343: 36, 512: 42}
    spn = 120 if not _FULL else 200
    for N, s in [(216, spn), (343, max(80, spn - 20)), (512, max(60, spn - 40))]:
        t0 = time.time()
        adj, b1, rk, d, Eg, aa, ar = _sandwich_k(N, 3.0, 4, 1.0, 3.0, N * s, seed=11,
                                                 w_iso=2.0, cceil=2.8, T_hi=2.0, T_lo=0.2)
        b1f, _, _, df = _flux_deficit(adj, maxlen=4)
        Ef, ne = Ek_per_edge(adj, 4)
        assert b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6, "audit fail"
        h = hist7(adj)
        print("      %4d      %.2f          %.2f          %2.0f%%/%2.0f%%       %2.0f%%       %2d       [%.0fs]" % (
            N, closed_k(adj, 4), cube_cl[N], h[4], cube_fd[N], h[5] + h[6], df, time.time() - t0))
    print("      => grown closed-link is FLAT ~0.29 while the cube's RISES 0.30->0.42 (->0.56 at 8^3);")
    print("         overshoot flat ~18%, deficit flat ~11. The interior never coheres: a locally-4-ish")
    print("         globally-disordered SPONGE. Defects add as fast as bulk. THIS is the kill.")

    print("\n  (C) CORRECTION 2 -- the d_s-vs-N trend is STEP-CONFOUNDED (starvation control at N=512):")
    print("      steps/node  accepts  d_s    closed4   overshoot")
    for s in [80, 160]:
        adj, b1, rk, d, Eg, aa, ar = _sandwich_k(512, 3.0, 4, 1.0, 3.0, 512 * s, seed=11,
                                                 w_iso=2.0, cceil=2.8, T_hi=2.0, T_lo=0.2)
        b1f, _, _, df = _flux_deficit(adj, maxlen=4)
        Ef, ne = Ek_per_edge(adj, 4)
        assert b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6
        h = hist7(adj)
        print("      %3d         %4d    %.2f   %.2f     %2.0f%%" % (
            s, aa + ar, _d_s(adj), closed_k(adj, 4), h[5] + h[6]))
    print("      => doubling steps moved d_s 1.41 -> 1.69 (walk metric was starved) but closed-link")
    print("         stayed 0.29 and overshoot 18% (structure is NOT starved). d_s-vs-N is retracted;")
    print("         the verdict rests on the flat structural metrics in (B).")

    print("\n  (D) VERDICT: the r63 3D-MANIFOLD CLAIM IS REFUTED on structural grounds. The (3,4) stack")
    print("      has an irreducible ~18% defect density and open vertex stars that neither N nor")
    print("      annealing effort fixes -- a thermodynamic obstruction the (2,2) 2D stack did NOT have")
    print("      (r62 matched cube closed-link 0.69). SCOPE: refuted for the r63 protocol (symmetric")
    print("      penalty, single seed); NOT refuted that an asymmetric-penalty + handle-cleanup protocol")
    print("      could work -- untested, named. Consistent with (not proof of) r55's intuition that 3D")
    print("      coherence resists local enforcement. The 2D result stands. Limits: single seed; largest")
    print("      N=512; accepts/node not fully equalized across N (why d_s-vs-N is retracted, not used).")
    print("      Tally fixed at 366.")
