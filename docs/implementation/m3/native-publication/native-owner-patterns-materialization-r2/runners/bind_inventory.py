"""Bind the reviewed additive inventory successor for NATIVE-OWNER-MATERIALIZATION (codex-native-owner-inventory-v{N}-r1, N from the lock at run time):
the architecture record (stage copy, the review, root assent), then the lock commit appending the successor and
re-pointing every inherited passage row to v{N}, with verify_design before each. Run through lead_locked_run.py, which
holds the lane lock (OPENSIP_LEAD_HOLDS_LANE_LOCK=1). The architecture head may have advanced past the prepare's by
unrelated publications: it must descend from it, and no moved path may be an inventory, this unit's or the parent's.
Untracked files other work added are preserved, and only this unit's own paths must leave the untracked set. The
successor counts are the prepare's, from the lock, re-checked against the lock on main. OWNPAT_INV_DRY_CHECK=1 checks the
preconditions only (the review need not exist yet). No pushes. (Adapted from integrate_v227.py.)"""
import json as _json
from pathlib import Path as _Path
# The successor's number follows the lock's last bound inventory successor (another unit may bind first).
_LOCK = _json.loads((_Path('/Users/sb/code/opensip-ai/opensip') / 'design-lock.json').read_bytes())
_LAST = _LOCK['inventorySuccessors'][-1]['candidate']['path']
PARENT_N = int(_LAST.rsplit('.v', 1)[1].split('.')[0])
COUNT = len(_LOCK['inventorySuccessors'])
N = PARENT_N + 1  # the successor this binds
from pathlib import Path
import json,hashlib,subprocess,os,shutil,copy,re
CHECK=os.environ.get('OWNPAT_INV_DRY_CHECK')=='1'
B=Path('/tmp/opensip-implementation/native-owner-patterns-2026-10-20/inventory');S=B/'architecture';Q=Path(f'/tmp/opensip-implementation/reviews/codex-native-owner-inventory-v{N}-r1');P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-c','user.name=sfbreen','-c','user.email=sfbreen@hotmail.com',*args],cwd=root,env=env).decode().strip()
def pin(root,rel):
 raw=(root/rel).read_bytes();return dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
prepared=json.loads((B/'prepared.json').read_text());assert prepared['inventoryNumber']==N and prepared['reviewDirectory']==str(Q)
counts=prepared['expectedCounts'];assert counts['inventorySuccessorsBefore']==COUNT
SD='docs/implementation/m3/native-publication/'
for row in json.loads((A/prepared['acceptedUnit']['productMap']).read_bytes())['rows']:assert pin(P,row['path'])==row['candidate'],row['path']
assert len(prepared['addedFiles'])==15 and all('.native-owner-r1.' in p for p in prepared['addedFiles'])
lane=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');assert CHECK or os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1','a lane holds the lock'
assert git(P,'rev-parse','HEAD')==prepared['productHead']==prepared['productCode']
# Architecture may advance by unrelated publications; never over this unit's paths, the parent or an inventory.
assert subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',prepared['architectureHead'],'HEAD'],cwd=A,env=env).returncode==0
moved=set(git(A,'diff','--name-only',prepared['architectureHead'],'HEAD').split());assert not any('repository-file-inventory' in x or f'native-owner-inventory-v{N}' in x for x in moved) and prepared['parent']['path'] not in moved,moved
assert git(P,'status','--porcelain')=='' and git(A,'diff','--name-only')=='' and git(A,'diff','--cached','--name-only')=='';untracked=git(A,'ls-files','--others','--exclude-standard')
for row in [prepared['parent']]:assert pin(A,row['path'])==row
manifest=json.loads((S/prepared['subjectManifest']['path']).read_text());assert len(manifest['files'])==3
for row in [*manifest['files'],prepared['subjectManifest']]:assert pin(S,row['path'])==row
if CHECK:
 print(json.dumps({'dryCheck':'passed','inventory':N,'productMain':prepared['productHead'],'architectureAdvancedSincePrepare':sorted(moved),'reviewPresent':(Q/'review.json').exists(),'laneLockHeld':lane.exists()},indent=2));raise SystemExit(0)
