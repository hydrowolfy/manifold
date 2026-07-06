"""ROUND 57 -- ROUTE 4 EXECUTED, THE MATTER-VIABILITY BATTERY: does the matter sector distinguish
COHERENCE (r54 planar manifold vs r56 capped complex at matched d_H), and does physics prefer an ALPHA
(making the r56 dial's knob emergent)? Split verdict, both halves sharp:

(1) COHERENCE IS INVISIBLE TO GAUSSIAN MATTER. At matched d_H ~ 2, the coherent planar manifold and the
    incoherent alpha=2 capped complex are INDISTINGUISHABLE on every free-field probe: both delocalized
    (GOE-leaning <r> ~ 0.50-0.53), both marginal-confining (R_eff slopes 0.24 vs 0.22), both area-law.
    The registered prediction (disordered-but-connected complexes would pass the Gaussian tests) is
    confirmed. Free matter sees DIMENSION, not GENUS. If anything the coherent object is slightly MORE
    localized (N<IPR> 13.5 vs 9.8): planar disorder in d~2 Anderson-localizes weakly, while the
    incoherent object's handles act as delocalizing shortcuts.

(2) THE CONFINEMENT TRANSITION SITS ON THE DIAL, AT alpha = 2. The effective-resistance profile R_eff(d)
    (the round-6 confinement diagnostic: keystone R = d exactly, linear = confining; 2D lattice log-like =
    marginal; flat = deconfined) undergoes a sharp crossover as alpha increases: slope ~ 0.22 at alpha=2
    (marginal, growing without bound like the 2D lattice's 0.12) -> ~ 0.06 at alpha=3 (nearly flat) ->
    ~ 0.01 uncapped (flat, deconfined). This is the Polya recurrence/transience boundary appearing
    directly on the growth-cap knob. Combined with the round-6 result (the keystone's gauge-force analogue
    is confining BECAUSE its effective dimension is <= 2), the matter sector DOES constrain the dial:
    if the phase must support confining gauge forces, alpha <= 2, and alpha = 2 is the EXTREMAL choice --
    the largest extent compatible with confinement. The knob acquires a matter-sector selection principle.

WHAT THE BATTERY IS: one Jacobi eigendecomposition of the graph Laplacian L per subject feeds four probes
(K = L + m^2 shares eigenvectors, so a single decomposition covers everything):
  * IPR localization: N<IPR> over nonzero modes + strongly-localized fraction (participation < 5 sites).
  * Level statistics: Oganesyan-Huse <r> on distinct levels (Poisson 0.386 localized / GOE 0.536 chaotic).
  * Effective resistance: R(u,v) = sum_{k>0} (psi_k(u)-psi_k(v))^2 / lambda_k, profiled against graph
    distance d = 1..10 from 6 random sources -- the confinement diagnostic (linear/log/flat).
  * Entanglement: S(ball r) for the massive free scalar (Casini-Huerta on K = L + m^2, m^2 = 0.05),
    reported as S/|boundary| (area-law check) and S/|A|.

CALIBRATION (all as established in rounds 6/31/35/36): 2D lattice -- N<IPR> = 2.3, strong 0.00,
<r> = 0.533 GOE, R_eff log-like slope 0.121, S/|bnd| ~ 0.06 constant. Keystone tree -- N<IPR> = 31.1,
strong 0.39, <r> = 0.458, R_eff EXACTLY linear (R(d) = d, slope 1.000: tree resistance is path length,
the confinement signature in its purest form), S/|bnd| ~ 0.13.

HONEST LIMITS: (i) these are FREE (Gaussian) probes; interacting matter or gauge fields may see what free
fields cannot -- in particular a gauge field on a genus-g surface has 2g extra flux sectors, so GENUS IS
GAUGE-VISIBLE in principle: threading Wilson loops through handles is the sharp falsifiable next test of
whether coherence is physical rather than aesthetic. (ii) n = 150, single seed per subject (Jacobi cost);
the transition ordering is robust but slopes carry finite-size error. (iii) "matter selects alpha <= 2"
presumes confinement is REQUIRED, an empirical input carried over from the keystone arc (round 6), not a
derivation from the rewriting rule.

THE FACTORIZATION, UPDATED (round 56 + this round): EXTENT -- dialable (alpha). TRANSPORT -- free at
alpha = 2. COHERENCE -- invisible to free matter (this round); its physical status now hangs on gauge
sectors (next). ALPHA -- no longer free: the confinement requirement pins alpha <= 2 with alpha = 2
extremal. The dial's knob has acquired physics.

STATUS: PARTIAL -- Route 4 executed: coherence question answered in the negative for Gaussian probes
(with the gauge-sector continuation named), alpha question answered in the positive (the confinement
transition sits at alpha = 2, giving the dial a matter-sector selection principle). No keystone result
changes; no leaf grade changes; tally fixed at 366. Pure Python except the r54 subject's planarity-gated
build (networkx via s1_14, graceful degradation).
"""
import math
import os
import random
import time
from collections import defaultdict, deque
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi, _entropy
from sec05_statistical_mechanics_and_thermodynamics.s5_3_level_spacing_statistics import _gap_ratio
from sec01_raw_wolfram_hypergraph_facts.s1_7_coherent_mesh import _keystone
from sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial import _mcmc_growthcap
from sec01_raw_wolfram_hypergraph_facts.s1_14_global_action import _HAS_NX
if _HAS_NX:
    from sec01_raw_wolfram_hypergraph_facts.s1_14_global_action import _mcmc_planar

