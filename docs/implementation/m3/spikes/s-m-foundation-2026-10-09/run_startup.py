from pathlib import Path
import os,json,hashlib,subprocess,time,tempfile,platform,statistics,datetime
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=Path('/Users/sb/code/opensip-ai/opensip');TOOLS=C/'sm-tools-2026-10-09';SYS=C/'g2-rust-1.95/sysroot';NODE=TOOLS/'node/node-v24.21.0-darwin-arm64/bin/node';TS=TOOLS/'typescript/package/lib/typescript.js';DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';owned=False
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
assert platform.system()=='Darwin'
for p in [NODE,TS,SYS/'bin/rustc']:assert p.is_file(),p
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();active=[x for x in ps if x.split() and x.split()[-1].rsplit('/',1)[-1] in ['cargo','rustc','clippy-driver']];assert not active,active
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-startup-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T),CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip());env.pop('RUSTC_BOOTSTRAP',None)
 buildenv=dict(env,RUSTC_BOOTSTRAP='1');exe=T/'startup';cmd=['/usr/bin/nice','-n','10',str(SYS/'bin/rustc'),'--edition','2024','--sysroot',str(SYS),'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc',str(B/'probe/startup.rs'),'-o',str(exe)]
 build=subprocess.run(cmd,env=buildenv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'evidence/build.log').write_bytes(build.stdout);assert build.returncode==0,build.stdout.decode();print('trusted Rust startup wrapper built',flush=True)
 def complete(cmd,label):
  with (B/'evidence'/f'{label}.stdout').open('wb') as o,(B/'evidence'/f'{label}.stderr').open('wb') as e:
   child=subprocess.Popen(['/usr/bin/nice','-n','10',*map(str,cmd)],env=env,stdout=o,stderr=e)
   _,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
  return dict(label=label,exitCode=child.returncode,ruMaxrssNative=int(usage.ru_maxrss),rssUnit='bytes',rssBytes=int(usage.ru_maxrss))
 (T/'valid.rs').write_text('pub fn increment(value: u32) -> u32 { value + 1 }\n');(T/'invalid.rs').write_text('pub fn bad() { let _: u32 = "wrong"; }\n');controls=[]
 for label,file in [('rust-positive',T/'valid.rs'),('rust-negative',T/'invalid.rs')]:
  controls.append(complete([exe,'--crate-type','lib','--edition','2024','--sysroot',SYS,'--emit','metadata',file,'--out-dir',T],label))
 assert controls[0]['exitCode']==0 and b'after_analysis' in (B/'evidence/rust-positive.stdout').read_bytes();assert controls[1]['exitCode']!=0 and b'E0308' in (B/'evidence/rust-negative.stderr').read_bytes() and b'after_analysis' not in (B/'evidence/rust-negative.stdout').read_bytes()
 results=[]
 for metric,command in [('SM-1-prototype',[NODE,'--no-addons',B/'probe/startup.cjs',TS]),('SM-3-prototype',[exe,'--startup-probe'])]:
  rows=[]
  for n in range(10):
   log=B/'evidence'/f'{metric}-{n}.stderr';err=log.open('wb');start=time.monotonic_ns();child=subprocess.Popen(['/usr/bin/nice','-n','10',*map(str,command)],env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err);line=child.stdout.readline();ready=time.monotonic_ns();event=json.loads(line);assert event['event']=='ready';child.stdin.write(b'finish\n');child.stdin.close();rest=child.stdout.read();_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status);child.stdout.close();err.close();assert child.returncode==0 and not rest
   row=dict(ordinal=n,warmup=n<3,startNanos=start,readyNanos=ready,readyElapsedNanos=ready-start,ruMaxrssNative=int(usage.ru_maxrss),rssUnit='bytes',rssBytes=int(usage.ru_maxrss),exitCode=child.returncode,ready=event);rows.append(row)
  samples=[r['readyElapsedNanos'] for r in rows if not r['warmup']];results.append(dict(metric=metric,standing='PRELIMINARY RETAINED S-P PROTOTYPE; NOT PRODUCTION CLOSURE',command=list(map(str,command)),runs=rows,medianReadyNanos=statistics.median(samples),maxReadyNanos=max(samples),statistic='3 warmups then 7 fresh process runs; integer median and maximum',SMPlaceholderFilled=False));print(metric,'median ns',statistics.median(samples),'max ns',max(samples),flush=True)
 def pin(path):
  raw=path.read_bytes();return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY STARTUP FOUNDATION; PARTIAL S-M, NOT L-G1 COMPLETION',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),TMPDIR=str(T),TMPDIRMode='0700',ownedLane=str(LOCK),laneHeldForEntireSet=True,noActiveBuildAtStart=True,nice=10,componentPins=[pin(NODE),pin(TS),pin(SYS/'bin/rustc'),pin(exe)],archiveAcquisition=json.loads((TOOLS/'acquisition.json').read_text()),probeControls=controls,startup=results,RUSTC_BOOTSTRAPWrapperBuildOnly=True,RUSTC_BOOTSTRAPAnalyzedInputs=False,repositoryCodeExecuted=False,heldOutSourceInspected=False,SMComplete=False,LG1Met=False,Q6Qualification=False,macOSWholeTreeSettlementVerified=False,memoryPeakRssEquivalenceSelected=False,effectiveL=False,productQualification=False)
 (B/'startup-results.json').write_text(json.dumps(report,indent=2)+'\n');print('startup results written',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
