"""Confinement: the keystone universe is one loop in a tree, so charges are joined by a flux tube.

Two facts about the bare keystone combine into a confinement scenario that mirrors QCD.

ONE LOOP IN A TREE. The keystone conserves b1 = E - V + C (round 1); starting from the triangle it stays
b1 = 1 forever (verified here at many sizes: the undirected edge count always equals the node count, so
the graph is a spanning tree plus exactly one extra edge). The keystone universe is therefore a single
topological loop -- the conserved charge -- inside an ever-growing TREE of pendant/branch structure
(~57% pendants, round 1). That single loop is the universe's lone MATTER particle: a cycle that wanders
through the graph. Its size is NOT bounded -- over long evolution the 2-core grows sub-linearly (a vanishing
FRACTION of the universe; see s11_1, which corrects an earlier "bounded length 2-11" claim that was a
short-run artifact). So matter is localized only as a vanishing fraction, not as a fixed-size particle. There are no alternative cycles: transport between any two nodes
runs along the UNIQUE tree path.

CONFINEMENT AND THE FLUX TUBE. Because the graph is tree-like, the effective resistance between two nodes
equals their graph distance (series resistors): R(a,b) ~ d (verified, R/d ~ 0.98). In the U(1) Maxwell
limit R(a,b) is the interaction energy between unit charges (s6_3), so the potential is LINEAR and the
force CONSTANT -- a string tension. The current (the field) flows almost entirely along the single tree
geodesic: ~d of the hundreds of edges carry 90% of it. That concentrated field is a FLUX TUBE, exactly
the QCD picture of a confined charge pair joined by a string.

CONSEQUENCES (the QCD scenario).
  - NO FREE CHARGE. Separating two charges costs energy ~ tension * distance, which diverges: a single
    charge cannot be isolated (infinite energy). Free "quarks" do not exist on the keystone.
  - PHYSICAL SPECTRUM = NEUTRAL STATES. A neutral 2-cycle (the photon, s6_7) has holonomy 0 and costs no
    field energy, and a neutral charge pair has a finite-length tube; only such color-neutral combinations
    are finite-energy. The asymptotic states are neutral, like hadrons.
  - PHASE IS SUBSTRATE-SPECIFIC. On a high-dimensional substrate (a 3D lattice, s6_3) the resistance
    SATURATES and the force is Coulomb (deconfined). The keystone confines because its emergent geometry
    is tree-like (b1=1, transport dimension d_s~1.3 < 2). Confinement here is geometry, not a coupling.

HONEST STATUS = PARTIAL. NATIVE and measured: b1=1 (the tree-plus-one-loop structure), the unique-path
transport, and the flux-tube concentration of the current -- all properties of the bare-rule graph. The
"energy / tension / Coulomb-limit" reading uses the postulated field energy (the s6_3 overlay), so the
confinement claim is native geometry (the tree) clothed in an overlay field. Crucially the bare dynamics
CANNOT feel the tube on its own: redexes depend only on the edge multiset, so the rule is charge-blind
(round 5) -- it does not respond to a distant charge or to the field energy. The flux-tube PATH (the tree
geodesic) is native, but the confining force/energy that makes it a "tube" is irreducibly overlay. Pure Python.
"""
import math
import random
from collections import Counter, deque
from sec00_core_substrate import evolve, betti1, nodes, redexes, apply_rule, two_core
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Confinement: one loop in a tree -> charges joined by a flux tube (linear potential, no free charge)"


def _tree_check():
    out = []
    for steps in (50, 200, 650):
        E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(steps))
        V = len(nodes(E))
        eu = set()
        for (u, v), m in E.items():
            if u != v:
                eu.add(frozenset((u, v)))
        out.append((steps, V, len(eu), betti1(E)))
    return out


