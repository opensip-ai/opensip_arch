"""Bind only the exact independently accepted native-owner predecessor description contract."""
from pathlib import Path
import os, json, hashlib, shutil, subprocess, copy
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F=Path(__file__).parent; B=F/'descriptions'; S=B/'architecture'
P=Path('/Users/sb/code/opensip-ai/opensip'); A=P.parent/'opensip_arch'
C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-descriptions-r1')
PRE='docs/implementation/m3/native-publication/native-owner-descriptions-r1'
RP='docs/implementation/m3/reviews/codex-native-owner-descriptions-r1'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-c','user.name=sfbreen','-c','user.email=sfbreen@hotmail.com',*args],cwd=root,env=E,text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
s=json.loads((B/'prepared.json').read_text());v=json.loads((Q/'review.json').read_text());a=json.loads((B/'lead-assent.json').read_text())
assert v['verdict']=='ACCEPT-DESIGN-UNIT' and not v['requiredFindings'] and v['subjectManifestSha256']==s['subjectManifest']['sha256']
assert a['rootSubstantiveAssent'] and a['subjectManifestSha256']==s['subjectManifest']['sha256'] and a['independentReview']==pin(Q,'review.json')
assert [x['id'] for x in v.get('nonBlockingObservations',[])]==[x['observation'] for x in a['observationDispositions']]
assert git(P,'rev-parse','HEAD')==s['productHead'] and git(A,'rev-parse','HEAD')==s['architectureHead']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD') and not git(A,'diff','--cached','--name-only')
drafts=git(A,'ls-files','--others','--exclude-standard')
assert pin(S,s['subjectManifest']['path'])==s['subjectManifest']
m=json.loads((S/s['subjectManifest']['path']).read_text());src=json.loads((S/PRE/'source.json').read_text())
assert pin(P,'design-lock.json')==src['productLock'] and pin(A,s['parent']['path'])==s['parent']
for p in src['authorities']:assert pin(A,p['path'])==p
code_map=json.loads((A/'docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2/product-map.json').read_text())
for p in code_map['rows']:assert pin(P,p['path'])==p['candidate']
paths=[]
for row in m['files']+[s['subjectManifest']]:
 assert pin(S,row['path'])==row
 dst=A/row['path'];assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/row['path'],dst);paths.append(row['path'])
for name in ['REQUEST.md','subject.json','REVIEW.md','review.json']:
 dst=A/RP/name;assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q/name,dst);paths.append(RP+'/'+name)
unit_rel=PRE+'-unit.json'
write(A/unit_rel,dict(schemaVersion=1,unit=s['unit'],status='ACCEPTED-DESIGN-UNIT',rootSubstantiveAssent=True,subjectManifest=s['subjectManifest'],independentReview=pin(A,RP+'/review.json'),acceptedSuccessor=s['record'],requiredUnitFindings=[],observationDispositions=a['observationDispositions'],rootAssessment=a['rootAssessment'],productCodeChanged=False,productQualification=False,entirePlanComplete=False));paths.append(unit_rel)
old=json.loads((P/'design-lock.json').read_text());future=copy.deepcopy(old)
assert len(old['contractSuccessors'])==src['contractSuccessorsBefore']
future['contractSuccessors'].append(dict(record=s['record'],subjectManifest=s['subjectManifest'],review=pin(A,RP+'/review.json'),assent=pin(A,unit_rel)))
assert len(future['contractSuccessors'])==s['contractSuccessorAfter']
for k in old:
 if k!='contractSuccessors':assert future[k]==old[k]
fl=B/'design-lock.native-owner-descriptions.json';write(fl,future)
cmd=[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(P),'--lock',str(fl)]
result=subprocess.run(cmd,cwd=P,env=E,capture_output=True);(B/'verify-design-precommit.log').write_bytes(result.stdout+result.stderr)
assert result.returncode==0 and json.loads(result.stdout)['passed']
git(A,'add','--',*paths);assert set(git(A,'diff','--cached','--name-only').splitlines())==set(paths)
git(A,'commit','-m','Record the reviewed native-owner retained-predecessor description qualification successor.');arch=git(A,'rev-parse','HEAD')
shutil.copyfile(fl,P/'design-lock.json');cmd[-1]=str(P/'design-lock.json')
result=subprocess.run(cmd,cwd=P,env=E,capture_output=True);(B/'verify-design-before-lock-commit.log').write_bytes(result.stdout+result.stderr)
assert result.returncode==0 and json.loads(result.stdout)['passed']
assert git(P,'diff','--name-only')=='design-lock.json';git(P,'add','--','design-lock.json');assert git(P,'diff','--cached','--name-only')=='design-lock.json'
git(P,'commit','-m',f'Bind native-owner retained-predecessor description qualification as contract successor {s["contractSuccessorAfter"]}.');head=git(P,'rev-parse','HEAD')
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD') and git(A,'ls-files','--others','--exclude-standard')==drafts
report=dict(unit=s['unit'],productCode=s['productHead'],productLock=head,architecture=arch,subjectManifest=s['subjectManifest'],record=s['record'],review=pin(A,RP+'/review.json'),inventoryUnchanged=int(s['parent']['path'].rsplit('.v',1)[1].split('.')[0]),inventorySuccessorsUnchanged=len(old['inventorySuccessors']),contractSuccessorsAfter=len(future['contractSuccessors']),inheritanceRowsUnchanged=len(old['inventoryPassageInheritance']),passageOverrides=15,verifyDesignPassed=True,closedObligations=['OWNPAT-DESCRIPTIONS'],blindRefreshComplete=False,productCodeChanged=False,productQualification=False,entirePlanComplete=False,pushed=False)
write(B/'integration.json',report)
j=json.loads((C/'CURRENT-STATE.json').read_text());j.update(productHead=head,architectureHead=arch);j['NativeOwnerDescriptionsBound']=report;write(C/'CURRENT-STATE.json',j)
shutil.copytree(B,C/'continuation-preserved/native-owner-descriptions-r1',dirs_exist_ok=True);shutil.copytree(Q,C/'continuation-preserved/reviews/codex-native-owner-descriptions-r1',dirs_exist_ok=True)
print(json.dumps(report,indent=2))
