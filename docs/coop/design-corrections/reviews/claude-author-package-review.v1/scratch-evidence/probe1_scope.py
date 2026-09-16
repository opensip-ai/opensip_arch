
import base64,hashlib,importlib.util,json,re,sys
from pathlib import Path
SRC=Path('/tmp/opensip-design-corrections/candidate-subject.v25')
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
CHK=PKG/'check-export.v4.py'
spec=importlib.util.spec_from_file_location('chk',CHK);CK=importlib.util.module_from_spec(spec);spec.loader.exec_module(CK)
mp=SRC/'docs/coop/design-corrections/foundation/identity-model.v3.py'
spec=importlib.util.spec_from_file_location('owner',mp);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
store=sys.argv[1]; runid=sys.argv[2]
raw=(PKG/store).read_bytes()
objects,blobs=CK.decode_store(raw,M,[])
domain,run=objects[runid]
print('run domain',domain)
rid,owner=M.open_run_closure(run,objects,blobs)
print('open_run_closure ->',rid)
rm=importlib.util.spec_from_file_location('rep',SRC/'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py')
R=importlib.util.module_from_spec(rm);rm.loader.exec_module(R)
out=R.replay(run,objects,blobs)
print('replay result:',json.dumps({k:v for k,v in out.items()},indent=1)[:800])
seal=objects[run['evaluationSealId']][1];proof=objects[seal['proofBundleId']][1]
pps=proof['predicateProofs']
print('predicateProof count',len(pps))
from collections import Counter
sig=Counter()
for pp in pps:
    sig[(pp['ruleId'],pp['predicateId'],tuple(pp['scopeIds']))]+=1
print('distinct scopeId tuples:',len({tuple(pp['scopeIds']) for pp in pps}))
for t in sorted({tuple(pp['scopeIds']) for pp in pps},key=len):
    print('  scopeset size',len(t),[x[:18] for x in t])
for pp in pps[:12]:
    print(' ',pp['ruleId'],pp['predicateId'],pp['operation'],'scopes',len(pp['scopeIds']),'refs',len(pp['inputRefs']),'value',pp['value'])
print('verdict',proof['verdict'])
print('executionDeficiencies count',len(proof['executionDeficiencies']))
for d in proof['executionDeficiencies']:
    print('  execdef',d['cause'],'refs',[(r['domain'],r['digest'][:12]) for r in d['inputRefs']],'nativeCause',d['nativeCause'],'universe',(d['universe'] or '')[:20])
