"""The free gauge quantum (photon) and the radiation sector: a chargeless loop, propagating at the causal speed.

This consolidates the §6.7 radiation sector and incorporates the "clean photon" finding. The gauge field
(§6.1, §6.6) lives as a U(1) phase on edges; its gauge-invariant content is the holonomy around loops
(§6.2). Two kinds of loop excitation are possible, and they are physically opposite:

  CHARGED loop -- a loop whose holonomy is nonzero (e.g. a rail closed by one phased back-edge): it is a
  source. Between charged loops the static force is the emergent-graph effective resistance R(d), which on
  the keystone GROWS ~ linearly (R(d) ~ d^~1, confining; see s6_3) -- a massive, confining interaction.

  CHARGELESS loop (the PHOTON) -- a neutral 2-cycle (v,w,phi),(w,v,-phi) dangling on a fresh node w. Its
  holonomy is exactly 0 for ANY phi (verified below, and basis-independent because the two phases cancel
  around the 2-cycle). So it carries NO charge and sources NO static force: it is a free, massless,
  chargeless excitation of the gauge field -- a photon-like quantum. Creating/absorbing such loops changes
  b1 (the loop count) but adds no charge: the free gauge field's quanta come and go freely.

  HONEST CORRECTION to the original investigation. That note inferred "photons are Wilson-energy-free" from
  the spanning-tree Wilson action S = sum (1 - cos(holonomy)) being unchanged. But S computed over a
  spanning-tree cycle basis is BASIS-DEPENDENT: for one fixed graph it varies under edge reordering (shown
  below). A graph has no canonical 2-cell (plaquette) structure, so a Wilson "energy" is not well defined on
  it; the robust, basis-independent invariants are the holonomies / total charge. The sound statement is
  therefore: the neutral 2-cycle has zero holonomy -> zero charge -> no static force. (Energy-free is not a
  basis-independent claim on a bare graph.)

THE PHOTON'S DYNAMICS (rounds 10-11, on an auxiliary 2D lattice). Made dynamical, this chargeless
excitation propagates: the discrete damped-wave (telegrapher) equation on the rule's own Laplacian has a
sharp causal front advancing at the substrate's causal speed (s6_5_retarded_field), and an oscillating
dipole emits an outward Poynting flux that is zero before the wavefront and sustained after (s6_4). So the
radiation sector is: a massless chargeless photon (free quantum), a confining static force between charges,
and finite-speed propagating radiation. Polarization and dispersion remain OPEN.

STATUS = PARTIAL. NATIVE and measured: the neutral 2-cycle has zero holonomy (no charge, no static force);
the basis-dependence of spanning-tree S. The propagation/radiation pieces are PARTIAL toy-lattice
demonstrations (rounds 10-11), not native keystone radiation. Pure Python.
"""
import math
import random
from collections import deque, Counter

STATUS = "PARTIAL"
TITLE = "The photon = chargeless gauge loop (holonomy 0, no force); radiation propagates at the causal speed"


def _holonomies(edges):
    par = {}
    def find(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    treeadj = {}; nontree = []
    for i, (u, v, p) in enumerate(edges):
        if find(u) != find(v):
            par[find(u)] = find(v)
            treeadj.setdefault(u, []).append((v, i, 1.0)); treeadj.setdefault(v, []).append((u, i, -1.0))
        else:
            nontree.append(i)
    def ps(a, b):
        seen = {a: 0.0}; dq = deque([a])
        while dq:
            x = dq.popleft()
            if x == b:
                return seen[x]
            for (nb, e, s) in treeadj.get(x, []):
                if nb not in seen:
                    seen[nb] = seen[x] + s * edges[e][2]; dq.append(nb)
        return seen.get(b, 0.0)
    return [edges[i][2] + ps(edges[i][1], edges[i][0]) for i in nontree]


def _S(edges):
    return sum(1.0 - math.cos(h) for h in _holonomies(edges))


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  1. PHOTON = neutral 2-cycle (v,w,phi),(w,v,-phi): holonomy is 0 for ANY phi -> no charge, no force.")
    for phi in (0.3, 1.0, 2.5):
        h = _holonomies([(0, 1, phi), (1, 0, -phi)])
        print("     phi=%.1f : holonomies=%s" % (phi, [round(x, 6) for x in h]))
    h = _holonomies([(i, i + 1, 0.0) for i in range(5)] + [(3, 2, 1.0)])
    print("  2. contrast -- a CHARGED loop (rail + one phased back-edge) has holonomy %s (a source; confining force, s6_3)."
          % [round(x, 4) for x in h])
    base = [(i, i + 1, 0.0) for i in range(8)] + [(3, 2, 1.0), (6, 5, -0.7), (2, 8, 0.5), (8, 2, -0.5)]
    vals = []
    for seed in range(6):
        e = base[:]; random.Random(seed).shuffle(e); vals.append(round(_S(e), 4))
    print("  3. honest check -- spanning-tree Wilson S of ONE fixed graph under 6 edge-orderings: %s" % vals)
    print("     => S %s (basis-DEPENDENT); the robust invariant is holonomy/charge, not a graph Wilson energy."
          % ("varies" if len(set(vals)) > 1 else "is invariant"))
    print("  4. dynamics (rounds 10-11, auxiliary lattice): the chargeless mode propagates at the causal speed")
    print("     (telegrapher eq, s6_5_retarded_field) and an oscillating dipole radiates (Poynting flux, s6_4).")
    print("  => gauge sector: a massless chargeless PHOTON, a confining static force between charges, finite-c radiation.")
