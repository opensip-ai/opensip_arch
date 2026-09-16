"""Q1 — which existing check-atoms cases reach the `_select_dep_coverages` mapped fallback?

argv[1] = frozen35 | successor: selects which tree's check-atoms.v1.py AND atom_model.v1.py run.
The selector is wrapped, not changed: before delegating, it records whether the call takes the
same-kind branch with covs non-empty and NO exact dependency scope (the fallback precondition), and
what the fallback returned. STANDING: instrumentation of synthetic reference checks only.
"""
import importlib.util
import json
import sys
from pathlib import Path

TREES = {
    "frozen35": Path("/tmp/opensip-design-corrections/candidate-subject.v35"),
    "successor": Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source"),
}
F = TREES[sys.argv[1]] / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_q1", F / "check-atoms.v1.py")
AM = K.AM
original = AM._select_dep_coverages
hits = []
current = {"case": None}


def wrapped(drel, drung, source_u, want_t, inputs, current_subjects, current_kind):
    out = original(drel, drung, source_u, want_t, inputs, current_subjects, current_kind)
    covs = AM._coverages_exact(inputs, drel, drung, source_u, want_t)
    same_kind = not (current_subjects is None or (current_kind and AM._source_kind_for_relation(drel) != current_kind))
    if covs and same_kind and not AM._scopes_exact(inputs, drel, drung, source_u):
        hits.append({"case": current["case"], "relation": drel, "rung": drung,
                     "fallbackReturned": [cid for cid, _ in out]})
    return out


AM._select_dep_coverages = wrapped
results = []
for fn in K.CASES:
    current["case"] = fn.__name__
    try:
        fn()
        results.append({"case": fn.__name__, "ok": True})
    except Exception as exc:  # noqa: BLE001
        results.append({"case": fn.__name__, "ok": False, "error": f"{type(exc).__name__}: {exc}"[:300]})

print(json.dumps({
    "tree": sys.argv[1],
    "cases": len(results), "passed": sum(r["ok"] for r in results),
    "failed": [r for r in results if not r["ok"]],
    "fallbackPreconditionHits": hits,
    "casesReachingFallback": sorted({h["case"] for h in hits}),
    "casesWhereFallbackSuppliedCoverage": sorted({h["case"] for h in hits if h["fallbackReturned"]}),
}, indent=1))
