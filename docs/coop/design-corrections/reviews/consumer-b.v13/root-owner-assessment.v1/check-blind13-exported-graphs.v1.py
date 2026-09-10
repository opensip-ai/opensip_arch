"""Root parses blind13 exported descriptors and exact retained blobs with frozen owner.
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
 # Consumer13 exports descriptors in objectTable and separate encoding metadata.
 # Read its bytes only; never import consumer helpers or add missing H frames.
 exported=json.loads(raw,object_pairs_hook=unique_object)
 assert type(exported['objectTable']) is dict and type(exported['blobs']) is dict
 assert type(exported['frames']) is dict
 blobs={}
 for digest,value in exported['blobs'].items():
  assert re.fullmatch('[0-9a-f]{64}',digest),'Malformed blob digest'
  payload=base64.b64decode(value,validate=True)
  assert sha(payload)==digest,'Exported blob digest mismatch'
  blobs[digest]=payload
 objects={};seen=set()
 for digest,meta in exported['frames'].items():
  assert re.fullmatch('[0-9a-f]{64}',digest),'Malformed frame metadata digest'
  domain=meta['domain'];ident=meta['identity']
  assert ident in exported['objectTable'],'Frame metadata names absent descriptor'
  assert ident not in seen,'Duplicate metadata identity';seen.add(ident)
  descriptor=exported['objectTable'][ident]
  cx=bytes.fromhex(meta['canonicalBytesHex'])
  assert M.C.canonical(descriptor)==cx,'Descriptor disagrees with canonical bytes'
  assert sha(cx)==meta['canonicalSha256'],'Canonical metadata digest mismatch'
  assert blobs.get(sha(cx))==cx,'Canonical descriptor bytes not retained'
  if domain=='canonical-record':
   assert digest==sha(cx) and ident==digest,'Canonical record identity mismatch'
  else:
   # Computing the expected digest verifies metadata. It does NOT retain a frame.
   assert M.C.identity(domain,descriptor)==digest,'H identity metadata mismatch'
   if domain in M.PREFIX:
    assert ident==M.PREFIX[domain]+':'+digest,'Typed identity mismatch'
    objects[ident]=(domain,descriptor)
   else:
    assert ident=='sha256:'+digest,'Untyped H identity mismatch'
 assert seen==set(exported['objectTable']),'Descriptor lacks encoding metadata'
 return objects,blobs

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--claims',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists();claims=json.loads(a.claims.read_text());assert isinstance(claims,list) and claims
 assert len({(x['path'],x['runId']) for x in claims})==len(claims)
 source=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('blind13_actual_owner3',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
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
