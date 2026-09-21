"""Only a known conditional semantic case mismatch counts as a model fault."""
from pathlib import Path
import ast,json,subprocess,sys
D=Path(__file__).parent;source=(D/'registry_model.py').read_text();out=D/'native-join-faults-r1';out.mkdir()
variants=[('baseline',None,None),('ignore-old-carrier',"if carrier!='DECODE_COMPLETE_V2': return 'UNAVAILABLE'","if False: return 'UNAVAILABLE'"),('ignore-profile',"if profile_observation!='qualified-macos-apfs-uuid-v1': return 'UNAVAILABLE'","if False: return 'UNAVAILABLE'"),('ignore-volatile',"if not volatile_consistent(volatile_before,volatile_after): return 'UNAVAILABLE'","if False: return 'UNAVAILABLE'"),('ignore-durable-and-marker',"return classify(document,root,marker_observation,tracking)","return 'MATCHED_ACTIVE'")]
results=[]
for name,before,after in variants:
 P=out/name;P.mkdir();code=source
 if before is not None:assert source.count(before)==1,(name,source.count(before));code=source.replace(before,after)
 (P/'registry_model.py').write_text(code);(P/'check_native_join.py').write_bytes((D/'check_native_join.py').read_bytes())
 c=subprocess.run([sys.executable,'-m','py_compile',str(P/'registry_model.py'),str(P/'check_native_join.py')],capture_output=True)
 (P/'compile.stdout').write_bytes(c.stdout);(P/'compile.stderr').write_bytes(c.stderr);assert c.returncode==0,(name,'compile failed')
 r=subprocess.run([sys.executable,'-B',str(P/'check_native_join.py')],capture_output=True,cwd=P,timeout=30);(P/'run.stdout').write_bytes(r.stdout);(P/'run.stderr').write_bytes(r.stderr)
 if name=='baseline':
  assert r.returncode==0;baseline=json.loads((P/'native-join-results.381.json').read_text());assert baseline['count']==19;expected_cases={c['name']:c['expected'] for c in baseline['cases']}
 else:
  assert r.returncode==1 and b'assert ok,(name,expected,observed)' in r.stderr
  last=r.stderr.decode().splitlines()[-1];assert last.startswith('AssertionError: ')
  value=ast.literal_eval(last[len('AssertionError: '):]);assert type(value) is tuple and len(value)==3
  case_name,expected,observed=value;assert case_name in expected_cases and expected_cases[case_name]==expected and expected!=observed
  assert b'FileNotFoundError' not in r.stderr and b'ImportError' not in r.stderr and b'SyntaxError' not in r.stderr
 results.append(dict(name=name,compiled=True,exitCode=r.returncode,semanticCaseAssertion=name!='baseline'))
(D/'native-join-fault-results.381.json').write_text(json.dumps(dict(standing='Pure model controls only; no native fault/OS qualification',results=results),indent=2)+'\n');print('Baseline19 passed;4 native-join semantic model faults detected')
