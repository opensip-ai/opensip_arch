from pathlib import Path
import os,json,hashlib,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'generator-profile-design-r1';P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-native-owner-patterns-takeover'
I=json.loads((B/'integration.json').read_text());assert I['verifyDesignPassed'] and I['contractSuccessorsAfter']==180
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
def check(path,pin):
 raw=path.read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'];return raw
assert git(P,'rev-parse','HEAD')==I['productLock'] and git(A,'rev-parse','HEAD')==I['architecture']
L=json.loads((P/'design-lock.json').read_text());assert L['contractSuccessors'][-1]['subjectManifest']==I['subjectManifest'] and L['contractSuccessors'][-1]['record']==I['record']
mine=git(W,'rev-parse','HEAD');assert mine=='4f5e8994f1177c97aafbd50af933d4c3be77e49a'
assert git(P,'diff','--name-only',mine,'HEAD')=='design-lock.json'
subprocess.run(['/usr/bin/git','-C',str(W),'checkout','-q','--detach',I['productLock']],check=True)
PRE='docs/implementation/m3/native-publication/native-owner-generator-profile-r1';audit=json.loads((A/PRE/'audit.json').read_text())
for row in audit['helperProductMap']:(W/row['productPath']).write_bytes(check(A/row['candidate']['path'],row['candidate']))
paths=git(W,'diff','--name-only').splitlines();assert len(paths)==15,len(paths)
report=dict(productBase=I['productLock'],architecture=I['architecture'],paths=paths,pins={p:dict(bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest()) for p in paths},realHelperDesignBound=True,unitAccepted=False,blindRefreshComplete=False)
(F/'generator-profile-applied.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
