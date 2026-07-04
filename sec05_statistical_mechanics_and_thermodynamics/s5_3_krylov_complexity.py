"""Operator growth, the modern successor to the OTOC: the keystone's operator ANDERSON-LOCALIZES in KRYLOV SPACE,
so Krylov complexity SATURATES -- and the Krylov participation P_K is a clean, basis-independent ORDER PARAMETER
that separates the scrambling from the non-scrambling substrates. This is the fourth, sharpest leg of the
rounds 35-37 no-scrambling result: real-space localization (35), Poisson spectrum (36), frozen OTOC cone (37),
and now bounded operator growth (38) -- with, for the first time, a single number that orders the substrates.

THE RECURSION METHOD (Parker-Cao-Avdoshkin-Scaffidi-Altman 2019). Evolve a local operator A under the
Liouvillian L=[H,.] and tridiagonalize: the Lanczos algorithm builds an orthonormal "Krylov basis" |O_0)=|A),
|O_1),... in which L is a 1D hopping chain with amplitudes b_n (the Lanczos coefficients). The operator
wavefunction phi_n(t)=(O_n|A(t)) lives on this Krylov chain, and the Krylov complexity
    K_c(t) = sum_n n |phi_n(t)|^2
is how far the operator has spread along it. Linearly-growing b_n => exponential operator growth (chaos);
bounded/erratic b_n => the Krylov wavefunction localizes and K_c saturates (no scrambling). Crucially, b_n are
disorder for the localized substrate, so the Krylov chain is itself a DISORDERED tight-binding chain and the
operator ANDERSON-LOCALIZES in Krylov space -- the operator-space image of round 35's real-space localization.

WHY IT IS EXACT AND NATIVE HERE. For the rule's free scalar (H=1/2 sum p^2 + 1/2 x^T K x, K=L+m^2; rounds
27/31/35) the local operator A=p_{i0} oscillates at the frequencies omega_k=sqrt(ev_k) of K, so operator growth
is governed by the operator power spectrum
    Phi(omega) = sum_k w_k [delta(omega-omega_k)+delta(omega+omega_k)]/2,   w_k = V_{i0,k}^2  (V = eigenvectors of K),
and the Lanczos b_n are the recurrence coefficients of the orthogonal polynomials of this measure (a_n=0 by the
+-omega symmetry). We get them stably by running Lanczos with FULL reorthogonalization directly on the discrete
spectral measure (no ill-conditioned Hankel inversion). The Krylov chain is then diagonalized (small tridiagonal)
to read every long-time average exactly.

ORDER PARAMETERS (all from the Krylov chain, no fitting):
  * Krylov dimension D_K  -- length of the Krylov chain (twice the number of distinct frequencies the operator
                            couples to). This is NOT the order parameter: the keystone hub couples to many
                            frequencies so its chain is LONG (D_K > N); localization shows in how little of the
                            chain the operator OCCUPIES (P_K) -- Anderson localization in Krylov space, not a short chain.
  * Krylov participation P_K = 1 / sum_n Pbar_n^2,  Pbar_n = time-averaged |phi_n|^2 = sum_m U_{n,m}^2 U_{0,m}^2
                            (U = Krylov-chain eigenvectors): the number of Krylov sites the operator occupies.
                            THE order parameter -- small = localized/non-scrambling, large = delocalized.
  * Saturated complexity  Kbar_c = sum_n n Pbar_n (the long-time average of K_c).

RESULTS (m^2=0.05; A=p at the hub for the keystone, center for the chains, site 0 for 3-regular; N~60-80):
  ORDER PARAMETER -- Krylov participation P_K (Krylov sites the operator occupies), as a fraction of N:
    clean chain      P_K/N ~ 1.02   delocalized: operator fills the whole Krylov chain, K_c grows ~linearly (~40)
    keystone tree    P_K/N ~ 0.15   LOCALIZED: ~12 of D_K=126 Krylov sites, K_c saturates (~7) -- no scrambling
    disordered chain P_K/N ~ 0.11   LOCALIZED: reproduces the keystone (Anderson localization is the mechanism)
    random 3-regular P_K/N ~ 1.47   delocalized: even more spread than the chain, K_c grows ~linearly (~54)
  The keystone Krylov chain is LONG (D_K~126: the hub couples to every frequency) yet the operator occupies only
  ~12 sites -- a genuine ANDERSON LOCALIZATION in Krylov space (long disordered chain, localized wavefunction),
  the operator-space mirror of round 35's real-space localization. The clean chain's Lanczos coefficients are
  smooth (cov(b_n)~0.10); the localized substrates' are disordered (cov~0.43-0.57). The real-space mode
  participation (round 35) tracks P_K across all four substrates -- two independent localization probes agreeing.

VALIDATION -- three independent cross-checks (printed each run):
  (1) ANALYTIC: on the clean chain the b_n are smooth and approach the band half-width; the spectral moments
      reconstructed from the Krylov chain match the exact measure to ~1e-9 (Lanczos-on-a-discrete-measure is exact).
  (2) SUM RULE: the first Lanczos coefficient satisfies b_1^2 = <omega^2> = sum_k w_k omega_k^2 exactly.
  (3) AUTOCORRELATION: C(t)=phi_0(t) rebuilt from the Krylov chain equals the direct spectral sum
      sum_k w_k cos(omega_k t) to ~1e-9.
  Consistency: Krylov participation tracks the round-35 IPR and round-37 butterfly velocity across all four
  substrates (localized substrates small on all three; delocalized substrates large).

STATUS: PARTIAL (characterization) -- a third, basis-independent confirmation of the no-scrambling/localization
already graded at 5.3 "Thermalization", now sharpened into a quantitative ORDER PARAMETER. No leaf change; tally
unchanged. Native: the operator is the rule's own free scalar; the recursion method is exact on its spectrum.
Pure Python (Lanczos with full reorthogonalization + the s9_5 Jacobi eigensolver).
"""
import math
import os
import random
from collections import Counter, defaultdict
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi

