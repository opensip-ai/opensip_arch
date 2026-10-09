from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib,statistics
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');C=Path('/Users/sb/code/.opensip-implementation-cache');source=A/'docs/implementation/m3/spikes/s-m-foundation-2026-10-09/startup-results.json';old=json.loads(source.read_text());pin=next(p for p in old['componentPins']if p['path'].endswith('/startup'));exe=Path(pin['path']);SYS=C/'g2-rust-1.95/sysroot';lib=SYS/'lib/rustlib/aarch64-apple-darwin/lib/librustc_driver-eea6b8737cd03a8e.dylib'
def observe(path):raw=path.read_bytes();return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
assert observe(exe)==pin;lp=observe(lib);assert lp['bytes']==203876200 and lp['sha256']=='d41766d9ed6e9c7959eeb7678b9a6bb301f70948664cd39a8a0d2d83ad23d54e'
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for Rust ready measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm3-ready-',dir=D)).resolve();T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for key in ['HOME','LANG','LC_ALL','TZ']:
  if key in os.environ:env[key]=os.environ[key]
 loads={str(p):subprocess.check_output(['/usr/bin/otool','-L',str(p)]).decode()for p in [exe,lib]};rpaths=subprocess.check_output(['/usr/bin/otool','-l',str(exe)]).decode();(B/'macho-loads.json').write_text(json.dumps(dict(standing='MEASUREMENT MACHO LOAD DECLARATIONS,NOT QUALIFIED RUNTIME SETTLEMENT',loadDeclarations=loads,executableLoadCommands=rpaths,measurementRuntimePins=[pin,lp],platformDependencies='disclosed currentmacOS SystemLibrary/usr/lib dependencies; no wholeplatform closure/qualification assertion'),indent=2)+'\n')
 source_control=T/'valid.rs';source_control.write_text('pub fn increment(value:u32)->u32 {value+1}\n');err=B/'control.stderr'
 with err.open('wb')as e:r=subprocess.run([str(exe),'--crate-type','lib','--edition','2024','--sysroot',str(SYS),'--emit','metadata',str(source_control),'--out-dir',str(T)],cwd=T,env=env,stdout=subprocess.PIPE,stderr=e)
 (B/'control.stdout').write_bytes(r.stdout);assert r.returncode==0 and r.stdout==b'{"event":"after_analysis"}\n'and err.read_bytes()==b''
 runs=[]
 for n in range(10):
  err=B/f'{n}.stderr';e=err.open('wb');start=time.monotonic_ns();child=subprocess.Popen([str(exe),'--startup-probe'],cwd=T,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=e);line=child.stdout.readline();ready=time.monotonic_ns();event=json.loads(line);assert event==dict(event='ready',compiler='1.95.0');child.stdin.write(b'finish\n');child.stdin.close();rest=child.stdout.read();_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status);child.stdout.close();e.close();assert child.returncode==0 and rest==b''and err.read_bytes()==b'';(B/f'{n}.stdout').write_bytes(line);rss=int(usage.ru_maxrss);assert 0<=rss<2**64;runs.append(dict(ordinal=n,warmup=n<3,startNanos=start,readyNanos=ready,startToReadyNanos=ready-start,ready=event,exitCode=0,rssNative=rss,rssUnit='bytes',rssBytes=rss))
 assert observe(exe)==pin and observe(lib)==lp;values=[r['startToReadyNanos']for r in runs if not r['warmup']];report=dict(standing='UNREVIEWED PRELIMINARY SM3 CALLBACK-READY FIGURE CANDIDATE,EXACT SIDECAR AND DYNAMIC COMPILERLIB PINS',runs=runs,medianStartToReadyNanos=statistics.median(values),maxStartToReadyNanos=max(values),measurementRuntimePins=[pin,lp],span='parent before spawn through received marker after linkedcompiler load and firstpartyCallbacks value construction; no protocol/handshake assertion',positiveSyntheticAfterAnalysisControlPassed=True,componentBytesUnchangedAfterSamples=True,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,HOMEUnchanged=True,RUSTC_BOOTSTRAPAbsent=True,noInheritedDYLDOverrides=True,repositoryCodeExecuted=False,SM3FigureCompletenessProposed=True,SM3PlaceholderFilled=False,SMComplete=False,LG1Met=False,confinementClaimed=False,effectiveL=False,productQualification=False);(B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('Rust callbackready measured:',statistics.median(values),max(values),'ns',flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
