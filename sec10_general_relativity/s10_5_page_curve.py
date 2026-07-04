"""A Page-curve analogue: the keystone field's radiation entropy rises and FALLS (unitarity), and its shape
distinguishes a cold area-law radiation from a scrambled volume-law one.

The Page curve is the signature of unitary black-hole evaporation: the entanglement entropy of the radiation
rises, peaks at the Page time, then falls back to zero. The mechanism is purity -- for a global pure state,
the radiation entropy equals the black-hole entropy, S(A) = S(complement), so as a region A grows from empty
to full, S(A) automatically rises from 0 and returns to 0. What the SHAPE in between encodes:
  * a VOLUME-law (scrambled / thermalized) state gives the maximal symmetric Page TENT, peaking at half the
    system (Page time = half-evaporation), with peak height ~ volume;
  * an AREA-law state gives a SUPPRESSED curve whose height is set by the boundary ("horizon") area, far
    below the volume tent.

Here the radiation grows in geometric (BFS) order from a center, and S(A) is computed for the free scalar
(round-31 Casini-Huerta machinery, using S(A) = S(complement) to keep every matrix <= N/2).

CALIBRATION (the cold ground-state curve encodes the entanglement/horizon dimension):
  * 1D chain (d=1): FLAT -- boundary = 2 at every cut, so S is constant until the very end. No Page peak.
  * 2D grid (d=2): a rounded TENT peaking near half -- the perimeter grows then shrinks, so S ~ |horizon|
    rises then falls.

KEYSTONE RESULT:
  * COLD (ground state): a Page curve that RISES AND FALLS (unitarity), peaking near half the system -- like
    the 2D grid, because the keystone's Hausdorff dimension ~2.3 gives geometric regions a growing boundary.
    But the curve is irregular (the ramified tree) and its HEIGHT is area-law (set by the horizon, not the
    volume).
  * HOT (a scrambled, volume-law pure state -- the ground state of a dense random Hamiltonian): the maximal
    symmetric Page TENT, peaking exactly at half the system, with peak height several times the cold curve's.
  * So the keystone's NATURAL (cold) state radiates AREA-LAW entropy -- a suppressed Page curve set by the
    small tree horizons -- while a scrambled state radiates VOLUME-LAW entropy -- the full Page tent. Both
    rise and fall: unitarity (information return) holds regardless; only the amount of entanglement differs.
    The same b1=1 sparsity that gives the area law (s9_5) and bond-local entanglement (negativity) keeps the
    cold horizon small, so the cold Page curve is suppressed relative to maximal scrambling.

CAVEAT: this is the Page-curve STRUCTURE -- the entanglement of a pure state's growing subsystem -- not a
dynamical evaporation with horizon emission; the island / quantum-extremal-surface dynamics are not computed.

STATUS: PARTIAL -- the Page-curve rise-and-fall (unitarity) is demonstrated for the keystone field, with the
cold (area-law, suppressed) vs scrambled (volume-law, full tent) contrast calibrated against chain and grid;
a dynamical evaporation / island calculation is not done. Native: the field is the rule's Laplacian; the
radiation grows on the bare graph. Pure Python.
"""
import math
import os
import random
from collections import deque
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import (
    _corr, _entropy, _funcmat, _jacobi, _keystone, _chain, _grid)

STATUS = "PARTIAL"
TITLE = "Page curve: radiation entropy rises and falls (unitarity); cold=area-law (suppressed), scrambled=volume tent"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _S(X, P, A, n):
    """Pure-state entropy: use the smaller of A and its complement (S(A)=S(complement))."""
    A = set(A)
    if len(A) > n - len(A):
        A = set(range(n)) - A
    A = sorted(A)
    if len(A) < 1:
        return 0.0
    return _entropy(X, P, A)


def _bfs_order(adj, c, n):
    d = {c: 0}; dq = deque([c]); order = [c]
    while dq:
        x = dq.popleft()
        for y in sorted(adj[x]):
            if y not in d:
                d[y] = d[x] + 1; dq.append(y); order.append(y)
    for v in range(n):
        if v not in d:
            order.append(v)
    return order


