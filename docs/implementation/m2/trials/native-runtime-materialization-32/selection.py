"""Apply runtime32 only after root reads and pins an actual accepting review."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';M=A/'docs/implementation/m2';U=M/'native-runtime-selection-v32';T=Path('/tmp/opensip-implementation')
R=T/'reviews/claude-opus5-runtime32-source395-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/native-runtime-materialization-32';P=T/'runtime32-activation/product'
py='/tmp/opensip-implementation/source-audit364-env/bin/python'
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**digest(p.read_bytes())}
def verify(root,r):
 p=root/r['path'];assert not p.is_symlink();assert digest(p.read_bytes())=={k:r[k]for k in ('bytes','sha256')},str(p)
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
args=argparse.ArgumentParser(description=__doc__);args.add_argument('--review-sha256',required=True);args.add_argument('--root-assessment',type=Path,required=True);a=args.parse_args()
root_assessment=a.root_assessment.read_text().strip();assert len(root_assessment)>100
manifest=M/'native-runtime-selection-v32-subject.json';assert pin(manifest)['sha256']=='1de2e8016adb9bc87737b514f5e0c98dc01e6d9c31f6758a0441f8901852e7e5'
for row in json.loads(manifest.read_bytes())['files']:verify(A,row)
assert digest((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==pin(manifest)['sha256']
assert review['sourceAcceptance']['accepted'] is True
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
for line in (R/'hashes.txt').read_text().splitlines():
 if line and not line.startswith('#'):
  sha,n,name=line.split(None,2);assert digest((R/name).read_bytes())=={'bytes':int(n),'sha256':sha}
assert D.is_dir() and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json'}
assert not E.exists()and not P.exists();E.mkdir()
for n in ['REVIEW.md','review.json','ADDENDUM.md']:
 if (R/n).exists():shutil.copy2(R/n,D/n)
save(D/'evidence-location.json',{'actualReviewer':'Claude Opus5 via Herdr wF:p1','originalReviewDirectory':str(R),'scope':'Exact substantive formal source/runtime review. Duplicate staged product and replay working copies remain in original directory; report bytes preserved.'})
checks=[]
def run(name,root,cmd,env=None):
 r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=240);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,(name,r.stderr.decode());return r.stdout
run('fresh-private-stage',A,[py,'-I','-B',str(U/'stage.py'),'--architecture',str(A),'--product',str(L),'--output',str(P)])
assent=M/'native-runtime-selection-v32-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'native-runtime-selection-v32','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(manifest),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(M/'native-runtime-selection-v32/successor.json'),'rootAssessment':root_assessment,'fullM2Complete':False,'productQualification':False})
assert json.loads(assent.read_bytes())['rootAssessment']==root_assessment
shutil.copy2(a.root_assessment,D/'root-assessment.md')
save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus5 via Herdr wF:p1','independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==34 and len(lock['contractSuccessors'])==52
lock['contractSuccessors'].append({'record':pin(M/'native-runtime-selection-v32/successor.json'),'subjectManifest':pin(manifest),'review':pin(D/'review.json'),'assent':pin(assent)})
new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
result=json.loads(run('private-design',P,[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)]));assert result['passed']and len(result['contractSuccessors'])==53
baseline=json.loads((U/'baseline.json').read_bytes())['files'];mapping=json.loads((U/'materialization-map.json').read_bytes())['files']
for row in baseline:verify(L,row)
for row in mapping:
 rel=row['productPath'];verify(P,{'path':rel,**row['after']})
 if row['before']is None:assert not(L/rel).exists()and not(L/rel).is_symlink()
 assert rel!='design-lock.json'
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);before=[]
for row in mapping:
 p=L/row['productPath'];before.append({'path':row['productPath'],'existed':p.exists(),'before':row['before']})
 if p.exists():
  b=E/'before'/row['productPath'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
save(E/'before-state.json',before)
# All candidates, prior files and private selection have passed before live writes.
for row in mapping:
 p=L/row['productPath'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((P/row['productPath']).read_bytes())
assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
source_rows=json.loads((M/'trials/directory-barrier-checkpoint-395/subject.json').read_bytes())['files'];count=0
for row in source_rows:
 if row['path'].startswith('product/')and row['path']!='product/design-lock.json':verify(L,{**row,'path':row['path'][8:]});count+=1
assert count==590
result=json.loads(run('live-design',L,[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)]));assert result['passed']and len(result['inventorySuccessors'])==34 and len(result['contractSuccessors'])==53
# Reuse the verified vendor configuration, not ambient dependency source selection.
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());env['CARGO_TARGET_DIR']=str(T/'runtime32-live-check-target')
for parent in (L,*L.parents):
 assert not any((parent/'.cargo'/n).exists()for n in ['config','config.toml']),'ambient Cargo config at '+str(parent)
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
run('live-cargo-check',L,[cargo,'check','--locked','--offline','--workspace','--all-targets'],env)
for row in source_rows:
 if row['path'].startswith('product/')and row['path']!='product/design-lock.json':verify(L,{**row,'path':row['path'][8:]})
assert(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'schemaVersion':1,'standing':'Actual Claude Opus5 independent source and formal development integration review plus root assent; exact private/live materialization, not release or complete M2.','inventorySuccessors':34,'contractSuccessors':53,'mappedFiles':2,'unchangedNonLockFiles':588,'finalSourceNonLockFilesVerified':590,'authorFresh395DirectoryTests':{'passed':5,'otherPlatformTestsFiltered':110},'historical393AuthorFallbackTest':{'passed':1,'otherPlatformTestsFiltered':114,'rerun395':False},'providerSourcesUnchangedFrom386':True,'providerRebuildClaimed':False,'independentReview':pin(D/'review.json'),'checks':checks,'fullM2Complete':False,'productQualification':False,'sourceQualification':'Development macOS arm64 only. Retained directory barrier primitive only, no switched production caller, original-name/parent/recursive/profile/custody/current authority. Initialization/binding and later milestones remain open.'})
shutil.copy2(Path(__file__),E/'selection.py');print('PASS live runtime32 34/53;2mapped590nonlockverified')
