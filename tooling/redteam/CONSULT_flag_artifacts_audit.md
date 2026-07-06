# Red-team consult: code audit of the flag generator + fns annealer

Seat: code-correctness / computational-topology auditor (archetype; Fable). It PROBED the new
artifacts (tooling/flag3_manifold.py) rather than reading them, and found real bugs. Fixes applied
this commit are noted inline.

## Bugs found (by probe)
1. **certify() false positive (critical) - FIXED.** "chi==2 + every edge in exactly 2 triangles +
   connected" does NOT imply a 2-sphere: a pinched pseudosurface (two spheres sharing two vertices)
   has chi=2 and passed at all vertices. The annealer's ONLY manifold safety net was this
   certificate, so a pinch-creating contraction could be silently accepted. FIX: added the
   local-disk condition - every vertex's link WITHIN the surface must be a single cycle. Verified
   the 16-cell and grown configs still certify (genuine manifolds), so the fix is not over-strict.
2. **count_empty_squares double-counted 2x - FIXED.** Dedup key was not canonical under swapping
   the two diagonal pairs. Probe: C4->2 (true 1), cube Q3->12 (true 6), 16-cell->12 (true 6). FIX:
   canonical unordered diagonal-pair key. Verified: Q3->6, 16-cell->6. **Every square count/density
   in DIRECTION_DECISION.md was 2x too high** - the real densities were ~1-2.5/vertex, not 2-5.
3. **d_H is uninstrumented at these N - RETRACTED.** The ball-growth d_H estimator reads ~0.99 on a
   genuine 3D control (3-torus, N=64), so the arm-B "d_H 0.2-0.5" numbers carry zero information and
   are withdrawn. GOOD NEWS: the lazy-RW d_s estimator reads 3.01 on the same 3-torus control, so
   d_s DOES work at these N - the gate must be d_s-vs-matched-control, not d_H.
4. **anneal_fns is a glassy OPTIMIZER, not valid MCMC.** No Metropolis-Hastings proposal-asymmetry
   correction; T advances on rejected proposals; 1-3% acceptance. Fine for "find min empty-square
   count" (an optimization), but must be LABELED as optimization, not equilibrium sampling.

## Assessment of the conclusions
- **Arm B ("flag crumples"): SOUND in direction, soft in numbers.** d_s discriminates (grown N=80
  reads 2.47 vs 2.94 for its degree-preserving rewire null; structurally diameter 3-4 at N=40-80
  with max degree ~50 = visibly crumpled) and matches Adamaszek-Hladky. But d_H retracted and d_s
  not to be quoted to 2 decimals.
- **Arm C ("inconclusive plateau"): the plateau's EXISTENCE is reproducible; its LEVEL is a sampler
  artifact; "inconclusive" is the correct label.** Rejection dominates (83-94%), doubling steps
  gained nothing, seed spread ~50%, last-improvement steps 434-2813 = kinetically frozen. Added
  confound the doc missed: a flag-no-square S^3 may simply NOT EXIST at N~24-80 (Przytycki-
  Swiatkowski fns triangulations are large), so E_min>0 can be forced by SIZE, not dynamics -
  a FAIL verdict therefore requires the density to fail to decrease ACROSS INCREASING N, and needs
  a known-fns positive control or a minimum-N existence argument to be interpretable.

## Actions taken
certify() local-disk fix + count halving are in this commit. The scheduled fns study is updated to
gate on d_s-vs-matched-3D-control (not d_H), to report corrected square densities, to escalate N,
and to caveat the min-N existence confound. d_H numbers retracted from DIRECTION_DECISION.md.
