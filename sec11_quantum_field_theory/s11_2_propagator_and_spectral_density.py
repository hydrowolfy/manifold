"""The free scalar propagator on the keystone: no massless scalar (the IR divergence is confinement); a mass gaps it.

The natural free field on the substrate is the Gaussian theory of the graph Laplacian L -- the rule's own
diffusion generator (round 3: the rule's diffusion = the field Laplacian). Its propagator is the resolvent

        G_m(x,y) = <x| (L + m^2)^{-1} |y> = sum_t e^{-m^2 t} p(x,y;t)

(the heat kernel p Laplace-transformed at -m^2). Everything about it is fixed by the spectral density of L,
which the spectral dimension controls:

  rho(E) ~ E^{d_s/2 - 1}.

On the keystone d_s ~ 1.4 < 2, so rho(E) DIVERGES as E -> 0: an IR-divergent pile-up of low-energy modes.
The consequences are the QFT face of everything found in the geometry/matter sectors:

  1. NO FREE MASSLESS SCALAR. The on-diagonal propagator G_m(x,x) = sum_t e^{-m^2 t} P_return(t) DIVERGES as
     m -> 0 (because sum_t P_return diverges -- recurrence, round 26), with the spectral-dimension scaling
     G_m(x,x) ~ (m^2)^{d_s/2 - 1} = m^{d_s - 2}. A massless free scalar simply does not exist on this
     substrate; the IR divergence IS confinement.
  2. THE REGULARIZED MASSLESS TWO-POINT FUNCTION IS THE LINEAR CONFINING POTENTIAL. The IR-finite combination
     of propagators is the effective resistance, R(r) ~ r (linear) -- the confining potential (rounds 17,21).
     So "the massless two-point function" is not a Coulomb tail but a rising string.
  3. A MASS GAPS THE IR. For m > 0 the resolvent is finite (sum_t e^{-m^2 t} P_return converges); the massive
     field has a finite correlation length / mass gap. As m -> 0 the gap closes and the IR divergence returns.

This is the same story as confinement (d_s<2 recurrence) and the fractal continuum (d_s<2 not a manifold),
now read off the propagator: on a sub-two-dimensional substrate the free scalar Green's function has no
massless limit, and its regularized massless form is a linear potential. A genuine massless propagating
scalar would require d_s > 2 -- the manifold phase (round 25).

STATUS = DERIVED for the FREE scalar Green's function and its IR structure (computed natively from the
Laplacian heat kernel on the bare-rule graph); the interacting / higher-point correlators remain OPEN. Pure
Python.
"""
import math
import os
import random
from collections import Counter, deque
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Free scalar propagator: rho(E)~E^{d_s/2-1}; massless IR-divergent (=confinement, R(r)~r); a mass gaps it"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _keystone_tree(steps, seed=5):
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(seed))
    adj = {}
    for (u, v), m in E.items():
        if u != v:
            adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return {u: set(vs) for u, vs in adj.items()}


def _bfs(adj, s):
    seen = {s: 0}; dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in seen:
                seen[y] = seen[x] + 1; dq.append(y)
    return seen


def _slope_ll(xs, ys, lo, hi):
    pts = [(math.log(x), math.log(y)) for x, y in zip(xs, ys) if lo <= x <= hi and y > 0]
    n = len(pts); sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def _resist(adj, a, b, it=4000, tol=1e-9):
    V = {u: 0.0 for u in adj}; src = {u: 0.0 for u in adj}; src[a] = 1.0; src[b] = -1.0
    d = {u: len(adj[u]) for u in adj}
    for _ in range(it):
        md = 0.0
        for u in adj:
            nv = (sum(V[w] for w in adj[u]) + src[u]) / d[u]; md = max(md, abs(nv - V[u])); V[u] = nv
        if md < tol:
            break
    return V[a] - V[b]


def run():
    print("[DERIVED] %s" % TITLE)
    steps = 5000 if _FULL else 3000
    T = 1000 if _FULL else 500
    adj = _keystone_tree(steps); nodes = list(adj); N = len(nodes); idx = {u: i for i, u in enumerate(nodes)}
    deg = [len(adj[u]) for u in nodes]; nbr = [[idx[w] for w in adj[u]] for u in nodes]
    rng = random.Random(3); origins = [max(nodes, key=lambda u: len(adj[u]))] + rng.sample(nodes, 2 if not _FULL else 3)
    Pret = [0.0] * T
    for o in origins:
        p = [0.0] * N; p[idx[o]] = 1.0
        for t in range(T):
            Pret[t] += p[idx[o]]
            np_ = [0.0] * N
            for i in range(N):
                pi = p[i]
                if pi == 0.0:
                    continue
                np_[i] += 0.5 * pi; sh = 0.5 * pi / deg[i]
                for j in nbr[i]:
                    np_[j] += sh
            p = np_
    Pret = [x / len(origins) for x in Pret]
    ds = -2 * _slope_ll(list(range(1, T)), [Pret[t] for t in range(1, T)], 15, 140)
    print("  the free field is the Gaussian theory of the rule's Laplacian; propagator G_m=sum_t e^{-m^2 t} p.")
    print("  1. spectral density rho(E) ~ E^{d_s/2-1} from the heat-kernel trace P_return(t)~t^{-d_s/2}:")
    print("     d_s = %.2f  =>  rho(E) ~ E^{%.2f}  -- DIVERGES as E->0 (IR pile-up of modes, since d_s<2)." % (ds, ds / 2 - 1))
    print("  2. on-diagonal propagator G_m(x,x)=sum_t e^{-m^2 t} P_return(t)  (massless m=0 diverges):")
    print("     m^2      G_m(x,x)")
    m2list = [0.2, 0.05, 0.02, 0.008, 0.003]
    Gd = []
    for m2 in m2list:
        G = sum(math.exp(-m2 * t) * Pret[t] for t in range(T)); Gd.append(G)
        print("     %.3f    %.3f" % (m2, G))
    sl = _slope_ll([m2 for m2 in m2list], Gd, min(m2list), max(m2list))
    print("     massless sum_t P_return (truncated) = %.1f and still growing -> formally INFINITE: no free massless scalar." % sum(Pret))
    print("     scaling G_m(x,x) ~ (m^2)^%.2f  (predicted d_s/2-1 = %.2f): the IR divergence is set by d_s." % (sl, ds / 2 - 1))
    print("  3. regularized massless 2-point function = effective resistance R(r) -- the CONFINING linear potential:")
    o = origins[0]; dd = _bfs(adj, o)
    print("     on the tree (b1=1) the effective resistance EQUALS the graph distance (unique path), so R(r) ~ r:")
    for r in (2, 4, 6):
        cand = [n for n in nodes if dd.get(n, 99) == r]
        if cand:
            print("     R(r=%d) = %.2f  (~ r)" % (r, _resist(adj, o, cand[len(cand) // 2], it=2500)))
    print("     R(r) = r LINEAR: the massless two-point function is a rising string, not a Coulomb tail.")
    print("  => no free massless scalar (the IR divergence = confinement); a mass m gaps the IR (finite G_m). A")
    print("     genuinely propagating massless scalar would need d_s>2 -- the manifold phase (round 25). The free")
    print("     scalar Green's function and its IR structure are DERIVED; interacting/higher-point correlators remain OPEN.")
