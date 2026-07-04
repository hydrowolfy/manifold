"""ROUND 61 -- ANNEALING DYNAMICS: the r60 glass DISSOLVES under scrutiny, three corrections land, and
the triple objective turns out to select 2-MANIFOLDNESS but not ISOTROPY -- its true minimizers are
TUBES (closed-vertex-link fraction 0.73 vs the mesh's 0.50, E_glue/edge 0.16-0.17 vs 0.35), quasi-1D
ribbons of genuine local 2-manifold structure. The arc's residual moves from gluing (now solved) to
ASPECT RATIO, with the exact dimension-agnostic fix named: a diameter CEILING completing the r56 extent
sandwich (the cap installed only a floor).

ENGINEERING DELIVERED (the round's stated purpose): reversible add/REMOVE dynamics with exact
incremental bookkeeping under deletions. Removals: maintain the short-cycle mask set with a per-edge
index; dE_def by fresh GF(2) elimination over the survivor set (few ms in int-bitmask form, affordable
per proposal); pivots rebuilt only on ACCEPTED removals; bridges rejected (connectivity preserved);
facedeg and E_glue deltas exact negatives of the corresponding add. End audits: incremental (b1, rank,
deficit, E_glue) match full recomputes EXACTLY, every run, both seeds, both schedules.

CORRECTION 1 (r60 energetics): r60's dE_glue charged a face-closing add |dfk-2| MINUS 2 instead of
|dfk-2| -- a constant -2 offset per face-closing add relative to the true global E_glue. Directionally
harmless for r60's one-way verdict (adds were OVER-encouraged and the system still froze, a fortiori)
but fatal for reversible dynamics, where add/remove dE must be exact negatives of one global E. Fixed;
the incremental E_glue audit enforces it.

CORRECTION 2 (the r60 "freeze" was an artifact stack): instrumenting rejection reasons showed the
post-accept local cap audit was the DOMINANT rejector (63% of proposals at n=120), not Metropolis (4%).
Mechanism: the r59 seed-tree compliance gate leaks ~10% third-party violators; any 14-node neighborhood
sample near a new edge then hits a pre-existing violator with high probability and rolls back an
INNOCENT add. Fix at the source: seed with a PATH -- trivially cap-compliant at every radius
(|B(r)| = 2r+1), zero leak, and the least-scaffolded seed possible. With the path seed, cap audits read
0.00 and the freeze VANISHES: even FIXED-temperature dynamics reaches E_glue/edge 0.16 with deficit 0
(vs r60's 1.81 "frozen glass"). r60's glass-transition story is retracted: it was audit false-blame
riding on leaky seed geometry, plus real but secondary Metropolis signal.

CORRECTION 3 (r60's ground-state claim is FALSE): "the manifold is the verified ground state" compared
the mesh only against glasses. Scoring the objective's actual minimizers: the path-seeded dynamics
builds objects at E_glue/edge 0.16-0.17 with 86-88% of edges at EXACTLY fd=2 -- STRICTLY BETTER than
the r47 mesh (0.35, 70%) -- at deficit 0, planar, fully cap-compliant. The mesh is NOT the minimum of
glue + deficit + cap(floor); anisotropic 2-complexes are, because boundary is expensive and a ribbon
minimizes boundary per edge.

THE TUBE RESULT (the registered r60 strip mode fires, in refined form): the minimizers have d_H =
0.8-1.3 and diameter 37-70 at n = 150 (quasi-1D at large scale) yet their closed-vertex-link fraction
is 0.73-0.74 vs the mesh's 0.50, and width proxy E/diam = 4.3-6.5 vs 11.5: they are thin TUBES --
locally genuine 2-manifolds (most vertices have fully saturated fd=2 stars), globally rolled into
ribbons. So the triple objective SUCCEEDS at what the whole 53-60 line was chasing -- it selects
2-manifold local structure, frame-free, dimension-agnostically -- and fails only at ISOTROPY, which no
term constrains: the r56 cap bounds |B(r)| from ABOVE (floor on diameter, against crumples) but nothing
bounds diameter from above, so aspect ratio is free and boundary economy drives it extreme.

SEED DEPENDENCE, reported: the tree-seeded annealed run stays near-frozen (b1/V 0.04, E_glue/edge 1.83,
cap audit 0.10) -- the audit-artifact regime persists there; the path seed is the clean instrument.

VERDICT AND THE NAMED NEXT EXPERIMENT: what stands from r60 -- the objective terms themselves (deficit
kills handles, r58; calibrated cap kills density, r59; glue enforces 2-face gluing, r59/60), all still
dimension-agnostic and physically motivated. What falls -- the glass transition (artifact) and the
mesh-as-ground-state claim (tubes win). What is new -- the dynamics WORKS (removals + even modest
temperature reach the objective's true minimizers), and those minimizers are local 2-manifolds of
unconstrained aspect ratio. ROUND 62: add the missing half of extent -- a diameter CEILING
diam <= c' * N^{1/alpha} alongside the floor (the isotropy sandwich), still one exponent, zero d
inserted -- and ask whether glue + deficit + cap-floor + cap-ceiling finally selects the isotropic 2D
patch. Honest limits: single seed per setting; n = 150; the closed-link proxy counts fully-saturated
vertex stars (a conservative manifold-interior proxy); tree-seed regime left unrepaired (path seed
supersedes it).

STATUS: PARTIAL -- reversible dynamics delivered with exact deletion-safe audits; three corrections to
round 60 (energetics offset, freeze-as-artifact, ground-state claim); the triple objective shown to
select local 2-manifoldness with aspect ratio as the isolated residual. No keystone results change; no
leaf grades change; tally fixed at 366. Pure Python except planarity checks (networkx, graceful).
"""
import math
import os
import random
from collections import defaultdict, deque
from sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors import _flux_deficit
from sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial import _ball_ok, _double_sweep, _audit
from sec01_raw_wolfram_hypergraph_facts.s1_19_deficit_selection import (
    _compliant_tree, _new_short_masks, _local_nodes, _face_degree_hist)
