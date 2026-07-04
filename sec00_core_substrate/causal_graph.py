"""Causal graph: the candidate emergent spacetime.

Events are rewrites. There is a causal edge A -> B when event B consumes an edge-token that
event A produced. We give every edge-instance a unique token id and track its producer, so the
causal partial order is reconstructed exactly from a rewriting history.
"""
from collections import Counter
from sec00_core_substrate.hypergraph import nodes
from sec00_core_substrate.rewriting import redexes


class TokenState:
    """A hypergraph whose individual edge-instances carry unique ids (for provenance)."""

    def __init__(self, edges):
        self.mult = Counter()      # (a,b) -> multiplicity
        self.tokens = {}           # (a,b) -> list of token ids
        self.producer = {}         # token id -> producing event index (None for seed)
        self._next = 0
        for e in edges:
            self._add(e, None)

    def _add(self, e, ev):
        tid = self._next
        self._next += 1
        self.mult[e] += 1
        self.tokens.setdefault(e, []).append(tid)
        self.producer[tid] = ev
        return tid


def build_causal_graph(edges, rhs, steps, rng):
    """Return (events, causal_edges); causal_edges are (producer_event, consumer_event)."""
    st = TokenState(edges)
    fresh = (max(nodes(Counter(edges))) + 1) if edges else 0
    events, causal = [], []
    for _ in range(steps):
        R = redexes(st.mult)
        if not R:
            break
        a, b, c = rng.choice(R)
        t1 = st.tokens[(a, b)].pop()
        t2 = st.tokens[(b, c)].pop()
        st.mult[(a, b)] -= 1; st.mult[(b, c)] -= 1
        if st.mult[(a, b)] <= 0:
            del st.mult[(a, b)]
        if st.mult[(b, c)] <= 0:
            del st.mult[(b, c)]
        ev = len(events)
        events.append((a, b, c))
        for t in (t1, t2):
            p = st.producer.get(t)
            if p is not None:
                causal.append((p, ev))
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        fresh += 1
        for (s, t) in rhs:
            st._add((sub[s], sub[t]), ev)
    return events, causal


# --- §0.3 Evolution history: build the causal graph and confirm it is an acyclic partial order ---
def run():
    import random
    from collections import deque
    from constants import KEYSTONE
    print("[DERIVED] 0.3 Evolution history -- the causal graph is reconstructed exactly, and is a DAG")
    rng = random.Random(0)
    events, causal = build_causal_graph([(0, 1), (1, 2), (2, 0)], KEYSTONE, 200, rng)
    back = sum(1 for (p, c) in causal if p >= c)
    indeg = {}; adj = {}
    for (p, c) in causal:
        indeg[c] = indeg.get(c, 0) + 1; adj.setdefault(p, []).append(c)
    q = deque([e for e in range(len(events)) if indeg.get(e, 0) == 0]); seen = 0
    while q:
        u = q.popleft(); seen += 1
        for v in adj.get(u, ()):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    print("  %d events, %d causal edges; edges with producer>=consumer: %d; acyclic (DAG): %s"
          % (len(events), len(causal), back, seen == len(events)))
    print("  -> a genuine partial order: no closed causal loops. The candidate spacetime is well-formed.")
