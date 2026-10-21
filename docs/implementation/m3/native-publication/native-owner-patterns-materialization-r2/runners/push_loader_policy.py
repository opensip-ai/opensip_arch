from pathlib import Path
import os,json,subprocess,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'loader-policy-design-r1';I=json.loads((B/'integration.json').read_text());P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT'):E.pop(key,None)
def git(root,*a):return subprocess.check_output(['/usr/bin/git','-C',str(root),*a],env=E,text=True).strip()
assert git(P,'rev-parse','HEAD')==I['productLock'] and git(A,'rev-parse','HEAD')==I['architecture'] and not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD')
rows=[]
for root,key in ((A,'architecture'),(P,'productLock')):
 subprocess.run(['/usr/bin/git','-C',str(root),'push','origin','main'],env=E,check=True)
 remote=git(root,'ls-remote','origin','refs/heads/main').split()[0];assert remote==I[key]
 rows.append(dict(repository=str(root),head=remote,remoteVerified=True))
report=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),repositories=rows,sourceDesignOnly=True,completeMaterializationAccepted=False)
(B/'push.json').write_text(json.dumps(report,indent=2)+'\n')
p=C/'CURRENT-STATE.json';d=json.loads(p.read_text());d['NativeOwnerGeneratorLoaderPolicyBound']=dict(I,pushed=True);d['currentExecution']['pushed']=True;d['pushed']=True;p.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(report,indent=2))
