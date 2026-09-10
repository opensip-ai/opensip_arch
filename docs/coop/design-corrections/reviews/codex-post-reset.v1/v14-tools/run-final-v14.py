"""Reproduce final proposed v14 reference checks before independent review."""
from pathlib import Path
import argparse,hashlib,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=a.root.resolve();out=a.out.resolve();out.mkdir(exist_ok=False)
dc='docs/coop/design-corrections/';py='/tmp/opensip-architecture-review-env/bin/python';activation={'applicationManifest':{'sha256':None}}
jobs=[('foundation','foundation/run-reference-checks.py',['--report',dc+'foundation/validation-report.json']),('security','security/check-security-lifecycle.v1.py',['--report',dc+'security/security-lifecycle-report.v1.json']),('native','native/check_native_evidence.v2.py',[]),('workflows','workflows/run-reference-checks.py',['--report',dc+'workflows/workflows-validation-report.json']),('workflow-surface','workflows/check_workflows.v1.py',['--report',dc+'workflows/workflows-report.v1.json']),('integration','check-integration.py',['--report',dc+'integration-report.v1.json'])]
rows=[]
for name,rel,args in jobs:
 source=root/(dc+rel);command=[py,'-I','-B',dc+rel]+args
 r=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=180);(out/(name+'.log')).write_text(r.stdout+r.stderr)
 rows.append({'name':name,'source':dc+rel,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'command':command,'workingDirectory':'. (selected candidate root)','exitCode':r.returncode,'log':name+'.log'})
 print(name,r.returncode,r.stdout[-220:],flush=True)
report={'standing':'Final candidate v14 reference checks before independent review, not product qualification. Report generated from executed commands, never assumed from prospective checks.','applicationManifestSha256':activation['applicationManifest']['sha256'],'commands':rows,'passed':all(v['exitCode']==0 for v in rows),'implementationAuthorized':False}
(out/'reference-checks.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not report['passed'])
