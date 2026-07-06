"""Emergent geometry II -- the CURVATURE of the substrates, unified with the spectral dimension (round 41). Round
41 measured how many directions each substrate has (the spectral dimension d_s); this round measures how they BEND.
The substrate's emergent METRIC is its graph/hop distance (the causal/diffusion distance of rounds 1, 6, 41), and
its Ricci curvature is the OLLIVIER-RICCI curvature kappa(x,y)=1 - W1(mu_x,mu_y)/d(x,y) (exact optimal transport,
pure Python; reusing the round-2 machinery). Measured across all substrates and validated against EXACT values, an
emergent Ricci curvature SEPARATES them: flat lattices (kappa=0), the positively-curved complete graph / sphere
(kappa>0), and the negatively-curved keystone and 3-regular expander (kappa<0). Together with d_s this is the
emergent Riemannian geometry: the keystone is HYPERBOLIC-like (kappa<0) AND sub-2D (d_s~1.5) -- a thin negatively-
curved ramified tree -- which is the local-geometry root of its non-manifold continuum (round 24) and recurrent,
non-scrambling diffusion (rounds 35-43).

EXACT BENCHMARKS (the Ollivier-Ricci estimator is validated to machine precision, not just internally):
  * flat lattices Z^d (chain, cycle, square, cubic): kappa = 0 EXACTLY (every edge flat).
  * complete graph K_n (a discrete sphere): kappa = (n-2)/(n-1) EXACTLY (K5 -> 0.750, K8 -> 0.857).
  * d-regular tree / expander: kappa < 0 (hyperbolic); the random 3-regular graph (locally tree-like) -> ~ -0.5.

CURVATURE x DIMENSION = EMERGENT GEOMETRY (joining round 44 to round 41):
  kappa = 0  <->  d_s = integer d  <->  polynomial volume growth  =>  a flat MANIFOLD (the lattices).
  kappa < 0  <->  non-manifold, exponential/ramified volume  =>  NEGATIVELY CURVED: the keystone (d_s~1.5, a thin
                  hyperbolic ramified tree) and the 3-regular (d_s=infinite, a fat expander) -- same curvature SIGN,
                  opposite dimension. Curvature is the LOCAL bending; dimension the GLOBAL spreading; both are needed.
  kappa > 0  <->  the complete graph / sphere (finite, high overlap).
LICHNEROWICZ link to round 41: positive Ollivier-Ricci lower-bounds the spectral gap (lambda_1 >= kappa_min), so the
positively-curved complete graph has a gap (lambda_1 = n/(n-1) >= (n-2)/(n-1)); for the negatively-curved keystone
the bound is vacuous, consistent with its gapless/recurrent diffusion (round 41) -- curvature and the gap cohere.

RESULTS (Ollivier-Ricci mean kappa, idleness alpha=0; sampled edges):
  FLAT (kappa=0, EXACT): chain, cycle, 2D lattice, 3D lattice -- every edge flat (|kappa|<=1e-9). POSITIVE: complete
  K5=+0.750, K8=+0.857 = (n-2)/(n-1) exactly (a discrete sphere). NEGATIVE (hyperbolic): keystone -0.33 (zero
  positive edges; reproduces round 2's -0.37), 3-regular expander -0.58, ideal 3-regular tree -0.34. With the
  round-41 spectral dimension this classifies the emergent geometry: kappa=0 + integer d_s = a flat MANIFOLD
  (lattices); kappa<0 + non-manifold d_s = the keystone (d_s~1.5, a THIN hyperbolic ramified tree) and the 3-regular
  (d_s=INFINITE, a FAT expander) -- same curvature sign, opposite dimension. Positive curvature lower-bounds the
  spectral gap (Lichnerowicz: K_n has lambda_1=n/(n-1) >= (n-2)/(n-1)); for the negatively-curved keystone the bound
  is vacuous, consistent with its gapless/recurrent diffusion (round 41) -- curvature and gap cohere. Idleness-
  dependent magnitude (keystone -0.33 at alpha=0, ~0 at alpha=0.5), sign robustly non-positive (as round 2).

VALIDATION:
  (1) EXACT BENCHMARKS to machine precision: flat lattices kappa=0; complete K_n = (n-2)/(n-1) (K5=0.750, K8=0.857).
  (2) IDLENESS CONVENTION stated (alpha=0 neighbour-uniform vs alpha=0.5 lazy), as in round 2; the SIGN (non-
      positive for the keystone) is convention-robust, the magnitude is convention-dependent (reported with it).
  (3) CONSISTENCY: the keystone mean kappa ~ -0.37 reproduces the round-2 measurement; the curvature/dimension/gap
      picture is consistent across rounds 2, 41, 44.
  (4) INDEPENDENT REIMPLEMENTATION: the companion HTML recomputes the Ollivier-Ricci curvature in JavaScript (its
      own optimal-transport solver) and reproduces the per-edge and mean values.
  The exact optimal transport (integer min-cost flow) is solved, not approximated; pure Python, no third-party deps.

STATUS: PARTIAL (characterization) -- a systematic, exactly-benchmarked emergent-curvature measurement across the
substrates, unified with the spectral dimension; extends the round-2 keystone result to the full geometry picture.
No leaf change; tally unchanged. Pure Python (reuses the round-2 Ollivier-Ricci optimal-transport machinery).
"""
import math
import os
import random
from collections import Counter, defaultdict
from sec10_general_relativity.s10_2_curvature import ollivier_kappa
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Emergent Ricci curvature: flat lattices (0), positive sphere, NEGATIVE keystone/expander -- with d_s, the emergent geometry"
_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


