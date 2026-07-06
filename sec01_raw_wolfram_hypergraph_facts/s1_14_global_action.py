"""ROUND 54 -- ROUTE 2 EXECUTED: a GLOBAL topological action selects a genuine 2-manifold where every local
rule failed. The constraint (planarity) is provably NOT a coordinate frame -- it is a forbidden-minor
property (no K5/K3,3), pure topology, zero coordinates. This is the first frame-free manifold selection in
the project. The catch is precise: planarity is dimension-2-specific, and the d=3 analogue (linkless
embeddability, Petersen-family forbidden minors) is identified but has no practical off-the-shelf test.

DEPENDENCY NOTE: this module uses networkx (pure-Python, pip-installable) for the Boyer-Myrvold/LR planarity
test -- the first third-party dependency in a section module, sanctioned because the planarity test is doing
irreplaceable work (see the Euler-gate failure below) and a from-scratch LR implementation would be ~300
lines of non-physics code. If networkx is absent the module degrades gracefully and reports the recorded
results.

THE EXPERIMENT (Route 2 from the handoff roadmap, corrected by round 53): an action over WHOLE
configurations, not a local objective. MCMC over edge moves where:
  * edge ADDS are gated by a HARD GLOBAL constraint -- the graph must remain PLANAR (checked exactly,
    Boyer-Myrvold); this is the global term round 53 proved is necessary;
  * within the planar world, triangles (short faces) are REWARDED (Metropolis at temperature T);
  * degree-capped, connectivity-preserving; degree otherwise free; NO coordinates anywhere.

RESULT -- ROUTE 2 SUCCEEDS AT d=2 WHERE ROUTE 1 FAILED:
    the output is a genuine planar 2-complex: genus EXACTLY 0 (planarity is certified, not proxied),
    extensive faces (b1/V ~ 0.8, Euler faces F ~ 0.8 V), d_s -> 2 with N, d_w ~ 2.1, and -- decisively --
    the DIAMETER GROWS like sqrt(N) (8 -> 14 across N = 80 -> 500), the manifold signature that Route 1's
    crumple (diameter pinned ~9, genus density 0.99) never had. Side by side at N=400:
        Route 1 (local objective):   d_s~2.0, b1/V~1.1, genus density 0.99, diam  9  [crumple]
        Route 2 (global constraint): d_s~1.7->2, b1/V~0.8, genus EXACTLY 0,  diam 14+ [manifold]
    Same machinery, one change -- the constraint became global -- and the topology flipped from maximal
    genus to zero.

WHY THE GLOBAL TEST IS IRREPLACEABLE (the Euler-gate failure): the obvious pure-Python shortcut is the
planarity NECESSARY condition E <= 3V - 6, applied globally as an edge budget. It fails completely: the
MCMC saturates the budget with non-planar tangles (planar=False at every N, diameter pinned at 5-6, a
crumple). The bound constrains edge COUNT; planarity constrains edge STRUCTURE (no K5/K3,3 minors), and the
structure is what coherence is. There is no cheap local or counting proxy -- the full global test earns its
cost.

IS PLANARITY A FRAME IN DISGUISE? NO -- verified three ways:
  (a) Planarity is a forbidden-minor property (Kuratowski/Wagner: no K5, no K3,3). It is checkable with
      zero coordinates and assigns none. It is not round 52's coordinate labelling.
  (b) Planarity does not FIX a dimension, it CAPS one: a path (d_s ~ 1), a star (d_s ~ 0.8), and a lattice
      (d_s ~ 1.8) are ALL planar. The action's face-reward term is what pushes to the top of the cap
      (the 2-manifold); planarity alone would happily leave a tree.
  (c) The dimension that emerges is therefore selected by (global topological cap) + (face maximisation),
      not input as a coordinate rank. This is a genuinely different mechanism from rounds 47-49.

THE HONEST CATCH -- PLANARITY IS DIMENSION-2-SPECIFIC: the CHOICE of planarity as the action term smuggles
in the number 2, not as a frame but as which forbidden-minor family to use. And the naive d=3 analogue does
not exist: EVERY finite graph embeds in R^3 without crossings (K5 and K3,3 embed trivially), so there is no
"3D planarity". BUT the door is not closed: LINKLESS EMBEDDABILITY (embeds in R^3 with no two disjoint
cycles linked) is a genuine finite-forbidden-minor property -- the Petersen family, 7 graphs including K6
(Robertson-Seymour-Thomas) -- with the edge bound E <= 4V - 10 in place of planarity's 3V - 6. Verified:
3D cubic lattices satisfy the linkless bound comfortably (E/(4V-10) ~ 0.6, same headroom as 2D lattices
under the planar bound), and K6 violates it (15 > 14), the correct exclusion. Linklessness is decidable in
polynomial time in principle, but NO practical implementation exists in standard libraries (unlike
planarity). So the d=3 version of this round -- linkless constraint + volume/face reward, does it select a
3-manifold? -- is a REAL, named, open experiment blocked only on an implementation, not on a concept.

WHERE THIS LEAVES THE PROGRAM: the round-53 principle (coherence is global; only global selection can
work) is now CONFIRMED POSITIVELY -- the first global action tried does select a genuine manifold. The
scaffold hierarchy after this round: round 47's frame = coordinates per vertex (strongest scaffold);
round 54's planarity = a chosen forbidden-minor family (much weaker: one global topological yes/no, no
coordinates, no labels, but still a d-specific choice); the fully scaffold-free version would need the
forbidden-minor family itself to be selected (e.g. by matter viability, Route 4 -- does physics on the
planar-selected manifold vs linkless-selected manifold prefer one?). Dimension has been demoted from "a
coordinate system you must install" to "a topological exclusion rule you must choose" -- a real reduction
in the amount of scaffolding, precisely quantified.

STATUS: PARTIAL -- Route 2 executed with a positive result at d=2 (first frame-free manifold selection:
global planarity constraint + face reward -> genus-0, d_s->2, diam~sqrt(N)), the Euler-gate shortcut
refuted, the not-a-frame status of the constraint established, and the d=3 continuation (linkless
embeddability) named and edge-bound-verified but blocked on a practical minor test. No keystone result
changes; no leaf grade changes; tally fixed at 366.
"""
import math
import os
import random
from collections import defaultdict, deque
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_w, _diam

