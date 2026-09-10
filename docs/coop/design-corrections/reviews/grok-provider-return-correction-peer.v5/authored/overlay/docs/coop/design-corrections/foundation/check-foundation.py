"""Retained adversarial cases. Runs only reference functions and local test signatures."""
import argparse,base64,copy,hashlib,importlib.util,json,platform,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
COMP=HERE.parents[1]/'completion'
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('test_canonical',HERE/'canonical.py');F=load('test_foundation',HERE/'host-foundation-model.v2.py');Q=load('test_quality',HERE/'g13-validator.v5.py')
checks=[]
def record(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
def refuses(fn):
 try:fn();return False
 except (ValueError,C.ValidationError):return True

def main(report):
 cases=json.loads((COMP/'host-foundation-cases.v1.json').read_text())['cases']
 base=copy.deepcopy(next(c['input'] for c in cases if c['id']=='compiled-profile-only'));base.pop('solverFixtureId',None)
 # The old unaffected cases retain their existing status contract. Detailed source
 # reason labels can change only for the added lexical gate, not D9 class.
 for case in cases:
  if case['kind'] not in ['configuration','policy','parser']:continue
  actual=F.evaluate(case['kind'],case['input'])
  expected=case['expected'].get('status')
  if expected is not None:record('inherited-status/'+case['id'],actual['status']==expected,actual.get('reason'))
 literals=['1.0','1e0','1E0','1.0000000000000001','9007199254740991.1','true','"1"','-0','0','-1','9007199254740992']
 for layer,path in [('global','host/settings.json'),('project','project/opensip.json'),('local','project/.opensip/local.json')]:
  for literal in ['1']+literals:
   x=copy.deepcopy(base);x.update(tty=True,ci=False)
   raw='{"schemaVersion":1,"analysis":{"budget":{"unit":"work-units","limit":'+literal+'}}}'
   # The global layer independently tests numeric schemaVersion admission.
   if layer=='global':raw='{"schemaVersion":'+literal+'}'
   x['files']={path:{'raw':raw}};out=F.configuration(x)
   record('numeric/'+layer+'/'+literal,(out['status']=='ACCEPT')==(literal=='1'),out.get('reason'))
 for field in ['defaults','hostEnvironment','hostFlags']:
  x=copy.deepcopy(base)
  if field=='defaults':x[field]['schemaVersion']=1.0
  else:x[field]={'analysis':{'budget':{'unit':'work-units','limit':1.0}}}
  record('typed-internal/'+field,F.configuration(x)['status']=='HOST-INVARIANT-FAILURE')
 for literal in ['1','1.0','1e0','true','"1"']:
  raw='{"policySchema":'+literal+',"policyScope":"global","grants":[],"denies":[],"consents":[]}'
  out=F.policy({'files':{'host/policies/permission-policy.json':{'raw':raw,'mode':384}}})
  record('policy-constant/'+literal,(out['status']=='ACCEPT')==(literal=='1'))
 # Canonical discriminators settle UR-1..5 with explicit independent byte goldens.
 vectors=[('key-plane',{'\ue000':0,'\U00010000':1},'{"\ue000":0,"\U00010000":1}'),
          ('integer-bounds',[0,-1,-2**63,2**64-1],'[0,-1,-9223372036854775808,18446744073709551615]'),
          ('nfd-preserved',{'s':'e\u0301'},'{"s":"e\u0301"}'),
          ('nfc-preserved',{'s':'é'},'{"s":"é"}'),
          ('escapes',{'s':'/\b\f\n\r\t\x01"\\é'},'{"s":"/\\b\\f\\n\\r\\t\\u0001\\"\\\\é"}')]
 for name,value,expected in vectors:
  record('canonical/'+name,C.canonical(value)==expected.encode('utf-8'))
  raw=expected.encode('utf-8');preimage=b'opensip.product.v1\0vector\0'+len(raw).to_bytes(8,'big')+raw
  record('domain-frame/'+name,C.identity('vector',value)==hashlib.sha256(preimage).hexdigest())
 for raw in [b'1.0',b'1e0',b'-0',b'NaN',b'Infinity',b'18446744073709551616',b'-9223372036854775809',b'"\\ud800"',b'{"a":1,"a":2}',b'{"a":1,"\\u0061":2}']:
  record('canonical-refusal/'+raw.decode(),refuses(lambda:C.parse(raw)))
 record('boolean-not-integer',refuses(lambda:C.validate({'type':'integer'},True)))
 record('boolean-not-const',refuses(lambda:C.validate({'const':1},True)))
 record('domain-separation',C.identity('a',{})!=C.identity('b',{}))
 # Independent expected atom counts for selected original corpus cells.
 expected_counts={'typescript.imports':{'acyclic':2,'cycle':3,'self':2,'unresolved':2,'malformed':2,'dynamic':2,'empty':1},
 'typescript.references':{'shadow':3,'malformed':2,'empty':1},'typescript.calls':{'acyclic':2,'malformed':2,'empty':1},
 'typescript.types':{'acyclic':2,'shadow':2,'malformed':2,'empty':1},'typescript.reachability':{'acyclic':2,'malformed':2,'empty':1},
 'host.integration':{'acyclic':2,'cycle':3,'self':3,'unresolved':3,'malformed':3,'dynamic':3,'shadow':2,'empty':2}}
 for row in Q.M['rows'][:6]:
  for project in row['projects']:record('oracle-count/'+row['capability']+'/'+project,len(Q.oracle(row,project))==expected_counts[row['capability']][project])
 sample=Q.OLD.reference();sample.update(schemaMajor=2,harnessDigest='d'*64)
 rows={r['id']:r for r in Q.M['rows']}
 for cell in sample['cells']:
  for f in cell['fixtureResults']:
   atoms=Q.oracle(rows[cell['cellId']],f['fixtureId']);f.update(actualObservations=atoms,expectedCount=len(atoms),actualCount=len(atoms))
 trusted={p['platform']:{k:p['runner'][k] for k in Q.OLD.HARDWARE} for p in sample['performance']}
 with tempfile.TemporaryDirectory(prefix='opensip-g13-test-sign-') as td:
  p=Path(td)
  subprocess.run(['openssl','genpkey','-algorithm','ED25519','-out',str(p/'key')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  public=subprocess.check_output(['openssl','pkey','-in',str(p/'key'),'-pubout']).decode()
  context={k:sample[k] for k in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest']}
  context.update(producerPublicKeyPem=public,baseline=None,trustedRunners=trusted)
  def sign(raw):
   (p/'message').write_bytes(Q.signature_message(raw,context))
   return subprocess.check_output(['openssl','pkeyutl','-sign','-inkey',str(p/'key'),'-rawin','-in',str(p/'message')])
  def accepted(value):
   raw=C.canonical(value);return Q.admit(raw,sign(raw),context)
  record('quality-valid-authenticated',accepted(sample))
  mutations=[]
  x=copy.deepcopy(sample);x['hostDigest']='b'*64;x['providerClosureDigest']='c'*64
  for pp in x['performance']:pp['runner'].update(hostDigest='b'*64,providerClosureDigest='c'*64)
  mutations.append(('consistently-relabelled-subject',x))
  x=copy.deepcopy(sample)
  for cell in x['cells']:
   for f in cell['fixtureResults']:f.update(expectedCount=0,actualCount=0,actualObservations=[])
  mutations.append(('zero-oracle-and-observations',x))
  x=copy.deepcopy(sample);x['cells'][0]['fixtureResults'][0]['actualObservations'][0]['value']='forged';mutations.append(('forged-observation',x))
  x=copy.deepcopy(sample);x['harnessDigest']='f'*64;mutations.append(('wrong-producer',x))
  x=copy.deepcopy(sample);x['performance'][0]['measurements']['coldDurationNs']=[10000000001]*30;mutations.append(('false-performance-pass',x))
  for name,value in mutations:record('quality-refusal/'+name,not accepted(value))
  raw=C.canonical(sample);sig=sign(raw)
  record('quality-signature-tamper',not Q.admit(raw,sig[:-1]+bytes([sig[-1]^1]),context))
  record('quality-unsigned',not Q.admit(raw,b'',context))
  float_raw=raw.replace(b'"schemaMajor":2',b'"schemaMajor":2.0')
  record('quality-float-schema',not Q.admit(float_raw,sign(float_raw),context))
 for depth in [32,33]:
  raw=(b'['*depth)+b'0'+(b']'*depth)
  record('canonical-depth-'+str(depth),refuses(lambda raw=raw:C.parse(raw))==(depth==33))
 out={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'environment':{'python':platform.python_version()},'productQualification':False,'signatureLimit':'Real temporary Ed25519 signatures test report integrity. Runner/producer observations are injected trusted qualification inputs, not measured product behavior.'}
 Path(report).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','passed','total']}))
 for c in checks:
  if not c['passed']:print(c)
 return 0 if out['status']=='PASS' else 1
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--report',required=True);raise SystemExit(main(p.parse_args().report))
