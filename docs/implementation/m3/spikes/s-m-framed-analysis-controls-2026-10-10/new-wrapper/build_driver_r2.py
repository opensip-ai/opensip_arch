from pathlib import Path
import os,subprocess,tempfile,json,hashlib
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path(__file__).resolve().parent;assert not (B/'build.log').exists();SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');O=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-framed-driver-build-',dir=O));T.chmod(0o700)
env=dict(os.environ,TMPDIR=str(T),RUSTC_BOOTSTRAP='1',CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip());home=os.environ.get('HOME')
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
source=json.loads((B/'sha-library-source-pins.json').read_bytes())
for row in source['files']:assert pin(Path(row['path']))==row
sha=T/'libsha2_const_stable.rlib';first=[str(SYS/'bin/rustc'),'--edition','2018','--sysroot',str(SYS),'--crate-type','rlib','--crate-name','sha2_const_stable','-C','opt-level=3',str(B/'sha-library-source/src/lib.rs'),'-o',str(sha)]
r=subprocess.run(first,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'sha-build.log').write_bytes(r.stdout);assert r.returncode==0,r.stdout.decode()
serde=SYS/'lib/rustlib/aarch64-apple-darwin/lib/libserde_json-9af384fe91ae3f17.rmeta';linked=[pin(sha),pin(serde)];(B/'linked-dependency-input-pins.json').write_text(json.dumps(dict(files=linked,SHAFromWholeChecksumPinnedExistingPublicArchive=True,serdeJSONFromPinnedOfficialRustcDevSysroot=True),indent=2)+'\n')
exe=T/'driver';cmd=[str(SYS/'bin/rustc'),'--edition','2024','--sysroot',str(SYS),'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc','--extern','sha2_const_stable='+str(sha),'--extern','serde_json='+str(serde),str(B/'driver.rs'),'-o',str(exe)]
r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'build.log').write_bytes(r.stdout);print(r.stdout.decode());assert r.returncode==0
for row in linked:assert pin(Path(row['path']))==row
for row in source['files']:assert pin(Path(row['path']))==row
assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
(B/'build.json').write_text(json.dumps(dict(standing='UNREVIEWED FIRSTPARTY FRAMED MAP ANALYSIS WRAPPER',executable=str(exe),**{k:v for k,v in pin(exe).items() if k!='path'},sourceSha256=pin(B/'driver.rs')['sha256'],bareRustc=True,CargoRun=False,RUSTC_BOOTSTRAPWrapperBuildOnly=True,corpusCodeCompiledOrExecuted=False,SHACompilation=first,command=cmd,linked=linked,parentBuildNiceness=os.getpriority(os.PRIO_PROCESS,0),TMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,sysroot=str(SYS)),indent=2)+'\n');print('Built unreviewed firstparty framed analysis driver',exe)
