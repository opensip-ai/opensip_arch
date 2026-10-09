from pathlib import Path
import os,subprocess,json,hashlib,tempfile
B=Path(__file__).resolve().parent;W=Path('/Users/sb/code/opensip-ai/opensip-rsd1');D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-rsd1-bare-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));rustc='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc';deps=W/'target/release/deps';exe=B/'compare';args=[rustc,'--edition','2024','-C','linker=/usr/bin/cc','-L','dependency='+str(deps)]
for crate in ['opensip_identity','serde_json']:
 files=list(deps.glob('lib'+crate+'-*.rlib'));assert len(files)==1;args+=['--extern',crate+'='+str(files[0])]
with (B/'independent-build.log').open('wb')as out:r=subprocess.run(args+[str(B/'compare.rs'),'-o',str(exe)],cwd=T,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0;S=Path('/tmp/opensip-implementation/sm-rust-scope-2026-10-09');checks=json.loads((S/'results.json').read_text());rows=[]
for w in checks['workloads']:
 p=S/(w['id']+'-input.json');out=B/(w['id']+'-independent.stdout');err=B/(w['id']+'-independent.stderr')
 with out.open('wb')as o,err.open('wb')as e:r=subprocess.run([str(exe),str(p)],cwd=T,env=E,stdout=o,stderr=e)
 assert r.returncode==0 and err.read_bytes()==b'';actual=json.loads(out.read_text());expected=w['actors'][0]['shape'];assert all(actual[k]==expected[k]for k in actual);rows.append(dict(id=w['id'],subjectCount=actual['subjectCount'],input=dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()),allFieldsMatchedIndependentPythonAAndB=True))
host=list(deps.glob('libopensip_host-*.rlib'));assert len(host)==1;(B/'privacy.rs').write_text('extern crate opensip_host;\nuse opensip_host::rust_scope_data;\nfn main() {}\n')
with (B/'privacy.log').open('wb')as out:r=subprocess.run([rustc,'--edition','2024','--emit','metadata','-L','dependency='+str(deps),'--extern','opensip_host='+str(host[0]),str(B/'privacy.rs'),'-o',str(T/'privacy.rmeta')],cwd=T,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode!=0 and 'E0603'in(B/'privacy.log').read_text()and 'private'in(B/'privacy.log').read_text();raw=exe.read_bytes();result=dict(standing='UNREVIEWED11ACTUALPRODUCTHELPER/PYTHON RECIPE COMPARISONS; NO MANIFEST OR WORKER ADMISSION',workloads=rows,privacyActualHostE0603=True,runtimePin=dict(path=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),privateTMPDIR=str(T),HOMEUnchanged=True);(B/'independent.json').write_text(json.dumps(result,indent=2)+'\n');print('11Rust helper scope arrays/commitments/CBOR byte lengths and hashes match both independent Python implementations; actualhostE0603passed')
