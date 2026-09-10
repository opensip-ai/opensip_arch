"""Root owner/replay validation of exact independently exported consumer graphs.
No consumer builders or evaluator imported. No repair or re-mint of input bytes.
"""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True)
source=a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py';spec=importlib.util.spec_from_file_location('blind10_actual_owner3',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for storepath in sorted(a.input.glob('*.store.json')):
 summarypath=storepath.with_name(storepath.name.replace('.store.json','.summary.json'));raw=storepath.read_bytes();summaryraw=summarypath.read_bytes();(a.out/storepath.name).write_bytes(raw);(a.out/summarypath.name).write_bytes(summaryraw)
 store=json.loads(raw);summary=json.loads(summaryraw);blobs={k:base64.b64decode(v,validate=True) for k,v in store['blobs'].items()};objects={};run=None
 row={'name':summary['name'],'storeSha256':sha(raw),'summarySha256':sha(summaryraw),'claimedRunId':summary['runId'],'claimedSchemaErrors':summary.get('schemaErrors'),'claimedReplayMatch':summary.get('replayMatch')}
 try:
  assert all(sha(v)==k for k,v in blobs.items()),'Exported blob digest mismatch'
  for obj in store['objectTable']:
   if obj['retention']!='h-preimage-frame':continue
   frame=blobs[obj['digest']];prefix=b'opensip.product.v1\0';assert frame.startswith(prefix)
   domain_raw,body=frame[len(prefix):].split(b'\0',1);domain=domain_raw.decode('ascii');assert int.from_bytes(body[:8],'big')==len(body[8:]);descriptor=json.loads(body[8:]);assert obj['domain']==domain
   if domain in M.PREFIX:
    assert obj['id']==M.identifier(domain,descriptor),'Exported typed id mismatch: '+obj['id'];objects[obj['id']]=(domain,descriptor)
    if obj['id']==summary['runId']:run=descriptor
  assert run is not None,'No claimed Run descriptor in export'
  rid,_=M.open_run_closure(run,objects,blobs);row['ownerAdmission']='ADMIT';assert rid==summary['runId']
  rid=M.close_run(run,objects,blobs);row['semanticAdmission']='ADMIT';assert rid==summary['runId'];row['passed']=True
 except Exception as exc:
  row['passed']=False;row['ownerAdmission']=row.get('ownerAdmission','REFUSE');row['semanticAdmission']='REFUSE' if row['ownerAdmission']=='ADMIT' else 'NOT-REACHED';row['exceptionType']=type(exc).__name__;row['reason']=str(exc)
 rows.append(row)
report={'standing':'Root validation of exact exported consumer bytes using actual selected owner and complete replay. No consumer code or author fixture builder imported; bytes not repaired. Reference evidence only.','sourceSha256':sha(source.read_bytes()),'checks':rows,'passed':bool(rows) and all(r['passed'] for r in rows),'count':len(rows)}
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'count':len(rows),'passed':report['passed'],'checks':rows},indent=2))
raise SystemExit(not report['passed'])
