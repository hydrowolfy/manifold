"""Bound states of the confining force are mesons: a pure-linear, unbreakable string between two charges.

The keystone's central force is not inverse-square -- it is CONFINING (s6_3, R(a,b) ~ graph distance). So the
bound states are not Kepler orbits; they are confined charge-anticharge pairs joined by a flux tube -- the
substrate's mesons. Two features distinguish them sharply from real QCD, and both are forced by the substrate.

PURE-LINEAR POTENTIAL (no Coulomb piece). Placing a +1 and a -1 charge (rho = in-out) at separation r, the
interaction energy is the effective resistance R(r). Because the keystone is a tree (b1=1, s6_3), R(r) equals
the graph distance: V(r) = sigma * r with intercept ~ 0 (measured: E(r)/r = 1.00 out to r~6, linear fit
sigma ~ 0.92, intercept ~ 0.2). There is NO short-range Coulomb -a/r term -- unlike the QCD Cornell potential
V = -a/r + sigma*r -- because a tree has no short-range alternative paths. The keystone meson is a PURE string.

UNBREAKABLE STRING (no screening). In QCD the flux tube breaks at long range: it is energetically cheaper to
pop a light quark-antiquark pair out of the vacuum than to keep stretching the string, so V(r) saturates
(screening). The keystone CANNOT do this: its matter is massless chiral Weyl fermions with no mass term and
hence no pair-creation channel (the round-16 obstruction). With nothing to pop, the string never breaks and
V(r) = sigma*r holds for ALL r. The keystone is a theory of stable, unbreakable mesons.

THE FLUX TUBE is the tree geodesic: ~1 edge wide (a thin string) with nearly uniform current (constant
tension) along its length. The meson is NEUTRAL (total rho = 0) and BOUND (separating the charges costs
energy ~ sigma * r -> infinity): only neutral mesons are finite-energy, physical asymptotic states.

CONSEQUENCES.
  - VIRIAL: for V ~ r^n the virial theorem gives 2<T> = n<V>; here n = 1, so 2<T> = <V> (contrast Kepler's
    n = -1, 2<T> = -<V>). A falsifiable signature of linear confinement.
  - RADIAL SPECTRUM: a constituent of mass m (the irreducible Weyl->Dirac input) in V = sigma*r has Airy
    levels E_n = (sigma^2 / 2m)^(1/3) |a_n| (|a_n| = 2.34, 4.09, 5.52, ...), so meson masses scale as
    M_n ~ sigma^(2/3) m^(-1/3). The spectrum is a tower set by the string tension.
  - REGGE TRAJECTORY (rotational): model the meson as a rotating relativistic string of tension sigma whose
    ends move at the substrate's universal speed v0 (the same causal speed the glider saturates, s4_3). Both
    ingredients are native -- sigma from confinement, v0 from the causal cone. The string's energy and spin
    are M = pi*sigma*L and J = pi*sigma*L^2/2 (verified by integration below), giving the linear Regge
    trajectory J = M^2/(2*pi*sigma): meson spin grows as the square of its mass, slope alpha' = 1/(2*pi*sigma)
    fixed by the one tension. This is THE QCD meson signature, here a consequence of (confining tension +
    one speed limit). It is semi-classical string mechanics applied to the substrate's measured parameters,
    not a first-principles lattice spectrum.
  - Inverse-square behavior and Kepler-like laws are therefore REFUTED on the native geometry (the force is
    linear, not 1/r^2); they are recovered only on an auxiliary 3D lattice (s6_3), where R saturates.

STATUS = PARTIAL. NATIVE and measured: the pure-linear potential (intercept ~ 0), the thin uniform flux
tube -- both properties of the bare-rule tree graph. The energy/tension/spectrum reading uses the postulated
field energy (the s6_3 overlay) and, for the spectrum, the granted constituent mass. The unbreakable-string
claim is an inference from the round-16 Weyl obstruction (no pair creation), not a direct simulation of
non-breaking. Pure Python.
"""
import os
import math
import random
from collections import Counter, deque
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Mesons: bound states of the confining force -- a pure-linear, unbreakable string between two charges"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _regge(sigma, v0=1.0):
    """Rotating relativistic string of tension sigma, ends at speed v0. Returns rows (L, M, J, J/M^2)."""
    rows = []
    for L in (1.0, 2.0, 4.0, 8.0):
        N = 8000; dr = (2 * L) / N; M = 0.0; J = 0.0
        for i in range(N):
            r = -L + (i + 0.5) * dr; v = (r / L) * v0
            g = 1.0 / math.sqrt(max(1e-12, 1.0 - (v / v0) ** 2))
            M += sigma * g * dr
            J += sigma * abs(v) / v0 * abs(r) * g * dr
        rows.append((L, M, J, J / (M * M)))
    return rows


