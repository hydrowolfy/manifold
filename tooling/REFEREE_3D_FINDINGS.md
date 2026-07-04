# Independent re-adjudication of the 3D manifold claim

Scope: does the project's frame-free 3D construction (`_sandwich_k` with α=3, fd target k=4,
round 63) reach a discrete 3-manifold? Judged with independent machinery (`tooling/referee_3d.py`),
against the project's own refutation (round 64). "Naturalness" is not an argument.

## New machinery (and why 3D is not just 2D-with-a-bigger-number)

A 3-manifold's local criterion is that every interior vertex LINK is a triangulated 2-SPHERE
(boundary vertex -> 2-disk) — the 3D analog of "link is a cycle." `referee_3d.py` implements
this and is calibrated on a Freudenthal (Kuhn) triangulation of a grid:

| control | interior links | boundary links | bad |
|---|---|---|---|
| Freudenthal 4^3 | 8 spheres | 56 disks | 0 |
| Freudenthal 5^3 | 27 spheres | 98 disks | 0 |

Decisive structural fact, made concrete: the cubic lattice `_lat3` FAILS the flag version of
this test — an interior cube vertex has 6 neighbors with **zero** edges among them, so its flag
link is 6 isolated points, not a 2-sphere (flag-link fail fraction = 1.0). A perfect cube is not
a flag 3-manifold. This is the minor-universality obstruction of round 55 made empirical: there
is no planarity-style graph criterion for d=3, so a "cubic-grade" graph cannot be certified a
3-manifold by links — neither can the cube. The cubic-target candidate is therefore judged by
SCALING and INTERIOR-FILL holdouts, matched to the cube's own finite-size line (not to 3).

## Independent re-adjudication (candidate `_sandwich_k(3,4)` vs cube `_lat3`)

N = k^3, 2 seeds, 40N MCMC steps. Independent ball-growth d_H, lazy-RW d_s, and interior-fill
(fraction of vertices with 2-ball volume ≥ the cube-interior value 25):

| N | cand d_H(3-8) | cand d_s(8-24) | cand artic frac | cand bulk | cube d_H | cube d_s | cube artic | cube bulk |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 64  | 1.07 | 1.07 | 0.125 | 0.03 | 0.82 | 1.88 | 0 | 0.00 |
| 125 | 1.62 | 1.26 | 0.040 | 0.01 | 1.29 | 2.03 | 0 | 0.01 |
| 216 | 1.79 | 1.29 | 0.062 | 0.02 | 1.56 | 2.13 | 0 | 0.04 |

Reading:
- **Spectral dimension fails.** Candidate d_s plateaus ~1.3 while the cube climbs 1.88 -> 2.13
  toward 3; the gap widens with N. (The cube's own d_s is far below 3 at reachable N — round 64
  was right that "does d_s climb to 3" is the wrong question — but the candidate is far below
  even the matched cube.)
- **The d_H / d_s split is the non-manifold signature.** The candidate's d_H (1.79) EXCEEDS its
  own d_s (1.29) and even the cube's d_H (1.56). High volume growth with poor transport is a
  disordered sponge, not a manifold — the same fractal split (d_H > d_s) that flags generic
  trees and the keystone. Round 63's "cubic-grade" claim rests on d_H (volume) matching the
  cube; the transport dimension refutes it.
- **The interior does not fill.** The candidate's cube-interior-bulk fraction sits at ~0.02 and
  is flat in N; the cube's rises (0 -> 0.04) as its interior fills. This independently
  reproduces round 64's structural kill with a different, dimension-agnostic measure.
- **Articulation points persist** (~0.04-0.06) where the cube has exactly 0.

## Verdict

The 3D construction does NOT reach a discrete 3-manifold, and our independent holdouts confirm
round 64 rather than overturn it (unlike the round-60 "glass" that was later retracted — this
refutation is real). The object is a locally-4-connected but globally disordered sponge:
volume-dimension keeps up with the cube, transport-dimension and interior coherence do not.

## The one constructive result, and the forward route

The new link machinery says something the project only argued abstractly: because the cube
itself fails the flag-link test, a cubic fd=4 target is the wrong objective for a *testable*
3-manifold. The only route that can be certified is one that targets TRIANGULATED local
structure — a construction whose objective drives each interior vertex link toward a 2-sphere
(calibrate against the Freudenthal control), then validate with the `referee_3d.py` link census
(interior spheres / boundary disks, bad -> 0 with N) plus d_s -> cube line. That is a concrete,
falsifiable next experiment, and it is a different construction from `_sandwich_k`.

## Limits

N ≤ 216 (6^3), 2 seeds, 40N steps — comparable to the project's own 3D N range; the estimators
are independent of the project's. The link criterion is calibrated (Freudenthal passes, cube
fails-as-expected). No fabricated numbers.
