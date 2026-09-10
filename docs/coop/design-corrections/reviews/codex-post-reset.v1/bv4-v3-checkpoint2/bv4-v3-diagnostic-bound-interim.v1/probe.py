"""Semantic-invalid but schema-shaped input must still yield a bounded failure envelope."""
from pathlib import Path
import hashlib,json,importlib.util,shutil
b=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3/work');dc=b/'docs/coop/design-corrections'
out=Path('/tmp/opensip-design-corrections/bv4-v3-diagnostic-bound-interim.v1');out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rels=['native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','workflows/workflows_model.v1.py','workflows/schemas/common.schema.json','workflows/schemas/command-envelope.schema.json','foundation/identity-schemas.v2.json']
sources=[]
for rel in rels:
 p=dc/rel;q=out/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':'docs/coop/design-corrections/'+rel,'sha256':sha(q)})
s=importlib.util.spec_from_file_location('native_bound',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
s=importlib.util.spec_from_file_location('workflow_bound',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
spec={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'syntax','languageMode':'x'*4096,'workspaceRoot':'.','required':True}],'policyPackIds':[],'parameters':[]}
N.validate_foundation('analysis-spec',spec)
try:N.admit_requested_capabilities(spec['requestedCapabilities']);raise AssertionError('Expected unknown mode refusal')
except N.AdmissionError as e:raw=str(e)
rows=[]
for origin in ['external-configuration','externally-supplied-spec','host-generated-internal-layer']:
 t=N.public_termination_for(raw,origin);errors=N.failure_envelope_errors(raw,origin)
 env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'f'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
 row={'origin':origin,'errorSubjectLength':len(errors[0]['subject'])}
 try:W.validate_import_record('workflows/schemas/command-envelope.schema.json','',env);row['envelopeAdmission']='ADMIT'
 except Exception as e:
  cause=e.__cause__ or e;row.update(envelopeAdmission='REFUSE',validator=getattr(cause,'validator',None),validatorValue=getattr(cause,'validator_value',None),instancePath=list(getattr(cause,'absolute_path',[])))
 rows.append(row)
for row in sources:assert sha(b/row['path'])==row['sha256'],'Source changed during probe; preserve failure'
r={'standing':'Interim actual semantic-guard composition diagnostic on synthetic schema-shaped spec. No host runtime, execution or final-source assent. Input is structurally admitted, then correctly refused by semantic mode membership; the issue is whether that refusal can be published within its output bounds.',
 'sources':sources,'inputSchemaAdmission':'ADMIT','modeLength':4096,'actualGuardKey':N.normalize_internal_key(raw)[0],'cases':rows,
 'observation':'A4096-character languageMode is allowed by analysis-spec Text but unregistered. Its actual semantic refusal is copied whole into DomainDetail.subject, producing4151characters and violating BoundedText1024. Define an explicit bounded diagnostic projection without losing the stable error code and meaningful subject identity; test boundary/overbound controls through the actual guard and full envelope.'}
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py');print(json.dumps({k:v for k,v in r.items() if k not in ('sources','standing')},indent=2))
