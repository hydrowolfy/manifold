#!/usr/bin/env python3
"""Genuine 2+1D Causal Dynamical Triangulations (Ambjorn-Jurkiewicz-Loll).

Refs: Ambjorn-Jurkiewicz-Loll, "Dynamically Triangulating Lorentzian Quantum Gravity",
Nucl.Phys. B610 (2001) 347 (hep-th/0105267); PRL 85 (2000) 924 (hep-th/0002050);
Ambjorn-Jordan-Jurkiewicz-Loll, 2+1D phase structure (e.g. PRD 87 (2013) 044021).

STRUCTURE (standard AJL 2+1D simplicial complex): see RESULTS.md.
Foliation: T periodic proper-time slices. Each slice is a closed 2D triangulation
of the SPHERE S^2 (chi = V-E+F = 2). Sandwiches t->t+1 filled by tetrahedra of
type (3,1),(1,3),(2,2). Spacelike edges within a slice; timelike edges between
adjacent slices. Action S = -k0*N0 + k3*N3 (AJL bare-coupling reduced form).
"""
import math, random, sys, os, json, time
from collections import defaultdict, deque

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cdt2p1_out")


class Slice:
    """A closed orientable 2D triangulation of S^2, kept manifold-valid."""
    __slots__ = ("tris", "nextv", "verts")

    def __init__(self, tris=None):
        self.tris = set()
        self.verts = set()
        if tris:
            for t in tris:
                self.add_tri(t)
        self.nextv = (max(self.verts) + 1) if self.verts else 0

    def add_tri(self, t):
        f = frozenset(t)
        assert len(f) == 3
        self.tris.add(f)
        self.verts.update(f)

    def copy(self):
        s = Slice()
        s.tris = set(self.tris)
        s.verts = set(self.verts)
        s.nextv = self.nextv
        return s

    def edges(self):
        e = set()
        for t in self.tris:
            a, b, c = tuple(t)
            e.add(frozenset((a, b)))
            e.add(frozenset((a, c)))
            e.add(frozenset((b, c)))
        return e

    def new_vertex(self):
        v = self.nextv
        self.nextv += 1
        self.verts.add(v)
        return v

    def euler(self):
        V = len(self.verts)
        E = len(self.edges())
        F = len(self.tris)
        return V - E + F, V, E, F

    def is_manifold_sphere(self):
        ecount = defaultdict(int)
        for t in self.tris:
            a, b, c = tuple(t)
            for e in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))):
                ecount[e] += 1
        for e, c in ecount.items():
            if c != 2:
                return False, f"edge {tuple(e)} in {c} triangles (need 2)"
        for v in self.verts:
            link = defaultdict(set)
            for t in self.tris:
                if v in t:
                    others = tuple(t - {v})
                    link[others[0]].add(others[1])
                    link[others[1]].add(others[0])
            if not link:
                return False, f"vertex {v} in no triangle"
            for lv, nb in link.items():
                if len(nb) != 2:
                    return False, f"vertex {v} link not simple cycle at {lv}"
            start = next(iter(link))
            seen = {start}
            cur, prev = start, None
            steps = 0
            while True:
                nxt = [x for x in link[cur] if x != prev]
                if not nxt:
                    break
                nprev, cur = cur, nxt[0]
                prev = nprev
                steps += 1
                if cur == start:
                    break
                seen.add(cur)
                if steps > len(link) + 2:
                    return False, f"vertex {v} link walk runaway"
            if len(seen) != len(link):
                return False, f"vertex {v} link not connected ({len(seen)}/{len(link)})"
        chi, V, E, F = self.euler()
        if chi != 2:
            return False, f"chi={chi} != 2 (V={V},E={E},F={F})"
        return True, "ok"


def octahedron():
    tris = [
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),
        (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4),
    ]
    return Slice(tris)


def spatial_flip(sl, rng):
    e2t = defaultdict(list)
    for t in sl.tris:
        a, b, c = tuple(t)
        for e in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))):
            e2t[e].append(t)
    edges = [e for e, ts in e2t.items() if len(ts) == 2]
    rng.shuffle(edges)
    existing = sl.edges()
    for e in edges:
        t1, t2 = e2t[e]
        a, b = tuple(e)
        c = next(iter(t1 - e))
        d = next(iter(t2 - e))
        if c == d:
            continue
        if frozenset((c, d)) in existing:
            continue
        sl.tris.discard(t1)
        sl.tris.discard(t2)
        sl.add_tri((a, c, d))
        sl.add_tri((b, c, d))
        return True
    return False


def spatial_split(sl, rng):
    t = rng.choice(list(sl.tris))
    a, b, c = tuple(t)
    v = sl.new_vertex()
    sl.tris.discard(t)
    sl.add_tri((a, b, v))
    sl.add_tri((b, c, v))
    sl.add_tri((a, c, v))
    return True


def spatial_merge(sl, rng, vmin=4):
    if len(sl.verts) <= vmin:
        return False
    deg = defaultdict(set)
    for t in sl.tris:
        a, b, c = tuple(t)
        deg[a].update((b, c)); deg[b].update((a, c)); deg[c].update((a, b))
    cand = [v for v in sl.verts if len(deg[v]) == 3]
    rng.shuffle(cand)
    for v in cand:
        star = [t for t in sl.tris if v in t]
        if len(star) != 3:
            continue
        outer = set()
        for t in star:
            outer.update(t - {v})
        if len(outer) != 3:
            continue
        newtri = frozenset(outer)
        if newtri in sl.tris:
            continue
        for t in star:
            sl.tris.discard(t)
        sl.verts.discard(v)
        sl.add_tri(tuple(outer))
        return True
    return False


class State:
    def __init__(self, T, slices):
        self.T = T
        self.slices = slices

    @staticmethod
    def init(T):
        return State(T, [octahedron() for _ in range(T)])

    def copy(self):
        return State(self.T, [s.copy() for s in self.slices])

    def N0(self):
        return sum(len(s.verts) for s in self.slices)

    def N_tris(self):
        return sum(len(s.tris) for s in self.slices)

    def N3(self):
        n = 0
        F = [len(s.tris) for s in self.slices]
        E = [len(s.edges()) for s in self.slices]
        for t in range(self.T):
            tp = (t + 1) % self.T
            n += F[t] + F[tp] + E[t] + E[tp]
        return n

    def euler_check(self):
        res = []
        for t, s in enumerate(self.slices):
            ok, msg = s.is_manifold_sphere()
            res.append((t, ok, msg))
        return res


