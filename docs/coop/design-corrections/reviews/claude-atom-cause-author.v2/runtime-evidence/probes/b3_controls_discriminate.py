"""Do the v2 controls discriminate? Run every added control against three atom models.

  * v2       — the corrected source as it now stands
  * v1-final — this runtime's BEFORE image (the v1 handoff bytes)
  * frozen33 — the original reference, before v1 and v2

atom_model.v1.py resolves its siblings from `Path(__file__).parent`, so the v1-final image has to
sit inside the foundation directory to be loadable at all. It is written under a temporary name and
removed in a finally block; the custody probe afterwards is the check that nothing was left behind.
AUTHOR/REFERENCE evidence; frozen33 is read only.
"""
import importlib.util
import json
import shutil
from pathlib import Path

NEW = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
           "docs/coop/design-corrections/foundation")
OLD = Path("/tmp/opensip-design-corrections/candidate-subject.v33/"
           "docs/coop/design-corrections/foundation")
V1_IMAGE = Path("/private/tmp/opensip-design-corrections/claude-atom-cause-author.v2/before/"
                "docs__coop__design-corrections__foundation__atom_model.v1.py")
TEMP = NEW / "_baseline_v1_atom_model.tmp.py"

V2_CASES = [
    "test_no_owed_binding_return_is_shared_by_both_endpoints",
    "test_incoming_keeps_both_cross_family_shapes",
    "test_same_family_unavailable_blocks_incoming_only",
    "test_same_kind_multi_scope_selection_is_ascending_coverage_id",
    "test_dep_fold_replaces_whole_records_and_keeps_ties",
]
V1_CASES = [
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
results = []
try:
    shutil.copy2(V1_IMAGE, TEMP)
    models = [("v2", K.AM),
              ("v1-final", load("atom_model_v1_final", TEMP)),
              ("frozen33", load("atom_model_frozen33", OLD / "atom_model.v1.py"))]
    for label, model in models:
        K.AM = model
        for name in V2_CASES + V1_CASES:
            try:
                getattr(K, name)()
                results.append({"model": label, "case": name, "ok": True})
            except Exception as exc:  # noqa: BLE001
                results.append({"model": label, "case": name, "ok": False,
                                "error": f"{type(exc).__name__}: {exc}"[:400]})
finally:
    if TEMP.exists():
        TEMP.unlink()

by_case = {}
for r in results:
    by_case.setdefault(r["case"], {})[r["model"]] = r["ok"]

print(json.dumps({
    "standing": "AUTHOR/REFERENCE control-discrimination evidence over synthetic atom inputs.",
    "tempBaselineRemoved": not TEMP.exists(),
    "results": results,
    "v2Added": V2_CASES,
    "discriminatesV1Final": sorted(c for c, m in by_case.items()
                                   if m.get("v2") and not m.get("v1-final")),
    "discriminatesFrozen33": sorted(c for c, m in by_case.items()
                                    if m.get("v2") and not m.get("frozen33")),
    "passesAllThree": sorted(c for c, m in by_case.items() if all(m.values())),
}, indent=2, default=str))
