"""Execute doctor/cache design fixtures; no product or measured RSS qualification."""
import argparse,copy,hashlib,importlib.util,json,statistics,subprocess,tempfile
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('security_behavior',B/'security-behavior-model.v3.py');security=importlib.util.module_from_spec(spec);spec.loader.exec_module(security)

def doctor_reader(x):
 raw=x['raw'].encode('utf-8');preserved=SHA(raw)
 def refuse(reason):return {'accepted':False,'reason':reason,'renderedMembers':[],'originalSha256':preserved}
 try:
  def unique(pairs):
   result={}
   for k,v in pairs:
    if k in result:raise ValueError('duplicate')
    result[k]=v
   return result
  def invalid_constant(value):raise ValueError('non-JSON constant')
  value=json.loads(raw,object_pairs_hook=unique,parse_constant=invalid_constant)
  if not isinstance(value,dict) or type(value.get('schemaVersion')) is not int:return refuse('MALFORMED-DOCTOR-REPORT')
  if value['schemaVersion']!=1:return refuse('UNSUPPORTED-DOCTOR-MAJOR')
  valid=security.doctor_reader({'report':value,'events':x.get('events')})
  if not valid['accepted']:return refuse('MALFORMED-DOCTOR-REPORT')
  return {'accepted':True,'mode':value['mode'],'outcome':value['outcome'],'renderedMembers':['mode','outcome'],'originalSha256':preserved}
 except (ValueError,TypeError,UnicodeError):return refuse('MALFORMED-DOCTOR-REPORT')

def withdrawal(x):
 valid=type(x['elapsedDays']) is int and x['elapsedDays']>=0 and type(x['subsequentHostMinors']) is int and x['subsequentHostMinors']>=0
 if not valid:return {'eligible':False,'reason':'MALFORMED-WINDOW-OBSERVATION'}
 eligible=x['revoked'] or (x['elapsedDays']>=90 and x['subsequentHostMinors']>=1)
 return {'eligible':bool(eligible),'reason':'REVOCATION-OVERRIDE' if x['revoked'] else 'BOTH-MINIMA-MET' if eligible else 'RETAIN-SAME-MAJOR-SUPPORT'}

def mode(x):
 # Real reads are confined to a temporary reference fixture; operations recorded.
 with tempfile.TemporaryDirectory(prefix='opensip-doctor-mode-') as td:
  root=Path(td);reads=[];checks=[]
  for p,value in x['files'].items():
   f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(bytes.fromhex(value))
  def read(p):
   reads.append(p)
   try:
    raw=(root/p).read_bytes()
    if x.get('resourceLimitReachedOn')==p:return 'UNDETERMINED'
    value=json.loads(raw)
    if p=='project/lock.json' and not security.schema_ok(value,json.loads((B/'component-lock-schema.completed.v2.json').read_text())):return 'UNDETERMINED'
    return 'PASS' if isinstance(value,dict) else 'UNDETERMINED'
   except (OSError,ValueError,UnicodeError):return 'UNDETERMINED'
  selected='core' if x['explicit']=='core' or (x['explicit'] is None and not x['projectSelected']) else 'project'
  checks.append({'id':'host-inventory','status':read('host/inventory.json')})
  checks.append({'id':'host-settings','status':read('host/settings.json')})
  if selected=='core':checks.extend({'id':k,'status':'NOT-APPLICABLE'} for k in ['project-config','project-lock'])
  else:
   checks.append({'id':'project-config','status':read('project/opensip.json')})
   if x['interactive'] and 'project/local.json' in x['files']:checks.append({'id':'local-override','status':read('project/local.json')})
   checks.append({'id':'project-lock','status':read('project/lock.json')})
  return {'mode':selected,'checks':checks,'trace':{'reads':reads,'processes':[],'network':[],'writes':[],'analysisInputs':[]},'analysisAdmitted':False}

def mode_trace(x):
 allowed={'host/inventory.json','host/settings.json'}
 if x['mode']=='project':allowed|={'project/opensip.json','project/lock.json'}|({'project/local.json'} if x['interactive'] else set())
 tr=x['trace'];valid=all(p in allowed for p in tr['reads']) and all(not tr[k] for k in ['processes','network','writes','analysisInputs'])
 return {'accepted':valid}

def rss(x):
 if x.get('consentedProbe'):return {'status':'OUTSIDE-READ-ONLY-G04','scored':False}
 try:
  if x['mode'] not in ['core','requested-core','project','unresolved-project'] or x['platform'] not in ['macos-arm64','macos-x86_64','linux-arm64','linux-x86_64'] or len(x['launches'])!=21:raise ValueError()
  scored=[]
  for index,launch in enumerate(x['launches']):
   if launch['launchId']!=index+1 or launch['warmPair'] is not False or launch['target']!='spawned-measurement-process-T':raise ValueError()
   samples=launch['samples'];end=launch['exitMs']
   if not samples or [s['elapsedMs'] for s in samples]!=list(range(0,end,10)):raise ValueError()
   if any(type(s['rssBytes']) is not int or s['rssBytes']<0 for s in samples):raise ValueError()
   steady_samples=[s['rssBytes'] for s in samples if s['elapsedMs']>=20] or [s['rssBytes'] for s in samples]
   steady=statistics.median(steady_samples);peak=max(s['rssBytes'] for s in samples)
   scored.append({'launchId':index+1,'steadyBytes':steady,'peakBytes':peak,'passed':steady<=60_000_000 and peak<=100_000_000})
  return {'status':'PASS' if all(s['passed'] for s in scored) else 'FAIL','scored':True,'launches':scored,'measurement':'SYNTHETIC-TRACE-SCORING-ONLY'}
 except (KeyError,ValueError,TypeError):return {'status':'NON-PASS','scored':False}