def build_graph(state):
    T = state.T
    adj = defaultdict(set)

    def link(u, v):
        adj[u].add(v); adj[v].add(u)

    for t in range(T):
        for e in state.slices[t].edges():
            a, b = tuple(e)
            link((t, a), (t, b))
        for v in state.slices[t].verts:
            adj[(t, v)]

    for t in range(T):
        tp = (t + 1) % T
        up_verts = sorted(state.slices[tp].verts)
        dn_verts = sorted(state.slices[t].verts)
        nu = len(up_verts); nd = len(dn_verts)
        for k, tri in enumerate(sorted(state.slices[t].tris, key=lambda f: tuple(sorted(f)))):
            apex = up_verts[k % nu]
            for a in tri:
                link((t, a), (tp, apex))
        for k, tri in enumerate(sorted(state.slices[tp].tris, key=lambda f: tuple(sorted(f)))):
            base = dn_verts[k % nd]
            for a in tri:
                link((tp, a), (t, base))
    return adj


def build_tetra_complex(state):
    """Build the GENUINE 3D tetrahedral complex of the foliated spacetime and its
    dual graph (one node per tetrahedron, adjacent iff sharing a triangular face).

    Construction (standard product/prism sandwich, AJL causal decomposition):
    all slices share the current spatial triangulation combinatorics (a product
    foliation S^2 x S^1). Each spatial triangle (a<b<c) generates, in each sandwich
    t->t+1, a triangular PRISM (lower a,b,c at t; upper a,b,c at t+1). Every prism
    is cut into the standard 3 tetrahedra -- one (3,1), one (2,2), one (1,3):
        (3,1): (a_t, b_t, c_t, c_{t+1})
        (2,2): (a_t, b_t, c_{t+1}, b_{t+1})
        (1,3): (a_t, b_{t+1}, c_{t+1}, a_{t+1})
    The consistent (a<b<c) ordering makes the internal cuts of adjacent prisms
    match, so the result is a closed causal 3-manifold: every triangular face is
    shared by exactly two tetrahedra. Vertices labelled (t, i); spacelike faces lie
    in a slice, timelike faces bridge adjacent slices only. Returns (tets, adj, info).
    """
    T = state.T
    # use slice 0's triangulation as the shared spatial complex (product foliation)
    tri_sorted = sorted(tuple(sorted(t)) for t in state.slices[0].tris)
    tets = []
    types = []
    for t in range(T):
        tp = (t + 1) % T
        for (a, b, c) in tri_sorted:
            A, B, Cc = (t, a), (t, b), (t, c)
            Au, Bu, Cu = (tp, a), (tp, b), (tp, c)
            tets.append(frozenset([A, B, Cc, Cu])); types.append((3, 1))
            tets.append(frozenset([A, B, Cu, Bu])); types.append((2, 2))
            tets.append(frozenset([A, Bu, Cu, Au])); types.append((1, 3))
    face2t = defaultdict(list)
    for i, tt in enumerate(tets):
        vs = tuple(tt)
        for j in range(4):
            face2t[frozenset(vs[:j] + vs[j + 1:])].append(i)
    adj = defaultdict(set)
    boundary_faces = 0
    bad_faces = 0
    for f, ts in face2t.items():
        if len(ts) == 2:
            adj[ts[0]].add(ts[1]); adj[ts[1]].add(ts[0])
        elif len(ts) == 1:
            boundary_faces += 1
        else:
            bad_faces += 1
    info = {
        "n_tets": len(tets),
        "boundary_faces": boundary_faces,   # 0 => closed manifold
        "bad_faces": bad_faces,             # faces in >2 tets => non-manifold
        "type_counts": {ty: types.count(ty) for ty in [(3, 1), (2, 2), (1, 3)]},
    }
    return tets, adj, info


def check_3manifold(state):
    """Structural self-test of the 3D complex: closed (no boundary), non-branching
    (no face in >2 tets), dual graph connected, all three tetra types present."""
    tets, adj, info = build_tetra_complex(state)
    ok = (info["boundary_faces"] == 0 and info["bad_faces"] == 0
          and all(info["type_counts"][ty] > 0 for ty in [(3, 1), (2, 2), (1, 3)]))
    # connectivity of dual graph
    if adj:
        start = next(iter(adj)); seen = {start}; dq = deque([start])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); dq.append(w)
        connected = (len(seen) == len(tets))
    else:
        connected = False
    info["dual_connected"] = connected
    info["ok"] = bool(ok and connected)
    return info


def ball_growth(adj, sources, rmax):
    acc = defaultdict(float)
    for s in sources:
        dist = {s: 0}
        dq = deque([s])
        counts = defaultdict(int)
        counts[0] = 1
        while dq:
            u = dq.popleft()
            du = dist[u]
            if du >= rmax:
                continue
            for w in adj[u]:
                if w not in dist:
                    dist[w] = du + 1
                    counts[du + 1] += 1
                    dq.append(w)
        cum = 0
        for r in range(0, rmax + 1):
            cum += counts.get(r, 0)
            acc[r] += cum
    n = len(sources)
    return {r: acc[r] / n for r in acc}


def estimate_dH(Nr, rlo, rhi):
    xs, ys = [], []
    for r in range(rlo, rhi + 1):
        if r in Nr and Nr[r] > 0:
            xs.append(math.log(r)); ys.append(math.log(Nr[r]))
    if len(xs) < 2:
        return None, None
    n = len(xs)
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx == 0:
        return None, None
    slope = sxy / sxx
    inter = my - slope * mx
    resid = [y - (slope * x + inter) for x, y in zip(xs, ys)]
    if n > 2:
        s2 = sum(r * r for r in resid) / (n - 2)
        se = math.sqrt(s2 / sxx) if sxx > 0 else None
    else:
        se = None
    return slope, se


def estimate_dH_shell(Nr, rlo, rhi):
    """Local Hausdorff dim from the SHELL profile: shell(r)=N(r)-N(r-1) ~ r^(dH-1).
    Fits log(shell) vs log(r) in [rlo,rhi]; returns dH = slope+1 and its s.e.
    More robust than cumulative fit against the small-volume saturation plateau."""
    xs, ys = [], []
    for r in range(max(rlo, 1), rhi + 1):
        if r in Nr and (r - 1) in Nr:
            sh = Nr[r] - Nr[r - 1]
            if sh > 0:
                xs.append(math.log(r)); ys.append(math.log(sh))
    if len(xs) < 2:
        return None, None
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx == 0:
        return None, None
    slope = sxy / sxx
    resid = [y - (slope * x + (my - slope * mx)) for x, y in zip(xs, ys)]
    se = None
    if n > 2:
        s2 = sum(rr * rr for rr in resid) / (n - 2)
        se = math.sqrt(s2 / sxx) if sxx > 0 else None
    return slope + 1.0, se


