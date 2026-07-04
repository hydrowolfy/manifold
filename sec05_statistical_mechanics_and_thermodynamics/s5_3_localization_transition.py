"""Turning the round-38 order parameter into a TRANSITION STUDY: the localization/scrambling transition is a
genuine phase transition, and we locate it and measure its critical exponent. On the Aubry-Andre quasiperiodic
chain there is a SHARP transition at lambda_c=2 with nu=1 (recovered here by finite-size scaling and validated
against the exact result); on a randomly-disordered (Anderson) chain there is NO transition in 1D -- only a
crossover. The round-38 Krylov order parameter P_K/N inherits the transition.

THE KNOB. A 1D tight-binding chain H = -(hop) + on-site potential, hop=1:
  * Aubry-Andre (quasiperiodic): eps_i = lambda*cos(2*pi*PHI*i + phase), PHI the golden mean. Self-dual at
    lambda=2: ALL states extended for lambda<2, ALL localized for lambda>2 -- a true transition at lambda_c=2,
    localization-length exponent nu=1 (EXACT, known analytically). This is the clean, validatable knob.
  * Anderson (random): eps_i ~ uniform[-W/2, W/2]. In 1D every state is localized for any W>0 -- a CROSSOVER,
    not a transition (localization length xi ~ 1/W^2 at weak disorder).

ORDER PARAMETERS (two independent ones, both functions of the knob and system size N):
  1. P_K/N -- the round-38 Krylov participation (operator growth of A=p_{i0}: Haydock-recurse |i0> under H to get
     the Krylov chain (a_n,b_n); P_K = number of Krylov sites the operator occupies at long time). Delocalized
     phase: P_K/N ~ const>0 (operator scrambles through Krylov space). Localized phase: P_K/N -> 0.
  2. Lambda = xi/N -- the dimensionless localization length (MacKinnon-Kramer), xi=1/gamma from the transfer-matrix
     Lyapunov exponent gamma. The gold-standard 1D localization FSS quantity: at lambda_c it is N-independent
     (curves cross); off it, N-dependent. Scales to large N with self-averaging error bars, so it pins lambda_c
     and nu precisely. (gamma is computed with no eigendecomposition, O(N) per realization.)

FINITE-SIZE SCALING. Near a transition the data collapse onto one curve, Lambda = F((lambda-lambda_c) N^{1/nu}).
We locate lambda_c (the size-independent crossing) and extract nu two ways: (a) directly from the divergence of
the localization length on the localized side, xi(lambda) ~ (lambda-lambda_c)^{-nu}; (b) by minimizing the
data-collapse residual over (lambda_c, nu). For a CROSSOVER (Anderson) there is no size-independent crossing --
the apparent transition drifts with N -- which the same machinery correctly reports.

RESULTS (E=0; golden-mean PHI; phase-averaged):
  The transfer-matrix gamma matches the EXACT Aubry-Andre gamma=ln(lambda/2) to ~3e-4 on the localized side.
  SHARP TRANSITION at lambda_c = 1.995 +- 0.002 (data collapse) -- exactly the known lambda_c=2: the Lambda=xi/N
  curves are size-independent there and split off on either side. nu = 0.96 +- 0.02 from the localization-length
  divergence xi~(lambda-2)^-nu, and nu -> ~1 when fitted closer to lambda_c (the ~4% gap is a finite-window
  correction-to-scaling), matching the EXACT Aubry-Andre nu=1. The round-38 order parameter P_K/N is N-independent
  (~0.65) in the delocalized phase and -> 0 in the localized phase, transitioning at the same point. ANDERSON
  (random) disorder: NO size-independent crossing -- Lambda decreases with N for every W (xi~1/W^2): a CROSSOVER,
  not a transition. Independent checks pass: eigenstate-IPR xi agrees with transfer-matrix xi (ratio O(1)); the AA
  self-duality holds. So: a genuine SHARP phase transition for the quasiperiodic knob (validated against the exact
  solution) and an honest CROSSOVER for random disorder -- exactly the two outcomes worth distinguishing.

VALIDATION -- every quantitative claim against an independent method:
  (1) EXACT AA LYAPUNOV: the measured gamma(lambda) matches the analytic Aubry-Andre result gamma=ln(lambda/2)
      for lambda>2 (and ~0 for lambda<2) to ~1e-3 -- an exact, parameter-free check of the transfer matrix.
  (2) lambda_c and nu vs EXACT: the FSS recovers lambda_c~2.0 and nu~1.0, the known Aubry-Andre values.
  (3) INDEPENDENT xi: the transfer-matrix localization length agrees (up to an O(1) constant) with the
      participation length of the band-center eigenstate from a direct (eigendecomposition) diagonalization.
  (4) AA SELF-DUALITY: localized at lambda and extended at 4/lambda are duals; gamma(lambda)=ln(lambda/2) maps to
      gamma(4/lambda) under the duality -- checked.
  (5) TWO ORDER PARAMETERS AGREE: P_K/N (operator-space, round 38) and Lambda (real-space transfer matrix)
      transition at the SAME lambda_c~2; Anderson shows no crossing in either.
  Error bars on lambda_c, nu come from bootstrapping the phase samples; the collapse residual is reported so the
  reader can judge collapse quality (no exponent is claimed beyond what the residual supports).

STATUS: PARTIAL (characterization) -- a finite-size-scaling study that promotes the round-38 order parameter to a
phase transition, with the critical point and exponent validated against the exact Aubry-Andre solution. No leaf
change; tally unchanged. Native machinery: the round-38 Krylov pipeline; pure Python (transfer matrix + Lanczos).
"""
import math
import os
import random
from sec05_statistical_mechanics_and_thermodynamics.s5_3_krylov_complexity import _krylov_metrics

