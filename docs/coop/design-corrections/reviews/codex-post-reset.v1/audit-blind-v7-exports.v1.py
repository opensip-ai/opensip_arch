"""Root audit of exact exported blind graphs; no feedback or edits to blind evidence.
Author reference is used only by root after the independent reconstruction.
Input files are copied and bound before audit. This is not Claude assent.
"""
from pathlib import Path
import argparse, base64, hashlib, importlib.util, json, datetime

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--audit',required=True);a=p.parse_args()
src=Path(a.output);out=Path(a.audit);out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
repo=Path('/Users/sb/code/opensip-ai/opensip_arch')
mp=repo/'docs/coop/design-corrections/reviews/candidate-subject.v18.json'
assert sha(mp.read_bytes())=='cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44'
manifest=json.loads(mp.read_text());frozen=Path(manifest['snapshotRoot'])
model=frozen/'docs/coop/design-corrections/foundation/identity-model.py'
assert sha(model.read_bytes())==next(r['sha256'] for r in manifest['files'] if r['path']=='docs/coop/design-corrections/foundation/identity-model.py')
spec=importlib.util.spec_from_file_location('root_v18_model',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
custody=[]
for source in sorted(src.rglob('*')):
 if not source.is_file() or '__pycache__' in source.parts:continue
 if source.suffix not in ('.json','.py','.md'):continue
 raw=source.read_bytes();dest=out/'inputs'/source.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 assert source.read_bytes()==raw
 custody.append({'path':str(source.relative_to(src)),'sha256':sha(raw),'bytes':len(raw)})
results=[]
for op in sorted((out/'inputs/vectors').glob('*.objects.json')):
 label=op.name.removesuffix('.objects.json');objects_doc=json.loads(op.read_text());blobs_doc=json.loads(op.with_name(label+'.blobs.json').read_text())
 blobs={k:base64.b64decode(v,validate=True) for k,v in blobs_doc['blobs'].items()};objects={};bad=[];rows_bad=[]
 for digest,raw in blobs.items():
  if sha(raw)!=digest:bad.append(digest)
  if raw.startswith(M.FRAME_PREFIX):
   domain,payload=raw[len(M.FRAME_PREFIX):].split(b'\0',1);domain=domain.decode();assert len(payload)>=8 and int.from_bytes(payload[:8],'big')==len(payload[8:]);desc=json.loads(payload[8:])
   if domain in M.PREFIX:objects[M.PREFIX[domain]+':'+digest]=(domain,desc)
 for key,row in objects_doc['objects'].items():
  digest=M.C.identity(row['domain'],row['descriptor'])
  expected=M.PREFIX.get(row['domain'],'sha256')+':'+digest
  if key!=expected or row['hDigest']!=digest:rows_bad.append(key)
  if key in objects and objects[key]!=(row['domain'],row['descriptor']):rows_bad.append(key+':frame-descriptor-mismatch')
 run_id=objects_doc['runId'];assert run_id==blobs_doc['runId']
 result={'id':label,'runId':run_id,'exportedObjects':len(objects_doc['objects']),'typedObjects':len(objects),'blobs':len(blobs),'badBlobDigests':bad,'badObjectIdentities':rows_bad}
 try:
  assert not bad and not rows_bad
  admitted=M.close_run(objects[run_id][1],objects,blobs)
  result.update(referenceResult='ADMITTED',detail=str(admitted))
 except Exception as exc:result.update(referenceResult='REFUSED',exception=type(exc).__name__,detail=str(exc))
 results.append(result)
report={'standing':__doc__,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(src),'parentSubjectSha256':sha(mp.read_bytes()),'referenceModelSha256':sha(model.read_bytes()),'inputFiles':custody,'results':results,'allAdmit':bool(results) and all(r['referenceResult']=='ADMITTED' for r in results),'claudeAssent':False,'productQualification':False}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'results':results,'allAdmit':report['allAdmit']},indent=2))
