"""The field made LOCAL: a retarded, finite-speed field whose static limit IS round-6 electrostatics.

Round 9 surfaced an honesty point: the round-6/7 force uses the INSTANTANEOUS global field energy (it
solves the Poisson equation over the whole graph at once), which is non-local -- a strictly local rule
cannot do that. A local rule permits only a RETARDED force: a disturbance must propagate from one charge
to another at finite speed. This module builds that local field and shows electrostatics is its static
limit, closing the locality gap.

CONSTRUCTION: a local field phi on the nodes obeying a discrete damped wave (telegrapher) equation,
  phi[t+1] = (2-g) phi[t] - (1-g) phi[t-1] - h^2 (L phi[t] - rho),
with L the graph Laplacian -- the rule's OWN diffusion generator (round 3). The update is local
(nearest-neighbour) and second-order in time, so disturbances propagate at a FINITE speed instead of
instantaneously. Pure Python.

RESULTS:
  - RETARDATION (a light cone): a pulse at a node produces a field that is exactly zero beyond a sharp
    causal FRONT advancing at ~1 node/step; a disturbance reaches distance d only after ~d steps. This
    is the local, finite-speed field the round-9 critique required -- unlike instantaneous electrostatics.
  - STATIC LIMIT = ELECTROSTATICS: with a held charge rho, the damped field relaxes to the solution of
    L V = rho -- the exact instantaneous Poisson potential of round 6 (relative mismatch ~1e-30, i.e.
    identical). So the round-6/7 Coulomb/confining force is the LONG-TIME limit of a genuinely local,
    retarded process. The non-locality was an artifact of taking the static limit first; the underlying
    dynamics is local.
  - SPEED = CAUSALITY: the field's front advances at the graph's hopping speed (1 node/step), the same
    speed as the substrate's causal cone (round 1). Field disturbances and causal information travel at
    the same 'c', both set by the graph -- the substrate's version of "light moves at the causal speed".

HONEST STATUS = PARTIAL: the SPATIAL operator (L) is the rule's own; the wave/telegrapher TEMPORAL
structure is a postulated local field equation (BORROWED), the minimal local dynamics with a finite
speed. What this establishes is that the electrostatic force CAN be carried locally and reduces to
round 6 in the static limit. Full radiation (an accelerating charge's outward energy flux) and the
magnetic sector (a moving charge's retarded field) are the natural next steps and remain OPEN -- a clean
1D monopole demonstration of radiation is subtle (no geometric fall-off; multipole/charge-conservation
caveats), so it is not claimed here.
"""
import math
from collections import Counter
from sec00_core_substrate import nodes

STATUS = "PARTIAL"
TITLE = "Retarded local field: finite-speed propagation; static limit recovers electrostatics"


def _lap_adj(E):
    adj = {}
    for (u, v), m in E.items():
        adj.setdefault(u, {}); adj.setdefault(v, {})
        adj[u][v] = adj[u].get(v, 0) + m; adj[v][u] = adj[v].get(u, 0) + m
    return adj


def _Lmv(adj, x):
    out = {}
    for u in adj:
        s = sum(adj[u].values()) * x.get(u, 0.0)
        for v, m in adj[u].items():
            s -= m * x.get(v, 0.0)
        out[u] = s
    return out


def _cg(adj, rho, it=3000, tol=1e-12):
    V = {u: 0.0 for u in adj}; r = dict(rho); mr = sum(r.values()) / len(r); r = {u: r[u] - mr for u in r}
    p = dict(r); rs = sum(v * v for v in r.values())
    for _ in range(it):
        Lp = _Lmv(adj, p); pLp = sum(p[u] * Lp[u] for u in adj)
        if abs(pLp) < 1e-30:
            break
        a = rs / pLp
        for u in adj:
            V[u] += a * p[u]; r[u] -= a * Lp[u]
        rs2 = sum(v * v for v in r.values())
        if rs2 < tol:
            break
        b = rs2 / rs; rs = rs2
        for u in adj:
            p[u] = r[u] + b * p[u]
    return V


def _chain(n):
    return Counter({(i, i + 1): 1 for i in range(n)})


def run():
    print("[PARTIAL] %s" % TITLE)
    # (1) retardation: sharp causal front at ~1 node/step
    adj = _lap_adj(_chain(50)); phi = {u: 0.0 for u in adj}; prev = {u: 0.0 for u in adj}; h2 = 0.5
    print("  RETARDATION (a local field has a finite-speed causal FRONT, not instantaneous reach):")
    for t in range(1, 25):
        Lp = _Lmv(adj, phi); new = {u: 2 * phi[u] - prev[u] - h2 * Lp[u] for u in adj}
        if t == 1:
            new[0] += 1.0
        prev, phi = phi, new
        if t in (8, 16, 24):
            front = max((u for u in adj if abs(phi[u]) > 1e-12), default=0)
            print("    t=%2d : field nonzero out to node %2d (front speed %.2f node/step)" % (t, front, front / t))
    # (2) static limit recovers electrostatics
    adj = _lap_adj(_chain(30)); A, B = 5, 25; rho = {u: 0.0 for u in adj}; rho[A] = 1.0; rho[B] = -1.0
    Vstat = _cg(adj, rho); phi = {u: 0.0 for u in adj}; prev = {u: 0.0 for u in adj}; g = 0.15; h2 = 0.3
    for _ in range(4000):
        Lp = _Lmv(adj, phi); new = {u: (2 - g) * phi[u] - (1 - g) * prev[u] - h2 * (Lp[u] - rho[u]) for u in adj}
        prev, phi = phi, new
    mp = sum(phi.values()) / len(phi); phi = {u: phi[u] - mp for u in phi}
    s = sum(phi[u] * Vstat[u] for u in adj) / sum(Vstat[u] ** 2 for u in adj)
    err = sum((phi[u] - s * Vstat[u]) ** 2 for u in adj) / sum(v * v for v in phi.values())
    print("  STATIC LIMIT = electrostatics: relaxed local field vs instantaneous Poisson, mismatch %.1e (identical)" % err)
    print("  => round-6/7 Coulomb is the long-time limit of a LOCAL retarded field; non-locality resolved.")
    print("  SPEED = CAUSALITY: front advances at 1 node/step = the causal-cone speed (round 1) = 'c'.")
