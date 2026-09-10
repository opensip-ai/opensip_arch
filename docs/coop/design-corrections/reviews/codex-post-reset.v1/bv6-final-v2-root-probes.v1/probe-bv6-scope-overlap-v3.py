"""Root-selected full retained Run controls; v2 extra declares capability was a harness mistake (fact relation is not request capability) for the already-published disjointness law."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections';source=dc/'integration-fixtures.py'
spec=importlib.util.spec_from_file_location('bv6_overlap_fixture',source);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
rows=[]
for label,overlap in [('disjoint',False),('overlap',True),('different-relation-same-subjects',True)]:
 try:
  run,objects,blobs=f.build(resolved=True,has_match=True);before=f.M.close_run(run,objects,blobs)
  original=copy.deepcopy(next(v for d,v in objects.values() if d=='subject-scope'));scope=copy.deepcopy(original)
  if label=='different-relation-same-subjects':scope.update(relation='declares',resolution='syntactic')
  scope['subjects']=sorted(set(['independent-symbol']+(original['subjects'] if overlap else [])))
  sid=f.M.identifier('subject-scope',scope);objects[sid]=('subject-scope',scope)
  paths=[r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
  payload=f.coverage_result(scope,scope['sourceUniverse'],True,blobs,paths)
  schema=next(v['payloadSchemaDigest'] for d,v in objects.values() if d=='coverage')
  producer=f.N.admit_coverage_result_v3(payload,scope,[],schema)
  coverage={'schemaVersion':2,'scopeId':sid,'payloadSchemaDigest':schema,'payloadDigest':f.put_blob(blobs,payload)}
  cid=f.M.identifier('coverage',coverage);objects[cid]=('coverage',coverage)
  vid=objects[run['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(objects[vid][1]);view['scopeIds'].append(sid);view['coverageIds'].append(cid);f.rekey(objects,vid,view,run)
  evidence=copy.deepcopy(objects[run['evidenceId']][1]);evidence['coverageIds'].append(cid);f.rekey(objects,run['evidenceId'],evidence,run)
  f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
  row={'case':label,'expected':'REFUSE-OVERLAP' if label=='overlap' else 'ADMIT','baselineRunId':before,'originalSubjects':original['subjects'],'secondSubjects':scope['subjects'],'producer':producer}
  try:row.update(actual='ADMIT',runId=f.M.close_run(run,objects,blobs))
  except Exception as e:row.update(actual='REFUSAL',error=type(e).__name__+':'+str(e))
  rows.append(row)
 except Exception as e:rows.append({'case':label,'actual':'HARNESS_OR_BASELINE_FAILURE','error':type(e).__name__+':'+str(e)})
print(json.dumps({'standing':'Root-selected full synthetic retained Run controls, shared fixture construction is not independent consumer evidence or native/host qualification. Expected disjointness derived from identity sec3. First actual failure recorded without presuming its cause.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [source,dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py']],'cases':rows},indent=2))
