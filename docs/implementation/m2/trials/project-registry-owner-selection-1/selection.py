"""Select exact reviewed registry owner v1; changes only product design-lock."""
from pathlib import Path
import hashlib,json,subprocess,tarfile,io,shutil
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';T=Path('/tmp/opensip-implementation');M=A/'docs/implementation/m2';U=M/'project-registry-owner-selection-v1';R=T/'reviews/grok-registry-selection-v1-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/project-registry-owner-selection-1';private=T/'registry-selection-private371'
assert not D.exists() and not E.exists() and not private.exists()
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**digest(p.read_bytes())}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
manifest=M/'project-registry-owner-selection-v1-subject.json';assert digest(manifest.read_bytes())['sha256']=='f0bbdce06f5d5b3332ef4552b6d042a826a7b4f56b40a8c667c4f4d6f2ec8435'
for r in json.loads(manifest.read_text())['files']:assert digest((A/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
review=json.loads((R/'review.json').read_text());assert review['verdict']=='ACCEPT-DESIGN-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pin(manifest)['sha256']
assert subprocess.check_output(['git','status','--porcelain','-z'],cwd=P)==b''
old=(P/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==31 and len(lock['contractSuccessors'])==45
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=P).split(b'\0');baseline=[]
for path in tracked:
 if not path:continue
 path=path.decode();b=(P/path).read_bytes();baseline.append({'path':path,**digest(b)})
assert len(baseline)==583
D.mkdir(parents=True);E.mkdir(parents=True);private.mkdir()
files={p.relative_to(R).as_posix():p.read_bytes() for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
for n in ('REVIEW.md','review.json'):(D/n).write_bytes(files[n])
rows=[{'path':n,**digest(b)} for n,b in sorted(files.items())]
with tarfile.open(D/'subject.tar.xz','w:xz') as tf:
 for n,b in sorted(files.items()):
  h=tarfile.TarInfo(n);h.size=len(b);h.mode=0o644;h.mtime=0;tf.addfile(h,io.BytesIO(b))
save(D/'subject.json',{'standing':'Actual formal registry contract review and replays; not native implementation','files':rows});save(D/'archive-pin.json',{'path':'subject.tar.xz',**digest((D/'subject.tar.xz').read_bytes()),'members':len(rows)})
with tarfile.open(D/'subject.tar.xz') as tf:
 for r in rows:assert digest(tf.extractfile(r['path']).read())=={k:r[k] for k in ('bytes','sha256')}
assessment='Root fully read actual Grok formal REVIEW.md and review.json after DONE, with no addendum or required findings. I accept this exact formal registry contract unit and six effective identity/S7/S9 passage overrides. Owner/schema/model bytes match independently reviewed371r4; historical ProjectId provenance is scoped to named marker/allocation selectors and cannot import old snapshot/plan/registry/lease semantics. I specifically assent to new bounded canonical registry, immutable allocationKind, complete document uniqueness, live-vs-historical identity, RESERVED/ACTIVE/RETIRED/ABANDONED, retained retired-N census, explicit adoption context on every adopt-kind recovery, native birth-identity gate, abandoned-remnant retention and S7 fence-to-lease handoff. The actual reviewer reproduced274cases,24schema checks,320555capacity and eight pure-model faults; initial shadowed history-reuse test failure is preserved honestly. This selects a design contract, not native runtime code or authority. It does not accept S9.3 or full-five-field acquisition, original-time/current-trust completion, writers, OS/Linux/release qualification or M2-M6 completion. No new inventory or dependency edge is selected; source layout/codecs still require their own review. Claude quota refusals are not concurrence.'
assent=M/'project-registry-owner-selection-v1-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'project-registry-owner-selection-v1','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(manifest),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(manifest),'review':pin(D/'review.json'),'assent':pin(assent)})
new=(json.dumps(lock,indent=2)+'\n').encode();(private/'design-lock.json').write_bytes(new)
py=T/'source-audit364-env/bin/python';checks=[]
def check(name,lockfile):
 cmd=[str(py),'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P),'--lock',str(lockfile)]
 r=subprocess.run(cmd,cwd=P,capture_output=True);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,r.stderr.decode();value=json.loads(r.stdout);assert value['passed'] and len(value['inventorySuccessors'])==31 and len(value['contractSuccessors'])==46;return value
check('private-design',private/'design-lock.json')
for r in baseline:assert digest((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);save(E/'baseline.json',{'standing':'All583tracked product files verified before selection; only lock may change','files':baseline})
assert (P/'design-lock.json').read_bytes()==old;(P/'design-lock.json').write_bytes(new)
check('live-design',P/'design-lock.json')
for r in baseline:
 if r['path']!='design-lock.json':assert digest((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert subprocess.check_output(['git','diff','--name-only'],cwd=P).decode().splitlines()==['design-lock.json']
save(E/'receipt.json',{'standing':'Formal registry owner selected after actual review/root assent/private+live validation; no source/runtime or qualification claim','inventorySuccessors':31,'contractSuccessors':46,'unchangedProductNonLockFiles':582,'lock':digest(new),'checks':checks,'fullM2Complete':False,'productQualification':False})
shutil.copy2(Path(__file__),E/'selection.py');print('PASS registry design31/46;582non-lock files unchanged',digest(new))
