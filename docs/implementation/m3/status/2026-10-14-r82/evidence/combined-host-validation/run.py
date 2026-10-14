from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib
P=Path('/Users/sb/code/opensip-ai/opensip');C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');B=Path('/tmp/opensip-implementation/combined-host-validation-r1');B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=P,env=E).decode().strip()
s=json.loads((C/'CURRENT-STATE.json').read_bytes());head=git('rev-parse','HEAD');assert head==s['NativeSourceKindDataPublication']['productCodeCommit'];assert s['WorkspaceSourceDataInventoryBound']['inventory']['path'].endswith('.v184.json') and git('status','--porcelain')==''
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-combined-host-',dir=D));T.chmod(0o700);E.update(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip());R='/opt/homebrew/Cellar/rust/1.95.0/bin/';rows=[]
 for name,args in [('host-full-library',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib']),('host-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'])]:
  print(name+' starting',flush=True)
  with(B/(name+'.log')).open('wb')as log:
   p=subprocess.Popen(args,cwd=P,env=E,stdout=log,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,p.pid);assert priority==10;code=p.wait()
  rows.append(dict(name=name,command=args,exitCode=code,niceness=priority));print(name+' exit '+str(code),flush=True)
  if code:print((B/(name+'.log')).read_text()[-4000:],flush=True);break
 passed=len(rows)==2 and all(r['exitCode']==0 for r in rows);j=dict(productHead=head,rows=rows,requiredChecksPassed=passed,wholeHostSuitePassed=passed and '289 passed; 0 failed' in (B/'host-full-library.log').read_text(),hostTestsExpected=289,TMPDIR=str(T),TMPDIRMode='0700',ordinaryLaneOwned=True,sourceAdmissionImplemented=False,ownerAdmissionImplemented=False,qualification=False)
 (B/'checks.json').write_text(json.dumps(j,indent=2)+'\n');assert j['wholeHostSuitePassed']
finally:
 if owned:lock.rmdir()
assert git('rev-parse','HEAD')==head and git('status','--porcelain')=='' and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
s=json.loads((C/'CURRENT-STATE.json').read_bytes());s['CombinedHostValidation']=j;(C/'CURRENT-STATE.json').write_text(json.dumps(s,indent=2)+'\n');print('combined host289 and Clippy passed; no qualification or code change')
