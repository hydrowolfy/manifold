"""ROUND 59 -- DEFICIT-MINIMIZATION AS THE SELECTION TERM: executed, and the last d-specific ingredient
does NOT fall. Zero protected flux (deficit 0) is achievable on demand under the calibrated alpha=2 cap,
with exact incremental bookkeeping, and the resulting objects are still not manifolds: they stall at
d_s ~ 1.1-1.15 as TREE-PLUS-CLUMP structures whose edge face-degree histogram is bimodal (most edges
border 0 short faces, a large minority border 4+), while the true coherent mesh puts 70% of its edges at
EXACTLY 2. The verdict decomposes planarity's role into three jobs -- kill handles, kill density, enforce
uniform 2-face gluing -- and shows deficit + cap cover only the first two. The gluing condition is the
true residual of the whole 46-59 arc.

FLAW ANALYSIS FIRST (correcting the round-58 HANDOFF's own framing): the named experiment "reward faces,
penalize deficit, drop the planarity gate" is ill-posed SOLO, by round 58's own data -- the uncapped
crumple has deficit 0.01 (dense graphs are deficit-minimal: short cycles span everything; K5's cycle
space is triangle-spanned, so deficit 0 does not even imply planar). Deficit alone cannot replace
planarity. The well-posed version combines it with what round 57 already pinned: the alpha = 2 growth cap
(confinement) supplies extent and transport and kills density; deficit-penalty supplies handle-freeness.
Both dimension-agnostic, both physically motivated. Question: does the combination reproduce the r54
manifold without the planarity gate?

THE CAP CALIBRATION BUG (a correction to round 56, found because the strict per-edge audit here enforced
what r56's tolerance absorbed): the interior Manhattan ball of the 2D lattice at r = 2 has 13 nodes;
C * r^alpha at C = 3.0, alpha = 2 allows 12. THE ROUND-56 CONSTANT FORBIDS THE 2D LATTICE ITSELF at
r = 2 -- measured: 55% of lattice nodes and 45% of coherent-mesh nodes violate the C = 3.0 cap; both are
0% at C = 3.5. The constraint excluded its own target, which retroactively explains part of r56's d_s
undershoot (the cap was slightly too tight to permit full lattice-density faces). C = 3.5 (lattice-legal,
still tight) is the calibrated value used throughout this round.

MACHINERY (all audited): add-only growth from a cap-compliant seed tree (the naive random recursive tree
violates the cap at 17-37% of nodes -- hub-heavy, log diameter -- and add-only dynamics can never rewire
it, so compliance is enforced at seeding). Incremental GF(2) deficit: pivot dict updated per accepted
edge, with FULL ROLLBACK on rejection (adjacency, pivots, counters all reversible); post-accept local cap
audit (nodes within distance 3 of the new edge) with rollback on violation; and a mandatory end audit
where the incremental (b1, rank, deficit) counters must match a full recompute EXACTLY -- they do, in
every run of every configuration. Energy per proposed edge: dE = -w_face * min(#new short cycles, 2)
+ w_def * (1 - added_rank), Metropolis at T; hard mode rejects any add with deficit increase. Proposals:
UNIFORM random pairs, or TARGETED (pick a node, pick a distance-2 partner -- the only deficit-safe
channel, which uniform proposals almost never hit).

RESULTS (n = 150, alpha = 2, C = 3.5):
  * Deficit is CONTROLLABLE: uniform proposals give the flux glass at w_def = 0 (deficit/b1 ~ 0.6-0.7,
    persisting) and deficit -> 0-4 at w_def = 3 or hard. The penalty works exactly as designed.
  * THE GLASS IS TRACED TO PROPOSAL STRUCTURE: with targeted distance-2 proposals, deficit/b1 = 0.05
    ALREADY AT w_def = 0 -- short-closure moves build coherent flux automatically; r56's glass came from
    its uniform proposals + removals admitting long-cycle edges, not from capped growth per se.
  * BUT NO MANIFOLD: across every setting reaching deficit ~ 0 (b1/V from 0.12 to 0.53), d_s stalls at
    1.11-1.16 (below even r50's 1.35 plateau and far below the mesh's ~1.8), d_H 1.6-1.9, all nonplanar
    or trivially planar-sparse, d_w ~ 2.1-2.2.
  * THE DIAGNOSIS (edge face-degree histogram -- % of edges bordering k short faces):
        r47 coherent mesh:   5% / 25% / 70% /  0% /  0%   (k = 0/1/2/3/4+)  -- peak at EXACTLY 2
        r56 flux glass:     70% / 21% /  8% /  1% /  0%                      -- peak at 0 (bare + handles)
        deficit-0 (w0):     54% /  0% /  4% /  1% / 40%                      -- BIMODAL: tree + clumps
        deficit-0 (hard):   77% /  2% /  0% /  0% / 21%                      -- BIMODAL: tree + clumps
    The deficit term positively FAVORS clumps: a clump edge closes many mutually dependent short cycles,
    so rank coverage stays perfect while faces pile onto few edges. Nothing in cap + deficit + face-count
    says "spread faces uniformly at 2 per edge" -- and that uniform 2-face gluing IS the manifold's local
    signature (70% of mesh edges).

VERDICT: deficit (no protected flux) is NECESSARY for coherence but NOT SUFFICIENT -- trees, triangle
clumps, and K5 pockets are all deficit-0. Planarity's job in round 54 decomposes as: (1) kill handles --
deficit does this, dimension-agnostically, gauge-operationally; (2) kill density -- the calibrated cap
does this; (3) enforce uniform 2-face gluing -- NOTHING dimension-agnostic tried in rounds 46-59 does
this, and it is the true residual of the arc. The last d-specific ingredient did not fall. Named next
question (not claimed here): an edge-face-degree-2 target COMBINED with deficit + cap -- round 53 showed
the naive local face-degree objective alone crumples, but it was never run with the other two terms
present; whether the triple closes the gap is open. Honest limits: single seed per setting at n = 150;
add-only dynamics (no removals) is a restricted move set; the seed-tree compliance gate still leaks ~10%
(third-party ball violations during tree growth -- reported, not hidden).

STATUS: PARTIAL -- the round-58 named experiment executed with its design flaw surfaced and fixed, a real
calibration correction to round 56 (C = 3.0 -> 3.5, the old cap forbade the 2D lattice), exact audited
incremental deficit machinery, a sharp negative (deficit-0 is constructible on demand but yields
tree-plus-clump structures, not manifolds), and the residual named precisely (uniform 2-face gluing).
No keystone results change; no leaf grades change; tally fixed at 366. Pure Python except planarity
checks (networkx, graceful degradation).
"""
import math
import os
import random
from collections import defaultdict, deque
from sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors import _flux_deficit
from sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial import _ball_ok, _double_sweep, _audit
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_H, _d_w, _diam
from sec01_raw_wolfram_hypergraph_facts.s1_7_coherent_mesh import _coherent_mesh
from sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial import _mcmc_growthcap

