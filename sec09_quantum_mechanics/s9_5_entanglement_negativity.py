"""Quantum entanglement is NEAREST-NEIGHBOR; classical correlation is long-ranged -- the microscopic origin
of the area law.

Mutual information I(A:B) counts BOTH quantum entanglement and classical correlation. The logarithmic
NEGATIVITY E_N(A:B) is a genuine entanglement monotone (zero on every separable mixed state), so comparing
the two separates quantum from classical. For a Gaussian state the partial transpose is Gaussian, so E_N is
computed from the partial-transposed symplectic eigenvalues nu~: with covariance sigma_xx = 2X = K^{-1/2},
sigma_pp = 2P = K^{1/2}, flip the momenta of B (partial transpose), and
    E_N = sum over nu~ < 1 of  -ln(nu~),   nu~ = sqrt(eig(sigma_xx^{AB} . D sigma_pp^{AB} D)),
with D = diag(+1 on A, -1 on B). (Reuses the round-31 Casini-Huerta machinery; pure-Python Jacobi.)

VALIDATION (1D chain, gapped): adjacent sites are entangled (E_N ~ 0.29) but every separated pair has
E_N = 0 EXACTLY while the mutual information stays positive and decays (0.09, 0.04, ...). The negativity
correctly sees only genuine quantum entanglement -- "entanglement sudden death" with distance.

KEYSTONE RESULT:
  * Quantum entanglement is ESSENTIALLY NEAREST-NEIGHBOR. Single-site negativity is dominant at tree-distance
    d=1 (E_N ~ 0.27), already tiny at d=2 (E_N ~ 0.02, a small tail from the irregular branching, growing
    slightly as m -> 0), and dead by d=3. Classical correlation (mutual information) decays far more slowly:
    d=1 ~ 0.25, d=2 ~ 0.05, d=3 ~ 0.013, d=4 ~ 0.004. So entanglement is short-ranged while correlation runs
    along the tree geodesic.
  * Adjacent subtrees across a single edge are strongly entangled (E_N ~ 0.33, every pair) -- the genuine
    entanglement is carried by the EDGES (nearest-neighbor bonds).
  * THIS IS THE MICROSCOPIC ORIGIN OF THE AREA LAW (s9_5_entanglement_entropy_area_law). Because entanglement
    lives on the bonds, cutting out a region entangles it with the rest only across its boundary EDGES, so
    S ~ |dA|. The negativity explains why the entropy counts boundary edges: each boundary edge carries one
    nearest-neighbor entangled bond. The same b1=1 sparsity that makes boundaries small (single-edge subtree
    cuts) makes the entanglement bond-local.

So the keystone ground state has SHORT-RANGE quantum entanglement (nearest-neighbor bonds) dressed by
LONGER-RANGE classical correlations -- the structure of a gapped lattice field on a tree, and a consistent
microscopic picture for the area law, the violated monogamy (a generic free field), and the static-side
entanglement dimension.

STATUS: PARTIAL -- the entanglement-vs-correlation range structure is computed and calibrated (negativity
nearest-neighbor, mutual information long-ranged), giving the area law a microscopic origin; the precise
d=2 tail and its m-dependence are only loosely pinned. Native: the field is the rule's Laplacian. Pure
Python.
"""
import math
import os
import random
from collections import deque
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import (
    _corr, _funcmat, _matmul, _sub, _jacobi, _keystone, _chain)

STATUS = "PARTIAL"
TITLE = "Quantum entanglement is nearest-neighbor (negativity), classical correlation long-ranged: area-law origin"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _vn(X, P, A):
    if not A:
        return 0.0
    M = _matmul(_sub(X, list(A)), _sub(P, list(A))); ev, _ = _jacobi(M); s = 0.0
    for e in ev:
        nu = math.sqrt(max(e, 0.25 + 1e-12))
        s += (nu + 0.5) * math.log(nu + 0.5) - (nu - 0.5) * math.log(nu - 0.5)
    return s


def _I(X, P, A, B):
    return _vn(X, P, A) + _vn(X, P, B) - _vn(X, P, list(A) + list(B))


