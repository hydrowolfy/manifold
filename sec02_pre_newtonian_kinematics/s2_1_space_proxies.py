"""Graph distance as the emergent metric

AXIOM/GOAL: Treat shortest-path graph distance as the spatial metric and identify geodesics.
APPROACH:   BFS shortest paths (already used by ball_dimension); geodesic deviation vs curvature is owed.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Graph distance as the emergent metric"
AXIOM = "Treat shortest-path graph distance as the spatial metric and identify geodesics."
APPROACH = "BFS shortest paths (already used by ball_dimension); geodesic deviation vs curvature is owed."


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
