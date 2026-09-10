"""Exact submitted checkpoint3 boundary controls, pure reference evidence only."""
from pathlib import Path
import hashlib,json,importlib.util,shutil,copy
B=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');b=B/'work';dc=b/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ready=json.loads((B/'review-ready.v3.json').read_text())
for row in ready['delta']['aggregateVsFrozenV13']['changedFiles']:assert sha(b/row['path'])==row['afterSha256'],row['path']
out=Path('/tmp/opensip-design-corrections/bv4-v3-checkpoint3-probes.v1');out.mkdir(exist_ok=False)
rels=['native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','native/native-capability-matrix.v2.json','workflows/workflows_model.v1.py','workflows/schemas/common.schema.json','workflows/schemas/command-envelope.schema.json','workflows/schemas/invocation-record.schema.json','workflows/command-inventory.v1.json','foundation/identity-schemas.v2.json','public-detail-registry.v1.json']
sources=[]
for rel in rels:
 p=dc/rel;q=out/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':'docs/coop/design-corrections/'+rel,'sha256':sha(q)})
s=importlib.util.spec_from_file_location('native_checkpoint3',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
s=importlib.util.spec_from_file_location('workflow_checkpoint3',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
def admission(doc,selector,value):
 try:W.validate_import_record(doc,selector,value);return {'result':'ADMIT'}
 except Exception as e:
  cause=e.__cause__ or e;return {'result':'REFUSE','validator':getattr(cause,'validator',None),'bound':getattr(cause,'validator_value',None),'instancePath':list(getattr(cause,'absolute_path',[]))}
CM='workflows/schemas/common.schema.json';ENV='workflows/schemas/command-envelope.schema.json'
selections=[N.default_capability_selection([{'rootPath':f'apps/s{step}/u{i:03}','languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(93)],[]) for step in range(2)]
avail=N.invocation_availability([(0,selections[0]['undeclaredCapabilities']),(1,selections[1]['undeclaredCapabilities'])])
single=N.invocation_availability([(0,selections[0]['undeclaredCapabilities'])])
env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'run','requestId':'req1_'+'b'*32,'projectId':'prj1-'+'a'*64,'termination':{'class':'success'},'exitCode':0,'run':{'kind':'analysis','authority':'authoritative','runId':'run2:'+'a'*64,'planId':'plan2:'+'b'*64,'verdict':'pass','requiredCoverage':'satisfied','durability':'committed','deficiency':'none','secondaryDeficiencies':[]},'availability':single}
r={'standing':'Root checkpoint source/schema/pure projection evidence on synthetic trusted selections and fake operational/content IDs for schema examples. No real host/renderer, full Invocation execution or Run closure claimed.',
 'checkpointSha256':sha(B/'review-ready.v3.json'),'sources':sources,
 'multistep':{'stepCounts':[v['noticeCount'] for v in avail['steps']],'total':avail['totalNoticeCount'],'schema':admission(CM,'#/$defs/CapabilityAvailabilityV1',avail)},'singleStepEnvelope':admission(ENV,'',env)}
# Own synthetic profile and scripted trusted results exercise the existing invocation reference, not
# a real authenticated profile installation or content-derived Run admission. Each availability entry
# is associated with an actual analysis StepId in the produced operational record.
steps=[{'stepId':i,'kind':'analysis','requirement':'required','dependsOn':[],'dependencyGate':'completed','retryPolicy':'none','params':{'kind':'analysis','profile':'default','role':'primary','durability':'authoritative','snapshotSource':'live-worktree'}} for i in range(2)]
record={'schemaFamily':'opensip.product.invocation','schemaMajor':1,'requestId':env['requestId'],'projectId':env['projectId'],'workflow':{'kind':'profile','contributionId':'root-synthetic-review','activationId':'root-synthetic-review','profileVersion':'1.0.0'},'mode':{'interactive':False,'ci':True,'ephemeral':False},'orderedSteps':steps}
script={str(i):[{'event':'completed','result':dict(env['run'],runId='run2:'+str(i+1)*64)}] for i in range(2)}
invocation,exitcode=W.run_invocation(record,script)
multi_env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'invocation','requestId':env['requestId'],'projectId':env['projectId'],'termination':invocation['termination'],'exitCode':exitcode,'invocation':invocation,'availability':avail}
r['multistep']['invocationReference']={'outcomes':[s['outcome'] for s in invocation['stepResults']],'schema':admission('workflows/schemas/invocation-record.schema.json','',invocation),'envelope':admission(ENV,'',multi_env),'stepIds':[s['stepId'] for s in invocation['orderedSteps']]}
mini=selections[0]['undeclaredCapabilities'][:1]
r['availabilityControls']={}
for name,pairs in [('empty-selection',[(0,[])]),('no-selection',[]),('same-tuple-two-steps',[(0,mini),(1,mini)])]:
 v=N.invocation_availability(pairs);r['availabilityControls'][name]={'value':v,'schema':admission(CM,'#/$defs/CapabilityAvailabilityV1',v)}
bad=copy.deepcopy(avail['steps'][0]['notices'][0]);bad['code']='CONFIG.INVALID';r['wrongNoticeCode']=admission(CM,'#/$defs/CapabilityAvailabilityNoticeV1',bad)
rows=[]
prefix='native.requested-capability-mode-unregistered:syntax:'
for raw_size in [1023,1024,1025,4149]:
 mode='x'*(raw_size-len(prefix))
 spec={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'syntax','languageMode':mode,'workspaceRoot':'.','required':True}],'policyPackIds':[],'parameters':[]};N.validate_foundation('analysis-spec',spec)
 try:N.admit_requested_capabilities(spec['requestedCapabilities']);raise AssertionError('Unknown mode unexpectedly admitted')
 except N.AdmissionError as e:raw=str(e)
 assert len(raw)==raw_size
 for origin in ['external-configuration','externally-supplied-spec','host-generated-internal-layer']:
  t=N.public_termination_for(raw,origin);errors=N.failure_envelope_errors(raw,origin);subject=errors[0]['subject']
  failure={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'f'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
  rows.append({'rawLength':len(raw),'origin':origin,'publicLength':len(subject),'unchangedWhenFits':subject==raw if len(raw)<=1024 else None,'fullRawDigestPreserved':subject.endswith(hashlib.sha256(raw.encode('utf-8')).hexdigest()) if len(raw)>1024 else None,'envelope':admission(ENV,'',failure)})
r['actualGuardBoundaries']=rows
reg=[{'capabilityId':'preview-typescript','languageModes':['ts-tsconfig']}];N.validate_native('ReleaseCapabilityRegistryV1',reg)
try:N.admit_release_capability_registry(reg);raise AssertionError('Preview unexpectedly admitted')
except N.AdmissionError as e:raw=str(e)
t=N.public_termination_for(raw);errors=N.failure_envelope_errors(raw);failure={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'f'*32,'termination':t,'exitCode':W.exit_code(t),'errors':errors}
r['previewGuard']={'raw':raw,'termination':t,'errors':errors,'envelope':admission(ENV,'',failure)}
cmd=next(c for c in json.loads((dc/'workflows/command-inventory.v1.json').read_text())['commands'] if c['name']=='default')
parity={k:'synthetic-'+k for k in cmd['parityFields']};parity['findings']=[];parity['capability-availability']=single
renderings=[W.render({'parity':parity,'envelope':env},fmt,cmd) for fmt in cmd['formats']]
r['parityControls']={'standing':'Pure model field selection using placeholder unrelated fields, not host projection-schema admission or renderer execution.','allAdvertisedFormatsKeepAvailability':all(x['parity'].get('capability-availability')==single for x in renderings),'formats':[x['format'] for x in renderings]}
missing=[]
for field in ['required-coverage','capability-availability']:
 p=copy.deepcopy(parity);del p[field]
 for fmt in cmd['formats']:
  try:v=W.render({'parity':p,'envelope':env},fmt,cmd);missing.append({'field':field,'format':fmt,'outcome':'RETURNED','fieldOmitted':field not in v['parity']})
  except Exception as e:missing.append({'field':field,'format':fmt,'outcome':'REFUSE','exception':type(e).__name__,'error':str(e)[:200]})
r['missingRequiredProjection']=missing
old=json.loads((b/'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_text())['codeMaps']['faultCauseToErrorCode'];expected={**old,'host-invariant':'SYSTEM.OUTCOME.ILLEGAL_STATE'}
common=json.loads((dc/'workflows/schemas/common.schema.json').read_text())
r['d9']={'exactInheritedPlusOne':W.FAULT_TO_ERROR==expected,'schemaCauseDomain':set(common['$defs']['D9FaultCause']['enum'])=={'none',*expected},'historicalSha256':sha(b/'docs/coop/artifacts/d9-exit-contract.v1.14.json')}
for row in sources:assert sha(b/row['path'])==row['sha256'],'Source changed during checkpoint probe'
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps({k:v for k,v in r.items() if k not in ('sources','standing','availabilityControls')},indent=2))