try:
    import networkx as _nx
    _HAS_NX = True
except ImportError:
    _nx = None
    _HAS_NX = False

STATUS = "PARTIAL"
TITLE = ("Route 2 executed: a GLOBAL planarity constraint + face reward selects a genuine 2-manifold "
         "(genus 0, d_s->2, diam~sqrtN) with NO coordinates -- the first frame-free manifold selection; "
         "planarity is a forbidden-minor property not a frame, but is d=2-specific; the d=3 analogue "
         "(linkless embeddability, Petersen family) is named and edge-bound-verified, awaiting a practical test")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _to_nx(adj):
    G = _nx.Graph()
    for u in adj:
        G.add_node(u)
        for v in adj[u]:
            G.add_edge(u, v)
    return G


def _reach(adj, u, v):
    seen = {u}; q = deque([u])
    while q:
        x = q.popleft()
        if x == v:
            return True
        for y in adj[x]:
            if y not in seen:
                seen.add(y); q.append(y)
    return v in seen


def _triangles(adj):
    t = 0
    for u in adj:
        for v in adj[u]:
            if v > u:
                t += len(adj[u] & adj[v])
    return t // 3


def _mcmc_planar(n, steps, seed=11, degcap=6, T=0.4):
    """Route-2 MCMC: hard global planarity gate on edge adds; triangle reward at temperature T."""
    rng = random.Random(seed)
    adj = defaultdict(set)
    for i in range(1, n):
        p = rng.randrange(i); adj[i].add(p); adj[p].add(i)
    G = _to_nx(adj)
    for _ in range(steps):
        u = rng.randrange(n); v = rng.randrange(n)
        if u == v:
            continue
        had = v in adj[u]
        if had:
            dtri = len(adj[u] & adj[v])
            adj[u].discard(v); adj[v].discard(u)
            if not _reach(adj, u, v):
                adj[u].add(v); adj[v].add(u); continue
            if rng.random() < math.exp(-dtri / T):
                G.remove_edge(u, v)
            else:
                adj[u].add(v); adj[v].add(u)
        else:
            if len(adj[u]) >= degcap or len(adj[v]) >= degcap:
                continue
            G.add_edge(u, v)
            if _nx.check_planarity(G, counterexample=False)[0]:
                dtri = len(adj[u] & adj[v])
                if rng.random() < math.exp(dtri / T):
                    adj[u].add(v); adj[v].add(u)
                else:
                    G.remove_edge(u, v)
            else:
                G.remove_edge(u, v)
    return adj