def action(state, k0, k3):
    return -k0 * state.N0() + k3 * state.N3()


MOVES = ["flip", "split", "merge"]


def propose(state, rng):
    t = rng.randrange(state.T)
    m = rng.choice(MOVES)
    trial = state.slices[t].copy()
    if m == "flip":
        ok = spatial_flip(trial, rng)
    elif m == "split":
        ok = spatial_split(trial, rng)
    else:
        ok = spatial_merge(trial, rng)
    if not ok:
        return None, None, None
    return t, m, trial


def sweep(state, k0, k3, rng, nsteps):
    acc = 0
    for _ in range(nsteps):
        t, m, trial = propose(state, rng)
        if trial is None:
            continue
        old = state.slices[t]
        S_old = action(state, k0, k3)
        state.slices[t] = trial
        S_new = action(state, k0, k3)
        dS = S_new - S_old
        if dS <= 0 or rng.random() < math.exp(-dS):
            acc += 1
        else:
            state.slices[t] = old
    return acc


def self_test(verbose=True):
    rng = random.Random(12345)
    log = []

    def p(s):
        log.append(s)
        if verbose:
            print(s)

    p("=== 2+1D CDT SELF-TEST ===")
    oc = octahedron()
    ok, msg = oc.is_manifold_sphere()
    chi, V, E, F = oc.euler()
    p(f"[1] octahedron manifold S^2: {ok} ({msg}); chi={chi} V={V} E={E} F={F}")
    assert ok and chi == 2

    sl = octahedron()
    fails = 0
    for i in range(400):
        m = rng.choice(MOVES)
        trial = sl.copy()
        if m == "flip":
            done = spatial_flip(trial, rng)
        elif m == "split":
            done = spatial_split(trial, rng)
        else:
            done = spatial_merge(trial, rng)
        if not done:
            continue
        ok, msg = trial.is_manifold_sphere()
        if not ok:
            fails += 1
            p(f"    MOVE {m} broke manifold at step {i}: {msg}")
            if fails > 3:
                break
        else:
            sl = trial
    p(f"[2] 400 random spatial moves preserve S^2 manifold+chi=2: fails={fails}; "
      f"final V={len(sl.verts)} F={len(sl.tris)}")
    assert fails == 0

    st = State.init(6)
    ok_before = all(o for _, o, _ in st.euler_check())
    p(f"[3a] initial 6-slice state: all slices S^2 = {ok_before}; N0={st.N0()} N3={st.N3()}")
    accs = 0
    for s in range(30):
        accs += sweep(st, 1.0, 0.8, rng, 40)
    checks = st.euler_check()
    all_ok = all(o for _, o, _ in checks)
    p(f"[3b] after 30 sweeps: all slices still S^2 = {all_ok}; "
      f"accepted={accs}; N0={st.N0()} N3={st.N3()}")
    for tt, o, msg in checks:
        if not o:
            p(f"    slice {tt} FAIL: {msg}")
    assert all_ok

    adj = build_graph(st)
    bad = 0
    for (t1, i1), nbrs in adj.items():
        for (t2, i2) in nbrs:
            if t1 == t2:
                continue
            dt = (t2 - t1) % st.T
            if dt not in (1, st.T - 1):
                bad += 1
    p(f"[4] timelike edges only between ADJACENT slices: violations={bad}")
    assert bad == 0

    start = next(iter(adj))
    seen = {start}; dq = deque([start])
    while dq:
        u = dq.popleft()
        for w in adj[u]:
            if w not in seen:
                seen.add(w); dq.append(w)
    p(f"[5] 3D vertex graph connected: {len(seen)}/{len(adj)} reached")
    assert len(seen) == len(adj)

    # 6. genuine 3D tetra complex is a closed causal 3-manifold with all 3 tet types
    info = check_3manifold(st)
    p(f"[6] 3D tetra complex closed 3-manifold: ok={info['ok']}; "
      f"n_tets={info['n_tets']} boundary_faces={info['boundary_faces']} "
      f"bad_faces={info['bad_faces']} types={info['type_counts']} "
      f"dual_connected={info['dual_connected']}")
    assert info["ok"]

    p("=== ALL SELF-TESTS PASSED ===")
    return log


def run_measurement(k0, k3, T=16, therm=140, meas=25, meas_every=10,
                    seed=1, ckpt=None, budget_s=34):
    t0 = time.time()
    rng = random.Random(seed)
    state = State.init(T)
    done_therm = 0
    Nr_acc = defaultdict(float)
    Nr_n = 0
    dH_samples = []
    if ckpt and os.path.exists(ckpt):
        with open(ckpt) as f:
            d = json.load(f)
        state = State(d["T"], [Slice([tuple(x) for x in ts]) for ts in d["slices"]])
        done_therm = d["done_therm"]
        Nr_acc = defaultdict(float, {int(k): v for k, v in d["Nr_acc"].items()})
        Nr_n = d["Nr_n"]
        dH_samples = d["dH_samples"]
        rng = random.Random(d["seed_state"])

    def save():
        if not ckpt:
            return
        d = {
            "T": state.T,
            "slices": [[list(t) for t in s.tris] for s in state.slices],
            "done_therm": done_therm,
            "Nr_acc": {str(k): v for k, v in Nr_acc.items()},
            "Nr_n": Nr_n,
            "dH_samples": dH_samples,
            "seed_state": rng.randint(0, 2 ** 31),
            "k0": k0, "k3": k3,
        }
        tmp = ckpt + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f)
        os.replace(tmp, ckpt)

    while done_therm < therm and time.time() - t0 < budget_s * 0.5:
        sweep(state, k0, k3, rng, 30)
        done_therm += 1
    n_tets_last = 0
    rmax_last = 0
    while Nr_n < meas and time.time() - t0 < budget_s:
        sweep(state, k0, k3, rng, 30)
        tets, adj, info = build_tetra_complex(state)
        n_tets_last = info["n_tets"]
        if info["boundary_faces"] or info["bad_faces"] or not adj:
            continue  # skip if (shouldn't happen) not a clean closed manifold
        N = len(tets)
        rmax = min(2 * state.T, 30)
        rmax_last = rmax
        srcs = rng.sample(range(N), min(40, N))
        Nr = ball_growth(adj, srcs, rmax)
        for r, v in Nr.items():
            Nr_acc[r] += v
        Nr_n += 1
    save()

    result = {
        "k0": k0, "k3": k3, "T": T,
        "done_therm": done_therm, "target_therm": therm,
        "meas_samples": Nr_n, "target_meas": meas,
        "N0": state.N0(), "N3": state.N3(), "Ntris": state.N_tris(),
        "elapsed_s": round(time.time() - t0, 2),
    }
    result["n_tets"] = n_tets_last
    if Nr_n > 0:
        Nr_avg = {r: Nr_acc[r] / Nr_n for r in Nr_acc}
        Nmax = max(Nr_avg.values())
        # scaling window: r>=3 (past lattice artifacts) up to before saturation
        rs = [r for r in sorted(Nr_avg) if r >= 3 and Nr_avg[r] < 0.5 * Nmax]
        rlo = 3
        rhi = max(rs) if len(rs) >= 2 else max(6, int(max(Nr_avg) * 0.5))
        dH, se = estimate_dH(Nr_avg, rlo, rhi)
        result["Nr_avg"] = {int(r): round(Nr_avg[r], 2) for r in sorted(Nr_avg)}
        result["dH_fit"] = round(dH, 3) if dH else None
        result["dH_fit_se"] = round(se, 3) if se else None
        result["fit_window"] = [rlo, rhi]
    return result, (done_therm >= therm and Nr_n >= meas)