def artifact(x):
 observed=SHA(bytes.fromhex(x['payloadHex']))
 if observed!=x['manifestDigest']:return {'accepted':False,'reason':'ARTIFACT-DIGEST-MISMATCH'}
 if x['catalogDigest']!=x['manifestDigest'] or not x['bindingCurrent']:return {'accepted':False,'reason':'CATALOG-MANIFEST-BINDING-MISMATCH'}
 if not x['trustCurrent'] or x['revoked']:return {'accepted':False,'reason':'CURRENT-TRUST-REFUSAL'}
 return {'accepted':True,'reason':'SAME-BYTE-ADMISSION-AS-FRESH'}

def contains(actual,expected):return isinstance(actual,dict) and all(k in actual and contains(actual[k],v) for k,v in expected.items()) if isinstance(expected,dict) else actual==expected

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path,default=B/'doctor-cache-report.v1.json');parser.add_argument('--typescript-root',type=Path,default=Path('/tmp/opensip-architecture-typescript/node_modules/typescript'));args=parser.parse_args()
 contract=json.loads((B/'doctor-cache-contract.v1.json').read_text());cases=json.loads((B/'doctor-cache-cases.v1.json').read_text());results=[]
 for pin in contract['sourcePins']:
  raw=(ROOT/pin['path']).read_bytes()
  if 'startHeading' in pin:
   text=raw.decode();raw=text[text.index(pin['startHeading']):text.index(pin['endHeading'])].encode()
  results.append({'id':'pin/'+pin['path']+pin.get('startHeading',''),'passed':SHA(raw)==pin['sha256']})
 matrix=json.loads((B/'compatibility-matrix.completed.v4.json').read_text());surface=next(r for r in matrix['rows'] if r['id']=='S-DOCTOR')
 actual_surface={'writer':surface['currentWriter'],'readerMin':surface['supportedReaders']['minMajor'],'readerMax':surface['supportedReaders']['maxMajor'],'days':surface['supportedReaders']['sameMajorSupportDays'],'minors':surface['supportedReaders']['subsequentHostMinors'],'revocationOverrides':surface['supportedReaders']['revocationOverrides'],'gates':surface['testEvidence']}
 expected_surface={'writer':1,'readerMin':1,'readerMax':1,'days':90,'minors':1,'revocationOverrides':True,'gates':[contract['gates'][g] for g in ['G12','G20','G32']]}
 results.append({'id':'matrix/S-DOCTOR','passed':actual_surface==expected_surface,'actual':actual_surface,'expected':expected_surface})
 methods={'reader':doctor_reader,'window':withdrawal,'mode':mode,'mode-trace':mode_trace,'rss':rss,'artifact':artifact}
 for case in cases['cases']:
  actual=methods[case['model']](case['input']);results.append({'id':case['id'],'gates':case['gates'],'passed':contains(actual,case['expected']),'expected':case['expected'],'actual':actual})
 with tempfile.TemporaryDirectory(prefix='opensip-cache-regeneration-') as td:
  root=Path(td);runs=[];before={}
  for case in cases['cacheCases']:
   cache=root/case['id'];
   if case['files'] is not None:
    cache.mkdir()
    for name,hexbytes in case['files'].items():(cache/name).write_bytes(bytes.fromhex(hexbytes))
   before[case['id']]={p.name:SHA(p.read_bytes()) for p in cache.iterdir()} if cache.exists() else None
   runs.append({'id':case['id'],'project':case['project'],'cacheState':case['state'],'cacheRoot':str(cache)})
  inp=root/'input.json';out=root/'output.json';inp.write_text(json.dumps(runs))
  subprocess.run(['node',str(B/'doctor-cache-native.v1.cjs'),'--typescript-root',str(args.typescript_root),'--input',str(inp),'--report',str(out)],check=True)
  native=json.loads(out.read_text());fresh={}
  if [r['id'] for r in native['results']]!=[c['id'] for c in cases['cacheCases']]:raise ValueError('native invocation coverage mismatch')
  for case,actual in zip(cases['cacheCases'],native['results']):
   cache=root/case['id'];after={p.name:SHA(p.read_bytes()) for p in cache.iterdir()} if cache.exists() else None
   semantic=actual['semantic'];same=case['state']=='fresh' or semantic==fresh[case['project']]
   if case['state']=='fresh':fresh[case['project']]=semantic
   valid=semantic==case['expected'] and same and after==before[case['id']] and actual['trace']['cacheReads']==0 and actual['trace']['durableResultRestores']==0 and len(actual['trace']['projectFilesRead'])==len(actual['inputFileObservations'])
   results.append({'id':case['id'],'gates':[contract['gates']['G18']],'passed':valid,'expected':case['expected'],'actual':actual,'equalFresh':same,'cacheUnchanged':after==before[case['id']]})
 report={'standing':'DESIGN-EVIDENCE-ONLY','productQualification':False,'performanceMeasurement':False,'total':len(results),'passed':sum(r['passed'] for r in results),'pins':{p.name:SHA(p.read_bytes()) for p in [Path(__file__),B/'doctor-cache-native.v1.cjs',B/'doctor-cache-contract.v1.json',B/'doctor-cache-cases.v1.json']},'compiler':{k:v for k,v in native.items() if k!='results'},'results':results}
 args.report.write_text(json.dumps(report,indent=2)+'\n');print(report['passed'],'/',report['total'])
 for r in results:
  if not r['passed']:print(json.dumps(r))
 return 0 if report['passed']==report['total'] else 1
if __name__=='__main__':raise SystemExit(main())
