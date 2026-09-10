"""Replay exported bytes without importing any fixture builder or expected proof."""
import argparse,base64,hashlib,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
source=a.source_root/'docs/coop/design-corrections/foundation/identity-model.v3.py'
spec=importlib.util.spec_from_file_location('exported_identity3',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
manifest=json.loads(a.manifest.read_text());rows=[]
for entry in manifest['files']:
    path=a.manifest.parent/entry['path'];raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==entry['sha256']
    g=json.loads(raw);run=g['run'];objects={k:(v['domain'],v['descriptor']) for k,v in g['objects'].items()};blobs={k:base64.b64decode(v,validate=True) for k,v in g['blobs'].items()}
    owner_id,_=M.open_run_closure(run,objects,blobs)
    try:
        actual=M.close_run(run,objects,blobs)
    except Exception as exc:
        assert entry['expectedAdmission']=='REFUSE' and str(exc)==entry['expectedRefusal'],(entry['path'],type(exc).__name__,str(exc))
        rows.append({'path':entry['path'],'ownerAdmission':'ADMIT','semanticAdmission':'REFUSE','reason':str(exc)})
    else:
        assert entry['expectedAdmission']=='ADMIT' and actual==entry['expectedRunId']==owner_id,entry['path']
        rows.append({'path':entry['path'],'ownerAdmission':'ADMIT','semanticAdmission':'ADMIT','runId':actual})
report={'standing':'Actual replay of exported synthetic graph bytes; no fixture construction and no product qualification','passed':True,'count':len(rows),'sourceRoot':str(a.source_root),'manifestSha256':hashlib.sha256(a.manifest.read_bytes()).hexdigest(),'checks':rows}
a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'count':len(rows)}))
