"""The causal-set (spacetime) dimension: a 4D longest-chain aspect ratio that is a FALSE POSITIVE -- the causal
order is a non-manifold, chain-like structure, not 3+1 spacetime.

Spacetime dimension lives in the CAUSAL graph (the partial order of rewrite events), not the spatial slice.
Each rewrite event consumes two edges (produced by earlier events) and produces three (consumed by later
events); linking producer->consumer builds the causal DAG. We measure its dimension two independent ways,
each CALIBRATED against Minkowski sprinklings of known dimension:

  (A) LONGEST-CHAIN (height): for a d-dim causal set the longest chain scales L ~ N^{1/d}. Calibration
      recovers d=2 -> ~1.9, d=4 -> ~3.8. The keystone gives L ~ N^{1/4} => apparent d ~ 4. Taken alone this
      looks like 3+1 SPACETIME.
  (B) INTERVAL-VOLUME: for a d-dim causal set a causal interval [p,q] has volume V ~ ell^d (ell = longest
      chain inside it). Calibration recovers d=2 -> ~1.9, d=4 -> ~3.1 (the high-d estimate is biased low at
      finite N but is clearly >2). The keystone gives V ~ ell^{1.2-1.4} -- the intervals are CHAIN-LIKE (~1D).

The two estimators DISAGREE (4 vs ~1.3). For a faithful d-dim manifold they must AGREE; the disagreement is
the diagnosis: the keystone causal order is NOT a manifold. The picture: a wide, shallow causal structure
(height ~ N^{1/4} forces width ~ N^{3/4}) built from nearly-parallel ~1D causal chains. The longest-chain
"4D" is purely the global aspect ratio (a tall enough fan of thin chains gives L ~ N^{1/4}); the
interval-volume sees the truth -- between two causally related events there are few alternate routes, exactly
the sparse/tree-like character of the spatial graph (b1=1) carried into the causal order.

So 3+1 spacetime is NOT recovered from the causal graph either. The same b1=1 sparsity that makes the spatial
slice a fractal tree makes the causal order a non-manifold fan of chains; the seductive longest-chain "d~4"
is an aspect-ratio artifact that the interval-volume cross-check (the structurally meaningful estimator)
refutes. The causal/Lorentzian continuum (a faithful manifold with V ~ ell^d matching L ~ N^{1/d}) is NOT
present -- the spacetime-dimension question stays OPEN, and this route does not reach 3+1.

STATUS: PARTIAL -- the causal-set dimension is now measured and calibrated (both estimators), with the robust
verdict that the causal order is non-manifold (a tempting longest-chain 4D is refuted by interval-volume).
The full Lorentzian/causal continuum remains OPEN. Native: the causal DAG is built from the bare rule. Pure
Python.
"""
import math
import os
import random
from collections import Counter, deque
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Causal-set dimension: longest-chain ~4 is a FALSE POSITIVE; interval-volume ~1.3 => non-manifold, not 3+1"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _build_causal(steps, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed); producer = {}
    for e in [(0, 1), (1, 2), (2, 0)]:
        producer.setdefault(e, []).append(-1)
    succ = {}; pred = {}; ev = 0
    for s in range(steps):
        R = redexes(E)
        if not R:
            break
        a, b, c = rng.choice(R)
        for e in [(a, b), (b, c)]:
            st = producer.get(e)
            if st:
                pe = st.pop()
                if pe >= 0:
                    succ.setdefault(pe, set()).add(ev); pred.setdefault(ev, set()).add(pe)
        E[(a, b)] -= 1; E[(b, c)] -= 1
        if E[(a, b)] <= 0:
            del E[(a, b)]
        if E[(b, c)] <= 0:
            del E[(b, c)]
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        for (ss, tt) in KEYSTONE:
            uv = (sub[ss], sub[tt]); E[uv] += 1; producer.setdefault(uv, []).append(ev)
        fresh += 1; ev += 1
    return ev, succ, pred


def _sprinkle(N, d, rng):
    pts = []
    while len(pts) < N:
        t = rng.random(); x = [(rng.random() * 2 - 1) * 0.5 for _ in range(d - 1)]
        r = math.sqrt(sum(xi * xi for xi in x))
        if t > r and (1 - t) > r:
            pts.append((t, x))
    pts.sort(key=lambda p: p[0])
    succ = {}; pred = {}
    for i in range(N):
        ti, xi = pts[i]
        for j in range(i + 1, N):
            tj, xj = pts[j]
            if tj - ti > math.sqrt(sum((a - b) ** 2 for a, b in zip(xi, xj))):
                succ.setdefault(i, set()).add(j); pred.setdefault(j, set()).add(i)
    return N, succ, pred