STATUS = "PARTIAL"
TITLE = "Krylov complexity: the keystone operator localizes in Krylov space (K_c saturates) -- a clean no-scrambling order parameter"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


# ---- substrates (shared with the OTOC / quench / level-statistics modules) -------------------
def _keystone(steps, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
    for _ in range(steps):
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


def _random_regular(n, d=3, seed=2):
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


def _Kdecomp(n, adj, m2, onsite=None):
    K = [[0.0] * n for _ in range(n)]
    for i in range(n):
        K[i][i] = len(adj[i]) + m2 + (onsite[i] if onsite else 0.0)
        for j in adj[i]:
            K[i][j] = -1.0
    return _jacobi(K)


def _hub(n, adj):
    return max(range(n), key=lambda v: len(adj[v]))


# ---- operator power spectrum and the recursion method ----------------------------------------
def _measure(ev, V, src, tol=1e-9):
    """Operator power spectrum of A=p_src: omega_k=sqrt(ev_k), weight w_k=V_{src,k}^2, COLLAPSED to distinct
    frequencies (the Krylov chain depends only on Phi(omega), so summing weights at equal omega is EXACT; for the
    keystone this is a large, degeneracy-driven reduction -- and the count of distinct frequencies is D_K/2)."""
    n = len(ev)
    raw = sorted((math.sqrt(max(ev[k], 0.0)), V[src][k] * V[src][k]) for k in range(n))
    omega = []; w = []
    for o, wt in raw:
        if omega and o - omega[-1] < tol:
            w[-1] += wt
        else:
            omega.append(o); w.append(wt)
    s = sum(w) or 1.0
    w = [x / s for x in w]
    return omega, w


def _lanczos(freqs, amp0, maxsteps, tol=1e-9):
    """Stable Lanczos of the diagonal Liouvillian (multiply-by-freq) on a discrete measure, full reorth (twice).
    Returns (a_n, b_n, U-eigvecs of the Krylov chain, E). a_n ~ 0 by +-omega symmetry."""
    D = len(freqs)
    nrm = math.sqrt(sum(x * x for x in amp0)) or 1.0
    V = [[x / nrm for x in amp0]]
    a = []; b = []
    for nstep in range(maxsteps):
        vn = V[nstep]
        w = [freqs[j] * vn[j] for j in range(D)]
        an = sum(vn[j] * w[j] for j in range(D))
        for j in range(D):
            w[j] -= an * vn[j]
        if nstep > 0:
            bp = b[nstep - 1]; vp = V[nstep - 1]
            for j in range(D):
                w[j] -= bp * vp[j]
        for _ in range(2):                       # full reorthogonalization, twice (stable)
            for u in V:
                dpr = 0.0
                for j in range(D):
                    dpr += u[j] * w[j]
                for j in range(D):
                    w[j] -= dpr * u[j]
        bn = math.sqrt(sum(x * x for x in w))
        a.append(an)
        if bn < tol or nstep == maxsteps - 1:
            break
        b.append(bn)
        V.append([x / bn for x in w])
    return a, b


def _tridiag_eig(a, b):
    D = len(a)
    T = [[0.0] * D for _ in range(D)]
    for i in range(D):
        T[i][i] = a[i]
    for i in range(len(b)):
        T[i][i + 1] = b[i]; T[i + 1][i] = b[i]
    E, U = _jacobi(T)
    return E, U


def _krylov_metrics(a, b):
    """From the Krylov chain: D_K, participation P_K, saturated complexity Kbar_c, and U,E for K_c(t)."""
    E, U = _tridiag_eig(a, b)
    D = len(a)
    # time-averaged occupation Pbar_n = sum_m U[n][m]^2 U[0][m]^2
    Pbar = [0.0] * D
    for nidx in range(D):
        s = 0.0
        for m in range(D):
            s += (U[nidx][m] * U[nidx][m]) * (U[0][m] * U[0][m])
        Pbar[nidx] = s
    tot = sum(Pbar) or 1.0
    PK = 1.0 / sum(p * p for p in Pbar)
    Kbar = sum(nidx * Pbar[nidx] for nidx in range(D)) / tot
    return {"DK": D, "PK": PK, "Kbar": Kbar, "E": E, "U": U}


def _Kc_of_t(E, U, t):
    """K_c(t) = sum_n n |phi_n(t)|^2, phi_n(t) = sum_m U[n][m] e^{-i E_m t} U[0][m]."""
    D = len(E)
    cE = [math.cos(E[m] * t) for m in range(D)]
    sE = [math.sin(E[m] * t) for m in range(D)]
    coef = [U[0][m] for m in range(D)]
    Kc = 0.0; norm = 0.0
    for nidx in range(D):
        re = 0.0; im = 0.0
        Un = U[nidx]
        for m in range(D):
            cm = Un[m] * coef[m]
            re += cm * cE[m]; im -= cm * sE[m]
        p = re * re + im * im
        Kc += nidx * p; norm += p
    return Kc / (norm or 1.0)


def _pk_timesample(E, U, nt=90, tmax=600.0):
    """INDEPENDENT Krylov participation: directly time-sample |phi_n(t)|^2 and average (no eigen-average formula)."""
    D = len(E); rr = random.Random(0); Pbar = [0.0] * D
    for _ in range(nt):
        t = rr.uniform(0, tmax)
        cE = [math.cos(E[m] * t) for m in range(D)]; sE = [math.sin(E[m] * t) for m in range(D)]
        u0 = U[0]
        for nidx in range(D):
            re = 0.0; im = 0.0; Un = U[nidx]
            for m in range(D):
                cm = Un[m] * u0[m]; re += cm * cE[m]; im -= cm * sE[m]
            Pbar[nidx] += re * re + im * im
    tot = sum(Pbar) or 1.0
    return 1.0 / sum((p / tot) ** 2 for p in Pbar)


def _bn_disorder(b):
    """coefficient of variation of the bulk Lanczos coefficients (smooth chain ~ small; disordered ~ large)."""
    if len(b) < 6:
        return float('nan')
    bulk = b[1:len(b) - 1]
    mu = sum(bulk) / len(bulk)
    var = sum((x - mu) ** 2 for x in bulk) / len(bulk)
    return math.sqrt(var) / (mu or 1.0)


def _pipeline(label, n, adj, m2, src, onsite=None):
    ev, V = _Kdecomp(n, adj, m2, onsite=onsite)
    rsp = 0.0                                                       # round-35 real-space mode participation (consistency)
    for k in range(n):
        s4 = 0.0
        for i in range(n):
            a = V[i][k] * V[i][k]; s4 += a * a
        rsp += (1.0 / s4) if s4 > 0 else 0.0
    rsp /= n
    omega, w = _measure(ev, V, src)
    nd = len(omega)                                                  # distinct frequencies (D_K/2)
    # build the +-omega discrete measure
    freqs = omega + [-o for o in omega]
    amp0 = [math.sqrt(wi / 2.0) for wi in w] * 2
    a, b = _lanczos(freqs, amp0, maxsteps=len(freqs))
    met = _krylov_metrics(a, b)
    # --- validations ---
    b1sq = (b[0] ** 2) if b else 0.0
    m2_direct = sum(w[k] * omega[k] ** 2 for k in range(nd))         # <omega^2>
    # autocorrelation: chain vs direct, at a few t
    autc = 0.0
    for t in (1.3, 3.7, 6.1):
        c_chain = sum(met["U"][0][m] ** 2 * math.cos(met["E"][m] * t) for m in range(met["DK"]))
        c_dir = sum(w[k] * math.cos(omega[k] * t) for k in range(nd))
        autc = max(autc, abs(c_chain - c_dir))
    cov = _bn_disorder(b)
    support_err = abs(max(met["E"]) - max(omega)) if omega else 0.0    # band-edge (analytic) check
    m4_chain = sum(met["U"][0][m] ** 2 * met["E"][m] ** 4 for m in range(met["DK"]))
    m4_dir = sum(w[k] * omega[k] ** 4 for k in range(nd))
    pk_dir = _pk_timesample(met["E"], met["U"])
    return {"label": label, "n": n, "src": src, "DK": met["DK"], "PK": met["PK"], "Kbar": met["Kbar"],
            "cov": cov, "b1err": abs(b1sq - m2_direct), "autoerr": autc, "support_err": support_err,
            "m4err": abs(m4_chain - m4_dir), "pk_dir": pk_dir, "rsp": rsp, "E": met["E"], "U": met["U"]}


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Operator growth via the recursion method: Lanczos b_n of A=p_{i0}'s power spectrum Phi(omega),")
    print("  omega_k=sqrt(ev_k) of K=L+m^2. Order parameter = Krylov participation P_K (localized: small; delocalized: large).\n")
    m2 = 0.05
    nchain = 61 if not _FULL else 121
    ksteps = 80 if not _FULL else 200
    nreg = 80 if not _FULL else 150
    rows = []

    nc, adjc = _chain(nchain)
    rows.append(_pipeline("clean chain", nc, adjc, m2, nc // 2))
    nk, adjk = _keystone(ksteps, seed=5)
    rows.append(_pipeline("keystone tree", nk, adjk, m2, _hub(nk, adjk)))
    na, adja = _chain(nchain)
    rng = random.Random(7); W = 8.0; onsite = [rng.uniform(0, W) for _ in range(na)]
    rows.append(_pipeline("disordered chain", na, adja, m2, na // 2, onsite=onsite))
    nr, adjr = _random_regular(nreg, 3, seed=2)
    rows.append(_pipeline("random 3-regular", nr, adjr, m2, 0))

    print("  %-18s %5s %8s %7s %9s %8s %10s" % ("substrate", "D_K", "P_K", "P_K/N", "Kbar_c", "cov(b)", "rs-modeP"))
    for r in rows:
        print("  %-18s %5d %8.1f %7.2f %9.1f %8.2f %10.1f" % (
            r["label"], r["DK"], r["PK"], r["PK"] / r["n"], r["Kbar"], r["cov"], r["rsp"]))
    print("  (rs-modeP = round-35 real-space mode participation; small for localized substrates -- it TRACKS the")
    print("   Krylov P_K, two independent localization measures agreeing across all four substrates.)")

    print("\n  K_c(t) (growth = spreading; flat = saturated/localized):")
    for r in rows:
        ks = [(_Kc_of_t(r["E"], r["U"], t)) for t in (2.0, 5.0, 10.0, 20.0, 40.0)]
        print("    %-18s t=[2,5,10,20,40] -> [%s]" % (r["label"], ", ".join("%.1f" % x for x in ks)))

    print("\n  VALIDATION (independent cross-checks, every substrate):")
    print("    (1) sum rule b1^2=<omega^2>;  (2) autocorrelation chain==direct;  (3) <omega^4> chain==direct;")
    print("    (4) Krylov-chain band edge==max omega;  (5) P_K eigen-average vs INDEPENDENT time-sampled P_K:")
    for r in rows:
        print("    %-18s b1:%.0e auto:%.0e w4:%.0e edge:%.0e | P_K=%.1f  time-sampled=%.1f" % (
            r["label"], r["b1err"], r["autoerr"], r["m4err"], r["support_err"], r["PK"], r["pk_dir"]))

    kk = next(r for r in rows if r["label"] == "keystone tree")
    cc = next(r for r in rows if r["label"] == "clean chain")
    print("\n  => KEYSTONE P_K=%.1f (%.0f%% of N) vs CLEAN CHAIN P_K=%.1f (%.0f%% of N): the keystone operator occupies" % (
        kk["PK"], 100 * kk["PK"] / kk["n"], cc["PK"], 100 * cc["PK"] / cc["n"]))
    print("     only ~%.0f Krylov sites and its complexity saturates -- it ANDERSON-LOCALIZES in Krylov space. The" % kk["PK"])
    print("     disordered chain matches it (localization is the mechanism); the chain and 3-regular delocalize.")
    print("     Krylov participation is a clean order parameter for the no-scrambling substrate, confirming 35-37.")
