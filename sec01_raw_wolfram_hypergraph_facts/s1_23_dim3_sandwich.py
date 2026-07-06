"""ROUND 63 -- THE d=3 SANDWICH: the aligned stack (alpha = 3, fd target k = 4) grows cubic-grade
3D bulk from a bare path -- width, diameter, closed-link, and glue energy land ON the 6^3 reference
column, d_H within 0.2 of the cube's own finite-size value -- while the MISALIGNED control (k = 2 under
the same alpha = 3 cap) builds rolled 2D sheet instead, demonstrating that dimension enters the stack
TWICE, as the cap exponent AND the face-degree target, coupled by k = 2(alpha - 1).

THE HONEST COST, stated first: the 2D result (r62) ran on (alpha, k) = (2, 2) with only ONE cap exponent
inserted; d = 3 needs (3, 4). The "zero d inserted" purity is spent: the full dial is the pair
(alpha, k) = (d, 2(d-1)) -- one integer, expressed twice, self-consistently. Still enormously weaker than
a coordinate frame, but the misaligned control shows the coupling is physical, not conventional: k = 2
under a 3D cap yields 79% of edges at fd = 2, closed-link-at-2 of 0.63, d_H 1.93 -- a crumpled SHEET
filling the ball, not a 3-complex. Alpha alone cannot raise dimension; the local cell type must agree.

CALIBRATION -- the reference is WEAK at this size: 6^3 cube (N = 216) has cap audit 0.00 at C = 3.5,
alpha = 3 (octahedral balls: 25 <= 28, 63 <= 94.5) and deficit 0 (unit squares span b1 = 325), but only
44% of edges at the interior value fd = 4, closed-link-at-4 just 0.30, E4/edge 0.66, d_s / d_H 2.39 /
2.25. The cube is mostly SURFACE at N = 216, so "success = match this column" is a LOW bar, and at this N
a genuine 3-manifold is not instrument-distinguishable from a thick slab. diam 15 pins cceil ~ 2.6-2.8.

RESULTS (path seed, w_glue = 1, w_def = 3, w_iso = 2, ceil 16, floor 4, exact audits every run):
  * aligned, annealed n*120:  b1/V 1.34 (ref 1.50), deficit 11, E4/edge 0.45, diam 13, closed4 0.31
    (ref 0.30 -- matched), width 38.8 (ref 36.0 -- matched), fd hist 61% at 4 with a 17% overshoot tail
    at 5-6, d_s 1.79 / d_H 2.07 (ref 2.39 / 2.25). Cubic-grade BULK on every extent metric.
  * aligned, fixed T = 0.5:   deficit 0, closed4 0.44 (above ref), 69% at 4, E4/edge 0.43 -- locally
    cleaner but under-dense (b1/V 1.02) and slab-ish (diam 19, width 22.9): the schedule TRADE -- the
    anneal buys bulk at the cost of handle debris (deficit 11 = contraction chords left uncovered), the
    fixed schedule buys cleanliness at the cost of bulk. Neither end is a manifold.
  * misaligned k = 2, alpha = 3: 79% at fd = 2, closed-link-at-2 0.63, d_H 1.93 -- the sheet. The
    consistency relation k = 2(d-1) has teeth.

RESIDUALS, named with numbers: (i) the fd = 5-6 OVERSHOOT population, ~17% of edges -- the 3D analogue of
r62's fd = 3 defects, enabled by the SYMMETRIC |fd - k| penalty (overshoot costs the same as undershoot;
the dynamics buys interior-like 4s by tolerating over-stacking); candidate fix: asymmetric penalty.
(ii) the deficit-11 handle debris under annealing -- candidate fix: a cold handle-cleanup phase after
contraction. (iii) the d_s gap ~ 0.6 (vs 0.4-0.5 in 2D), plausibly the same defects scattering the walk.
NOT claimed: "a 3D manifold." CLAIMED: a cubic-grade 3-dimensional complex matching a boundary-dominated
reference on extent and gluing columns, with quantified defect populations and a demonstrated two-slot
dimension dial.

DECISIVE TEST NOT YET RUN: N-scaling (512, 1000). If d_s climbs toward 3 and the interior fd = 4 fraction
grows as boundary shrinks, the frame-free 3D result stands and the arc closes. If d_s sticks ~1.8-2.0
while the cube's OWN d_s climbs with N, the defects are thermodynamic and the honest headline is
"cubic-grade complex with irreducible defect density," not a manifold. N = 216 cannot answer this.

HONEST LIMITS: single seed per setting; N = 216 (the reference cube itself reads d_H 2.25); ceiling on
the double-sweep estimate; the r55 minor-universality theorem is NOT contradicted (this route is
non-minor-closed by construction -- that was its design requirement, chosen in r55).

STATUS: PARTIAL -- the d = 3 sandwich executed: aligned stack reaches the cubic reference column on
extent/gluing metrics, misaligned control proves the k = 2(alpha-1) coupling, residual defect
populations quantified, the decisive N-scaling test named and not yet run. No keystone results change; no
leaf grades change; tally fixed at 366.
"""
import os
import math
import random
import itertools
from collections import defaultdict, deque, Counter
from sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors import _flux_deficit
from sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial import _ball_ok, _double_sweep, _audit
from sec01_raw_wolfram_hypergraph_facts.s1_19_deficit_selection import _new_short_masks, _local_nodes
from sec01_raw_wolfram_hypergraph_facts.s1_20_triple_objective import _E_glue_per_edge, _mask_edges
from sec01_raw_wolfram_hypergraph_facts.s1_21_annealing_dynamics import _fd_map, _reach, _rank_masks
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_H, _diam

