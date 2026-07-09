#!/usr/bin/env python3
"""cdt_torus_run.py -- STAGE 1 of the topology frontier: causal CDT on T^2 x S^1.

The S^2 x S^1 program (campaign 7, REPORT_CDT_HUB.md) closed the joint (d_H AND d_s) 3-manifold
by the per-slice Euler identity: spatial slices are 2-spheres (F = 2V - 4), which forces, for the
whole foliated complex,   N31 = N13 = 2 N0 - 4 T,   N22 = N3 - 4 N0 + 8 T,   f22 = 1 - 4(N0-2T)/N3,
locking spatial-vertex density to the (2,2) "stitching". This runner breaks that assumption by
making each spatial slice a 2-TORUS (chi = 0) instead of a 2-sphere (chi = 2). The manifold is
then T^2 x S^1 -- which is exactly the topology of the flat 3-torus benchmark foliated along one
circle, so the benchmark's own geometry lives in this ensemble.

GENERALIZED IDENTITY (derived, verified exact in selftest). For a genus-g closed orientable slice,
chi = 2 - 2g and F = 2V - 2 chi, so
      N31 = N13 = 2 N0 - 2 chi T,     N22 = N3 - 4 N0 + 4 chi T,     f22 = 1 - 4 (N0 - chi T) / N3.
Sphere (chi=2): N22 = N3 - 4 N0 + 8 T (the campaign-7 result).  Torus (chi=0): N22 = N3 - 4 N0.
The +8T offset -> +4 chi T -> 0.  CRUX: at fixed (N3, T), dN22 = -4 dN0 + 4 T dchi, and chi is a
topological invariant of the (fixed) slice topology, so dchi = 0 under every foliation-preserving
move. Hence dN22 = -4 dN0 holds for EVERY genus: the differential lock is topology-INDEPENDENT;
breaking F=2V-4 only shifts the CONSTANT term, it does NOT dissolve the lock. Consequence for the
acceptance weights: dN22 = dN3 - 4 dN0 gives 2-3:+1, 3-2:-1, 2-6:0, 6-2:0, 4-4:0 -- IDENTICAL to
the sphere runner. So the entire Metropolis core (moves, ratios, detailed balance) is reused
VERBATIM from cdt_causal_run; only the SEED (flat torus grid vs octahedron) and the per-slice
CENSUS (chi=0 vs chi=2, + orientability) change.

Everything the sphere runner verifies (foliation, closed 3-manifold, link census bad=0, DB via
exact move round-trips) is re-verified here for the torus in --selftest, plus: (a) the generalized
identity holds exactly on seed/grown/thermalized states, (b) every accepted move preserves it,
(c) slices stay orientable chi=0 tori, (d) an EXACT flat T^2 x S^1 calibrant (identical flat slices
stacked by prisms == a flat 3-torus) is census-clean with the predicted counts (f22 = 1/3).

Run:  MANIFOLD_REPO=$(pwd) PYTHONPATH=.:tooling python3 cdt_torus_run.py --selftest
      ... --calibrant --m 10 --n 10 --T 10 --measure-seeds 8
      ... --chunk --k0 2.0 --T 12 --V 6000 --m 5 --n 5 --sweeps 100000 --budget-s 36 \
              --scratch scratch --log rec.jsonl
"""
import argparse, itertools, json, os, pickle, random, time as _time, math
from collections import Counter, defaultdict

import cdt_causal_run as C
from cdt_causal_run import (Causal, FS, PROB, measure,
                            lazy_rw_sdim, ball_growth_dim, nx_to_adj, to_graph, link_census)


# ------------------------------------------------------ flat torus slice (uniform degree 6)
def torus_grid_tris(m, n, off=0):
    """Triangulated flat 2-torus on an m x n vertex grid (m,n >= 3), every vertex degree 6.
    Vertex (i,j) -> off + (i%m)*n + (j%n). Each unit square split by the (i,j)-(i+1,j+1) diagonal
    -> triangles {(i,j),(i+1,j),(i+1,j+1)} and {(i,j),(i,j+1),(i+1,j+1)}. V=mn, E=3mn, F=2mn, chi=0."""
    assert m >= 3 and n >= 3, "need m,n>=3 for a simplicial torus (no doubled edges)"
    vid = lambda i, j: off + (i % m) * n + (j % n)
    tris = []
    for i in range(m):
        for j in range(n):
            a, b, c, d = vid(i, j), vid(i + 1, j), vid(i, j + 1), vid(i + 1, j + 1)
            tris.append(tuple(sorted((a, b, d))))
            tris.append(tuple(sorted((a, c, d))))
    return list(range(off, off + m * n), ), tris


