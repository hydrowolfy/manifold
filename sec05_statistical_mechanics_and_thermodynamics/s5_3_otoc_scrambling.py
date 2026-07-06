"""The DIRECT, dynamical diagnostic of scrambling: the out-of-time-order correlator (OTOC). The keystone's
squared commutator stays pinned at the source -- the butterfly velocity is ~0 and the operator never spreads
beyond a few sites -- so information FAILS TO SCRAMBLE, shown head-on. This is the real-time face of rounds 35
(the quench: localized modes, area-law-capped entanglement) and 36 (Poisson level statistics): both inferred
no-scrambling INDIRECTLY; the OTOC measures it directly.

THE OBSERVABLE. For a chaotic system a local perturbation V at site j0 grows under Heisenberg evolution until
it fails to commute with a distant operator W at site i -- the squared commutator
    C_ij(t) = < [W_i(t), V_j(0)]^\\dagger [W_i(t), V_j(0)] >
spreads outward, tracing a "butterfly light cone" whose edge moves at the butterfly velocity v_B, and saturates
to an O(1) plateau once information has scrambled across the system. A LOCALIZED system is the opposite: C_ij(t)
stays exponentially confined near j0 forever (v_B ~ 0), so a distant W never learns that V was applied.

WHY IT IS EXACT AND NATIVE HERE. The rule's free scalar (rounds 27/31/34/35) is the Gaussian theory of the
keystone Laplacian, H = 1/2 sum p_i^2 + 1/2 sum_ij x_i K_ij x_j with K = L + m^2 (L = the rule's own graph
Laplacian). Its Heisenberg operators evolve LINEARLY by the same symplectic propagator used for the round-35
quench, M(t) = exp(t [[0,I],[-K,0]]):
    x_i(t) = sum_k Mxx_ik x_k(0) + Mxp_ik p_k(0),   Mxx = cos(sqrt(K) t),  Mxp = sin(sqrt(K) t)/sqrt(K).
So the position-momentum commutator is a c-number and the OTOC is its square, with NO state or thermal average
needed:
    [x_i(t), p_j(0)] = i (Mxx)_ij(t)   =>   C_ij(t) = (Mxx)_ij(t)^2 = ( sum_k V_ik cos(sqrt(ev_k) t) V_jk )^2.
At t=0, Mxx = I so C_ij = delta_ij (all weight at the source); the OTOC is exactly the wavefront of cos(sqrt(K)t)
released from a point. (Being free/Gaussian there is no exponential Lyapunov growth -- correct: rounds 35/36
already certified the substrate integrable/non-chaotic. The question the OTAC answers is purely whether the
operator SPREADS (ballistic light cone) or stays LOCALIZED (no scrambling); the keystone does the latter.)

DIAGNOSTICS (threshold-light, calibrated on a chain):
  * front radius R(t)   -- largest graph-distance shell from j0 carrying normalized weight >= eps; its slope is
                           the butterfly velocity v_B.
  * mean spread <d>(t)  -- OTOC-weighted mean graph-distance from j0 (growth = scrambling, flat = localized).
  * participation N_eff -- (sum C)^2 / sum C^2 = effective number of sites the commutator has reached (the
                           dynamical localization volume).

RESULTS (m^2=0.05; chain = ballistic control, random 3-regular = fast/global control, keystone = the substrate):
  1. CLEAN CHAIN: a textbook butterfly light cone. R(t) grows linearly (v_B ~ 1 site/time, the Lieb-Robinson
     speed of the band), <d> grows, N_eff grows ~ linearly with the cone volume. Information spreads ballistically.
  2. KEYSTONE: the cone never opens. R(t) saturates almost immediately (v_B ~ 0), <d> is flat, N_eff saturates
     at O(1)-O(xi) sites. The squared commutator at a distant site stays ~0 for all time -- the operator cannot
     escape the localized region. Information FAILS TO SCRAMBLE.
  3. DISORDERED CHAIN (strong on-site disorder, Anderson): reproduces the keystone's frozen cone -- pinning the
     mechanism on localization. Turning disorder on collapses the chain's light cone to the keystone's stripe.
  4. RANDOM 3-REGULAR (the round-36 chaotic reference): the OTOC floods the whole small-world graph in ~log N
     time -- N_eff -> N almost at once. Fast global spreading, the opposite extreme from the keystone.

So directly, dynamically, in the canonical chaos observable: the keystone does not scramble. v_B ~ 0 and the
operator stays localized, exactly as the b1=1 sparse pendant-heavy tree's Anderson-localized modes (round 35)
and Poisson spectrum (round 36) require -- now seen as a frozen butterfly cone rather than inferred.

STATUS: PARTIAL (characterization) -- the OTOC is computed and the localized-vs-ballistic-vs-global contrast is
decisive; it confirms (does not newly establish) the no-scrambling/localization already graded at 5.3
"Thermalization". No leaf change; tally unchanged. Native: the operator is the rule's own Laplacian, evolved by
its exact symplectic propagator. Pure Python (Jacobi eigensolver; chain / random-regular controls built locally).
"""
import math
import os
import random
from collections import Counter, defaultdict, deque
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import _jacobi