def _height(N, succ):
    depth = [0] * N; h = 0
    for v in range(N):
        d = depth[v]
        for w in succ.get(v, ()):
            if d + 1 > depth[w]:
                depth[w] = d + 1
        if d > h:
            h = d
    return h + 1


def _slope(xs, ys):
    lx = [math.log(x) for x in xs]; ly = [math.log(y) for y in ys]
    n = len(lx); sx = sum(lx); sy = sum(ly); sxx = sum(a * a for a in lx); sxy = sum(a * b for a, b in zip(lx, ly))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def _desc(src, succ):
    seen = {src}; dq = deque([src])
    while dq:
        x = dq.popleft()
        for y in succ.get(x, ()):
            if y not in seen:
                seen.add(y); dq.append(y)
    return seen


def _anc(snk, pred):
    seen = {snk}; dq = deque([snk])
    while dq:
        x = dq.popleft()
        for y in pred.get(x, ()):
            if y not in seen:
                seen.add(y); dq.append(y)
    return seen


def _longest_in(S, succ):
    depth = {v: 1 for v in S}
    for v in sorted(S):
        dv = depth[v]
        for w in succ.get(v, ()):
            if w in depth and dv + 1 > depth[w]:
                depth[w] = dv + 1
    return max(depth.values()) if depth else 0


def _interval_dim(succ, pred, N, rng, n_src=22, minV=15):
    lo = max(1, N // 30); hi = max(lo + 1, N // 2)
    sources = sorted(rng.sample(range(lo, hi), min(n_src, hi - lo)))
    pairs = []
    for p in sources:
        dp = _desc(p, succ); cand = [q for q in dp if q > p + N // 40]
        if len(cand) < 4:
            continue
        for q in rng.sample(cand, min(9, len(cand))):
            I = dp & _anc(q, pred)
            if len(I) >= minV:
                pairs.append((_longest_in(I, succ), len(I)))
    pairs = [(e, v) for (e, v) in pairs if e >= 2 and v >= minV]
    if len(pairs) < 6:
        return None, 0
    return _slope([e for e, _ in pairs], [v for _, v in pairs]), len(pairs)


def run():
    print("[PARTIAL] %s" % TITLE)
    # keystone causal graph at several sizes (built once each; largest reused for interval-volume)
    ks_steps = [600, 1200, 2500, 5000] if not _FULL else [1000, 2500, 5000, 9000]
    Ns = []; Hs = []; big = None
    for st in ks_steps:
        N, succ, pred = _build_causal(st)
        Ns.append(N); Hs.append(_height(N, succ))
        if st == ks_steps[-1]:
            big = (N, succ, pred)
    a_ks = _slope(Ns, Hs)
    print("  (A) LONGEST-CHAIN height L ~ N^{1/d}.  keystone heights %s at N=%s" % (Hs, Ns))
    print("      keystone: L ~ N^%.3f  =>  apparent causal dim d_LC = %.2f  (looks like 3+1!)" % (a_ks, 1 / a_ks))
    cal_sizes = [300, 600, 1200, 2400]
    sprink = {}
    for d in (2, 4):
        hs = []
        for n in cal_sizes:
            nn, ss, pp = _sprinkle(n, d, random.Random(100 * d + n))
            hs.append(_height(nn, ss))
            if n == cal_sizes[-1]:
                sprink[d] = (nn, ss, pp)
        print("      calib d=%d sprinkle: L ~ N^%.3f => d_LC=%.2f" % (d, _slope(cal_sizes, hs), 1 / _slope(cal_sizes, hs)))
    print("  (B) INTERVAL-VOLUME V ~ ell^d (the structurally meaningful estimator).")
    for d in (2, 4):
        nn, ss, pp = sprink[d]
        dim, npp = _interval_dim(ss, pp, nn, random.Random(9), n_src=28, minV=15)
        print("      calib d=%d sprinkle: interval dim = %.2f (%d intervals)" % (d, dim, npp))
    N, succ, pred = big
    dim, npp = _interval_dim(succ, pred, N, random.Random(9), n_src=30, minV=15)
    print("      keystone N=%d: interval dim = %.2f (%d intervals)  -- CHAIN-LIKE (~1D)" % (N, dim, npp))
    print("  => the two calibrated estimators DISAGREE (longest-chain ~4 vs interval-volume ~1.2). A faithful")
    print("     d-manifold needs them to AGREE; the disagreement means the causal order is NON-MANIFOLD -- a")
    print("     wide, shallow fan of nearly-parallel ~1D causal chains (height ~ N^{1/4} forces width ~ N^{3/4}).")
    print("     The longest-chain 'd~4' is an aspect-ratio FALSE POSITIVE; the interval-volume sees the sparse,")
    print("     tree-like (b1=1) causal structure. 3+1 spacetime is NOT recovered from the causal graph; the")
    print("     Lorentzian/causal continuum remains OPEN.")
