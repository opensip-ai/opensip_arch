"""Stage 1: introspect maintained synthetic worlds. No mutation; admission standing only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_common as P  # noqa: E402

CONFIGS = {
    "default": {},
    "unsupported-required": {"unsupported_cell": "required"},
    "unsupported-optional": {"unsupported_cell": "optional"},
    "multiple-universes": {"multiple_universes": True},
    "symbol-rows": {"symbol_rows": [{"nativeSubjectId": "x"}]},
    "symbol-only-second-program": {"multiple_universes": True, "symbol_rows": [{"nativeSubjectId": "x"}],
                                   "symbol_only_second_program": True},
    "optional-unselected": {"optional_unselected_cell": True},
}

out = {"standing": "admission (reference self-consistency); no closed Run in this stage", "worlds": {}}
for name, kwargs in CONFIGS.items():
    try:
        kw = P.K.manifest_from_owner(P.F.build_file_inputs(**kwargs))
    except Exception as exc:  # noqa: BLE001
        out["worlds"][name] = {"kwargs": kwargs, "buildError": type(exc).__name__ + ":" + str(exc)}
        continue
    out["worlds"][name] = {"kwargs": kwargs, "describe": P.describe(kw), "admission": P.admit_summary(kw)}
digest = P.write_json("receipts/stage1-introspect.json", out)
for name, w in out["worlds"].items():
    print("==", name, w.get("buildError") or (w["admission"]["result"], w["admission"]["refusals"]))
    if "describe" in w:
        for c in w["describe"]["cells"]:
            print("  cell", c["cell"], c["capabilityId"], c["languageMode"], c["matrixState"], c["matrixRelations"],
                  "U", c["universe"], c["enumerator"], c["rowState"], "views", c["viewDigests"])
        for v in w["describe"]["views"]:
            print("  view", v["view"], "prod", v["producer"], v["scopes"], "cov", v["coverageCount"],
                  "facts", v["factCount"], "receipt", v["inReceipt"], "selected", v["inSelected"])
print("receipt sha256", digest)
