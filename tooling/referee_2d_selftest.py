#!/usr/bin/env python3
"""Self-tests that CALIBRATE the referee 2D tooling on objects with KNOWN topology.

If these pass, the topology layer returns the textbook answer on a disk, a triangulated
disk, and an annulus, and the holdout estimators respond in the expected direction on a
degree-preserving rewire. That is what licenses trusting the same code on the candidate.

Run:  PYTHONPATH=. python3 tooling/referee_2d_selftest.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import networkx as nx
import referee_2d_topology as TP
import referee_2d_scaling as SC

_fail = []


def check(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        _fail.append(name)


# 1) GF(2) rank primitive
check("gf2_rank: dependent vector detected", TP.gf2_rank([0b011, 0b110, 0b101]) == 2)
check("gf2_rank: independent basis", TP.gf2_rank([1, 2, 4]) == 3)

# 2) rectangular grid must be a clean disk
g, _ = TP.rect_grid_adj(100)
r = TP.analyze(g, "grid")
check("grid: planar", r["planar"])
check("grid: euler_char == 1 (disk)", r["euler_char"] == 1)
check("grid: b1 == 0 and b2 == 0", r["b1"] == 0 and r["b2"] == 0)
check("grid: 0 bridges", r["bridges"] == 0)
check("grid: 0 articulation points", r["articulation_points"] == 0)
check("grid: 0 bad vertex links", r["bad_links"] == 0)
check("grid: single simple boundary cycle", r["single_simple_boundary_cycle"])
check("grid: orientable", r["orientable"])
check("grid: all faces quads (81), no triangles", r["n_quads"] == 81 and r["n_triangles"] == 0)

# 3) triangulated disk must also be a clean disk
t, _ = TP.rect_tri_grid_adj(100)
rt = TP.analyze(t, "tri")
check("tri_disk: euler_char == 1", rt["euler_char"] == 1)
check("tri_disk: b1 == 0", rt["b1"] == 0)
check("tri_disk: 0 bridges", rt["bridges"] == 0)
check("tri_disk: single simple boundary", rt["single_simple_boundary_cycle"])

# 4) annulus: fill every bounded face EXCEPT one -> the open face is a hole -> b1 == 1
G = TP.to_graph(g)
isp, faces, he2face, outer = TP.planar_faces(G)
edges = list(G.edges())
eidx = {frozenset(e): i for i, e in enumerate(edges)}
cols = []
dropped = None
for fid, f in enumerate(faces):
    if fid == outer:
        continue
    if dropped is None and len(f) == 4:      # leave one interior quad OPEN (a hole)
        dropped = fid
        continue
    cnt = {}
    for i in range(len(f)):
        e = frozenset((f[i], f[(i + 1) % len(f)]))
        cnt[eidx[e]] = cnt.get(eidx[e], 0) + 1
    vec = 0
    for ei, c in cnt.items():
        if c % 2:
            vec |= (1 << ei)
    if vec:
        cols.append(vec)
c0 = nx.number_connected_components(G)
E = len(edges)
b1 = (E - (G.number_of_nodes() - c0)) - TP.gf2_rank(cols)
check("annulus (grid minus one face): b1 == 1", b1 == 1)

# 5) candidate: disk-by-construction, but riddled with local defects
adj = TP.candidate_adj(150, 0, 120)
rc = TP.analyze(adj, "candidate")
check("candidate: planar euler_char == 1", rc["euler_char"] == 1)
check("candidate: bridges > 0", rc["bridges"] > 0)
check("candidate: bad vertex links > 0", rc["bad_links"] > 0)
check("candidate: triangles dominate quads", rc["n_triangles"] > rc["n_quads"])

# 6) holdout estimator responds: degree-preserving rewire raises lazy-RW d_s
cand_ds = SC.lazy_rw_sdim(adj)["8-24"]
rw_ds = SC.lazy_rw_sdim(SC.rewire(adj, 0))["8-24"]
check("rewire raises lazy-RW d_s above candidate (%.2f > %.2f)" % (rw_ds, cand_ds), rw_ds > cand_ds)

# 7) grid holdout d_s clearly exceeds candidate (calibration of the gap)
check("grid lazy-RW d_s > candidate", SC.lazy_rw_sdim(g)["8-24"] > cand_ds)

print()
if _fail:
    print("SELF-TESTS FAILED: %d" % len(_fail))
    sys.exit(1)
print("ALL SELF-TESTS PASSED")
