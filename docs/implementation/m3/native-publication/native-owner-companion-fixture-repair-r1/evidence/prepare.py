"""Prepare the separate one-line product test repair only after receipt integration."""
from pathlib import Path
import os,json,hashlib,subprocess,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'companion-fixture-repair-r1';assert not B.exists()
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-companion-fixture-repair'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,env=E,text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
accepted=json.loads((F/'combined-refresh-r2/postrun-r1/integration.json').read_text())
assert accepted['receiptRefreshComplete'] and accepted['verifyDesignPassed']
assert git(P,'rev-parse','HEAD')==accepted['productCode'] and git(A,'rev-parse','HEAD')==accepted['architecture']
assert not git(P,'status','--porcelain') and not W.exists()
PRE='docs/implementation/m3/native-publication/native-owner-c1b-refresh-postcheck-remedy-r2'
procedure=json.loads((A/(PRE+'-unit.json')).read_text());assert procedure['rootSubstantiveAssent'] and procedure['supplementAuthorized']
manifest=json.loads((A/procedure['subjectManifest']['path']).read_text())
for row in manifest['files']:assert pin(A,row['path'])==row
path='tools/tests/test_snapshot_ledger_census_blind.py';candidate=(A/PRE/'product'/path).read_bytes();parent=(P/path).read_bytes()
needle=b'    paths |= set(model.SESSION_FILES) | {model.WORK_LEDGER} | set(slc.ANCHORED)\n'
assert parent.count(needle)==1 and candidate==parent.replace(needle,b'    paths |= {p for _, p, _ in model.VCS_ANCHORS}\n'+needle)
git(P,'worktree','add','--detach',str(W),accepted['productCode']);assert not git(W,'status','--porcelain')
(W/path).write_bytes(candidate);assert git(W,'diff','--name-only')==path
B.mkdir();report=dict(unit='NATIVE-OWNER-COMPANION-FIXTURE-REPAIR-r1',productBase=accepted['productCode'],architectureBase=accepted['architecture'],worktree=str(W),path=path,parent=pin(P,path),candidate=pin(W,path),acceptedReceiptUnit=accepted['subjectManifest'],syntheticProcedure=procedure['subjectManifest'],sourceChange='one additive VCS_ANCHORS fixture path union; all test bodies unchanged',productQualification=False)
(B/'prepared.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