STATUS = "PARTIAL"
TITLE = ("The d=3 sandwich: aligned (alpha=3, k=4) grows cubic-grade bulk from a bare path -- width, "
         "diam, closed-link, glue energy ON the 6^3 reference column, d_H within 0.2 of the cube's own "
         "finite-size value; misaligned (k=2) builds rolled 2D sheet instead -- dimension enters twice, "
         "coupled by k=2(alpha-1); residuals: 17% fd-overshoot defects, deficit-11 anneal debris, d_s "
         "gap 0.6; N-scaling (the decisive test) not yet run")

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _sandwich_k(n, alpha, k_t, w_glue, w_def, steps, seed=11, C=3.5, rmax=8, degcap=10,
                T_hi=2.0, T_lo=0.2, p_remove=0.3, p_target=0.8, cdiam=0.8, w_iso=2.0, cceil=2.8):
    """Generalized sandwich: fd target k_t (2 for 2D, 4 for cubic 3D). Path seed. Exact audits."""
    rng = random.Random(seed)
    adj = defaultdict(set)
    for i in range(n - 1):
        adj[i].add(i + 1); adj[i + 1].add(i)
    eidx = {}
    for u in adj:
        for v in adj[u]:
            e = frozenset((u, v))
            if e not in eidx:
                eidx[e] = len(eidx)
    fd = defaultdict(int)
    mask_set = set(); by_edge = defaultdict(set)
    pivots = {}; b1 = 0; rank = 0
    E_glue = float(k_t) * (n - 1)
    edges_list = list(eidx.keys())
    floor = max(3, int(cdiam * n ** (1.0 / alpha)))
    ceil_d = int(cceil * n ** (1.0 / alpha))
    d_cur = _double_sweep(adj, 0)
    acc_add = acc_rem = n_acc = 0
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
            gone = by_edge.get(ebit_i, set())
            delta_fd = defaultdict(int)
            for m in gone:
                for eb2 in _mask_edges(m):
                    delta_fd[eb2] -= 1
            dE_glue = -abs(fd[ebit_i] - k_t)
            for eb2, dfk in delta_fd.items():
                if eb2 != ebit_i:
                    dE_glue += abs(fd[eb2] + dfk - k_t) - abs(fd[eb2] - k_t)
            surv = mask_set - gone
            r_new, piv_new = _rank_masks(surv)
            ddef = ((b1 - 1) - r_new) - (b1 - rank)
            dE_iso = 0.0
            if w_iso > 0:
                d_new = _double_sweep(adj, u)
                dE_iso = max(0, d_new - ceil_d) - max(0, d_cur - ceil_d)
            adj[u].add(v); adj[v].add(u)
            dE = w_glue * dE_glue + w_def * ddef + w_iso * dE_iso
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
                if w_iso > 0:
                    d_cur = d_new
                n_acc += 1
                if n_acc % 200 == 0:
                    d_cur = _double_sweep(adj, 0)
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
            dE_iso = (max(0, d_est - ceil_d) - max(0, d_cur - ceil_d)) if w_iso > 0 else 0.0
            e = frozenset((u, v))
            if e not in eidx:
                eidx[e] = len(eidx); edges_list.append(e)
            ebit_i = eidx[e]; ebit = 1 << ebit_i
            masks = _new_short_masks(adj, u, v, ebit, eidx)
            delta_fd = defaultdict(int)
            for m in masks:
                for eb2 in _mask_edges(m):
                    delta_fd[eb2] += 1
            dE_glue = abs(delta_fd.get(ebit_i, 0) - k_t)
            for eb2, dfk in delta_fd.items():
                if eb2 != ebit_i:
                    dE_glue += abs(fd[eb2] + dfk - k_t) - abs(fd[eb2] - k_t)
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
            dE = w_glue * dE_glue + w_def * ddef + w_iso * dE_iso
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
                if w_iso > 0:
                    d_cur = d_est
                n_acc += 1
                if n_acc % 200 == 0:
                    d_cur = _double_sweep(adj, 0)
            else:
                for hb in added:
                    del pivots[hb]
    return adj, b1, rank, b1 - rank, E_glue, acc_add, acc_rem


def Ek_per_edge(adj, k_t):
    fdm = _fd_map(adj)
    return sum(abs(v - k_t) for v in fdm.values()) / max(len(fdm), 1), len(fdm)


def closed_k(adj, k_t):
    fdm = _fd_map(adj); g = 0
    for v in adj:
        if adj[v] and all(fdm[frozenset((v, w))] == k_t for w in adj[v]):
            g += 1
    return g / len(adj)


