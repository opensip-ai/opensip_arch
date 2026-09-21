"""Select reviewed additive inventory58 only, after root substantive reading."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tarfile,io
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';T=Path('/tmp/opensip-implementation');M=A/'docs/implementation/m2'
U=M/'shared-store-codecs-inventory-v58';R=T/'reviews/grok-shared-codecs-inventory58-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/shared-store-codecs-inventory-selection-58';private=T/'inventory58-private'
args=argparse.ArgumentParser();args.add_argument('--review-sha256',required=True);args.add_argument('--root-assessment',type=Path,required=True);a=args.parse_args();root_assessment=a.root_assessment.read_text().strip();assert len(root_assessment)>100
assert not D.exists() and not E.exists() and not private.exists()
def dig(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p):return dict(path=str(p.relative_to(A)),**dig(p.read_bytes()))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
subject=M/'shared-store-codecs-inventory-v58-subject.json'
assert pin(subject)['sha256']=='29c55690b025e571e9c778b49bad0b6ec66b32d608cc409d32e47bbe73c679a9'
for r in json.loads(subject.read_text())['files']:assert pin(A/r['path'])==r
assert dig((R/'review.json').read_bytes())['sha256']==a.review_sha256
review=json.loads((R/'review.json').read_text());assert review['verdict']=='ACCEPT-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pin(subject)['sha256']
record=json.loads((U/'successor.json').read_text());parent=A/record['parent']['path'];candidate=A/record['candidate']['path']
old_inventory=json.loads(parent.read_text());new_inventory=json.loads(candidate.read_text());new_rows={r['path']:r for r in new_inventory['files']}
assert len(old_inventory['files'])==701 and len(new_inventory['files'])==705
assert all(new_rows[r['path']]==r for r in old_inventory['files'])
assert all(new_inventory[k]==old_inventory[k] for k in old_inventory if k not in ('files','standing'))
peer_assessment=review['inventoryCandidateAssessment'];assert peer_assessment['verdict']=='ACCEPT' and peer_assessment['requiredFindings']==[]
assert {k:peer_assessment[k] for k in ('path','bytes','sha256')}==pin(candidate)
assert {k:peer_assessment['parent'][k] for k in ('path','bytes','sha256')}==pin(parent)
assert subprocess.check_output(['git','status','--porcelain'],cwd=P)==b''
before=(P/'design-lock.json').read_bytes();lock=json.loads(before);assert len(lock['inventorySuccessors'])==33 and len(lock['contractSuccessors'])==50
assert lock['inventorySuccessors'][-1]['candidate']==pin(parent)
baseline=[]
for n in subprocess.check_output(['git','ls-files','-z'],cwd=P).decode().split('\0'):
 if n:baseline.append(dict(path=n,**dig((P/n).read_bytes())))
assert len(baseline)==587
D.mkdir();E.mkdir();private.mkdir()
files={p.relative_to(R).as_posix():p.read_bytes() for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and (len(p.relative_to(R).parts)==1 or (len(p.relative_to(R).parts)==2 and p.relative_to(R).parts[0] in ('grok-out','evidence')))}
for n in ('REVIEW.md','review.json'):(D/n).write_bytes(files[n])
rows=[dict(path=n,**dig(b)) for n,b in sorted(files.items())]
with tarfile.open(D/'subject.tar.xz','w:xz') as tf:
 for n,b in sorted(files.items()):
  h=tarfile.TarInfo(n);h.size=len(b);h.mode=0o644;h.mtime=0;tf.addfile(h,io.BytesIO(b))
save(D/'subject.json',dict(standing='Actual additive inventory58 review only',files=rows));save(D/'archive-pin.json',dict(path='subject.tar.xz',**dig((D/'subject.tar.xz').read_bytes()),members=len(rows)))
assent=M/'shared-store-codecs-inventory-v58-unit.json';assert not assent.exists()
save(assent,dict(schemaVersion=1,unit='shared-store-codecs-inventory-v58',status='ACCEPTED-UNIT',subjectManifest=pin(subject),independentReview=pin(D/'review.json'),rootSubstantiveAssent=True,requiredUnitFindings=[],acceptedInventory=pin(candidate),rootAssessment=root_assessment,fullM2Complete=False,productQualification=False))
assert json.loads(assent.read_text())['rootAssessment']==root_assessment and isinstance(root_assessment,str)
(D/'root-assessment.md').write_text(root_assessment+'\n')
lock['inventorySuccessors'].append(dict(parent=pin(parent),candidate=pin(candidate),record=pin(U/'successor.json'),review=pin(D/'review.json'),assent=pin(assent)))
indices={r['path']:i for i,r in enumerate(new_inventory['files'])};projected=[]
for override in lock['inventoryPassageInheritance']:
 assert override['parent']==pin(parent);bits=override['selector']['jsonPointer'].split('/');assert bits[1]=='files' and bits[3]=='description'
 old_row=old_inventory['files'][int(bits[2])];assert new_rows[old_row['path']]==old_row
 projected.append({**override,'parent':pin(candidate),'selector':dict(jsonPointer=f"/files/{indices[old_row['path']]}/description")})
assert len(projected)==4;lock['inventoryPassageInheritance']=sorted(projected,key=lambda r:json.dumps(r['selector'],sort_keys=True))
after=(json.dumps(lock,indent=2)+'\n').encode();(private/'design-lock.json').write_bytes(after);checks=[]
def check(name,path):
 cmd=[str(T/'source-audit364-env/bin/python'),'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P),'--lock',str(path)]
 r=subprocess.run(cmd,capture_output=True);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append(dict(name=name,command=cmd,exitCode=r.returncode));save(E/'checks.json',checks);assert r.returncode==0,r.stderr.decode()
 value=json.loads(r.stdout);assert value['passed'] and len(value['inventorySuccessors'])==34 and len(value['contractSuccessors'])==50
check('private-design',private/'design-lock.json')
for r in baseline:assert dig((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
(E/'before-design-lock.json').write_bytes(before);(E/'after-design-lock.json').write_bytes(after);save(E/'baseline.json',baseline)
(P/'design-lock.json').write_bytes(after);check('live-design',P/'design-lock.json')
for r in baseline:
 if r['path']!='design-lock.json':assert dig((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert subprocess.check_output(['git','diff','--name-only'],cwd=P).decode().splitlines()==['design-lock.json']
save(E/'receipt.json',dict(inventorySuccessors=34,contractSuccessors=50,plannedFiles=705,packages=20,inheritedOverrides=4,unchangedNonLockProductFiles=586,lock=dig(after),checks=checks,scope='Additive layout only; no source/native/full-authority/M2 acceptance'))
(E/'selection.py').write_bytes(Path(__file__).read_bytes());print('PASS34/50,705planned,586nonlockunchanged',dig(after))
