"""Maintained native cases (native-cases.v2.json) through check_native_evidence.v2.run_case, without main().

main() verifies source pins and writes its report into the native directory; this runner does neither.
Usage: native_cases.py ROOT. Stdout only.
"""
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "docs/coop/design-corrections/native"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


chk = load("nc_native_checker", root / "check_native_evidence.v2.py")
model = load("nc_native_model", root / "native_evidence_model.v2.py")
cases = json.loads((root / "native-cases.v2.json").read_text())
results = [chk.run_case(c, model, cases.get("fixtures", {})) for c in cases["cases"]]
failed = [{"id": r["id"], "faults": r.get("faults", [])[:4]} for r in results if not r["passed"]]
print(json.dumps({"total": len(results), "passed": len(results) - len(failed), "failed": failed}, indent=1))
raise SystemExit(1 if failed else 0)
