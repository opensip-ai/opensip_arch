"""Isolated first-party fixture probe; not native adapter or product admission."""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile,time
R=Path('/tmp/opensip-implementation/native-source-namespace-probe-r2');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
try:
 while not owned:
  try:LANE.mkdir();owned=True
  except FileExistsError:print('Waiting for shared lane; no child process launched.',flush=True);time.sleep(15)
 private=Path(tempfile.mkdtemp(prefix='opensip-native-source-probe-',dir=str(LANE.parent)));os.chmod(private,0o700)
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 executable='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
 rows=[];fixture_pins=[]
 for mode in ['separate-source-roots','shared-source-root-one-declaration']:
  base=private/mode;root=base/'workspace';root.mkdir(parents=True)
  for origin in ['one','two']:
   pkg=base/('sources/'+origin if mode=='separate-source-roots' else 'sources/shared')/('pkg-'+origin)
   manifest='[package]\nname = "same-name"\nversion = "0.1.0"\nedition = "2024"\n'
   code='pub const ORIGIN: &str = "'+origin+'";\n';write(pkg/'Cargo.toml',manifest);write(pkg/'src/lib.rs',code)
   checksum={'files':{'Cargo.toml':sha(manifest.encode()),'src/lib.rs':sha(code.encode())},'package':'0'*64};write(pkg/'.cargo-checksum.json',json.dumps(checksum))
   fixture_pins.append({'mode':mode,'origin':origin,'directory':str(pkg),'members':[{'path':n,'bytes':len((pkg/n).read_bytes()),'sha256':sha((pkg/n).read_bytes())}for n in ['Cargo.toml','src/lib.rs','.cargo-checksum.json']]})
  write(root/'Cargo.toml','[package]\nname = "opensip-source-namespace-probe"\nversion = "0.1.0"\nedition = "2024"\n[dependencies]\ndep_one = {package="same-name", version="=0.1.0", registry="one"}\ndep_two = {package="same-name", version="=0.1.0", registry="two"}\n')
  write(root/'src/lib.rs','pub fn first_party_fixture() {}\n')
  config=''
  for origin in ['one','two']:
   config+=f'[registries.{origin}]\nindex = "https://example.invalid/{origin}"\n[source.{origin}]\nregistry = "https://example.invalid/{origin}"\nreplace-with = "'+('sealed-'+origin if mode=='separate-source-roots' else 'sealed')+'"\n'
   if mode=='separate-source-roots':config+=f'[source.sealed-{origin}]\ndirectory = '+json.dumps(str(base/'sources'/origin))+'\n'
  if mode!='separate-source-roots':config+='[source.sealed]\ndirectory = '+json.dumps(str(base/'sources/shared'))+'\n'
  write(root/'.cargo/config.toml',config)
  lock='version = 4\n[[package]]\nname = "opensip-source-namespace-probe"\nversion = "0.1.0"\ndependencies = ["same-name 0.1.0 (registry+https://example.invalid/one)", "same-name 0.1.0 (registry+https://example.invalid/two)"]\n'
  for origin in ['one','two']:lock+=f'[[package]]\nname = "same-name"\nversion = "0.1.0"\nsource = "registry+https://example.invalid/{origin}"\nchecksum = "'+('0'*64)+'"\n'
  write(root/'Cargo.lock',lock);before=(root/'Cargo.lock').read_bytes()
  cmd=[executable,'metadata','--locked','--offline','--frozen','--format-version','1','--filter-platform','aarch64-apple-darwin']
  result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=60)
  (R/(mode+'.stdout')).write_bytes(result.stdout);(R/(mode+'.stderr')).write_bytes(result.stderr)
  assert (root/'Cargo.lock').read_bytes()==before
  packages=[]
  if result.returncode==0:
   data=json.loads(result.stdout)
   for p in data['packages']:
    if p['name']=='same-name':packages.append({'id':p['id'],'source':p['source'],'manifest_path':p['manifest_path'],'actualLibSha256':sha((Path(p['manifest_path']).parent/'src/lib.rs').read_bytes())})
  rows.append({'mode':mode,'argv':cmd,'cwd':str(root),'exitCode':result.returncode,'stdoutBytes':len(result.stdout),'stdoutSha256':sha(result.stdout),'stderrBytes':len(result.stderr),'stderrSha256':sha(result.stderr),'packages':packages,'lockBytesUnchanged':True})
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 report={'standing':'Actual installed pinned Cargo metadata over synthetic first-party fixtures. No native carrier/adapter/owner/source/custody/product admission or qualification. Zero lock checksums are self-asserted fixture values, never authenticated tarballs. No network or repository build/proc-macro/test execution requested. Ordinary owned lane/private0700TMPDIR; no HOME assignment; CARGO_HOME remains user-prescribed /Users/sb/.cargo, so CC2/native constructed environment is NOT asserted.','privateTmpdir':str(private),'executable':{'path':executable,'sha256':sha(Path(executable).read_bytes())},'fixtureMembers':fixture_pins,'runs':rows,'productImplemented':False,'ownerMappingPublished':False,'R3Resolved':False,'productQualification':False}
 (R/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'runs':rows,'report':str(R/'report.json'),'productAdmissionAsserted':False},indent=2),flush=True)
finally:
 if owned:LANE.rmdir()