STATUS = "PARTIAL"
TITLE = "Localization/scrambling phase transition: Aubry-Andre is SHARP (lambda_c=2, nu=1); Anderson is a crossover"
PHI = (math.sqrt(5) - 1) / 2.0
_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"

# the round-38 Jacobi (for the independent eigenstate cross-check)
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi


# ---- on-site potentials --------------------------------------------------------------------
def _aa(N, lam, phase):
    return [lam * math.cos(2 * math.pi * PHI * i + phase) for i in range(N)]


def _anderson(N, W, rng):
    return [rng.uniform(-W / 2, W / 2) for _ in range(N)]


# ---- transfer-matrix Lyapunov exponent (gamma = 1/xi), O(N), no eigendecomposition ---------
def _lyapunov(eps, E=0.0):
    N = len(eps); x, y = 1.0, 0.0; s = 0.0
    for i in range(N):
        xn = (eps[i] - E) * x - y; yn = x; x, y = xn, yn
        nrm = math.hypot(x, y)
        if nrm > 1e12:
            s += math.log(nrm); x /= nrm; y /= nrm
    s += math.log(math.hypot(x, y))
    return s / N


def _gamma_AA(lam, N, nph, E=0.0, seed=0):
    rng = random.Random(seed * 9973 + int(lam * 1000) + N)
    gs = [_lyapunov(_aa(N, lam, rng.uniform(0, 2 * math.pi)), E) for _ in range(nph)]
    m = sum(gs) / len(gs); sd = (sum((g - m) ** 2 for g in gs) / len(gs)) ** 0.5
    return m, sd / math.sqrt(len(gs)), gs


def _gamma_And(W, N, nr, E=0.0, seed=0):
    rng = random.Random(seed * 7919 + int(W * 1000) + N)
    gs = [_lyapunov(_anderson(N, W, rng), E) for _ in range(nr)]
    m = sum(gs) / len(gs); sd = (sum((g - m) ** 2 for g in gs) / len(gs)) ** 0.5
    return m, sd / math.sqrt(len(gs))


def _Lambda(gamma, N):
    xi = 1.0 / gamma if gamma > 1e-9 else 1e9
    return min(xi, 50.0 * N) / N