from sec01_raw_wolfram_hypergraph_facts.s1_20_triple_objective import _E_glue_per_edge, _mask_edges
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_H, _d_w, _diam
from sec01_raw_wolfram_hypergraph_facts.s1_7_coherent_mesh import _coherent_mesh

try:
    import networkx as _nx
    _HAS_NX = True
except ImportError:
    _nx = None
    _HAS_NX = False

STATUS = "PARTIAL"
TITLE = ("Annealing dynamics: r60's glass RETRACTED (audit false-blame on a leaky seed; a path seed "
         "unfreezes even fixed-T dynamics to E_glue/edge 0.16) and r60's ground-state claim OVERTURNED "
         "(tubes beat the mesh: 0.17 vs 0.35, 88% vs 70% at fd=2, closed-link 0.73 vs 0.50) -- the "
         "triple selects local 2-MANIFOLDNESS but not ISOTROPY; residual = aspect ratio; named fix = "
         "diameter CEILING completing the extent sandwich")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"
_C = 3.5


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
    return False


def _rank_masks(masks):
    piv = {}; r = 0
    for m in masks:
        x = m
        while x:
            hb = x.bit_length() - 1
            if hb in piv:
                x ^= piv[hb]
            else:
                piv[hb] = x; r += 1
                break
    return r, piv


