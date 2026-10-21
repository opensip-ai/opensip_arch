from pathlib import Path
import os,json,subprocess,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-send-takeover';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
def pin(root,p):b=(root/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
s=json.loads((C/'CURRENT-STATE.json').read_text());r=s['SharedStatusR119'];assert r['pushed']and r['remoteVerified'];ph=git(P,'rev-parse','HEAD');ah=git(A,'rev-parse','HEAD');assert ph==r['productHead']and ah==r['architectureCommit'];assert not git(P,'status','--porcelain')and not git(A,'diff','--name-only','HEAD');assert not W.exists()
lock=json.loads((P/'design-lock.json').read_text());assert len(lock['inventorySuccessors'])==196 and len(lock['contractSuccessors'])==184 and len(lock['inventoryPassageInheritance'])==138
assert pin(A,r['subjectManifest']['path'])==r['subjectManifest']and pin(A,r['review']['path'])==r['review'];v=json.loads((A/r['review']['path']).read_text());assert v['verdict']=='ACCEPT'and not v['requiredFindings']
drafts=git(A,'ls-files','--others','--exclude-standard');subprocess.run(['git','worktree','add','--detach',str(W),ph],cwd=P,check=True);assert git(W,'rev-parse','HEAD')==ph and not git(W,'status','--porcelain')and git(A,'ls-files','--others','--exclude-standard')==drafts
paths=['docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md','docs/implementation/m3/supervisor-d/d2b-4a-r2-unit.json','docs/implementation/m3/supervisor-d/d2b4a-inventory-v236-r1-unit.json','docs/implementation/m3/supervisor-d/d2b4a-descriptions-r1-unit.json']
prepared=dict(standing='UNACCEPTED FULL RUST3 BASE HOST BUILDERS/SCHEDULE/SENDER/PARTICIPANT D2b-4b',productParent=ph,architectureParent=ah,worktree=str(W),cargoTarget=str(F/'target'),selectedLock=pin(P,'design-lock.json'),authorities=[pin(A,p)for p in paths],inventory=236,inventorySuccessors=196,contractSuccessors=184,inheritedMeanings=138,currentDirectMeanings=7,nextInventoryMeaningProjection=145,nextInventory=237,productionCallerAdded=False,baseReceiveAccepted=True,fa2LimScope='Separate4c, no hidden4b claim',source39OrOwnerAdmissionAdded=False,productQualification=False,entireProjectComplete=False)
(F/'PREPARED.json').write_text(json.dumps(prepared,indent=2)+'\n');print(json.dumps(prepared,indent=2))
