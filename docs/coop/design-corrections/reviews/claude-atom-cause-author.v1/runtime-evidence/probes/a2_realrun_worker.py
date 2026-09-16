
import hashlib, importlib.util, json
from pathlib import Path
F = Path(r"/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation")
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=load("g","/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py"); R=load("r","/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py"); S=load("s","/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py"); M=R.M
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
