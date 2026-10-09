from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib
os.setpriority(os.PRIO_PROCESS,0,10)
parent_nice=os.getpriority(os.PRIO_PROCESS,0)
assert parent_nice==10
B=Path('/tmp/opensip-implementation/rsd1-2026-10-09');B.mkdir(exist_ok=True);W=Path('/Users/sb/code/opensip-ai/opensip-rsd1');D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';T=Path(tempfile.mkdtemp(prefix='opensip-rsd1-checks-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip())
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
operations=[('format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/rust_scope_data.rs'],W/'crates/host'),('focused',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','rust_scope_data'],W),('clippy',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'],W),('release',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','--release','-p','opensip-host'],W)]
rows=[]
for name,cmd,cwd in operations:
 owned=False
 while True:
  try:lock.mkdir();owned=True;break
  except FileExistsError:print('waiting for RSD1 check lane',flush=True);time.sleep(5)
 try:
  print(name,'running',flush=True)
  with (B/(name+'.log')).open('wb')as out:
   r=subprocess.Popen(cmd,cwd=cwd,env=E,stdout=out,stderr=subprocess.STDOUT);child_nice=os.getpriority(os.PRIO_PROCESS,r.pid);assert child_nice==10;r.wait()
  row=dict(check=name,argv=cmd,observedParentNiceness=parent_nice,observedChildNiceness=child_nice,exitCode=r.returncode,laneOwned=True,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True);rows.append(row);(B/'checks.json').write_text(json.dumps(rows,indent=2)+'\n');assert r.returncode==0,(name,r.returncode)
 finally:
  if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
print('RSD1format/focused/clippy/release passed',flush=True)
