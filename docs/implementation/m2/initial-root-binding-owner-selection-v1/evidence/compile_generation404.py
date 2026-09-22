from pathlib import Path
import json,shutil,subprocess,hashlib
T=Path('/tmp/opensip-implementation');D=T/'initial-diagnostics-generation404';P=D/'product';result=json.loads((D/'generation/result.json').read_text());assert result['passed']
changes=[]
for row in result['outputs']:
 src=D/'generation/assembly/output'/row['path'];raw=src.read_bytes();assert len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'];dest=P/row['path']
 if dest.read_bytes()!=raw:changes.append(row['path'])
 dest.write_bytes(raw)
(D/'output-materialization.json').write_text(json.dumps({'standing':'Private prospective generation only; unselected.','changedOutputs':changes,'allOutputs':result['outputs']},indent=2)+'\n')
env=json.loads((T/'host-materialization368-r1/environment.json').read_text());env['CARGO_TARGET_DIR']=str(D/'target');env['RUST_TEST_THREADS']='1';(D/'compile-environment.json').write_text(json.dumps(env,indent=2)+'\n')
cmd=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','check','--locked','--offline','--workspace','--all-targets']
with (D/'workspace.stdout').open('wb')as out,(D/'workspace.stderr').open('wb')as err:r=subprocess.run(cmd,cwd=P,env=env,stdout=out,stderr=err)
(D/'compile-result.json').write_text(json.dumps({'command':cmd,'exitCode':r.returncode,'privateProduct':True,'sourceApproved':False},indent=2)+'\n');print('workspace',r.returncode,flush=True);assert r.returncode==0
