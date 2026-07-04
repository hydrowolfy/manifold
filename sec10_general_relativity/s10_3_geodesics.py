"""Matter follows geodesics

AXIOM/GOAL: Show a free excitation tracks geodesics of the curved emergent graph.
APPROACH:   Couple mechanics/inertia (the glider path) to gravity/curvature; not started.
STATUS:     OPEN
"""
STATUS = "OPEN"
TITLE = "Matter follows geodesics"
AXIOM = "Show a free excitation tracks geodesics of the curved emergent graph."
APPROACH = "Couple mechanics/inertia (the glider path) to gravity/curvature; not started."


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
