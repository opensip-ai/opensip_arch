"""Re-sample both nondeterminism probes AFTER the reference ordering correction."""
import collections
import json
import subprocess
from pathlib import Path

PY = "/tmp/opensip-architecture-review-env/bin/python"
H = Path(__file__).resolve().parent
out = {"standing": "AUTHOR/REFERENCE evidence, after the ascending-id ordering correction."}

for name, script in (("fold", "a1_order_trigger.py"), ("surface", "a2_surfacing.py")):
    rows = []
    for _ in range(20):
        p = subprocess.run([PY, "-I", "-B", str(H / script)], capture_output=True, text=True)
        rows.append(json.loads(p.stdout) if p.returncode == 0 else {"error": p.stderr[-300:]})
    ok = [r for r in rows if "error" not in r]
    if name == "fold":
        out["fold"] = {
            "runs": len(ok),
            "distinctDictOrders": len({tuple(r["coverageDictOrder"]) for r in ok}),
            "distinctHelperOrders": len({tuple(r["directFold"]["covsOrder"]) for r in ok}),
            "helperOrders": sorted({tuple(r["directFold"]["covsOrder"]) for r in ok}),
            "deficiencyTally": dict(collections.Counter(
                r["directFold"]["foldedDeficiency"] for r in ok)),
            "nativeCauseTally": dict(collections.Counter(
                str(r["directFold"]["foldedNativeCause"]) for r in ok)),
            "DETERMINISTIC": len({(r["directFold"]["foldedDeficiency"],
                                   str(r["directFold"]["foldedNativeCause"])) for r in ok}) == 1,
        }
    else:
        out["surface"] = {
            "runs": len(ok),
            "distinctDictOrders": len({tuple(r["coverageDictOrder"]) for r in ok}),
            "nativeCauseTally": dict(collections.Counter(
                str(r["coverageUnknownNativeCause"]) for r in ok)),
            "valueTally": dict(collections.Counter(r["value"] for r in ok)),
            "DETERMINISTIC": len({str(r["coverageUnknownNativeCause"]) for r in ok}) == 1,
        }
print(json.dumps(out, indent=2, default=str))
