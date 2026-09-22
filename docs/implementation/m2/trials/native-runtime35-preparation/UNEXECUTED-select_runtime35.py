"""Guarded one-file source410 activation after actual Opus5 review and root assent."""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,subprocess,shutil,tarfile,io
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';M=A/'docs/implementation/m2';T=Path('/tmp/opensip-implementation');U=M/'native-runtime-selection-v35';F=M/'trials/endpoint-lineage-410';R=T/'reviews/claude-opus5-runtime35-source410-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/native-runtime-materialization-35';P=T/'runtime35-activation/product';S=M/'native-runtime-selection-v35-subject.json';py=str(T/'source-audit364-env/bin/python')
q=argparse.ArgumentParser();q.add_argument('--root-assessment',type=Path,required=True);q.add_argument('--review-sha256',required=True);a=q.parse_args()
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def verify(root,row):
 p=root/row['path'];assert p.is_file()and not p.is_symlink();assert dig(p.read_bytes())=={k:row[k]for k in ('bytes','sha256')},str(p)
assert dig(S.read_bytes())=={'bytes':2472,'sha256':'172da5fa5333f8d36cd905b0695ffff6bbc731bf3ec374b1465fb6c3e6d7f9d8'}
for row in json.loads(S.read_bytes())['files']:verify(A,row)
assert dig((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==pin(S)['sha256']
source=review['sourceAcceptance'];assert source['accepted']is True and source['unit']=='endpoint-lineage-410'
assert source['archive']['sha256']=='6e67855cb57be6f35c37bf889bb841a90412aded041db558cb263d292d57e370'and source['archive']['manifestSha256']=='16c329491148082d71069798f5a167971657f199f669f94b4c11dc8eb5bd9774'
assessment=a.root_assessment.read_text();assert len(assessment)>500 and a.review_sha256 in assessment and pin(S)['sha256']in assessment
assert not E.exists()and not P.exists()and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json','INTERRUPTION.md','RESUME-REQUEST.md'}
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
evidence=[]
for line in (R/'hashes.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 sha,n,name=line.split(maxsplit=2);path=PurePosixPath(name);assert not path.is_absolute()and '..'not in path.parts;b=(R/name).read_bytes();assert dig(b)=={'bytes':int(n),'sha256':sha}
 if name.startswith('evidence/'):evidence.append({'path':name,**dig(b)})
for name in ('REVIEW.md','review.json','hashes.txt'):(D/name).write_bytes((R/name).read_bytes())
with tarfile.open(D/'replay-evidence.tar.xz','w:xz')as arc:
 for row in evidence:
  b=(R/row['path']).read_bytes();i=tarfile.TarInfo(row['path']);i.size=len(b);i.mode=0o644;i.mtime=0;arc.addfile(i,io.BytesIO(b))
save(D/'replay-evidence.json',{'archive':dig((D/'replay-evidence.tar.xz').read_bytes()),'files':evidence});(D/'root-assessment.md').write_text(assessment)
E.mkdir();checks=[]
def run(name,cmd,cwd,env=None):
 r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=900);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,(name,r.stdout.decode()[-2000:],r.stderr.decode()[-2000:]);return r.stdout
run('private-stage',[py,'-I','-B',str(U/'stage.py'),'--architecture',str(A),'--product',str(L),'--output',str(P)],A)
assent=M/'native-runtime-selection-v35-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'native-runtime-selection-v35','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(S),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==35 and len(lock['contractSuccessors'])==56
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(S),'review':pin(D/'review.json'),'assent':pin(assent)});new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
r=json.loads(run('private-design',[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)],P));assert r['passed']and len(r['contractSuccessors'])==57
baseline=json.loads((U/'baseline.json').read_bytes())['files'];mapping=json.loads((U/'materialization-map.json').read_bytes())['files'];assert len(mapping)==1;row=mapping[0];assert row['productPath']=='crates/host/src/installation_lineage.rs'and row['before']is not None
for b in baseline:verify(L,b)
verify(P,{'path':row['productPath'],**row['after']});(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);(E/'before-installation_lineage.rs').write_bytes((L/row['productPath']).read_bytes())
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
(L/row['productPath']).write_bytes((P/row['productPath']).read_bytes());assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
source_rows=[{**r,'path':r['path'][8:]}for r in json.loads((F/'subject.json').read_bytes())['files']if r['path'].startswith('product/')and r['path']!='product/design-lock.json'];assert len(source_rows)==591
for r in source_rows:verify(L,r)
r=json.loads(run('live-design',[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],L));assert r['passed']and len(r['contractSuccessors'])==57
for parent in (L,*L.parents):assert not any((parent/'.cargo'/n).exists()for n in ['config','config.toml'])
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());env['CARGO_TARGET_DIR']=str(T/'runtime35-live-check-target');env['RUST_TEST_THREADS']='1';assert not Path(env['CARGO_TARGET_DIR']).exists();save(E/'environment.json',env)
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
run('live-lineage-tests',[cargo,'test','--locked','--offline','-p','opensip-host','--lib','installation_lineage::'],L,env)
run('live-cargo-check',[cargo,'check','--locked','--offline','--workspace','--all-targets'],L,env)
for r in source_rows:verify(L,r)
assert(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'passed':True,'inventorySuccessors':35,'contractSuccessors':57,'mappedFiles':1,'unchangedNonLockFiles':590,'finalSourceNonLockFilesVerified':591,'independentReview':pin(D/'review.json'),'checks':checks,'fullM2Complete':False,'productQualification':False,'standing':'Actual Opus5 source/formal review and root assent, exact materialization and macOS development checks only. Conditional lineage sequencing is not native endpoint custody, registry/core/current trust authority, shared budget or creation qualification.'});(E/'selection.py').write_bytes(Path(__file__).read_bytes());save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus 5','rootSubstantiveAssent':True,'selected':True});print('PASS runtime35 selected35/57;1mapped590unchanged591nonlockverified;no commit/push')