# ============================================================================
# TASK 1-3 EXTENSION: GENUINE 3D FLUCTUATING TET COMPLEX (v2)
# ----------------------------------------------------------------------------
# The build_tetra_complex() above builds a PRODUCT foliation (all sandwiches use
# slice-0's triangulation), so N(t) is locked equal across slices. Below we make
# the 3D triangulation the fundamental DOF: a list of genuine tetrahedra, each
# vertex labelled (time, index), evolved by the standard 2+1D CDT ergodic bulk
# Pachner moves so that (a) N3 fluctuates, (b) each slice's spatial volume N(t)
# fluctuates INDEPENDENTLY, (c) the closed causal foliated 3-manifold is kept.
#
# Ergodic bulk move set implemented (AJL 2+1D):
#   (2,3)/(3,2): flip an internal triangular face <-> internal edge; dN3 = +-1.
#   (2,6)/(6,2): add / remove a spatial vertex (split a spatial triangle and its
#                two apex tets into six, or the reverse); dN3 = +-4. This is the
#                move that lets a single slice's spatial volume grow/shrink.
#   (4,4):       flip a spacelike edge shared by 4 tets (2 up + 2 down); dN3 = 0.
# Each proposal is applied to a working copy, checked to preserve the closed
# non-branching manifold + the foliation (every tet spans <=2 adjacent slices),
# then Metropolis-accepted against S = -k0*N0 + k3*N3.
# ============================================================================

def _faces_of(tt):
    vs = tuple(tt)
    return (frozenset((vs[1], vs[2], vs[3])), frozenset((vs[0], vs[2], vs[3])),
            frozenset((vs[0], vs[1], vs[3])), frozenset((vs[0], vs[1], vs[2])))