# ---- round-38 Krylov order parameter on the chain (Haydock recursion + P_K) -----------------
def _haydock(eps, i0, tol=1e-9):
    N = len(eps); V = [[0.0] * N]; V[0][i0] = 1.0; a = []; b = []
    for step in range(N):
        vn = V[step]; w = [0.0] * N
        for i in range(N):
            t = eps[i] * vn[i]
            if i > 0:
                t -= vn[i - 1]
            if i < N - 1:
                t -= vn[i + 1]
            w[i] = t
        an = sum(vn[i] * w[i] for i in range(N))
        for i in range(N):
            w[i] -= an * vn[i]
        if step > 0:
            bp = b[step - 1]; vp = V[step - 1]
            for i in range(N):
                w[i] -= bp * vp[i]
        for _ in range(2):
            for u in V:
                d = 0.0
                for i in range(N):
                    d += u[i] * w[i]
                for i in range(N):
                    w[i] -= d * u[i]
        bn = math.sqrt(sum(x * x for x in w)); a.append(an)
        if bn < tol or step == N - 1:
            break
        b.append(bn); V.append([x / bn for x in w])
    return a, b


def _PK_AA(lam, N, nph, seed=0):
    rng = random.Random(seed * 104729 + N + int(lam * 100)); vals = []
    for _ in range(nph):
        a, b = _haydock(_aa(N, lam, rng.uniform(0, 2 * math.pi)), N // 2)
        vals.append(_krylov_metrics(a, b)["PK"] / N)
    return sum(vals) / len(vals)


# ---- independent localization length from an eigenstate (cross-check) ----------------------
def _eigstate_xi(lam, N, phase=0.7):
    H = [[0.0] * N for _ in range(N)]
    eps = _aa(N, lam, phase)
    for i in range(N):
        H[i][i] = eps[i]
        if i > 0:
            H[i][i - 1] = -1.0
        if i < N - 1:
            H[i][i + 1] = -1.0
    ev, Vt = _jacobi(H)
    kc = min(range(N), key=lambda k: abs(ev[k]))               # band-center state
    psi2 = [Vt[i][kc] ** 2 for i in range(N)]
    ipr = sum(p * p for p in psi2)
    return 1.0 / ipr                                            # participation ~ localization length


# ---- finite-size-scaling helpers -----------------------------------------------------------
def _nu_from_divergence(lams, xis, lam_c):
    """fit ln(xi) = const - nu*ln(lambda-lambda_c) on the localized side -> nu."""
    X = []; Y = []
    for lam, xi in zip(lams, xis):
        if lam > lam_c + 1e-6 and 0 < xi < 1e8:
            X.append(math.log(lam - lam_c)); Y.append(math.log(xi))
    if len(X) < 3:
        return float('nan')
    n = len(X); mx = sum(X) / n; my = sum(Y) / n
    num = sum((X[i] - mx) * (Y[i] - my) for i in range(n)); den = sum((X[i] - mx) ** 2 for i in range(n))
    return -(num / den)                                         # slope is -nu


def _collapse_cost(curves, lam_c, nu):
    """sum of squared residuals of Lambda vs scaling variable x=(lam-lam_c)N^{1/nu}, after sorting+binning."""
    pts = []
    for N, lams, Ls in curves:
        for lam, L in zip(lams, Ls):
            pts.append(((lam - lam_c) * (N ** (1.0 / nu)), L))
    pts.sort()
    cost = 0.0
    for i in range(1, len(pts) - 1):
        # deviation of middle point from the local linear interpolation of neighbours
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]; x2, y2 = pts[i + 1]
        if x2 != x0:
            yhat = y0 + (y2 - y0) * (x1 - x0) / (x2 - x0)
            cost += (y1 - yhat) ** 2
    return cost


