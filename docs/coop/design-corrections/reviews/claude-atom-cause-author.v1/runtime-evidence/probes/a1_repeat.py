"""Run the order-trigger probe in N separate processes and report whether the fold varies."""
import collections
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 16

rows = []
for i in range(N):
    p = subprocess.run([PY, "-I", "-B", str(HERE / "a1_order_trigger.py")],
                       capture_output=True, text=True)
    if p.returncode != 0:
        rows.append({"run": i, "error": p.stderr[-600:]})
        continue
    rows.append(json.loads(p.stdout))

folds = [r.get("directFold", {}) for r in rows if "directFold" in r]
orders = [tuple(f.get("covsOrder") or []) for f in folds]
defs = [f.get("foldedDeficiency") for f in folds]
ncs = [f.get("foldedNativeCause") for f in folds]
atom_nc = [r.get("coverageUnknownNativeCause") for r in rows if "coverageUnknownNativeCause" in r]

print(json.dumps({
    "standing": "AUTHOR/REFERENCE evidence. Separate processes; -I ignores PYTHONHASHSEED so each "
                "process gets a fresh hash seed. No consumer input used.",
    "runs": len(rows),
    "errors": [r for r in rows if "error" in r][:2],
    "distinctCoverageDictOrders": len({tuple(r.get("coverageDictOrder") or []) for r in rows}),
    "distinctHelperDepOrders": len(set(orders)),
    "helperDepOrderTally": {str(k): v for k, v in collections.Counter(orders).items()},
    "distinctFoldedDeficiencies": sorted(set(defs)),
    "foldedDeficiencyTally": dict(collections.Counter(defs)),
    "distinctFoldedNativeCauses": sorted(set(map(str, ncs))),
    "foldedNativeCauseTally": dict(collections.Counter(map(str, ncs))),
    "atomCoverageUnknownNativeCauseTally": dict(collections.Counter(map(str, atom_nc))),
    "atomValueTally": dict(collections.Counter(r.get("value") for r in rows if "value" in r)),
    "FOLD_IS_NONDETERMINISTIC": len(set(defs)) > 1 or len(set(map(str, ncs))) > 1,
    "sampleRun": rows[0] if rows else None,
}, indent=2, default=str))
