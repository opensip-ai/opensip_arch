"""Root transport reader for blind15's DECLARED export shape. No consumer imports.
Only exact supplied frames/blobs are offered to the frozen owner. No missing byte,
record, identity or semantic result is filled in, reminted or repaired.
"""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json,re
SUBJECT='bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON key: '+k)
  d[k]=v
 return d
def invalid_constant(s):raise ValueError('Non-JSON constant: '+s)
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid_constant)
def decode(raw,M):
 d=parse(raw);assert type(d['objectTable']) is dict and type(d['blobs']) is dict
 blobs={};objects={};notes=[]
 for k,v in d['blobs'].items():
  assert re.fullmatch('[0-9a-f]{64}',k) and type(v) is str,'Malformed blob transport'
  b=base64.b64decode(v,validate=True);assert sha(b)==k,'Blob key does not hash to retained bytes';blobs[k]=b
 for key,row in d['objectTable'].items():
  assert type(row) is dict and set(row)=={'domain','frameDigest','record'},'Unexpected transport record shape'
  domain=row['domain'];digest=row['frameDigest'];record=row['record']
  assert type(domain) is str and re.fullmatch('[0-9a-f]{64}',digest),'Malformed frame metadata'
  assert '\x00' not in domain
  c=M.C.canonical(record);expected=b'opensip.product.v1\x00'+domain.encode('ascii')+b'\x00'+len(c).to_bytes(8,'big')+c
  assert digest==sha(expected),'Frame metadata identity mismatch'
  assert blobs.get(digest)==expected,'Missing/different exact retained H frame'
  if domain in M.PREFIX:
   assert key==M.PREFIX[domain]+':'+digest,'Typed object key mismatch'
   objects[key]=(domain,record)
  else:
   # Non-product/nested metadata labels are transport-local. The owner admits their
   # actual retained frame only when a selected registered law requires it.
   notes.append({'transportLabel':key,'domain':domain,'frameDigest':digest,'standing':'Verified frame bytes; not injected into product typed object table'})
 return objects,blobs,notes

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists(),'Preserve prior evidence: use a fresh output path'
 for q in [a.source,a.input.parent]:assert not a.out.resolve().is_relative_to(q.resolve()),'Output must be outside inputs'
 mf=a.manifest.read_bytes();assert sha(mf)==SUBJECT;manifest=parse(mf)
 for row in manifest['files']:
  b=(a.source/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'],'Frozen source drift: '+row['path']
 model=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('root_blind15_owner',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
 raw=a.input.read_bytes();a.out.mkdir(parents=True);(a.out/'exact-export.json').write_bytes(raw)
 report={'standing':'Root exact transport and frozen owner verification. Not a consumer helper result, implementation qualification or complete charter assessment.','sourceManifestSha256':SUBJECT,'ownerSha256':sha(model.read_bytes()),'parserSha256':sha(Path(__file__).read_bytes()),'exportSha256':sha(raw),'runId':a.run_id,'sourceFilesVerified':len(manifest['files']),'transportAdmission':'NOT-REACHED','structuralAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED','passed':False}
 try:
  report['transportAdmission']='REFUSE';objects,blobs,notes=decode(raw,M);report['transportAdmission']='ADMIT';report['transportNotes']=notes
  domain,run=objects[a.run_id];assert domain=='run';report['structuralAdmission']='REFUSE';rid,_=M.open_run_closure(run,objects,blobs);assert rid==a.run_id;report['structuralAdmission']='ADMIT'
  report['semanticAdmission']='REFUSE';rid=M.close_run(run,objects,blobs);assert rid==a.run_id;report['semanticAdmission']='ADMIT';report['passed']=True
 except Exception as e:report['exceptionType']=type(e).__name__;report['reason']=str(e)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
if __name__=='__main__':main()
