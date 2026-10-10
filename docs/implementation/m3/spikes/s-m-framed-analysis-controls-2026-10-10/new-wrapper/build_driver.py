from pathlib import Path
import os,subprocess,tempfile,json,hashlib
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path(__file__).resolve().parent;assert not (B/'build.log').exists();SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-rust-driver-',dir=D));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T),RUSTC_BOOTSTRAP='1',CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip());exe=T/'driver';cmd=[str(SYS/'bin/rustc'),'--edition','2024','--sysroot',str(SYS),'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc','-L','dependency=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps','--extern','opensip_identity=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps/libopensip_identity-49c8c63d61772d58.rlib','--extern','serde_json=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps/libserde_json-6a07d5ee01360a2d.rlib',str(B/'driver.rs'),'-o',str(exe)]
deps=Path('/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps')
def pin(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
linked=[pin(p) for p in sorted(deps.iterdir()) if p.is_file() and p.suffix in ['.rlib','.rmeta']]
reference=json.loads((B/'linked-parent-reference.json').read_bytes())
for row in reference['linkedExistingFirstpartyArtifacts']:assert pin(Path(row['path']))==row
(B/'linked-dependency-input-pins.json').write_text(json.dumps(dict(files=linked,compilerExecutedByCensus=False),indent=2)+'\n')
r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'build.log').write_bytes(r.stdout);print(r.stdout.decode());assert r.returncode==0
raw=exe.read_bytes();(B/'build.json').write_text(json.dumps(dict(standing='UNREVIEWED THROWAWAY VIRTUAL SOURCE RUST DRIVER; NO PRODUCT CODE OR ADMISSION',executable=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),sourceSha256=hashlib.sha256((B/'driver.rs').read_bytes()).hexdigest(),bareRustc=True,CargoRun=False,RUSTC_BOOTSTRAPWrapperBuildOnly=True,corpusCodeCompiledOrExecuted=False,firstpartyLibrariesLinked=True,command=cmd,parentBuildNiceness=os.getpriority(os.PRIO_PROCESS,0),TMPDIR=str(T),TMPDIRMode='0700',sysroot=str(SYS)),indent=2)+'\n');print('Built first-party virtual source driver',exe)

for row in linked:assert pin(Path(row['path']))==row
