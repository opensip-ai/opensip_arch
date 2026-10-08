from pathlib import Path
import json, os, subprocess, tempfile, time
B=Path('/tmp/opensip-implementation/o1-definition-r2-preparation');B.mkdir(exist_ok=True)
root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-o1-assertion-',dir=root));private.chmod(0o700)
 source=B/'assertion-probe.rs';source.write_text('fn main() { println!("{}", cfg!(debug_assertions)); }\n')
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip())
 rows=[]
 for name,assertions,opt in [('unoptimized-on','yes','0'),('optimized-on','yes','3'),('unoptimized-off','no','0'),('optimized-off','no','3')]:
  target=private/name
  args=['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','linker=/usr/bin/clang','-C','debug-assertions='+assertions,'-C','opt-level='+opt,str(source),'-o',str(target)]
  r=subprocess.run(args,env=env,capture_output=True,check=True);assert not r.stdout and not r.stderr
  out=subprocess.check_output([str(target)],env=env).decode().strip();assert out==('true' if assertions=='yes' else 'false')
  rows.append({'id':name,'debugAssertions':assertions,'optLevel':opt,'actualCfgDebugAssertions':out,'proposedMember':'debug-assertions-on' if out=='true' else 'debug-assertions-off'})
 (B/'assertion-probe.json').write_text(json.dumps({'standing':'ISOLATED BARE RUSTC COMPILED FACT OBSERVATION, not selected law or OpenSIP test/qualification','rustc':'1.95.0','edition':2024,'rows':rows,'buildScriptUsed':False,'cargoUsed':False,'productCodeChanged':False,'productQualification':False},indent=2)+'\n')
 print(json.dumps({'assertionPredicateControls':len(rows),'optimizationIndependent':True,'buildScriptUsed':False,'productQualification':False}))
finally:
 if owned:lane.rmdir()
