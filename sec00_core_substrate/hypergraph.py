"""Multiset hypergraph substrate.

Edges are directed and stored as a Counter: parallel edges are DISTINCT (the Wolfram-model
reading). This multiset structure is not optional -- the conserved topological charge (first
Betti number) only holds because parallel edges count separately.
"""
from collections import Counter


def nodes(E):
    s = set()
    for (a, b) in E:
        s.add(a); s.add(b)
    return s


def num_edges(E):
    return sum(E.values())


def components(E):
    """Number of weakly-connected components."""
    adj = {}
    for (a, b), m in E.items():
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen, c = set(), 0
    for s in nodes(E):
        if s in seen:
            continue
        c += 1; stack = [s]; seen.add(s)
        while stack:
            u = stack.pop()
            for v in adj.get(u, ()):
                if v not in seen:
                    seen.add(v); stack.append(v)
    return c


def from_edges(edges):
    return Counter(edges)


def copy(E):
    return Counter(E)


# --- §0.1 Hypergraph state: a runnable demonstration of the substrate's read-outs ---
def run():
    from collections import Counter
    print("[DEF] 0.1 Hypergraph state -- the substrate is a multiset of directed edges")
    E = Counter([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)])
    print("  example world: %d edges, %d nodes, %d weakly-connected component(s)"
          % (num_edges(E), len(nodes(E)), components(E)))
    print("  parallel edges are DISTINCT (multiset): adding a 2nd (0,1) ->")
    E[(0, 1)] += 1
    print("    %d edges, %d nodes (same node set, one more edge) -- this is load-bearing for charge b1."
          % (num_edges(E), len(nodes(E))))
