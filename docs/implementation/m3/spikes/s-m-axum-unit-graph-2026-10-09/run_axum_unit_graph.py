from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time,re
B=Path(__file__).resolve().parent;N=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');os.setpriority(os.PRIO_PROCESS,0,10)
def pin(p):raw=Path(p).read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
a=json.loads((B/'axum-resolved-metadata-attempt.json').read_text());root=Path(a['originalLock']['path']).parent;before={str(p.relative_to(root)):pin(p) for p in root.rglob('*') if p.is_file()};image=Path(re.search(r'Executable unittests src/cargo/lib.rs \(([^)]+)\)',(N/'spike-unitgraph-build.log').read_text())[1]);runtime=pin(image)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-axum-units-',dir=D));T.chmod(0o700);packet=T/'packet.json';packet.write_text(json.dumps(dict(cwd=str(root),privateCargoHome=a['privateCargoHome'],manifestPath=str(root/'Cargo.toml'),output=str(T/'unused.json'),rustc='/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc',unitGraphTargetDir=str(T/'target')))+'\n');E=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),OPENSIP_SPIKE_METADATA_PACKET=str(packet))
if 'HOME' in os.environ:E['HOME']=os.environ['HOME']
lane=D/'opensip-lanes.lock';owned=False
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary unit-graph lane',flush=True);time.sleep(5)
try:
 stdout=B/'axum-unit-graph.stdout';stderr=B/'axum-unit-graph.stderr';start=time.monotonic_ns()
 with stdout.open('wb') as o,stderr.open('wb') as e:
  child=subprocess.Popen([str(image),'util::context::sealed_spike_metadata_tests::opensip_spike_metadata_collect','--exact','--ignored','--nocapture'],cwd=T,env=E,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;code=child.wait()
 after={str(p.relative_to(root)):pin(p) for p in root.rglob('*') if p.is_file()};assert before==after,'original source changed'
 v=dict(standing='UNREVIEWED ACTUAL CARGO CHECK UNIT GRAPH; NO EXECUTOR/BUILD RUNNER',exitCode=code,elapsedNanos=time.monotonic_ns()-start,runtime=runtime,privateTMPDIR=str(T),privateTarget=str(T/'target'),observedNiceness=priority,ownedLane=True,originalSourceCopiesUnchanged=True,originalLock=a['originalLock'],generatedOrUpdatedLockfile=False,repositoryCodeExecuted=False,sourceAdmission=False,fullSM=False,stdout=str(stdout),stderr=str(stderr))
 if code==0:
  raw=stdout.read_text();assert '1 passed' in raw;g,end=json.JSONDecoder().raw_decode(raw[raw.index('{'):]);assert g['version']==1;(B/'axum-unit-graph.json').write_text(json.dumps(g,indent=2)+'\n');v.update(units=len(g['units']),roots=len(g['roots']),customBuildUnits=sum(u['target']['kind']==['custom-build'] for u in g['units']),proceduralMacroUnits=sum('proc-macro' in u['target']['kind'] for u in g['units']))
 (B/'axum-unit-graph-attempt.json').write_text(json.dumps(v,indent=2)+'\n');print('Actual unit graph','PASS' if code==0 else 'INCOMPLETE',v.get('units',''),flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
