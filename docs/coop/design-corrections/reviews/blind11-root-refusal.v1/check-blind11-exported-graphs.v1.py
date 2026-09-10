"""Root admission/replay of exact blind11 exports; never import consumer helpers.
Claims are a root-reviewed explicit list of positive export path + RunId selections.
Parse raw retained frames, not caller-supplied truth or summaries. No remint/repair.
"""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--claims',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
assert not a.out.exists();claims=json.loads(a.claims.read_text());assert isinstance(claims,list) and claims
assert len({(x['path'],x['runId']) for x in claims})==len(claims)
source=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('blind11_actual_owner3',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
a.out.mkdir(parents=True);(a.out/'claims.json').write_bytes(a.claims.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for i,claim in enumerate(claims):
 rel=Path(claim['path']);assert not rel.is_absolute() and '..' not in rel.parts
 src=a.input/rel;assert src.resolve().is_relative_to(a.input.resolve()) and src.is_file()
 raw=src.read_bytes();copy=a.out/'exact-inputs'/rel;copy.parent.mkdir(parents=True,exist_ok=True)
 if copy.exists():assert copy.read_bytes()==raw
 else:copy.write_bytes(raw)
 row={'name':claim.get('name',rel.name),'path':str(rel),'exportSha256':sha(raw),'claimedRunId':claim['runId'],'ownerAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED'}
 try:
  store=json.loads(raw);assert isinstance(store['objectTable'],dict) and isinstance(store['blobs'],dict)
  blobs={k:base64.b64decode(v,validate=True) for k,v in store['blobs'].items()};assert all(sha(v)==k for k,v in blobs.items()),'Exported blob digest mismatch'
  assert store.get('blobCount',len(blobs))==len(blobs) and store.get('objectCount',len(store['objectTable']))==len(store['objectTable'])
  objects={};run=None
  for key,obj in store['objectTable'].items():
   assert obj['id']==key
   frame=blobs[obj['digest']];prefix=b'opensip.product.v1\0';assert frame.startswith(prefix),'Wrong H frame prefix'
   domain_raw,body=frame[len(prefix):].split(b'\0',1);domain=domain_raw.decode('ascii');assert len(body)>=8 and int.from_bytes(body[:8],'big')==len(body[8:]),'H frame length mismatch'
   canonical=body[8:];descriptor=M.C.parse(canonical);assert M.C.canonical(descriptor)==canonical,'Noncanonical retained H descriptor'
   assert obj['domain']==domain and M.C.canonical(obj['descriptor'])==canonical,'Object table disagrees with retained frame'
   expected=M.identifier(domain,descriptor) if domain in M.PREFIX else 'sha256:'+obj['digest'];assert key==expected,'Typed identity disagrees with retained preimage'
   if domain in M.PREFIX:
    objects[key]=(domain,descriptor)
    if key==claim['runId']:assert domain=='run';run=descriptor
  assert run is not None,'Claimed positive Run missing from retained object table'
  row['ownerAdmission']='REFUSE';rid,_=M.open_run_closure(run,objects,blobs);assert rid==claim['runId'];row['ownerAdmission']='ADMIT'
  row['semanticAdmission']='REFUSE';rid=M.close_run(run,objects,blobs);assert rid==claim['runId'];row['semanticAdmission']='ADMIT';row['passed']=True
 except Exception as exc:
  row.update(passed=False,exceptionType=type(exc).__name__,reason=str(exc))
 rows.append(row)
report={'standing':'Root validation of exact exported blind11 bytes through selected owner and complete semantic replay. Consumer builders/evaluator not imported. No remint, repair or expected-output substitution.','sourceSha256':sha(source.read_bytes()),'claimsSha256':sha(a.claims.read_bytes()),'checks':rows,'count':len(rows),'passed':all(x['passed'] for x in rows)}
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
