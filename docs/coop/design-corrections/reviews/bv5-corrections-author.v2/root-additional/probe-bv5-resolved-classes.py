"""Root negative control for the published complete unresolved-class set law."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections'
spec=importlib.util.spec_from_file_location('bv5_resolved_root',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
rows=[]
for label,classes in [('valid-complete-empty',[]),('contradictory-complete-nonempty',['computed-member-access'])]:
 try:
  run,objects,blobs=f.build(resolved=True,has_match=True)
  baseline=f.M.close_run(run,objects,blobs)
  cid=next(k for k,(d,v) in objects.items() if d=='coverage');cov=copy.deepcopy(objects[cid][1])
  payload=f.C.parse(blobs[cov['payloadDigest']]);payload['entry']['resolutionCompleteness']['unresolvedEdgeClasses']=classes
  cov['payloadDigest']=f.put_blob(blobs,payload);f.rekey(objects,cid,cov,run)
  f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
  final=f.M.close_run(run,objects,blobs)
  rows.append({'case':label,'baselineRunId':baseline,'result':'ADMIT','runId':final,'completeness':payload['entry']['resolutionCompleteness']})
 except Exception as e:rows.append({'case':label,'result':'REFUSAL_OR_HARNESS_ERROR','error':type(e).__name__+':'+str(e)[:500]})
print(json.dumps({'scope':'Synthetic full reference Run; current shared fixture construction, root mutation and actual retained admission. No product qualification.','sourceRoot':str(root),'nativeModelSha256':hashlib.sha256((dc/'native/native_evidence_model.v2.py').read_bytes()).hexdigest(),'nativeSchemaSha256':hashlib.sha256((dc/'native/native-evidence.schemas.v2.json').read_bytes()).hexdigest(),'cases':rows},indent=2))