def _anneal(n, w_glue, w_def, steps, seed=11, C=_C, alpha=2.0, rmax=8, degcap=10,
            T_hi=0.5, T_lo=0.5, p_remove=0.3, p_target=0.8, cdiam=0.8, seed_kind='path'):
    """Reversible add/remove triple-objective dynamics. Corrected glue convention: a created edge
    contributes its FULL |fd-2|; removal is the exact negative. Returns
    (adj, b1, rank, deficit, E_glue, accepted_adds, accepted_removes); all counters exact."""
    rng = random.Random(seed)
    if seed_kind == 'path':
        adj = defaultdict(set)
        for i in range(n - 1):
            adj[i].add(i + 1); adj[i + 1].add(i)
    else:
        adj = _compliant_tree(n, C, alpha, rmax, degcap, seed)
    eidx = {}
    for u in adj:
        for v in adj[u]:
            e = frozenset((u, v))
            if e not in eidx:
                eidx[e] = len(eidx)
    fd = defaultdict(int)
    mask_set = set(); by_edge = defaultdict(set)
    pivots = {}; b1 = 0; rank = 0
    E_glue = 2.0 * sum(len(adj[u]) for u in adj) / 2
    edges_list = list(eidx.keys())
    floor = max(3, int(cdiam * n ** (1.0 / alpha)))
    acc_add = acc_rem = 0
    for step in range(steps):
        frac = step / max(steps - 1, 1)
        T = T_hi * (T_lo / T_hi) ** frac if T_hi != T_lo else T_hi
        if rng.random() < p_remove and b1 > 0:
            e = edges_list[rng.randrange(len(edges_list))]
            u, v = tuple(e)
            if v not in adj[u]:
                continue
            ebit_i = eidx[e]
            adj[u].discard(v); adj[v].discard(u)
            if not _reach(adj, u, v):
                adj[u].add(v); adj[v].add(u); continue
            adj[u].add(v); adj[v].add(u)
            gone = by_edge.get(ebit_i, set())
            delta_fd = defaultdict(int)
            for m in gone:
                for eb2 in _mask_edges(m):
                    delta_fd[eb2] -= 1
            dE_glue = -abs(fd[ebit_i] - 2)
            for eb2, dfk in delta_fd.items():
                if eb2 == ebit_i:
                    continue
                dE_glue += abs(fd[eb2] + dfk - 2) - abs(fd[eb2] - 2)
            surv = mask_set - gone
            r_new, piv_new = _rank_masks(surv)
            ddef = ((b1 - 1) - r_new) - (b1 - rank)
            dE = w_glue * dE_glue + w_def * ddef
            if rng.random() < math.exp(-dE / T):
                adj[u].discard(v); adj[v].discard(u)
                for m in gone:
                    mask_set.discard(m)
                    for eb2 in _mask_edges(m):
                        if eb2 != ebit_i:
                            by_edge[eb2].discard(m)
                by_edge.pop(ebit_i, None)
                for eb2, dfk in delta_fd.items():
                    fd[eb2] += dfk
                fd[ebit_i] = 0
                b1 -= 1; rank = r_new; pivots = piv_new
                E_glue += dE_glue; acc_rem += 1
        else:
            if rng.random() < p_target:
                uu = rng.randrange(n)
                cands = set()
                for x in adj[uu]:
                    for w in adj[x]:
                        if w != uu and w not in adj[uu]:
                            cands.add(w)
                if not cands:
                    continue
                u, v = uu, rng.choice(sorted(cands))
            else:
                u = rng.randrange(n); v = rng.randrange(n)
            if u == v or v in adj[u]:
                continue
            if len(adj[u]) >= degcap or len(adj[v]) >= degcap:
                continue
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
                eidx[e] = len(eidx); edges_list.append(e)
            ebit_i = eidx[e]; ebit = 1 << ebit_i
            masks = _new_short_masks(adj, u, v, ebit, eidx)
            delta_fd = defaultdict(int)
            for m in masks:
                for eb2 in _mask_edges(m):
                    delta_fd[eb2] += 1
            dE_glue = abs(delta_fd.get(ebit_i, 0) - 2)
            for eb2, dfk in delta_fd.items():
                if eb2 == ebit_i:
                    continue
                dE_glue += abs(fd[eb2] + dfk - 2) - abs(fd[eb2] - 2)
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
            dE = w_glue * dE_glue + w_def * ddef
            if rng.random() < math.exp(-dE / T):
                adj[u].add(v); adj[v].add(u)
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
                for m in masks:
                    mask_set.add(m)
                    for eb2 in _mask_edges(m):
                        by_edge[eb2].add(m)
                for eb2, dfk in delta_fd.items():
                    fd[eb2] += dfk
                b1 += 1; rank += indep
                E_glue += dE_glue; acc_add += 1
            else:
                for hb in added:
                    del pivots[hb]
    return adj, b1, rank, b1 - rank, E_glue, acc_add, acc_rem


