"""Contact with observation

AXIOM/GOAL: Connect emergent quantities to real observations.
APPROACH:   Map emergent expansion/curvature to observables (e.g. Hubble tension); no quantitative prediction yet. Not started.
STATUS:     OPEN
"""
STATUS = "OPEN"
TITLE = "Contact with observation"
AXIOM = "Connect emergent quantities to real observations."
APPROACH = "Map emergent expansion/curvature to observables (e.g. Hubble tension); no quantitative prediction yet. Not started."


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
