from pathlib import Path
import concurrent.futures,json,subprocess
b=Path('/tmp/opensip-design-corrections');o=Path(__file__).parent
rows=json.loads((o/'capture.json').read_text())['files']
def run(r):
 cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(b/'check-blind-successor31-export.v1.py'),'--input',r['input'],'--run-id',r['runId'],'--source',str(b/'candidate-subject.v31'),'--manifest','/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json','--out',str(o/r['name'])]
 p=subprocess.run(cmd,capture_output=True,text=True);(o/(r['name']+'.process.json')).write_text(json.dumps({'command':cmd,'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2)+'\n');report=json.loads((o/r['name']/'report.json').read_text());return {k:report.get(k) for k in ['runId','structuralAdmission','semanticAdmission','reason','passed']}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(run,rows):print(json.dumps(r),flush=True)
