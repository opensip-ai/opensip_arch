from pathlib import Path
import json,os,subprocess,tempfile,hashlib
B=Path(__file__).resolve().parent;os.setpriority(os.PRIO_PROCESS,0,10);prior=json.loads(Path('/tmp/opensip-implementation/sm-rust-scope-2026-10-09/rust-helper/build.json').read_text());args=prior['command'][:];args[-3]=str(B/'compare_scope.rs');D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-scope-helper-',dir=D));T.chmod(0o700);args[-1]=str(T/'compare_scope')
for row in prior['linked']:
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
with (B/'build.log').open('wb') as log:
 child=subprocess.Popen(args,cwd=T,env=E,stdout=log,stderr=subprocess.STDOUT);nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert nice==10;code=child.wait()
assert code==0,(B/'build.log').read_text()
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(B/'build.json').write_text(json.dumps(dict(standing='EXACT ACCEPTED RSD1 SCOPE ARRAY ONLY HELPER; NO DOMAIN/KEYS/SOURCE ADMISSION',command=args,executable=pin(T/'compare_scope'),linked=prior['linked'],source=pin(B/'compare_scope.rs'),module=pin(B/'rust_scope_data.rs'),acceptedProductModule=pin(Path('/Users/sb/code/opensip-ai/opensip/crates/host/src/rust_scope_data.rs')),observedChildNiceness=nice,TMPDIR=str(T),TMPDIRMode='0700',bareRustc=True,CargoRun=False),indent=2)+'\n');print('Built exact scope-only helper')
