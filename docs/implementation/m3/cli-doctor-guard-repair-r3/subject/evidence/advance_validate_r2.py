from pathlib import Path
import os, subprocess, json, hashlib, tempfile
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent; W=Path('/Users/sb/code/opensip-ai/opensip-doctor-gate-repair'); P=W.parent/'opensip'
B=F/'post-base-r2'; B.mkdir(exist_ok=False)
p='apps/cli/tests/doctor_tests.rs'; raw=(W/p).read_bytes(); sha=hashlib.sha256(raw).hexdigest()
assert sha==json.loads((F/'owning-r7/report.json').read_text())['source']['sha256']
def git(*a):return subprocess.check_output(['git',*a],cwd=W,text=True).strip()
assert git('diff','--name-only','HEAD')==p
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
subprocess.run(['git','checkout','--detach',head],cwd=W,check=True)
assert (W/p).read_bytes()==raw
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
for n,args in [('doctor-tests',['cargo','test','--locked','--offline','-p','opensip-cli','--test','doctor_tests']),('cli-clippy',['cargo','clippy','--locked','--offline','-p','opensip-cli','--all-targets','--','-D','warnings'])]:
 with (B/(n+'.log')).open('wb')as out:r=subprocess.run([R+args[0],*args[1:]],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,n
assert b'7 passed; 0 failed' in (B/'doctor-tests.log').read_bytes()
assert (W/p).read_bytes()==raw
(B/'report.json').write_text(json.dumps(dict(parent=head,source=dict(path=p,bytes=len(raw),sha256=sha),doctorTests=7,cliClippyPassed=True,allPassed=True,sourceUnchangedFromElevenMutantOwningR7=True,productQualification=False),indent=2)+'\n')
print('POST-BASE7TESTS/CLIPPY PASS',head)