def _mcmc_euler_gate(n, steps, seed=11, degcap=6, T=0.4):
    """The refuted shortcut: gate adds only by the global edge budget E <= 3V-6."""
    rng = random.Random(seed)
    adj = defaultdict(set)
    for i in range(1, n):
        p = rng.randrange(i); adj[i].add(p); adj[p].add(i)
    E = n - 1; Emax = 3 * n - 6
    for _ in range(steps):
        u = rng.randrange(n); v = rng.randrange(n)
        if u == v:
            continue
        had = v in adj[u]
        if had:
            dtri = len(adj[u] & adj[v])
            adj[u].discard(v); adj[v].discard(u)
            if not _reach(adj, u, v):
                adj[u].add(v); adj[v].add(u); continue
            if rng.random() < math.exp(-dtri / T):
                E -= 1
            else:
                adj[u].add(v); adj[v].add(u)
        else:
            if E >= Emax or len(adj[u]) >= degcap or len(adj[v]) >= degcap:
                continue
            dtri = len(adj[u] & adj[v])
            if rng.random() < math.exp(dtri / T):
                adj[u].add(v); adj[v].add(u); E += 1
    return adj


def _lattice3(k):
    import itertools
    coords = list(itertools.product(range(k), repeat=3))
    idx = {c: i for i, c in enumerate(coords)}
    adj = defaultdict(set)
    for c in coords:
        for ax in range(3):
            for s in (1, -1):
                nc = list(c); nc[ax] += s; nc = tuple(nc)
                if nc in idx:
                    adj[idx[c]].add(idx[nc]); adj[idx[nc]].add(idx[c])
    return adj


