"""Replay the retained reference-fixture Run N times in separate processes, after the v2 edits.

This is the RETAINED REAL FIXTURE path — seal_fixture -> open_run_closure -> derive -> seal_derived
-> replay -> close_run — not a synthetic atom input. It is reported separately from any randomized
process sampling of synthetic inputs, and it covers one fixture, not the retained corpus.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"
F = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
         "docs/coop/design-corrections/foundation")

WORKER = r'''
import hashlib, importlib.util, json
from pathlib import Path
F = Path(r"%s")
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=load("g","%s"); R=load("r","%s"); S=load("s","%s"); M=R.M
g=G.build_file_inputs()
seed,objects,blobs,_=G.seal_fixture(g)
_,owner=M.open_run_closure(seed,objects,blobs)
i=g["inputs"]
out=R.derive(i["planId"],i["executionPlanId"],i["evaluatorClosure"],i["evaluationInputRefs"],objects,blobs,owner)
run,objects,blobs=S.seal_derived(g,out,objects,blobs)
res=R.replay(run,objects,blobs)
rid=M.close_run(run,objects,blobs)
proof=out["proof"]
print(json.dumps({
  "runId":res["runId"],"closeRunId":rid,"verdict":res["verdict"],
  "proofBundleId":out["proofBundleId"],
  "proofSha256":hashlib.sha256(M.C.canonical(proof)).hexdigest(),
  "findingCount":len(proof["findingIds"]),
  "predicateCount":len(proof["predicateProofs"]),
}))
''' % (F, F / "evaluator_graph_fixture.v3.py", F / "evaluator_replay_model.v3.py",
       F / "evaluator_semantic_fixture.v3.py")

wp = HERE / "b4_realrun_worker.py"
wp.write_text(WORKER)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
rows = []
for _ in range(N):
    p = subprocess.run([PY, "-I", "-B", str(wp)], capture_output=True, text=True)
    rows.append(json.loads(p.stdout) if p.returncode == 0
                else {"error": p.stderr.strip().splitlines()[-1][:300] if p.stderr else "?"})

ok = [r for r in rows if "error" not in r]
print(json.dumps({
    "standing": "Retained reference FIXTURE Run, replayed end to end. One fixture, not the "
                "retained corpus. Distinct from synthetic-input process sampling.",
    "atomModelSha256": hashlib.sha256((F / "atom_model.v1.py").read_bytes()).hexdigest(),
    "runs": len(rows), "ok": len(ok),
    "errors": [r for r in rows if "error" in r][:2],
    "distinctProofSha256": sorted({r["proofSha256"] for r in ok}),
    "distinctRunIds": sorted({r["runId"] for r in ok}),
    "stableAcrossProcesses": len({r["proofSha256"] for r in ok}) <= 1,
    "sample": ok[0] if ok else None,
}, indent=2, default=str))
