"""Source-bound checkpoint2 probes. Not independent acceptance or host execution."""
from pathlib import Path
import hashlib,json,importlib.util,shutil
B=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');b=B/'work';dc=b/'docs/coop/design-corrections'
ready=json.loads((B/'review-ready.v2.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in ready['delta']['aggregateVsFrozenV13']['changedFiles']:assert sha(b/row['path'])==row['afterSha256'],row['path']
out=Path('/tmp/opensip-design-corrections/bv4-v3-checkpoint2-probes.v1');out.mkdir(exist_ok=False)
rels=['native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','native/native-capability-matrix.v2.json','workflows/workflows_model.v1.py','workflows/schemas/common.schema.json','workflows/schemas/command-envelope.schema.json','workflows/schemas/invocation-record.schema.json','workflows/command-inventory.v1.json','foundation/identity-schemas.v2.json','public-detail-registry.v1.json']
sources=[]
for rel in rels:
 p=dc/rel;q=out/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':'docs/coop/design-corrections/'+rel,'sha256':sha(q)})
s=importlib.util.spec_from_file_location('native_checkpoint2',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
s=importlib.util.spec_from_file_location('workflow_checkpoint2',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
def admission(doc,selector,value):
 try:W.validate_import_record(doc,selector,value);return {'result':'ADMIT'}
 except Exception as e:
  cause=e.__cause__ or e
  return {'result':'REFUSE','validator':getattr(cause,'validator',None),'bound':getattr(cause,'validator_value',None),'instancePath':list(getattr(cause,'absolute_path',[]))}
CM='workflows/schemas/common.schema.json';ENV='workflows/schemas/command-envelope.schema.json'
selections=[]
for step in range(2):
 units=[{'rootPath':f'apps/s{step}/unit{i:03}','languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(93)]
 selections.append(N.default_capability_selection(units,[]))
collections=[N.release_absence_notices(s['undeclaredCapabilities']) for s in selections]
combined=N.release_absence_notices([r for s in selections for r in s['undeclaredCapabilities']])
r={'standing':'Root coauthor checkpoint diagnostic: pure reference selection/guards/schema/render projection on synthetic trusted inputs. No real host/renderer, full invocation execution or Run closure is claimed. Full subject acceptance still requires independent review.',
 'checkpointSha256':sha(B/'review-ready.v2.json'),'sources':sources,
 'multistep':{'eachRequestedCounts':[len(s['analysisSpec']['requestedCapabilities']) for s in selections],
 'eachCollectionAdmission':[admission(CM,'#/$defs/CapabilityAvailabilityV1',v) for v in collections],
 'flatAggregateCount':combined['noticeCount'],'flatAggregateAdmission':admission(CM,'#/$defs/CapabilityAvailabilityV1',combined)}}
spec={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'syntax','languageMode':'x'*4096,'workspaceRoot':'.','required':True}],'policyPackIds':[],'parameters':[]}
N.validate_foundation('analysis-spec',spec)
try:N.admit_requested_capabilities(spec['requestedCapabilities']);raise AssertionError('Unknown mode unexpectedly admitted')
except N.AdmissionError as e:raw=str(e)
rows=[]
for origin in ['external-configuration','externally-supplied-spec','host-generated-internal-layer']:
 t=N.public_termination_for(raw,origin);errors=N.failure_envelope_errors(raw,origin)
 env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'f'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
 rows.append({'origin':origin,'subjectLength':len(errors[0]['subject']),'admission':admission(ENV,'',env)})
r['longDiagnostic']={'inputSchemaAdmission':'ADMIT','modeLength':4096,'actualGuardKey':N.normalize_internal_key(raw)[0],'compositions':rows}
reg=[{'capabilityId':'preview-typescript','languageModes':['ts-tsconfig']}];N.validate_native('ReleaseCapabilityRegistryV1',reg)
try:N.admit_release_capability_registry(reg);raise AssertionError('Preview unexpectedly admitted')
except N.AdmissionError as e:raw=str(e)
try:result=N.failure_envelope_errors(raw);pr={'composition':'ADMIT','errors':result}
except Exception as e:pr={'composition':'REFUSE','error':str(e)}
r['previewGuard']={'inputSchemaAdmission':'ADMIT','actualGuardOutput':raw,**pr}
cmd=next(c for c in json.loads((dc/'workflows/command-inventory.v1.json').read_text())['commands'] if c['name']=='default')
# Same projection harness shape as the existing renderer reference checker; placeholder values are not
# admitted as a host semantic projection. The question is solely whether selecting declared field names drops
# the new availability value, which does not depend on the placeholder values of unrelated fields.
parity={k:'synthetic-'+k for k in cmd['parityFields']};parity['findings']=[];parity['availability']=collections[0]
projected={'parity':parity,'envelope':{'availability':collections[0]},'hints':[]}
renderings=[W.render(projected,fmt,cmd) for fmt in cmd['formats']]
r['parityProjection']={'standing':'Actual pure render field-selection diagnostic with synthetic unrelated fields; not host projection/schema admission or actual renderer implementation.',
 'declaredFields':cmd['parityFields'],'formats':[{'format':v['format'],'availabilityInParity':'availability' in v['parity'],'availabilityInEnvelope':'availability' in v.get('envelope',{})} for v in renderings]}
notice=collections[0]['notices'][0].copy();notice['code']='CONFIG.INVALID'
r['noticeWrongCode']=admission(CM,'#/$defs/CapabilityAvailabilityNoticeV1',notice)
for row in sources:assert sha(b/row['path'])==row['sha256'],'Source changed during checkpoint probe'
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps({k:v for k,v in r.items() if k not in ('sources','standing')},indent=2))