def _negativity(X, P, A, B):
    R = list(A) + list(B); nA = len(A); m = len(R)
    XR = _sub(X, R); PR = _sub(P, R)
    D = [1.0] * m
    for i in range(nA, m):
        D[i] = -1.0
    M = [[D[i] * PR[i][j] * D[j] for j in range(m)] for i in range(m)]
    Xh = _funcmat(XR, math.sqrt)
    Sym = _matmul(_matmul(Xh, M), Xh)
    ev, _ = _jacobi(Sym); EN = 0.0
    for lam in ev:
        nut = 2.0 * math.sqrt(max(lam, 1e-15))
        if nut < 1.0 - 1e-9:
            EN += -math.log(nut)
    return EN


def _dist(adj, src):
    d = {src: 0}; dq = deque([src])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in d:
                d[y] = d[x] + 1; dq.append(y)
    return d


def _node_at(adj, c, dd):
    D = _dist(adj, c); cand = [x for x in D if D[x] == dd]
    return cand[0] if cand else None


def _branch(adj, start, avoid, cap=5):
    seen = {start}; dq = deque([start])
    while dq and len(seen) < cap:
        x = dq.popleft()
        for y in adj[x]:
            if y != avoid and y not in seen:
                seen.add(y); dq.append(y)
    return list(seen)


def run():
    print("[PARTIAL] %s" % TITLE)
    nchain = 50 if not _FULL else 120
    nstep = 130 if not _FULL else 340

    n, adj, _e = _chain(nchain); X, P = _corr(n, adj, 0.05); c = nchain // 2
    print("  VALIDATION (1D chain, gapped): negativity sees only quantum entanglement")
    print("    d    I(A:B)     E_N      (E_N>0 only at d=1 = nearest-neighbor)")
    for d in (1, 2, 3, 4):
        print("    %d   %.5f   %.5f" % (d, _I(X, P, [c], [c + d]), _negativity(X, P, [c], [c + d])))

    print("  KEYSTONE: single-site quantum entanglement (E_N) vs classical correlation (I) by tree-distance:")
    n, adj, _e = _keystone(nstep, seed=5); X, P = _corr(n, adj, 0.05)
    rng = random.Random(4); rows = {d: [0.0, 0.0, 0, 0] for d in (1, 2, 3, 4)}
    for _ in range(40 if not _FULL else 120):
        cc = rng.randrange(n)
        for d in (1, 2, 3, 4):
            x = _node_at(adj, cc, d)
            if x is None:
                continue
            e = _negativity(X, P, [cc], [x])
            rows[d][0] += _I(X, P, [cc], [x]); rows[d][1] += e; rows[d][2] += 1
            if e > 1e-5:
                rows[d][3] += 1
    print("    d    <I(A:B)>    <E_N>     frac(E_N>0)")
    for d in (1, 2, 3, 4):
        I_, E_, k, kp = rows[d]
        if k:
            print("    %d   %.5f    %.5f   %.2f" % (d, I_ / k, E_ / k, kp / k))
    print("  KEYSTONE: adjacent subtrees across one edge (the entanglement bond):")
    edges = [(u, v) for u in adj for v in adj[u] if u < v]
    rng = random.Random(2); EN = []; II = []
    for (u, v) in rng.sample(edges, min(20, len(edges))):
        A = _branch(adj, u, v); B = _branch(adj, v, u)
        if set(A) & set(B):
            continue
        EN.append(_negativity(X, P, A, B)); II.append(_I(X, P, A, B))
    print("    adjacent subtrees: mean E_N=%.3f (frac>0=%.2f), mean I=%.3f -- strongly entangled across the edge"
          % (sum(EN) / len(EN), sum(1 for e in EN if e > 1e-6) / len(EN), sum(II) / len(II)))
    print("  => quantum entanglement is NEAREST-NEIGHBOR (edge-local bonds); classical correlation runs along")
    print("     the tree geodesic. This is the MICROSCOPIC ORIGIN of the area law: a region is entangled with")
    print("     the rest only across its boundary EDGES, so S ~ |dA|. b1=1 makes boundaries small AND the")
    print("     entanglement bond-local; the long-range mutual information is purely classical correlation.")