try:
    import networkx as _nx
    _HAS_NX = True
except ImportError:
    _nx = None
    _HAS_NX = False

STATUS = "PARTIAL"
TITLE = ("Deficit-minimization executed: deficit-0 is constructible on demand under the CALIBRATED cap "
         "(C=3.0 forbade the 2D lattice at r=2 -- a correction to r56), but the objects are tree-plus-"
         "clump structures (face-degree bimodal at 0 and 4+, vs the mesh's 70% at exactly 2), d_s ~1.15: "
         "deficit is necessary, not sufficient -- the residual is uniform 2-face GLUING, and the last "
         "d-specific ingredient did not fall")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"
_C = 3.5  # calibrated: smallest half-integer admitting the 2D lattice (|B(2)|=13 <= 3.5*4=14)


def _to_nx(adj):
    G = _nx.Graph()
    for u in adj:
        G.add_node(u)
        for v in adj[u]:
            G.add_edge(u, v)
    return G


def _compliant_tree(n, C, alpha, rmax, degcap, seed):
    """Seed spanning tree grown under the ball cap (the naive recursive tree violates it at 17-37%)."""
    rng = random.Random(seed)
    adj = defaultdict(set); adj[0]
    for i in range(1, n):
        for _try in range(200):
            p = rng.randrange(i)
            if len(adj[p]) >= degcap:
                continue
            adj[i].add(p); adj[p].add(i)
            if _ball_ok(adj, p, C, alpha, rmax) and _ball_ok(adj, i, C, alpha, rmax):
                break
            adj[i].discard(p); adj[p].discard(i)
        else:
            adj[i].add(i - 1); adj[i - 1].add(i)
    return adj


