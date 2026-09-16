"""Development pre-check (not the control of record): run selected native cases through the checker's own
run_case without pin verification, reading the work copy and writing nothing into it.

usage: run_selected_cases.py <candidate-root> <id-prefix> [<id-prefix> ...]
The control of record is the full pinned checker run in a scratch copy.
"""
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prefixes = tuple(sys.argv[2:])
native = root / "docs" / "coop" / "design-corrections" / "native"
spec = importlib.util.spec_from_file_location("selected_checker", native / "check_native_evidence.v2.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
model = checker.load_model()
doc = json.loads((native / "native-cases.v2.json").read_text(encoding="utf-8"))
results = [checker.run_case(c, model, doc["fixtures"]) for c in doc["cases"] if c["id"].startswith(prefixes)]
failed = [r for r in results if not r["passed"]]
for r in failed:
    print("FAIL", r["id"])
    for f in r["faults"]:
        print("   ", f[:900])
print(json.dumps({"selected": len(results), "passed": len(results) - len(failed), "failed": len(failed)}))
