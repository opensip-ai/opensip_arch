"""Are the new controls discriminating? Run them against the UNCORRECTED frozen33 atom model.

Loads the corrected checker, then rebinds its `AM` to frozen33's atom_model.v1.py (read-only) and
runs only the six new cases. A control that passes against both models would not be evidence.
AUTHOR/REFERENCE evidence; frozen33 is never written.
"""
import importlib.util
import json
from pathlib import Path

NEW = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
           "docs/coop/design-corrections/foundation")
OLD = Path("/tmp/opensip-design-corrections/candidate-subject.v33/"
           "docs/coop/design-corrections/foundation")

NEW_CASES = [
    "test_outgoing_early_stop_cause_and_universe",
    "test_unmatched_scope_stop_cites_every_scope_and_no_coverage",
    "test_known_hit_dominates_every_outgoing_early_stop",
    "test_cross_family_disclosure_survives_outgoing_selector_stop",
    "test_dep_fold_carrier_is_first_partition_in_selection_order",
    "test_incoming_reports_every_universe_without_early_stop",
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_v1", NEW / "check-atoms.v1.py")
OLD_AM = load("atom_model_frozen33", OLD / "atom_model.v1.py")

out = {
    "standing": "AUTHOR/REFERENCE control-discrimination evidence.",
    "correctedModel": str(NEW / "atom_model.v1.py"),
    "uncorrectedModel": str(OLD / "atom_model.v1.py"),
    "results": [],
}
for model_label, model in (("corrected", K.AM), ("frozen33-uncorrected", OLD_AM)):
    K.AM = model
    for name in NEW_CASES:
        try:
            getattr(K, name)()
            out["results"].append({"model": model_label, "case": name, "ok": True})
        except Exception as exc:  # noqa: BLE001
            out["results"].append({"model": model_label, "case": name, "ok": False,
                                   "error": f"{type(exc).__name__}: {exc}"})

by_case = {}
for r in out["results"]:
    by_case.setdefault(r["case"], {})[r["model"]] = r["ok"]
out["discriminating"] = sorted(c for c, m in by_case.items()
                               if m.get("corrected") and not m.get("frozen33-uncorrected"))
out["passesBothModels"] = sorted(c for c, m in by_case.items()
                                 if m.get("corrected") and m.get("frozen33-uncorrected"))
print(json.dumps(out, indent=2, default=str))
