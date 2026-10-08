"""Actual first-party fixture observation; not an admitted native source."""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile,time
R=Path('/tmp/opensip-implementation/native-source-serialization-probe-r1');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def form_encode(text):
 return ''.join(chr(b) if b in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*-._' else '+' if b==32 else '%'+format(b,'02X') for b in text.encode())
try:
 while not owned:
  try:LANE.mkdir();owned=True
  except FileExistsError:print('Waiting for shared lane; no child launched.',flush=True);time.sleep(15)
 private=Path(tempfile.mkdtemp(prefix='opensip-source-serialization-',dir=str(LANE.parent)));os.chmod(private,0o700)
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 executable='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';rows=[]
 for label,branch in [('git-main','main'),('git-encoded-branch','topic/foo+bar')]:
  base=private/label;root=base/'workspace';pkg=base/'sealed-source/pkg-one';root.mkdir(parents=True)
  manifest='[package]\nname="same-name"\nversion="0.1.0"\nedition="2024"\n';code='pub fn first_party_source_fixture() {}\n'
  write(pkg/'Cargo.toml',manifest);write(pkg/'src/lib.rs',code);write(pkg/'.cargo-checksum.json',json.dumps({'files':{'Cargo.toml':sha(manifest.encode()),'src/lib.rs':sha(code.encode())},'package':None}))
  write(root/'Cargo.toml','[package]\nname="opensip-serialization-probe"\nversion="0.1.0"\nedition="2024"\n[dependencies]\ndep = {package="same-name", version="=0.1.0", git="https://example.invalid/repo", branch='+json.dumps(branch)+'}\n')
  write(root/'src/lib.rs','pub fn first_party_fixture() {}\n')
  write(root/'.cargo/config.toml','[source.original-git]\ngit="https://example.invalid/repo"\nbranch='+json.dumps(branch)+'\nreplace-with="sealed-git"\n[source.sealed-git]\ndirectory='+json.dumps(str(base/'sealed-source'))+'\n')
  lock_source='git+https://example.invalid/repo?branch='+form_encode(branch)+'#'+('0'*40)
  expected_metadata_source='git+https://example.invalid/repo?branch='+branch+'#'+('0'*40)
  lock='version=4\n[[package]]\nname="opensip-serialization-probe"\nversion="0.1.0"\ndependencies=["same-name"]\n[[package]]\nname="same-name"\nversion="0.1.0"\nsource='+json.dumps(lock_source)+'\n';write(root/'Cargo.lock',lock);before=(root/'Cargo.lock').read_bytes()
  cmd=[executable,'metadata','--locked','--offline','--frozen','--format-version','1','--filter-platform','aarch64-apple-darwin'];result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=60)
  (R/(label+'.stdout')).write_bytes(result.stdout);(R/(label+'.stderr')).write_bytes(result.stderr);assert (root/'Cargo.lock').read_bytes()==before
  observed=None;key_mismatch=None
  if result.returncode==0:
   packages=[p for p in json.loads(result.stdout)['packages'] if p['name']=='same-name'];assert len(packages)==1;observed=packages[0]['source'];assert observed==expected_metadata_source
   assert Path(packages[0]['manifest_path'])==pkg/'Cargo.toml'
   # These vectors use only exact three-string arrays; no host path in the key recipe.
   a=json.dumps(['same-name','0.1.0',lock_source],ensure_ascii=False,separators=(',',':')).encode();b=json.dumps(['same-name','0.1.0',observed],ensure_ascii=False,separators=(',',':')).encode();key_mismatch=sha(a)!=sha(b)
  rows.append({'case':label,'branch':branch,'argv':cmd,'cwd':str(root),'exitCode':result.returncode,'lockSourceId':lock_source,'expectedMetadataSource':expected_metadata_source,'observedMetadataSource':observed,'directStringEquality':lock_source==observed if observed else None,'substitutingMetadataSourceChangesPackageKey':key_mismatch,'lockBytesUnchanged':True,'stdoutBytes':len(result.stdout),'stdoutSha256':sha(result.stdout),'stderrBytes':len(result.stderr),'stderrSha256':sha(result.stderr),'sourceManifest':{'path':str(pkg/'Cargo.toml'),'sha256':sha(manifest.encode())},'sourceLibSha256':sha(code.encode())})
 assert all(r['exitCode']==0 for r in rows),rows
 assert rows[0]['directStringEquality'] is True and rows[1]['directStringEquality'] is False and rows[1]['substitutingMetadataSourceChangesPackageKey'] is True
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 report={'standing':'Actual installed Cargo metadata over two synthetic first-party Git-source replacement fixtures only. Null package checksum/zero revision are declared fixture assertions, not an authenticated Git checkout or registry archive. No native CC2/environment/carrier/profile/source/owner/custody/launch or product admission. No HOME assignment; user-prescribed CARGO_HOME=/Users/sb/.cargo. No network or fixture build/proc-macro/test execution requested. Exact source serializer bridge still needs complete publication.','privateTmpdir':str(private),'executable':{'path':executable,'sha256':sha(Path(executable).read_bytes())},'runs':rows,'R3Resolved':False,'productImplemented':False,'productQualification':False}
 (R/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
finally:
 if owned:LANE.rmdir()
