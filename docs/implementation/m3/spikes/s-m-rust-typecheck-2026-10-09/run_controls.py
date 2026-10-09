from pathlib import Path
import os,subprocess,json,hashlib,tempfile,time,struct
B=Path(__file__).resolve().parent;SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');build=json.loads((B/'build.json').read_text());EXE=Path(build['executable']);raw=EXE.read_bytes();assert len(raw)==build['bytes']and hashlib.sha256(raw).hexdigest()==build['sha256'];D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=D/'opensip-lanes.lock';owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned Rust probe lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']];T=Path(tempfile.mkdtemp(prefix='opensip-sm-rust-driver-controls-',dir=D));T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));
 if 'HOME'in os.environ:env['HOME']=os.environ['HOME']
 for key in ['LANG','LC_ALL','TZ']:
  if key in os.environ:env[key]=os.environ[key]
 cases={'positive':{'root.rs':b'pub fn increment(value: u32) -> u32 { value + 1 }\n'},'type-error':{'root.rs':b'pub fn bad() { let _: u32 = "wrong"; }\n'},'nested-includes':{'root.rs':b'mod child; pub const TEXT: &str = include_str!("text.txt"); pub const DATA: &[u8] = include_bytes!("payload.bin"); pub fn value() -> u32 { child::value() }\n','child.rs':b'pub fn value() -> u32 { 4 }\n','text.txt':b'prepared text\n','payload.bin':b'\0\xff\0prepared'},'build-output-unavailable':{'root.rs':b'include!(concat!(env!("OUT_DIR"), "/generated.rs"));\n'},'proc-macro-unavailable':{'root.rs':b'use absent_derive::Example; #[derive(Example)] pub struct Item;\n'}}
 outside=T/'outside.txt';outside.write_bytes(b'owned-control-text\n');outsideDigest=hashlib.sha256(outside.read_bytes()).hexdigest();cases['denied-include']={'root.rs':('pub const TEXT: &str = include_str!(r#"'+str(outside)+'"#);\n').encode()};records=[]
 for label,files in cases.items():
  root=T/label;root.mkdir(mode=0o700);output=root/'output';output.mkdir(mode=0o700);encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(files))
  for name,data in sorted(files.items()):
   path=str(root/name).encode();encoded+=struct.pack('>Q',len(path))+path+struct.pack('>Q',len(data))+data
  mp=root/'map.bin';mp.write_bytes(encoded);(B/f'control-{label}-source-map.bin').write_bytes(encoded);out=B/f'control-{label}.stdout';err=B/f'control-{label}.stderr';start=time.monotonic_ns()
  with out.open('wb')as o,err.open('wb')as e:
   child=subprocess.Popen(['/usr/bin/nice','-n','10',str(EXE),'--prepared-map',str(mp),'--crate-type','lib','--edition','2024','--sysroot',str(SYS),'--emit','metadata',str(root/'root.rs'),'--out-dir',str(output)],cwd=root,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
  end=time.monotonic_ns();events=[json.loads(line)for line in out.read_text().splitlines()if line.startswith('{')];after=any(v['event']=='after_analysis'for v in events)
  if label in ['positive','nested-includes']:assert child.returncode==0 and after,(label,err.read_text());assert not list(output.iterdir());assert all(v['deniedReadCalls']==0 for v in events)
  else:assert child.returncode!=0 and not after,(label,err.read_text())
  if label=='type-error':assert 'E0308'in err.read_text()
  if label=='denied-include':assert 'outside prepared map'in err.read_text()
  if label=='build-output-unavailable':assert 'OUT_DIR'in err.read_text()
  if label=='proc-macro-unavailable':assert 'absent_derive'in err.read_text()
  records.append(dict(label=label,synthetic=True,exitCode=child.returncode,afterAnalysisReachedSuccessfully=after,afterExpansionReached=any(v['event']=='after_expansion'for v in events),events=events,wholeProcessNanos=end-start,rssNative=int(usage.ru_maxrss),rssUnit='bytes',sourceMapSha256=hashlib.sha256(encoded).hexdigest()))
 assert hashlib.sha256(outside.read_bytes()).hexdigest()==outsideDigest;(B/'controls.json').write_text(json.dumps(dict(standing='UNREVIEWED FIRST-PARTY RUST DRIVER VIRTUAL SOURCE/API CONTROLS ONLY',controls=records,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeld=True,nice=10,HOMEUnchanged=True,CARGO_HOME='/Users/sb/.cargo',RUSTC_BOOTSTRAPAnalyzedInputs=False,repositoryCodeExecuted=False,productCodeChanged=False,confinementClaimed=False,sourceAdmissionClaimed=False,SM4PlaceholderFilled=False,SMComplete=False),indent=2)+'\n');print(json.dumps(records,indent=2))
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
