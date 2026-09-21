from pathlib import Path
import json,hashlib,shutil,subprocess
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';M=A/'docs/implementation/m2';U=M/'cumulative-native-inventory-v55';R=Path('/tmp/opensip-implementation/reviews/grok-cumulative-native-inventory55-20260921-r1');D=M/'reviews'/R.name;E=M/'trials/cumulative-inventory-selection-55';P=Path('/tmp/opensip-implementation/inventory55-activation/product')
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
manifest=M/'cumulative-native-inventory-v55-subject.json';assert pin(manifest)['sha256']=='8da30746898d2b3f87b79f47147fdfabadc14ea49401a37b8cafd634f57fadcc'
for r in json.loads(manifest.read_text())['files']:assert pin(A/r['path'])==r
review=json.loads((R/'review.json').read_text());assert review['verdict']=='ACCEPT-UNIT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pin(manifest)['sha256']
assert dig((R/'review.json').read_bytes())['sha256']=='9c7d41f5ff5c79d286895db31a35dc49c7603d871ffd3fb639e56adde38f0292'
assert dig((R/'REVIEW.md').read_bytes())['sha256']=='14ef27a6fa190d8355df5d42f936abc22218afa27accd272f763d09650e07bc9'
assert not D.exists() and not E.exists() and not P.exists();shutil.copytree(R,D);E.mkdir();P.mkdir(parents=True)
paths=subprocess.check_output(['git','-C',str(L),'ls-files','-z']).decode().split('\0')[:-1]
baseline=[]
for rel in sorted(paths):
 s=L/rel;assert not s.is_symlink();dst=P/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,dst);baseline.append({'path':rel,**dig(s.read_bytes())})
assert len(baseline)==271;save(E/'baseline.json',baseline)
candidate=M/'repository-file-inventory.v55.json';record=json.loads((U/'successor.json').read_text());parent=A/record['parent']['path'];before=json.loads(parent.read_text());after=json.loads(candidate.read_text());by={r['path']:r for r in after['files']}
assert all(by[r['path']]==r for r in before['files']) and len(after['files'])==697
assert all(before[k]==after[k] for k in before if k not in ('standing','files'))
assert review['inventoryCandidateAssessment']['addedFiles']==record['addedFiles'] and len(record['addedFiles'])==288
assent=M/'cumulative-native-inventory-v55-unit.json'
assert not assent.exists()
save(assent,{'schemaVersion':1,'unit':'cumulative-native-inventory-v55','status':'ACCEPTED-UNIT','subjectManifest':pin(manifest),'independentReview':pin(D/'review.json'),'rootSubstantiveAssent':True,'requiredUnitFindings':[],'acceptedInventory':pin(candidate),'rootAssessment':'Root read complete actual Grok REVIEW and all JSON claims, with all288 added paths compared to frozen successor. Direct selected32 parent preserves409 rows,20package DAG and9pending decisions;697rows account583 frozen368 files and114future. Both extra unselected obligations remain explicitly unresolved outside selected policy. Description overrides project by stable path to7/13/494/561. This accepts additive layout only, not prior33–54 proposals, source/runtime/dependencies, current authority, platform qualification or M2 completion.','fullM2Complete':False,'productQualification':False})
old=(L/'design-lock.json').read_bytes();lock=json.loads(old);assert len(lock['inventorySuccessors'])==30 and len(lock['contractSuccessors'])==44
lock['inventorySuccessors'].append({'parent':pin(parent),'candidate':pin(candidate),'record':pin(U/'successor.json'),'review':pin(D/'review.json'),'assent':pin(assent)})
indices={r['path']:i for i,r in enumerate(after['files'])};projected=[]
for override in lock['inventoryPassageInheritance']:
 assert override['parent']==pin(parent);ptr=override['selector']['jsonPointer'].split('/');assert ptr[1]=='files' and ptr[3]=='description'
 row=before['files'][int(ptr[2])];assert by[row['path']]==row
 projected.append({**override,'parent':pin(candidate),'selector':{'jsonPointer':f"/files/{indices[row['path']]}/description"}})
assert len(projected)==4
lock['inventoryPassageInheritance']=sorted(projected,key=lambda p:json.dumps(p['selector'],sort_keys=True))
new=(json.dumps(lock,indent=2)+'\n').encode();(P/'design-lock.json').write_bytes(new)
py='/tmp/opensip-implementation/source-audit364-env/bin/python';checks=[]
for name,root in [('private',P),('live',L)]:
 if name=='live':
  for r in baseline:assert dig((L/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
  (E/'before-design-lock.json').write_bytes(old);(E/'after-design-lock.json').write_bytes(new);(L/'design-lock.json').write_bytes(new)
 cmd=[py,'-I','-B',str(root/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(root)]
 r=subprocess.run(cmd,capture_output=True,timeout=180);(E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr);checks.append({'name':name,'command':cmd,'exitCode':r.returncode});assert r.returncode==0,r.stderr.decode()
for r in baseline:
 if r['path']!='design-lock.json':assert dig((L/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
save(E/'receipt.json',{'inventorySuccessors':31,'contractSuccessors':44,'plannedFiles':697,'packages':20,'inheritedDescriptionOverrides':4,'onlyLiveProductMutation':'design-lock.json','unchangedRuntimeSources':270,'checks':checks,'scope':'Additive layout only. All cumulative source/runtime/dependency acceptance remains separate. M2–M6 open.'})
shutil.copy2(Path(__file__),E/'selection.py');print('PASS selected inventory55; private/live31/44;270 non-lock files unchanged')
