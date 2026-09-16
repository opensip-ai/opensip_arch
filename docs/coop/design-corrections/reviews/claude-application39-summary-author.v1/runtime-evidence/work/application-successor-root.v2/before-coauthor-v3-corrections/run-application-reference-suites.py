"""Execute all retained and current-profile reference groups. Never grade design."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,subprocess,json,hashlib,sys
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--application-manifest-sha256');a=p.parse_args()
root=a.root.resolve();out=a.out.resolve();out.mkdir(exist_ok=False,parents=True)
dc='docs/coop/design-corrections/'
jobs=[('foundation','foundation/run-reference-checks.py',['--report',str(out/'foundation.json'),'--report-dir',str(out/'foundation')],3600),
 ('security','security/check-security-lifecycle.v1.py',['--report',str(out/'security.json')],900),
 ('native','native/check_native_evidence.v2.py',[],900),
 ('workflows','workflows/run-reference-checks.py',['--report',str(out/'workflows.json')],900),
 ('integration','check-integration.py',['--report',str(out/'integration.json')],900),
 ('evaluator3','foundation/run-evaluator3-checks.py',['--out',str(out/'evaluator3')],8400)]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(job):
 name,rel,args,budget=job;source=root/(dc+rel);before=sha(source);command=[sys.executable,'-I','-B',str(source)]+args
 try:
  r=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=budget);code,stdout,stderr,timed=r.returncode,r.stdout,r.stderr,False
 except subprocess.TimeoutExpired as exc:
  dec=lambda x:x.decode('utf-8','replace') if isinstance(x,bytes) else x or ''
  code,stdout,stderr,timed=None,dec(exc.stdout),dec(exc.stderr),True
 (out/(name+'.stdout')).write_text(stdout);(out/(name+'.stderr')).write_text(stderr)
 return {'name':name,'source':dc+rel,'sourceSha256':before,'sourceUnchanged':sha(source)==before,'command':command,'exitCode':code,'timedOut':timed,'outerTimeoutSeconds':budget,'stdoutSha256':sha(out/(name+'.stdout')),'stderrSha256':sha(out/(name+'.stderr')),'executedAs':'top-level suite child'}
rows=[]
with ThreadPoolExecutor(max_workers=6) as pool:
 for future in as_completed([pool.submit(run,job) for job in jobs]):
  row=future.result();rows.append(row);print(json.dumps({'name':row['name'],'exitCode':row['exitCode'],'timedOut':row['timedOut']}),flush=True)
workflow=out/'workflows.json'
if workflow.is_file():
 w=json.loads(workflow.read_text());source=dc+'workflows/check_workflows.v1.py'
 rows.append({'name':'workflow-surface','source':source,'sourceSha256':sha(root/source),'sourceUnchanged':True,'command':[sys.executable,'-I','-B',str(root/source),'--report',str(root/(dc+'workflows/workflows-report.v1.json'))],'exitCode':w.get('check',{}).get('exitCode'),'timedOut':False,'executedAs':'nested child of workflows/run-reference-checks.py','parentCommandEvidence':'workflows.json'})
report={'standing':'Executed source-pinned reference evidence, including all current-profile checks; no implementation qualification. Workflow-surface is the observed nested child, not an extra run.','commands':sorted(rows,key=lambda r:r['name']),'passed':len(rows)==7 and all(r['exitCode']==0 and not r['timedOut'] and r['sourceUnchanged'] for r in rows),'implementationAuthorized':False}
if a.application_manifest_sha256:report['applicationManifestSha256']=a.application_manifest_sha256
(out/'reference-checks.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not report['passed'])