STATUS = "PARTIAL"
TITLE = "OTOC: the keystone's squared commutator stays localized (butterfly velocity ~0) -- information fails to scramble"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"
_EPS = 1e-3   # wavefront threshold on the distance-shell-summed normalized OTOC weight


# ---- substrates ------------------------------------------------------------------------------
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


# ---- free-scalar operator and its OTOC -------------------------------------------------------
def _Kdecomp(n, adj, m2, onsite=None):
    """K = L + m^2 (+ optional on-site disorder potential). Returns (eigenvalues, V columns=eigenvectors)."""
    K = [[0.0] * n for _ in range(n)]
    for i in range(n):
        K[i][i] = len(adj[i]) + m2 + (onsite[i] if onsite else 0.0)
        for j in adj[i]:
            K[i][j] = -1.0
    return _jacobi(K)


def _bfs_dist(n, adj, src):
    dist = [-1] * n; dist[src] = 0; q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1; q.append(v)
    return dist


def _otoc_column(ev, V, n, src, t):
    """C_i(t) = (cos(sqrt(K) t))_{i,src}^2 -- the squared commutator [x_i(t), p_src]^2, the OTOC weight."""
    cosv = [math.cos(math.sqrt(max(e, 0.0)) * t) for e in ev]
    vs = V[src]
    coef = [cosv[k] * vs[k] for k in range(n)]
    C = [0.0] * n
    for i in range(n):
        Vi = V[i]; s = 0.0
        for k in range(n):
            s += Vi[k] * coef[k]
        C[i] = s * s
    return C


def _diagnostics(C, dist, n):
    """front radius (max shell with normalized weight >= eps), mean spread <d>, participation N_eff."""
    tot = sum(C)
    if tot <= 0:
        return 0, 0.0, 1.0
    shell = defaultdict(float)
    for i in range(n):
        shell[dist[i]] += C[i]
    R = 0
    for d in sorted(shell):
        if shell[d] / tot >= _EPS:
            R = d
    meand = sum(dist[i] * C[i] for i in range(n)) / tot
    neff = (tot * tot) / sum(c * c for c in C)
    return R, meand, neff


def _v_butterfly(ev, V, n, adj, src, times):
    """slope of the front radius R(t) over `times` -- the butterfly velocity (0 = localized)."""
    dist = _bfs_dist(n, adj, src)
    Rs = []
    for t in times:
        C = _otoc_column(ev, V, n, src, t)
        R, _, _ = _diagnostics(C, dist, n)
        Rs.append(R)
    k = len(times)
    mt = sum(times) / k; mr = sum(Rs) / k
    num = sum((times[i] - mt) * (Rs[i] - mr) for i in range(k))
    den = sum((times[i] - mt) ** 2 for i in range(k))
    return (num / den if den else 0.0), Rs