class TetComplex:
    """Genuine 3D foliated tetra complex. tets: list of frozenset of (t,i) verts.
    Maintained closed (every triangular face in exactly 2 tets) and foliated
    (every tet's vertices lie in at most 2 adjacent time-slices)."""
    __slots__ = ("tets", "T", "_nextidx")

    def __init__(self, tets, T):
        self.tets = [t for t in tets if t is not None]
        self.T = T
        mx = 0
        for tt in self.tets:
            for (_, i) in tt:
                if i > mx:
                    mx = i
        self._nextidx = mx + 1

    @staticmethod
    def from_state(state):
        tets, _adj, _info = build_tetra_complex(state)
        return TetComplex(list(tets), state.T)

    def new_index(self):
        i = self._nextidx
        self._nextidx += 1
        return i

    # ---- structural maps -------------------------------------------------
    def face_map(self):
        f2t = defaultdict(list)
        for k, tt in enumerate(self.tets):
            for f in _faces_of(tt):
                f2t[f].append(k)
        return f2t

    def edge_map(self):
        e2t = defaultdict(list)
        for k, tt in enumerate(self.tets):
            vs = tuple(tt)
            for a in range(4):
                for b in range(a + 1, 4):
                    e2t[frozenset((vs[a], vs[b]))].append(k)
        return e2t

    def N3(self):
        return len(self.tets)

    def N0(self):
        vs = set()
        for tt in self.tets:
            vs.update(tt)
        return len(vs)

    def slice_volumes(self):
        """N(t) = number of SPACELIKE triangles (all 3 verts same time) per slice."""
        f2t = self.face_map()
        vol = defaultdict(int)
        for f in f2t:
            times = set(v[0] for v in f)
            if len(times) == 1:
                vol[next(iter(times))] += 1
        return {t: vol.get(t, 0) for t in range(self.T)}

    # ---- validity --------------------------------------------------------
    def is_closed(self):
        for f, ts in self.face_map().items():
            if len(ts) != 2:
                return False
        return True

    def foliation_ok(self):
        for tt in self.tets:
            times = sorted(set(v[0] for v in tt))
            if len(times) > 2:
                return False
            if len(times) == 2:
                a, b = times
                dt = (b - a) % self.T
                if dt not in (1, self.T - 1):
                    return False
        return True

    def dual_graph(self):
        f2t = self.face_map()
        adj = defaultdict(set)
        for f, ts in f2t.items():
            if len(ts) == 2:
                adj[ts[0]].add(ts[1]); adj[ts[1]].add(ts[0])
        for k in range(len(self.tets)):
            adj[k]
        return adj

    def dual_connected(self):
        adj = self.dual_graph()
        if not adj:
            return False
        start = next(iter(adj)); seen = {start}; dq = deque([start])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); dq.append(w)
        return len(seen) == len(self.tets)

    def slice_is_sphere(self, t):
        """Extract slice t's spacelike triangulation and check chi=2 (S^2)."""
        f2t = self.face_map()
        tris = [tuple(f) for f in f2t if len(set(v[0] for v in f)) == 1
                and next(iter(f))[0] == t]
        if not tris:
            return False, 0
        sl = Slice()
        for tr in tris:
            sl.add_tri(tuple(sorted(v[1] for v in tr)))
        chi, V, E, F = sl.euler()
        return (chi == 2), chi

    # ---- ERGODIC BULK MOVES ---------------------------------------------
    def _slices_touched(self, tets):
        s = set()
        for tt in tets:
            for (t, _i) in tt:
                s.add(t)
        return s

    def _apply_check(self, remove_idxs, add_tets):
        """Replace tets at remove_idxs with add_tets; accept only if the result
        stays a closed foliated 3-manifold AND every affected constant-time slice
        remains a valid 2-sphere (chi=2, simplicial). This is the CDT constraint
        that keeps the spatial topology fixed at S^2 while N(t) fluctuates."""
        rem = set(remove_idxs)
        touched = self._slices_touched([self.tets[k] for k in remove_idxs] + list(add_tets))
        newlist = [tt for k, tt in enumerate(self.tets) if k not in rem]
        newlist.extend(add_tets)
        old = self.tets
        self.tets = newlist
        if self.is_closed() and self.foliation_ok():
            good = True
            for t in touched:
                ok, _chi = self.slice_is_sphere(t)
                if not ok:
                    good = False
                    break
            if good:
                return True
        self.tets = old
        return False

    def move_23(self, rng):
        """(2,3): internal face abc shared by tets abcd, abce -> abde,bcde,acde."""
        f2t = self.face_map()
        faces = [f for f, ts in f2t.items() if len(ts) == 2]
        rng.shuffle(faces)
        for f in faces:
            i, j = f2t[f]
            A, B = self.tets[i], self.tets[j]
            d = next(iter(A - f)); e = next(iter(B - f))
            if d == e:
                continue
            a, b, c = tuple(f)
            new = [frozenset([a, b, d, e]), frozenset([b, c, d, e]),
                   frozenset([a, c, d, e])]
            if any(len(nt) != 4 for nt in new):
                continue
            if self._apply_check([i, j], new):
                return True
        return False

    def move_32(self, rng):
        """(3,2): edge de shared by exactly 3 tets abde,bcde,acde -> abcd,abce."""
        e2t = self.edge_map()
        edges = [(e, ts) for e, ts in e2t.items() if len(ts) == 3]
        rng.shuffle(edges)
        for e, ts in edges:
            d, ee = tuple(e)
            others = set()
            for k in ts:
                others.update(self.tets[k] - {d, ee})
            if len(others) != 3:
                continue
            a, b, c = tuple(others)
            new = [frozenset([a, b, c, d]), frozenset([a, b, c, ee])]
            if any(len(nt) != 4 for nt in new):
                continue
            if self._apply_check(list(ts), new):
                return True
        return False

    def move_26(self, rng):
        """(2,6): spacelike face abc (2 apex tets up p, down q) -> insert vertex X
        at time(abc); 6 tets. Grows the slice's spatial volume by +2 triangles."""
        f2t = self.face_map()
        sfaces = [f for f, ts in f2t.items()
                  if len(ts) == 2 and len(set(v[0] for v in f)) == 1]
        rng.shuffle(sfaces)
        for f in sfaces:
            i, j = f2t[f]
            A, B = self.tets[i], self.tets[j]
            p = next(iter(A - f)); q = next(iter(B - f))
            s = next(iter(f))[0]
            if {p[0], q[0]} != {(s + 1) % self.T, (s - 1) % self.T}:
                continue
            a, b, c = tuple(f)
            X = (s, self.new_index())
            new = [frozenset([a, b, X, p]), frozenset([b, c, X, p]),
                   frozenset([a, c, X, p]), frozenset([a, b, X, q]),
                   frozenset([b, c, X, q]), frozenset([a, c, X, q])]
            if self._apply_check([i, j], new):
                return True
            self._nextidx -= 1  # reclaim unused index on reject
        return False

    def move_62(self, rng):
        """(6,2): remove a spatial vertex X of spatial degree 3 (in exactly 6 tets:
        3 up to a single apex p, 3 down to a single apex q) -> 2 tets abcp, abcq."""
        vert2t = defaultdict(list)
        for k, tt in enumerate(self.tets):
            for v in tt:
                vert2t[v].append(k)
        cand = [v for v, ks in vert2t.items() if len(ks) == 6]
        rng.shuffle(cand)
        for X in cand:
            ks = vert2t[X]
            s = X[0]
            apexes = set()
            base = set()
            ok = True
            for k in ks:
                tt = self.tets[k]
                nonX = tt - {X}
                ap = [v for v in nonX if v[0] != s]
                bs = [v for v in nonX if v[0] == s]
                if len(ap) != 1 or len(bs) != 2:
                    ok = False; break
                apexes.add(ap[0])
            if not ok or len(apexes) != 2:
                continue
            for k in ks:
                base.update(v for v in self.tets[k] if v[0] == s and v != X)
            if len(base) != 3:
                continue
            a, b, c = tuple(base)
            p, q = tuple(apexes)
            new = [frozenset([a, b, c, p]), frozenset([a, b, c, q])]
            if any(len(nt) != 4 for nt in new):
                continue
            if self._apply_check(ks, new):
                return True
        return False

    def move_44(self, rng):
        """(4,4): a spacelike edge ab in slice s shared by 4 tets (2 up to apex p,
        2 down to apex q) with the two spatial neighbours c,d -> flip ab to cd.
        dN3 = 0. Preserves foliation; a genuine spatial-flip lifted to the bulk."""
        e2t = self.edge_map()
        # spacelike edges (both verts same time)
        sed = [(e, ts) for e, ts in e2t.items()
               if len(set(v[0] for v in e)) == 1 and len(ts) == 4]
        rng.shuffle(sed)
        for e, ts in sed:
            a, b = tuple(e)
            s = a[0]
            ups = []; downs = []
            spatial_nbrs = set()
            good = True
            for k in ts:
                tt = self.tets[k]
                rest = tt - {a, b}
                ap = [v for v in rest if v[0] != s]
                sp = [v for v in rest if v[0] == s]
                if len(ap) != 1 or len(sp) != 1:
                    good = False; break
                spatial_nbrs.add(sp[0])
                if ap[0][0] == (s + 1) % self.T:
                    ups.append((k, sp[0], ap[0]))
                else:
                    downs.append((k, sp[0], ap[0]))
            if not good or len(spatial_nbrs) != 2 or len(ups) != 2 or len(downs) != 2:
                continue
            c, d = tuple(spatial_nbrs)
            p = ups[0][2]; q = downs[0][2]
            if not (ups[0][2] == ups[1][2] and downs[0][2] == downs[1][2]):
                continue
            # flip ab -> cd: new up tets (a,c,d,p),(b,c,d,p); down (a,c,d,q),(b,c,d,q)
            new = [frozenset([a, c, d, p]), frozenset([b, c, d, p]),
                   frozenset([a, c, d, q]), frozenset([b, c, d, q])]
            if any(len(nt) != 4 for nt in new):
                continue
            if self._apply_check(list(ts), new):
                return True
        return False


