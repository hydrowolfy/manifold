#!/usr/bin/env python3
"""Read-only: dump the per-time-slice spatial-volume profile N3(t) of a saved causal-CDT
state pickle (or an exact Kuhn T^3), plus preregistered collapse-vs-extended shape stats.
Profile p(t) = number of spatial triangles (all 3 verts in slice t) per slice t=0..T-1 --
identical definition to remeasure.py. Deterministic given the state (no estimator seed)."""
import argparse, json, math, os, pickle, sys, itertools
from collections import Counter, defaultdict
os.environ.setdefault("MANIFOLD_REPO", os.getcwd())
sys.path[:0] = [os.getcwd(), os.path.join(os.getcwd(), "tooling")]
import cdt_causal_run as C
import __main__
__main__.Causal = C.Causal
__main__.IndexedSet = C.IndexedSet


def profile_from_state(st):
    pf = Counter()
    for f in st.stris:
        pf[st.time[next(iter(f))]] += 1
    return [pf.get(t, 0) for t in range(st.T)]


def stats(prof):
    T = len(prof); tot = sum(prof); mean = tot / max(1, T)
    var = sum((x - mean) ** 2 for x in prof) / max(1, T)
    sd = math.sqrt(var)
    cv = sd / mean if mean else 0.0
    mx, mn = max(prof), min(prof)
    srt = sorted(prof, reverse=True)
    c1 = srt[0] / tot if tot else 0.0
    c2 = (srt[0] + srt[1]) / tot if (tot and T > 1) else c1
    half = mx / 2.0
    stalk_q = sum(1 for x in prof if x <= 0.25 * mean)   # depleted-to-floor slices
    above_half = sum(1 for x in prof if x >= half)        # slices in the "blob"
    return dict(T=T, total=tot, mean=round(mean, 1), sd=round(sd, 1), cv=round(cv, 3),
                max=mx, min=mn, min_over_mean=round(mn / mean, 3) if mean else 0.0,
                max_over_mean=round(mx / mean, 3) if mean else 0.0,
                C1_topslice_frac=round(c1, 3), C2_top2_frac=round(c2, 3),
                stalk_slices_le_0p25mean=stalk_q, blob_slices_ge_halfmax=above_half)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    with open(a.pkl, "rb") as fh:
        blob = pickle.load(fh)
    st = blob["st"]
    prof = profile_from_state(st)
    s = stats(prof)
    meta = dict(tag=a.tag, N0=st.N0, N3=st.N3, T=st.T,
                f22=round(st.nk[2] / max(1, st.N3), 4), k3=round(blob.get("k3", float("nan")), 4))
    print(json.dumps(dict(meta=meta, stats=s, profile=prof)))


if __name__ == "__main__":
    main()