review=json.loads((Q/'review.json').read_text());assessment=review['inventoryCandidateAssessment']
assert review['verdict']=='ACCEPT-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==prepared['subjectManifest']['sha256'] and review['productQualification'] is False
assert assessment['verdict']=='ACCEPT' and assessment['requiredFindings']==[] and assessment['parent']==prepared['parent'] and assessment['successorRecord']==prepared['record']
assert all(assessment[k]==prepared['candidate'][k]for k in ['path','bytes','sha256'])
assent=json.loads((B/'lead-assent.json').read_text());assert assent['rootSubstantiveAssent'] and assent['subjectManifestSha256']==prepared['subjectManifest']['sha256'] and assent['independentReview']==pin(Q,'review.json')
assert [r['id'] for r in review.get('nonBlockingObservations',[])]==[r['observation'] for r in assent['observationDispositions']]
assert (Q/'REVIEW.md').exists() and (Q/'review.json').exists()
rp=f'docs/implementation/m3/reviews/codex-native-owner-inventory-v{N}-r1';assentrel=SD+f'native-owner-inventory-v{N}-unit.json'
owned_paths={r['path']for r in manifest['files']}|{prepared['subjectManifest']['path'],assentrel}|{rp+'/'+n for n in ['REQUEST.md','subject.json','REVIEW.md','review.json']}
paths=[]
for row in [*manifest['files'],prepared['subjectManifest']]:
 if (A/row['path']).exists():assert pin(A,row['path'])==row
 else:(A/row['path']).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/row['path'],A/row['path'])
 paths.append(row['path'])
for name in ['REQUEST.md','subject.json','REVIEW.md','review.json']:
 rel=rp+'/'+name
 if (A/rel).exists():assert (A/rel).read_bytes()==(Q/name).read_bytes()
 else:(A/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q/name,A/rel)
 paths.append(rel)
write(A/assentrel,dict(schemaVersion=1,unit=f'NATIVE-OWNER-MATERIALIZATION-inventory-v{N}',status='ACCEPTED-UNIT',subjectManifest=prepared['subjectManifest'],subjectManifestSha256=prepared['subjectManifest']['sha256'],independentReview=pin(A,rp+'/review.json'),acceptedInventory=prepared['candidate'],acceptedSuccessor=prepared['record'],rootSubstantiveAssent=True,requiredUnitFindings=[],carriedObservations=assent['observationDispositions'],priorRounds=[],productCode=prepared['productCode'],rootAssessment=assent['rootAssessment'],productionCallerAdded=False,productQualification=False))
paths.append(assentrel)
old=json.loads((P/'design-lock.json').read_text());assert len(old['contractSuccessors'])==counts['contractSuccessors'] and len(old['inventorySuccessors'])==counts['inventorySuccessorsBefore'] and old['inventorySuccessors'][-1]['candidate']==prepared['parent']
future=copy.deepcopy(old);future['inventorySuccessors'].append({'parent':prepared['parent'],'candidate':prepared['candidate'],'record':prepared['record'],'review':pin(A,rp+'/review.json'),'assent':pin(A,assentrel)})
parent=json.loads((A/prepared['parent']['path']).read_text());candidate=json.loads((A/prepared['candidate']['path']).read_text());indices={row['path']:i for i,row in enumerate(candidate['files'])}
for inherited in future['inventoryPassageInheritance']:
 assert inherited['parent']==prepared['parent'];match=re.fullmatch(r'/files/([0-9]+)/description',inherited['selector']['jsonPointer']);assert match
 row=parent['files'][int(match[1])];assert candidate['files'][indices[row['path']]]==row and inherited['before']==row['description']
 inherited['parent']=prepared['candidate'];inherited['selector']['jsonPointer']='/files/'+str(indices[row['path']])+'/description'
