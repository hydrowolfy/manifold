"""Cosmological expansion (de Sitter)

AXIOM/GOAL: Recover an expanding cosmology.
APPROACH:   The de Sitter sector with negative curvature K and linear volume growth; quantitative cosmology owed.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Cosmological expansion (de Sitter)"
AXIOM = "Recover an expanding cosmology."
APPROACH = "The de Sitter sector with negative curvature K and linear volume growth; quantitative cosmology owed."


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
