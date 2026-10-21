from pathlib import Path
import os,json,subprocess,tempfile,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'core-clippy-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
def pins():return [dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in paths]
before=pins();r=subprocess.run([R+'cargo','clippy','--locked','--offline','-p','opensip-platform','-p','opensip-components','--all-targets','--','-D','warnings'],cwd=W,env=E,capture_output=True);(B/'clippy.log').write_bytes(r.stdout+r.stderr);report=dict(standing='Current D4 factory core/platform all-target lint only; native adapter, integration controls, mutants, inventory and complete-unit review still owed.',sourcePins=before,exitCode=r.returncode,allPassed=r.returncode==0,productQualification=False);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert pins()==before;assert r.returncode==0
print('D4 core/platform all-target warning-denied Clippy PASS')
