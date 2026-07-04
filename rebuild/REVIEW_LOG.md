# Review log — rebuild/2d-manifold-minimal

Protocol: reviewers examine the work in the voice of the paper's primary author, cite a real
paper for each critique, and the primary agent must resolve each before merge. Merge to `main`
is gated on all reviewers signing off. **Status: NOT signed off — round 1 only.** One review
round is recorded here (performed by the orchestrator standing in as reviewer); the full
multi-agent reviewer panel is the next step and is required before any merge.

## Round 1

**R1 — Declare the 2-cells; a graph is not a complex.**
Source: Klee & Novik, face enumeration; Grigor'yan et al., *Graphs Associated with Simplicial
Complexes*. A 1-skeleton does not fix the 2-cells, and graph homology can differ from simplicial
homology.
Primary agent: Accepted. The construction's 2-cells are declared as the bounded faces of the
planar embedding, computed deterministically in `tooling/referee_2d_topology.py`; all link and
incidence tests run on that declared complex, not on a short-cycle proxy. **Resolved.**

**R2 — A spectral dimension near the grid is necessary, not sufficient.**
Source: Ambjørn–Jurkiewicz–Loll (CDT); Durhuus–Jónsson–Wheater (generic trees: d_H=2, d_s=4/3);
Le Gall/Miermont (Brownian sphere: S² topology, Hausdorff dim 4). A single exponent, or even a
pair, cannot certify manifoldness.
Primary agent: Accepted, and this is why the branch reports link-correctness, edge incidence,
and boundary structure alongside d_s. At N=140 the planar route gives articulation fraction
0.019 and 100% simple boundary, not merely a matching d_s. **Partially resolved — the defect
densities must still be shown to → 0 with N (open).**

**R3 — The boundary must be a stable simple cycle across sizes.**
Source: Datta, *Minimal Triangulations of Manifolds* (boundary vertex links are intervals).
Primary agent: 100% single simple boundary at N=140 and at N=120/170 in the validation report.
**Partially resolved — N-scaling of boundary stability is open.**

**R4 — Discriminate against the degree-preserving null.**
Source: Maslov & Sneppen (Science 2002), degree-preserving rewiring at 10×|E| swaps.
Primary agent: The prior null panel shows the s1_22 candidate fails this (rewire *raises* d_s).
The planar route has not yet been run against its own rewire on the topology holdouts.
**Open — required before sign-off.**

### Round-1 outcome
Two of four comments resolved; two require an N-scaling sweep of the planar route and a rewire
comparison. Reviewer sign-off withheld. Per the merge gate, `rebuild/2d-manifold-minimal` does
**not** merge to `main` yet.
