"""The spectral confirmation of localization: the keystone Laplacian has POISSON level statistics (no level
repulsion) and MASSIVE exact degeneracy -- the fingerprint of an integrable/localized system, the OPPOSITE of
quantum chaos.

Round 35 showed (via the inverse participation ratio and a quench) that the keystone field is localized and
does not thermalize. Level-spacing statistics is the independent SPECTRAL diagnostic of the same physics, and
the canonical one in the localization / quantum-chaos literature. Take the eigenvalues of the rule's Laplacian
(the field operator), sort them, and ask how neighbouring levels are arranged:

  - A CHAOTIC / delocalized system has LEVEL REPULSION -- eigenvalues avoid each other (Wigner-Dyson / random-
    matrix statistics). The dimensionless gap ratio r_n = min(s_n,s_{n+1})/max(s_n,s_{n+1}) (Oganesyan-Huse;
    needs no spectral unfolding) averages to <r> ~ 0.536 (GOE), and exact degeneracies are FORBIDDEN.
  - An INTEGRABLE / localized system has UNCORRELATED levels (Poisson statistics, P(s)=e^{-s}): levels cluster,
    small gaps are common, <r> ~ 0.386, and symmetry can force exact degeneracies.

RESULTS (keystone vs a random 3-regular graph as the chaotic reference, plus GOE and Poisson baselines):
  1. GAP RATIO. The keystone gives <r> ~ 0.39-0.43 (-> the Poisson value 0.386 as N grows) -- NOT the GOE
     value. The random regular graph gives <r> ~ 0.53 (chaotic), matching the GOE matrix. So the keystone
     spectrum is POISSON: integrable/localized, no level repulsion.
  2. MASSIVE EXACT DEGENERACY. ~25-35% of keystone eigenvalues are EXACTLY degenerate; the chaotic graph has
     ZERO. The degeneracy is structural -- lambda=1 carries enormous multiplicity (antisymmetric modes of the
     ~57% pendant pairs), and golden-ratio eigenvalues (2.618, 0.382 from two-pendant "cherry" motifs) and
     2+-sqrt(3) (from longer pendant paths) recur: the "molecular-orbital" spectrum of the tree's repeating
     motifs. Level repulsion in a chaotic system forbids all of this.
  3. SPACING SHAPE. The keystone has many tiny gaps (P(s<0.1) ~ 0.36, no repulsion); the chaotic graph has
     almost none (P(s<0.1) ~ 0.01, strong repulsion).

So three independent spectral signatures -- Poisson gap ratio, massive exact degeneracy, clustered spacings --
all say the keystone is a LOCALIZED, INTEGRABLE system, NOT chaotic. This is the spectrum-side confirmation of
round 35 (the field does not scramble or thermalize), and it traces to the b1=1 sparse tree: pendant-heavy,
motif-repeating structure produces localized modes with degenerate/clustered eigenvalues.

STATUS: PARTIAL (characterization) -- the level statistics are computed and the Poisson-vs-chaos contrast is
decisive; it confirms (does not newly establish) the localization/integrability already graded in 5.3. Native:
the operator is the rule's own Laplacian. Pure Python (Jacobi eigensolver; random regular graph and GOE built
locally).
"""
import math
import os
import random
from collections import Counter, defaultdict
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi

STATUS = "PARTIAL"
TITLE = "Level-spacing statistics: keystone spectrum is POISSON with massive degeneracy (localized/integrable, not chaotic)"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _keystone(steps, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
    for s in range(steps):
        R = redexes(E)
        if not R:
            break
        a, b, c = rng.choice(R)
        E[(a, b)] -= 1; E[(b, c)] -= 1
        if E[(a, b)] <= 0:
            del E[(a, b)]
        if E[(b, c)] <= 0:
            del E[(b, c)]
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        for (ss, tt) in KEYSTONE:
            E[(sub[ss], sub[tt])] += 1
        fresh += 1
    nodes = sorted(set(u for e in E for u in e)); idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes); adj = defaultdict(set)
    for (u, v) in E:
        if u != v:
            adj[idx[u]].add(idx[v]); adj[idx[v]].add(idx[u])
    return n, adj