assert len(future['inventorySuccessors'])==counts['inventorySuccessorsAfter']
future['inventoryPassageInheritance'].sort(key=lambda entry:(entry['parent']['path'],json.dumps(entry['selector'],sort_keys=True)))
write(B/f'design-lock.native-owner-v{N}.json',future);assert b'SCRATCH'not in(B/f'design-lock.native-owner-v{N}.json').read_bytes()
cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/verify_design.py','--architecture',str(A),'--lock',str(B/f'design-lock.native-owner-v{N}.json')]
r=subprocess.run(cmd,cwd=P,env=env,capture_output=True,check=True);(B/'verify-design-precommit.log').write_bytes(r.stdout)
git(A,'add','--',*paths);assert sorted(git(A,'diff','--cached','--name-only').splitlines())==sorted(paths);git(A,'commit','-m',f'Record the accepted additive inventory v{N} (the current native-owner synthetic companions and metadata).');archhead=git(A,'rev-parse','HEAD')
assert git(P,'status','--porcelain')=='';shutil.copyfile(B/f'design-lock.native-owner-v{N}.json',P/'design-lock.json');cmd[-1]=str(P/'design-lock.json');r=subprocess.run(cmd,cwd=P,env=env,capture_output=True,check=True);(B/'verify-design-before-lock-commit.log').write_bytes(r.stdout)
assert git(P,'diff','--name-only')=='design-lock.json';git(P,'add','--','design-lock.json');assert git(P,'diff','--cached','--name-only')=='design-lock.json';git(P,'commit','-m',f'Bind reviewed additive inventory v{N} (the current native-owner synthetic companions and metadata).');producthead=git(P,'rev-parse','HEAD')
assert git(P,'status','--porcelain')=='' and git(A,'diff','--name-only')=='' and git(A,'diff','--cached','--name-only')=='' and not (set(git(A,'ls-files','--others','--exclude-standard').splitlines())&owned_paths)
report={'unit':f'NATIVE-OWNER-MATERIALIZATION-inventory-v{N}','productCode':prepared['productCode'],'productLock':producthead,'architecture':archhead,'inventory':prepared['candidate'],'subjectManifest':prepared['subjectManifest'],'review':pin(A,rp+'/review.json'),'inventorySuccessorsAfter':counts['inventorySuccessorsAfter'],'contractSuccessors':counts['contractSuccessors'],'inheritedPassageRows':len(future['inventoryPassageInheritance']),'addedFiles':15,'realizedPlannedFiles':[],'architectureAdvancedSincePrepare':sorted(moved),'packagesUnchanged':True,'pendingDecisionsUnchanged':True,'verifyDesignPassed':True,'productionCallerAdded':False,'productQualification':False,'pushed':False};write(B/'integration.json',report);write(Path(f'/tmp/opensip-implementation/native-owner-inventory-v{N}-integration.json'),dict(report,lockCommit=producthead))
state=json.loads((C/'CURRENT-STATE.json').read_text());state.update(productHead=producthead,architectureHead=archhead,boundInventory=N,nextInventory=N+1);state[f'NativeOwnerInventoryV{N}Bound']=report;write(C/'CURRENT-STATE.json',state);p=C/'ACTIVE-PLAN.md';p.write_text(f'2026-10-21: inventory v{N} (NATIVE-OWNER-MATERIALIZATION) bound: lock '+producthead+', ARCH '+archhead+' ('+str(counts['inventorySuccessorsAfter'])+' inventory successors, '+str(counts['contractSuccessors'])+' contracts).\n\n'+p.read_text());shutil.copytree(B,C/f'continuation-preserved/native-owner-inventory-v{N}',dirs_exist_ok=True);shutil.copytree(Q,C/f'continuation-preserved/reviews/codex-native-owner-inventory-v{N}-r1',dirs_exist_ok=True);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name);print(json.dumps(report))
