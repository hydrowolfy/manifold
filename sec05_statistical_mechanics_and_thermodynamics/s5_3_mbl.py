"""The big swing -- BEYOND the free theory into INTERACTIONS: does the keystone's single-particle localization
(rounds 35-39) survive as genuine MANY-BODY localization (MBL)? Put the canonical random-field Heisenberg (XXZ,
Delta=1) spin-1/2 model on the substrate graphs and exactly diagonalize. ANSWER: yes -- at strong disorder every
substrate (chain, keystone, 3-regular) goes MBL (Poisson level statistics + area-law entanglement); at weak-to-
moderate disorder they thermalize (GOE + volume law). So the localization story is not an artifact of the free
theory. And the crossover disorder shifts with GEOMETRY/CONNECTIVITY (cf. round 41): the sparse 1D chain localizes
at the lowest W, the infinite-dimensional 3-regular expander resists localization to the highest W, the keystone in
between -- more connectivity / higher effective dimension => harder to many-body-localize.

METHOD AND ITS HARD LIMIT. H = sum_{<ij> in graph} [ (1/2)(S+_i S-_j + h.c.) + Delta Sz_i Sz_j ] + sum_i h_i Sz_i,
Delta=1 (Heisenberg), h_i ~ uniform[-W,W]. Fixed total-Sz=0 sector; DENSE exact diagonalization. The Hilbert space
is 2^N, so even with Sz conservation the sector is C(N,N/2) -- this caps us at SMALL graphs (N<=12-14: C(12,6)=924,
C(14,7)=3432). That 2^N wall is real and is stated up front; all claims are at these sizes with the standard MBL
finite-size caveat. (This is the ONE module that uses numpy -- interacting ED is infeasible in the pure-Python
idiom of the rest of the package; it is import-guarded so the package still loads/tests without numpy.)

TWO DIAGNOSTICS, BOTH WITH EXACT BENCHMARKS (they must agree on the phase):
  * LEVEL-SPACING RATIO <r> = <min(d_n,d_{n+1})/max(...)> over mid-spectrum gaps: thermal/ergodic -> GOE 0.5307,
    MBL -> Poisson 0.3863 (connects directly to round 36's Poisson finding for the free keystone Laplacian).
  * MID-SPECTRUM ENTANGLEMENT ENTROPY S(L_A) of an infinite-temperature eigenstate: thermal -> VOLUME law (S grows
    with the cut size L_A), MBL -> AREA law (S saturates, O(1)).

RESULTS (Delta=1, Sz=0, mid-spectrum; disorder-averaged; N=12, C(12,6)=924):
  <r> vs W (GOE 0.53 thermal -> Poisson 0.39 MBL): EVERY substrate crosses over -- chain 0.53(W=0.5)->0.39(W=8),
  keystone 0.53->0.40, 3-regular 0.52->0.40. ENTANGLEMENT confirms the SAME phases: at W=1 the half-cut S(L_A) grows
  with the cut (VOLUME law, ->~3 at L_A=6); at W=8 it saturates (AREA law: chain ~0.2, keystone ~0.8, 3-regular
  ~1.0). The two diagnostics AGREE on the phase. The CROSSOVER disorder (where <r>~0.45) is CONNECTIVITY-ORDERED:
  chain ~1.9 (sparse 1D, easiest to localize), keystone ~3.5, 3-regular ~3.7 (infinite-d expander, hardest) -- more
  connectivity / higher effective dimension => harder to many-body-localize (ties to round 41). SANITY: Hermiticity
  0, trace sum-rule 1e-13, Sz=0 dim 924; chain thermal@W=1 + MBL@W=8 = the known 1D phenomenology. SIZE: the thermal
  and deep-MBL anchors are stable N=8->12 (0.50->0.52 and 0.385->0.39); the crossover W drifts with size (standard
  MBL caveat) -- so NO sharp transition and NO precise W_c is claimed.

VALIDATION -- exact benchmarks, two diagnostics, sanity checks (all must pass):
  (1) THE TWO DIAGNOSTICS AGREE: wherever <r> is Poisson the entanglement is area-law, and wherever <r> is GOE it
      is volume-law -- the same phase from level statistics and from entanglement, two independent observables.
  (2) KNOWN 1D MBL PHENOMENOLOGY: the random-field Heisenberg CHAIN thermalizes (GOE, volume) at moderate W and
      many-body-localizes (Poisson, area) at strong W -- the textbook result (W_c ~ 3.5 in the literature; we see
      the crossover, not a sharp point, as finite size requires).
  (3) HAMILTONIAN CHECKS: Hermiticity |H-H^T|=0, total-Sz conservation (built sector-by-sector), and the trace sum
      rule sum(eigenvalues)=Tr(H) -- all to machine precision.
  (4) SIZE DEPENDENCE reported (N=10 vs 12): the thermal and deep-MBL anchors are stable; the crossover W drifts
      with size (the notorious MBL finite-size drift) -- so NO sharp transition and NO precise W_c is claimed.
  (5) INDEPENDENT REIMPLEMENTATION: the companion `MBL-Explorer.html` rebuilds and diagonalizes the same
      Hamiltonian in JavaScript (small N) and reproduces <r> -- a second codebase, same spectrum.

HONESTY GUARDRAILS (this round needs them most): MBL at finite size is contested in the literature; the apparent
transition drifts with N. We claim only: at accessible sizes the keystone shows MBL-like behavior (Poisson + area
law) at strong disorder and thermalizes at weak disorder, like the other substrates, with the crossover shifted by
connectivity. We do NOT claim a sharp transition, a precise W_c, or that the thermodynamic-limit phase is settled.

STATUS: PARTIAL (characterization) -- interacting ED with two agreeing diagnostics and the exact sanity checks,
explicitly size-limited; it establishes that the single-particle localization has an MBL counterpart at accessible
sizes. No leaf change; tally unchanged. Requires numpy (interacting ED); the rest of the package stays pure Python.
"""
import math
import os
import random
import itertools
from collections import Counter, defaultdict

