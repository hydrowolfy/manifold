"""Decoherence and the classical limit

AXIOM/GOAL: Explain decoherence and horizons via one monotone quantity.
APPROACH:   The de Sitter / circuit-complexity conjecture: decoherence, black-hole horizons and cosmological horizons unified by monotonicity of branch-swap unitary complexity. Proposed, untested.
STATUS:     CONJECTURE
"""
STATUS = "CONJECTURE"
TITLE = "Decoherence and the classical limit"
AXIOM = "Explain decoherence and horizons via one monotone quantity."
APPROACH = "The de Sitter / circuit-complexity conjecture: decoherence, black-hole horizons and cosmological horizons unified by monotonicity of branch-swap unitary complexity. Proposed, untested."


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