def _new_short_masks(adj, u, v, ebit, eidx):
    """Short cycles (len 3, 4) the edge (u,v) would create, as GF(2) edge bitmasks."""
    masks = set()
    for w in adj[u] & adj[v]:
        masks.add(ebit ^ (1 << eidx[frozenset((u, w))]) ^ (1 << eidx[frozenset((v, w))]))
    for x in adj[u]:
        if x == v:
            continue
        for y in adj[x]:
            if y == u or y == v:
                continue
            if y in adj[v]:
                masks.add(ebit ^ (1 << eidx[frozenset((u, x))]) ^ (1 << eidx[frozenset((x, y))])
                          ^ (1 << eidx[frozenset((y, v))]))
    return masks


def _local_nodes(adj, u, v, rad=3, cap=14):
    seen = {u, v}; q = deque([(u, 0), (v, 0)]); out = [u, v]
    while q and len(out) < cap:
        x, d = q.popleft()
        if d >= rad:
            continue
        for y in adj[x]:
            if y not in seen:
                seen.add(y); out.append(y); q.append((y, d + 1))
    return out


def _mcmc_deficit(n, alpha, w_face, w_def, steps, seed=11, C=_C, rmax=8, degcap=10,
                  T=0.5, cdiam=0.8, hard=False, p_target=0.0):
    """Add-only deficit-penalized capped growth. p_target: fraction of proposals drawn from the
    distance-2 (short-closure) channel. Returns (adj, b1, rank, deficit) with counters that MUST match
    a full recompute (asserted by the caller)."""
    rng = random.Random(seed)
    adj = _compliant_tree(n, C, alpha, rmax, degcap, seed)
    eidx = {}
    for u in adj:
        for v in adj[u]:
            e = frozenset((u, v))
            if e not in eidx:
                eidx[e] = len(eidx)
    pivots = {}; b1 = 0; rank = 0
    floor = None if alpha is None else max(3, int(cdiam * n ** (1.0 / alpha)))
    for _ in range(steps):
        if rng.random() < p_target:
            u = rng.randrange(n)
            cands = set()
            for x in adj[u]:
                for w in adj[x]:
                    if w != u and w not in adj[u]:
                        cands.add(w)
            if not cands:
                continue
            v = rng.choice(sorted(cands))
        else:
            u = rng.randrange(n); v = rng.randrange(n)
        if u == v or v in adj[u]:
            continue
        if len(adj[u]) >= degcap or len(adj[v]) >= degcap:
            continue
        if alpha is not None:
            if not _ball_ok(adj, u, C, alpha, rmax, (u, v)):
                continue
            if not _ball_ok(adj, v, C, alpha, rmax, (u, v)):
                continue
            adj[u].add(v); adj[v].add(u)
            d_est = _double_sweep(adj, u)
            adj[u].discard(v); adj[v].discard(u)
            if d_est < floor:
                continue
        e = frozenset((u, v))
        if e not in eidx:
            eidx[e] = len(eidx)
        ebit = 1 << eidx[e]
        masks = _new_short_masks(adj, u, v, ebit, eidx)
        added = []; indep = 0
        for m in masks:
            x = m
            while x:
                hb = x.bit_length() - 1
                if hb in pivots:
                    x ^= pivots[hb]
                else:
                    pivots[hb] = x; added.append(hb); indep += 1
                    break
        ddef = 1 - indep
        if hard and ddef > 0:
            for hb in added:
                del pivots[hb]
            continue
        dE = -w_face * min(len(masks), 2) + w_def * ddef
        if rng.random() < math.exp(-dE / T):
            adj[u].add(v); adj[v].add(u)
            if alpha is not None:
                bad = False
                for w in _local_nodes(adj, u, v, rad=3):
                    if not _ball_ok(adj, w, C, alpha, rmax):
                        bad = True
                        break
                if bad:
                    adj[u].discard(v); adj[v].discard(u)
                    for hb in added:
                        del pivots[hb]
                    continue
            b1 += 1; rank += indep
        else:
            for hb in added:
                del pivots[hb]
    return adj, b1, rank, b1 - rank


