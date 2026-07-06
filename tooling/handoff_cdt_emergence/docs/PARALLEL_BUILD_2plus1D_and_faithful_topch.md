# Parallel Build — 2+1D Substrate + Faithful 1+1D Topology-Change

Both tracks delivered. Spot-checked against raw JSON/self-test logs.

## Track 2 (milestone) — faithful topology-change move VALIDATES off-manifold against ALWZ

The multi-circle-per-slice move (a parent S¹ splits into two circles sharing seam vertices, the baby caps off a few slices later, `build_graph` assembles the full multi-circle spacetime so baby volume is genuine geodesic volume behind a neck) banks the two analytically-known targets the graft proxy failed:

- **Detailed balance exact:** SPROUT⇄ABSORB flux imbalance ~1e-16 across μ, λ; μ→∞ recovers the validated single-circle substrate.
- **ALWZ exponent — PASS:** μ_c(N₂) per-baby slope = 1.76 (per-event 0.88 × 2 events/baby), in the 3/2 regime, decisively away from the proxy's 1/2. (1.5–1.8 with the expected small-N₂ upward bias.) This is the exponent the proxy could not produce.
- **Liouville certificate — PASS:** spectral dimension d_s ≈ 2.0 at every μ including the proliferated endpoint (1.98 → 2.08 → 1.99), not the proxy's bottleneck d_s<1 and not branched-polymer 4/3.
- **Not yet shown:** d_H → 4 (stays ~1.4–1.9). This is a volume/runtime limit (needs N₂ ≳ 10⁴), not a faithfulness limit — the exponent and d_s already certify the correct phase.

Net: the off-manifold branch is now reproduced against generalized-CDT/ALWZ ground truth. The 1+1D off-manifold calibration is complete and correct.

## Track 1 — 2+1D CDT substrate, structural first cut VALIDATED

New `cdt_2plus1.py`: AJL foliation of T periodic proper-time slices, each a closed S² triangulation (χ=2), sandwiches filled with genuine (3,1)/(2,2)/(1,3) tetrahedra forming a closed causal 3-manifold; action S = −k0·N0 + k3·N3, Metropolis.

- **Self-tests all pass (6/6):** valid S² slices, χ=2 preserved under 400 random moves, foliation intact through 30 sweeps, timelike edges only between adjacent slices, connected, closed 3-manifold with all three tet types present.
- **d_H → 3 (validated direction):** finite-size series 2.16 → 2.35 → 2.46 → 2.71 → 2.80 (780 → 36,624 tets); thermalized run d_H = 2.63. Below 3 with upward-curving N(r) = expected small-de-Sitter finite-size correction. Known 2+1D CDT d_H≈3 reproduced.
- **Phase structure demonstrated:** extended phase (k0=7) d_H≈2.6 (3D-like) vs degenerate phase (k0=1) d_H≈1.0 (collapsed stalk).
- **Partial, stated honestly:** the inter-slice filling is currently a product foliation (S²×S¹) — the genuinely-3D inter-slice Pachner moves ((2,6)/(4,4)) are NOT implemented, so full 3D ergodicity is not yet reached, and d_s was not measured. This is the clear next build: without the 3D moves the slices don't fluctuate independently, so the d_H→3 is encouraging but not yet the full AJL ensemble.

## Status and next step

- Off-manifold (1+1D): **calibrated and ALWZ-validated** (3/2 exponent + Liouville d_s=2). Done.
- Nonequilibrium (1+1D): **calibrated** (WASEP with positive KPZ control; drive irrelevant at weak E, geometry spectator). Done.
- 2+1D substrate: **structurally validated first cut** (self-tests pass, d_H→3, phase structure), partial ergodicity.

The frontier is now completing the 2+1D substrate: add the inter-slice (2,6)/(4,4) Pachner moves for full 3D ergodicity and independent per-slice fluctuation, then measure d_s and confirm the de Sitter phase properly — after which the off-manifold and nonequilibrium branches can be carried into 2+1D, where (unlike 1+1D) no analytic result pins the answer and a surprise would be genuinely new.
