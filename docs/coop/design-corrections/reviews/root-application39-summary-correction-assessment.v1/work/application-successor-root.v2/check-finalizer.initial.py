"""Synthetic disposable tests of documentation application safety; no actual acceptance or application."""
from pathlib import Path
import contextlib,hashlib,importlib.util,io,json,tempfile
SOURCE=Path(__file__).with_name('files')/'docs/coop/design-corrections/finalize-application.v1.py'
spec=importlib.util.spec_from_file_location('documentation_finalizer',SOURCE);F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
def setup(base,verdict='ACCEPT'):
 root=base/'root';package=base/'package';root.mkdir();(package/'files/docs').mkdir(parents=True);(root/'docs').mkdir()
 (root/'docs/current.md').write_text('existing user work\n');(package/'files/docs/current.md').write_text('reviewed synthetic after image\n');(package/'files/docs/new.md').write_text('new synthetic document\n')
 entries=[]
 for rel in ['docs/current.md','docs/new.md']:
  p=package/'files'/rel;live=root/rel;entries.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size,'beforeSha256':sha(live) if live.exists() else None})
 mr='docs/manifest.json';rr='docs/review.json';m={'standing':'SYNTHETIC TEST ONLY, NO REAL ACCEPTANCE','implementationAuthorized':False,'retainedManifestPath':mr,'retainedReviewPath':rr,'files':entries}
 mp=package/'manifest.json';mp.write_text(json.dumps(m));mh=sha(mp)
 rp=package/'review.json';rp.write_text(json.dumps({'standing':'SYNTHETIC TEST ONLY','verdict':verdict,'subjectManifestSha256':mh}));rh=sha(rp)
 (root/mr).write_bytes(mp.read_bytes());(root/rr).write_bytes(rp.read_bytes())
 return root,package,mp,mh,rp,rh

def inventory(root):return {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}
def negative(label,mutation):
 with tempfile.TemporaryDirectory(prefix='opensip-finalizer-test-') as td:
  args=list(setup(Path(td)));mutation(args);before=inventory(args[0]);caught=False
  try:
   with contextlib.redirect_stdout(io.StringIO()):F.apply(*args)
  except (AssertionError,ValueError):caught=True
  rows.append({'id':label,'passed':caught and before==inventory(args[0]),'writesAfterRefusal':before!=inventory(args[0])})
negative('changed-user-file-refuses-without-writes',lambda a:(a[0]/'docs/current.md').write_text('later user change\n'))
negative('changed-staged-file-refuses-without-writes',lambda a:(a[1]/'files/docs/current.md').write_text('unreviewed change\n'))
negative('incorrect-manifest-digest-refuses-without-writes',lambda a:a.__setitem__(3,'f'*64))
negative('incorrect-review-digest-refuses-without-writes',lambda a:a.__setitem__(5,'f'*64))
def altered_verdict(a):
 d=json.loads(a[4].read_text());d['verdict']='CHANGES_REQUIRED';a[4].write_text(json.dumps(d));a[5]=sha(a[4]);(a[0]/'docs/review.json').write_bytes(a[4].read_bytes())
negative('changes-required-is-never-application-authority',altered_verdict)
def wrong_subject(a):
 d=json.loads(a[4].read_text());d['subjectManifestSha256']='0'*64;a[4].write_text(json.dumps(d));a[5]=sha(a[4]);(a[0]/'docs/review.json').write_bytes(a[4].read_bytes())
negative('different-reviewed-subject-refuses-without-writes',wrong_subject)
negative('missing-retained-review-refuses-without-writes',lambda a:(a[0]/'docs/review.json').unlink())
for interrupted in (False,True):
 with tempfile.TemporaryDirectory(prefix='opensip-finalizer-test-') as td:
  args=setup(Path(td));root,package=args[:2]
  if interrupted:(root/'docs/current.md').write_bytes((package/'files/docs/current.md').read_bytes())
  before=inventory(root)
  with contextlib.redirect_stdout(io.StringIO()):F.apply(*args,check_only=True)
  rows.append({'id':'check-only-writes-nothing-'+str(interrupted),'passed':before==inventory(root)})
  with contextlib.redirect_stdout(io.StringIO()):F.apply(*args)
  activation=json.loads((root/'docs/coop/design-corrections/application-activation.v1.json').read_text())
  rows.append({'id':'exact-application-with-activation-last-'+str(interrupted),'passed':all((root/r).read_bytes()==(package/'files'/r).read_bytes() for r in ['docs/current.md','docs/new.md']) and activation['appliedFileCount']==2 and activation['implementationAuthorized'] is False})
  before=inventory(root);caught=False
  try:
   with contextlib.redirect_stdout(io.StringIO()):F.apply(*args)
  except AssertionError:caught=True
  rows.append({'id':'existing-activation-not-overwritten-'+str(interrupted),'passed':caught and before==inventory(root)})
report={'standing':'Synthetic disposable documentation-finalizer tests only; test ACCEPT strings are not actual review evidence and cannot confer project readiness. All writes stayed in temporary synthetic roots, removed afterward.','source':str(SOURCE),'sourceSha256':sha(SOURCE),'checks':rows,'passed':sum(r['passed'] for r in rows),'failed':[r['id'] for r in rows if not r['passed']],'actualApplicationPerformed':False}
Path(__file__).with_name('finalizer-selftest.v1.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['passed','failed','actualApplicationPerformed']}));raise SystemExit(bool(report['failed']))
