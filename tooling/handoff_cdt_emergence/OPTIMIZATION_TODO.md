# Scoped next task: O(1)-per-move sampler (unlocks N3 = 16k-32k)

## Why
The verified sampler (`src/cdt_2plus1_faithful.c`) is O(N3) per move: each step rescans the
whole complex to (a) enumerate the forward redexes to pick one uniformly and set
`last_Nforward`, and (b) count reverse redexes for the Metropolis-Hastings ratio. That makes a
sweep O(N3^2) and caps practical volumes at ~8k. Production CDT codes are O(1) per move, which
is what makes CDT workstation-scale. This is the single change that lets the de Sitter gate
reach the decisive 16k-32k.

## What to build
Maintain, for each of the five move types, a **dynamic redex set** (a dense array of the
currently-valid redexes for that move) supporting O(1) append, O(1) swap-remove, and O(1)
uniform sampling, plus its length = the redex count.

- Move selection becomes: pick move type (1/5), sample a redex uniformly from its set in O(1),
  and `last_Nforward` = set length. `Nr` = the inverse set's length after applying. No scans.
- Incremental maintenance: a move changes tets only in a bounded region. The redex status of a
  face/edge/vertex depends only on the classes of its incident tets, and a tet's class depends
  only on its own 4 vertices, so **only elements incident to the removed-or-added tets can
  change status**. Before `apply_replace`: for each affected element, if it is currently in a
  redex set, swap-remove it. After `apply_replace`: for each affected element (new adjacency),
  test the five per-element predicates and append to the matching sets. `undo_last` must
  restore the sets symmetrically (snapshot the affected elements' membership before applying).
- Factor the per-element predicates out of the existing `count_23/32/26/62/44` (the geometric
  logic is already there): `is23(face), is26(face), is32(edge), is44(edge), is62(vert)`.

## Mandatory verification (do NOT skip -- this is why the ensemble is trustworthy)
1. `selftest` and `dbtest` still pass (closed/foliated/chi=2; DB residual ~1e-16).
2. **Independent recount agreement**: run `enumdump` on the FAST binary and check the
   maintained redex counts equal the from-scratch geometric recount (`recount_db_verify.py`)
   on >=1000 states in both phases -- exactly the check that defeated the common-mode-bug
   objection. If any state disagrees, the incremental maintenance has a bug; fix before use.
3. Observable match: frac22, N3 distribution, and the N(t) profile agree (within MC error)
   between the fast and reference binaries at a small volume.
4. Benchmark: confirm moves/sec is now ~volume-independent (O(1)/move) and report the speedup.

Only after 1-4 pass is the fast binary safe to swap into `run_desitter_gate.sh` and push the
volumes to 16k/32k.

## Risk note
This is correctness-critical surgery on the exact bookkeeping the referee round scrutinized.
It should be done as a focused effort with the recount verifier in the loop, NOT rushed. A
silent redex-set bug would break the ensemble while leaving forward/reverse residuals tiny --
which is the precise failure mode `recount_db_verify.py` exists to catch.