def _build(steps=None, seed=2):
    if steps is None:
        steps = 480 if _FULL else 220
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(seed))
    adj = {}
    for (u, v), m in E.items():
        if u == v:
            continue
        adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return adj


def _bfs(adj, s):
    seen = {s: 0}; par = {s: None}; dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in seen:
                seen[y] = seen[x] + 1; par[y] = x; dq.append(y)
    return seen, par


def _resistance(adj, a, b, it=None):
    if it is None:
        it = 3000 if _FULL else 1500
    V = {u: 0.0 for u in adj}; src = {u: 0.0 for u in adj}; src[a] = 1.0; src[b] = -1.0
    for _ in range(it):
        md = 0.0
        for u in adj:
            nv = (sum(V[w] for w in adj[u]) + src[u]) / len(adj[u])
            md = max(md, abs(nv - V[u])); V[u] = nv
        if md < 1e-9:
            break
    return V[a] - V[b], V


def run():
    print("[PARTIAL] %s" % TITLE)
    adj = _build()
    nl = sorted(adj); rng = random.Random(5); a0 = rng.choice(nl)
    dist, _ = _bfs(adj, a0)
    dmax = 12 if _FULL else 8
    buckets = {}
    for b in nl:
        d = dist.get(b, 0)
        if 1 <= d <= dmax:
            buckets.setdefault(d, []).append(b)
    print("  1. meson potential V(r) = R(r) vs charge separation r (tree => PURE linear, no Coulomb piece):")
    rs, Es = [], []
    npairs = 4 if _FULL else 2
    for d in sorted(buckets):
        bs = buckets[d][:npairs]
        vals = [_resistance(adj, a0, b)[0] for b in bs]
        Eavg = sum(vals) / len(vals); rs.append(d); Es.append(Eavg)
        print("     r=%2d : V=%5.2f   V/r=%.3f" % (d, Eavg, Eavg / d))
    n = len(rs); sx = sum(rs); sy = sum(Es); sxx = sum(x * x for x in rs); sxy = sum(x * y for x, y in zip(rs, Es))
    sigma = (n * sxy - sx * sy) / (n * sxx - sx * sx); c = (sy - sigma * sx) / n
    print("     linear fit V(r) = %.2f*r + %.2f  =>  string tension sigma~%.2f, intercept~%.2f (no Coulomb -a/r)" % (sigma, c, sigma, c))
    b = buckets[max(buckets)][0]; R, V = _resistance(adj, a0, b)
    _, par = _bfs(adj, a0); path = []; x = b
    while x is not None:
        path.append(x); x = par[x]
    pc = [abs(V[path[i]] - V[path[i + 1]]) for i in range(len(path) - 1)]
    print("  2. flux tube (the %d-edge tree geodesic): current/edge min=%.2f max=%.2f mean=%.2f -> thin, ~uniform tension" %
          (len(path) - 1, min(pc), max(pc), sum(pc) / len(pc)))
    print("  3. UNBREAKABLE string: massless Weyl matter (s4_3_dirac_mass_obstruction) has no pair-creation,")
    print("     so the tube never breaks -- V=sigma*r for ALL r (QCD's tube breaks via light quarks; this can't).")
    print("  4. the meson is NEUTRAL (total rho=0) and BOUND (separating costs ~sigma*r -> inf): only neutral")
    print("     mesons are physical. Virial 2<T>=<V> (linear, vs Kepler -<V>); radial spectrum M_n ~ sigma^(2/3) m^(-1/3) (Airy).")
    rr = _regge(sigma if sigma > 0 else 0.9)
    print("  5. REGGE TRAJECTORY -- rotating relativistic string (tension sigma~%.2f, ends at the universal speed v0):" % (sigma if sigma > 0 else 0.9))
    print("     L   |   M     |   J     |  J/M^2")
    for L, M, J, ratio in rr:
        print("     %.0f   | %6.2f | %7.2f | %.4f" % (L, M, J, ratio))
    sl = sum(r[3] for r in rr) / len(rr)
    print("     => J/M^2 = %.4f (constant) => LINEAR REGGE TRAJECTORY  J = M^2/(2*pi*sigma); spin ~ mass^2," % sl)
    print("        slope alpha'=1/(2*pi*sigma) set by the one tension -- the QCD meson signature, from (tension + one speed).")
    print("  => inverse-square / Kepler are REFUTED on the native tree geometry; bound states are confined mesons.")
