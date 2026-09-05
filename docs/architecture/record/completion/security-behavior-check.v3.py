"""Validate authored design cases; optional report path keeps frozen sources immutable."""
import argparse, copy, hashlib, importlib.util, json
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('model',P/'security-behavior-model.v3.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def contains(actual,expected):
 if isinstance(expected,dict):return isinstance(actual,dict) and all(k in actual and contains(actual[k],v) for k,v in expected.items())
 return actual==expected
obj=json.loads((P/'security-behavior-cases.v3.json').read_text());results=[]
for source,pin in obj['sources'].items():assert hashlib.sha256((P.parent/'artifacts'/(source+'.json')).read_bytes()).hexdigest()==pin,source
repair_pin=obj['repairReviewPin'];assert hashlib.sha256((P/repair_pin['path']).read_bytes()).hexdigest()==repair_pin['sha256'],'repair review pin changed'
ids=set()
for c in obj['cases']:
 assert c['id'] not in ids;ids.add(c['id'])
 actual=m.run(c); errors=[]
 if c['model']=='airgap':
  for manifest in c['input']['payload'].get('manifests',[]):
   if hashlib.sha256((P/manifest['fixturePath']).read_bytes()).hexdigest()!=manifest['sha256']:errors.append('manifest fixture pin changed')
 if c['model']=='doctor-reader':
  import jsonschema
  schema=json.loads((P/'security-behavior-doctor-schema.v3.json').read_text())
  schema_valid=not list(jsonschema.Draft202012Validator(schema).iter_errors(c['input']['report']))
  if c['expected'].get('accepted') and not schema_valid:errors.append('full report schema refused accepted golden')
 if not contains(actual,c['expected']):errors.append('expected projection differs')
 if 'expectedComplete' in c and actual!=c['expectedComplete']:errors.append('complete oracle differs')
 if 'expectedDurableBeforeCrash' in c and actual['journal'][:len(c['expectedDurableBeforeCrash'])]!=c['expectedDurableBeforeCrash']:errors.append('durable prefix changed')
 for prop in c['properties']:
  if prop=='journal-invariants':
   js=actual['journal'];seq=[r['seq'] for r in js]
   if seq!=list(range(1,len(js)+1)):errors.append('non-contiguous sequence')
   rev=next((r['seq'] for r in js if r['type'] in ('REV','EXPIRY')),None)
   if rev is not None and any(r['seq']>rev and r['type'] in ('RA','RCI','ICI') for r in js):errors.append('post-revocation intent')
   for req in actual['initiated']:
    if not any(r.get('request')==req and r['type'] in ('RCI','ICI') for r in js):errors.append('effect without intent')
   if sum(r['type']=='CLN' for r in js)>1:errors.append('duplicate cleanup')
  elif prop=='no-undo-wording':
   raw=json.dumps(actual).lower()
   for forbidden in ('undone','reversed','rollback','compensated','contained','mitigated'):
    if forbidden in raw:errors.append('dishonest wording '+forbidden)
  elif prop=='secret-noninterference':
   altered=copy.deepcopy(c);altered['input']['secret']='OTHER-SECRET-29439';altered['input']['projectPath']='/different/private/path'
   if m.run(altered)!=actual:errors.append('classified secret affects output')
   if c['input']['secret'] in json.dumps(actual):errors.append('secret output')
  else:raise ValueError(prop)
 results.append({'id':c['id'],'classes':c['classes'],'status':'FAIL' if errors else 'PASS','errors':errors,'actual':actual})
# Compare whole normalized outputs across paired clock and transport perturbations.
pairs={}
for case,result in zip(obj['cases'],results):
 if case['model']=='journal':
  key=json.dumps({k:v for k,v in case['input'].items() if k!='clockPerturbation'},sort_keys=True)
  if key in pairs and pairs[key]!=result['actual']:
   result['status']='FAIL';result['errors'].append('paired whole journal/decision invariance failed')
  else:pairs[key]=result['actual']
# Supplemental executions prove local child env construction and ambient negative-space only.
# No four-platform, confinement, product, crypto, or kernel qualification is inferred.
import os, subprocess, sys, tempfile
local=[]
with tempfile.TemporaryDirectory(prefix='opensip-security-design-') as td:
 root=Path(td); (root/'outside.txt').write_bytes(b'ambient-read-observed\n')
 env={'A':'allowed','LANG':'C'}
 prior_b=os.environ.get('B');os.environ['B']='host-only-secret'
 r=subprocess.run(['/usr/bin/env','-0'],env=env,capture_output=True,check=True)
 if prior_b is None:del os.environ['B']
 else:os.environ['B']=prior_b
 actual=dict(part.decode().split('=',1) for part in r.stdout.split(b'\0') if part)
 local.append({'id':'local-environment-child','status':'PASS' if actual==env else 'FAIL','observed':actual,'scope':'Actual /usr/bin/env child reports only constructed variables; no claim about learning secrets by other means.'})
 for name,code in [('ambient-read','from pathlib import Path; print(Path('+repr(str(root/'outside.txt'))+').read_text(),end="")'),('ambient-write','from pathlib import Path; Path('+repr(str(root/'ambient-write'))+').write_bytes(b"written")'),('ambient-exec','print("child-executed")')]:
  out=subprocess.run([sys.executable,'-I','-S','-c',code],capture_output=True,check=True)
  local.append({'id':name,'status':'PASS','stdoutHex':out.stdout.hex(),'hostJournal':[],'scope':'Unconstrained local process under denied model grant; no OS sandbox claimed.'})
 # Loopback socket actual transfer avoids external service dependency.
 import socket,threading
 server=socket.socket();server.bind(('127.0.0.1',0));server.listen(1);captured=[]
 def recv():
  conn,_=server.accept();captured.append(conn.recv(100));conn.close()
 th=threading.Thread(target=recv);th.start()
 subprocess.run([sys.executable,'-I','-S','-c','import socket; s=socket.create_connection('+repr(server.getsockname())+'); s.sendall(b"ambient-egress"); s.close()'],check=True)
 th.join();server.close();local.append({'id':'ambient-egress','status':'PASS' if captured==[b'ambient-egress'] else 'FAIL','receivedHex':captured[0].hex(),'hostJournal':[],'scope':'Local loopback only; demonstrates absence of host mediation, not Internet reachability.'})
for r in local:
 r['classes']=['FX-3'] if r['id']=='local-environment-child' else ['FX-2B','FX-8']
 results.append(r)
report={'schemaVersion':1,'standing':'DESIGN-EVIDENCE-ONLY','status':'PASS' if all(r['status']=='PASS' for r in results) else 'FAIL','caseCount':len(obj['cases']),'localProbeCount':len(local),'passCount':sum(r['status']=='PASS' for r in results),'sources':obj['sources'],'repairReviewPin':repair_pin,'artifactPins':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['security-behavior-model.v3.py','security-behavior-author.v3.py','security-behavior-cases.v3.json','security-behavior-check.v3.py','security-behavior-doctor-schema.v3.json']},'results':results}
a=argparse.ArgumentParser();a.add_argument('--report',default=str(P/'security-behavior-report.v3.json'));args=a.parse_args();Path(args.report).write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['passCount'],'/',len(results))
for r in results:
 if r['status']!='PASS':print(r['id'],r.get('errors'),r.get('actual'))
raise SystemExit(0 if report['status']=='PASS' else 1)
