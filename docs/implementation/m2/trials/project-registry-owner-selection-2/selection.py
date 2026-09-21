"""Select exact reviewed registry owner v2; changes only product design-lock."""
from pathlib import Path
import hashlib,json,subprocess,tarfile,io,shutil,argparse
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';T=Path('/tmp/opensip-implementation');M=A/'docs/implementation/m2';U=M/'project-registry-owner-selection-v2';R=T/'reviews/grok-registry-owner-v2-20260921-r1';D=M/'reviews'/R.name;E=M/'trials/project-registry-owner-selection-2';private=T/'registry-selection-private381'
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--review-sha256',required=True);parser.add_argument('--root-assessment',type=Path,required=True);args=parser.parse_args()
assessment=args.root_assessment.read_text().strip();assert len(assessment)>100
assert not D.exists() and not E.exists() and not private.exists()
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**digest(p.read_bytes())}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
manifest=M/'project-registry-owner-selection-v2-subject.json';assert digest(manifest.read_bytes())['sha256']=='abfa0cf16ec8f1439b8443612c25aec467e20b4587baab3e9c45f81cac659f0e'
for r in json.loads(manifest.read_text())['files']:assert digest((A/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert digest((R/'review.json').read_bytes())['sha256']==args.review_sha256
review=json.loads((R/'review.json').read_text());assert review['verdict']=='ACCEPT-DESIGN-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pin(manifest)['sha256']
assert subprocess.check_output(['git','status','--porcelain','-z'],cwd=P)==b''
old=(P/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==33 and len(lock['contractSuccessors'])==48
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=P).split(b'\0');baseline=[]
for path in tracked:
 if not path:continue
 path=path.decode();b=(P/path).read_bytes();baseline.append({'path':path,**digest(b)})
assert len(baseline)==587
D.mkdir(parents=True);E.mkdir(parents=True);private.mkdir()
# Preserve exact full reports, including any addendum. Replay trees stay at their explicit location.
for n in ('REVIEW.md','review.json','ADDENDUM.md'):
 if (R/n).exists():shutil.copy2(R/n,D/n)
save(D/'evidence-location.json',{'actualReviewer':'Grok via Herdr wN:p1','originalReviewDirectory':str(R),'scope':'Exact formal owner-v2 selection review. No claim of native runtime qualification.'})
(D/'root-assessment.md').write_text(assessment+'\n')
assent=M/'project-registry-owner-selection-v2-unit.json';assert not assent.exists();save(assent,{'schemaVersion':1,'unit':'project-registry-owner-selection-v2','status':'ACCEPTED-DESIGN-UNIT','subjectManifest':pin(manifest),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedSuccessor':pin(U/'successor.json'),'rootAssessment':assessment,'fullM2Complete':False,'productQualification':False})
lock['contractSuccessors'].append({'record':pin(U/'successor.json'),'subjectManifest':pin(manifest),'review':pin(D/'review.json'),'assent':pin(assent)})
new=(json.dumps(lock,indent=2)+'\n').encode();(private/'design-lock.json').write_bytes(new)
py=T/'source-audit364-env/bin/python';checks=[]
def check(name,lockfile):
 cmd=[str(py),'-I','-B',str(P/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(P),'--lock',str(lockfile)]
 r=subprocess.run(cmd,cwd=P,capture_output=True);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});save(E/'checks.json',checks);assert r.returncode==0,r.stderr.decode();value=json.loads(r.stdout);assert value['passed'] and len(value['inventorySuccessors'])==33 and len(value['contractSuccessors'])==49;return value
check('private-design',private/'design-lock.json')
for r in baseline:assert digest((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
(E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);save(E/'baseline.json',{'standing':'All587tracked product files verified before selection; only lock may change','files':baseline})
assert (P/'design-lock.json').read_bytes()==old;(P/'design-lock.json').write_bytes(new)
check('live-design',P/'design-lock.json')
for r in baseline:
 if r['path']!='design-lock.json':assert digest((P/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert subprocess.check_output(['git','diff','--name-only'],cwd=P).decode().splitlines()==['design-lock.json']
save(E/'receipt.json',{'standing':'Formal registry owner selected after actual review/root assent/private+live validation; no source/runtime or qualification claim','inventorySuccessors':33,'contractSuccessors':49,'unchangedProductNonLockFiles':586,'lock':digest(new),'checks':checks,'fullM2Complete':False,'productQualification':False})
shutil.copy2(Path(__file__),E/'selection.py');print('PASS registry design33/49;586non-lock files unchanged',digest(new))
