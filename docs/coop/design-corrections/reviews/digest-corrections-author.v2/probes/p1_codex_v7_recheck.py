"""Codex draft coauthor probe: a self-consistent frame must not bypass native admission."""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil
root=Path.cwd();base=Path('/tmp/opensip-design-corrections/native-run-probe.v7-recheck');snapshot=base/'subject';dc='docs/coop/design-corrections/'
assert snapshot.is_dir()
captured=[{'path':str(p.relative_to(snapshot)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for unit in ['foundation','native','security','workflows'] for p in (snapshot/dc/unit).rglob('*') if p.is_file() and p.suffix in ('.py','.json')]
spec=importlib.util.spec_from_file_location('native_run_probe',snapshot/dc/'integration-fixtures.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F);M=F.M;C=F.C;N=F.M.native_admission()
run,objects,blobs=F.build(resolved=True,has_match=True)
original=M.close_run(run,objects,blobs)
plan=copy.deepcopy(objects[run['planId']][1]);old_context=next(d for d in plan['nativeContextDigests'] if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')
_,context,_=M.parse_h_frame(blobs[old_context],'native-context')
context['moduleResolutionMode']='bundler' if context['moduleResolutionMode']!='bundler' else 'node16'
native=N.admit_native_context('typescript',context,{k:v for k,(d,v) in objects.items() if d=='closure'})
new_context=M.native_context_frame('native.context.typescript.v2',context,blobs)
scope_id=next(k for k,(d,v) in objects.items() if d=='subject-scope');old_universe=objects[scope_id][1]['sourceUniverse']
_,universe,_=M.parse_h_frame(blobs[old_universe],'native-semantic-universe');universe['nativeContextId']='sha256:'+new_context
new_universe=M.native_universe_frame('native.semantic-universe.typescript.v2',universe,blobs)
for key in list(objects):
    if key not in objects:continue
    domain,value=objects[key]
    if domain in ('fact','subject-scope'):
        value=copy.deepcopy(value);value['sourceUniverse']=new_universe;value['targetUniverse']=new_universe;F.rekey(objects,key,value,run)
plan=copy.deepcopy(objects[run['planId']][1]);plan['nativeContextDigests']=sorted(new_context if d==old_context else d for d in plan['nativeContextDigests']);F.rekey_plan(objects,blobs,run,plan)
proof_id=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[proof_id][1]);view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']]);witness['matchingFactIds']=view['facts'];witness['coverageIds']=view['coverageIds'];proof['predicateProofs'][0]['witnessDigest']=F.put_blob(blobs,witness);F.rekey(objects,proof_id,proof,run)
try:result={'admitted':True,'runId':M.close_run(run,objects,blobs)}
except Exception as exc:result={'admitted':False,'error':type(exc).__name__+':'+str(exc)}
out={'standing':'Codex independent probe of IN-PROGRESS coauthor bytes, not an independent acceptance review','capturedSources':captured,'originalPositiveRun':original,'nativeAdmissionRefusals':native['refusals'],'reframedCompleteRun':result}
(base/'result.recheck.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='capturedSources'},indent=2))