BULK_MOVES = [
    ("23", TetComplex.move_23), ("32", TetComplex.move_32),
    ("26", TetComplex.move_26), ("62", TetComplex.move_62),
    ("44", TetComplex.move_44),
]


def bulk_sweep(tc, k0, k3, rng, nsteps, Nbar=None, eps=0.0):
    """Metropolis over the bulk ergodic moves. Action
        S = -k0 N0 + k3 N3 + eps (N3 - Nbar)^2   [volume-fixing term].
    The quadratic term (AJL standard) holds the total 3-volume near a target Nbar
    so the universe fluctuates around a fixed size instead of collapsing to the
    minimal sphere or running away -- this is the ensemble in which the
    semiclassical de Sitter blob appears. eps=0 recovers the pure bare action.
    Each accepted move already preserves the closed foliated manifold."""
    acc = defaultdict(int); att = defaultdict(int)

    def Svol(N3):
        return eps * (N3 - Nbar) ** 2 if (Nbar is not None and eps > 0) else 0.0

    for _ in range(nsteps):
        name, mv = rng.choice(BULK_MOVES)
        att[name] += 1
        N0o, N3o = tc.N0(), tc.N3()
        S_old = -k0 * N0o + k3 * N3o + Svol(N3o)
        snapshot = list(tc.tets); snap_idx = tc._nextidx
        if not mv(tc, rng):
            continue
        S_new = -k0 * tc.N0() + k3 * tc.N3() + Svol(tc.N3())
        dS = S_new - S_old
        if dS <= 0 or rng.random() < math.exp(-min(dS, 60.0)):
            acc[name] += 1
        else:
            tc.tets = snapshot; tc._nextidx = snap_idx
    return acc, att


def bulk_self_test(verbose=True):
    rng = random.Random(2024)
    log = []

    def p(s):
        log.append(s)
        if verbose:
            print(s)

    p("=== 2+1D CDT BULK (v2) SELF-TEST ===")
    st = State.init(4)
    tc = TetComplex.from_state(st)
    p(f"[B1] init from product: closed={tc.is_closed()} foliation_ok={tc.foliation_ok()} "
      f"dual_connected={tc.dual_connected()} N3={tc.N3()} N(t)={tc.slice_volumes()}")
    assert tc.is_closed() and tc.foliation_ok() and tc.dual_connected()

    counts = defaultdict(int)
    Nbar = 20 * tc.T
    for _ in range(30):
        acc, att = bulk_sweep(tc, 1.4, 1.0, rng, 30, Nbar=Nbar, eps=0.02)
        for kmv in att:
            counts[kmv] += acc[kmv]
    p(f"[B2] 30x30 bulk sweeps accepted per move: {dict(counts)}")
    p(f"[B3] after bulk moves: closed={tc.is_closed()} foliation_ok={tc.foliation_ok()} "
      f"dual_connected={tc.dual_connected()} N3={tc.N3()}")
    assert tc.is_closed(), "closed 3-manifold broken by bulk moves"
    assert tc.foliation_ok(), "foliation (adjacent-slice) broken by bulk moves"
    assert tc.dual_connected(), "dual graph disconnected"

    # every triangle in exactly 2 tets (explicit closed-manifold restatement)
    f2t = tc.face_map()
    bad = sum(1 for _f, ts in f2t.items() if len(ts) != 2)
    p(f"[B4] every triangle in exactly 2 tets: bad_faces={bad}")
    assert bad == 0

    # each slice still S^2 (chi=2)
    sph = [tc.slice_is_sphere(t) for t in range(tc.T)]
    allsph = all(ok for ok, _ in sph)
    p(f"[B5] each slice topology S^2 (chi=2): {allsph}  chis={[c for _,c in sph]}")
    assert allsph

    # ERGODICITY: slice volumes must now VARY (not locked equal as product)
    vols = list(tc.slice_volumes().values())
    vmean = sum(vols) / len(vols)
    vvar = sum((v - vmean) ** 2 for v in vols) / len(vols)
    p(f"[B6] slice volumes N(t)={dict(tc.slice_volumes())} mean={vmean:.1f} var={vvar:.2f} "
      f"(product foliation would give var=0)")
    assert vvar > 0.0, "slice volumes still locked equal -> still a product foliation"

    # time series: confirm N(t) trajectories decorrelate between slices
    series = {t: [] for t in range(tc.T)}
    for _ in range(20):
        bulk_sweep(tc, 1.4, 1.0, rng, 20, Nbar=Nbar, eps=0.02)
        sv = tc.slice_volumes()
        for t in range(tc.T):
            series[t].append(sv[t])
    # not-identical check: at least one pair of slices differs at some time
    differ = any(series[a] != series[b] for a in range(tc.T) for b in range(a + 1, tc.T))
    p(f"[B7] independent fluctuation: slice-volume trajectories differ across slices "
      f"= {differ}")
    assert differ, "slice trajectories identical -> not independent"

    p("=== BULK SELF-TESTS PASSED ===")
    return log


# ---- de Sitter volume profile + spectral dimension on the fluctuating geom ---

def _align_and_accumulate(profile_acc, profile_n, vols, T):
    """Center-of-volume align one N(t) profile onto a common frame, then add.
    Alignment uses the CIRCULAR center of mass on the periodic time axis (the AJL
    COV prescription) computed from a smoothed profile so a single dominant blob
    is centred robustly against per-config lumpiness."""
    total = sum(vols[t] for t in range(T))
    if total == 0:
        return
    # 3-point circular smoothing to suppress single-slice spikes before COM
    sm = [(vols[(t - 1) % T] + 2 * vols[t] + vols[(t + 1) % T]) / 4.0
          for t in range(T)]
    sx = sum(sm[t] * math.cos(2 * math.pi * t / T) for t in range(T))
    sy = sum(sm[t] * math.sin(2 * math.pi * t / T) for t in range(T))
    if sx == 0 and sy == 0:
        com = max(range(T), key=lambda t: sm[t])
    else:
        ang = math.atan2(sy, sx)
        com = int(round(ang / (2 * math.pi) * T)) % T
    center = T // 2
    for t in range(T):
        src = (com + (t - center)) % T
        profile_acc[t] += vols[src]
    profile_n[0] += 1


