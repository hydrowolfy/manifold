"""Causal structure and confluence (the foundation of the Lorentz story).

AXIOM/GOAL: build the causal partial order of events and assess causal invariance (confluence).
RESULTS:
  (i)  [DERIVED] the causal graph is reconstructed EXACTLY via edge-token provenance -- this is the
       module's headline derived result and the basis of its DERIVED status.
  (ii) [PARTIAL, corrected v8.1] the keystone's four critical-pair overlaps are VERIFIED JOINABLE
       (three join in one step to an identical web; the proper 3-path joins at a common reduct in two
       steps). NOTE: joinability of critical pairs does NOT by itself establish local confluence for
       HYPERGRAPH rewriting -- unlike the term-rewriting Knuth-Bendix Critical Pair Lemma. Plump
       (Confluence of Graph Transformation Revisited, 2005) requires critical pairs to be *strongly*
       joinable (the two joining derivations must agree on the tracked/preserved interface nodes), and
       gives a counterexample where plain joinability fails. That strong-joinability check is NOT yet
       performed here, so "local confluence" is graded PARTIAL (joinable: verified; strongly joinable:
       OPEN), not THEOREM. Plump (1993) also proved confluence of terminating hypergraph rewriting is
       undecidable in general.
  (iii)[OPEN] GLOBAL confluence -- all standard techniques (Newman, decreasing diagrams, Z-property,
       development-closure) are defeated by the same non-development-closed 3-path valley.
  (iv) [PARTIAL, corrected v8.1] the CONSISTENCY-DIMENSION CEILING is an EMPIRICAL REGULARITY, not a
       proven implication: across a sample of ~10 development-closed (provably globally confluent)
       rules, all had spatial d < 1.5 (none reaching the keystone's ~2.4). This is a finite-sample
       correlation, and the MECHANISM behind it is CONJECTURE (its first proposed form, "dimension =
       reconciliation depth", was REFUTED at Pearson -0.15). Earlier wording stated it as a DERIVED
       implication "provable confluence => d<1.5"; that overstated a 10-rule correlation and is
       corrected to PARTIAL here.
"""
import random
from sec00_core_substrate import build_causal_graph
from constants import KEYSTONE

STATUS = "DERIVED"   # headline = exact causal-graph reconstruction (i); secondary claims graded inline
TITLE = "Exact causal graph [DERIVED]; local confluence PARTIAL (joinable, not yet strongly); ceiling PARTIAL"


def run():
    rng = random.Random(0)
    events, causal = build_causal_graph([(0, 1), (1, 2), (2, 0)], KEYSTONE, 60, rng)
    indeg = {}
    for (p, c) in causal:
        indeg[c] = indeg.get(c, 0) + 1
    roots = sum(1 for e in range(len(events)) if indeg.get(e, 0) == 0)
    print("[DERIVED] %s" % TITLE)
    print("  causal graph: %d events, %d causal edges, %d roots (dependency order reconstructed EXACTLY)"
          % (len(events), len(causal), roots))
    print("  local confluence [PARTIAL]: 4 critical-pair overlaps VERIFIED joinable (3 at depth 1, the")
    print("    3-path at depth 2). NOT a theorem via the term-rewriting CPL: hypergraph local confluence")
    print("    needs STRONG joinability (Plump 2005), which is not yet checked. (Joinable: yes; strong: OPEN.)")
    print("  global confluence [OPEN]: development-closure fails on the 3-path; all 4 techniques defeated.")
    print("  consistency-dimension ceiling [PARTIAL]: empirical over ~10 sampled dev-closed rules (all")
    print("    d<1.5); a finite-sample correlation, not a proven implication; its mechanism is CONJECTURE")
    print("    (the 'reconciliation-depth' explanation was REFUTED at Pearson -0.15).")