def seed_torus(T, m=5, n=5):
    """Foliated T^2 x S^1 seed: T identical flat-torus slices, consecutive slices joined by the
    SAME ordered-prism split (lower-vertex -> higher-vertex diagonal) used by the octahedral seed."""
    st = Causal(T)
    S = m * n
    for t in range(T):
        for i in range(S):
            st.time[t * S + i] = t
    st.next_id = S * T
    _, base_tris = torus_grid_tris(m, n, off=0)      # local labels 0..S-1, shared by every slice
    for t in range(T):
        t2 = (t + 1) % T
        for tri in base_tris:
            a, b, c = sorted(tri)
            A, B, Cc = t * S + a, t * S + b, t * S + c
            A2, B2, C2 = t2 * S + a, t2 * S + b, t2 * S + c
            st.add_tet(FS((A, B, Cc, C2)))            # (3,1)
            st.add_tet(FS((A, B, B2, C2)))            # (2,2)
            st.add_tet(FS((A, A2, B2, C2)))           # (1,3)
    return st


# ------------------------------------------------------ orientability of a triangulated surface
def slice_orientable(fs):
    """fs: iterable of frozenset triangles forming a closed surface. True iff orientable
    (torus), False iff not (Klein bottle), None iff not a closed surface."""
    tri = [tuple(sorted(t)) for t in fs]
    e2t = defaultdict(list)
    for t in tri:
        a, b, c = t
        for e in (FS((a, b)), FS((b, c)), FS((a, c))):
            e2t[e].append(t)
    if any(len(v) != 2 for v in e2t.values()):
        return None
    de = lambda o: ((o[0], o[1]), (o[1], o[2]), (o[2], o[0]))   # directed boundary edges
    orient = {}
    for s in tri:
        if s in orient:
            continue
        orient[s] = s
        stack = [s]
        while stack:
            t = stack.pop()
            for (x, y) in de(orient[t]):
                for u in e2t[FS((x, y))]:
                    if u == t:
                        continue
                    w = next(iter(set(u) - {x, y}))
                    if u in orient:
                        if (y, x) not in de(orient[u]):     # shared edge must be traversed oppositely
                            return False
                    else:
                        orient[u] = (y, x, w)
                        stack.append(u)
    return True


# ------------------------------------------------------ validation (chi=0 slices, no trust)
def validate_torus(st, heavy=False):
    ec, tc = Counter(), Counter()
    for tet in st.tets:
        st.kind_of(tet)
        for e in itertools.combinations(tet, 2):
            ec[FS(e)] += 1
        for tr in itertools.combinations(tet, 3):
            tc[FS(tr)] += 1
    assert all(c == 2 for c in tc.values()), "complex not closed: face not in exactly 2 tets"
    assert set(ec) == set(st.ecnt) and all(st.ecnt[e] == ec[e] for e in ec), "edge cache drift"
    stris = {f for f in tc if len({st.time[v] for v in f}) == 1}
    assert stris == set(st.stris.pos), "spatial-triangle cache drift"
    sedges = {e for e in ec if len({st.time[v] for v in e}) == 1}
    assert sedges == set(st.sedges.pos), "spatial-edge cache drift"
    verts = set()
    for tet in st.tets:
        verts |= tet
    assert verts == set(st.valive.pos), "vertex cache drift"
    by_t = defaultdict(list)
    for f in stris:
        by_t[st.time[next(iter(f))]].append(f)
    assert set(by_t) == set(range(st.T)), "a slice lost all its spatial triangles"
    for t, fs in by_t.items():
        ec2 = Counter()
        vs = set()
        for f in fs:
            vs |= f
            for e in itertools.combinations(sorted(f), 2):
                ec2[FS(e)] += 1
        assert all(c == 2 for c in ec2.values()), "slice %d not a closed surface" % t
        chi = len(vs) - len(ec2) + len(fs)
        assert chi == 0, "slice %d has chi=%d, not a 2-torus" % (t, chi)      # <-- the ONLY topology change
        g = defaultdict(set)
        for e in ec2:
            a, b = tuple(e); g[a].add(b); g[b].add(a)
        seen = {next(iter(vs))}; stk = [next(iter(vs))]
        while stk:
            xx = stk.pop()
            for y in g[xx]:
                if y not in seen:
                    seen.add(y); stk.append(y)
        assert len(seen) == len(vs), "slice %d disconnected" % t
        if heavy:
            assert slice_orientable(fs) is True, "slice %d not an ORIENTABLE torus (Klein bottle?)" % t
    # generalized identity, torus (chi=0): N31=N13=2 N0 ; N22 = N3 - 4 N0
    assert st.nk[3] == st.nk[1] == 2 * st.N0, "N31/N13 != 2 N0 (torus identity broken)"
    assert st.nk[2] == st.N3 - 4 * st.N0, "N22 != N3 - 4 N0 (torus identity broken)"
    if heavy:
        c = link_census(list(st.tets))
        assert c["bad"] == 0 and c["disk"] == 0, "link census not clean: %s" % c
    return True


