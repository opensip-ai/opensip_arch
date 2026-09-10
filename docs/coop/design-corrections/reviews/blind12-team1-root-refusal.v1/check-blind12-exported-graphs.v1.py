"""Root parses blind12 transport metadata and tests exact retained frames with frozen owner.
Never imports consumer builders/checkers; no repair/remint or expected-output substitution.
"""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json,re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def unique_object(pairs):
 result={}
 for key,value in pairs:
  assert key not in result,'Duplicate export key: '+key
  result[key]=value
 return result

def decode_store(raw,M):
 store=json.loads(raw,object_pairs_hook=unique_object)
 assert isinstance(store['objectTable'],dict) and isinstance(store['blobs'],dict)
 blobs={}
 for digest,value in store['blobs'].items():
  assert re.fullmatch('[0-9a-f]{64}',digest),'Malformed blob digest'
  payload=base64.b64decode(value,validate=True);assert sha(payload)==digest,'Exported blob digest mismatch';blobs[digest]=payload
 assert store.get('blobCount',len(blobs))==len(blobs),'Blob count mismatch'
 objects={}
 for key,meta in store['objectTable'].items():
  assert isinstance(meta,dict)
  kind=meta['kind'];assert kind in ['h-identity','raw-artifact','canonical-record'],'Unknown export metadata kind'
  digest=meta['digest'] if kind=='h-identity' else key
  assert digest in blobs,'Metadata names absent blob'
  frame=blobs[digest];assert type(meta['bytes']) is int and meta['bytes']==len(frame),'Metadata byte count mismatch'
  if kind!='h-identity':
   assert key==digest
   if kind=='canonical-record':assert M.C.canonical(M.C.parse(frame))==frame,'Noncanonical exported record'
   continue
  prefix=b'opensip.product.v1\0';assert frame.startswith(prefix),'Wrong H frame prefix'
  domain_bytes,body=frame[len(prefix):].split(b'\0',1);domain=domain_bytes.decode('ascii')
  assert len(body)>=8 and int.from_bytes(body[:8],'big')==len(body[8:]),'H frame length mismatch'
  descriptor=M.C.parse(body[8:]);assert M.C.canonical(descriptor)==body[8:],'Noncanonical retained descriptor'
  assert meta['domain']==domain,'Metadata domain disagrees with retained frame'
  assert meta['sha256Text']=='sha256:'+digest,'Metadata sha256Text mismatch'
  typed=M.identifier(domain,descriptor) if domain in M.PREFIX else None
  assert meta['typedId']==typed,'Metadata typed identity disagrees with retained frame'
  assert key==digest or (typed is not None and key==typed),'Metadata alias mismatch'
  assert digest in store['objectTable'] and store['objectTable'][digest]==meta,'Metadata aliases disagree'
  if typed is not None:
   if typed in objects:assert objects[typed]==(domain,descriptor),'Conflicting typed object'
   objects[typed]=(domain,descriptor)
 return objects,blobs

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--claims',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists();claims=json.loads(a.claims.read_text());assert isinstance(claims,list) and claims
 assert len({(x['path'],x['runId']) for x in claims})==len(claims)
 source=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('blind12_actual_owner3',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
 a.out.mkdir(parents=True);(a.out/'claims.json').write_bytes(a.claims.read_bytes());rows=[]
 for claim in claims:
  rel=Path(claim['path']);assert not rel.is_absolute() and '..' not in rel.parts
  src=a.input/rel;assert src.resolve().is_relative_to(a.input.resolve()) and src.is_file()
  raw=src.read_bytes();dst=a.out/'exact-inputs'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if dst.exists():assert dst.read_bytes()==raw
  else:dst.write_bytes(raw)
  row={'name':claim.get('name',rel.name),'path':str(rel),'exportSha256':sha(raw),'claimedRunId':claim['runId'],'ownerAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED'}
  try:
   objects,blobs=decode_store(raw,M);domain,run=objects[claim['runId']];assert domain=='run'
   row['ownerAdmission']='REFUSE';rid,_=M.open_run_closure(run,objects,blobs);assert rid==claim['runId'];row['ownerAdmission']='ADMIT'
   row['semanticAdmission']='REFUSE';rid=M.close_run(run,objects,blobs);assert rid==claim['runId'];row['semanticAdmission']='ADMIT';row['passed']=True
  except Exception as exc:row.update(passed=False,exceptionType=type(exc).__name__,reason=str(exc))
  rows.append(row)
 report={'standing':'Exact exported bytes through frozen structural owner and complete semantic replay; consumer helpers not imported.','sourceSha256':sha(source.read_bytes()),'parserSha256':sha(Path(__file__).read_bytes()),'claimsSha256':sha(a.claims.read_bytes()),'checks':rows,'count':len(rows),'passed':all(r['passed'] for r in rows)}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
if __name__=='__main__':main()
