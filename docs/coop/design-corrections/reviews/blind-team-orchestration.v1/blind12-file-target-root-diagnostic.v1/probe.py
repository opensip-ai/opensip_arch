from pathlib import Path
import json,importlib.util,hashlib
from jsonschema import Draft202012Validator
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('parser',B/'check-blind12-exported-graphs.v1.py');M=load('identity',F/'identity-model.v3.py');A=load('atom',F/'atom_model.v1.py')
raw=(B/'consumer-b.v12-team-other-runs-corrections.v6/output/runs/ts.store.json').read_bytes();objects,blobs=P.decode_store(raw,M)
fid='fact2:dd591620d4edbfb9441534cf910e9192bcb93ae571a19269db2773c356092cd9';fact=objects[fid][1];payload=M.C.parse(blobs[fact['payloadDigest']]);native_path='src/index.ts'
rows=[]
for digest,blob in blobs.items():
 try:d=M.C.parse(blob)
 except Exception:continue
 if isinstance(d,dict) and 'cellOrdinal' in d and d.get('kind')=='file':
  rows += [{'inventoryDigest':digest,'row':r} for r in d.get('rows',[]) if r['nativeSubjectId']==native_path]
assert rows
schema=json.loads((F.parent/'native/relation-payload-schemas.v2.json').read_text()) if (F.parent/'native/relation-payload-schemas.v2.json').exists() else None
if schema is None:
 paths=list((B/'candidate-subject.v24').rglob('relation-payload-schemas.v2.json'));paths=[p for p in paths if '/reviews/' not in str(p)];assert len(paths)==1;schema=json.loads(paths[0].read_text())
v=Draft202012Validator(schema['$defs']['SubjectIdV1'])
subject={'universe':fact['targetUniverse'],'kind':'file','nativeSubjectId':native_path}
actual=A._native_occupancy({**fact,'payload':payload},subject,{'targetNativeIdField':'resolvedTarget'},{'endpoint':'target'}, {})
r={'standing':'Bounded root diagnostic on an owner-structurally-admitted but full-enumeration-refused TS graph. Direct occupancy function only; no atom/full Run acceptance, no proven final false absence. No input remint, namespace parsing or blind actor feedback.','exportSha256':hashlib.sha256(raw).hexdigest(),'factId':fid,'payload':payload,'fileInventoryRows':rows,'subject':subject,'payloadTargetGrammar':{'ordinaryFileIdAdmitted':v.is_valid(native_path),'retainedTargetAdmitted':v.is_valid(payload['resolvedTarget'])},'actualOccupancy':actual,'limitation':'This measures known-nonmatch routing before attribution for mismatched raw target/native file IDs. Whether advertised functional coverage requires a design correction is separately under independent review; no complete-search or final none=true construction is asserted.'}
(Path(__file__).parent/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