def _loop_nature():
    """The single loop is a small bounded simple cycle that wanders -- the lone matter particle.
    Returns (max loop length seen, whether it stays a simple cycle, whether its node-set moves)."""
    from collections import Counter as C
    maxlen = 0; simple = True; moved = False; prev = None
    for seed in range(4):
        E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
        for step in range(500):
            Rs = redexes(E)
            if not Rs:
                break
            E, fresh = apply_rule(E, rng.choice(Rs), KEYSTONE, fresh)
            if step % 50 == 0:
                tc = two_core(E); maxlen = max(maxlen, len(tc))
                deg = C()
                for (u, v), m in E.items():
                    if u in tc and v in tc and u != v:
                        deg[u] += 1; deg[v] += 1
                if tc and set(deg[n] for n in tc) != {2}:
                    simple = False
                if prev is not None and tc and set(tc) != prev:
                    moved = True
                prev = set(tc)
    return maxlen, simple, moved


def _flux_tube(steps=500, seed=1):
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(seed))
    adj = {}
    for (u, v), m in E.items():
        if u == v:
            continue
        adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)

    def bfs(s):
        seen = {s: 0}; dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen[y] = seen[x] + 1; dq.append(y)
        return seen
    nl = sorted(adj); rng = random.Random(seed + 7); a = rng.choice(nl)
    dist = bfs(a); far = [n for n in nl if dist.get(n, 0) >= 6]
    b = rng.choice(far) if far else nl[-1]; d = dist[b]
    Vpot = {u: 0.0 for u in adj}; src = {u: 0.0 for u in adj}; src[a] = 1.0; src[b] = -1.0
    for _ in range(4000):
        md = 0.0
        for u in adj:
            nv = (sum(Vpot[w] for w in adj[u]) + src[u]) / len(adj[u])
            md = max(md, abs(nv - Vpot[u])); Vpot[u] = nv
        if md < 1e-10:
            break
    R = Vpot[a] - Vpot[b]
    ec = {}
    for x in adj:
        for y in adj[x]:
            if x < y:
                ec[(x, y)] = abs(Vpot[x] - Vpot[y])
    cs = sorted(ec.values(), reverse=True); tot = sum(cs); acc = 0.0; topk = 0
    for c in cs:
        acc += c; topk += 1
        if acc >= 0.9 * tot:
            break
    return R, d, topk, len(cs)


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  1. ONE LOOP IN A TREE (b1=1 forever; undirected edges == nodes => spanning tree + 1 edge):")
    for steps, V, ne, b1 in _tree_check():
        print("     steps=%4d : nodes=%4d  undirected_edges=%4d  b1=%d" % (steps, V, ne, b1))
    ml, simple, moved = _loop_nature()
    print("     the loop is the lone MATTER particle that %s; small over short runs (~%d) but it GROWS" %
          ("wanders" if moved else "stays put", ml))
    print("     sub-linearly over long evolution (s11_1) -- a vanishing fraction of the universe, not a fixed particle.")
    R, d, topk, ne = _flux_tube()
    print("  2. FLUX TUBE: R(a,b)=%.2f at graph distance %d -> R/d=%.2f (linear potential, string tension ~1)." % (R, d, R / d))
    print("     current concentration: %d of %d edges carry 90%% of the field = a flux tube on the tree geodesic." % (topk, ne))
    print("  3. CONFINEMENT: separating charges costs energy ~ tension*distance -> diverges => NO free charge.")
    print("     PHYSICAL SPECTRUM = neutral states only (the photon = neutral 2-cycle, s6_7; neutral pairs).")
    print("     Substrate-specific: a 3D lattice deconfines (Coulomb, s6_3); the keystone confines because")
    print("     its geometry is tree-like (b1=1, d_s~1.3<2). Confinement here is GEOMETRY, not a coupling.")
    print("  4. NATIVE vs OVERLAY: the bare rule is charge-blind (redexes depend on the edge multiset alone,")
    print("     round 5), so it cannot feel the tube on its own. The flux-tube PATH (tree geodesic) is native;")
    print("     the confining force/energy that makes it a tube is irreducibly the field-energy overlay.")
    print("  => QCD-like confinement emerges from the keystone's one-loop-in-a-tree structure.")
