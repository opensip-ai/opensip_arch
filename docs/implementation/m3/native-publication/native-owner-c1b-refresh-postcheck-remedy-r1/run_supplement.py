"""Proposed supplementary public/synthetic verification only; never run a real blind mode.

One reviewed invocation after independent authorization and root assent. The failed
original postcheck lane is retained. No product/source/receipt/census file is edited.
"""
from pathlib import Path
import os,sys,subprocess,tempfile,time,json,hashlib
EV=Path(__file__).resolve().parent
P=Path('/Users/sb/code/opensip-ai/opensip');LIVE_A=P.parent/'opensip_arch';A=P.parent/'opensip-native-owner-c1b-refresh-architecture';W=P.parent/'opensip-native-owner-c1b-refresh'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
PRE='docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1'
PROPOSAL=json.loads((EV/'FAILURE-AND-PROPOSAL.json').read_text())
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
authorization=json.loads(Path(sys.argv[1]).read_text())
self_pin=authorization['runner'];assert pin(EV,'run_supplement.py')==self_pin
assert authorization['rootSubstantiveAssent'] and authorization['supplementAuthorized']
review_pin=authorization['independentReview'];assert pin(Path('/'),review_pin['path'])==review_pin
review=json.loads(Path(review_pin['path']).read_text());assert review['verdict']=='ACCEPT' and review['supplementAuthorized'] and not review['requiredFindings']
manifest_pin=authorization['subjectManifest'];assert pin(Path('/'),manifest_pin['path'])==manifest_pin
assert manifest_pin['sha256']==review['subjectManifestSha256']
S=Path(authorization['architectureStage']);manifest=json.loads(Path(manifest_pin['path']).read_text())
for row in manifest['files']:assert pin(S,row['path'])==row
for row in manifest['gate']:assert pin(A,row['path'])==row
interpreter=json.loads((A/PRE/'source.json').read_text())['interpreter'];assert pin(Path('/'),interpreter['path'])==interpreter
B=Path(sys.argv[2]);B.mkdir(parents=True)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False
os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='ncb-',dir='/private/tmp'));T.chmod(0o700)
 assert len(os.fsencode(T/'s0123456789ab'))<104
 E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
 E.update(CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,env=E,text=True).strip()
 def guards():
  assert git(A,'rev-parse','HEAD')==manifest['architectureBase']==PROPOSAL['frozenArchitectureBase']
  assert str(A)==PROPOSAL['frozenArchitectureWorktree'] and not git(A,'status','--porcelain','--untracked-files=all')
  assert subprocess.run(['/usr/bin/git','symbolic-ref','-q','HEAD'],cwd=A,env=E,capture_output=True).returncode!=0
  assert Path(git(A,'rev-parse','--path-format=absolute','--git-common-dir'))==Path(git(LIVE_A,'rev-parse','--path-format=absolute','--git-common-dir'))
  assert pin(W,PROPOSAL['verifier']['path'])==PROPOSAL['verifier']==pin(P,PROPOSAL['verifier']['path'])
  assert git(P,'rev-parse','HEAD')==PROPOSAL['productBase']==git(W,'rev-parse','HEAD') and not git(P,'status','--porcelain')
  assert subprocess.run(['/usr/bin/git','symbolic-ref','-q','HEAD'],cwd=W,env=E,capture_output=True).returncode!=0
  assert Path(git(P,'rev-parse','--path-format=absolute','--git-common-dir'))==Path(git(W,'rev-parse','--path-format=absolute','--git-common-dir'))
  status=subprocess.check_output(['/usr/bin/git','status','--porcelain','--untracked-files=all'],cwd=W,env=E,text=True)
  assert sorted(line[3:] for line in status.splitlines())==sorted(r['path'] for r in PROPOSAL['receiptAndCensusPins'])
  for row in PROPOSAL['receiptAndCensusPins']+[PROPOSAL['parentTest']]:assert pin(W,row['path'])==row
  candidate=PROPOSAL['candidateTest'];assert pin(S,candidate['path'])==candidate
  for p in [PROPOSAL['blindRun'],PROPOSAL['failedChecks']]:assert pin(Path('/'),p['path'])==p
  frozen=json.loads((A/PRE/'evidence/frozen-bindings.json').read_text())
  assert frozen['freezeBase']==PROPOSAL['productBase']
  for root,rows in [(P,frozen['tools']),(W,frozen['tools']),(A,frozen['architectureInputs'])]:
   for row in rows:assert pin(root,row['path'])==row
  now=json.loads(subprocess.check_output([PY,'-I','-B',str(A/PRE/'evidence/freeze_c1b_refresh.py'),'--bindings',str(W),str(A),str(P)],cwd=W,env=E))
  assert now==frozen['frozenBindings']
 guards()
 # The candidate differs from the existing public synthetic test in exactly one additive fixture path union.
 parent=(W/PROPOSAL['parentTest']['path']).read_bytes();candidate=(S/PROPOSAL['candidateTest']['path']).read_bytes()
 needle=b'    paths |= set(model.SESSION_FILES) | {model.WORK_LEDGER} | set(slc.ANCHORED)\n'
 assert parent.count(needle)==1 and candidate==parent.replace(needle,b'    paths |= {p for _, p, _ in model.VCS_ANCHORS}\n'+needle)
 # Execute unchanged test assertions using the candidate fixture constructor and the original helper/import root.
 adapter=T/'run_synthetic_companion.py'
 adapter.write_text('''from pathlib import Path
import sys,types,unittest
original=Path(sys.argv[1]);candidate=Path(sys.argv[2])
sys.path.insert(0,str(original.parent))
module=types.ModuleType("supplement_companion_controls");module.__file__=str(original)
sys.modules[module.__name__]=module
exec(compile(candidate.read_bytes(),str(candidate),'exec'),module.__dict__)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
assert suite.countTestCases()==21
result=unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun==21
raise SystemExit(0 if result.wasSuccessful() else 1)
''')
 steps=[('census-tests',[R+'cargo','test','--locked','--offline','-p','opensip-security','--lib','--','snapshot_walk::tests::the_snapshot_census','custody::discovery_census','snapshot_vcs::tests::the_observation_charges_exactly']),('companion-blind-controls',[PY,'-I','-B',str(adapter),str(W/PROPOSAL['parentTest']['path']),str(S/PROPOSAL['candidateTest']['path'])]),('discovery-blind-controls',[PY,'-I','-B','tools/tests/test_discovery_census_blind.py']),('verify-design',[PY,'-I','-B',str(W/PROPOSAL['verifier']['path']),'--architecture',str(A),'--implementation',str(W)])]
 rows=[]
 for name,args in steps:
  with (B/(name+'.log')).open('wb') as log:code=subprocess.run(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT).returncode
  rows.append(dict(name=name,exitCode=code));print(name,code,flush=True)
  if code!=0:break
 guards()
 result=dict(rows=rows,allPassed=len(rows)==4 and all(x['exitCode']==0 for x in rows),standing='INDEPENDENTLY AUTHORIZED PUBLIC/SYNTHETIC POSTCHECK SUPPLEMENT',privateTMPDIR=str(T),privateTMPDIRMode=oct(T.stat().st_mode&0o777),socketPathBytes=len(os.fsencode(T/'s0123456789ab')),blindModeInvocations=0,receiptAndCensusPins=PROPOSAL['receiptAndCensusPins'],productFilesChanged=False,originalFailureRetained=True,architectureHead=git(A,'rev-parse','HEAD'),architectureClean=True,architectureWorktree=str(A),verifier=PROPOSAL['verifier'])
 (B/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
finally:
 if owned:lane.rmdir()
