"""Pure source faults: only named semantic case assertion failures count."""
from pathlib import Path
import ast,json,subprocess,sys
D=Path(__file__).parent;source=(D/'registry_model.py').read_text();out=D/'persistent-faults-r2';out.mkdir()
variants=[
 ('baseline',None,None),
 ('accept-zero-uuid',"require(volume['value']!='0'*32,'volume-absent')","pass"),
 ('locator-inside-incarnation',"return (root['platform'],root['volumeIdentity']['kind']","return (root['canonicalPathBytesHex'],root['platform'],root['volumeIdentity']['kind']"),
 ('drop-volume-from-incarnation',"root['volumeIdentity']['kind'],root['volumeIdentity']['value'],",""),
 ('ignore-live-device-fsid-change','return before==after','return True'),
 ('ignore-legacy-carrier',"if old!='absent' or current=='unavailable':","if current=='unavailable':"),
 ('permit-unauthorized-init','if established or not authorized_pristine_creation:','if established:'),
 ('ignore-exact-durable-root',"if row['root']!=root or (pid is not None and pid!=row['projectId']):","if pid is not None and pid!=row['projectId']:")]
results=[]
for name,before,after in variants:
 P=out/name;P.mkdir();code=source
 if before is not None:assert source.count(before)==1,(name,source.count(before));code=source.replace(before,after)
 (P/'registry_model.py').write_text(code);(P/'check_persistent_root.py').write_bytes((D/'check_persistent_root.py').read_bytes())
 c=subprocess.run([sys.executable,'-m','py_compile',str(P/'registry_model.py'),str(P/'check_persistent_root.py')],capture_output=True)
 (P/'compile.stdout').write_bytes(c.stdout);(P/'compile.stderr').write_bytes(c.stderr);assert c.returncode==0,(name,'compile failed')
 r=subprocess.run([sys.executable,'-B',str(P/'check_persistent_root.py')],capture_output=True,cwd=P,timeout=30)
 (P/'run.stdout').write_bytes(r.stdout);(P/'run.stderr').write_bytes(r.stderr)
 if name=='baseline':
  assert r.returncode==0
  baseline=json.loads((P/'persistent-results.379.json').read_text());assert baseline['count']==69
  expected_cases={c['name']:c['expected'] for c in baseline['cases']}
 else:
  # Every case uses assert ok,(name,expected,result), so only that exact traceback
  # plus semantic case tuple is accepted. Import/IO/timeouts/unrelated failures fail.
  assert r.returncode==1 and b'assert ok,(name,expected,result)' in r.stderr and b'AssertionError: ' in r.stderr,(name,r.stderr.decode())
  last=r.stderr.decode().splitlines()[-1]
  assert last.startswith('AssertionError: ')
  value=ast.literal_eval(last[len('AssertionError: '):]);assert type(value) is tuple and len(value)==3
  case_name,expected,observed=value
  assert case_name in expected_cases and expected_cases[case_name]==expected and expected!=observed
  assert b'FileNotFoundError' not in r.stderr and b'ImportError' not in r.stderr and b'SyntaxError' not in r.stderr
 results.append(dict(name=name,compiled=True,exitCode=r.returncode,semanticCaseAssertion=name!='baseline'))
(D/'persistent-fault-results.379-r2.json').write_text(json.dumps(dict(standing='Pure model controls only; not native compiled faults or OS qualification',results=results),indent=2)+'\n');print('Baseline69 passed;7 semantic model faults detected')
