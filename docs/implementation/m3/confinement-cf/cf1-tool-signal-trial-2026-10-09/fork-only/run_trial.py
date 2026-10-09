from pathlib import Path
import os,json,subprocess,time,tempfile,signal,select,hashlib,datetime,platform
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());L=D/'opensip-lanes.lock';owned=False
while True:
 try:L.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 active=[r for r in subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines() if r.split()[-1].rsplit('/',1)[-1] in ['cargo','rustc','clippy-driver']];assert not active,active
 T=Path(tempfile.mkdtemp(prefix='opensip-cf1-signals-',dir=D)).resolve();T.chmod(0o700);exe=T/'fixture';env=dict(os.environ,TMPDIR=str(T));cmd=['/usr/bin/nice','-n','10','/usr/bin/clang','-std=c11','-Wall','-Wextra','-Werror',str(B/'fixture.c'),'-o',str(exe)];p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'build.log').write_bytes(p.stdout);assert p.returncode==0,p.stdout.decode()
 base='''(version 1)
(allow default)
(deny network*)
(deny file-write* (require-all (require-not (subpath (param "SCRATCH"))) (require-not (literal "/dev/null"))))
(deny file-link (require-not (subpath (param "SCRATCH"))))
(deny process-exec (require-not (subpath (param "CLOSURE_ROOT"))))
(deny process-info* (target others))
(deny sysctl-read (sysctl-name-prefix "kern.procargs"))
(deny mach-lookup)
'''
 variants=[('unconfined-control',None),('original-others','(deny signal (target others))'),('children-exception','(deny signal (require-all (target others) (require-not (target children))))'),('same-sandbox-exception','(deny signal (require-all (target others) (require-not (target same-sandbox))))')];rows=[]
 for name,rule in variants:
  profile='none'
  if rule:
   source=B/(name+'.sb');source.write_text(base+rule+'\n');profile=str(source)
  for repeat in range(3):
   scratch=T/f'{name}-{repeat}';scratch.mkdir(mode=0o700);scratch=scratch.resolve();observer=subprocess.Popen(['/usr/bin/nice','-n','10',str(exe),'observer'],env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);assert observer.stdout.readline()==b'ready\n';root=None
   try:
    err=B/f'{name}-{repeat}.stderr';f=err.open('wb');root=subprocess.Popen(['/usr/bin/nice','-n','10',str(exe),profile,str(scratch),str(T),str(observer.pid),name],env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=f,start_new_session=True)
    readable,_,_=select.select([root.stdout],[],[],10);assert readable,(name,'test fixture timed out before report');line=root.stdout.readline();observed=json.loads(line);observerReceipt=False
    if observed.get('outsideOwnedObserverSignal',{}).get('rc')==0:
     ready,_,_=select.select([observer.stdout],[],[],1);observerReceipt=bool(ready and os.read(observer.stdout.fileno(),1)==b'O')
    row=dict(variant=name,repeat=repeat,observed=observed,outsideOwnedObserverReceived=observerReceipt,profile=str(profile),scratch=str(scratch),rootPid=root.pid,observerPid=observer.pid);rows.append(row);print(name,repeat,json.dumps(observed),flush=True)
   finally:
    if root is not None:
     try:os.killpg(root.pid,signal.SIGKILL)
     except ProcessLookupError:pass
     _,status,usage=os.wait4(root.pid,0);root.returncode=os.waitstatus_to_exitcode(status);root.stdout.close();root.stdin.close();f.close()
    try:os.killpg(observer.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    _,status,usage=os.wait4(observer.pid,0);observer.returncode=os.waitstatus_to_exitcode(status);observer.stdout.close();observer.stderr.close()
 def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 report=dict(schemaVersion=1,standing='UNREVIEWED CF1 FIRST-PARTY AD-HOC SIGNAL TRIAL; NOT SIGNED ENFORCEMENT MATRIX ROW',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),osRelease=subprocess.check_output(['/usr/bin/sw_vers','-productVersion']).decode().strip(),osBuild=subprocess.check_output(['/usr/bin/sw_vers','-buildVersion']).decode().strip(),executable=pin(exe),source=pin(B/'fixture.c'),ownedLane=str(L),laneHeldForWholeSet=True,nice=10,TMPDIR=str(T),TMPDIRMode='0700',onlyOwnedFixtureProcessGroupsSignalled=True,rootUnreapedUntilGroupCleanup=True,rows=rows,linuxLanesRun=False,signedHardenedNotarizedLauncher=False,realProviderOrToolClosureMeasured=False,CF1Complete=False,signalPolicySelected=False,confinementAvailabilityClaimed=False,productQualification=False,effectiveL=False,repositoryCodeExecuted=False)
 (B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('trial complete',flush=True)
finally:
 if owned:L.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
