"""Root transport reader for blind24's observed list-of-retained-frame metadata. No consumer imports.
Only exact supplied frames/blobs are offered to the frozen owner. No missing byte,
record, identity or semantic result is filled in, reminted or repaired.
"""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json,re
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
 d=parse(raw);assert type(d['objectTable']) is list and type(d['blobs']) is dict
 blobs={};objects={};notes=[];seen=set()
 for k,v in d['blobs'].items():
  assert re.fullmatch('[0-9a-f]{64}',k) and type(v) is str,'Malformed blob transport'
  raw_blob=base64.b64decode(v,validate=True)
  assert sha(raw_blob)==k,'Blob key does not hash to retained bytes'
  blobs[k]=raw_blob
 for row in d['objectTable']:
  assert type(row) is dict and set(row)=={'domain','frameBytes','frameSha256','id'},'Unexpected transport record shape'
  domain=row['domain'];digest=row['frameSha256'];key=row['id'];length=row['frameBytes']
  assert type(domain) is str and '\x00' not in domain and type(key) is str,'Malformed object metadata'
  assert key not in seen,'Duplicate object id';seen.add(key)
  assert type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest),'Malformed frame digest'
  assert type(length) is int and length>0,'Malformed frame byte count'
  frame=blobs.get(digest);assert frame is not None and len(frame)==length,'Missing or differently sized retained frame'
  prefix=b'opensip.product.v1\x00'+domain.encode('ascii')+b'\x00'
  assert frame.startswith(prefix) and len(frame)>=len(prefix)+8,'Wrong retained frame header'
  size=int.from_bytes(frame[len(prefix):len(prefix)+8],'big');body=frame[len(prefix)+8:]
  assert len(body)==size,'Wrong retained frame extent'
  record=parse(body);assert M.C.canonical(record)==body,'Retained frame body not canonical'
  if domain in M.PREFIX:
   assert key==M.PREFIX[domain]+':'+digest,'Typed object key mismatch'
   objects[key]=(domain,record)
  else:
   notes.append({'transportLabel':key,'domain':domain,'frameDigest':digest,'standing':'Verified exact retained frame; not injected into product typed object table'})
 return objects,blobs,notes

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists(),'Preserve prior evidence: use a fresh output path'
 for q in [a.source,a.input.parent]:assert not a.out.resolve().is_relative_to(q.resolve()),'Output must be outside inputs'
 mf=a.manifest.read_bytes();assert sha(mf)==a.manifest_sha256;manifest=parse(mf)
 for row in manifest['files']:
  b=(a.source/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'],'Frozen source drift: '+row['path']
 model=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('root_blind24_owner',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
 raw=a.input.read_bytes();a.out.mkdir(parents=True);(a.out/'exact-export.json').write_bytes(raw)
 report={'standing':'Root exact transport and frozen owner verification. Not a consumer helper result, implementation qualification or complete charter assessment.','sourceManifestSha256':a.manifest_sha256,'ownerSha256':sha(model.read_bytes()),'parserSha256':sha(Path(__file__).read_bytes()),'exportSha256':sha(raw),'runId':a.run_id,'sourceFilesVerified':len(manifest['files']),'transportAdmission':'NOT-REACHED','structuralAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED','passed':False}
 try:
  report['transportAdmission']='REFUSE';objects,blobs,notes=decode(raw,M);report['transportAdmission']='ADMIT';report['transportNotes']=notes
  domain,run=objects[a.run_id];assert domain=='run';report['structuralAdmission']='REFUSE';rid,_=M.open_run_closure(run,objects,blobs);assert rid==a.run_id;report['structuralAdmission']='ADMIT'
  report['semanticAdmission']='REFUSE';rid=M.close_run(run,objects,blobs);assert rid==a.run_id;report['semanticAdmission']='ADMIT';report['passed']=True
 except Exception as e:report['exceptionType']=type(e).__name__;report['reason']=str(e)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
if __name__=='__main__':main()
