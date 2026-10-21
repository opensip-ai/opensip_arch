from pathlib import Path
import os,json,subprocess,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F;P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');i=json.loads((B/'integration-r3.json').read_text())
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],env=E,text=True).strip()
assert git(P,'rev-parse','HEAD')==i['productCode'] and git(A,'rev-parse','HEAD')==i['architecture'] and not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD') and not git(A,'diff','--cached','--name-only');drafts=git(A,'ls-files','--others','--exclude-standard');rows=[]
for root,key in [(A,'architecture'),(P,'productCode')]:
 assert git(root,'branch','--show-current')=='main';subprocess.run(['/usr/bin/git','-C',str(root),'push','origin','main'],env=E,check=True);remote=git(root,'ls-remote','origin','refs/heads/main').split()[0];assert remote==i[key];rows.append(dict(repository=str(root),head=remote,remoteVerified=True))
assert git(A,'ls-files','--others','--exclude-standard')==drafts
report=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit='CLI-DOCTOR-GUARD-REPAIR-r3',repositories=rows,codeUnitAcceptedRootAssentedIntegrated=True,newPaths=0,inventoryUnchanged=236,contractSuccessorsUnchanged=183,statusReviewOwed=True,productQualification=False);(B/'push-r3.json').write_text(json.dumps(report,indent=2)+'\n');p=C/'CURRENT-STATE.json';d=json.loads(p.read_text());d.update(productHead=i['productCode'],architectureHead=i['architecture'],pushed=True);d['CLIDoctorGuardRepairPush']=report;p.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(report,indent=2))