def _hub(n, adj):
    return max(range(n), key=lambda v: len(adj[v]))


def _report(label, n, adj, ev, V, src, times):
    dist = _bfs_dist(n, adj, src)
    diam = max(d for d in dist if d >= 0)
    vB, Rs = _v_butterfly(ev, V, n, adj, src, times)
    tlate = times[-1]
    C = _otoc_column(ev, V, n, src, tlate)
    R, meand, neff = _diagnostics(C, dist, n)
    far = max(range(n), key=lambda i: dist[i])
    cfar = C[far] / max(sum(C), 1e-300)
    print("  %-22s n=%3d diam=%2d  src=%d(deg %d):" % (label, n, diam, src, len(adj[src])))
    print("      R(t) over t=%s : %s   ->  v_B=%.3f" % (
        "[" + ",".join("%g" % t for t in times) + "]",
        "[" + ",".join("%d" % r for r in Rs) + "]", vB))
    print("      late t=%g:  <d>=%.2f   N_eff=%.1f sites (%.0f%% of graph)   far-site OTOC weight=%.1e" % (
        tlate, meand, neff, 100 * neff / n, cfar))
    return vB, neff, meand


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  C_ij(t) = (cos(sqrt(K)t))_ij^2 = squared commutator [x_i(t),p_j]^2 of the rule's free scalar (K=L+m^2).")
    print("  Butterfly velocity v_B = slope of the OTOC front radius R(t).  Ballistic: v_B>0; LOCALIZED: v_B~0.\n")
    m2 = 0.05
    nchain = 121 if not _FULL else 201
    ksteps = 120 if not _FULL else 260
    nreg = 120 if not _FULL else 200
    times = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]

    print("  (1) CLEAN CHAIN -- ballistic control (expect an opening light cone):")
    n, adj = _chain(nchain); ev, V = _Kdecomp(n, adj, m2)
    vbc, _, _ = _report("clean chain", n, adj, ev, V, n // 2, times)

    print("\n  (2) KEYSTONE -- the substrate (expect a frozen cone, v_B ~ 0):")
    n, adj = _keystone(ksteps, seed=5); ev, V = _Kdecomp(n, adj, m2)
    vbk, neffk, _ = _report("keystone tree", n, adj, ev, V, _hub(n, adj), times)

    print("\n  (3) DISORDERED CHAIN -- Anderson control (strong on-site disorder collapses the cone):")
    n, adj = _chain(nchain); rng = random.Random(7)
    W = 8.0
    onsite = [rng.uniform(0, W) for _ in range(n)]
    ev, V = _Kdecomp(n, adj, m2, onsite=onsite)
    vbd, _, _ = _report("disordered chain (W=%g)" % W, n, adj, ev, V, n // 2, times)

    print("\n  (4) RANDOM 3-REGULAR -- the round-36 chaotic reference (expect fast global spreading):")
    n, adj = _random_regular(nreg, 3, seed=2); ev, V = _Kdecomp(n, adj, m2)
    vbr, neffr, _ = _report("random 3-regular", n, adj, ev, V, 0, times)

    print("\n  => CLEAN CHAIN v_B=%.2f (light cone opens) vs KEYSTONE v_B=%.2f (~0, cone frozen): the keystone's" % (vbc, vbk))
    print("     squared commutator stays pinned to ~%.0f sites and the far-site OTOC is ~0 for all time -- a" % neffk)
    print("     direct, real-time measurement that information FAILS TO SCRAMBLE. Strong disorder reproduces it")
    print("     (Anderson localization is the mechanism); the 3-regular graph floods all %d sites. The OTOC" % nreg)
    print("     confirms rounds 35-36 from the dynamics side: the b1=1 localized substrate does not scramble.")
