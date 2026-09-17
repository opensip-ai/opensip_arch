from pathlib import Path
import importlib.util,json,copy,lzma,hashlib,itertools,datetime,sys,unicodedata
assert sys.version_info[:3]==(3,12,13)and unicodedata.unidata_version=='15.0.0'
S=Path(__file__).resolve().parent;O=S/'checks-r3';assert not O.exists();O.mkdir()
def load(lane,name):
 p=S/lane/name;sp=importlib.util.spec_from_file_location('sec56_'+lane+str(len(name)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
name='docs/coop/design-corrections/security/security_lifecycle_model_v1.py';P=load('parent',name);N=load('candidate',name);V=load('parent','docs/coop/completion/security_unit_lib_v8.py');rows=[]
for r in json.loads((S/'parent-inputs.json').read_bytes())['files']:
 raw=(S/'parent'/r['path']).read_bytes();assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256'])
assert V.KIND_ROUTING['revocation']==('opensip.metadata.revocation.1','ROOT');assert N.ENVELOPE_KINDS['revocation']==('revocation v8','opensip.metadata.revocation.1','ROOT keys@rootThreshold')
assert {k:v for k,v in P.ENVELOPE_KINDS.items()if k!='revocation'}=={k:v for k,v in N.ENVELOPE_KINDS.items()if k!='revocation'}
# Candidate53 was not selected. Reproduce its complete qualified clock corpus,
# and prove these additional changes do not alter any of its1833 results.
clock_rows=[json.loads(l)for l in lzma.decompress((S/'clock53-cases.ndjson.xz').read_bytes()).split(b'\n')if l]
for r in clock_rows:
 q=r['input']
 try:out={'value':N.clock_decision(q['record'],q['observation'],q.get('payload'),q.get('reportOnly',False))}
 except N.Reject as e:out={'rejected':str(e)}
 assert out==r['candidate'],r['label']
f=json.loads((S/'parent/docs/coop/design-corrections/security/root-schema-cases.v1.json').read_bytes())
for c in f['rootCases']:
 q=copy.deepcopy(c['input']);root=q['root'];root=copy.deepcopy(f['roots'][root[1:]])if isinstance(root,str)and root.startswith('$')else root
 out=N.admit_root_document(root,reader_schemas=tuple(q.get('readerSchemas',[1])));old=P.admit_root_document(root,reader_schemas=tuple(q.get('readerSchemas',[1])));assert out==old,c['id']
 for path,want in c['expect'].items():
  value=out
  for part in path.split('.'):value=len(value)if part=='length'else value[int(part)]if isinstance(value,list)else value[part]
  assert value==want,(c['id'],path)
 rows.append({'label':c['id'],'input':{'root':root,'readers':q.get('readerSchemas',[1])},'candidate':out,'parentUnchanged':True})
valid=invalid=0
for y,m,d,h,minute,second in itertools.product([0,1,1900,2000,2024,2026,9999],[0,1,2,4,12,13],[0,1,28,29,30,31,32],[0,23,24],[0,59,60],[0,59,60]):
 text=f'{y:04d}-{m:02d}-{d:02d}T{h:02d}:{minute:02d}:{second:02d}Z'
 try:want=int(datetime.datetime(y,m,d,h,minute,second,tzinfo=datetime.timezone.utc).timestamp())
 except ValueError:
  try:N.ts(text)
  except N.Reject as e:assert str(e).startswith('TIMESTAMP_GRAMMAR:');invalid+=1
  else:raise AssertionError('invalid calendar accepted:'+text)
 else:assert N.ts(text)==want and P.ts(text)==want;valid+=1
for r in json.loads((S/'original-probes.json').read_bytes())['rootDateCases']:
 root=copy.deepcopy(f['roots'][r['root']]);root[r['field']]=r['timestamp'];out=N.admit_root_document(root,reader_schemas=(1,2));assert(out['result'],out['refusal'],out['detail'])==('REFUSE','PAYLOAD-NOT-ADMISSIBLE','ROOT.TIMESTAMP_GRAMMAR');rows.append({'label':r['root']+'-'+r['field']+'-'+r['timestamp'],'candidate':out,'parentException':r['actual']})
(O/'root-results.json').write_text(json.dumps(rows,indent=2)+'\n');result={'clock53ResultsUnchanged':len(clock_rows),'selectedRootCasesUnchanged':len(f['rootCases']),'invalidRootDatesNowTyped':16,'timestampCases':valid+invalid,'validTimestampsUnchanged':valid,'invalidTimestampsTyped':invalid,'revocationPreservesV8RootAuthority':True,'otherEnvelopeRoutesUnchanged':True,'standing':'Root proposal validation only; actual independent review and formal selection required; no crypto/OS/publication qualification'};(O/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
