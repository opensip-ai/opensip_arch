"""Preliminary root audit of current blind output; no feedback or edits to blind session.
This is not the final blind assessment. Actual current source bytes are snapshotted before
execution; later changed blind source requires reassessment. Uses author reference only here.
"""
from pathlib import Path
import json,hashlib,shutil,ast,sys,importlib.util,contextlib,io,traceback,datetime
root=Path('/Users/sb/code/opensip-ai/opensip_arch');base=Path('/tmp/opensip-design-corrections');src=base/'consumer-b.v7/output/work';out=base/'codex-post-reset.v1/blind-v7-preliminary-admission.v1';assert not out.exists();out.mkdir();work=out/'work';work.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
for name in ['oslib.py','graph.py','build.py','vec_ts.py','vec_rust.py','vec_syntax.py']:
 p=src/name;bb=p.read_bytes();ast.parse(bb);q=work/name;q.write_bytes(bb);assert p.read_bytes()==bb;rows.append({'path':name,'sha256':sha(q),'bytes':len(bb)})
(out/'source-custody.json').write_text(json.dumps({'standing':__doc__,'source':str(src),'files':rows},indent=2)+'\n')
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
