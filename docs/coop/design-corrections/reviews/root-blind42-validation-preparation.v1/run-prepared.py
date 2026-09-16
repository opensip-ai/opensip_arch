from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,hashlib,subprocess,shutil
B=Path('/tmp/opensip-design-corrections');O=Path(__file__).parent;L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');C=B/'consumer-b.v24-source42.v1';I=C/'output';P=B/'root-blind39-transport-preparation.v1/check-export.py';S=B/'candidate-subject.v42';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((C/'process-completion.json').read_bytes())['exitCode']==0
assert H(P)=='6fa376bb59548bd9d52dbc52a3a35f27e0d12e4a963a6730624467c3a8f63074'
review=I/'blind-review.json';r=json.loads(review.read_bytes());rows=r['claimedCompletePositives'];assert r['verdict']=='ACCEPT-RECONSTRUCTABLE' and len(rows)==27 and len({x['run'] for x in rows})==len(rows)
for x in rows:
 assert x['runId']==json.loads((I/x['store']).read_bytes())['runId']
 assert (I/x['store']).resolve().is_relative_to(I.resolve()) and '/' not in x['run'] and x['run'] not in ['.','..']
(O/'claimed-positives.json').write_text(json.dumps({'reviewSha256':H(review),'rows':rows},indent=2)+'\n')
def run(row):
 inp=I/row['store'];h=H(inp);dest=O/'runs'/row['run'];cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(P),'--input',str(inp),'--run-id',row['runId'],'--source',str(S),'--manifest',str(L/'candidate-subject.v42.json'),'--manifest-sha256','f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307','--out',str(dest)]
 p=subprocess.run(cmd,capture_output=True,text=True);dest.mkdir(parents=True,exist_ok=True);(dest/'command.json').write_text(json.dumps({'argv':cmd,'exitCode':p.returncode},indent=2)+'\n');(dest/'stdout.json').write_text(p.stdout);(dest/'stderr.txt').write_text(p.stderr);assert H(inp)==h
 report=json.loads((dest/'report.json').read_bytes()) if (dest/'report.json').exists() else {'passed':False,'reason':p.stderr};return {'run':row['run'],'runId':row['runId'],'exportSha256':h,'exitCode':p.returncode,'transportAdmission':report.get('transportAdmission'),'structuralAdmission':report.get('structuralAdmission'),'semanticAdmission':report.get('semanticAdmission'),'reason':report.get('reason'),'passed':report.get('passed') is True}
results=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(run,row) for row in rows]):
  x=f.result();results.append(x);print(json.dumps(x),flush=True)
assert H(review)==json.loads((O/'claimed-positives.json').read_bytes())['reviewSha256']
d={'standing':'Exact27 claimed positives from completed source42 blind review checked by frozen42 owner, no repair/remint/import of consumer implementation. This is full structural+semantic replay per Run, not complete charter/application acceptance.','sourceManifestSha256':'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307','transportSha256':H(P),'reviewSha256':H(review),'runs':sorted(results,key=lambda x:x['run']),'passed':all(x['passed'] for x in results)};(O/'verification.json').write_text(json.dumps(d,indent=2)+'\n');shutil.copytree(O,L/O.name);print('ROOT COMPLETED BLIND42 EXACT POSITIVES',sum(x['passed'] for x in results),'/',len(results),flush=True)
