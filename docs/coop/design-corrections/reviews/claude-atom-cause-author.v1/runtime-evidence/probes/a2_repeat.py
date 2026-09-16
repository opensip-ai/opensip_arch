"""Repeat the surfacing probe across processes; also replay a REAL fixture Run N times."""
import collections
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20

rows = []
for _ in range(N):
    p = subprocess.run([PY, "-I", "-B", str(HERE / "a2_surfacing.py")],
                       capture_output=True, text=True)
    rows.append(json.loads(p.stdout) if p.returncode == 0 else {"error": p.stderr[-500:]})

ok = [r for r in rows if "error" not in r]
ncs = [str(r.get("coverageUnknownNativeCause")) for r in ok]
codes = [tuple(r.get("causeCodes") or []) for r in ok]

# Real fixture Run: does the currently shipped fixture corpus trigger it?
real = subprocess.run([PY, "-I", "-B", str(HERE / "a2_realrun.py"), str(min(N, 8))],
                      capture_output=True, text=True)
print(json.dumps({
    "standing": "AUTHOR/REFERENCE evidence. Separate processes, fresh hash seed each. No consumer "
                "input, no consumer expected output.",
    "controlledCase": {
        "runs": len(ok),
        "errors": [r for r in rows if "error" in r][:1],
        "coverageUnknownNativeCauseTally": dict(collections.Counter(ncs)),
        "causeCodeSetTally": {str(k): v for k, v in collections.Counter(codes).items()},
        "SURFACES_AS_DIFFERING_PROOF_CAUSE": len(set(ncs)) > 1,
        "sample": ok[0] if ok else None,
    },
    "realFixtureRun": json.loads(real.stdout) if real.returncode == 0 else
                      {"exit": real.returncode, "stderrTail": real.stderr[-1500:]},
}, indent=2, default=str))
