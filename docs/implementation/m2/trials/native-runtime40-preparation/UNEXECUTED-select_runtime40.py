"""Guarded three-file source430 activation after actual Claude review and root assent."""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,subprocess,shutil,tarfile,io
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';M=A/'docs/implementation/m2';T=Path('/tmp/opensip-implementation');U=M/'native-runtime-selection-v40';F=M/'trials/work-reader-430';R=T/'reviews/claude-opus5-runtime40-source430-r1';D=M/'reviews'/R.name;E=M/'trials/native-runtime-materialization-40';P=T/'runtime40-activation/product';S=M/'native-runtime-selection-v40-subject.json';py=str(T/'source-audit364-env/bin/python')
q=argparse.ArgumentParser();q.add_argument('--root-assessment',type=Path,required=True);q.add_argument('--review-sha256',required=True);a=q.parse_args()
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def verify(root,row):
 p=root/row['path'];assert p.is_file()and not p.is_symlink();assert dig(p.read_bytes())=={k:row[k]for k in ('bytes','sha256')},str(p)
assert dig(S.read_bytes())=={'bytes':2453,'sha256':'b4046feb32fde212812b7557d10898f8aa8b8a4a5febaf4cb846093ef1b1d168'}
for row in json.loads(S.read_bytes())['files']:verify(A,row)
assert dig((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==pin(S)['sha256']
source=review['sourceAcceptance'];assert source['accepted']is True and source['unit']=='work-reader-430'
assert source['archive']['sha256']=='874c6ae3c698c82d61b948384ba5cd14196f12cb261496482d9452c03caa3b3c'and source['archive']['manifestSha256']=='cafaa7cccc839e461e4a5437521a9430f0f154f8419130034fa1612f4f5100a6'
assessment=a.root_assessment.read_text();assert len(assessment)>500 and a.review_sha256 in assessment and pin(S)['sha256']in assessment
assert not E.exists()and not P.exists()and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json'}
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
assert len(snapshots)<1000 and sum(map(len,snapshots.values()))<50*1024*1024,'unexpected build/cache artifacts in reviewer evidence'
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
assent=M/'native-runtime-selection-v40-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'native-runtime-selection-v40','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(S),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==37 and len(lock['contractSuccessors'])==61 and len(lock['inventoryPassageInheritance'])==5
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(S),'review':pin(D/'review.json'),'assent':pin(assent)});new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
r=json.loads(run('private-design',[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)],P));assert r['passed']and len(r['contractSuccessors'])==62 and len(r['inventorySuccessors'])==37
baseline=json.loads((U/'baseline.json').read_bytes())['files'];mapping=json.loads((U/'materialization-map.json').read_bytes())['files'];assert len(mapping)==3
assert {r['productPath'] for r in mapping}=={'crates/platform/src/lib.rs','crates/platform/src/work_reader.rs','crates/platform/tests/work_reader_tests.rs'}
assert sum(row['before'] is None for row in mapping)==2
for b in baseline:verify(L,b)
for row in mapping:
 verify(P,{'path':row['productPath'],**row['after']})
 if row['before']is None:assert not (L/row['productPath']).exists()
 else:(E/('before-'+Path(row['productPath']).name)).write_bytes((L/row['productPath']).read_bytes())
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new)
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
for row in mapping:
 dst=L/row['productPath'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((P/row['productPath']).read_bytes())
assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
source_rows=[{**r,'path':r['path'][8:]}for r in json.loads((F/'subject.json').read_bytes())['files']if r['path'].startswith('product/')and r['path']!='product/design-lock.json'];assert len(source_rows)==595
for r in source_rows:verify(L,r)
r=json.loads(run('live-design',[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],L));assert r['passed']and len(r['contractSuccessors'])==62 and len(r['inventorySuccessors'])==37
for parent in (L,*L.parents):assert not any((parent/'.cargo'/n).exists()for n in ['config','config.toml'])
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());env['CARGO_TARGET_DIR']=str(T/'runtime40-live-check-target');env['RUST_TEST_THREADS']='1';assert not Path(env['CARGO_TARGET_DIR']).exists();save(E/'environment.json',env)
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
run('live-reader-tests',[cargo,'test','--locked','--offline','-p','opensip-platform','--test','work_reader_tests'],L,env)
run('live-ledger-integration-tests',[cargo,'test','--locked','--offline','-p','opensip-platform','--test','work_ledger_tests'],L,env)
run('live-cargo-check',[cargo,'check','--locked','--offline','--workspace','--all-targets'],L,env)
for r in source_rows:verify(L,r)
assert(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'passed':True,'inventorySuccessors':37,'contractSuccessors':62,'mappedFiles':3,'unchangedNonLockFiles':592,'finalSourceNonLockFilesVerified':595,'independentReview':pin(D/'review.json'),'checks':checks,'fullM2Complete':False,'productQualification':False,'standing':'Actual Claude Opus5 source/formal review and root assent, exact materialization and macOS development checks only. Standalone bounded reader accounting does not qualify arbitrary reader internals, allocatorRSS, native error/postcheck composition, custody, current authority or creation.'});(E/'selection.py').write_bytes(Path(__file__).read_bytes());save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus5 (Herdr observed)','rootSubstantiveAssent':True,'selected':True});print('PASS runtime40 selected37/62;3mapped592unchanged595nonlockverified;no commit/push')