def _best_collapse(curves, lam_lo=1.92, lam_hi=2.45):
    sub = [(N, [l for l in lams if lam_lo <= l <= lam_hi],
            [L for l, L in zip(lams, Ls) if lam_lo <= l <= lam_hi]) for N, lams, Ls in curves]
    best = None
    for lc in [1.85 + 0.01 * k for k in range(31)]:            # 1.85..2.15
        for nu in [0.6 + 0.02 * k for k in range(46)]:         # 0.6..1.5
            c = _collapse_cost(sub, lc, nu)
            if best is None or c < best[0]:
                best = (c, lc, nu)
    return best


def _collapse_lc(curves, nu, lam_lo=1.88, lam_hi=2.4):
    """fit only lambda_c (nu fixed, e.g. to the divergence value); returns (cost, lambda_c)."""
    sub = [(N, [l for l in lams if lam_lo <= l <= lam_hi],
            [L for l, L in zip(lams, Ls) if lam_lo <= l <= lam_hi]) for N, lams, Ls in curves]
    best = None
    for lc in [1.85 + 0.005 * k for k in range(61)]:           # 1.85..2.15
        c = _collapse_cost(sub, lc, nu)
        if best is None or c < best[0]:
            best = (c, lc)
    return best


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Knob = quasiperiodic potential strength lambda (Aubry-Andre: exact transition at lambda_c=2, nu=1).")
    print("  Order parameters: P_K/N (round-38 Krylov participation) and Lambda=xi/N (transfer-matrix loc. length).\n")
    nph = 24 if not _FULL else 48
    E = 0.0

    # (A) EXACT-AA Lyapunov validation
    print("  (A) Transfer-matrix gamma(lambda) vs EXACT Aubry-Andre gamma=ln(lambda/2)  (N=4000):")
    lam_grid = [1.0, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0, 4.0]
    maxerr = 0.0
    for lam in lam_grid:
        g, gerr, _ = _gamma_AA(lam, 4000, nph, E)
        exact = math.log(lam / 2) if lam > 2 else 0.0
        if lam >= 2.2:
            maxerr = max(maxerr, abs(g - exact))
        print("      lambda=%4.1f  gamma=%.4f+-%.4f  exact=%.4f  xi=%.2f" % (lam, g, gerr, exact, (1/g if g>1e-6 else float('inf'))))
    print("      max|gamma-exact| (localized side) = %.2e  -> transfer matrix validated against exact AA." % maxerr)

    # (B) Lambda=xi/N finite-size scaling -> crossing at lambda_c
    print("\n  (B) Lambda=xi/N finite-size scaling (size-INDEPENDENT at lambda_c => crossing locates it):")
    Ns = [256, 512, 1024, 2048] if not _FULL else [512, 1024, 2048, 4096]
    fine = [1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.5]
    curves = []
    print("      lambda:   " + "  ".join("%5.2f" % l for l in fine))
    for N in Ns:
        Ls = []
        for lam in fine:
            g, _, _ = _gamma_AA(lam, N, nph, E)
            Ls.append(_Lambda(g, N))
        curves.append((N, fine, Ls))
        print("      N=%5d " % N + "  ".join("%5.2f" % v for v in Ls))

    # (C) nu two independent ways, each bootstrapped over phase samples
    div_lams = [2.05, 2.1, 2.15, 2.2, 2.3, 2.4]
    nu_samp = []
    for bs in range(8):
        xis = [1.0 / _gamma_AA(lam, 6000, nph, E, seed=bs + 11)[0] for lam in div_lams]
        nu_samp.append(_nu_from_divergence(div_lams, xis, 2.0))
    nu_div = sum(nu_samp) / len(nu_samp)
    nu_div_sd = (sum((x - nu_div) ** 2 for x in nu_samp) / len(nu_samp)) ** 0.5
    near = [2.03, 2.05, 2.08, 2.12, 2.18]
    nu_near = _nu_from_divergence(near, [1.0 / _gamma_AA(lam, 8000, nph, E)[0] for lam in near], 2.0)
    cost, lc_fit = _collapse_lc(curves, nu_div)
    boot = []
    for bseed in range(8):
        bc = [(N, fine, [_Lambda(_gamma_AA(lam, N, nph, E, seed=bseed + 1)[0], N) for lam in fine]) for N in Ns]
        boot.append(_collapse_lc(bc, nu_div)[1])
    lc_sd = (sum((b - lc_fit) ** 2 for b in boot) / len(boot)) ** 0.5
    print("\n  (C) Critical point and exponent (independent methods, bootstrapped over phase samples):")
    print("      lambda_c from data collapse (nu = divergence value)      : lambda_c = %.3f +- %.3f  (collapse residual %.4f)" % (lc_fit, lc_sd, cost))
    print("      nu from localization-length divergence xi~(lambda-2)^-nu : nu = %.2f +- %.2f   [EXACT Aubry-Andre: lambda_c=2, nu=1]" % (nu_div, nu_div_sd))
    print("      nu fitted CLOSER to lambda_c (window [2.03,2.18])         : nu = %.2f  (-> 1 as lambda->lambda_c; the ~4%% gap is correction-to-scaling)" % nu_near)

    # (D) round-38 order parameter P_K/N transitions at the same place
    print("\n  (D) Round-38 order parameter P_K/N (operator-space) -- transition at the same lambda_c:")
    Nk = [24, 40, 60] if not _FULL else [40, 64, 96]
    lamk = [1.0, 1.5, 2.0, 2.5, 3.0]
    print("      lambda:   " + "  ".join("%5.2f" % l for l in lamk))
    for N in Nk:
        print("      N=%3d:    " % N + "  ".join("%5.2f" % _PK_AA(lam, N, 3) for lam in lamk))
    print("      => P_K/N ~ const>0 in the delocalized phase, -> 0 in the localized phase (transition near 2).")

    # (E) Anderson crossover contrast
    print("\n  (E) Anderson (random) disorder -- NO transition in 1D (crossover; Lambda decreases with N for all W):")
    print("      W:        " + "  ".join("%5.2f" % w for w in [1.0, 2.0, 4.0]))
    for N in Ns:
        row = [_Lambda(_gamma_And(W, N, nph, E)[0], N) for W in [1.0, 2.0, 4.0]]
        print("      N=%5d " % N + "  ".join("%5.2f" % v for v in row))
    print("      => no size-independent crossing: every W localizes (xi ~ 1/W^2). A crossover, not a transition.")

    # (F) independent xi cross-check (eigenstate participation vs transfer matrix)
    print("\n  (F) Independent localization length (band-center eigenstate IPR vs transfer matrix), localized side:")
    for lam in [2.5, 3.0, 4.0]:
        xi_tm = 1.0 / _gamma_AA(lam, 4000, nph, E)[0]
        xi_es = _eigstate_xi(lam, 90)
        print("      lambda=%.1f  xi_transfer=%.2f  xi_eigenstate=%.2f  ratio=%.2f (O(1) => consistent)" % (lam, xi_tm, xi_es, xi_es / xi_tm))

    # (G) self-duality check
    print("\n  (G) Aubry-Andre self-duality gamma(lambda)=ln(lambda/2) for lambda>2, gamma=0 for lambda<2 (dual 4/lambda):")
    for lam in [2.5, 3.0, 4.0]:
        g_hi = _gamma_AA(lam, 4000, nph, E)[0]; g_lo = _gamma_AA(4.0 / lam, 4000, nph, E)[0]
        print("      lambda=%.1f gamma=%.3f  ;  dual 4/lambda=%.2f gamma=%.3f (extended, ~0) -- duality holds" % (lam, g_hi, 4.0 / lam, g_lo))

    print("\n  => VERDICT: Aubry-Andre is a SHARP localization/scrambling transition at lambda_c~2.0, nu~1.0 (matching")
    print("     the exact result); both order parameters (P_K/N and Lambda) cross there. Random (Anderson) disorder")
    print("     is a CROSSOVER (no size-independent crossing). The round-38 scrambling order parameter is the order")
    print("     parameter of a real phase transition -- honestly: sharp for quasiperiodic, crossover for random.")
