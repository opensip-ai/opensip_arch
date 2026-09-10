from pathlib import Path
import importlib.util,json,hashlib
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('parser',B/'check-blind12-exported-graphs.v1.py');M=load('identity',F/'identity-model.v3.py')
p=B/'consumer-b.v12-team-other-runs-corrections.v6/output/runs/ts.store.json';raw=p.read_bytes();objects,blobs=P.decode_store(raw,M)
rid='run3:26dd437679e894c1cf01d5fb4b94de66bc15cc4ce8c8aaf26b3864144bc60164';run=objects[rid][1]
opened,owner=M.open_run_closure(run,objects,blobs);assert opened==rid
rows=[]
for iid in owner['plan']['importIds']:
 imp=objects[iid][1]
 for field in ('producerClosure','adapterClosure'):
  expected=M.SCHEMA['x-opensip-digest-domains']['closureKinds']['byField']['import.'+field]
  cid=imp[field];actual=objects[cid][1]['kind'];rows.append({'importId':iid,'field':field,'closureId':cid,'requiredKind':expected,'actualKind':actual,'matches':actual==expected})
r={'standing':'Root reproduces an actual reference-enforcement omission against published existing law using exact consumer bytes. Not full Run admission or product qualification. This root-reference result is not blind-team input.','exportSha256':hashlib.sha256(raw).hexdigest(),'runId':rid,'rootStructuralChecker':'ADMIT','normativeSelector':'identity-schemas.v3.json#/x-opensip-digest-domains/closureKinds/byField','sourceSha256':hashlib.sha256((F/'identity-model.v3.py').read_bytes()).hexdigest(),'observations':rows,'existingLawEnforcementGap':any(not x['matches'] for x in rows),'fullReplayStanding':'Previously refuses enumeration before complete proof; this report does not accept later semantic work.'}
(Path(__file__).parent/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
