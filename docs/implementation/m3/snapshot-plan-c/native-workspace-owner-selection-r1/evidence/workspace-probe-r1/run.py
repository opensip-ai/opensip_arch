"""Synthetic first-party workspace metadata observation only; not native admission."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time
R=Path('/tmp/opensip-implementation/native-workspace-owner-probe-r1'); LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
try:
 while not owned:
  try:LANE.mkdir();owned=True
  except FileExistsError:print('Waiting for shared lane; no child launched.',flush=True);time.sleep(15)
 private=Path(tempfile.mkdtemp(prefix='opensip-workspace-owner-',dir=LANE.parent));os.chmod(private,0o700)
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 exe='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';rows=[]
 root=private/'snapshot/workspace';root.mkdir(parents=True)
 write(root/'Cargo.toml','[workspace]\nresolver="3"\nmembers=["members/a","members/b"]\nexclude=["deps/external","deps/dormant"]\n')
 for rel,name in [('members/a','member-a'),('members/b','member-b'),('deps/external','external'),('deps/dormant','dormant')]:
  text='[package]\nname='+json.dumps(name)+'\nversion="0.1.0"\nedition="2024"\n'
  if name=='member-a':text+='[dependencies]\nmember-b={path="../b"}\nexternal={path="../../deps/external"}\ndormant={path="../../deps/dormant",optional=true}\n'
  write(root/rel/'Cargo.toml',text);write(root/rel/'src/lib.rs','pub fn fixture_only() {}\n')
 lock='version=4\n'
 for name in ['dormant','external','member-a','member-b']:
  lock+='[[package]]\nname='+json.dumps(name)+'\nversion="0.1.0"\n'
  if name=='member-a':lock+='dependencies=["dormant","external","member-b"]\n'
 write(root/'Cargo.lock',lock)
 for label,cwd in [('workspace-and-path',root),('equal-tuple-root-one',private/'snapshot/one'),('equal-tuple-root-two',private/'snapshot/two')]:
  if cwd!=root:
   write(cwd/'Cargo.toml','[package]\nname="same-path-package"\nversion="0.1.0"\nedition="2024"\n');write(cwd/'src/lib.rs','pub fn fixture_only() {}\n');write(cwd/'Cargo.lock','version=4\n[[package]]\nname="same-path-package"\nversion="0.1.0"\n')
  before=(cwd/'Cargo.lock').read_bytes();cmd=[exe,'metadata','--locked','--offline','--frozen','--format-version','1','--filter-platform','aarch64-apple-darwin'];out=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=60)
  (R/(label+'.stdout')).write_bytes(out.stdout);(R/(label+'.stderr')).write_bytes(out.stderr)
  assert out.returncode==0,(label,out.stderr.decode());assert before==(cwd/'Cargo.lock').read_bytes();m=json.loads(out.stdout)
  names={p['id']:p['name'] for p in m['packages']};assert len(names)==len(m['packages']);members=[names[i] for i in m['workspace_members']]
  if cwd==root:
   assert set(members)=={'member-a','member-b'};assert set(names.values())=={'member-a','member-b','external'}
   assert (root/'deps/dormant/Cargo.toml').exists() and b'dormant' in before
   a=next(n for n in m['resolve']['nodes'] if names[n['id']]=='member-a');assert {names[d['pkg']] for d in a['deps']}=={'member-b','external'}
  else:assert members==['same-path-package']
  assert all(p['source'] is None for p in m['packages'])
  retained=[{'path':p.relative_to(private/'snapshot').as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(cwd.rglob('*')) if p.is_file()]
  rows.append({'case':label,'argv':cmd,'cwd':str(cwd),'exitCode':out.returncode,'lockBytesUnchanged':True,'workspaceMemberNames':members,'observedPackageNames':sorted(names.values()),'observedPackages':[{'name':p['name'],'version':p['version'],'source':p['source'],'id':p['id'],'manifest_path':p['manifest_path']} for p in m['packages']],'retainedFixtureFiles':retained,'stdoutBytes':len(out.stdout),'stdoutSha256':sha(out.stdout),'stderrBytes':len(out.stderr),'stderrSha256':sha(out.stderr)})
 assert rows[1]['observedPackages'][0]['id']!=rows[2]['observedPackages'][0]['id']
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 report={'standing':'Three actual installed Cargo metadata observations over synthetic first-party path/workspace fixtures only. No fixture code build or execution, no HOME assignment; prescribed CARGO_HOME=/Users/sb/.cargo. Native CC2/constructed environment/profile/source/owner/custody/admission/qualification are not established. Absolute ids/manifest paths and retained fixture ledger are operational evidence, not admitted semantic witnesses. Inactive path fixture is retained in its lock and tree despite omission from metadata graph; no authority to prune acquired candidates.','privateTmpdir':str(private),'executable':{'path':exe,'sha256':sha(Path(exe).read_bytes())},'runs':rows,'R3Resolved':False,'productImplemented':False,'productQualification':False}
 (R/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
finally:
 if owned:LANE.rmdir()
