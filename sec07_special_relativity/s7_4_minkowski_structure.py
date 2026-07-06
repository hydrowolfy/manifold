"""Minkowski-signature metric from order

AXIOM/GOAL: Recover a Lorentzian-signature metric from the causal partial order.
APPROACH:   Causal-set order-plus-count (Myrheim-Meyer, Benincasa-Dowker); relied upon, not re-derived.
STATUS:     BORROWED
"""
STATUS = "BORROWED"
TITLE = "Minkowski-signature metric from order"
AXIOM = "Recover a Lorentzian-signature metric from the causal partial order."
APPROACH = "Causal-set order-plus-count (Myrheim-Meyer, Benincasa-Dowker); relied upon, not re-derived."


def run():
    print("[%s] %s" % (STATUS, TITLE))
    print("  goal:     " + AXIOM)
    print("  approach: " + APPROACH)
    _note = {
        "OPEN": ">> Not yet derived. Target and approach recorded; no result is claimed.",
        "BORROWED": ">> Relies on an external theorem; not re-derived inside this program.",
        "CONJECTURE": ">> Proposed but untested. No numerical support yet.",
        "PARTIAL": ">> A partial result exists; the full derivation is incomplete (see whitepaper).",
    }.get(STATUS)
    if _note:
        print("  " + _note)
