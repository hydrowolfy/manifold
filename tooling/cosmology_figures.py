"""Cosmology figures

AXIOM/GOAL: Render figures for the gravity/cosmology results.
APPROACH:   Plot curvature, expansion, horizon scaling once derived. Not started.
STATUS:     OPEN
"""
STATUS = "OPEN"
TITLE = "Cosmology figures"
AXIOM = "Render figures for the gravity/cosmology results."
APPROACH = "Plot curvature, expansion, horizon scaling once derived. Not started."


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