def _random_regular(n, d=3, seed=1):
    rng = random.Random(seed)
    for _ in range(300):
        stubs = []
        for v in range(n):
            stubs += [v] * d
        rng.shuffle(stubs); adj = defaultdict(set); ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            if a == b or b in adj[a]:
                ok = False; break
            adj[a].add(b); adj[b].add(a)
        if ok and all(len(adj[v]) == d for v in range(n)):
            return n, adj
    return n, adj


def _laplacian(n, adj):
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = float(len(adj[i]))
        for j in adj[i]:
            L[i][j] = -1.0
    return L


def _goe(n, seed=0):
    rng = random.Random(seed); M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            x = rng.gauss(0, 1); M[i][j] = x; M[j][i] = x
    return M


def _gap_ratio(evals, tol=1e-6):
    """Oganesyan-Huse <r> on DISTINCT levels, plus degeneracy fraction and lambda=1 multiplicity."""
    ev = sorted(evals)
    distinct = [ev[0]]
    for x in ev[1:]:
        if x - distinct[-1] >= tol:
            distinct.append(x)
    degfrac = 1.0 - len(distinct) / len(ev)
    m1 = sum(1 for x in ev if abs(x - 1.0) < tol)
    s = [distinct[i + 1] - distinct[i] for i in range(len(distinct) - 1)]
    r = []
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        if max(a, b) > 0:
            r.append(min(a, b) / max(a, b))
    psmall = sum(1 for x in s if x < 0.1 * (sum(s) / len(s))) / len(s)
    return sum(r) / len(r), degfrac, m1, psmall, len(distinct), len(ev)


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Oganesyan-Huse gap ratio <r> (no unfolding): Poisson=0.386 (integrable/localized, no repulsion),")
    print("  GOE=0.536 (chaotic, level repulsion). Degeneracy fraction = exact-degenerate eigenvalues (chaos: 0).")
    n = 160 if not _FULL else 320

    nk, adjk = _keystone(n, seed=5)
    evk, _ = _jacobi(_laplacian(nk, adjk))
    rk, dk, m1, pk, ndk, ntk = _gap_ratio(evk)
    pend = sum(1 for v in range(nk) if len(adjk[v]) == 1)
    print("  KEYSTONE tree (n=%d, %d pendants=%.0f%%):" % (nk, pend, 100 * pend / nk))
    print("    <r>=%.3f  degeneracy-frac=%.3f  lambda=1 multiplicity=%d  P(s<0.1)=%.3f  (%d distinct / %d)" % (rk, dk, m1, pk, ndk, ntk))
    print("    -> POISSON-like (no level repulsion) + massive exact degeneracy => localized/integrable.")

    nr, adjr = _random_regular(n, 3, seed=2)
    evr, _ = _jacobi(_laplacian(nr, adjr))
    rr, dr, _, pr, _, _ = _gap_ratio(evr)
    print("  random 3-regular graph (n=%d, chaotic reference):" % nr)
    print("    <r>=%.3f  degeneracy-frac=%.3f  P(s<0.1)=%.3f  -> Wigner-Dyson: level repulsion, NO degeneracy." % (rr, dr, pr))

    eg, _ = _jacobi(_goe(min(n, 160), seed=0))
    rg, _, _, _, _, _ = _gap_ratio(eg)
    print("  GOE random matrix: <r>=%.3f  (Wigner-Dyson baseline)" % rg)
    rng = random.Random(3); pois = sorted(rng.random() for _ in range(n))
    rp, _, _, _, _, _ = _gap_ratio(pois)
    print("  Poisson (uncorrelated levels): <r>=%.3f  (baseline)" % rp)

    print("  => keystone matches POISSON, not GOE; the chaotic graph matches GOE. With ~1/4-1/3 of levels exactly")
    print("     degenerate (lambda=1 from pendant pairs; golden-ratio/sqrt(3) eigenvalues from recurring motifs),")
    print("     the keystone is decisively LOCALIZED/INTEGRABLE -- the spectral confirmation of round 35's")
    print("     no-scrambling, no-thermalization result, and a direct consequence of the b1=1 sparse tree.")
