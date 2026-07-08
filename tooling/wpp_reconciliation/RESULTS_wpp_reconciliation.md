# WPP reconciliation experiment — results and verdict

**Date:** 2026-07-08. Preregistration: `PREREG_wpp_reconciliation.md` (committed before any run).
Code: `wpp_referee.py`. Selftests passed before touching WPP rules: triangulated torus reads
d_H=1.76/d_s=2.13/links 100% cycle; binary tree reads links 100% other; random cubic expander
reads diam=14 at N=3000 with ball-growth d_H=3.03 — the false-positive the suite exists to catch.

Rules exactly as documented in the WPP registry (init {{1,1,1},{1,1,1}}):
R1 = wm7714 ("knits a grid"), R2 = wm8619 (sphere-like), C1 = tree rule (negative control).
"GEN" = Wolfram's default oldest-first generational updating; "RND" = random sequential updating
(shown in the registry itself as a legitimate ordering). Event DAG recorded for all runs.

## Results

| run | N | d_H (r=2-8) | d_s peak | diam | link cycle/path/other | chain height |
|-----|-----|------|------|------|------|------|
| R1 GEN | 4000 | 1.72 | 2.08 | 88 (~√N) | .914 / .085 / .001 | = events |
| R1 RND s1 | 4000 | 1.06 | 1.24 | 1489 (~0.37N) | .006 / .612 / .382 | = events |
| R1 RND s2 | 4000 | 1.09 | 1.23 | 1481 | .007 / .603 / .390 | = events |
| R1 RND s3 | 4000 | 1.11 | 1.34 | 1505 | .007 / .604 / .389 | = events |
| R2 GEN | 4000 | 1.81 | 2.13 | 44 (~√N) | .881 / .077 / .041 | = events |
| R2 RND s1 | 4000 | 1.79 | 2.12 | 49 | .875 / .085 / .041 | = events |
| R2 RND s2 | 8000 | 1.78 | 2.13 | 62 | .910 / .059 / .030 | = events |
| C1 tree | 8000 | **2.88** | 1.61 | 39 (~log) | .000 / .000 / 1.000 | ~2.6·ln E |

## Findings

**1. The flagship grid rule's geometry lives in the scheduler, not the rule.** Under Wolfram's
default deterministic ordering, R1 knits a certified 2-manifold-with-boundary patch (d_s≈2,
diameter ~√N, 91% cycle links with the path fraction shrinking as N^(-1/2) — a clean boundary).
Under random sequential updating — an ordering the registry itself displays — the same rule
produces a quasi-1D filament (d_H≈1.1, diameter ≈ 0.37·N, <1% cycle links), reproducibly across
3 seeds. Structurally, R1 only ever has ~1-2 available matches (each event consumes one yy-edge
and mints exactly one), so it grows by a single front, and WHICH partner edge the front consumes —
oldest-first vs random — decides grid vs filament. A deterministic global updating order is an
implicit synchronization/foliation. This is precisely the ingredient CDT adds explicitly (and
pays for honestly); here it is present but hidden in the evolution convention, and the claimed
emergent geometry does not survive removing it.

**2. The sphere rule is ordering-robust but not quite a manifold.** R2 evolves identically under
GEN and RND (seed-identical observables — effectively confluent, i.e. trivially causal-invariant,
apparently because it too never has more than ~1 match). It reads d_s≈2.13, diameter ~√N, and its
link census is 91% cycle at N=8000 with the boundary fraction shrinking — but a persistent
singular set remains: "other" links at 4.1% → 3.0% (4k→8k), i.e. a singular-vertex COUNT growing
~N^0.55 while the fraction shrinks. Verdict: asymptotically-almost-everywhere a 2-manifold with a
sub-extensive cusp set (matching the "orbifold-like cusps" wolframphysics.org itself notes). Under
this program's certification standard (0 bad links, as met by construct_3manifold.py and the CDT
chain) it does not pass; as an emergent almost-manifold it is the best object in the tested set.

**3. The ball-growth dimension estimator ranks a TREE above the genuine surfaces.** The C1 control
(random tree growth) reads ball-growth d_H = 2.88 at N=8000 — higher than either actual
2D-surface rule — while being 100% non-manifold, log-diameter, and causally shallow. This is the
sharpest concrete demonstration of the program's standing methodological critique: V_r ~ r^d
ball growth, the WPP's headline dimension evidence, false-positives on non-geometric growth.
Any WPP dimension claim not accompanied by a joint d_s/d_H gate, diameter scaling, and a link
census should be treated as unestablished.

**4. No spacetime in the causal graph of the geometry showcases.** Both R1 and R2 have causal-DAG
longest-chain height = event count exactly: their event DAGs are width-~1 worldlines (never more
than ~1-2 concurrent matches). A (2+1)-dimensional causal graph would show height ~ E^(1/3). The
rules that produce the WPP's showcased spatial geometry produce NO emergent causal-graph
dimensionality at all — the growth is sequential crystallization. (C1 shows the opposite
degeneracy: Kleitman-Rothschild-style shallowness, height ~ log E.) The interesting WPP regime —
many concurrent matches with causal invariance — is exactly where our crumpling results predict
non-manifold attractors; the showcase rules avoid it by having no concurrency to be invariant over.

**5. Preregistration scorecard.** R2 and C1: as preregistered. R1: the preregistered d→2
prediction held only under the deterministic ordering — the prereg did not anticipate the
ordering-dependence, and the random-updating outcome (filament) falsifies the unconditional
form of the prediction. The headline prereg claims held: all documented geometry lives at d=2;
nothing in the tested set approaches a certified d=3 object; our falsifier (a WPP rule with joint
d_s=d_H=3, N^(1/3) diameter, clean 3-manifold census) was not triggered.

## Relation to the manifold program

The reconciliation lands where the red team's Wolfram seat predicted, but with a sharper
mechanism than expected: the WPP's emergent geometry, where real, is purchased either by a hidden
global scheduler (R1: the foliation is in the updating order) or by total sequentiality (R2: a
confluent, zero-concurrency growth process — geometric but with a worldline for a universe).
Neither route exhibits what the weaker thesis requires and CDT delivers at d=3: extended geometry
from an ensemble of concurrent local moves under an explicit causal structure, certified at the
link level, with matching d_s and d_H. The strong "geometry for free from generic rewriting"
reading remains falsified — now also empirically on the WPP's own flagship rules.

## Caveats

- Random-updating match selection here is A-uniform-then-B-uniform, not uniform over (A,B) pairs;
  with ~1-2 concurrent matches this is unlikely to matter, but it is not identical to
  SetReplace's "Random" ordering in edge cases.
- N ≤ 8000-16000, single growth trajectories (no ensemble averaging beyond seeds); the R2 cusp
  trend (sub-extensive singular set) could resolve either way at larger N.
- Only three rules tested; the registry is large. These are, however, the rules the WPP's own
  technical introduction leads with as emergent-geometry evidence.
- Skeleton graph = pairs within each ternary relation (the WPP's own convention for distance).