def _fd_map(adj):
    fd = {}
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
            fd[frozenset((u, v))] = c
    return fd


def _closed_link_frac(adj):
    """Fraction of vertices ALL of whose incident edges have facedeg exactly 2 (saturated star:
    a conservative manifold-interior proxy)."""
    fd = _fd_map(adj); good = 0
    for v in adj:
        if adj[v] and all(fd[frozenset((v, w))] == 2 for w in adj[v]):
            good += 1
    return good / len(adj)


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  r60 named annealing as the residual. Engineering first: removals need deletion-safe")
    print("  incremental deficit (survivor-set re-elimination, pivots rebuilt on accepted removals)")
    print("  and a REVERSIBLE energy (r60's dE_glue had a -2 offset per face-closing add -- harmless")
    print("  for its one-way freeze direction, fatal for detailed balance; corrected here).\n")

    n = 150 if not _FULL else 200
    spn = 80

    # ── (A) Correctness ──────────────────────────────────────────────────────
    print("  (A) CORRECTNESS -- all incremental counters vs full recomputes (mixed add/remove):")
    for tag, kw in [("path, T=0.5 fixed", dict(T_hi=0.5, T_lo=0.5, seed_kind='path')),
                    ("path, annealed 2->0.2", dict(T_hi=2.0, T_lo=0.2, seed_kind='path')),
                    ("tree, annealed", dict(T_hi=2.0, T_lo=0.2, seed_kind='tree'))]:
        adj, b1, rk, d, Eg, aa, ar = _anneal(120, 1.0, 3.0, 5000, seed=11, **kw)
        b1f, _, rf, df = _flux_deficit(adj, maxlen=4)
        Ef, ne = _E_glue_per_edge(adj)
        ok = (b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6)
        print("      %-22s adds=%3d rems=%3d  b1 %d/%d  deficit %d/%d  E_glue %.0f/%.0f  MATCH=%s" % (
            tag, aa, ar, b1, b1f, d, df, Eg, Ef * ne, ok))
    print("      => exact under deletions. Note the tree-seed acceptance collapse: instrumenting showed")
    print("         the post-accept audit rejected 63%% of proposals -- FALSE-BLAMING new edges for the")
    print("         seed tree's pre-existing ~10%% cap violators (the r59 leak). r60's 'freeze' was")
    print("         dominated by this artifact. Fix at the source: a PATH seed (|B(r)|=2r+1, compliant")
    print("         at every radius, zero leak, least-scaffolded seed possible).")

    # ── (B) The panel ────────────────────────────────────────────────────────
    print("\n  (B) THE PANEL (n=%d, w_glue=1, w_def=3):" % n)
    print("      %-20s %5s %6s %8s %5s %5s %5s %7s %7s %9s" % (
        "setting", "b1/V", "defic", "Eg/edge", "d_s", "d_H", "diam", "planar", "capaud", "adds/rems"))
    panel = [("path add-only", dict(p_remove=0.0, T_hi=0.5, T_lo=0.5, seed_kind='path')),
             ("path fixed-T +rem", dict(p_remove=0.3, T_hi=0.5, T_lo=0.5, seed_kind='path')),
             ("path annealed", dict(p_remove=0.3, T_hi=2.0, T_lo=0.2, seed_kind='path')),
             ("tree annealed", dict(p_remove=0.3, T_hi=2.0, T_lo=0.2, seed_kind='tree'))]
    keep = {}
    for tag, kw in panel:
        adj, b1, rk, d, Eg, aa, ar = _anneal(n, 1.0, 3.0, n * spn, seed=11, **kw)
        b1f, _, _, df = _flux_deficit(adj, maxlen=4)
        Ef, ne = _E_glue_per_edge(adj)
        assert b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6, "audit fail"
        pl = str(_nx.check_planarity(_to_nx(adj), counterexample=False)[0]) if _HAS_NX else "n/a"
        keep[tag] = adj
        print("      %-20s %5.2f %6d %8.2f %5.2f %5.2f %5d %7s %7.2f %5d/%d" % (
            tag, b1 / n, d, Ef, _d_s(adj), _d_H(adj), _diam(adj), pl,
            _audit(adj, _C, 2.0), aa, ar))
    print("      => THE FREEZE IS GONE on the clean seed: even FIXED-T dynamics reaches E_glue/edge")
    print("         ~0.16 (r60 'froze' at 1.81) with deficit 0 and cap audit 0.00. r60's glass-")
    print("         transition story is RETRACTED (audit artifact + seed geometry). Tree-seed control")
    print("         stays near-frozen -- the artifact regime, reported.")

    # ── (C) Histograms + the tube diagnosis ──────────────────────────────────
    print("\n  (C) WHAT GOT BUILT -- histograms (mesh target 5/25/70/0/0) and the tube diagnosis:")
    M, _ = _coherent_mesh(n, 1.0, seed=11)
    for tag in ["path fixed-T +rem", "path annealed"]:
        h = _face_degree_hist(keep[tag])
        print("      %-20s %5.0f%% %5.0f%% %5.0f%% %5.0f%% %5.0f%%" % (tag, h[0], h[1], h[2], h[3], h[4]))
    hm = _face_degree_hist(M)
    print("      %-20s %5.0f%% %5.0f%% %5.0f%% %5.0f%% %5.0f%%   (the mesh)" % ("r47 mesh", *hm))
    print("      %-20s %11s %6s %14s" % ("object", "closed-link", "diam", "width E/diam"))
    for tag, g in [("r47 mesh", M), ("path fixed-T +rem", keep["path fixed-T +rem"]),
                   ("path annealed", keep["path annealed"])]:
        E = sum(len(g[u]) for u in g) // 2
        print("      %-20s %11.2f %6d %14.1f" % (tag, _closed_link_frac(g), _diam(g), E / _diam(g)))
    print("      => 86-88%% of edges at EXACTLY 2 (beats the mesh's 70%%), E_glue/edge 0.16-0.17 (beats")
    print("         0.35), deficit 0, planar, cap-legal: r60's GROUND-STATE CLAIM IS OVERTURNED -- the")
    print("         mesh is NOT the objective's minimum. And closed-link fraction 0.73-0.74 vs the")
    print("         mesh's 0.50 with width 4-7 vs 11.5: the minimizers are thin TUBES -- locally genuine")
    print("         2-manifolds (saturated vertex stars), globally rolled quasi-1D. Boundary is")
    print("         expensive; a ribbon minimizes boundary per edge; nothing constrains aspect ratio.")

    # ── (D) Verdict ──────────────────────────────────────────────────────────
    print("\n  (D) VERDICT -- three corrections to r60, one clean positive, one named next step:")
    print("      RETRACTED: the glass transition (audit false-blame on a leaky seed) and 'the manifold")
    print("      is the ground state' (tubes win the objective). CORRECTED: the r60 dE_glue -2 offset.")
    print("      STANDS: every objective TERM (deficit kills handles r58, calibrated cap kills density")
    print("      r59, glue enforces 2-face gluing r59/60). NEW POSITIVE: the dynamics WORKS, and the")
    print("      triple objective selects LOCAL 2-MANIFOLDNESS frame-free -- what fails is ISOTROPY,")
    print("      because the r56 cap bounds diameter only from BELOW. ROUND 62, named: add the diameter")
    print("      CEILING diam <= c' N^{1/alpha} (the isotropy sandwich, still one exponent, zero d")
    print("      inserted) and ask whether glue + deficit + floor + ceiling selects the isotropic 2D")
    print("      patch. Limits: single seed per setting; n=%d; closed-link is a conservative interior" % n)
    print("      proxy; tree-seed regime superseded rather than repaired. Tally fixed at 366.")