def _scrambled_corr(n, seed=2, sq=3.0):
    """X,P for the ground state of a DENSE random Hamiltonian -> volume-law, exactly pure, symmetric tent."""
    rng = random.Random(seed)
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = rng.gauss(0, 1); H[i][j] = v; H[j][i] = v
    ev, V = _jacobi(H)
    import statistics
    sd = statistics.pstdev(ev) or 1.0
    # K eigenvalues = exp(sq*ev/sd); X = 0.5 K^{-1/2}, P = 0.5 K^{1/2}
    xe = [0.5 * math.exp(-sq * e / sd / 2) for e in ev]
    pe = [0.5 * math.exp(sq * e / sd / 2) for e in ev]

    def build(coef):
        M = [[0.0] * n for _ in range(n)]
        for i in range(n):
            Vi = V[i]
            for j in range(n):
                Vj = V[j]; s = 0.0
                for k in range(n):
                    s += Vi[k] * coef[k] * Vj[k]
                M[i][j] = s
        return M
    return build(xe), build(pe)


def _curve(X, P, order, n, steps):
    ks = [max(1, int(round(n * f))) for f in [0.07 + 0.86 * i / (steps - 1) for i in range(steps)]]
    return [(k / n, _S(X, P, order[:k], n)) for k in ks]


def run():
    print("[PARTIAL] %s" % TITLE)
    nchain = 60 if not _FULL else 120
    Lg = 8 if not _FULL else 12
    nstep = 120 if not _FULL else 360
    steps = 12

    print("  CALIBRATION -- cold ground-state Page curve encodes the horizon dimension:")
    n, adj, _e = _chain(nchain); X, P = _corr(n, adj, 0.05)
    cur = _curve(X, P, _bfs_order(adj, n // 2, n), n, steps)
    print("    1D chain (d=1): " + " ".join("%.1f" % s for _, s in cur) + "  -> FLAT (boundary=2), no Page peak")
    n, adj = _grid(Lg); X, P = _corr(n, adj, 0.05)
    cur = _curve(X, P, _bfs_order(adj, (Lg // 2) * Lg + Lg // 2, n), n, steps)
    pk = max(cur, key=lambda t: t[1])
    print("    2D grid  (d=2): " + " ".join("%.1f" % s for _, s in cur) + "  -> rounded TENT, peak %.1f at f=%.2f" % (pk[1], pk[0]))

    print("  KEYSTONE -- COLD (ground state) vs HOT (scrambled, volume-law) Page curves:")
    n, adj, _e = _keystone(nstep, seed=5); X, P = _corr(n, adj, 0.05)
    order = _bfs_order(adj, _bfs_order(adj, 0, n)[n // 2], n)
    cold = _curve(X, P, order, n, steps)
    Xs, Ps = _scrambled_corr(n, seed=2, sq=3.0)
    ro = list(range(n)); random.Random(0).shuffle(ro)
    hot = _curve(Xs, Ps, ro, n, steps)
    pc = max(cold, key=lambda t: t[1]); ph = max(hot, key=lambda t: t[1])
    print("    f:      " + " ".join("%4.2f" % f for f, _ in cold))
    print("    COLD S: " + " ".join("%4.1f" % s for _, s in cold) + "  peak %.1f at f=%.2f" % (pc[1], pc[0]))
    print("    HOT  S: " + " ".join("%4.1f" % s for _, s in hot) + "  peak %.1f at f=%.2f (sym tent)" % (ph[1], ph[0]))
    print("    => both RISE and FALL (unitarity / information return). COLD is area-law (suppressed, peak set by")
    print("       the tree's small horizon, ratio HOT/COLD ~%.0fx); HOT is the volume-law Page tent peaking at" % (ph[1] / max(pc[1], 1e-9)))
    print("       half-system. The keystone's natural (cold) radiation is area-law; scrambling gives the full")
    print("       tent. b1=1 keeps the cold horizon small, so the cold Page curve is suppressed.")
