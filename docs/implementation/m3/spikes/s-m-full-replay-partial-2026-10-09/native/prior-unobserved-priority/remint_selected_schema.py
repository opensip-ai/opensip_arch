from pathlib import Path
import json,hashlib,importlib.util,sys
B=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('sm_remint_builder',B/'prepare_packet.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P);M=P.P.load('sm_remint_identity',P.P.HERE/'identity-model.v3.py')
count=int(sys.argv[1])if len(sys.argv)>1 else 3;packet=json.loads((B/f'packet-{count}.json').read_text());diff=json.loads((B/'selected-schema-differences.json').read_text());assert len(diff)==1;mapping={diff[0]['old']:diff[0]['selected']};original_objects={r['id']:(r['domain'],r['descriptor'])for r in packet['objects']};original_blobs={r['sha256']:bytes.fromhex(r['hex'])for r in packet['blobs']}
def can(v):return M.C.canonical(v)
def substitute(v):
 if isinstance(v,str):
  for old,new in sorted(mapping.items(),key=lambda p:-len(p[0])):v=v.replace(old,new)
  return v
 if isinstance(v,list):
  ordered=all(can(a)<=can(b)for a,b in zip(v,v[1:]));out=[substitute(x)for x in v]
  return sorted(out,key=can)if ordered else out
 if isinstance(v,dict):return {substitute(k):substitute(value)for k,value in v.items()}
 return v
for round_ in range(100):
 changes={};objects={};blobs={}
 for key,(domain,descriptor)in original_objects.items():
  value=substitute(descriptor);new=M.identifier(domain,value);objects[new]=(domain,value)
  if new!=key:
   changes[key]=new;changes[key.rsplit(':',1)[1]]=new.rsplit(':',1)[1]
 for key,raw in original_blobs.items():
  try:value=M.C.parse(raw)
  except Exception:value=None
  if value is not None and can(value)==raw:raw=can(substitute(value))
  else:
   for old,new in sorted(mapping.items(),key=lambda p:-len(p[0])):raw=raw.replace(old.encode(),new.encode())
  new=hashlib.sha256(raw).hexdigest();blobs[new]=raw
  if new!=key and key!=diff[0]['old']:changes[key]=new
 selected=Path(diff[0]['source']).read_bytes();assert hashlib.sha256(selected).hexdigest()==diff[0]['selected'];blobs[diff[0]['selected']]=selected
 merged=dict(mapping,**changes)
 if merged==mapping:break
 mapping=merged
else:raise AssertionError('remint failed to settle')
packet.update(standing='SYNTHETIC CLAIM GRAPH REMINTED TO EXACT CURRENT SELECTED NATIVEV2SCHEMA; NATIVE FULLREPLAY MUST INDEPENDENTLY ACCEPT',runId=substitute(packet['runId']),objects=[dict(id=k,domain=v[0],descriptor=v[1])for k,v in sorted(objects.items())],blobs=[dict(sha256=k,hex=v.hex())for k,v in sorted(blobs.items())]);(B/f'packet-{count}-selected.json').write_text(json.dumps(packet,separators=(',',':'))+'\n');(B/f'remint-{count}-report.json').write_text(json.dumps(dict(schemaSourceDifference=diff,settledRound=round_,rewrittenReferences=len(mapping),nativeReplayAccepted=False,productCodeUnedited=True),indent=2)+'\n')
