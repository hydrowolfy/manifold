# Red-team consult: is E5 a sound frame-freeness test?

Seat: rigor-first PL / combinatorial-topology specialist (archetype; Fable). Charge: does the
committee's E5 — "reconstruct the manifold's 2-cells from the UNLABELED 1-skeleton; if it
certifies without the foliation labels, frame-free stands" — actually decide frame-freeness?

## Verdict: REPLACE E5. As stated it is ill-posed in 3D.

### Why the 1-skeleton cannot decide this
- **Dancis (1984), Topology Appl. 18:17-26:** a closed triangulated n-manifold is determined by
  its (floor(n/2)+1)-skeleton. For n=3 that is the **2-skeleton**. The 1-skeleton sits strictly
  below the reconstruction threshold, so "recover the 3-manifold from its graph" has no unique
  answer in general.
- **Explicit catastrophe:** every 2-neighborly triangulation has the complete graph K_n as its
  1-skeleton. On 9 vertices the Altshuler-Steinberg census gives **1296 neighborly 3-spheres plus
  Walkup's 9-vertex twisted S^2-bundle over S^1** (uniqueness reproved by Bagchi-Datta). So the
  single graph K_9 supports **1297 certified 3-manifold triangulations in TWO homeomorphism
  types.** Graph -> manifold is massively underdetermined.
- Graph reconstruction DOES work for simplicial 2-spheres (Steinitz/Whitney) and simple polytopes
  (Blind-Mani 1987, Kalai 1988, Friedman 2009) - which is why the intuition misleads. Those do not
  transfer to 3-manifolds.
- **The one clean regime:** if the complex is **flag** (equals the clique complex of its graph),
  graph reconstruction is unique, polynomial, and automorphism-equivariant - the only case where a
  graph-only test is legitimate.

### Two loopholes E5 misses
1. **Canonicalization = a smuggled frame.** Because the graph underdetermines the complex, any
   reconstruction algorithm must SELECT among candidates; "lex-least under a vertex ordering" or
   any index-greedy fill-in imports a total order on vertices, i.e. a frame. "G determines K"
   silently becomes "G plus my canonicalization determines K."
2. **Category error (the deeper one).** Frame-freeness is a property of the THEORY (the move rule),
   not of a single configuration. A construction can emit individually graph-nice states while the
   permitted MOVES depend on the time label. E5 tests a snapshot and cannot see this at all.

Plus false-negative modes: non-uniqueness (2-neighborly outputs fail automatically), intractability
(superexponential candidate space; a timeout is not a frame), and testing the wrong unlabeled
object (graph-only is strictly stronger than label-free).

## Replacement test (adopted)
- **Tier A - state test:** strip labels; run the vertex-link-2-sphere census on the unlabeled
  **2-skeleton** (Dancis-sufficient, label-free). Optional bonus A': if the complex is flag, verify
  Cl(G) ~= K and re-run graph-only.
- **Tier B - the real content, a GAUGE-INVARIANCE test:** let F be the forgetful map
  {labeled configs} -> {unlabeled complexes up to iso}. Require the move relation to DESCEND to the
  quotient (if F(x)~=F(y) then F(Moves(x))~=F(Moves(y))) and every exported observable to factor
  through F. No reconstruction is ever attempted, so the canonicalization loophole cannot arise.
- **PASS = A and B.** Reconstruction non-uniqueness or timeout = INCONCLUSIVE, never FAIL.
- **Controls:** positive = pure unlabeled Pachner dynamics must PASS A+B; negative = a deliberately
  foliation-dependent move set (moves only across even t) must FAIL B while passing A (proving A
  alone is insufficient); scramble = relabelings must leave the verdict exactly invariant.
- **Robustness:** every verdict must be a function of isomorphism classes only; adversarial vertex
  permutations must not change it; canonical forms allowed only INSIDE certified iso-invariant
  subroutines.

Sources (verified): Dancis 1984, Topology Appl. 18:17-26; Bagchi-Datta, uniqueness of Walkup's
9-vertex Klein-bottle triangulation (arXiv:math/0610825) and minimal triangulations of sphere
bundles over S^1 (arXiv:math/0610829); Bayer, "Graphs, Skeleta and Reconstruction of Polytopes"
(arXiv:1710.00118, covering Blind-Mani, Kalai, Perles, Friedman).
