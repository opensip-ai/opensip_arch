"""Stage distinct synthetic companions and exact runtime digest metadata only.
No worktree or repository edits; complete review/testing still required.
"""
from pathlib import Path
import json,hashlib,shutil
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';assert not S.exists()
P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
old='81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712';new='7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132'
rows=[]
def pin(path):
 raw=path.read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def stage(source,rel,prior):
 target=S/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 assert not (W/rel).exists();assert (W/prior).read_bytes()==(P/prior).read_bytes()
 rows.append(dict(path=rel,candidate=pin(target),priorPath=prior,prior=pin(P/prior)))
stage(B/'replay-fixtures.native-owner-r1.json','crates/host/tests/fixtures/replay-fixtures.native-owner-r1.json','crates/host/tests/fixtures/replay-fixtures.current.json')
for path in sorted((B/'pooled-candidates-r1').glob('*-fixtures.native-owner-r1.json')):
 stage(path,'crates/host/tests/fixtures/'+path.name,'crates/host/tests/fixtures/'+path.name.replace('.native-owner-r1.json','.current.json'))
stage(B/'native-context-candidate/native-context-fixtures.native-owner-r1.json','crates/host/tests/fixtures/native-context-fixtures.native-owner-r1.json','crates/host/tests/fixtures/native-context-fixtures.current.json')
stage(B/'cycle-representative.native-owner-r1.v1.json','crates/evaluator/tests/fixtures/cycle-representative.native-owner-r1.v1.json','crates/evaluator/tests/fixtures/cycle-representative.current.v1.json')
metadata=[]
for name in ['coverage-registry','import-payload-registry']:
 prior='crates/evaluator/src/'+name+'.current.json';rel='crates/evaluator/src/'+name+'.native-owner-r1.json';before=(P/prior).read_text();count=before.count(old);assert count>0
 after=before.replace(old,new);target=S/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(after)
 assert not (W/rel).exists() and (W/prior).read_bytes()==(P/prior).read_bytes();assert after.replace(new,old)==before
 rows.append(dict(path=rel,candidate=pin(target),priorPath=prior,prior=pin(P/prior)));metadata.append(dict(path=rel,changedCurrentNativeDigests=count,allOtherRawBytesEqual=True,noRowsDomainsSelectorsOwnersAdded=True))
replay=json.loads((S/'crates/host/tests/fixtures/replay-fixtures.native-owner-r1.json').read_text());oldjournal=json.loads((P/'crates/security/tests/fixtures/journal-seal-replay.current.json').read_text());label=oldjournal['case']['label'];case=next(c for c in replay['cases'] if c['label']==label);assert case['expected']['value']['result']=='ADMIT'
fixture=dict(case=case,objectPool={k:replay['objectPool'][k] for k in case['objects']},blobPool={k:replay['blobPool'][k] for k in case['blobs']})
target=S/'crates/security/tests/fixtures/journal-seal-replay.native-owner-r1.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(fixture,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
prior='crates/security/tests/fixtures/journal-seal-replay.current.json';assert not (W/target.relative_to(S)).exists();rows.append(dict(path=str(target.relative_to(S)),candidate=pin(target),priorPath=prior,prior=pin(P/prior)))
assert len(rows)==15
for row in rows:assert row['candidate']['bytes']<=4*1024*1024
report=dict(standing='PUBLIC SYNTHETIC COMPANION PROPOSAL; NO WORKTREE WRITES OR RUNTIME/CORRESPONDENCE ACCEPTANCE',newFiles=rows,runtimeDigestMetadata=metadata,
 journalExactNewHostSubset=True,journalObjects=len(case['objects']),journalBlobs=len(case['blobs']),allOriginalHistoricalAndCurrentCompanionsUnchanged=True,parserLimitUnchanged=True,sourceGuardUnchanged=True,
 expectedVerdictsNotRewritten=True,remaining=['Independent full correspondence and canonical expected-identity/debug/order checks','Explicit owning include changes only after complete staged construction; full focused and owning verification','Independent complete unit review and root assent','Own additive inventory successor after accepted code presence; mandatory immediate reviewed blind refresh before census-dependent consumption'],testsPassed=False,unitAccepted=False,productQualification=False)
(B/'staged-companions.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(files=len(rows),metadata=metadata,journalObjects=len(case['objects']),journalBlobs=len(case['blobs'])),indent=2))
