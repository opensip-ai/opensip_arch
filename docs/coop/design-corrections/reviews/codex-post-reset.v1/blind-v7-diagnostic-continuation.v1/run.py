"""Root diagnostic variants only; not original blind graphs or final assessment."""
from pathlib import Path
import json,hashlib,sys,importlib.util,contextlib,io,traceback,datetime
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
out=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/blind-v7-diagnostic-continuation.v1')
work=out/'work'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(work.glob('*.py'))]
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v18.json';assert sha(mp)=='cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44';manifest=json.loads(mp.read_text());snapshot=Path(manifest['snapshotRoot']);model=snapshot/'docs/coop/design-corrections/foundation/identity-model.py';assert sha(model)==next(r['sha256'] for r in manifest['files'] if r['path']=='docs/coop/design-corrections/foundation/identity-model.py')
spec=importlib.util.spec_from_file_location('root_v18_identity',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);sys.path.insert(0,str(work));stdout=io.StringIO();checks=[]
with contextlib.redirect_stdout(stdout):
 import vec_ts,vec_rust,vec_syntax,graph
 for label,build in [('TS',lambda:vec_ts.build()),('Rust-A',lambda:vec_rust.build()),('Syntax-code',lambda:vec_syntax.build('code')),('Syntax-data',lambda:vec_syntax.build('data'))]:
  row={'id':label}
  try:
   built=build();world=built['kit'].w;objects={};badblobs=[]
   for digest,bb in world.cas.items():
    if hashlib.sha256(bb).hexdigest()!=digest:badblobs.append(digest)
    if bb.startswith(M.FRAME_PREFIX):
     domain,raw=bb[len(M.FRAME_PREFIX):].split(b'\0',1);domain=domain.decode();assert int.from_bytes(raw[:8],'big')==len(raw[8:]);record=json.loads(raw[8:]);
     if domain in M.PREFIX:objects[M.PREFIX[domain]+':'+digest]=(domain,record)
   own=graph.Closure(world);own_errors=own.close_run(built['run']);row.update(runId=built['run'],casObjects=len(world.cas),typedObjects=len(objects),badBlobDigests=badblobs,ownChecks=own.checks,ownErrors=own_errors)
   try:
    value=M.close_run(world.objects[built['run']],objects,world.cas);row.update(referenceResult='ADMITTED',value=str(value))
   except Exception as exc:row.update(referenceResult='REFUSED',exception=type(exc).__name__,detail=str(exc))
  except Exception as exc:row.update(referenceResult='BUILD_OR_AUDIT_EXCEPTION',exception=type(exc).__name__,detail=str(exc),traceback=traceback.format_exc())
  checks.append(row)
(out/'stdout.txt').write_text(stdout.getvalue());report={'standing':__doc__,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'acceptedParentSha256':sha(mp),'referenceModelSha256':sha(model),'copiedSourceFiles':rows,'checks':checks,'noFeedbackToBlindReviewer':True,'noProductQualification':True}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'standing':'Preliminary current output only. Final blind work still pending.','checks':checks},indent=2))
