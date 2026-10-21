"""Direct owning verification of the separate test-only repair; no real census mode."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'companion-fixture-repair-r1';prep=json.loads((B/'prepared.json').read_text())
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=Path(prep['worktree']);PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,env=E,text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def guards():
 assert git(P,'rev-parse','HEAD')==prep['productBase']==git(W,'rev-parse','HEAD') and git(A,'rev-parse','HEAD')==prep['architectureBase']
 assert not git(P,'status','--porcelain') and pin(P,prep['path'])==prep['parent'] and pin(W,prep['path'])==prep['candidate']
 status=subprocess.check_output(['/usr/bin/git','status','--porcelain','--untracked-files=all'],cwd=W,env=E,text=True)
 assert sorted(line[3:] for line in status.splitlines())==[prep['path']]
guards();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());T=Path(tempfile.mkdtemp(prefix='n-',dir=D));T.chmod(0o700);E['TMPDIR']=str(T);os.setpriority(os.PRIO_PROCESS,0,10)
receipt_files=['crates/security/src/custody/discovery_census.json','crates/security/src/custody/discovery_census_held_out.json','crates/security/src/snapshot_ledger_census.json','crates/security/src/snapshot_ledger_census_held_out.json'];before=[pin(W,p) for p in receipt_files]
out=B/'checks';out.mkdir();rows=[]
for name,cmd,count in [('companion-controls',[PY,'-I','-B',prep['path']],21),('discovery-controls',[PY,'-I','-B','tools/tests/test_discovery_census_blind.py'],25),('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)],None)]:
 r=subprocess.run(cmd,cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(out/(name+'.log')).write_bytes(raw);passed=r.returncode==0
 if count is not None:passed=passed and re.search(rb'Ran '+str(count).encode()+rb' tests\b',raw) is not None and re.search(rb'\nOK\s*$',raw) is not None
 else:passed=passed and json.loads(r.stdout)['passed']
 rows.append(dict(name=name,exitCode=r.returncode,expectedTests=count,passed=passed));print(name,r.returncode,passed,flush=True)
 if not passed:break
if len(rows)==3 and all(x['passed'] for x in rows):
 helper=A/'docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1/evidence/freeze_c1b_refresh.py'
 now=json.loads(subprocess.check_output([PY,'-I','-B',str(helper),'--bindings',str(W),str(A),str(P)],cwd=W,env=E))
 actual={n:json.loads((W/p).read_text())['bindings'] for n,p in [('discovery',receipt_files[1]),('companion',receipt_files[3])]}
 assert now==actual
 rows.append(dict(name='public-current-receipt-bindings-unchanged',passed=True))
guards();assert before==[pin(W,p) for p in receipt_files]
report=dict(unit=prep['unit'],rows=rows,allPassed=len(rows)==4 and all(r['passed'] for r in rows),privateTMPDIR=str(T),privateTMPDIRMode=oct(T.stat().st_mode&0o777),receiptAndCensusPinsUnchanged=before,realBlindInvocations=0,candidate=prep['candidate'],allExistingAssertionsUnchanged=True,productQualification=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['allPassed']
