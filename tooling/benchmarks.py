"""Engine benchmarks

AXIOM/GOAL: Benchmark the substrate engine at scale.
APPROACH:   Time evolution and observation at increasing N; partial.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Engine benchmarks"
AXIOM = "Benchmark the substrate engine at scale."
APPROACH = "Time evolution and observation at increasing N; partial."


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
