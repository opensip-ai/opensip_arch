"""Actual semantic guard to public-envelope composition, synthetic bounded inputs."""
from pathlib import Path
import hashlib,json,importlib.util,shutil
b=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3/work');dc=b/'docs/coop/design-corrections'
out=Path('/tmp/opensip-design-corrections/bv4-v3-actual-guard-interim.v1');out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rels=['native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','native/native-capability-matrix.v2.json','workflows/workflows_model.v1.py','workflows/schemas/common.schema.json','workflows/schemas/command-envelope.schema.json','public-detail-registry.v1.json']
sources=[]
for rel in rels:
 p=dc/rel;q=out/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':'docs/coop/design-corrections/'+rel,'sha256':sha(q)})
s=importlib.util.spec_from_file_location('native_actualguard',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
s=importlib.util.spec_from_file_location('workflow_actualguard',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
def request(cap,mode):return [{'capabilityId':cap,'languageMode':mode,'workspaceRoot':'.','required':True}]
cases=[('unregistered-capability',lambda:N.admit_requested_capabilities(request('made-up','ts-tsconfig')),['external-configuration','externally-supplied-spec','host-generated-internal-layer']),
 ('unregistered-mode',lambda:N.admit_requested_capabilities(request('syntax','made-up')),['external-configuration','externally-supplied-spec','host-generated-internal-layer']),
 ('outside-selected-matrix',lambda:N.admit_requested_capabilities(request('clones-cross-tsjs','rust-cargo')),['external-configuration','externally-supplied-spec','host-generated-internal-layer']),
 ('release-unknown-capability',lambda:N.admit_release_capability_registry([{'capabilityId':'made-up','languageModes':['ts-tsconfig']}]),[None])]
rows=[]
for name,fn,origins in cases:
 try:fn();raise AssertionError('Expected semantic refusal: '+name)
 except N.AdmissionError as e:raw=str(e)
 for origin in origins:
  t=N.public_termination_for(raw,origin);errors=N.failure_envelope_errors(raw,origin)
  env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'e'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
  W.validate_import_record('workflows/schemas/command-envelope.schema.json','',env)
  rows.append({'case':name,'actualGuardRefusal':raw,'origin':origin,'normalized':N.normalize_internal_key(raw),'envelope':env,'schemaAdmission':'ADMIT'})
for row in sources:assert sha(b/row['path'])==row['sha256'],'Source changed during probe; preserve failure'
r={'standing':'Root interim pure semantic guard -> normalization -> origin-aware termination and required errors -> actual failure-envelope schema admission. Synthetic valid-shaped inputs and RequestId, no host runtime, full Run or final-source assent. Schema syntactic failures before these semantic guards are not exercised.','sources':sources,'cases':rows}
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps({'cases':len(rows),'allEnvelopeSchemas':'ADMIT','routes':[{'case':r['case'],'origin':r['origin'],'class':r['envelope']['termination']['class'],'error':r['envelope']['termination']['errorCode']} for r in rows]},indent=2))
