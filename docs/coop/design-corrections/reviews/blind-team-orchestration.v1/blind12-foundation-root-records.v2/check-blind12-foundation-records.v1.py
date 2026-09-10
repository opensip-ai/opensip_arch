from pathlib import Path
import importlib.util,json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v24';F=S/'docs/coop/design-corrections/foundation/identity-model.v3.py'
s=importlib.util.spec_from_file_location('root_foundation_record_owner',F);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
I=B/'consumer-b.v12-team-foundation-corrections.v2/output/foundation';O=B/'blind12-foundation-root-records.v1';O.mkdir();rows=[]
def read(name):
 p=I/name;shutil.copy2(p,O/name);return json.loads(p.read_text())
def check(label,entry):
 d=entry['domain'];r=entry['record'];raw=M.C.canonical(r);frame=M.h_preimage_frame(d,r);tid=M.identifier(d,r)
 ok=tid==entry['typedId'] and raw.hex()==entry['C_hex'] and frame.hex()==entry['frameHex'] and hashlib.sha256(frame).hexdigest()==entry['H']==entry['frameSha256'] and len(frame)==entry['frameByteLength'] and hashlib.sha256(raw).hexdigest()==entry['C_sha256']
 rows.append({'name':label,'recordSchemaAndOrder':'ADMIT','typedId':tid,'exactCAndHFrameMatch':ok,'passed':ok})
a=read('acyclic-joins.json');chain=a['positive']['chain'];by={x['domain']:x for x in chain}
for e in chain:check('acyclic:'+e['domain'],e)
ids={e['typedId']:e['domain'] for e in chain};edges=[]
def walk(value):
 if isinstance(value,str) and value in ids:yield value
 elif isinstance(value,dict):
  for v in value.values():yield from walk(v)
 elif isinstance(value,list):
  for v in value:yield from walk(v)
for e in chain:
 for target in walk(e['record']):edges.append([e['typedId'],target])
adj={i:[]for i in ids}
for s,t in edges:adj[s].append(t)
active=set();done=set()
def visit(n):
 if n in active:raise RuntimeError('cycle among retained chain records')
 if n in done:return
 active.add(n)
 for t in adj[n]:visit(t)
 active.remove(n);done.add(n)
for n in ids:visit(n)
rows.append({'name':'retained-chain-directed-acyclic','passed':True,'edges':edges,'limitation':'Only these seven standalone records and their retained cross references; not complete Run closure.','viewNamedByProof':by['view']['typedId'] in list(walk(by['proof-bundle']['record']))})
try:M.identifier('proof-bundle',a['cycle']['input']);refused=False;reason=None
except M.C.AdmissionError as e:refused=True;reason=str(e)
rows.append({'name':'illegal-proof-evidence-cycle-input','passed':refused,'reason':reason})
h=read('h-helper.json')
for i,e in enumerate(h['vectors']):
 if 'record'in e:check('snapshot-pair:'+str(i),e)
v=read('imported-observation-boundary.json')['retainedImport'];check('import-wrapper',v);row=M.PAYLOADS['classes']['import']['rows'][v['record']['kind']+'|'+v['payload']['payloadDomain']];M.validate_registered_record(row['document'],row['selector'],v['payload']);doc=S/'docs/coop/design-corrections'/row['document'];raw=M.C.canonical(v['payload']);ok=raw.hex()==v['payloadC_hex'] and hashlib.sha256(raw).hexdigest()==v['record']['payloadDigest']==v['payloadDigest'] and hashlib.sha256(doc.read_bytes()).hexdigest()==v['record']['payloadSchemaDigest'];rows.append({'name':'registered-runtime-payload-and-byte-joins','passed':ok,'selector':row})
r={'standing':'Actual frozen owner checks on exact new standalone record preimages. No consumer helper imported. This is bounded schema/C/H/retained-chain and runtime-payload validation, not full Run or whole foundation acceptance.','ownerSha256':hashlib.sha256(F.read_bytes()).hexdigest(),'checks':rows,'passed':all(x['passed']for x in rows),'limitations':['No complete closure admission of the seven standalone records; external referenced graph is not retained by this vector.','The proof does not name the view in this standalone chain. Whether the original positive-join obligation is fully exhibited needs original-charter scope assessment; this report does not grant that grade.','Imported correspondence/build/observation nested preimages, named gates, protocol and other foundation vectors not checked by this script.']}
shutil.copy2(Path(__file__),O/Path(__file__).name);(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(rows),'passed':r['passed'],'viewNamedByProof':rows[7]['viewNamedByProof']}));assert r['passed']