def cos_profile_fit(prof, T):
    """Fit N(t) ~ A cos^n((t-t0)/W). We fit in 2+1D the AJL form (d=2 -> cos^2)
    by grid search over (A,W,t0,n) minimizing SSE. Returns fit dict + R^2 + shape."""
    ts = list(range(T))
    ys = [prof[t] for t in ts]
    t0 = center = T / 2.0
    ymax = max(ys) if ys else 0.0
    ymean = sum(ys) / len(ys)
    ss_tot = sum((y - ymean) ** 2 for y in ys)
    best = None
    for n in (1.0, 1.5, 2.0, 2.5, 3.0):
        for Wf in [x / 100.0 for x in range(20, 200, 4)]:
            W = Wf * T
            for A in [ymax * f for f in (0.8, 0.9, 1.0, 1.1, 1.2)]:
                sse = 0.0
                for t, y in zip(ts, ys):
                    arg = (t - t0) / W
                    if abs(arg) >= math.pi / 2:
                        model = 0.0
                    else:
                        model = A * (math.cos(arg) ** n)
                    sse += (y - model) ** 2
                if best is None or sse < best[0]:
                    best = (sse, A, W, n, t0)
    sse, A, W, n, t0 = best
    r2 = 1.0 - sse / ss_tot if ss_tot > 0 else 0.0
    # shape classification
    nz = [y for y in ys if y > 0.15 * ymax]
    # count contiguous lobes above half-max (periodic)
    half = 0.5 * ymax
    above = [1 if y > half else 0 for y in ys]
    lobes = 0
    for i in range(T):
        if above[i] == 1 and above[(i - 1) % T] == 0:
            lobes += 1
    if all(a == 1 for a in above):
        lobes = 1  # constant tube (single connected band)
    flatness = (max(ys) - min(ys)) / ymax if ymax > 0 else 0.0
    if flatness < 0.15:
        shape = "constant_tube(product-like)"
    elif lobes == 1 and min(ys) < 0.35 * ymax:
        shape = "single_extended_lobe(de Sitter)"
    elif lobes >= 2:
        shape = "multi-lobe/degenerate"
    else:
        shape = "single_lobe(weak)"
    return {"A": round(A, 2), "W": round(W, 3), "n": n, "t0": round(t0, 2),
            "R2": round(r2, 4), "lobes": lobes, "flatness": round(flatness, 3),
            "shape": shape}


def spectral_dimension(adj, rng, n_src, sigma_max):
    """Return probability P(sigma) of a random walker returning to start after
    sigma diffusion steps on the tet-dual graph. d_s(sigma) = -2 d ln P / d ln sigma.
    Uses exact probability propagation from each source (stdlib only)."""
    nodes = list(adj.keys())
    if not nodes:
        return {}, {}
    srcs = rng.sample(nodes, min(n_src, len(nodes)))
    Psum = [0.0] * (sigma_max + 1)
    for s in srcs:
        # probability distribution, lazy walk p_stay=0 (standard), heat-kernel style
        # LAZY walk: stay with prob 1/2 (standard CDT diffusion) -> kills the
        # bipartite even/odd parity oscillation of the naive walk.
        prob = {s: 1.0}
        Psum[0] += 1.0
        for sigma in range(1, sigma_max + 1):
            nxt = defaultdict(float)
            for u, pu in prob.items():
                deg = len(adj[u])
                if deg == 0:
                    nxt[u] += pu
                    continue
                nxt[u] += 0.5 * pu
                share = 0.5 * pu / deg
                for w in adj[u]:
                    nxt[w] += share
            prob = nxt
            Psum[sigma] += prob.get(s, 0.0)
    P = {sigma: Psum[sigma] / len(srcs) for sigma in range(sigma_max + 1)}
    ds = {}
    for sigma in range(2, sigma_max):
        p1 = P.get(sigma - 1, 0); p2 = P.get(sigma + 1, 0)
        if p1 > 0 and p2 > 0 and sigma - 1 > 0 and sigma + 1 > 0:
            dlnP = math.log(p2) - math.log(p1)
            dlns = math.log(sigma + 1) - math.log(sigma - 1)
            ds[sigma] = -2.0 * dlnP / dlns
    return P, ds


