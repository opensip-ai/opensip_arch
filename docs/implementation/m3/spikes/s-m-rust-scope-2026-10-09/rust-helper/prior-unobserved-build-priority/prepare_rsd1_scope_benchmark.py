from pathlib import Path
import os,subprocess,json,hashlib,tempfile
B=Path('/tmp/opensip-implementation/sm-rust-scope-2026-10-09/rust-helper');B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-rsd1');source=Path('/tmp/opensip-implementation/rsd1-2026-10-09/compare.rs').read_text()
source=source.replace('let data=scope::rebuild(j["snapshotId"].as_str().unwrap(),&entries).unwrap();let keys:Vec<_>=j["requestedCoverageDomain"].as_array().unwrap().iter().map(inert).collect();','let keys:Vec<_>=j["requestedCoverageDomain"].as_array().unwrap().iter().map(inert).collect();\n let start=std::time::Instant::now();let data=scope::rebuild(j["snapshotId"].as_str().unwrap(),&entries).unwrap();')
source=source.replace('let domain=scope::domain_commitment(&data,&keys).unwrap();let out=', 'let domain=scope::domain_commitment(&data,&keys).unwrap();let elapsed=u64::try_from(start.elapsed().as_nanos()).unwrap();let out=')
source=source.replace('("subjects".into(),data.subjects),', '("elapsedNanos".into(),number(elapsed)),("subjects".into(),data.subjects),')
(B/'compare.rs').write_text(source)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-rsd-bench-build-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));deps=W/'target/release/deps';exe=B/'compare';args=['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','opt-level=3','-C','linker=/usr/bin/cc','-L','dependency='+str(deps)]
linked=[]
for crate in ['opensip_identity','serde_json']:
 files=list(deps.glob('lib'+crate+'-*.rlib'));assert len(files)==1;args+=['--extern',crate+'='+str(files[0])];raw=files[0].read_bytes();linked.append(dict(path=str(files[0]),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
with (B/'build.log').open('wb')as out:r=subprocess.run(args+[str(B/'compare.rs'),'-o',str(exe)],cwd=T,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
raw=exe.read_bytes();module=(W/'crates/host/src/rust_scope_data.rs').read_bytes();result=dict(standing='UNREVIEWED actual candidate private Rust helper measurement image; no operational native worker/admission',command=args+[str(B/'compare.rs'),'-o',str(exe)],runtimePin=dict(path=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),modulePin=dict(path=str(W/'crates/host/src/rust_scope_data.rs'),bytes=len(module),sha256=hashlib.sha256(module).hexdigest()),linked=linked,privateTMPDIR=str(T),HOMEUnchanged=True);(B/'build.json').write_text(json.dumps(result,indent=2)+'\n');print('Built separate optimized exact Rust helper measurement image; candidate code/stage untouched.')
