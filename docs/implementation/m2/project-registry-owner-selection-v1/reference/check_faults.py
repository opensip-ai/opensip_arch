from pathlib import Path
import json,subprocess,sys
D=Path(__file__).parent; source=(D/'registry_model.py').read_text(); runner=(D/'check_registry.py').read_bytes(); O=D/'fault-runs-r2';O.mkdir()
variants=[('baseline',None,None),('marker-prefix',"raw[:22]==b'opensip-project-id-v1\\n'","raw[:21]==b'opensip-project-id-v1\\n'"),('reuse-retired-project',"if kind=='reserve-random':","if False:"),('reuse-namespace',"require(prev is None or n > prev,'namespace-order-unique')","require(prev is None or n >= prev,'namespace-order-unique')"),('skip-live-project-uniqueness',"p not in ids and r not in roots and l not in paths","r not in roots and l not in paths"),('ignore-stop',"if stopped or durable_registry is not True:","if durable_registry is not True:"),('ninth-project-candidate','for p in project_candidates[:8]:','for p in project_candidates[:9]:'),('ordinary-inconsistent-prefix',"if row['allocationKind']=='random' and namespace_observation=='absent' and marker_observation=='exact':","if False:"),('adoption-completed-as-ordinary',"if row['allocationKind']=='adopt':","if row['allocationKind']=='adopt' and mode=='admitted-adoption':")]
results=[]
for name,before,after in variants:
 out=O/name;out.mkdir();code=source
 if before:
  assert source.count(before)==1,(name,source.count(before));code=source.replace(before,after)
 (out/'registry_model.py').write_text(code);(out/'check_registry.py').write_bytes(runner)
 c=subprocess.run([sys.executable,'-m','py_compile',str(out/'registry_model.py')],capture_output=True);assert c.returncode==0
 p=subprocess.run([sys.executable,str(out/'check_registry.py')],cwd=out,capture_output=True)
 (out/'stdout.txt').write_bytes(p.stdout);(out/'stderr.txt').write_bytes(p.stderr)
 assert (p.returncode==0)==(name=='baseline'),name
 if name!='baseline':assert b'AssertionError' in p.stderr,name
 results.append({'variant':name,'compiled':True,'exitCode':p.returncode,'detected':name!='baseline'})
(D/'fault-results.r4b.json').write_text(json.dumps({'standing':'Author pure-model fault controls, not native mutation/qualification','results':results},indent=2)+'\n');print(json.dumps(results))
