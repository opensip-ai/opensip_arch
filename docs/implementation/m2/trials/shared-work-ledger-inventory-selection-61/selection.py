"""Select reviewed additive inventory61 only, after root substantive reading."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tarfile,io
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';T=Path('/tmp/opensip-implementation');M=A/'docs/implementation/m2'
U=M/'shared-work-ledger-inventory-v61';R=T/'reviews/claude-opus5-shared-work-inventory61-r1';D=M/'reviews'/R.name;E=M/'trials/shared-work-ledger-inventory-selection-61';private=T/'inventory61-private'
args=argparse.ArgumentParser();args.add_argument('--review-sha256',required=True);args.add_argument('--root-assessment',type=Path,required=True);a=args.parse_args();root_assessment=a.root_assessment.read_text().strip();assert len(root_assessment)>100
assert D.is_dir() and {p.name for p in D.iterdir()}=={'REQUEST.md','status.json'}
assert not E.exists() and not private.exists()
def dig(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p):return dict(path=str(p.relative_to(A)),**dig(p.read_bytes()))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
subject=M/'shared-work-ledger-inventory-v61-subject.json'
assert pin(subject)['sha256']=='1c0a422273576160de49adc83658a5138eeac9688a1102bb7a6350bdbb9908d8'
for r in json.loads(subject.read_text())['files']:assert pin(A/r['path'])==r
assert dig((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_text());assert review['verdict']=='ACCEPT-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pin(subject)['sha256']
record=json.loads((U/'successor.json').read_text());parent=A/record['parent']['path'];candidate=A/record['candidate']['path']
old_inventory=json.loads(parent.read_text());new_inventory=json.loads(candidate.read_text());new_rows={r['path']:r for r in new_inventory['files']}
assert len(old_inventory['files'])==706 and len(new_inventory['files'])==708
assert all(new_rows[r['path']]==r for r in old_inventory['files'])
assert all(new_inventory[k]==old_inventory[k] for k in old_inventory if k not in ('files','standing'))
peer_assessment=review['inventoryCandidateAssessment'];assert peer_assessment['verdict']=='ACCEPT' and peer_assessment['requiredFindings']==[]
assert {k:peer_assessment[k] for k in ('path','bytes','sha256')}==pin(candidate)
assert {k:peer_assessment['parent'][k] for k in ('path','bytes','sha256')}==pin(parent)
assert {k:peer_assessment['successorRecord'][k]for k in ('path','bytes','sha256')}==pin(U/'successor.json')
for line in (R/'hashes.txt').read_text().splitlines():
 if line and not line.startswith('#'):
  sha,n,name=line.split(None,2);base=A if name.startswith('docs/')else R;assert dig((base/name).read_bytes())=={'bytes':int(n),'sha256':sha}
assert subprocess.check_output(['git','status','--porcelain'],cwd=P)==b''
before=(P/'design-lock.json').read_bytes();lock=json.loads(before);assert len(lock['inventorySuccessors'])==35 and len(lock['contractSuccessors'])==58
assert lock['inventorySuccessors'][-1]['candidate']==pin(parent)
effective={}
for r in lock['inventoryPassageInheritance']:
 assert r['parent']==pin(parent);i=int(r['selector']['jsonPointer'].split('/')[2]);effective[old_inventory['files'][i]['path']]=r
for binding in lock['contractSuccessors']:
 for r in json.loads((A/binding['record']['path']).read_bytes())['passageOverrides']:
  if r['parent']==pin(parent):
   i=int(r['selector']['jsonPointer'].split('/')[2]);n=old_inventory['files'][i]['path'];assert n not in effective or effective[n]==r;effective[n]=r
assert len(effective)==5
expected=[];idx={r['path']:i for i,r in enumerate(new_inventory['files'])}
for n,r in sorted(effective.items()):
 i=int(r['selector']['jsonPointer'].split('/')[2]);row=old_inventory['files'][i];assert new_rows[n]==row and row['description']==r['before']
 expected.append({'filePath':n,'parentSelector':r['selector'],'candidateSelector':{'jsonPointer':f"/files/{idx[n]}/description"},'before':r['before'],'effectiveDescription':r['after']})
assert record['descriptionOverrideProjection']==expected and len(expected)==5
baseline=[]
for n in subprocess.check_output(['git','ls-files','-z'],cwd=P).decode().split('\0'):
 if n:baseline.append(dict(path=n,**dig((P/n).read_bytes())))
assert len(baseline)==592
E.mkdir();private.mkdir()
files={p.relative_to(R).as_posix():p.read_bytes() for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
for n in ('REVIEW.md','review.json','hashes.txt'):(D/n).write_bytes(files[n])
rows=[dict(path=n,**dig(b)) for n,b in sorted(files.items())]
with tarfile.open(D/'subject.tar.xz','w:xz') as tf:
 for n,b in sorted(files.items()):
  h=tarfile.TarInfo(n);h.size=len(b);h.mode=0o644;h.mtime=0;tf.addfile(h,io.BytesIO(b))
save(D/'subject.json',dict(standing='Actual additive inventory61 review only',files=rows));save(D/'archive-pin.json',dict(path='subject.tar.xz',**dig((D/'subject.tar.xz').read_bytes()),members=len(rows)))
assent=M/'shared-work-ledger-inventory-v61-unit.json';assert not assent.exists()
save(assent,dict(schemaVersion=1,unit='shared-work-ledger-inventory-v61',status='ACCEPTED-UNIT',subjectManifest=pin(subject),independentReview=pin(D/'review.json'),rootSubstantiveAssent=True,requiredUnitFindings=[],acceptedInventory=pin(candidate),rootAssessment=root_assessment,fullM2Complete=False,productQualification=False))
assert json.loads(assent.read_text())['rootAssessment']==root_assessment and isinstance(root_assessment,str)
(D/'root-assessment.md').write_text(root_assessment+'\n')
save(D/'status.json',{'status':'ACCEPT-UNIT','actualReviewer':'Claude Opus5 via Herdr wH:p6','rootSubstantiveAssent':True,'review':pin(D/'review.json')})
lock['inventorySuccessors'].append(dict(parent=pin(parent),candidate=pin(candidate),record=pin(U/'successor.json'),review=pin(D/'review.json'),assent=pin(assent)))
projected=[{'parent':pin(candidate),'selector':r['candidateSelector'],'before':r['before'],'after':r['effectiveDescription']}for r in expected]
assert len(projected)==5;lock['inventoryPassageInheritance']=sorted(projected,key=lambda r:json.dumps(r['selector'],sort_keys=True))
after=(json.dumps(lock,indent=2)+'\n').encode();(private/'design-lock.json').write_bytes(after);checks=[]
def check(name,path):
 cmd=[str(T/'source-audit364-env/bin/python'),'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P),'--lock',str(path)]
 r=subprocess.run(cmd,capture_output=True);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append(dict(name=name,command=cmd,exitCode=r.returncode));save(E/'checks.json',checks);assert r.returncode==0,r.stderr.decode()
 value=json.loads(r.stdout);assert value['passed'] and len(value['inventorySuccessors'])==36 and len(value['contractSuccessors'])==58 and len(value['inventoryPassageInheritance'])==5
check('private-design',private/'design-lock.json')
for r in baseline:assert dig((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
(E/'before-design-lock.json').write_bytes(before);(E/'after-design-lock.json').write_bytes(after);save(E/'baseline.json',baseline)
(P/'design-lock.json').write_bytes(after);check('live-design',P/'design-lock.json')
for r in baseline:
 if r['path']!='design-lock.json':assert dig((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert subprocess.check_output(['git','diff','--name-only'],cwd=P).decode().splitlines()==['design-lock.json']
save(E/'receipt.json',dict(inventorySuccessors=36,contractSuccessors=58,plannedFiles=708,packages=20,inheritedOverrides=5,unchangedNonLockProductFiles=591,lock=dig(after),checks=checks,scope='Additive layout only; no source/native/full-authority/M2 acceptance'))
(E/'selection.py').write_bytes(Path(__file__).read_bytes());print('PASS36/58,708planned,591nonlockunchanged',dig(after))
