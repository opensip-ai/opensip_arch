"""Compare retained fact-free scopes with and without registered relation/rung membership."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections'
sp=importlib.util.spec_from_file_location('bv5_scope_root',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
rows=[]
for rung in ['observed','enumerated']:
 try:
  run,objects,blobs=f.build(resolved=True,has_match=True);baseline=f.M.close_run(run,objects,blobs)
  scope=copy.deepcopy(next(v for d,v in objects.values() if d=='subject-scope'));scope.update(relation='unresolved-edge',resolution=rung)
  sid=f.M.identifier('subject-scope',scope);objects[sid]=('subject-scope',scope)
  vid=objects[run['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(objects[vid][1]);view['scopeIds'].append(sid)
  f.rekey(objects,vid,view,run);f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
  rid=f.M.close_run(run,objects,blobs)
  rows.append({'pair':'unresolved-edge@'+rung,'baselineRunId':baseline,'extraScopeId':sid,'extraCoverageAdded':False,'result':'ADMIT','runId':rid})
 except Exception as e:rows.append({'pair':'unresolved-edge@'+rung,'result':'REFUSAL_OR_HARNESS_ERROR','error':type(e).__name__+':'+str(e)[:500]})
print(json.dumps({'scope':'Full synthetic retained reference Run using existing fixture; extra scope without coverage. No claim that this scopes a requested/output capability bijection or tests a product implementation.','sourceRoot':str(root),'nativeModelSha256':hashlib.sha256((dc/'native/native_evidence_model.v2.py').read_bytes()).hexdigest(),'identityModelSha256':hashlib.sha256((dc/'foundation/identity-model.py').read_bytes()).hexdigest(),'cases':rows},indent=2))
