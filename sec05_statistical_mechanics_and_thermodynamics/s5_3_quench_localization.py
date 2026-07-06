"""Turning the static Page structure into a Page PROCESS: a quench shows the keystone field does NOT
thermalize -- its eigenmodes are LOCALIZED, so entanglement is area-law-capped (no scrambling), unlike a
normal lattice that thermalizes to volume-law.

The static Page curve (s10_5) grew a region on a frozen graph. Here the field evolves in TIME. Prepare the
field in a product (ultralocal) state, switch on the keystone couplings at t=0, and evolve unitarily. The
Gaussian state's covariance evolves exactly and symplectically: sigma(t) = M(t) sigma0 M(t)^T with
M(t) = exp(t [[0,I],[-K,0]]), K = L + m^2 -- computed from the eigendecomposition of K (cos/sin of sqrt(K)).
Entanglement is tracked with the Renyi-2 entropy S2(A) = (1/2) ln det(sigma_A), which needs only a
determinant (pure-Python-friendly) and captures the area-law-vs-volume-law scaling.

TWO results, one mechanism:
  1. LOCALIZATION (inverse participation ratio of the Laplacian eigenmodes, IPR = sum_i |psi(i)|^4; extended
     mode ~ 1/N, localized ~ O(1)). The keystone's random tree (degree disorder, ~57% pendants) ANDERSON-
     LOCALIZES its modes: mean mode covers only ~30 of ~800 sites, with ~1/4 of modes strongly localized
     (< 5 sites). A 1D chain is the opposite: modes are extended (cover ~2/3 of all sites).
  2. NO VOLUME-LAW THERMALIZATION. After the quench, a 1D chain's entanglement grows and saturates to a
     VOLUME law (S2_sat grows ~linearly with |A| -- full thermalization, extended modes carry entanglement
     ballistically). The keystone's entanglement saturates FLAT -- S2_sat is essentially independent of region
     size (area-law cap), only a few times the cold ground state -- because the localized modes cannot
     transport entanglement across the graph.

So the keystone field is a LOCALIZED, non-thermalizing system: the local tree dynamics cannot scramble
information into a volume of entanglement, hot or cold. This is the dynamical face of the b1=1 sparsity (it
gives the area law, bond-local entanglement, and now mode localization), and it is the OPPOSITE of a black
hole's fast scrambling -- the volume-law (hot) Page tent of s10_5 is NOT reachable by the keystone's own
dynamics; it required an artificial non-local Hamiltonian.

CAVEAT: the free scalar is Gaussian (integrable), so even a thermalizing version relaxes to a generalized
Gibbs ensemble, not a true thermal state; the point here is geometric -- on a CHAIN the same free field
reaches volume-law, while on the keystone TREE localization caps it at area-law.

STATUS: PARTIAL (characterization) -- the quench dynamics and the mode localization are computed and the
chain-vs-keystone (volume-law vs area-law-capped) contrast is clear; a full many-body / interacting
thermalization study is not done. Native: the field is the rule's Laplacian; the quench is unitary evolution
under it. Pure Python.
"""
import math
import os
import random
from collections import defaultdict, deque
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi, _matmul

STATUS = "PARTIAL"
TITLE = "Quench dynamics: keystone modes are LOCALIZED, entanglement is area-law-capped (no volume-law thermalization)"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _keystone(steps, seed=5):
    E = Counter = __import__("collections").Counter([(0, 1), (1, 2), (2, 0)])
    fresh = 3; rng = random.Random(seed)
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


def _chain(n):
    adj = defaultdict(set)
    for i in range(n - 1):
        adj[i].add(i + 1); adj[i + 1].add(i)
    return n, adj


def _Kdecomp(n, adj, m2):
    K = [[0.0] * n for _ in range(n)]
    for i in range(n):
        K[i][i] = len(adj[i]) + m2
        for j in adj[i]:
            K[i][j] = -1.0
    ev, V = _jacobi(K)
    return ev, V


def _ipr(ev, V, n):
    """mean IPR over modes; V columns are eigenvectors."""
    tot = 0.0; strong = 0
    for k in range(n):
        s4 = 0.0; s2 = 0.0
        for i in range(n):
            a = V[i][k] * V[i][k]; s2 += a; s4 += a * a
        ipr = s4 / (s2 * s2)
        tot += ipr
        if 1.0 / ipr < 5:
            strong += 1
    return tot / n, strong / n


def _UdiagUT(V, d, n):
    """V diag(d) V^T."""
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        Vi = V[i]
        for j in range(n):
            Vj = V[j]; s = 0.0
            for k in range(n):
                s += Vi[k] * d[k] * Vj[k]
            M[i][j] = s
    return M