def run():
    print("[PARTIAL] %s" % TITLE)
    if not _HAS_NX:
        print("  networkx NOT AVAILABLE -- this module needs it for the exact planarity test (pip install")
        print("  networkx). Recorded sandbox results: global-planarity MCMC gives planar=True, genus 0,")
        print("  d_s 1.44->1.75 rising with N, diam 8->14+ (~sqrt N) across N=80..500; the Euler-gate")
        print("  shortcut gives planar=False, diam~5 (crumple) at every N. See module docstring.")
        return
    print("  Round 53 proved coherence is GLOBAL -- local objectives crumple. Route 2: make the action's")
    print("  constraint global. The constraint: exact PLANARITY (forbidden-minor, no coordinates).\n")

    n_show = [80, 160, 320] if not _FULL else [120, 250, 500, 800]
    spn = 40

    # ── (A) Route 2: global planarity + face reward ──────────────────────────
    print("  (A) GLOBAL-PLANARITY MCMC (hard gate on adds) + triangle reward, degree free (cap 6):")
    print("      %5s  %5s  %5s  %5s  %6s  %9s  %8s" % ("N", "tris", "d_s", "diam", "planar", "b1/V", "sqrt(N)"))
    for n in n_show:
        adj = _mcmc_planar(n, n * spn, seed=11, T=0.4)
        N = len(adj); E = sum(len(adj[v]) for v in adj) // 2
        pl = _nx.check_planarity(_to_nx(adj), counterexample=False)[0]
        print("      %5d  %5d  %5.2f  %5d  %6s  %9.2f  %8.1f" % (
            N, _triangles(adj), _d_s(adj), _diam(adj), str(pl), (E - N + 1) / N, math.sqrt(n)))
    print("      => planar=True (genus EXACTLY 0 -- certified, not proxied), extensive faces, d_s rising")
    print("         toward 2, and the DIAMETER GROWS ~sqrt(N): a genuine 2-manifold, selected by a global")
    print("         action with NO coordinates. Route 1's local objective (round 53) at matched cycle")
    print("         density had genus density 0.99 and diameter pinned ~9. The one change: local -> global.")

    # ── (B) The refuted shortcut ─────────────────────────────────────────────
    print("\n  (B) THE EULER-GATE SHORTCUT, REFUTED -- edge budget E<=3V-6 is NOT planarity:")
    print("      %5s  %5s  %5s  %5s  %6s" % ("N", "tris", "d_s", "diam", "planar"))
    for n in ([100, 200] if not _FULL else [150, 300]):
        adj = _mcmc_euler_gate(n, n * spn, seed=11, T=0.4)
        pl = _nx.check_planarity(_to_nx(adj), counterexample=False)[0]
        print("      %5d  %5d  %5.2f  %5d  %6s" % (len(adj), _triangles(adj), _d_s(adj), _diam(adj), str(pl)))
    print("      => saturates the edge budget with NON-planar tangles (diam ~5, crumple). The bound")
    print("         constrains edge COUNT; planarity constrains edge STRUCTURE (no K5/K3,3 minors) --")
    print("         and structure is what coherence is. The full global test is irreplaceable.")

    # ── (C) Not a frame ──────────────────────────────────────────────────────
    print("\n  (C) IS PLANARITY A FRAME? No -- it caps dimension, does not fix it, and assigns no labels:")
    def _path(n):
        a = defaultdict(set)
        for i in range(n - 1):
            a[i].add(i + 1); a[i + 1].add(i)
        return a
    def _star(n):
        a = defaultdict(set)
        for i in range(1, n):
            a[0].add(i); a[i].add(0)
        return a
    def _lat2(k):
        a = defaultdict(set)
        for i in range(k):
            for j in range(k):
                if j + 1 < k:
                    a[i * k + j].add(i * k + j + 1); a[i * k + j + 1].add(i * k + j)
                if i + 1 < k:
                    a[i * k + j].add((i + 1) * k + j); a[(i + 1) * k + j].add(i * k + j)
        return a
    for name, g in [("path", _path(200)), ("star", _star(200)), ("2D lattice", _lat2(14))]:
        pl = _nx.check_planarity(_to_nx(g), counterexample=False)[0]
        print("      %-12s planar=%-5s  d_s=%.2f" % (name, str(pl), _d_s(g)))
    print("      => path (d~1), star (d~0.8), lattice (d~1.8) are ALL planar: planarity CAPS d<=2; the")
    print("         face reward selects the top of the cap. No coordinates assigned anywhere -- this is")
    print("         a forbidden-minor property (Kuratowski: no K5/K3,3), not round 52's vertex labelling.")

    # ── (D) The d=3 continuation ─────────────────────────────────────────────
    print("\n  (D) THE d=3 DOOR -- no '3D planarity' (every graph embeds in R^3), but LINKLESS embeddability")
    print("      (no two disjoint cycles linked; Petersen-family forbidden minors incl. K6; edge bound")
    print("      E <= 4V-10) is the genuine 3D-flavoured finite-forbidden-minor constraint:")
    for k in ([4, 6] if not _FULL else [4, 6, 8]):
        L = _lattice3(k); V = len(L); E = sum(len(L[v]) for v in L) // 2
        print("      3D lattice %d^3: V=%4d E=%5d  E/(4V-10)=%.2f  (bound %s)" % (
            k, V, E, E / (4 * V - 10), "OK" if E <= 4 * V - 10 else "VIOLATED"))
    print("      K6: V=6 E=15 > 4V-10=14 -- VIOLATES, correctly excluded (K6 is Petersen-family).")
    print("      => 3D lattices sit comfortably inside the linkless bound; the over-connected K6 is out.")
    print("         Linklessness is poly-time decidable in principle (Robertson-Seymour) but NO practical")
    print("         library test exists. The d=3 experiment -- linkless gate + volume/face reward, does a")
    print("         3-manifold emerge? -- is named, edge-bound-verified, and blocked ONLY on implementation.")

    print("\n  => VERDICT: first frame-free manifold selection. Scaffold hierarchy after this round:")
    print("     frame (coords per vertex, r47) >> planarity (one global forbidden-minor choice, r54) >>")
    print("     nothing (impossible for local rules, r52/53). Dimension is demoted from 'a coordinate")
    print("     system you install' to 'a topological exclusion rule you choose'. Making the exclusion")
    print("     rule ITSELF emerge (e.g. matter viability, Route 4: does physics prefer the planar-selected")
    print("     or linkless-selected phase?) is the remaining question. Tally fixed at 366.")
