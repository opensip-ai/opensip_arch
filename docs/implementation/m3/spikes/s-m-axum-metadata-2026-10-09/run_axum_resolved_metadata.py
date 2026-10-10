from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time,re
B=Path(__file__).resolve().parent;N=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');os.setpriority(os.PRIO_PROCESS,0,10)
def pin(p):
 raw=Path(p).read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
receipt=json.loads((B/'axum-locked-inputs/receipt.json').read_text());census=json.loads((B/'t2-metadata-census.json').read_text());root=Path(census['privateTMPDIR'])/'rs-medium-axum'
assert pin(receipt['originalLock']['path'])['sha256']==receipt['originalLock']['sha256']
for r in receipt['packages']:
 q=pin(r['archive']);assert q['sha256']==r['checksum']==r['sha256'] and q['bytes']==r['bytes']
for r in receipt['indexFiles']:
 q=pin(r['path']);assert q['sha256']==r['sha256'] and q['bytes']==r['bytes']
assert pin(receipt['registryConfigPath'])['sha256']==receipt['registryConfigSha256']
before={str(p.relative_to(root)):pin(p) for p in root.rglob('*') if p.is_file()};image=Path(re.search(r'Executable unittests src/cargo/lib.rs \(([^)]+)\)',(N/'spike-metadata-build.log').read_text())[1]);runtime=pin(image)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-axum-resolve-',dir=D));T.chmod(0o700);home=T/'home';home.mkdir(mode=0o700);out=B/'axum-resolved-metadata.json';assert not out.exists();packet=T/'packet.json';packet.write_text(json.dumps(dict(cwd=str(root),privateCargoHome=str(home),manifestPath=str(root/'Cargo.toml'),output=str(out),rustc='/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc',dependencyCacheReceipt=str(B/'axum-locked-inputs/receipt.json'),noDeps=False,filterPlatform='aarch64-apple-darwin'))+'\n')
E=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),OPENSIP_SPIKE_METADATA_PACKET=str(packet))
if 'HOME' in os.environ:E['HOME']=os.environ['HOME']
lane=D/'opensip-lanes.lock';owned=False
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary metadata lane',flush=True);time.sleep(5)
try:
 stdout=B/'axum-resolved-metadata.stdout';stderr=B/'axum-resolved-metadata.stderr';start=time.monotonic_ns()
 with stdout.open('wb') as o,stderr.open('wb') as e:
  child=subprocess.Popen([str(image),'util::context::sealed_spike_metadata_tests::opensip_spike_metadata_collect','--exact','--ignored','--nocapture'],cwd=T,env=E,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;code=child.wait()
 after={str(p.relative_to(root)):pin(p) for p in root.rglob('*') if p.is_file()};assert before==after,'immutable public files changed or new source file created'
 v=dict(standing='UNREVIEWED ACTUAL OFFLINE LOCKED FROZEN CARGO METADATA RESOLUTION ATTEMPT; OUTSIDE PRODUCT',exitCode=code,elapsedNanos=time.monotonic_ns()-start,runtime=runtime,privateTMPDIR=str(T),privateCargoHome=str(home),observedNiceness=priority,ownedLane=True,originalSourceCopiesUnchanged=True,originalLock=receipt['originalLock'],generatedOrUpdatedLockfile=False,repositoryCodeExecuted=False,sourceAdmission=False,fullSM=False,filterPlatform='aarch64-apple-darwin',stdout=str(stdout),stderr=str(stderr),metadata=pin(out) if out.exists() else None)
 if code==0:
  assert '1 passed' in stdout.read_text();m=json.loads(out.read_text());assert m['resolve'] is not None;v.update(packages=len(m['packages']),resolvedNodes=len(m['resolve']['nodes']),workspaceMembers=len(m['workspace_members']))
 (B/'axum-resolved-metadata-attempt.json').write_text(json.dumps(v,indent=2)+'\n');print('Axum offline resolution', 'PASS' if code==0 else 'INCOMPLETE',v.get('resolvedNodes',''),flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