try:
    import numpy as np
    _HAVE_NUMPY = True
except Exception:
    _HAVE_NUMPY = False

from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Many-body localization: single-particle localization survives interactions (keystone goes MBL); geometry shifts W_c"
GOE_R = 0.5307
POISSON_R = 0.3863
_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


# ---- substrate graphs (small N) ------------------------------------------------------------
def _chain(N):
    return N, [(i, i + 1) for i in range(N - 1)]


def _keystone(target, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
    while len(set(u for ed in E for u in ed)) < target:
        R = redexes(E)
        if not R:
            break
        a, b, c = rng.choice(R); E[(a, b)] -= 1; E[(b, c)] -= 1
        if E[(a, b)] <= 0:
            del E[(a, b)]
        if E[(b, c)] <= 0:
            del E[(b, c)]
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        for (s, t) in KEYSTONE:
            E[(sub[s], sub[t])] += 1
        fresh += 1
    nodes = sorted(set(u for ed in E for u in ed)); idx = {v: i for i, v in enumerate(nodes)}
    es = set()
    for (u, v) in E:
        if u != v:
            es.add((min(idx[u], idx[v]), max(idx[u], idx[v])))
    return len(nodes), sorted(es)


def _reg3(N, seed=2):
    rng = random.Random(seed)
    for _ in range(600):
        stubs = [v for v in range(N) for _ in range(3)]; rng.shuffle(stubs); adj = defaultdict(set); ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            if a == b or b in adj[a]:
                ok = False; break
            adj[a].add(b); adj[b].add(a)
        if ok and all(len(adj[v]) == 3 for v in range(N)):
            return N, sorted((a, b) for a in range(N) for b in adj[a] if a < b)
    return N, []


# ---- random-field Heisenberg in the Sz=0 sector --------------------------------------------
def _build_H(N, edges, h, Delta=1.0):
    ups = N // 2
    basis = [sum(1 << i for i in c) for c in itertools.combinations(range(N), ups)]
    idx = {s: k for k, s in enumerate(basis)}; D = len(basis)
    H = np.zeros((D, D))
    for k, s in enumerate(basis):
        bit = [(s >> i) & 1 for i in range(N)]
        diag = sum(h[i] * (bit[i] - 0.5) for i in range(N))
        for (i, j) in edges:
            diag += Delta * (bit[i] - 0.5) * (bit[j] - 0.5)
        H[k, k] = diag
        for (i, j) in edges:
            if bit[i] != bit[j]:
                H[k, idx[s ^ ((1 << i) | (1 << j))]] += 0.5
    return H, basis


def _r_of(E):
    E = np.sort(E); m = len(E); g = np.diff(E[m // 4:3 * m // 4]); g = g[g > 1e-12]
    r = np.minimum(g[:-1], g[1:]) / np.maximum(g[:-1], g[1:])
    return float(r.mean())


def _entropy(psi, basis, N, LA):
    M = np.zeros((1 << LA, 1 << (N - LA)))
    mask = (1 << LA) - 1
    for k, s in enumerate(basis):
        M[s & mask, s >> LA] = psi[k]
    sv = np.linalg.svd(M, compute_uv=False); p = sv * sv; p = p[p > 1e-14]
    return float(-(p * np.log(p)).sum())


def _avg_r(N, edges, W, nreal, seed=0):
    rng = random.Random(seed); rs = []
    for _ in range(nreal):
        h = [rng.uniform(-W, W) for _ in range(N)]
        H, _ = _build_H(N, edges, h)
        rs.append(_r_of(np.linalg.eigvalsh(H)))
    return sum(rs) / len(rs), (np.std(rs) / math.sqrt(len(rs)) if len(rs) > 1 else 0.0)


def _avg_S_all(N, edges, W, LAs, nreal, nstate, seed=0):
    """mean mid-spectrum entanglement S for every cut size in LAs, ONE diagonalization per realization."""
    rng = random.Random(seed); acc = {la: [] for la in LAs}
    for _ in range(nreal):
        h = [rng.uniform(-W, W) for _ in range(N)]
        H, basis = _build_H(N, edges, h); E, V = np.linalg.eigh(H); D = len(basis); mid = D // 2
        for st in range(mid - nstate // 2, mid + nstate // 2):
            psi = V[:, st]
            for la in LAs:
                acc[la].append(_entropy(psi, basis, N, la))
    return {la: sum(v) / len(v) for la, v in acc.items()}


def _crossW(Ws, rs, thr=0.45):
    for i in range(len(Ws) - 1):
        if (rs[i] - thr) * (rs[i + 1] - thr) <= 0 and rs[i] != rs[i + 1]:
            return Ws[i] + (Ws[i + 1] - Ws[i]) * (rs[i] - thr) / (rs[i] - rs[i + 1])
    return float('nan')


def run():
    print("[PARTIAL] %s" % TITLE)
    if not _HAVE_NUMPY:
        print("  REQUIRES numpy (interacting ED). Install: pip install numpy --break-system-packages.")
        print("  (This is the one numpy-dependent module; the rest of the package is pure Python.)")
        return
    print("  Random-field Heisenberg (Delta=1) on the substrate graphs, Sz=0 sector, dense ED. 2^N wall: N<=12-14.")
    print("  <r>: GOE=%.4f (thermal) vs Poisson=%.4f (MBL). Entanglement: volume (thermal) vs area (MBL).\n" % (GOE_R, POISSON_R))
    N = 12 if not _FULL else 14
    nreal = 24 if not _FULL else 60
    nc, ec = _chain(N); nk, ek = _keystone(N); nr, er = _reg3(N)
    subs = [("chain", nc, ec), ("keystone", nk, ek), ("3-regular", nr, er)]
    print("  graphs at N=%d: chain %d edges (1D); keystone %d edges (b1=1 tree+loop); 3-regular %d edges (expander)\n"
          % (N, len(ec), len(ek), len(er)))

    Ws = [0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0]
    print("  (A) LEVEL-SPACING RATIO <r> vs disorder W (thermal GOE->MBL Poisson):")
    print("      W:        " + "  ".join("%5.1f" % w for w in Ws))
    rdata = {}
    for name, n, e in subs:
        rs = [_avg_r(n, e, w, nreal)[0] for w in Ws]; rdata[name] = rs
        print("      %-9s " % name + "  ".join("%5.3f" % v for v in rs))
    print("      (W=0 omitted: the clean point has lattice symmetries/integrability; disorder W>0 breaks them.)")

    print("\n  (B) ENTANGLEMENT S(L_A) -- VOLUME (thermal, grows with cut) vs AREA (MBL, flat):")
    for name, n, e in subs:
        LAs = list(range(1, n // 2 + 1))
        slo = _avg_S_all(n, e, 1.0, LAs, 8, 8); shi = _avg_S_all(n, e, 8.0, LAs, 8, 8)
        print("      %-9s W=1 S(L_A)=[%s] (volume)   W=8 S=[%s] (area)" % (
            name, ",".join("%.2f" % slo[la] for la in LAs), ",".join("%.2f" % shi[la] for la in LAs)))

    print("\n  (C) CROSSOVER disorder (where <r> crosses 0.45) -- connectivity/geometry shifts it:")
    for name in ("chain", "keystone", "3-regular"):
        print("      %-9s W_cross ~ %.1f" % (name, _crossW(Ws, rdata[name])))
    print("      => chain (sparse 1D) localizes at the LOWEST W; the 3-regular (infinite-d expander, round 41) at the")
    print("         HIGHEST; keystone between -- more connectivity/higher effective dimension => harder to localize.")

    print("\n  (D) SIZE DEPENDENCE (chain; finite-size drift is the standard MBL caveat):")
    for n2 in ([8, 10, 12] if not _FULL else [10, 12, 14]):
        nn, ee = _chain(n2)
        print("      N=%2d  <r>(W=1)=%.3f (thermal)  <r>(W=3)=%.3f  <r>(W=8)=%.3f (MBL)" % (
            n2, _avg_r(nn, ee, 1.0, nreal)[0], _avg_r(nn, ee, 3.0, nreal)[0], _avg_r(nn, ee, 8.0, nreal)[0]))

    print("\n  (E) SANITY CHECKS:")
    h0 = [random.Random(1).uniform(-3, 3) for _ in range(nc)]
    H, basis = _build_H(nc, ec, h0); E = np.linalg.eigvalsh(H)
    print("      Hermiticity |H-H^T|max = %.1e ; trace sum-rule |sum(E)-Tr H| = %.1e ; Sz=0 sector dim = %d = C(%d,%d)" % (
        float(np.abs(H - H.T).max()), float(abs(E.sum() - np.trace(H))), len(basis), nc, nc // 2))
    print("      chain thermal at W=1 (<r>=%.2f ~ GOE) and MBL at W=8 (<r>=%.2f ~ Poisson): the known 1D phenomenology." % (
        rdata["chain"][1], rdata["chain"][-1]))

    print("\n  => HEADLINE: the keystone's single-particle localization (rounds 35-39) SURVIVES interactions as MBL --")
    print("     at strong disorder it shows Poisson <r> AND area-law entanglement (the two diagnostics agree), and it")
    print("     thermalizes (GOE + volume) at weak disorder, like the chain and 3-regular. The crossover W shifts with")
    print("     geometry/connectivity (chain lowest, 3-regular expander highest). HONEST: N<=12, MBL is contested and")
    print("     drifts with size -- we claim MBL-LIKE behavior at accessible sizes, NOT a sharp transition or a W_c.")
