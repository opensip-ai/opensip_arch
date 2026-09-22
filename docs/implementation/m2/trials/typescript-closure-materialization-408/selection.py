"""Guarded one-file maintenance binding; actual review/root assessment required."""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,subprocess,sys,shutil,tarfile,io
q=argparse.ArgumentParser();q.add_argument('--root-assessment',required=True,type=Path);a=q.parse_args()
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';L=A.parent/'opensip';T=Path('/tmp/opensip-implementation');U=M/'typescript-closure-selection-v1';S=M/'typescript-closure-selection-v1-subject.json';R=T/'reviews/claude-opus5-typescript408-20260921-r1';D=M/'reviews'/R.name;P=T/'typescript-closure408-selected-product';E=M/'trials/typescript-closure-materialization-408';EXPECTED='62834a7a0c496a65a4df4c53d358a020e2fef99a3dfea6cb308caf008fa35877';py=sys.executable

def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def check(root,row):
 p=root/row['path'];assert p.is_file()and not p.is_symlink();b=p.read_bytes();assert dig(b)=={k:row[k]for k in ('bytes','sha256')};return b
assert dig(S.read_bytes())=={'bytes':1929,'sha256':EXPECTED};subject=json.loads(S.read_bytes());assert len(subject['files'])==9
for row in subject['files']:check(A,row)
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==EXPECTED
assessment=a.root_assessment.read_text();assert len(assessment)>400 and EXPECTED in assessment and dig((R/'review.json').read_bytes())['sha256']in assessment
assert not P.exists()and not E.exists()and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json'}
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
base_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=L,text=True).strip();assert base_head.startswith('7e1e18b')
evidence=[]
for line in (R/'hashes.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 sha,n,name=line.split(maxsplit=2);path=PurePosixPath(name);assert not path.is_absolute()and '..'not in path.parts
 b=(R/name).read_bytes();assert dig(b)=={'bytes':int(n),'sha256':sha}
 if name.startswith('evidence/'):evidence.append({'path':name,**dig(b)})
for name in ('REVIEW.md','review.json','hashes.txt'):(D/name).write_bytes((R/name).read_bytes())
with tarfile.open(D/'replay-evidence.tar.xz','w:xz')as arc:
 for row in evidence:
  b=(R/row['path']).read_bytes();i=tarfile.TarInfo(row['path']);i.size=len(b);i.mode=0o644;i.mtime=0;arc.addfile(i,io.BytesIO(b))
save(D/'replay-evidence.json',{'archive':dig((D/'replay-evidence.tar.xz').read_bytes()),'files':evidence});(D/'root-assessment.md').write_text(assessment)
E.mkdir();P.mkdir();baseline=[]
for name in sorted(subprocess.check_output(['git','ls-files','-z'],cwd=L).decode().split('\0')):
 if not name:continue
 b=(L/name).read_bytes();dest=P/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);shutil.copymode(L/name,dest);baseline.append({'path':name,**dig(b)})
assert len(baseline)==592;save(E/'baseline.json',{'head':base_head,'files':baseline})
row=json.loads((U/'materialization-map.json').read_bytes())['files'][0];target=row['productPath'];assert dig((L/target).read_bytes())==row['before'];assert dig((A/row['candidatePath']).read_bytes())==row['after'];(P/target).write_bytes((A/row['candidatePath']).read_bytes())
assent=M/'typescript-closure-selection-v1-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'typescript-closure-selection-v1','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(S),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==35 and len(lock['contractSuccessors'])==55
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(S),'review':pin(D/'review.json'),'assent':pin(assent)});new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
checks=[]
def run(name,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=900);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,(name,r.stdout.decode()[-2500:],r.stderr.decode()[-1500:]);return r.stdout
r=json.loads(run('private-design',[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)],P));assert r['passed']and len(r['contractSuccessors'])==56
filled=[]
for registry in ('tools/typescript-lanes.json','tools/contracts/generator-closure.json'):
 for dep in json.loads((P/registry).read_bytes())['files']:
  dest=P/dep['path']
  if not dest.exists():
   b=check(L,dep);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);shutil.copymode(L/dep['path'],dest);filled.append(dep['path'])
  check(P,dep)
save(E/'copied-ignored-dependencies.json',{'files':filled,'exactPinsVerified':True,'packageInstall':False})
node='/Users/sb/.nvm/versions/node/v24.16.0/bin/node';cmd=[py,'-I','-B',str(P/'tools/check_typescript.py'),'--root',str(P),'--architecture',str(A),'--node',node]
raw=run('private-selected-typescript',cmd,P);result=json.loads(raw.decode().splitlines()[-1]);assert result['passed']and len(result['lanes'])==3
for b in baseline:check(L,b)
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);(E/'before-typescript-lanes.json').write_bytes((L/target).read_bytes())
(L/target).write_bytes((P/target).read_bytes());assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
r=json.loads(run('live-design',[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],L));assert r['passed']and len(r['contractSuccessors'])==56
r=json.loads(run('live-selected-typescript',[py,'-I','-B',str(L/'tools/check_typescript.py'),'--root',str(L),'--architecture',str(A),'--node',node],L).decode().splitlines()[-1]);assert r['passed']and len(r['lanes'])==3
for b in baseline:
 if b['path']not in {target,'design-lock.json'}:check(L,b)
assert dig((L/target).read_bytes())==row['after']and(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'passed':True,'inventorySuccessors':35,'contractSuccessors':56,'changedProductFilesExcludingLock':[target],'unchangedNonLockFiles':590,'selectedTypeScriptLanes':r,'checks':checks,'standing':'Exact maintenance closure repair and actual selected development lane checks only; no native creator, release or wholeM2 qualification.'});(E/'selection.py').write_bytes(Path(__file__).read_bytes());save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus 5','rootSubstantiveAssent':True,'selected':True});print('PASS408 live35/56;all3selectedTypeScript lanes pass private/live; no commit/push')