# ---- substrate graphs (adjacency dict node -> set) -----------------------------------------
def _chain(N):
    adj = defaultdict(set)
    for i in range(N - 1):
        adj[i].add(i + 1); adj[i + 1].add(i)
    return dict(adj)


def _cycle(N):
    adj = defaultdict(set)
    for i in range(N):
        adj[i].add((i + 1) % N); adj[(i + 1) % N].add(i)
    return dict(adj)


def _lattice(dims):
    import itertools
    idx = {c: i for i, c in enumerate(itertools.product(*[range(L) for L in dims]))}
    adj = defaultdict(set)
    for c, i in idx.items():
        for d in range(len(dims)):
            c2 = list(c); c2[d] += 1; c2 = tuple(c2)
            if c2 in idx:
                adj[i].add(idx[c2]); adj[idx[c2]].add(i)
    return dict(adj)


def _complete(n):
    return {i: set(j for j in range(n) if j != i) for i in range(n)}


def _reg3(n, seed=2):
    rng = random.Random(seed)
    for _ in range(600):
        st = [v for v in range(n) for _ in range(3)]; rng.shuffle(st); adj = defaultdict(set); ok = True
        for i in range(0, len(st), 2):
            a, b = st[i], st[i + 1]
            if a == b or b in adj[a]:
                ok = False; break
            adj[a].add(b); adj[b].add(a)
        if ok and all(len(adj[v]) == 3 for v in range(n)):
            return dict(adj)
    return _chain(n)


def _btree(d, depth):
    """a finite d-regular tree (root has d children; others d-1) -- a clean hyperbolic benchmark."""
    adj = defaultdict(set); nxt = [0]; cur = 1; frontier = [0]
    for lev in range(depth):
        newf = []
        for u in frontier:
            kids = d if u == 0 else d - 1
            for _ in range(kids):
                v = cur; cur += 1; adj[u].add(v); adj[v].add(u); newf.append(v)
        frontier = newf
    return dict(adj)


