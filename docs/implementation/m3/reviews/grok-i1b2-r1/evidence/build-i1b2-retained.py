import json,hashlib,copy,sys
variant=sys.argv[1] if len(sys.argv)>1 else "self-cycle"
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip-i1b2')
f=json.loads((root/'crates/host/tests/fixtures/composition-fixtures.json').read_text())
q=next(q for q in f['cases'] if q['label']=='references-original')
canon=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def h(domain,value):
 raw=canon(value);return hashlib.sha256(b'opensip.product.v1\0'+domain.encode()+b'\0'+len(raw).to_bytes(8,'big')+raw).hexdigest()
def cve(raw):
 pos=0
 def read(n):
  nonlocal pos
  v=raw[pos:pos+n];pos+=n;return v
 def val():
  tag=read(1)[0]
  if tag in (0,1,2):return (None,False,True)[tag]
  if tag in (3,7):return int.from_bytes(read(8),'big',signed=(tag==7))
  if tag==4:return read(int.from_bytes(read(4),'big')).decode()
  n=int.from_bytes(read(4),'big')
  if tag==5:return [val() for _ in range(n)]
  if tag==6:return {val():val() for _ in range(n)}
  raise ValueError(tag)
 out=val();assert pos==len(raw);return out


objects={f['objectPool'][k]['id']:copy.deepcopy(f['objectPool'][k]) for k in q['objects']}
blobs={f['blobPool'][k]['digest']:bytes.fromhex(f['blobPool'][k]['hex']) for k in q['blobs']}
parsed={}
for digest,raw in blobs.items():
 try:v=json.loads(raw)
 except (ValueError,UnicodeDecodeError):continue
 if raw!=canon(v):continue
 if isinstance(v,dict) and ('$schema' in v or '$id' in v):continue
 parsed[digest]=v
old_program=next(d for d,v in parsed.items() if isinstance(v,dict) and v.get('op')=='exists')
node={'op':'cycle-representative','relation':'imports','minResolution':'resolved-target','filters':[]}
def change(v):
 if isinstance(v,list):return [change(x) for x in v]
 if isinstance(v,dict):
  if 'referrer' in v and 'resolvedBinding' in v:return {'importer':v['referrer'],'specifier':'./a','resolvedTarget':v['resolvedBinding']}
  if 'op' in v and v['op']=='exists':return node
  out={k:change(x) for k,x in v.items()}
  if 'cellOrdinal' in out:out['cellOrdinal']=1-out['cellOrdinal']
  if 'cellOutcomes' in out:
   out['cellOutcomes'].sort(key=lambda r:(r['cellOrdinal'],r['programOrdinal']))
   for i,r in enumerate(out['cellOutcomes']):r['ordinal']=i
  if 'cells' in out:out['cells'].sort(key=lambda r:(r['capabilityId'],r['languageMode'],r['workspaceRoot']))
  if 'subjectEnumeration' in out:out['subjectEnumeration']['subjectKind']='file'
  if out.get('relation')=='imports' and 'resolutionCompleteness' in out:
   out['resolutionCompleteness'].update(attempted=True,state='complete')
  return out
 return {'references':'imports','resolved-binding':'resolved-target'}.get(v,v) if isinstance(v,str) else v
parsed={d:change(v) for d,v in parsed.items()}
objects={oid:{**r,'descriptor':change(r['descriptor'])} for oid,r in objects.items()}
if variant != 'self-cycle':
 import_facts={oid for oid,r in objects.items() if r['domain']=='fact' and r['descriptor'].get('relation')=='imports'}
 for r in objects.values():
  if r['domain']=='view':r['descriptor']['facts']=[fid for fid in r['descriptor']['facts'] if fid not in import_facts]
if variant in ('file-partial','symbol-partial-optional'):
 kind='file' if variant=='file-partial' else 'symbol'
 for v in parsed.values():
  if isinstance(v,dict) and v.get('kind')==kind and 'examinedPaths' in v:v.update(state='partial',deficiency='budget-exhausted',nativeCause=None)
  if isinstance(v,dict) and 'cellOutcomes' in v:
   for r in v['cellOutcomes']:
    if kind in r['kinds']:r.update(state='partial',deficiency='budget-exhausted',nativeCause=None)
 if variant=='symbol-partial-optional':
  for v in parsed.values():
   if not isinstance(v,dict):continue
   for key in ('cells','requestedCapabilities','cellOutcomes'):
    for r in v.get(key,[]):
     if r.get('capabilityId')=='imports':r['required']=False
# Resolve immutable blob/object DAG. Old fixture bytes stay unchanged; every dependent new pin is recomputed.
remap={}
set_fields={'parameters','requestedCapabilities','hostDerivedRefs','outputRefs','outputDomains','selectedRefs','candidateResultRefs','evaluationInputRefs','inputRefs','semanticClosures','coverageIds','scopeIds','facts','importIds','schemaDigests','inventoryDigests','viewDigests','subjects','nativeCoverageAccounts','anchors'}
def replace(v,key=None):
 if isinstance(v,str):
  if v in remap:return remap[v]
  for prefix in ('sha256:',):
   if v.startswith(prefix) and v[len(prefix):] in remap:return prefix+remap[v[len(prefix):]]
  return v
 if isinstance(v,list):
  out=[replace(x) for x in v]
  return sorted(out,key=canon) if key in set_fields else out
 if isinstance(v,dict):return {replace(k):replace(x,k) for k,x in v.items()}
 return v
for iteration in range(40):
 changes=0
 for old,v in parsed.items():
  new=hashlib.sha256(canon(replace(v))).hexdigest()
  if remap.get(old,old)!=new:changes+=1
  remap[old]=new
 for old,r in objects.items():
  digest=h(r['domain'],replace(r['descriptor']));prefix=old.split(':')[0]+':'
  new=prefix+digest
  if remap.get(old,old)!=new:changes+=1
  remap[old]=new;remap[old.split(':')[1]]=digest
 if not changes:break
else:raise RuntimeError('cyclic fixture dependencies')
new_objects=[{'id':replace(old),'domain':r['domain'],'descriptor':replace(r['descriptor'])} for old,r in objects.items()]
new_blobs=[{'digest':replace(old),'hex':(canon(replace(parsed[old])) if old in parsed else raw).hex()} for old,raw in blobs.items()]
query=replace({k:v for k,v in q.items() if k in ('planId','executionId','evaluatorClosure','inputRefs')})
case={'label':'retained-typescript-'+variant,'expectedVerdict':'fail' if variant=='self-cycle' else 'indeterminate' if 'partial' in variant else 'pass','query':query,'objects':new_objects,'blobs':new_blobs}
path=root/'crates/evaluator/tests/fixtures/cycle-representative.v1.json'
v=json.loads(path.read_text());v['retainedCases']=[c for c in v.get('retainedCases',[]) if c['label']!=case['label']]+[case];path.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
print('retained case',iteration,len(new_objects),len(new_blobs),query['planId'])
