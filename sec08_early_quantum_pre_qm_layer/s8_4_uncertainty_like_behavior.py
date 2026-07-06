"""An uncertainty relation

AXIOM/GOAL: Derive conjugate-observable uncertainty.
APPROACH:   Non-commutativity of spatial vs branchial (rewrite-order) observables; not started.
STATUS:     OPEN
"""
STATUS = "OPEN"
TITLE = "An uncertainty relation"
AXIOM = "Derive conjugate-observable uncertainty."
APPROACH = "Non-commutativity of spatial vs branchial (rewrite-order) observables; not started."


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
