import os,pathlib,subprocess,tempfile,time,json
p=pathlib.Path('/tmp/opensip-implementation/c3-pinned-producer-source');lane=pathlib.Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock');owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(1)
try:
 tmp=tempfile.mkdtemp(prefix='opensip-c3-producer-',dir=str(lane.parent));os.chmod(tmp,0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=tmp,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CARGO_TARGET_DIR=str(p/'target'))
 for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(key,None)
 args=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','package','--no-verify','--locked','--offline','--allow-dirty']
 result=subprocess.run(args,cwd=p/'fixture',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(p/'package.log').write_bytes(result.stdout)
 (p/'package-run.json').write_text(json.dumps({'argv':args,'exitCode':result.returncode,'privateTmpdir':tmp,'productQualification':False,'repositoryModified':False},indent=2)+'\n')
 print(result.stdout.decode());raise SystemExit(result.returncode)
finally:
 if owned:lane.rmdir()