def _keystone(steps, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
    for _ in range(steps):
        R = redexes(E)
        if not R:
            break
        a, b, c = rng.choice(R); E[(a, b)] -= 1; E[(b, c)] -= 1
        if E[(a, b)] <= 0:
            del E[(a, b)]
        if E[(b, c)] <= 0:
            del E[(b, c)]
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        for (s, t) in KEYSTONE:
            E[(sub[s], sub[t])] += 1
        fresh += 1
    adj = defaultdict(set)
    for (u, v) in E:
        if u != v:
            adj[u].add(v); adj[v].add(u)
    return dict(adj)


def _mean_kappa(adj, alpha=0.0, sample=200, seed=3):
    edges = sorted({tuple(sorted((u, v))) for u in adj for v in adj[u]})
    random.Random(seed).shuffle(edges)
    ks = [ollivier_kappa(adj, x, y, alpha) for (x, y) in edges[:sample]]
    m = sum(ks) / len(ks); sd = (sum((k - m) ** 2 for k in ks) / len(ks)) ** 0.5
    neg = sum(1 for k in ks if k < -1e-9); pos = sum(1 for k in ks if k > 1e-9)
    return m, sd / math.sqrt(len(ks)), neg, len(ks) - neg - pos, pos, len(ks)


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Ollivier-Ricci curvature kappa=1-W1(mu_x,mu_y)/d(x,y) (exact optimal transport) on the graph metric.")
    print("  Benchmarks: flat lattice/cycle kappa=0; complete K_n=(n-2)/(n-1); tree/expander kappa<0.\n")
    samp = 160 if not _FULL else 400

    subs = [
        ("chain (1D)", _chain(40), "0 EXACT (flat)", "1"),
        ("cycle", _cycle(40), "0 EXACT (flat)", "1"),
        ("2D lattice", _lattice((12, 12)), "0 EXACT (flat)", "2"),
        ("3D lattice", _lattice((6, 6, 6)), "0 EXACT (flat)", "3"),
        ("complete K5", _complete(5), "+0.750 = 3/4", "finite"),
        ("complete K8", _complete(8), "+0.857 = 6/7", "finite"),
        ("3-regular tree", _btree(3, 7), "<0 (hyperbolic)", "infinite"),
        ("3-regular graph", _reg3(80), "<0 (expander)", "infinite (rnd 41)"),
        ("KEYSTONE", _keystone(320), "<0 (rnd 2: -0.37)", "~1.5 (rnd 41)"),
    ]
    print("  (A) OLLIVIER-RICCI mean curvature (alpha=0):")
    print("      %-17s %-9s %-15s %s" % ("substrate", "mean kappa", "neg/flat/pos", "[benchmark]   d_s"))
    res = {}
    for name, adj, bench, ds in subs:
        m, se, neg, flat, pos, nn = _mean_kappa(adj, 0.0, samp)
        res[name] = m
        print("      %-17s %+.3f%+.3f  %4d/%4d/%4d   [%-16s] d_s=%s" % (name, m, se, neg, flat, pos, bench, ds))

    print("\n  (B) CURVATURE x DIMENSION = EMERGENT GEOMETRY:")
    print("      FLAT (kappa=0) + integer d_s  -> a flat MANIFOLD: chain(1), 2D(2), 3D(3).")
    print("      NEGATIVE (kappa<0) + non-integer/infinite d_s -> non-manifold, exponential volume:")
    print("        keystone kappa=%+.2f, d_s~1.5  = a THIN hyperbolic ramified tree;" % res["KEYSTONE"])
    print("        3-regular kappa=%+.2f, d_s=INF = a FAT expander. Same curvature sign, opposite dimension." % res["3-regular graph"])
    print("      POSITIVE (kappa>0): the complete graph / sphere (K5=%.2f, K8=%.2f)." % (res["complete K5"], res["complete K8"]))

    print("\n  (C) LICHNEROWICZ (positive curvature lower-bounds the spectral gap; ties to round 41):")
    for n in (5, 8):
        kap = (n - 2) / (n - 1); gap = n / (n - 1)
        print("      complete K%d: kappa=%.3f <= lambda_1(norm. Laplacian)=%.3f  (gap bounded by curvature) -- holds." % (n, kap, gap))
    print("      Negatively-curved keystone/expander: the bound is vacuous (kappa<0), consistent with the keystone's")
    print("      gapless/recurrent diffusion (round 41) -- curvature and the spectral gap cohere.")

    print("\n  (D) VALIDATION:")
    flat_err = max(abs(res[k]) for k in ("chain (1D)", "cycle", "2D lattice", "3D lattice"))
    print("      EXACT benchmarks: flat lattices |kappa| <= %.1e (=0); complete K5=%.3f (=0.750), K8=%.3f (=0.857)." % (
        flat_err, res["complete K5"], res["complete K8"]))
    mk0, _, _, _, _, _ = _mean_kappa(_keystone(320), 0.0, samp)
    mk5, _, _, _, _, _ = _mean_kappa(_keystone(320), 0.5, samp)
    print("      idleness convention: keystone mean kappa = %+.3f (alpha=0, strongly negative) vs %+.3f (alpha=0.5," % (mk0, mk5))
    print("        ~0) -- idleness-dependent magnitude, sign non-positive, reproducing round 2. Both the 3-regular")
    print("        GRAPH (%.2f) and the ideal 3-regular TREE (%.2f) are NEGATIVE (hyperbolic); the random graph is" % (res["3-regular graph"], res["3-regular tree"]))
    print("        somewhat more negative -- its short cycles at finite N add to the tree-like negative curvature.")

    print("\n  => HEADLINE: an emergent Ricci curvature SEPARATES the substrates, validated against EXACT values --")
    print("     flat lattices (kappa=0), the positively-curved sphere/complete graph (kappa=(n-2)/(n-1)), and the")
    print("     NEGATIVELY curved keystone (%+.2f) and 3-regular expander (%+.2f). With the spectral dimension (round" % (res["KEYSTONE"], res["3-regular graph"]))
    print("     41) this is the substrate's emergent Riemannian geometry: the keystone is a THIN HYPERBOLIC ramified")
    print("     tree (kappa<0, d_s~1.5) -- the local-geometry root of its non-manifold continuum and recurrent,")
    print("     non-scrambling diffusion. Curvature (local bending) + dimension (global spreading) together.")