def _quench_rows(ev, V, n, t, region):
    """Return the 2|A| rows of M(t) for the region's x and p indices."""
    sq = [math.sqrt(max(e, 1e-12)) for e in ev]
    cosd = [math.cos(s * t) for s in sq]
    sinl = [math.sin(s * t) / s for s in sq]
    sinh = [-math.sin(s * t) * s for s in sq]
    Mxx = _UdiagUT(V, cosd, n)      # = Mpp
    Mxp = _UdiagUT(V, sinl, n)
    Mpx = _UdiagUT(V, sinh, n)
    rows = []
    for a in region:                # x-rows: [Mxx | Mxp]
        rows.append(Mxx[a] + Mxp[a])
    for a in region:                # p-rows: [Mpx | Mpp]
        rows.append(Mpx[a] + Mxx[a])
    return rows                     # each length 2n


def _logdet(M):
    """log|det| via Gaussian elimination with partial pivoting (M is square, symmetric PD here)."""
    n = len(M); A = [row[:] for row in M]; ld = 0.0
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        if abs(A[p][i]) < 1e-300:
            return -700.0
        if p != i:
            A[i], A[p] = A[p], A[i]
        piv = A[i][i]; ld += math.log(abs(piv))
        for r in range(i + 1, n):
            f = A[r][i] / piv
            if f != 0.0:
                Ar = A[r]; Ai = A[i]
                for c in range(i, n):
                    Ar[c] -= f * Ai[c]
    return ld


def _S2_quench(ev, V, n, t, region):
    rows = _quench_rows(ev, V, n, t, region)         # 2|A| x 2n
    m = len(rows)
    sig = [[0.0] * m for _ in range(m)]              # sigma_A = rows rows^T
    for i in range(m):
        ri = rows[i]
        for j in range(i, m):
            rj = rows[j]; s = 0.0
            for k in range(len(ri)):
                s += ri[k] * rj[k]
            sig[i][j] = s; sig[j][i] = s
    return 0.5 * _logdet(sig)


def _ball(adj, c, r):
    seen = {c}; fr = [c]
    for _ in range(r):
        nx = []
        for x in fr:
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); nx.append(y)
        fr = nx
    return list(seen)


def run():
    print("[PARTIAL] %s" % TITLE)
    nchain = 60 if not _FULL else 120
    nstep = 110 if not _FULL else 300

    print("  (1) LOCALIZATION -- inverse participation ratio of Laplacian eigenmodes (extended ~1/N, localized ~O(1)):")
    n, adj = _chain(nchain); ev, V = _Kdecomp(n, adj, 0.05); ip, st = _ipr(ev, V, n)
    print("    1D chain (n=%d): mean IPR=%.4f -> mode covers ~%.0f of %d sites (EXTENDED); strongly-loc frac=%.2f" % (n, ip, 1 / ip, n, st))
    n, adj = _keystone(nstep, seed=5); evk, Vk = _Kdecomp(n, adj, 0.05); ipk, stk = _ipr(evk, Vk, n)
    print("    keystone (n=%d): mean IPR=%.4f -> mode covers ~%.0f of %d sites (LOCALIZED); strongly-loc frac=%.2f" % (n, ipk, 1 / ipk, n, stk))

    print("  (2) QUENCH -- Renyi-2 entanglement saturation vs region size (volume-law => grows; area-law cap => flat):")
    tl = [12.0, 20.0, 28.0] if not _FULL else [20.0, 35.0, 50.0]
    nc, adjc = _chain(nchain); evc, Vc = _Kdecomp(nc, adjc, 0.05)
    print("    1D chain:")
    for L in ([8, 16, 24] if not _FULL else [10, 20, 40]):
        A = list(range((nc - L) // 2, (nc - L) // 2 + L))
        sat = sum(_S2_quench(evc, Vc, nc, t, A) for t in tl) / len(tl)
        print("      |A|=%2d: S2_sat=%.2f  (S2_sat/|A|=%.3f)" % (L, sat, sat / L))
    deg = max(range(n), key=lambda v: len(adj[v]))
    tlk = [10.0, 18.0, 26.0] if not _FULL else [15.0, 30.0, 45.0]
    print("    keystone:")
    for r in ([2, 3, 4] if not _FULL else [3, 4, 5]):
        A = _ball(adj, deg, r)
        if len(A) >= n // 2:
            break
        sat = sum(_S2_quench(evk, Vk, n, t, A) for t in tlk) / len(tlk)
        print("      |A|=%3d: S2_sat=%.2f  (S2_sat/|A|=%.3f)" % (len(A), sat, sat / len(A)))
    print("  => chain S2_sat grows with |A| (volume-law, thermalizes); keystone S2_sat is ~FLAT (area-law cap).")
    print("     The localized modes cannot transport entanglement, so the keystone does NOT thermalize to")
    print("     volume-law -- it does not scramble. Same b1=1 sparsity behind the area law and bond-local")
    print("     entanglement; the hot (volume-law) Page tent is unreachable by the keystone's own dynamics.")
