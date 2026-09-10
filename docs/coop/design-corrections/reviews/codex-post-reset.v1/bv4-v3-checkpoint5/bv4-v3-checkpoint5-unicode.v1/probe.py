from pathlib import Path
import json,hashlib,importlib.util,shutil
B=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');dc=B/'work/docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ready=json.loads((B/'review-ready.v5.json').read_text())
for row in ready['delta']['aggregateVsFrozenV13']['changedFiles']:assert sha(B/'work'/row['path'])==row['afterSha256']
out=Path('/tmp/opensip-design-corrections/bv4-v3-checkpoint5-unicode.v1');out.mkdir(exist_ok=False)
mods=[]
for name,rel in [('native5','native/native_evidence_model.v2.py'),('workflow5','workflows/workflows_model.v1.py')]:
 s=importlib.util.spec_from_file_location(name,dc/rel);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);mods.append(m)
N,W=mods;prefix='native.requested-capability-mode-unregistered:syntax:';rows=[]
for char in ['\U0001f980','\u00e9']:
 for size in [1023,1024,1025,4149]:
  mode=char*(size-len(prefix));spec={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'syntax','languageMode':mode,'workspaceRoot':'.','required':True}],'policyPackIds':[],'parameters':[]};N.validate_foundation('analysis-spec',spec)
  try:N.admit_requested_capabilities(spec['requestedCapabilities']);raise AssertionError('Unexpected admission')
  except N.AdmissionError as e:raw=str(e)
  assert len(raw)==size
  expected=raw if size<=1024 else raw[:950]+'...#sha256:'+hashlib.sha256(raw.encode('utf-8')).hexdigest()
  for origin in ['external-configuration','externally-supplied-spec','host-generated-internal-layer']:
   t=N.public_termination_for(raw,origin);errors=N.failure_envelope_errors(raw,origin)
   failure={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'f'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
   W.validate_import_record('workflows/schemas/command-envelope.schema.json','',failure)
   assert errors[0]['subject']==expected
   rows.append({'character':char,'rawScalars':len(raw),'rawUtf8Bytes':len(raw.encode('utf-8')),'origin':origin,'subjectScalars':len(expected),'exactIndependentProjection':True,'fullFailureEnvelope':'ADMIT'})
for row in ready['delta']['aggregateVsFrozenV13']['changedFiles']:
 p=B/'work'/row['path'];assert sha(p)==row['afterSha256'];q=out/'submitted-source'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
r={'checkpointSha256':sha(B/'review-ready.v5.json'),'standing':'Actual semantic mode guard on structurally admitted synthetic specs, exact independent Unicode scalar slicing/UTF8 digest projection and full failure-envelope schema admission; not actual host execution or product qualification. Prior checkpoint4 behaviors unchanged only where source comparison proves it.','cases':rows}
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copy2(__file__,out/'probe.py');print(json.dumps({'cases':len(rows),'allAdmitted':True,'checkpointSha256':r['checkpointSha256']}))
