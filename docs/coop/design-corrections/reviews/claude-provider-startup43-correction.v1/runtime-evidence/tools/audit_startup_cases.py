"""Audit every startup- case: record the ACTUAL exchange outcome (phase, trace, refusal text/key, conversion).

usage: audit_startup_cases.py <scratch-candidate-root> <json-out>
"""
import importlib.util
import json
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
native = root / "docs" / "coop" / "design-corrections" / "native"
spec = importlib.util.spec_from_file_location("audit_checker", native / "check_native_evidence.v2.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
model = checker.load_model()
doc = json.loads((native / "native-cases.v2.json").read_text(encoding="utf-8"))
rows = []
for case in doc["cases"]:
    if not case["id"].startswith("startup-"):
        continue
    env = {"fixtures": doc["fixtures"]}
    steps = []
    for step in case["steps"]:
        args = checker.resolve(step.get("args", {}), env)
        record = {"fn": step["fn"], "expectError": step.get("expectError")}
        try:
            result = model.validate_native(args["def"], args["value"]) if step["fn"] == "validate" else getattr(model, step["fn"])(**args)
            if isinstance(result, dict) and "finalPhase" in result:
                conv = result.get("hostConversion") or {}
                record["outcome"] = {"finalPhase": result["finalPhase"], "terminalKind": result.get("terminalKind"),
                                     "trace": result["trace"], "refusal": result.get("refusal"),
                                     "conversion": {"coverageSource": conv.get("coverageSource"), "allAdmitted": conv.get("allAdmitted"),
                                                    "authority": (conv.get("stageAuthority") or {}).get("authority"),
                                                    "d9": (conv.get("termination") or conv.get("stageAuthority") or {}).get("d9")} if conv else None}
            else:
                record["outcome"] = result
        except Exception as exc:  # noqa: BLE001
            result = {"error": str(exc)}
            record["raised"] = str(exc)
        if step.get("bind"):
            env[step["bind"]] = result
        steps.append(record)
    rows.append({"id": case["id"], "kind": case["kind"], "steps": steps})
out.write_text(json.dumps({"cases": len(rows), "rows": rows}, indent=1, default=str) + "\n", encoding="utf-8")
for r in rows:
    s = r["steps"][0]
    o = s.get("outcome")
    if isinstance(o, dict) and "finalPhase" in o:
        ref = o["refusal"]
        print(f"{r['id'][8:80]:72} {o['finalPhase']:6} {(ref or {}).get('key') or ''} {(ref or {}).get('detailHead') or ''} {o['trace'][-1] if o['trace'] else ''}")
    else:
        print(f"{r['id'][8:80]:72} {'raised ' + s['raised'][:90] if 'raised' in s else 'ok'}")