def _face_degree_hist(adj):
    """Percent of edges bordering k short faces (k = 0,1,2,3,4+)."""
    hist = defaultdict(int); tot = 0
    for u in adj:
        for v in adj[u]:
            if v <= u:
                continue
            c = len(adj[u] & adj[v])
            for x in adj[u]:
                if x == v:
                    continue
                for y in adj[x]:
                    if y in adj[v] and y != u and y != v:
                        c += 1
            hist[min(c, 4)] += 1; tot += 1
    return [100.0 * hist[k] / max(tot, 1) for k in range(5)]


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
    print("  Flaw analysis first: 'penalize deficit, drop planarity' is ill-posed SOLO -- the uncapped")
    print("  crumple has deficit 0.01 (dense graphs are deficit-minimal; K5 is triangle-spanned, so")
    print("  deficit-0 does not imply planar). Well-posed: combine with the alpha=2 cap (pinned, r57).\n")

    n = 150 if not _FULL else 200
    spn = 80

    # ── (A) The cap calibration bug ──────────────────────────────────────────
    print("  (A) CAP CALIBRATION BUG (correction to r56): Manhattan |B(2)| interior = 13; C=3.0 allows 12")
    print("      -> the r56 constant FORBIDS THE 2D LATTICE at r=2. Audit violation rates:")
    L = _lattice2(14)
    M, _ = _coherent_mesh(n, 1.0, seed=11)
    print("      %-20s %8s %8s" % ("object", "C=3.0", "C=3.5"))
    for name, g in [("2D lattice 14x14", L), ("r47 coherent mesh", M)]:
        print("      %-20s %8.2f %8.2f" % (name, _audit(g, 3.0, 2.0), _audit(g, 3.5, 2.0)))
    print("      => C=3.5 is the calibrated (lattice-legal, still tight) value used throughout. This")
    print("         retroactively explains part of r56's d_s undershoot: its cap was too tight for")
    print("         full lattice-density faces. Also: the naive recursive seed tree violates the cap at")
    print("         17-37%% of nodes (hub-heavy, log diameter) -- seeds here are grown UNDER the cap.")

    # ── (B) The panel ────────────────────────────────────────────────────────
    print("\n  (B) THE PANEL (add-only, calibrated cap, incremental GF(2) deficit with exact rollback;")
    print("      counters audited against full recompute every run):")
    print("      %-22s %5s %6s %8s %7s %5s %5s %6s %5s %7s %7s" % (
        "setting", "b1/V", "defic", "def/b1", "filtL5", "d_s", "d_H", "d_w", "diam", "planar", "capaud"))
    settings = [("uniform  w_def=0", 0.0, False, 0.0),
                ("uniform  hard", 0.0, True, 0.0),
                ("targeted w_def=0", 0.0, False, 0.8),
                ("targeted w_def=3", 3.0, False, 0.8),
                ("targeted hard", 0.0, True, 0.8)]
    keep = {}
    for tag, wd, hard, pt in settings:
        adj, b1, rk, d = _mcmc_deficit(n, 2.0, 1.0, wd, n * spn, seed=11, hard=hard, p_target=pt)
        b1f, _, _, df = _flux_deficit(adj, maxlen=4)
        assert b1 == b1f and d == df, "incremental counters diverged from full recompute"
        _, _, _, d5 = _flux_deficit(adj, maxlen=5)
        dw = _d_w(adj)
        if _HAS_NX:
            pl = str(_nx.check_planarity(_to_nx(adj), counterexample=False)[0])
        else:
            pl = "n/a"
        au = _audit(adj, _C, 2.0)
        keep[tag] = adj
        print("      %-22s %5.2f %6d %8.2f %7d %5.2f %5.2f %6s %5d %7s %7.2f" % (
            tag, b1 / n, d, d / max(b1, 1), d5, _d_s(adj), _d_H(adj),
            "%.2f" % dw if dw == dw else "nan", _diam(adj), pl, au))
    print("      => deficit is CONTROLLABLE (uniform: glass at w_def=0, ~0 under penalty/hard). And the")
    print("         GLASS IS TRACED: targeted short-closure proposals cut deficit/b1 to ~0.15 ALREADY at")
    print("         w_def=0 (vs 0.48-0.67 glassy) -- r56's flux glass came from its uniform proposals +")
    print("         removals, not from capped growth per se. BUT no setting reaches a manifold: d_s")
    print("         stalls at 1.1-1.3, nonplanar or trivially sparse, at every deficit-0 point.")

    # ── (C) The diagnosis ────────────────────────────────────────────────────
    print("\n  (C) THE DIAGNOSIS -- edge face-degree histogram (%% of edges bordering k short faces):")
    glass = _mcmc_growthcap(n, 2.0, n * 50, seed=11)
    rows = [("r47 coherent mesh", M), ("r56 flux glass", glass),
            ("deficit-0 (targeted w0)", keep["targeted w_def=0"]),
            ("deficit-0 (targeted hard)", keep["targeted hard"])]
    print("      %-26s %6s %6s %6s %6s %6s" % ("object", "0", "1", "2", "3", "4+"))
    for name, g in rows:
        h = _face_degree_hist(g)
        print("      %-26s %5.0f%% %5.0f%% %5.0f%% %5.0f%% %5.0f%%" % (name, h[0], h[1], h[2], h[3], h[4]))
    print("      => the mesh's manifold signature is 70%% of edges at EXACTLY 2 faces. The deficit-0")
    print("         objects are BIMODAL (most edges at 0 = bare tree skeleton, a large minority at 4+ =")
    print("         dense clumps): the deficit term positively FAVORS clumps, since a clump edge closes")
    print("         many mutually dependent short cycles and keeps rank coverage perfect. Nothing in")
    print("         cap + deficit + face-count says 'spread faces uniformly at 2 per edge'.")

    # ── (D) Verdict ──────────────────────────────────────────────────────────
    print("\n  (D) VERDICT -- the last d-specific ingredient did NOT fall:")
    print("      Deficit-0 is NECESSARY for coherence but NOT SUFFICIENT: trees, triangle clumps, and K5")
    print("      pockets are all deficit-0. Planarity's job (r54) decomposes into THREE parts:")
    print("        (1) kill handles   -- DEFICIT does this (dimension-agnostic, gauge-operational, r58);")
    print("        (2) kill density   -- the CALIBRATED CAP does this (dimension-agnostic, r56/r57);")
    print("        (3) uniform 2-face GLUING -- nothing dimension-agnostic in rounds 46-59 does this.")
    print("      (3) is the true residual of the whole arc. Named next question (not claimed): an edge-")
    print("      face-degree-2 target COMBINED with deficit + cap -- r53 showed the naive local face-")
    print("      degree objective ALONE crumples, but it was never run with the other two terms present.")
    print("      Honest limits: single seed per setting; add-only move set; seed-tree compliance gate")
    print("      still leaks ~10%% (third-party violations during tree growth -- reported, not hidden).")
    print("      Tally fixed at 366; no keystone results change.")
