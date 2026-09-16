"""Audit every provider-wire case: record the ACTUAL refusal text of each step, not just pass/fail.

usage: audit_wire_cases.py <scratch-candidate-root> <json-out>

A negative case passes in the checker when its expectError substring occurs in the refusal text. This
audit re-runs each provider-wire step with the checker's own resolver and records the full refusal, so a
reviewer can see that each negative is refused for the stated reason and not by an earlier accident.
"""
import importlib.util
import json
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
native = root / "docs" / "coop" / "design-corrections" / "native"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load("audit_checker", native / "check_native_evidence.v2.py")
model = checker.load_model()
doc = json.loads((native / "native-cases.v2.json").read_text(encoding="utf-8"))
rows = []
for case in doc["cases"]:
    if not case["id"].startswith("provider-wire-"):
        continue
    env = {"fixtures": doc["fixtures"]}
    steps = []
    for step in case["steps"]:
        args = checker.resolve(step.get("args", {}), env)
        record = {"fn": step["fn"], "expectError": step.get("expectError")}
        try:
            if step["fn"] == "domainSha256Hex":
                import hashlib
                result = "sha256:" + hashlib.sha256(args["domain"].encode("utf-8") + b"\0" + bytes.fromhex(args["hex"])).hexdigest()
            else:
                result = getattr(model, step["fn"])(**args)
            record["result"] = {k: result[k] for k in ("outcome", "payload", "batchCommitment", "targetAttributionNegotiated")
                                if isinstance(result, dict) and k in result} if isinstance(result, dict) else result
            record["refused"] = False
        except Exception as exc:  # noqa: BLE001
            result = {"error": str(exc)}
            record["refused"] = True
            record["refusal"] = str(exc)
            record["matchesExpectation"] = bool(step.get("expectError")) and step["expectError"] in str(exc)
        if step.get("bind"):
            env[step["bind"]] = result
        steps.append(record)
    rows.append({"id": case["id"], "kind": case["kind"], "steps": steps})
out.write_text(json.dumps({"cases": len(rows), "rows": rows}, indent=1) + "\n", encoding="utf-8")
for r in rows:
    for s in r["steps"]:
        print(f"{r['id'][14:78]:64} {s['fn'][:26]:26} {'REFUSED ' + s['refusal'][:110] if s['refused'] else 'ok'}")
