"""P3 — do the two NEW maintained native cases discriminate? Run them with the ASSEMBLY case file and runner,
once under the assembly native model and once under the frozen36 native model. Writes nothing into any tree.
STANDING: direct native helper evidence only (no Coverage admission, no Run).
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOTS = {
    "assembly": Path("/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source/docs/coop/design-corrections/native"),
    "frozen36": Path("/tmp/opensip-design-corrections/candidate-subject.v36/docs/coop/design-corrections/native"),
}
NEW = ("native-deficiency-whole-run-route-is-total-and-d9-owned", "run-termination-code-is-the-primary-deficiency-route")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


chk = load("check_native_assembly", ROOTS["assembly"] / "check_native_evidence.v2.py")
cases_doc = json.loads((ROOTS["assembly"] / "native-cases.v2.json").read_text())
selected = [c for c in cases_doc["cases"] if c["id"] in NEW]
out = {"selected": [c["id"] for c in selected]}
for label, root in ROOTS.items():
    model = load("native_model_p3_" + label, root / "native_evidence_model.v2.py")
    out[label] = [chk.run_case(c, model, cases_doc.get("fixtures", {})) for c in selected]
out["discriminating"] = [r["id"] for r, f in zip(out["assembly"], out["frozen36"]) if r["passed"] and not f["passed"]]
print(json.dumps(out, indent=1))
