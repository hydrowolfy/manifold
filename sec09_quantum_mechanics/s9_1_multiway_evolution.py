"""Branchial space (space of rewrite-order branches)

AXIOM/GOAL: Build the multiway evolution graph and the branchial metric.
APPROACH:   Branches = distinct rewrite orders; branchial distance = common-ancestor metric; structure defined, metric not characterised.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Branchial space (space of rewrite-order branches)"
AXIOM = "Build the multiway evolution graph and the branchial metric."
APPROACH = "Branches = distinct rewrite orders; branchial distance = common-ancestor metric; structure defined, metric not characterised."


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
