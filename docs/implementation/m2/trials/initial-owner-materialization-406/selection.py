"""Guarded selection; run only after complete actual review and root assessment.

Never invoke on required findings, never push, and never overwrite a prior run.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,subprocess,sys,shutil,tarfile,io
p=argparse.ArgumentParser();p.add_argument('--root-assessment',required=True,type=Path);args=p.parse_args()
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';L=A.parent/'opensip';T=Path('/tmp/opensip-implementation');U=M/'initial-root-binding-owner-selection-v1';S=M/'initial-root-binding-owner-selection-v1-subject.json';R=T/'reviews/claude-opus5-initial-owner406-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/initial-owner-materialization-406';P=T/'initial-owner406-selection-product';G=T/'initial-owner406-selected-generation';py=sys.executable
EXPECTED='45e719a52313aca1427286dd90c09e2b841a5d6e0ee734727cb14dadf0757e32'
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def checked(root,row):
 p=root/row['path'];assert p.is_file()and not p.is_symlink();b=p.read_bytes();assert dig(b)=={k:row[k]for k in ('bytes','sha256')};return b
assessment=args.root_assessment.read_text();assert len(assessment)>=500 and EXPECTED in assessment
assert dig(S.read_bytes())=={'bytes':18865,'sha256':EXPECTED}
subject=json.loads(S.read_bytes());assert len(subject['files'])==82
for row in subject['files']:checked(A,row)
review=json.loads((R/'review.json').read_bytes());assert review['verdict']=='ACCEPT-DESIGN-UNIT'and review['requiredFindings']==[]and review['subjectManifestSha256']==EXPECTED
review_sha=dig((R/'review.json').read_bytes())['sha256'];assert review_sha in assessment
assert (R/'REVIEW.md').stat().st_size>1000
assert not E.exists()and not P.exists()and not G.exists()
assert {p.name for p in D.iterdir()}=={'REQUEST.md','status.json'}
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
base=json.loads((U/'baseline.json').read_bytes());assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=L,text=True).strip()==base['productHead']=='883f9634da5ffc422f07c8ac699a98ffdf7d4338'
assert len(base['files'])==592
for row in base['files']:checked(L,row)
# Verify every original reviewer hash before copying or archiving evidence.
evidence=[]
for line in (R/'hashes.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 sha,n,name=line.split(maxsplit=2);rel=PurePosixPath(name);assert not rel.is_absolute()and '..'not in rel.parts and str(rel)==name
 b=(R/name).read_bytes();assert dig(b)=={'bytes':int(n),'sha256':sha}
 if name.startswith('evidence/'):evidence.append({'path':name,**dig(b)})
assert evidence
for name in ('REVIEW.md','review.json','hashes.txt'):(D/name).write_bytes((R/name).read_bytes())
with tarfile.open(D/'replay-evidence.tar.xz','w:xz')as arc:
 for row in evidence:
  b=(R/row['path']).read_bytes();i=tarfile.TarInfo(row['path']);i.size=len(b);i.mode=0o644;i.mtime=0;arc.addfile(i,io.BytesIO(b))
save(D/'replay-evidence.json',{'archive':dig((D/'replay-evidence.tar.xz').read_bytes()),'files':evidence})
(D/'root-assessment.md').write_text(assessment);E.mkdir();checks=[]
def run(name,cmd,cwd,env=None):
 r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=300);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,(name,r.stderr.decode()[-3000:]);return r.stdout
run('private-stage',[py,'-I','-B',str(U/'stage.py'),'--architecture',str(A),'--product',str(L),'--output',str(P)],A)
assent=M/'initial-root-binding-owner-selection-v1-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'initial-root-binding-owner-selection-v1','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(S),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==35 and len(lock['contractSuccessors'])==54 and len(lock['inventoryPassageInheritance'])==4
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(S),'review':pin(D/'review.json'),'assent':pin(assent)})
new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
r=json.loads(run('private-design',[py,'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P)],P));assert r['passed']and len(r['contractSuccessors'])==55 and len(r['inventorySuccessors'])==35
# Provision only missing ignored generator inputs by exact already reviewed pins.
closure=json.loads((P/'tools/contracts/generator-closure.json').read_bytes());filled=[]
for row in closure['files']:
 target=P/row['path']
 if not target.exists():
  raw=checked(L,row);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);filled.append(row['path'])
 checked(P,row)
assert len(closure['files'])==349
save(E/'private-generator-dependencies.json',{'copiedMissingExactPins':filled,'closureFiles':349,'installedPackages':False})
node='/Users/sb/.nvm/versions/node/v24.16.0/bin/node';generator=str(T/'contracts-generator-rebuild-403/opensip-contract-generator');child='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
result=json.loads(run('selected-public-generator-drift',[py,'-I','-B',str(P/'tools/generate_contracts.py'),'--root',str(P),'--architecture',str(A),'--output',str(G),'--node',node,'--generator',generator,'--python',child],P).decode().splitlines()[-1]);assert result['passed']and result['changed']==[]and not result['write']and result['generatorClosureSelected']
for name in ('selection-result.json','result.json','input-closure.json'):(E/('generation-'+name)).write_bytes((G/name).read_bytes())
# No live mutation until selected preflight and public generation drift both pass.
for row in base['files']:checked(L,row)
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
map=json.loads((U/'materialization-map.json').read_bytes());assert len(map['files'])==12 and len(map['unchanged'])==579
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new)
for row in map['files']:
 path=row['productPath'];assert dig((P/path).read_bytes())==row['after'];backup=E/'before'/path;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes((L/path).read_bytes())
for row in map['files']:(L/row['productPath']).write_bytes((P/row['productPath']).read_bytes())
assert(L/'design-lock.json').read_bytes()==old;(L/'design-lock.json').write_bytes(new)
r=json.loads(run('live-design',[py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],L));assert r['passed']and len(r['contractSuccessors'])==55
for row in map['unchanged']:checked(L,row)
for row in map['files']:assert dig((L/row['productPath']).read_bytes())==row['after']
for row in closure['files']:checked(L,row)
for row in json.loads((G/'result.json').read_bytes())['outputs']:checked(L,row)
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());env['CARGO_TARGET_DIR']=str(T/'initial-owner406-live-target');env['RUST_TEST_THREADS']='1'
for parent in (L,*L.parents):assert not any((parent/'.cargo'/n).exists()for n in ('config','config.toml'))
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
run('live-admission-tests',[cargo,'test','--locked','--offline','-p','opensip-host','--lib','schema_sources::'],L,env)
run('live-workspace',[cargo,'check','--locked','--offline','--workspace','--all-targets'],L,env)
for row in map['unchanged']:checked(L,row)
for row in map['files']:assert dig((L/row['productPath']).read_bytes())==row['after']
assert(L/'design-lock.json').read_bytes()==new
save(E/'receipt.json',{'passed':True,'inventorySuccessors':35,'contractSuccessors':55,'mapped':12,'unchangedNonLock':579,'trackedFiles':592,'inventoryInheritanceRows':4,'effectiveInventoryDescriptions':5,'publicGeneratorDrift':result,'liveInputsMatchAll349ReviewedClosurePins':True,'liveOutputsMatchAll8PublicGeneratedOutputs':True,'checks':checks,'standing':'Actual independent formal/source review plus root assent and exact private/live development integration. No native creator, P0, current authority, fullM2 or platform/release qualification.'})
save(D/'status.json',{'status':'ACCEPT-DESIGN-UNIT','actualReviewer':'Claude Opus 5 via Herdr wF:p1','rootSubstantiveAssent':True,'selected':True,'independentReview':pin(D/'review.json')})
(E/'selection.py').write_bytes(Path(__file__).read_bytes());print('PASS initial owner406 live35/55;12mapped579unchanged;public drift zero; no commit/push performed')
