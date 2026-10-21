from pathlib import Path
import os,subprocess,json,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;S=F/'unit-r1/architecture';Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-materialization-r1');P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-native-owner-patterns-takeover';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');PRE='docs/implementation/m3/native-publication/native-owner-patterns-materialization-r1';RP='docs/implementation/m3/reviews/codex-native-owner-materialization-r1';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(r,*a):return subprocess.check_output(['/usr/bin/git','-c','user.name=sfbreen','-c','user.email=sfbreen@hotmail.com',*a],cwd=r,env=E,text=True).strip()
def pin(r,p):b=(r/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
s=json.loads((Q/'subject.json').read_text());v=json.loads((Q/'review.json').read_text());a=json.loads((F/'lead-assent.json').read_text());assert v['verdict']=='ACCEPT-UNIT' and not v['requiredFindings'] and v['subjectManifestSha256']==s['subjectManifest']['sha256'];assert a['rootSubstantiveAssent'] and a['subjectManifestSha256']==s['subjectManifest']['sha256'] and a['independentReview']==pin(Q,'review.json')
assert [r['id'] for r in v.get('nonBlockingObservations',[])]==[r['observation'] for r in a['observationDispositions']]
assert pin(S,s['subjectManifest']['path'])==s['subjectManifest'];m=json.loads((S/s['subjectManifest']['path']).read_text())
for f in m['files']:assert pin(S,f['path'])==f
assert git(P,'rev-parse','HEAD')==git(W,'rev-parse','HEAD')==s['productBase'] and git(A,'rev-parse','HEAD')==s['architectureBase'];assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD') and not git(A,'diff','--cached','--name-only');drafts=git(A,'ls-files','--others','--exclude-standard')
source=json.loads((S/PRE/'source.json').read_text());assert pin(P,'design-lock.json')==source['productLock']
for root,rows in [(P,source.get('productAuthorities',[])),(A,source['authorities'])]:
 for f in rows:assert pin(root,f['path'])==f
rows=json.loads((S/PRE/'product-map.json').read_text())['rows'];paths=[r['path'] for r in rows];newpaths=[r['path'] for r in rows if r['parent'] is None];assert len(paths)==42 and len(newpaths)==15 and newpaths==source['newPaths']
assert sorted(git(W,'diff','--name-only').splitlines())==sorted(r['path'] for r in rows if r['parent'] is not None) and sorted(git(W,'ls-files','--others','--exclude-standard').splitlines())==sorted(newpaths) and not git(W,'diff','--cached','--name-only')
for r in rows:
 assert pin(W,r['path'])==r['candidate'] and pin(S,r['archived']['path'])==r['archived']
 if r['parent'] is None:assert not (P/r['path']).exists()
 else:assert pin(P,r['path'])==r['parent']
checks=json.loads((S/PRE/'checks-summary.json').read_text());assert checks['completeOwning']['allPassed'] and checks['storageReleaseBoundary']['allPassed']
assert checks['compiledMutants']==14 and checks['originalMutants']['allRestored'] and checks['companionMutants']['restored']
for row in rows:assert row['candidate']['sha256']==checks['completeOwning']['sourcePins'][row['path']]
git(W,'add','--',*paths);assert git(W,'diff','--cached','--name-only').splitlines()==paths;git(W,'commit','-m','Materialize reviewed native-owner schema patterns and current synthetic companions.');code=git(W,'rev-parse','HEAD');assert not git(W,'status','--porcelain');git(P,'merge','--ff-only',code)
for r in rows:assert pin(P,r['path'])==r['candidate']
with (F/'verify-integrated.log').open('wb') as log:r=subprocess.run([PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(P)],cwd=P,env=E,stdout=log,stderr=subprocess.STDOUT)
assert r.returncode==0 and json.loads((F/'verify-integrated.log').read_text())['passed']
add=[]
for f in m['files']+[s['subjectManifest']]:
 dst=A/f['path'];assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/f['path'],dst);add.append(f['path'])
for name in ['REQUEST.md','subject.json','REVIEW.md','review.json']:
 dst=A/RP/name;assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q/name,dst);add.append(RP+'/'+name)
write(A/RP/'lead-assent.json',a);add.append(RP+'/lead-assent.json');u=dict(schemaVersion=1,unit='NATIVE-OWNER-MATERIALIZATION-r1',status='ACCEPTED-UNIT',rootSubstantiveAssent=True,subjectManifest=s['subjectManifest'],subjectManifestSha256=s['subjectManifest']['sha256'],independentReview=pin(A,RP+'/review.json'),requiredFindings=[],nonBlockingObservations=v.get('nonBlockingObservations',[]),observationDispositions=a['observationDispositions'],rootAssessment=a['rootAssessment'],productCode=code,laneBase=s['productBase'],newPaths=newpaths,inventorySuccessorNeeded=True,productionCallerAdded=False,publicApiChanged=False,newDependencies=False,blindRefreshComplete=False,blindReceiptStanding='STALE/PENDING; mandatory immediate reviewed exact-main refresh before census-dependent consumption',carriedObligations=json.loads((S/PRE/'carried-obligations.json').read_text())['obligations'],productQualification=False,entirePlanComplete=False);write(A/(PRE+'-unit.json'),u);add.append(PRE+'-unit.json')
git(A,'add','-f','--',*add);assert set(git(A,'diff','--cached','--name-only').splitlines())==set(add);git(A,'commit','-m','Record independently reviewed native-owner complete materialization unit.');arch=git(A,'rev-parse','HEAD');assert git(A,'ls-files','--others','--exclude-standard')==drafts and not git(A,'diff','--name-only','HEAD')
report=dict(unit='NATIVE-OWNER-MATERIALIZATION-r1',productCode=code,architecture=arch,subjectManifest=s['subjectManifest'],review=pin(A,RP+'/review.json'),newPaths=newpaths,inventorySuccessorNeeded=True,verifyDesignPassed=True,productQualification=False,entirePlanComplete=False,pushed=False);write(F/'integration.json',report);j=json.loads((C/'CURRENT-STATE.json').read_text());j.update(productHead=code,architectureHead=arch,sharedStatusReconciliationOwed='Accepted native-owner materialization integrated; mandatory own15path additive inventory/retained-description qualification and immediate independently reviewed blind refresh before census-dependent continuation; reviewed status/push owed.');j['NativeOwnerMaterializationPublication']=report;write(C/'CURRENT-STATE.json',j);shutil.copytree(S,C/'continuation-preserved/native-owner-materialization-r1-stage');shutil.copytree(Q,C/'continuation-preserved/reviews/codex-native-owner-materialization-r1',dirs_exist_ok=True);print(json.dumps(report,indent=2))
