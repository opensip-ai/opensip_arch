"""Guarded two-file source415 activation after actual Claude review and root assent."""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,subprocess,shutil,tarfile,io
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';M=A/'docs/implementation/m2';T=Path('/tmp/opensip-implementation');U=M/'native-runtime-selection-v36';F=M/'trials/trust-budget-scope-415';R=T/'reviews/claude-opus5-runtime36-source415-r1';D=M/'reviews'/R.name;E=M/'trials/native-runtime-materialization-36';P=T/'runtime36-activation/product';S=M/'native-runtime-selection-v36-subject.json';py=str(T/'source-audit364-env/bin/python')
q=argparse.ArgumentParser();q.add_argument('--root-assessment',type=Path,required=True);q.add_argument('--review-sha256',required=True);a=q.parse_args()
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def verify(root,row):
 p=root/row['path'];assert p.is_file()and not p.is_symlink();assert dig(p.read_bytes())=={k:row[k]for k in ('bytes','sha256')},str(p)
assert dig(S.read_bytes())=={'bytes':2480,'sha256':'43e059a622b531c7c876ef563fe0c4a5ee8650858dc58a17845799b43d0f582d'}
for row in json.loads(S.read_bytes())['files']:verify(A,row)
assert dig((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==pin(S)['sha256']
source=review['sourceAcceptance'];assert source['accepted']is True and source['unit']=='trust-budget-scope-415'
assert source['archive']['sha256']=='8b9fa526c8d548bfe5abbe5d34151bb747e94fb406c1c18097c1d10fedc3625f'and source['archive']['manifestSha256']=='225a23a86a31066c2a4813e66e788a661a65b6195dfd36220c2113371349d41e'
assessment=a.root_assessment.read_text();assert len(assessment)>500 and a.review_sha256 in assessment and pin(S)['sha256']in assessment
assert not E.exists()and not P.exists()and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json','RESUME-REQUEST.md','interruption.json'}
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
evidence=[];resolved=[];snapshots={}
for line in (R/'hashes.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 sha,n,name=line.split(maxsplit=2);path=PurePosixPath(name);assert not path.is_absolute()and '..'not in path.parts
 base=A if name.startswith('docs/') else R
 p=base/name;assert p.is_file()and not p.is_symlink();b=p.read_bytes();assert dig(b)=={'bytes':int(n),'sha256':sha},name
 entry={'path':name,'resolvedRoot':str(base),**dig(b)}
 if base==R:
  archived='reviewer/'+name;entry['archivedAs']=archived;snapshots[archived]=b
 resolved.append(entry)
for name in ('REVIEW.md','review.json'):
 assert any(r['path']==name for r in resolved),('reviewer hash missing',name)
for p in sorted((R/'evidence').rglob('*')) if (R/'evidence').exists() else []:
 if p.is_file():
  assert not p.is_symlink();snapshots.setdefault('reviewer/'+str(p.relative_to(R)),p.read_bytes())
for name,b in sorted(snapshots.items()):evidence.append({'path':name,**dig(b)})
save(D/'resolved-reviewer-inputs.json',resolved)
for name in ('REVIEW.md','review.json','hashes.txt'):(D/name).write_bytes((R/name).read_bytes())
with tarfile.open(D/'replay-evidence.tar.xz','w:xz')as arc:
 for row in evidence:
  b=snapshots[row['path']];i=tarfile.TarInfo(row['path']);i.size=len(b);i.mode=0o644;i.mtime=0;arc.addfile(i,io.BytesIO(b))
save(D/'replay-evidence.json',{'archive':dig((D/'replay-evidence.tar.xz').read_bytes()),'files':evidence});(D/'root-assessment.md').write_text(assessment)
E.mkdir();checks=[]
def run(name,cmd,cwd,env=None):
 r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=900);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,(name,r.stdout.decode()[-2000:],r.stderr.decode()[-2000:]);return r.stdout
run('private-stage',[py,'-I','-B',str(U/'stage.py'),'--architecture',str(A),'--product',str(L),'--output',str(P)],A)
assent=M/'native-runtime-selection-v36-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'native-runtime-selection-v36','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(S),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==35 and len(lock['contractSuccessors'])==57
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(S),'review':pin(D/'review.json'),'assent':pin(assent)});new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
r=json.loads(run('private-design',[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)],P));assert r['passed']and len(r['contractSuccessors'])==58
baseline=json.loads((U/'baseline.json').read_bytes())['files'];mapping=json.loads((U/'materialization-map.json').read_bytes())['files'];assert len(mapping)==2
assert {r['productPath'] for r in mapping}=={'crates/security/src/trust/retained_metadata_index.rs','crates/security/src/trust/retained_metadata_index_tests.rs'}
for b in baseline:verify(L,b)
for row in mapping:
 assert row['before']is not None;verify(P,{'path':row['productPath'],**row['after']});(E/('before-'+Path(row['productPath']).name)).write_bytes((L/row['productPath']).read_bytes())
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new)
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
for row in mapping:(L/row['productPath']).write_bytes((P/row['productPath']).read_bytes())
assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
source_rows=[{**r,'path':r['path'][8:]}for r in json.loads((F/'subject.json').read_bytes())['files']if r['path'].startswith('product/')and r['path']!='product/design-lock.json'];assert len(source_rows)==591
for r in source_rows:verify(L,r)
r=json.loads(run('live-design',[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],L));assert r['passed']and len(r['contractSuccessors'])==58
for parent in (L,*L.parents):assert not any((parent/'.cargo'/n).exists()for n in ['config','config.toml'])
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());env['CARGO_TARGET_DIR']=str(T/'runtime36-live-check-target');env['RUST_TEST_THREADS']='1';assert not Path(env['CARGO_TARGET_DIR']).exists();save(E/'environment.json',env)
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
run('live-scope-tests',[cargo,'test','--locked','--offline','-p','opensip-security','--lib','budget_scope_'],L,env)
run('live-cargo-check',[cargo,'check','--locked','--offline','--workspace','--all-targets'],L,env)
for r in source_rows:verify(L,r)
assert(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'passed':True,'inventorySuccessors':35,'contractSuccessors':58,'mappedFiles':2,'unchangedNonLockFiles':589,'finalSourceNonLockFilesVerified':591,'independentReview':pin(D/'review.json'),'checks':checks,'fullM2Complete':False,'productQualification':False,'standing':'Actual Claude Opus5 source/formal review and root assent, exact materialization and macOS development checks only. Existing trust scope failure closure is not shared creator precharge, native custody, current authority or creation qualification.'});(E/'selection.py').write_bytes(Path(__file__).read_bytes());save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus5 (Herdr observed)','rootSubstantiveAssent':True,'selected':True});print('PASS runtime36 selected35/58;2mapped589unchanged591nonlockverified;no commit/push')