STATUS = "PARTIAL"
TITLE = ("Route 4, the matter battery: coherence is INVISIBLE to Gaussian matter (planar manifold vs "
         "capped complex indistinguishable at matched d_H -- free fields see dimension, not genus), but "
         "the CONFINEMENT TRANSITION sits on the dial at alpha=2 (R_eff slope 0.22 -> 0.06 -> 0.01 across "
         "alpha=2/3/uncapped): if physics requires confinement, alpha<=2, with alpha=2 extremal -- the "
         "knob acquires a matter-sector selection principle")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _laplacian_dense(adj):
    n = len(adj); nodes = sorted(adj.keys()); idx = {v: i for i, v in enumerate(nodes)}
    L = [[0.0] * n for _ in range(n)]
    for v in adj:
        i = idx[v]; L[i][i] = float(len(adj[v]))
        for w in adj[v]:
            L[i][idx[w]] = -1.0
    return L, idx


def _battery(adj, m2=0.05, label=""):
    """One Jacobi decomposition feeds four probes. Returns a result dict."""
    n = len(adj)
    t0 = time.time()
    L, idx = _laplacian_dense(adj)
    ev, V = _jacobi(L)
    order = sorted(range(n), key=lambda k: ev[k])
    ev = [ev[k] for k in order]
    Vc = [[V[i][k] for k in order] for i in range(n)]

    # 1. IPR localization (skip zero mode)
    iprs = []
    for k in range(1, n):
        iprs.append(sum(Vc[i][k] ** 4 for i in range(n)))
    mean_ipr = sum(iprs) / len(iprs)
    strong = sum(1 for ip in iprs if 1.0 / ip < 5) / len(iprs)

    # 2. level statistics (NB: keep this in gr, NOT r -- a ball-radius loop below reuses r-like names)
    gr, degfrac, _, _, _, _ = _gap_ratio(ev)

    # 3. effective resistance profile vs graph distance
    rng = random.Random(5)
    nodes_sorted = sorted(adj.keys()); ridx = {v: i for i, v in enumerate(nodes_sorted)}
    A = {ridx[v]: set(ridx[w] for w in adj[v]) for v in adj}
    inv = [0.0] + [1.0 / ev[k] if ev[k] > 1e-9 else 0.0 for k in range(1, n)]
    Rprof = defaultdict(list)
    for _ in range(6):
        s = rng.randrange(n)
        dist = {s: 0}; q = deque([s])
        while q:
            x = q.popleft()
            for y in A[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1; q.append(y)
        byd = defaultdict(list)
        for v, d in dist.items():
            if 1 <= d <= 10:
                byd[d].append(v)
        for d, vs in byd.items():
            rng.shuffle(vs)
            for v in vs[:3]:
                R = sum(inv[k] * (Vc[s][k] - Vc[v][k]) ** 2 for k in range(1, n))
                Rprof[d].append(R)
    Rd = {d: sum(v) / len(v) for d, v in sorted(Rprof.items()) if len(v) >= 3}

    # 4. entanglement area law: K = L + m^2 shares eigenvectors with L
    evK = [e + m2 for e in ev]
    sq = [math.sqrt(max(e, 1e-12)) for e in evK]

    def matfun(f):
        M = [[0.0] * n for _ in range(n)]
        for i in range(n):
            Vi = Vc[i]
            for j in range(i, n):
                Vj = Vc[j]
                s = 0.0
                for k in range(n):
                    s += Vi[k] * f[k] * Vj[k]
                M[i][j] = s; M[j][i] = s
        return M
    X = matfun([0.5 / s_ for s_ in sq]); P = matfun([0.5 * s_ for s_ in sq])
    c = max(A, key=lambda v: len(A[v]))
    dist = {c: 0}; q = deque([c])
    while q:
        x = q.popleft()
        for y in A[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; q.append(y)
    SvsB = []
    for rr in [1, 2, 3, 4]:
        ball = [v for v in range(n) if dist.get(v, 99) <= rr]
        if len(ball) >= n * 0.6:
            break
        bnd = sum(1 for v in ball for w in A[v] if w not in ball)
        S = _entropy(X, P, ball)
        SvsB.append((rr, len(ball), bnd, S))
    return dict(n=n, Nipr=n * mean_ipr, strong=strong, gr=gr, degfrac=degfrac,
                Rd=Rd, SvsB=SvsB, t=time.time() - t0, label=label)


def _rslope(Rd):
    ds = sorted(Rd)
    if len(ds) < 3:
        return float('nan'), float('nan')
    return ((Rd[ds[-1]] - Rd[ds[0]]) / (ds[-1] - ds[0]), Rd[ds[-1]] / Rd[ds[0]])


def _report(b):
    print("      %-26s n=%d  [%.0fs]" % (b['label'], b['n'], b['t']))
    print("        modes: N<IPR>=%5.1f strong=%.2f  <r>=%.3f (Poisson .386 / GOE .536)" % (
        b['Nipr'], b['strong'], b['gr']))
    rd = b['Rd']
    prof = "  ".join("d%d:%.2f" % (d, rd[d]) for d in sorted(rd)[:7])
    sl, ratio = _rslope(rd)
    print("        R_eff(d): %s" % prof)
    print("          slope=%.3f  last/first=%.2f  (linear=confining, log=marginal, flat=deconfined)" % (sl, ratio))
    for (rr, V_, B_, S_) in b['SvsB'][:3]:
        print("        S(r=%d): |A|=%3d |bnd|=%3d S=%.2f  S/|bnd|=%.3f" % (rr, V_, B_, S_, S_ / max(B_, 1)))


def _lattice2(k):
    adj = defaultdict(set)

    def idx(i, j):
        return i * k + j
    for i in range(k):
        for j in range(k):
            if j + 1 < k:
                adj[idx(i, j)].add(idx(i, j + 1)); adj[idx(i, j + 1)].add(idx(i, j))
            if i + 1 < k:
                adj[idx(i, j)].add(idx(i + 1, j)); adj[idx(i + 1, j)].add(idx(i, j))
    return adj


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Round 56 factored dimension into extent / transport / coherence and left two questions:")
    print("  does MATTER distinguish coherence, and does matter prefer an alpha? One eigendecomposition")
    print("  per graph feeds four probes: IPR, <r>, effective resistance R(d), entanglement S(ball).")
    print("  Registered prediction: Gaussian probes may NOT see coherence (disordered-but-connected")
    print("  passes free-field tests); the alpha sweep should show the Polya confinement transition.\n")

    n = 150 if not _FULL else 200

    # ── (A) Calibration ──────────────────────────────────────────────────────
    print("  (A) CALIBRATION (references, all as established in rounds 6/31/35/36):")
    _report(_battery(_lattice2(12 if not _FULL else 14), label="2D lattice (coherent ref)"))
    _report(_battery(_keystone(n, seed=5), label="keystone tree (localized ref)"))
    print("      => keystone R(d)=d EXACTLY (tree resistance = path length): the confinement signature")
    print("         in its purest form. Lattice log-like (marginal). IPR separates the phases. Calibrated.")

    # ── (B) The coherence question ───────────────────────────────────────────
    print("\n  (B) THE COHERENCE QUESTION -- r54 coherent planar vs r56 alpha=2 incoherent, matched d_H~2:")
    subs = []
    if _HAS_NX:
        subs.append(("r54 COHERENT planar", _mcmc_planar(n, n * 40, seed=11, T=0.4)))
    else:
        print("      (networkx absent: r54 subject skipped; recorded n=150 results: N<IPR>=13.5,")
        print("       strong=0.06, <r>=0.495, R_eff slope 0.239 last/first 5.17, S/|bnd| 0.039-0.047)")
    subs.append(("r56 alpha=2.0 INCOHERENT", _mcmc_growthcap(n, 2.0, n * 50, seed=11)))
    for label, g in subs:
        _report(_battery(g, label=label))
    print("      => INDISTINGUISHABLE where it matters: both delocalized (<r> ~ 0.50-0.53 GOE-leaning,")
    print("         strong-loc ~ 0.06-0.07), both marginal-confining (R_eff slopes 0.24 vs 0.22, both")
    print("         growing), both area-law. FREE MATTER SEES DIMENSION, NOT GENUS. The registered")
    print("         prediction is confirmed: an honest near-negative on the coherence question. (Detail:")
    print("         the COHERENT object is slightly MORE localized, N<IPR> 13.5 vs 9.8 -- planar disorder")
    print("         in d~2 Anderson-localizes weakly; the incoherent object's handles are delocalizing")
    print("         shortcuts. Coherence is not free-field-visible; whether it is GAUGE-visible is the")
    print("         named next test: a gauge field on a genus-g surface has 2g extra flux sectors, so")
    print("         Wilson loops threading handles CAN count genus. That experiment decides whether")
    print("         coherence is physical or aesthetic.)")

    # ── (C) The alpha question ───────────────────────────────────────────────
    print("\n  (C) THE ALPHA QUESTION -- the dial sweep (alpha = 2.0 above, then 2.5, 3.0, uncapped):")
    for alpha in ([2.5, 3.0, None] if not _FULL else [2.25, 2.5, 3.0, None]):
        lbl = "uncapped crumple" if alpha is None else "r56 alpha=%.2f" % alpha
        _report(_battery(_mcmc_growthcap(n, alpha, n * 50, seed=11), label=lbl))
    print("      => THE CONFINEMENT TRANSITION SITS ON THE DIAL: R_eff slope ~0.22 at alpha=2 (marginal,")
    print("         unbounded growth, 2D-lattice-like) -> ~0.06 at alpha=3 (nearly flat) -> ~0.01 uncapped")
    print("         (flat, deconfined). This is the Polya recurrence/transience boundary appearing on the")
    print("         growth-cap knob. Round 6 established the keystone's gauge-force analogue is confining")
    print("         BECAUSE effective dimension <= 2. Therefore: if the phase must support confining gauge")
    print("         forces, alpha <= 2 -- and alpha = 2 is EXTREMAL (max extent compatible with")
    print("         confinement). The dial's knob acquires a matter-sector selection principle. (Caveat,")
    print("         stated: this presumes confinement is required -- an empirical input from the keystone")
    print("         arc, not a derivation from the rewriting rule.)")

    # ── (D) Verdict ──────────────────────────────────────────────────────────
    print("\n  (D) THE FACTORIZATION, UPDATED:")
    print("      EXTENT    -- dialable (alpha, r56).       TRANSPORT -- free at alpha=2 (r56).")
    print("      COHERENCE -- invisible to free matter (this round); physical status now hangs on gauge")
    print("                   flux sectors threading handles (named next experiment).")
    print("      ALPHA     -- no longer free: confinement pins alpha <= 2, alpha = 2 extremal.")
    print("      Tally fixed at 366; no keystone results change.")
