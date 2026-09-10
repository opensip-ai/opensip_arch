"""Root interim composition control: a StepTermination versus its pre-Plan Failure CommandEnvelope.
Synthetic schema-only request id; no host runtime or actual request/public delivery claimed.
"""
from pathlib import Path
import hashlib,importlib.util,json,shutil
base=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');dc=base/'work/docs/coop/design-corrections'
p=dc/'native/native_evidence_model.v2.py';s=importlib.util.spec_from_file_location('root_v3_n',p);n=importlib.util.module_from_spec(s);s.loader.exec_module(n)
p=dc/'workflows/workflows_model.v1.py';s=importlib.util.spec_from_file_location('root_v3_w',p);w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
rows=[]
for origin in ['external-configuration','externally-supplied-spec','host-generated-internal-layer']:
 term=n.public_termination_for('native.requested-capability-unregistered',origin)
 envelope={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'a'*32,'termination':term,'exitCode':w.EXIT[term['class']]}
 if 'domainDetail' in term:envelope['errors']=[term['domainDetail']]
 row={'origin':origin,'termination':term,'envelope':envelope}
 for key,doc,selector,value in [('termination','common.schema.json','#/$defs/StepTermination',term),('envelope','command-envelope.schema.json','',envelope)]:
  try:w.validate_import_record('workflows/schemas/'+doc,selector,value);row[key+'Admission']='ADMIT'
  except Exception as exc:row[key+'Admission']='REFUSE';row[key+'Error']=str(exc.__cause__).split('\n')[0] if exc.__cause__ else str(exc)
 rows.append(row)
assert all(r['terminationAdmission']=='ADMIT' for r in rows)
assert rows[0]['envelopeAdmission']=='ADMIT' and all(r['envelopeAdmission']=='REFUSE' for r in rows[1:])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Interim root composition diagnostic, not final-source assent or host output. The deliberately minimal Failure envelope includes the generated termination and, when present, its actual domainDetail as errors. Omitted errors demonstrates a required carrier the new projection does not supply; it is NOT a claim that a real host currently emits this invalid envelope.','sourceRoot':str(base/'work'),'sources':[{'path':str(p.relative_to(base/'work')),'sha256':sha(p)} for p in [dc/'native/native_evidence_model.v2.py',dc/'native/native-evidence.schemas.v2.json',dc/'workflows/workflows_model.v1.py',dc/'workflows/schemas/common.schema.json',dc/'workflows/schemas/command-envelope.schema.json']], 'cases':rows}
out=Path('/tmp/opensip-design-corrections/bv4-v3-envelope-interim.v1');out.mkdir(exist_ok=False);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
for row in report['sources']:
 p=base/'work'/row['path'];assert sha(p)==row['sha256'];q=out/'source'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
print(json.dumps({'cases':[{k:v for k,v in r.items() if k not in ['termination','envelope']} for r in rows]},indent=2))
