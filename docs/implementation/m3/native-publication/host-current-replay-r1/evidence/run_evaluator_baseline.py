from pathlib import Path
import os,subprocess,tempfile,time,json
P=Path('/Users/sb/code/opensip-ai/opensip');B=Path(__file__).resolve().parent/'evaluator-baseline-r1';B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-current-corpus-baseline-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
 args=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-evaluator','--lib','cycle_retained_evaluation_and_replay_match_known_and_partial_results'];print('unchanged evaluator retained-cycle baseline starting',flush=True)
 with (B/'baseline.log').open('wb')as f:
  c=subprocess.Popen(args,cwd=P,env=E,stdout=f,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,c.pid);assert priority==10;code=c.wait()
 (B/'check.json').write_text(json.dumps(dict(command=args,exitCode=code,niceness=priority,TMPDIR=str(T),TMPDIRMode='0700',ordinaryLaneOwned=True,baselineSourceUnchanged=True),indent=2)+'\n');print('baseline exit',code,flush=True);print((B/'baseline.log').read_text()[-2800:])
finally:
 if owned:lock.rmdir()
