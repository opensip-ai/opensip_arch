"""Root-selected coverage mutations through full retained reference Run closure."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections'
source=dc/'integration-fixtures.py'
spec=importlib.util.spec_from_file_location('bv5_root_full_graph',source)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
rows=[]
for label,rung,delta in [('valid-observed','observed',{}),('wrong-cross-relation-rung','enumerated',{}),('wrong-attempted','observed',{'attempted':True}),('wrong-classes','observed',{'unresolvedEdgeClasses':['computed-member-access']})]:
 try:
  run,objects,blobs=f.build(resolved=True,has_match=True)
  before=f.M.close_run(run,objects,blobs)
  plan=copy.deepcopy(objects[run['planId']][1]);analysis=f.C.parse(blobs[plan['analysisSpecDigest']])
  request=copy.deepcopy(analysis['requestedCapabilities'][0]);request['capabilityId']='unresolved-edge'
  if request not in analysis['requestedCapabilities']:analysis['requestedCapabilities'].append(request)
  plan['analysisSpecDigest']=f.put_blob(blobs,f.sort_canonical_sets('analysis-spec',analysis))
  f.rekey_plan(objects,blobs,run,plan)
  scope=copy.deepcopy(next(v for d,v in objects.values() if d=='subject-scope'))
  scope.update(relation='unresolved-edge',resolution=rung)
  sid=f.M.identifier('subject-scope',scope);objects[sid]=('subject-scope',scope)
  paths=[r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
  payload=f.coverage_result(scope,scope['sourceUniverse'],True,blobs,paths)
  payload['entry']['resolutionCompleteness'].update(delta)
  schema=next(v['payloadSchemaDigest'] for d,v in objects.values() if d=='coverage')
  producer=f.N.admit_coverage_result_v3(payload,scope,[],schema)
  coverage={'schemaVersion':2,'scopeId':sid,'payloadSchemaDigest':schema,'payloadDigest':f.put_blob(blobs,payload)}
  cid=f.M.identifier('coverage',coverage);objects[cid]=('coverage',coverage)
  vid=objects[run['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(objects[vid][1])
  view['scopeIds'].append(sid);view['coverageIds'].append(cid);f.rekey(objects,vid,view,run)
  evidence=copy.deepcopy(objects[run['evidenceId']][1]);evidence['coverageIds'].append(cid)
  f.rekey(objects,run['evidenceId'],evidence,run)
  f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
  final=f.M.close_run(run,objects,blobs)
  rows.append({'case':label,'baselineRunId':before,'pair':'unresolved-edge@'+rung,'completeness':payload['entry']['resolutionCompleteness'],'producer':producer,'result':'ADMIT','runId':final})
 except Exception as e:rows.append({'case':label,'result':'REFUSAL_OR_HARNESS_ERROR','error':type(e).__name__+':'+str(e)[:600]})
print(json.dumps({'scope':'Synthetic full retained Run closure with current shared fixture builder; root-selected mutations and re-keying. No product/native compiler/OS qualification. Exceptions are not automatically design refusals.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [source,dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py',dc/'native/native-evidence.schemas.v2.json']],'cases':rows},indent=2))
