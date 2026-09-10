from pathlib import Path
import json,hashlib,base64,importlib.util
P=Path(__file__).parent;S=Path('/tmp/opensip-design-corrections/candidate-subject.v21');kit=Path('/tmp/opensip-design-corrections/consumer-b.v9/subject');sha=lambda b:hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('audit_v21',S/'docs/coop/design-corrections/foundation/identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
man=json.loads((kit/'consumer-input-manifest.json').read_text());schema={}
for row in man['files']:
 p=kit/row['path']
 if p.suffix=='.json':
  b=p.read_bytes();assert sha(b)==row['sha256'];schema[sha(b)]=b
results=[]
for p in sorted(P.glob('RUN-*.json')):
 d=json.loads(p.read_text());blobs={h:base64.b64decode(v,validate=True) for h,v in d['blobs'].items()};added=sorted(set(schema)-set(blobs));blobs.update(schema);objects={r['id']:(r['domain'],r['descriptor']) for r in d['objects'] if r['domain'] in M.PREFIX};rid=d['run']['id'];r={'label':p.stem,'originalExportSha256':sha(p.read_bytes()),'addedNormativeJsonBlobs':added}
 try:r['admittedRunId']=M.close_run(objects[rid][1],objects,blobs);r['result']='CLOSURE_ADMITTED_WITH_ROOT_ADDED_CUSTODY'
 except Exception as e:r.update(result='REFUSED',exception=type(e).__name__,detail=str(e))
 results.append(r)
o={'standing':'Diagnostic ONLY: root adds exact normative JSON bytes to each observed export to unmask deeper admission failures. Original exact exports ALL refused missing native schema. These are NOT blind-provided complete positives and NOT semantic replay or source defects. No bytes supplied to blind reviewer.','runs':results};(P/'diagnostic-result.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k!='addedNormativeJsonBlobs'} for r in results],indent=2))
