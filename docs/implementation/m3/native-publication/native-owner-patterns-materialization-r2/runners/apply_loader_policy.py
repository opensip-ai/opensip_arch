from pathlib import Path
import os,json,hashlib,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'loader-policy-design-r1';I=json.loads((B/'integration.json').read_text());P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-native-owner-patterns-takeover'
def git(root,*a):return subprocess.check_output(['/usr/bin/git','-C',str(root),*a],text=True).strip()
assert I['contractSuccessorsAfter']==181 and I['verifyDesignPassed'];assert git(P,'rev-parse','HEAD')==I['productLock'] and git(A,'rev-parse','HEAD')==I['architecture']
L=json.loads((P/'design-lock.json').read_text());assert L['contractSuccessors'][-1]['subjectManifest']==I['subjectManifest']
assert git(W,'rev-parse','HEAD')=='19549dcb29c1e2c77f53419f18db8d0c451259aa';assert git(P,'diff','--name-only',git(W,'rev-parse','HEAD'),'HEAD')=='design-lock.json'
source=json.loads((F/'companion-focused-r5/report.json').read_text());assert source['allPassed']
for p,h in source['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h,p
subprocess.run(['/usr/bin/git','-C',str(W),'checkout','-q','--detach',I['productLock']],check=True)
PRE='docs/implementation/m3/native-publication/native-owner-generator-loader-policy-r1';audit=json.loads((A/PRE/'audit.json').read_text());assert len(audit['productMap'])==1
row=audit['productMap'][0];raw=(A/row['candidate']['path']).read_bytes();assert len(raw)==row['candidate']['bytes'] and hashlib.sha256(raw).hexdigest()==row['candidate']['sha256'];(W/row['productPath']).write_bytes(raw)
paths=sorted(git(W,'diff','--name-only').splitlines()+git(W,'ls-files','--others','--exclude-standard').splitlines());assert len(paths)==41
report=dict(productBase=I['productLock'],architecture=I['architecture'],policyDesignBound=True,productPaths=41,newPaths=15,onlyAdditionalPath='tools/typescript-lanes.json',allPrevious40ProductPathsExact=True,sourcePins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths},unitAccepted=False,blindRefreshComplete=False,productQualification=False)
(F/'loader-policy-applied.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(productBase=I['productLock'],productPaths=41,policyDesignBound=True),indent=2))
