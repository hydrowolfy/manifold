"""Relativistic velocity addition

AXIOM/GOAL: Derive the velocity-composition law for emergent excitations.
APPROACH:   The glider has a definite velocity (1/2 rail-node per firing); the composition (addition) law is not yet derived.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Relativistic velocity addition"
AXIOM = "Derive the velocity-composition law for emergent excitations."
APPROACH = "The glider has a definite velocity (1/2 rail-node per firing); the composition (addition) law is not yet derived."


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