# ------------------------------------------------------ degree / condensation diagnostics
def adj_of(st):
    adj = defaultdict(set)
    for e in st.ecnt:
        a, b = tuple(e); adj[a].add(b); adj[b].add(a)
    return adj


def deg_stats(adj):
    ds = [len(adj[v]) for v in adj]
    n = len(ds); mean = sum(ds) / n
    sd = (sum((d - mean) ** 2 for d in ds) / n) ** 0.5
    return dict(deg_mean=round(mean, 2), deg_sd=round(sd, 2), deg_max=max(ds), deg_min=min(ds))


def profile_cv(st):
    prof = Counter()
    for f in st.stris:
        prof[st.time[next(iter(f))]] += 1
    p = [prof.get(t, 0) for t in range(st.T)]
    mean = sum(p) / len(p)
    sd = (sum((x - mean) ** 2 for x in p) / len(p)) ** 0.5
    return p, round(sd / max(1e-9, mean), 3)


def seed_avg_dims(adj, dswins, dhwins, seeds, tmax):
    g = nx_to_adj(to_graph({u: set(v) for u, v in adj.items()}))
    out = {}
    for w in dswins:
        vals = [lazy_rw_sdim(g, windows=[w], tmax=tmax, seed=100 + s).get("%d-%d" % w) for s in range(seeds)]
        vals = [v for v in vals if v is not None]
        m = sum(vals) / len(vals); sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
        out["ds_%d-%d" % w] = dict(mean=round(m, 4), sd=round(sd, 4))
    for w in dhwins:
        vals = [ball_growth_dim(g, windows=[w], seed=200 + s).get("%d-%d" % w) for s in range(seeds)]
        vals = [v for v in vals if v is not None]
        m = sum(vals) / len(vals); sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
        out["dh_%d-%d" % w] = dict(mean=round(m, 4), sd=round(sd, 4))
    return out


# ------------------------------------------------------ exact flat calibrant
def run_calibrant(a):
    st = seed_torus(a.T, a.m, a.n)
    validate_torus(st, heavy=True)
    adj = adj_of(st)
    dims = seed_avg_dims(adj, [(4, 12), (8, 24), (16, 48)], [(2, 6), (3, 8)], a.measure_seeds, 100)
    rec = dict(kind="torus_calibrant", T=a.T, m=a.m, n=a.n, N0=st.N0, N3=st.N3,
               f22=round(st.nk[2] / st.N3, 4), n31=st.nk[3], n22=st.nk[2], n13=st.nk[1],
               **deg_stats(adj), **dims)
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("CALIBRANT flat T^2xS^1  T=%d %dx%d  N0=%d N3=%d f22=%.4f  deg(mean/sd/max)=%.1f/%.1f/%d"
          % (a.T, a.m, a.n, st.N0, st.N3, st.nk[2] / st.N3, rec["deg_mean"], rec["deg_sd"], rec["deg_max"]))
    print("   d_s 8-24 = %s +- %s   16-48 = %s +- %s   |   d_H 2-6 = %s +- %s   3-8 = %s +- %s"
          % (dims["ds_8-24"]["mean"], dims["ds_8-24"]["sd"], dims["ds_16-48"]["mean"], dims["ds_16-48"]["sd"],
             dims["dh_2-6"]["mean"], dims["dh_2-6"]["sd"], dims["dh_3-8"]["mean"], dims["dh_3-8"]["sd"]))


