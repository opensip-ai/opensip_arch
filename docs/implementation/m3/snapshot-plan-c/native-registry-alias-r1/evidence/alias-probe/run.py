"""Actual synthetic registry protocol fixtures; no registry authentication."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time
R=Path('/tmp/opensip-implementation/native-registry-alias-probe-r1');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
try:
 while not owned:
  try:LANE.mkdir();owned=True
  except FileExistsError:print('Waiting for shared lane; no child launched.',flush=True);time.sleep(15)
 private=Path(tempfile.mkdtemp(prefix='opensip-registry-alias-',dir=LANE.parent));os.chmod(private,0o700);assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 exe='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';rows=[]
 for label,index,source,alias in [('registry-valid','https://example.invalid/index','registry+https://example.invalid/index','https://example.invalid/index'),('sparse-valid','sparse+https://example.invalid/index/','sparse+https://example.invalid/index/','sparse+https://example.invalid/index/'),('registry-stripped','https://example.invalid/index','registry+https://example.invalid/index',None),('registry-misbound','https://example.invalid/index','registry+https://example.invalid/index','https://other.invalid/index')]:
  base=private/label;root=base/'consumer';pkg=base/'source/package';manifest='[package]\nname="registry-family-fixture"\nversion="0.1.0"\nedition="2024"\n';code='pub fn fixture_only() {}\n';write(pkg/'Cargo.toml',manifest);write(pkg/'src/lib.rs',code);write(pkg/'.cargo-checksum.json',json.dumps({'files':{'Cargo.toml':sha(manifest.encode()),'src/lib.rs':sha(code.encode())},'package':'0'*64}))
  write(root/'Cargo.toml','[package]\nname="registry-family-consumer"\nversion="0.1.0"\nedition="2024"\n[dependencies]\na={package="registry-family-fixture",version="=0.1.0",registry="fixture"}\n');write(root/'src/lib.rs','pub fn fixture_only() {}\n')
  write(root/'.cargo/config.toml',('' if alias is None else '[registries.fixture]\nindex='+json.dumps(alias)+'\n')+'[source.original]\nregistry='+json.dumps(index)+'\nreplace-with="sealed"\n[source.sealed]\ndirectory='+json.dumps(str(base/'source'))+'\n')
  write(root/'Cargo.lock','version=4\n[[package]]\nname="registry-family-consumer"\nversion="0.1.0"\ndependencies=["registry-family-fixture"]\n[[package]]\nname="registry-family-fixture"\nversion="0.1.0"\nsource='+json.dumps(source)+'\nchecksum="'+('0'*64)+'"\n')
  before=(root/'Cargo.lock').read_bytes();cmd=[exe,'metadata','--locked','--offline','--frozen','--format-version','1','--filter-platform','aarch64-apple-darwin'];out=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=60);(R/(label+'.stdout')).write_bytes(out.stdout);(R/(label+'.stderr')).write_bytes(out.stderr);assert before==(root/'Cargo.lock').read_bytes();expected=0 if label.endswith('-valid') else 101;assert out.returncode==expected,(label,out.stderr.decode());p=None
  if expected==0:
   m=json.loads(out.stdout);p=next(x for x in m['packages'] if x['name']=='registry-family-fixture');assert p['source']==source and Path(p['manifest_path'])==pkg/'Cargo.toml'
  else:assert out.stdout==b''
  rows.append({'case':label,'argv':cmd,'cwd':str(root),'exitCode':out.returncode,'rawLockSource':source,'metadataSource':p['source'] if p else None,'manifestPath':p['manifest_path'] if p else None,'declaredManifestRegistry':'fixture','projectedAliasIndex':alias,'knownFixtureCondition':label,'publicFailureRouteEstablished':False,'lockBytesUnchanged':True,'stdoutBytes':len(out.stdout),'stdoutSha256':sha(out.stdout),'stderrBytes':len(out.stderr),'stderrSha256':sha(out.stderr),'fixtureChecksumPackage':'0'*64,'fixtureFileHashes':{'Cargo.toml':sha(manifest.encode()),'src/lib.rs':sha(code.encode())}})
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 report={'standing':'Four actual installed Cargo metadata observations of synthetic first-party registry and sparse-registry directory replacements with valid, absent and misbound manifest registry alias associations. Known fixture associations come from retained configuration bytes, never from English stderr or exit status. No public failure mapping is selected. Zero lock/package checksum is an explicit self-asserted fixture value, not a tarball digest authentication or native source admission. Original protocol source is preserved in metadata and lock. No HOME assignment; prescribed CARGO_HOME=/Users/sb/.cargo. NativeCC2/environment/profile/carrier/source/owner/launch/custody/product qualification not established, fixture code not built or run. Closed native registry sourceKind interpretation still needs complete explicit source/acquisition mapping before implementation.','privateTmpdir':str(private),'executable':{'path':exe,'sha256':sha(Path(exe).read_bytes())},'runs':rows,'registryAuthenticated':False,'sourceClassificationPublished':False,'R3Resolved':False,'productImplemented':False,'productQualification':False}
 (R/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
finally:
 if owned:LANE.rmdir()