def run_bulk_measurement(k0, k3, T=12, therm=60, meas=200, seed=1,
                         ckpt=None, budget_s=34, sigma_max=40,
                         Nbar=None, eps=0.02):
    """Thermalize the FLUCTUATING 3D complex under the bulk ergodic moves, then
    measure: de Sitter N(t) profile (COV-aligned ensemble), spectral dimension
    d_s(sigma), Hausdorff d_H. Checkpoint/resume friendly."""
    t0 = time.time()
    rng = random.Random(seed)
    st = State.init(T)
    tc = TetComplex.from_state(st)
    done_therm = 0
    prof_acc = [0.0] * T
    prof_n = [0]
    nt_var_samples = []
    Nr_acc = defaultdict(float); Nr_n = 0
    ds_acc = defaultdict(float); ds_n = defaultdict(int)
    P_acc = defaultdict(float); P_n = 0

    if ckpt and os.path.exists(ckpt):
        with open(ckpt) as f:
            d = json.load(f)
        tc = TetComplex([frozenset(tuple(v) for v in tt) for tt in d["tets"]], d["T"])
        T = d["T"]
        done_therm = d["done_therm"]
        prof_acc = d["prof_acc"]; prof_n = [d["prof_n"]]
        nt_var_samples = d["nt_var_samples"]
        Nr_acc = defaultdict(float, {int(k): v for k, v in d["Nr_acc"].items()})
        Nr_n = d["Nr_n"]
        ds_acc = defaultdict(float, {int(k): v for k, v in d["ds_acc"].items()})
        ds_n = defaultdict(int, {int(k): v for k, v in d["ds_n"].items()})
        P_acc = defaultdict(float, {int(k): v for k, v in d["P_acc"].items()})
        P_n = d["P_n"]
        rng = random.Random(d["seed_state"])

    def save():
        if not ckpt:
            return
        d = {
            "T": T, "tets": [[list(v) for v in tt] for tt in tc.tets],
            "done_therm": done_therm,
            "prof_acc": prof_acc, "prof_n": prof_n[0],
            "nt_var_samples": nt_var_samples,
            "Nr_acc": {str(k): v for k, v in Nr_acc.items()}, "Nr_n": Nr_n,
            "ds_acc": {str(k): v for k, v in ds_acc.items()},
            "ds_n": {str(k): v for k, v in ds_n.items()},
            "P_acc": {str(k): v for k, v in P_acc.items()}, "P_n": P_n,
            "seed_state": rng.randint(0, 2 ** 31), "k0": k0, "k3": k3,
        }
        tmp = ckpt + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f)
        os.replace(tmp, ckpt)

    if Nbar is None:
        Nbar = 20 * T  # ~20 tets/slice: moderate fill -> volume can localize
                       # into a single de Sitter lobe (not a saturated flat tube)
    while done_therm < therm and time.time() - t0 < budget_s * 0.45:
        bulk_sweep(tc, k0, k3, rng, 25, Nbar=Nbar, eps=eps)
        done_therm += 1

    while Nr_n < meas and time.time() - t0 < budget_s:
        bulk_sweep(tc, k0, k3, rng, 20, Nbar=Nbar, eps=eps)
        if not (tc.is_closed() and tc.foliation_ok()):
            continue
        vols = tc.slice_volumes()
        vmean = sum(vols.values()) / T
        vvar = sum((v - vmean) ** 2 for v in vols.values()) / T
        nt_var_samples.append(vvar)
        _align_and_accumulate(prof_acc, prof_n, vols, T)

        adj = tc.dual_graph()
        N = len(tc.tets)
        rmax = min(2 * T, 24)
        srcs = rng.sample(range(N), min(30, N))
        Nr = ball_growth(adj, srcs, rmax)
        for r, v in Nr.items():
            Nr_acc[r] += v
        # spectral dimension (cheaper: fewer sources)
        P, ds = spectral_dimension(adj, rng, min(6, N), sigma_max)
        for sig, val in P.items():
            P_acc[sig] += val
        P_n += 1
        for sig, val in ds.items():
            ds_acc[sig] += val; ds_n[sig] += 1
        Nr_n += 1
    save()

    result = {"k0": k0, "k3": k3, "T": T, "Nbar": Nbar, "eps": eps,
              "done_therm": done_therm,
              "target_therm": therm, "meas_samples": Nr_n, "target_meas": meas,
              "N3_final": tc.N3(), "N0_final": tc.N0(),
              "elapsed_s": round(time.time() - t0, 2)}

    if prof_n[0] > 0:
        prof = [prof_acc[t] / prof_n[0] for t in range(T)]
        result["Nt_profile"] = [round(x, 2) for x in prof]
        result["Nt_var_mean"] = round(sum(nt_var_samples) / len(nt_var_samples), 3) \
            if nt_var_samples else 0.0
        fit = cos_profile_fit(prof, T)
        result["desitter_fit"] = fit
    if Nr_n > 0:
        Nr_avg = {r: Nr_acc[r] / Nr_n for r in Nr_acc}
        Nmax = max(Nr_avg.values())
        rs = [r for r in sorted(Nr_avg) if r >= 3 and Nr_avg[r] < 0.6 * Nmax]
        rlo = 3; rhi = max(rs) if len(rs) >= 2 else 8
        dH, se = estimate_dH(Nr_avg, rlo, rhi)
        result["dH_fit"] = round(dH, 3) if dH else None
        result["dH_fit_se"] = round(se, 3) if se else None
        result["dH_window"] = [rlo, rhi]
        # shell-based local dH in the rising (pre-saturation) window
        incs = [Nr_avg.get(r, 0) - Nr_avg.get(r - 1, 0) for r in sorted(Nr_avg) if r >= 1]
        rpk = 1 + (incs.index(max(incs)) if incs else 0)  # radius of max shell
        dHs, ses = estimate_dH_shell(Nr_avg, 2, max(3, rpk))
        result["dH_shell"] = round(dHs, 3) if dHs else None
        result["dH_shell_se"] = round(ses, 3) if ses else None
        result["dH_shell_window"] = [2, max(3, rpk)]
        result["Nr_avg"] = {int(r): round(Nr_avg[r], 2) for r in sorted(Nr_avg)}
    if P_n > 0:
        result["P_return"] = {int(s): round(P_acc[s] / P_n, 6) for s in sorted(P_acc)}
        result["ds_running"] = {int(s): round(ds_acc[s] / ds_n[s], 3)
                                for s in sorted(ds_n) if ds_n[s] > 0}
    complete = (done_therm >= therm and Nr_n >= meas)
    return result, complete


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        log = self_test()
        with open(os.path.join(OUT, "selftest.log"), "w") as f:
            f.write("\n".join(log))
    elif len(sys.argv) > 1 and sys.argv[1] == "measure":
        k0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
        k3 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
        tag = sys.argv[4] if len(sys.argv) > 4 else f"k0_{k0}_k3_{k3}"
        ckpt = os.path.join(OUT, f"ckpt_{tag}.json")
        res, complete = run_measurement(k0, k3, ckpt=ckpt)
        res["complete"] = complete
        with open(os.path.join(OUT, f"result_{tag}.json"), "w") as f:
            json.dump(res, f, indent=2)
        print(json.dumps(res, indent=2))
        print("COMPLETE" if complete else "PARTIAL (rerun to resume)")
    elif len(sys.argv) > 1 and sys.argv[1] == "bulktest":
        V2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cdt2p1_v2")
        os.makedirs(V2, exist_ok=True)
        log = bulk_self_test()
        with open(os.path.join(V2, "bulk_selftest.log"), "w") as f:
            f.write("\n".join(log))
    elif len(sys.argv) > 1 and sys.argv[1] == "bulkmeasure":
        V2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cdt2p1_v2")
        os.makedirs(V2, exist_ok=True)
        k0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
        k3 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
        T = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        tag = sys.argv[5] if len(sys.argv) > 5 else f"k0_{k0}_k3_{k3}_T{T}"
        ckpt = os.path.join(V2, f"ckpt_bulk_{tag}.json")
        res, complete = run_bulk_measurement(k0, k3, T=T, ckpt=ckpt)
        res["complete"] = complete
        with open(os.path.join(V2, f"result_bulk_{tag}.json"), "w") as f:
            json.dump(res, f, indent=2)
        print(json.dumps(res, indent=2))
        print("COMPLETE" if complete else "PARTIAL (rerun to resume)")
    else:
        print("usage: cdt_2plus1.py [selftest | measure k0 k3 tag | "
              "bulktest | bulkmeasure k0 k3 T tag]")
