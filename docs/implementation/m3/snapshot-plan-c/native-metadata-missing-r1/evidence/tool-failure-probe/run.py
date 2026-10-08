"""Actual synthetic fixture failures, not a selected public failure route."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time
R=Path('/tmp/opensip-implementation/native-tool-failure-probe-r1');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
try:
 while not owned:
  try:LANE.mkdir();owned=True
  except FileExistsError:print('Waiting for shared lane; no child launched.',flush=True);time.sleep(15)
 private=Path(tempfile.mkdtemp(prefix='opensip-native-tool-failure-',dir=LANE.parent));os.chmod(private,0o700)
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 exe='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';rows=[]
 for label in ['known-missing-path-manifest','known-malformed-path-manifest']:
  base=private/label;root=base/'workspace';write(root/'Cargo.toml','[package]\nname="tool-failure-fixture"\nversion="0.1.0"\nedition="2024"\n[dependencies]\ndep={path="../dep"}\n');write(root/'src/lib.rs','pub fn fixture_only() {}\n')
  write(root/'Cargo.lock','version=4\n[[package]]\nname="dep"\nversion="0.1.0"\n[[package]]\nname="tool-failure-fixture"\nversion="0.1.0"\ndependencies=["dep"]\n')
  if label=='known-malformed-path-manifest':write(base/'dep/Cargo.toml','[package\nname="dep"\n');write(base/'dep/src/lib.rs','pub fn fixture_only() {}\n')
  before=(root/'Cargo.lock').read_bytes();cmd=[exe,'metadata','--locked','--offline','--frozen','--format-version','1','--filter-platform','aarch64-apple-darwin'];out=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=60)
  (R/(label+'.stdout')).write_bytes(out.stdout);(R/(label+'.stderr')).write_bytes(out.stderr);assert before==(root/'Cargo.lock').read_bytes();assert out.returncode!=0
  dep=base/'dep/Cargo.toml';assert dep.exists()==(label=='known-malformed-path-manifest')
  rows.append({'case':label,'argv':cmd,'cwd':str(root),'exitCode':out.returncode,'lockBytesUnchanged':True,'dependencyManifestExists':dep.exists(),'dependencyManifestSha256':sha(dep.read_bytes()) if dep.exists() else None,'constructedFixtureCause':'absent explicit path manifest' if not dep.exists() else 'retained malformed explicit path manifest','stdoutBytes':len(out.stdout),'stdoutSha256':sha(out.stdout),'stderrBytes':len(out.stderr),'stderrSha256':sha(out.stderr)})
 assert rows[0]['exitCode']==rows[1]['exitCode']==101;assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 report={'standing':'Actual installed Cargo1.95 metadata over two synthetic first-party failure fixtures, not native CC2/constructed environment/authenticated producer/source/owner admission. Known causes come from constructed fixture and actual manifest existence/bytes, not parsing English stderr or assigning a public origin/code. Both failures exit101; exit alone cannot establish missing input. No HOME assignment, prescribed CARGO_HOME=/Users/sb/.cargo. No fixture build/code/proc-macro execution requested, locks unchanged. Complete owning public failure/coverage composition is unselected here.','privateTmpdir':str(private),'executable':{'path':exe,'sha256':sha(Path(exe).read_bytes())},'runs':rows,'publicFailureRoutePublished':False,'R3Resolved':False,'productImplemented':False,'productQualification':False}
 (R/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
finally:
 if owned:LANE.rmdir()
