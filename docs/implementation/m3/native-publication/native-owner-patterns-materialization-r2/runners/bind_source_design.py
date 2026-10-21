"""Publish/bind only independently accepted pure source selection."""
from pathlib import Path
import json,hashlib,shutil,subprocess,os,copy
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'source-design-r1';S=B/'architecture';Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-patterns-source-r1')
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PRE='docs/implementation/m3/native-publication/native-owner-patterns-source-r1';RP='docs/implementation/m3/reviews/codex-native-owner-patterns-source-r1';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(r,*args):return subprocess.check_output(['/usr/bin/git','-c','user.name=sfbreen','-c','user.email=sfbreen@hotmail.com',*args],cwd=r,env=E,text=True).strip()
def pin(root,p):
 b=(root/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
s=json.loads((B/'prepared.json').read_text());v=json.loads((Q/'review.json').read_text());a=json.loads((B/'lead-assent.json').read_text())
assert v['verdict']=='ACCEPT-DESIGN-UNIT' and not v['requiredFindings'] and v['subjectManifestSha256']==s['subjectManifest']['sha256']
assert a['rootSubstantiveAssent'] and a['subjectManifestSha256']==s['subjectManifest']['sha256'] and a['independentReview']==pin(Q,'review.json')
assert [r['id'] for r in v.get('nonBlockingObservations',[])]==[r['observation'] for r in a['observationDispositions']]
assert git(P,'rev-parse','HEAD')==s['productBase'] and git(A,'rev-parse','HEAD')==s['architectureBase']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD') and not git(A,'diff','--cached','--name-only')
drafts=git(A,'ls-files','--others','--exclude-standard');product_paths_before=git(P,'ls-files')
assert pin(S,s['subjectManifest']['path'])==s['subjectManifest'];manifest=json.loads((S/s['subjectManifest']['path']).read_text())
for r in manifest['files']:assert pin(S,r['path'])==r
for r in s['parents']:assert pin(A,r['path'])==r
paths=[]
for r in manifest['files']+[s['subjectManifest']]:
 dst=A/r['path'];assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['path'],dst);paths.append(r['path'])
for src in Q.iterdir():
 assert src.is_file();dst=A/RP/src.name;assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);paths.append(RP+'/'+src.name)
unit_path=PRE+'-unit.json'
write(A/unit_path,dict(schemaVersion=1,unit=s['unit'],status='ACCEPTED-DESIGN-UNIT',rootSubstantiveAssent=True,subjectManifest=s['subjectManifest'],independentReview=pin(A,RP+'/review.json'),acceptedSuccessor=s['record'],requiredUnitFindings=[],observationDispositions=a['observationDispositions'],rootAssessment=a['rootAssessment'],sourcePatternChanges=35,generatorSources=43,admissionSources=52,aliases=15,materializationCodeAccepted=False,generatorExecuted=False,blindRefreshComplete=False,productQualification=False,entirePlanComplete=False));paths.append(unit_path)
old=json.loads((P/'design-lock.json').read_text());future=copy.deepcopy(old);assert len(old['contractSuccessors'])+1==s['prospectiveContractSuccessor']==179
future['contractSuccessors'].append(dict(record=s['record'],subjectManifest=s['subjectManifest'],review=pin(A,RP+'/review.json'),assent=pin(A,unit_path)))
for k in old:
 if k!='contractSuccessors':assert future[k]==old[k]
FL=B/'design-lock.source-selection.json';write(FL,future)
cmd=[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(P),'--lock',str(FL)]
r=subprocess.run(cmd,cwd=P,env=E,capture_output=True);(B/'verify-design-precommit.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0 and json.loads(r.stdout)['passed']
git(A,'add','--',*paths);assert set(git(A,'diff','--cached','--name-only').splitlines())==set(paths);git(A,'commit','-m','Select reviewed native-owner pattern source corrections without accepting materialization.');arch=git(A,'rev-parse','HEAD')
shutil.copyfile(FL,P/'design-lock.json');cmd[-1]=str(P/'design-lock.json')
r=subprocess.run(cmd,cwd=P,env=E,capture_output=True);(B/'verify-design-before-lock-commit.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0 and json.loads(r.stdout)['passed']
assert git(P,'diff','--name-only')=='design-lock.json';git(P,'add','--','design-lock.json');assert git(P,'diff','--cached','--name-only')=='design-lock.json';git(P,'commit','-m','Bind native-owner selected-source design as contract successor 179.');head=git(P,'rev-parse','HEAD')
assert not git(P,'status','--porcelain') and git(P,'ls-files')==product_paths_before and not git(A,'diff','--name-only','HEAD') and git(A,'ls-files','--others','--exclude-standard')==drafts
report=dict(unit=s['unit'],productLock=head,architecture=arch,subjectManifest=s['subjectManifest'],record=s['record'],review=pin(A,RP+'/review.json'),contractSuccessorsAfter=179,inventoryUnchanged=233,inventorySuccessorsUnchanged=len(old['inventorySuccessors']),inheritanceRowsUnchanged=len(old['inventoryPassageInheritance']),verifyDesignPassed=True,productCodeChanged=False,materializationCodeAccepted=False,generatorExecuted=False,blindRefreshComplete=False,productQualification=False,entirePlanComplete=False,pushed=False)
write(B/'integration.json',report);state=json.loads((C/'CURRENT-STATE.json').read_text());state.update(productHead=head,architectureHead=arch,boundContractSuccessorCount=179,contractSuccessorCount=179,pushed=False,sharedStatusReconciliationOwed='Native-owner pure source selection contract179 accepted/bound; code materialization/generator/owning and immediate reviewed blind refresh still owed.');state['NativeOwnerSourceSelectionBound']=report;write(C/'CURRENT-STATE.json',state)
shutil.copytree(B,C/'continuation-preserved/native-owner-patterns-source-r1',dirs_exist_ok=True);shutil.copytree(Q,C/'continuation-preserved/reviews/codex-native-owner-patterns-source-r1',dirs_exist_ok=True);print(json.dumps(report,indent=2))