def hist7(adj):
    fdm = _fd_map(adj); h = Counter(min(v, 6) for v in fdm.values()); t = sum(h.values())
    return [100.0 * h.get(i, 0) / t for i in range(7)]


def _lat3(k):
    coords = list(itertools.product(range(k), repeat=3)); idx = {c: i for i, c in enumerate(coords)}
    a = defaultdict(set)
    for c in coords:
        for ax in range(3):
            nc = list(c); nc[ax] += 1; nc = tuple(nc)
            if nc in idx:
                a[idx[c]].add(idx[nc]); a[idx[nc]].add(idx[c])
    return a


def _report(tag, adj, kt):
    Ef, ne = Ek_per_edge(adj, kt)
    _, _, _, df = _flux_deficit(adj, maxlen=4)
    E = sum(len(adj[u]) for u in adj) // 2
    print("      %-26s b1/V=%.2f defic=%d E%d/e=%.2f diam=%d d_s=%.2f d_H=%.2f closed%d=%.2f width=%.1f" % (
        tag, (E - len(adj) + 1) / len(adj), df, kt, Ef, _diam(adj), _d_s(adj), _d_H(adj),
        kt, closed_k(adj, kt), E / _diam(adj)))
    print("        fd: " + "  ".join("%d:%2.0f%%" % (i, x) for i, x in enumerate(hist7(adj))))


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Honest cost first: d=3 needs the pair (alpha, k) = (3, 4) -- dimension enters TWICE,")
    print("  coupled by k = 2(alpha-1). The misaligned control below shows the coupling is physical.\n")
    n = 216
    print("  (A) THE 6^3 REFERENCE COLUMN (N=216) -- WEAK at this size:")
    L = _lat3(6)
    print("      cap audit %.2f at C=3.5, alpha=3 (must be 0)" % _audit(L, 3.5, 3.0))
    _report("6^3 cube", L, 4)
    print("      => boundary dominates: only 44%% at the interior value 4; success = match THIS column,")
    print("         a LOW bar -- at N=216 a real 3-manifold is not distinguishable from a thick slab.")
    print("         Ceiling pinned by diam 15: ceil=16, floor=4.")

    print("\n  (B) ALIGNED (alpha=3, k=4), path seed, exact audits:")
    spn = 120 if not _FULL else 200
    for tag, kw in [("annealed 2->0.2 (n*%d)" % spn, dict(T_hi=2.0, T_lo=0.2)),
                    ("fixed T=0.5   (n*%d)" % spn, dict(T_hi=0.5, T_lo=0.5))]:
        adj, b1, rk, d, Eg, aa, ar = _sandwich_k(n, 3.0, 4, 1.0, 3.0, n * spn, seed=11, w_iso=2.0,
                                                 cceil=2.8, **kw)
        b1f, _, _, df = _flux_deficit(adj, maxlen=4)
        Ef, ne = Ek_per_edge(adj, 4)
        assert b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6, "audit fail"
        _report(tag + " a/r %d/%d" % (aa, ar), adj, 4)
    print("      => annealed: width ~39 (ref 36), closed4 ~0.31 (ref 0.30), d_H ~2.07 (ref 2.25) --")
    print("         cubic-grade BULK; but deficit ~11 (contraction-chord handle debris) and a ~17%%")
    print("         fd=5-6 OVERSHOOT tail (the symmetric |fd-4| penalty tolerates over-stacking).")
    print("         fixed-T: deficit 0, cleaner but under-dense and slab-ish -- a schedule TRADE.")

    print("\n  (C) MISALIGNED CONTROL (k=2 under the alpha=3 cap):")
    adj, b1, rk, d, Eg, aa, ar = _sandwich_k(n, 3.0, 2, 1.0, 3.0, n * 60, seed=11, w_iso=2.0,
                                             cceil=2.8, T_hi=2.0, T_lo=0.2)
    b1f, _, _, df = _flux_deficit(adj, maxlen=4)
    Ef, ne = Ek_per_edge(adj, 2)
    assert b1 == b1f and d == df and abs(Eg - Ef * ne) < 1e-6
    _report("k=2, alpha=3", adj, 2)
    print("      => ~79%% at fd=2, closed2 ~0.63: a crumpled 2D SHEET filling the 3D ball. Alpha alone")
    print("         cannot raise dimension; the cell-type target k must agree. k = 2(alpha-1) has teeth.")

    print("\n  (D) VERDICT: cubic-grade 3-COMPLEX reached frame-free; the dial is the PAIR (alpha, k)")
    print("      = (d, 2(d-1)) -- one integer, twice, self-consistently. NOT a manifold: residuals are")
    print("      overshoot defects (~17%%; fix: asymmetric penalty), handle debris (deficit 11; fix:")
    print("      cold cleanup phase), d_s gap ~0.6. r55 NOT contradicted (route is non-minor-closed by")
    print("      design). DECISIVE TEST NOT YET RUN: N-scaling to 512/1000 -- does d_s climb toward 3")
    print("      and the interior fraction grow, or do the defects prove thermodynamic? N=216 cannot")
    print("      answer. Limits: single seed; N=216; ceiling on the double-sweep estimate. Tally 366.")
