"""Scope of the in-memory owner pattern successor: which canonical modules are patched, and what the patch does to
EVERY pattern in all pinned JSON schema documents (unsupported constructs, Python-vs-ECMA result changes), including
documents outside the successor's declared parents. ASCII-only source; non-ASCII corpus built with chr()."""
import sys, os, json, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); COPY = os.path.join(HERE, "copy")
sys.pycache_prefix = os.path.join(HERE, "tmp", "pycache")
sys.path.insert(0, os.path.join(COPY, "tools"))
import common as CM, wirecodec as W, owner_successor as OS

arch = CM.arch_root()
succ = json.load(open(os.path.join(COPY, "owner-pattern-successor.v1.json")))
mods = OS.load_models(arch, succ, "rv_")
out = {}
out["patchedCanonicalModules"] = [[k, C.__name__, getattr(C, "__file__", ""), id(C), bool(getattr(C, OS.MARK, False))]
                                  for k, m in mods.items() for C in OS._canonical_modules(m)]
out["sysModulesCanonicalLike"] = [[n, id(m), bool(getattr(m, OS.MARK, False))] for n, m in sys.modules.items() if "canonical" in n.lower()]
NE = mods["NE"]
out["nativeModelModuleRefs"] = sorted(k for k, v in vars(NE).items() if type(v).__name__ == "module")
parents = {p["key"] for p in succ["parents"]}
LF, CR, LS, NEL, BOM = "\n", "\r", chr(0x2028), chr(0x85), chr(0xFEFF)
corpus = ["", "a", "a/b", "a" + LF, LF, "a" + LF + "b", "x" + LF + "/../y", "a/.." + LF, ".." + LF, "a" + CR + "/./b", "a" + LS + "/..",
          NEL, "a" + NEL, BOM, " a", "a ", "0" * 64 + LF, "sha256:" + "0" * 64 + LF, "A", "abc-DEF_1.2", "a.b", "a:b", chr(0xE9),
          "e" + chr(0x301), chr(0x1F600), "\t", "a\tb", "x" * 300, "1.0.0", "1.0.0" + LF, "/a", "a/", "a//b", "./a", "a/.", "C:x", "a\\b", "a" + chr(0) + "b"]
per = {}
for key, (path, sha, size) in CM.ARCH_PINS.items():
    if not path.endswith(".json"):
        continue
    d = json.load(open(os.path.join(arch, path)))
    pats = []

    def w(o, p):
        if isinstance(o, dict):
            for kk, v in o.items():
                if kk == "pattern" and isinstance(v, str):
                    pats.append((p, v))
                w(v, p + "/" + kk)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                w(v, p + "/" + str(i))
    w(d, "#")
    if not pats:
        continue
    unsupported, changed = [], []
    for p, v in pats:
        try:
            for s in corpus:
                e = W.ecma_test(v, "u", s)
                py = re.search(v, s) is not None
                if e != py:
                    changed.append([p, v, s])
                    break
        except Exception as ex:  # noqa: BLE001
            unsupported.append([p, v, type(ex).__name__ + ":" + str(ex)[:60]])
    per[key] = {"inSuccessorParents": key in parents, "patterns": len(pats), "unsupportedByTranslation": len(unsupported),
                "unsupportedExamples": unsupported[:4], "pythonVsEcmaChangedOnCorpus": len(changed), "changedExamples": changed[:6]}
out["perDocument"] = per
json.dump(out, open(os.path.join(HERE, "probe_dialect_scope.out.json"), "w"), indent=1, ensure_ascii=True)
print(json.dumps(out, indent=1, ensure_ascii=True)[:9000])
