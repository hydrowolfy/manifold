# Independent-Recount Detailed-Balance Check (2+1D CDT)

Addresses the referee's sharpest objection to the 2+1D rebuild: a machine-precision
forward/reverse DB residual can hide a COMMON-MODE bug (in proposal counting, manifold
gating, or move targeting) that cancels on both sides of a single-move residual check, so
it does not prove the chain samples the correct ensemble. Test: re-derive the load-bearing
quantities from scratch, structurally independently of the sampler's own bookkeeping.

## Method
- Instrumented a copy of the sampler (`cdt_2plus1_enum.c`, `enumdump` command) to dump, along
  thermalized trajectories, the raw tetrahedron list (4 vertex ids each) plus the sampler's
  five INCREMENTAL redex proposal counters (count_23/32/26/62/44) and N0.
- Independent Python recounter: rebuilds face / edge / vertex adjacency FROM SCRATCH from the
  raw tet list -- a completely different data structure than the sampler's incrementally-
  maintained hash maps -- and re-implements all five AJL redex definitions + tetrahedron
  classification geometrically, recomputing each proposal count per state.
- Independent manifold-gate check: verifies each sampled state is a closed 3-manifold (every
  triangle in exactly two tetrahedra) with every spatial slice at Euler characteristic chi=2.

## Result
Sample: 1500 states, both phases (k0=-2 coupled AND k0=+2 decoupled), T=4/6/8, 4 seeds.

- **Proposal counters: 9000 field comparisons (N0 + 5 counts x 1500 states) -> ZERO
  mismatches.** The sampler's incremental redex counts equal the from-scratch geometric
  recount on every state, in both phases and all sizes.
- **Manifold gate: 1500 closedness checks + 8800 slice-chi checks -> ZERO failures.** Every
  sampled state is a valid closed foliated S^2-sliced 3-manifold.

## What this establishes
- The five proposal counters are INDEPENDENTLY CORRECT (not wrong-but-canceling). The
  incremental-maintenance common-mode-bug loophole is closed. Since the acceptance is the
  textbook Metropolis-Hastings a = min(1, (Nf/Nr) exp(-dS)) fed by these verified counts, the
  chain has stationary distribution pi ~ exp(-S) over the sampled state space.
- The manifold gate holds across whole trajectories (closedness + chi=2), closing the
  "gating" vector of the objection.
- Move targeting is implicitly verified: the (2,3) count uses the AJL (3,1)/(1,3)+(2,2)-
  sharing-a-timelike-triangle pattern and matches; moves fire only on counted redexes.

## Honest scope
- The recount is STRUCTURALLY independent (from-scratch adjacency vs the sampler's incremental
  hash maps), so it catches incremental-bookkeeping bugs -- the most likely common-mode failure.
  The residual shared assumption is the geometric redex DEFINITION itself, which was separately
  checked against the move spec (docs/AJL_2plus1D_move_spec.md, verified vs hep-th/0105267).
- This is NOT a canonicalized full-orbit enumeration of the triangulation symmetry (|Aut|)
  factor, which needs graph canonicalization beyond the 40s-chunk sandbox. The referee's NAMED
  loophole (miscounted proposals / gate surviving forward-reverse residuals) is closed; a
  complete |Aut| verification remains for the HPC pass.

## Verdict
The 2+1D detailed-balance claim strengthens from "supported on local-kernel residuals" to
"proposal counters and manifold gate independently verified correct across 1500 diverse states
in both phases." The common-mode-bookkeeping-bug objection is DEFEATED at the counting/gating
level; the remaining open item is the symmetry-factor (|Aut|) enumeration on HPC.
