"""emergence -- document-0 view. Entry point that renders the canonical reconstruction hierarchy
as the primary scoreboard and dispatches to the implementation library.

  python main.py tree                 the full document-0 hierarchy, every node graded
  python main.py status               grade tally (leaf + subsection) and section rollup
  python main.py section 4            one section, expanded to leaves
  python main.py run 4.1              run the library experiment backing subsection 4.1
  python main.py mono glider          run a monolith experiment (archive)  [needs numpy/scipy for some]
  python main.py map                  subsection -> library module / monolith command map

The implementation now lives DIRECTLY in the section folders (sec00_core_substrate/ ... sec13_*/),
one module per subsection, mirroring document 0; sec00 is the shared engine. tree.py is the single
source of truth for grades; dev tooling (regression checks, figure stubs) lives in tooling/.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tree as T

# subsection rollup = the "best" (most-resolved) grade among its leaves, for a quick read
_ORDER = {"DERIVED": 0, "PARTIAL": 1, "BORROWED": 2, "CONJECTURE": 3, "DEF": 4, "EXT": 5,
          "REFUTED": 6, "OPEN": 7}
_TAG = {"DERIVED": "[DERIVED]   ", "PARTIAL": "[PARTIAL]   ", "BORROWED": "[BORROWED]  ",
        "CONJECTURE": "[CONJECTURE]", "OPEN": "[OPEN]      ", "REFUTED": "[REFUTED]   ",
        "DEF": "[DEF]       ", "EXT": "[EXT]       "}


def _rollup(sub):
    grades = [lf["status"] for lf in sub["leaves"]]
    return min(grades, key=lambda g: _ORDER.get(g, 9)) if grades else sub["status"]


def tree(full_leaves=True):
    print("=" * 86)
    print(" emergence -- reconstruction hierarchy (document 0), every node graded")
    print("=" * 86)
    for num, name, subs in T.SECTIONS:
        print("\n%s. %s" % (num, name.upper()))
        for s in subs:
            avail = []
            _e = T.explist(s)
            if _e:
                avail.append("code:" + ",".join(_e))
            if s["mono"]:
                avail.append("mono:" + ",".join(s["mono"][:3]) + ("+" if len(s["mono"]) > 3 else ""))
            tail = ("   (" + " | ".join(avail) + ")") if avail else ""
            print("  %-5s %s %-34s %s" % (s["id"], _TAG[s["status"]], s["name"], tail))
            if full_leaves:
                for lf in s["leaves"]:
                    print("        %s %s" % (_TAG[lf["status"]], lf["name"]))
    _tally_block()


def _tally_block():
    lt = T.leaf_tally()
    print("\n" + "-" * 86)
    print(" leaf tally:  " + "   ".join("%s=%d" % (g, lt[g]) for g in T.GRADES if lt[g]))
    print(" total leaves: %d   subsections: %d   sections: 14"
          % (sum(lt.values()), sum(1 for _ in T.all_subsections())))
    real = sum(1 for _, _, s in T.all_subsections() if T.explist(s))
    mono = sum(1 for _, _, s in T.all_subsections() if s["mono"])
    print(" subsections with native section code: %d   backed by monolith archive: %d" % (real, mono))
    print(" key: DERIVED/PARTIAL = real; BORROWED = external theorem; CONJECTURE = proposed;")
    print("      OPEN = not started; REFUTED = tested & failed; DEF = infrastructure; EXT = experiment.")


def status():
    print("=" * 86)
    print(" emergence -- grade rollup")
    print("=" * 86)
    sub_t = {}
    for num, name, subs in T.SECTIONS:
        secg = {}
        for s in subs:
            r = _rollup(s)
            sub_t[r] = sub_t.get(r, 0) + 1
            secg[r] = secg.get(r, 0) + 1
        summ = " ".join("%s:%d" % (g, secg[g]) for g in T.GRADES if secg.get(g))
        print("  %-3s %-42s %s" % (num, name, summ))
    print("\n subsection rollup:  " + "   ".join("%s=%d" % (g, sub_t[g]) for g in T.GRADES if sub_t.get(g)))
    _tally_block()


def section(num):
    for n, name, subs in T.SECTIONS:
        if n == str(num):
            print("%s. %s" % (n, name.upper()))
            for s in subs:
                print("\n  %-5s %s %s" % (s["id"], _TAG[s["status"]], s["name"]))
                if T.explist(s):
                    print("        library: %s   (run: python main.py run %s)" % (", ".join(T.explist(s)), s["id"]))
                if s["mono"]:
                    print("        monolith: %s" % ", ".join(s["mono"]))
                for lf in s["leaves"]:
                    print("          %s %s" % (_TAG[lf["status"]], lf["name"]))
            return
    print("no such section: %s" % num)


def run(sub_id):
    s = T.find(sub_id)
    if s is None:
        print("no such subsection: %s" % sub_id); return
    exps = T.explist(s)
    if not exps:
        print("%s %s -- no ported library experiment." % (sub_id, s["name"]))
        print("  status: %s" % s["status"])
        if s["mono"]:
            print("  backed by monolith: %s  (try: python main.py mono %s)" % (", ".join(s["mono"]), s["mono"][0]))
        else:
            print("  this subsection is not yet implemented; its leaves and grades:")
            for lf in s["leaves"]:
                print("    %s %s" % (_TAG[lf["status"]], lf["name"]))
        return
    for i, e in enumerate(exps):
        if i:
            print()
        print("### %s  %s   ->   library %s\n" % (sub_id, s["name"], e))
        importlib.import_module(e).run()


def mono(cmd):
    print("  [archive] running emergence_monolith.py (v7.9). Its INLINE grades predate the v8.1")
    print("  [archive] referee corrections -- e.g. it still calls local confluence a 'theorem via the")
    print("  [archive] Critical Pair Lemma'. The CURRENT honest grade is in tree.py (run: status).\n")
    m = importlib.import_module("emergence_monolith")
    fn = getattr(m, "exp_" + cmd, None)
    if fn is None:
        print("unknown monolith command: %s" % cmd); return
    fn()


def cmap():
    print(" subsection -> implementation map")
    print("-" * 70)
    for _, _, s in T.all_subsections():
        impl = ",".join(T.explist(s)) or "-"
        mn = ",".join(s["mono"]) if s["mono"] else "-"
        print("  %-5s %-34s code:%-26s mono:%s" % (s["id"], s["name"], impl, mn))


if __name__ == "__main__":
    a = sys.argv[1:] or ["tree"]
    cmd = a[0]
    if cmd in ("tree", "manifest"):
        tree()
    elif cmd == "status":
        status()
    elif cmd == "section" and len(a) > 1:
        section(a[1])
    elif cmd == "run" and len(a) > 1:
        run(a[1])
    elif cmd == "mono" and len(a) > 1:
        mono(a[1])
    elif cmd == "map":
        cmap()
    elif cmd == "test":
        import tooling.regression_test as rt
        rt.main()
    else:
        print(__doc__)
