"""P2 — old36 versus new behaviour, and whether the new controls discriminate. Writes nothing into any tree.

(a) QUERY: the ASSEMBLY checker's control functions, run once with its own query model and once with the
    frozen36 query model rebound as `Q`. Controls that fail only under frozen36 discriminate the helper change;
    public-wrapper controls that pass under both pin behaviour frozen36 already had and the prose now states.
(b) NATIVE: `run_termination` over the same stage/entry matrix under the frozen36 and assembly native models.
STANDING: reference helper and public-wrapper controls over the retained semantic fixture; no product claim.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOTS = {
    "frozen36": Path("/tmp/opensip-design-corrections/candidate-subject.v36/docs/coop/design-corrections"),
    "assembly": Path("/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source/docs/coop/design-corrections"),
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


out = {"query": {}, "native": {}}
for label in ("assembly", "frozen36"):
    chk = load("query_checker_" + label, ROOTS["assembly"] / "workflows" / "check-query-projection.v3.py")
    chk.Q = load("query_model_" + label, ROOTS[label] / "workflows" / "query_projection_model.v3.py")
    chk.CHECKS.clear()
    for fn in (chk.schema_controls, chk.table_controls, chk.algorithm_controls, chk.owner_controls, chk.hook_control):
        fn()
    out["query"][label] = {c["id"]: c["ok"] for c in chk.CHECKS}
a, f = out["query"]["assembly"], out["query"]["frozen36"]
out["queryDiscrimination"] = {
    "assemblyCount": len(a), "assemblyFailed": sorted(k for k, v in a.items() if not v),
    "failOnlyUnderFrozen36Model": sorted(k for k in a if a[k] and not f.get(k, False)),
}

STAGES = ("complete", "budget-exhausted", "unavailable")
ENTRY_SETS = {
    "none-deficient": [{"relation": "references", "deficiency": None, "nativeCause": None}],
    "budget-exhausted": [{"relation": "references", "deficiency": "budget-exhausted", "nativeCause": None}],
    "language-tier-unsupported": [{"relation": "declares", "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"}],
    "confidence-floor-unmet": [{"relation": "clones", "deficiency": "confidence-floor-unmet", "nativeCause": None}],
    "required-relation-missing": [{"relation": "references", "deficiency": "required-relation-missing", "nativeCause": None}],
    "provider-unavailable": [{"relation": "references", "deficiency": "provider-unavailable", "nativeCause": "capability-missing"}],
    "input-closure-incomplete": [{"relation": "references", "deficiency": "input-closure-incomplete", "nativeCause": "lockfile-missing"}],
    "resolution-incomplete+budget-exhausted": [{"relation": "references", "deficiency": "resolution-incomplete", "nativeCause": None},
                                               {"relation": "types", "deficiency": "budget-exhausted", "nativeCause": None}],
}
for label, root in ROOTS.items():
    N = load("native_model_" + label, root / "native" / "native_evidence_model.v2.py")
    rows = {}
    for stage in STAGES:
        st = N.stage_authority(stage)
        for name, entries in ENTRY_SETS.items():
            t = N.run_termination(st, entries)
            rows[f"{stage}/{name}"] = {"code": t["d9"]["code"], "class": t["d9"]["class"], "exit": t["d9"]["exitCode"],
                                       "typedDetail": t["typedDetail"] and {k: t["typedDetail"][k] for k in ("deficiency", "nativeCauses")}}
    out["native"][label] = rows
out["nativeChanged"] = {k: {"frozen36": out["native"]["frozen36"][k], "assembly": v}
                        for k, v in out["native"]["assembly"].items() if v != out["native"]["frozen36"][k]}
print(json.dumps(out, indent=1, default=str))