# ------------------------------------------------------ chunked runner (resumable)
def run_chunk(a):
    os.makedirs(a.scratch, exist_ok=True)
    tag = "tor_k0%+.2f_T%d_V%d_m%d_n%d_k22%+.2f_s%d" % (a.k0, a.T, a.V, a.m, a.n, a.k22, a.seed)
    sf = os.path.join(a.scratch, "%s.pkl" % tag)
    if os.path.exists(sf):
        with open(sf, "rb") as fh:
            blob = pickle.load(fh)
        st, k3, done, rng = blob["st"], blob["k3"], blob["done"], blob["rng"]
    else:
        st = seed_torus(a.T, a.m, a.n); k3 = a.k3_init; done = 0; rng = random.Random(a.seed)
        while st.N3 < a.V:
            st.sweep(rng, a.k0, -0.5, a.eps, a.V)
    if a.measure_long:
        adj = adj_of(st)
        dims = seed_avg_dims(adj, [(4, 12), (8, 24), (16, 48)], [(2, 6), (3, 8)], a.measure_seeds, 100)
        _, cv = profile_cv(st)
        rec = dict(kind="torus_long", k0=a.k0, T=a.T, V=a.V, m=a.m, n=a.n, k22=a.k22, seed=a.seed,
                   sweeps=done, N0=st.N0, N3=st.N3, f22=round(st.nk[2] / st.N3, 4),
                   profile_cv=cv, **deg_stats(adj), **dims)
        if a.log:
            with open(a.log, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
        print("LONG tor k0=%+.2f V=%d T=%d f22=%.3f CV=%.3f deg=%.1f/%.1f/%d | d_s 8-24=%s+-%s 16-48=%s+-%s | d_H 2-6=%s+-%s"
              % (a.k0, a.V, a.T, st.nk[2] / st.N3, cv, deg_stats(adj)["deg_mean"], deg_stats(adj)["deg_sd"],
                 deg_stats(adj)["deg_max"], dims["ds_8-24"]["mean"], dims["ds_8-24"]["sd"],
                 dims["ds_16-48"]["mean"], dims["ds_16-48"]["sd"], dims["dh_2-6"]["mean"], dims["dh_2-6"]["sd"]))
        return
    t0 = _time.time()
    while done < a.sweeps and _time.time() - t0 < a.budget_s:
        st.sweep(rng, a.k0, k3, a.eps, a.V, a.k22)
        if done < a.tune:
            k3 += min(max((st.N3 - a.V) * 2e-5, -2e-3), 2e-3)
        done += 1
    validate_torus(st, heavy=False)
    m = measure(st)
    adj = adj_of(st); _, cv = profile_cv(st)
    rec = dict(kind="torus_chunk", k0=a.k0, T=a.T, V=a.V, m=a.m, n=a.n, eps=a.eps, seed=a.seed,
               k3=round(k3, 4), sweeps=done, tuned=done >= a.tune, k22=a.k22,
               wall=round(_time.time() - t0, 1), profile_cv=cv, **deg_stats(adj), **m)
    with open(sf, "wb") as fh:
        pickle.dump(dict(st=st, k3=k3, done=done, rng=rng), fh)
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    cc = m["census"]
    print("tor k0=%+.2f sw=%d/%d k3=%.3f | N0=%d N3=%d f22=%.3f | bad=%d | d_s(4-12)=%s d_H(2-6)=%s | CV=%.3f deg_max=%d prof %d/%d"
          % (a.k0, done, a.sweeps, k3, m["N0"], m["N3"], m["f22"], cc["bad"],
             m["ds"].get("4-12"), m["dh"].get("2-6"), cv, deg_stats(adj)["deg_max"],
             min(m["profile"]), max(m["profile"])))


# ------------------------------------------------------ selftest
def selftest():
    print("=== TORUS causal CDT selftest: T^2 x S^1, chi=0 slices, generalized identity ===")
    for T in (3, 4, 6):
        st = seed_torus(T, 5, 5)
        validate_torus(st, heavy=True)
        chi3 = st.N0 - len(st.ecnt) + len(st.tri2) - st.N3
        assert chi3 == 0, "3-manifold chi=%d != 0" % chi3
        assert st.nk[2] == st.N3 - 4 * st.N0 and st.nk[3] == st.nk[1] == 2 * st.N0
        print("  seed T=%d 5x5: N0=%d N3=%d (31/22/13=%d/%d/%d) f22=%.3f chi3=0 slices=orientable-tori census-clean"
              % (T, st.N0, st.N3, st.nk[3], st.nk[2], st.nk[1], st.nk[2] / st.N3))
    # move round-trips + identity preservation (detailed-balance reversibility, verbatim core)
    rng = random.Random(0)
    st = seed_torus(4, 5, 5)
    base = set(st.tets)

    def force(key, tries=6000):
        for _ in range(tries):
            p = getattr(st, "prop_" + key)(rng)
            if p is not None:
                n0b, n3b, n22b = st.N0, st.N3, st.nk[2]
                if len(p) == 6 and p[5][0] == "newv":
                    st.time[p[5][1]] = p[5][2]; st.next_id += 1
                for tet in p[3]:
                    st.rem_tet(tet)
                for tet in p[4]:
                    st.add_tet(tet)
                dN22, dN3, dN0 = st.nk[2] - n22b, st.N3 - n3b, st.N0 - n0b
                assert dN22 == dN3 - 4 * dN0, "move %s broke dN22=dN3-4dN0: %d vs %d" % (key, dN22, dN3 - 4 * dN0)
                assert st.nk[2] == st.N3 - 4 * st.N0, "identity broken after %s" % key
                return True
        return False

    for pair in (("23", "32"), ("26", "62")):
        assert force(pair[0]); validate_torus(st, heavy=True)
        assert force(pair[1]); validate_torus(st, heavy=True)
        assert set(st.tets) == base, "%s/%s did not round-trip exactly" % pair
        print("  %s/%s round-trip: exact, census clean, dN22=dN3-4dN0 both steps" % pair)
    assert force("44"); validate_torus(st, heavy=True)
    assert force("44"); validate_torus(st, heavy=True)
    print("  4-4: applied twice, census clean, identity preserved")
    # random chain: manifold + foliation + torus identity + orientability must hold throughout
    st = seed_torus(4, 5, 5)
    rng = random.Random(2)
    k3 = 0.6
    for s in range(200):
        st.sweep(rng, k0=1.0, k3=k3, eps=0.02, V=1100)
        k3 += min(max((st.N3 - 1100) * 2e-5, -2e-3), 2e-3)
        if (s + 1) % 50 == 0:
            validate_torus(st, heavy=True)
    print("  200-sweep chain (T=4, V~1100): N0=%d N3=%d f22=%.3f, orientable-torus census clean every 50 sweeps"
          % (st.N0, st.N3, st.nk[2] / st.N3))
    assert len([k for k in PROB if st.accs[k] > 0]) == 5, "some move never accepted"
    print("  accepted move mix:", {k: st.accs[k] for k in ("23", "32", "26", "62", "44")})
    m = measure(st)
    assert m["census"]["bad"] == 0
    print("  estimator smoke: d_s(4-12)=%s d_H(2-6)=%s profile=%s" % (m["ds"].get("4-12"), m["dh"].get("2-6"), m["profile"]))
    # exact flat calibrant sanity: f22 must be exactly 1/3, census clean
    cal = seed_torus(6, 6, 6)
    validate_torus(cal, heavy=True)
    assert abs(cal.nk[2] / cal.N3 - 1.0 / 3.0) < 1e-12, "flat calibrant f22 != 1/3"
    print("  flat calibrant T=6 6x6: N0=%d N3=%d f22=%.4f (=1/3 exact) census clean"
          % (cal.N0, cal.N3, cal.nk[2] / cal.N3))
    print("ALL TORUS SELF-TESTS PASSED")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--calibrant", action="store_true")
    ap.add_argument("--chunk", action="store_true")
    ap.add_argument("--measure-long", action="store_true", dest="measure_long")
    ap.add_argument("--k0", type=float, default=2.0)
    ap.add_argument("--k3-init", type=float, default=0.8, dest="k3_init")
    ap.add_argument("--T", type=int, default=12)
    ap.add_argument("--V", type=int, default=6000)
    ap.add_argument("--m", type=int, default=5)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--eps", type=float, default=0.002)
    ap.add_argument("--k22", type=float, default=0.0)
    ap.add_argument("--sweeps", type=int, default=3000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--budget-s", type=float, default=34.0, dest="budget_s")
    ap.add_argument("--measure-seeds", type=int, default=8, dest="measure_seeds")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--scratch", default="scratch")
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.calibrant:
        run_calibrant(a)
    elif a.chunk:
        run_chunk(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
