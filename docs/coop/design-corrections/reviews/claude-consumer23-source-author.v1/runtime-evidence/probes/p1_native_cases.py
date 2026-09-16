"""P1 — run the maintained native-cases.v2.json through check_native_evidence.v2.run_case, writing NOTHING.

argv[1] = frozen36 | assembly. The native checker's main() verifies source pins and always writes
native-evidence-report.v2.json into its own tree; pins are intentionally stale after authoring and root owns
that generated report, so main() is NOT called. This executes exactly its case loop (cases_doc fixtures +
run_case over every case) against that tree's model. It does not re-run the ladder/matrix/digest-law checks.
"""
import importlib.util
import json
import sys
from pathlib import Path

TREES = {
    "frozen36": Path("/tmp/opensip-design-corrections/candidate-subject.v36"),
    "assembly": Path("/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source"),
}
NATIVE = TREES[sys.argv[1]] / "docs/coop/design-corrections/native"
spec = importlib.util.spec_from_file_location("check_native_probe", NATIVE / "check_native_evidence.v2.py")
CHK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CHK)
model = CHK.load_model()
cases_doc = model.C.parse(CHK.CASES_PATH.read_bytes())
fixtures = cases_doc.get("fixtures", {})
results = [CHK.run_case(c, model, fixtures) for c in cases_doc["cases"]]
ids = [r["id"] for r in results]
passed = sum(1 for r in results if r["passed"])
print(json.dumps({
    "tree": sys.argv[1], "casesPath": str(CHK.CASES_PATH), "total": len(results), "passed": passed,
    "failed": [r for r in results if not r["passed"]], "duplicateIds": len(ids) != len(set(ids)),
    "ids": ids,
}, indent=1))
