from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,hashlib,subprocess,shutil
B=Path('/tmp/opensip-design-corrections');O=Path(__file__).parent;C=B/'consumer-b.v24-source45.v1/output';S=B/'candidate-subject.v45';L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');V=C/'vectors/graph-query.json';P=O/'replay-query.py';T=B/'root-blind39-transport-preparation.v1/check-export.py';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(P)=='ef17a34341c6736528f15b78ac30c3255b8060277fdfbd20c919298b720aaebe' and h(T)=='6fa376bb59548bd9d52dbc52a3a35f27e0d12e4a963a6730624467c3a8f63074';assert json.loads((C.parent/'process-completion.json').read_bytes())['exitCode']==0
v=json.loads(V.read_bytes());vh=h(V);r=json.loads((C/'blind-review.json').read_bytes());positives={x['run']:x for x in r['claimedCompletePositives']};assert len(v['vectors'])==66
for label,rid in v['runs'].items():assert positives[label]['runId']==rid

def run(item):
 label,rid=item;export=C/positives[label]['store'];eh=h(export);out=O/label;cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(P),'--source',str(S),'--manifest',str(L/'candidate-subject.v45.json'),'--manifest-sha256','8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155','--export',str(export),'--vectors',str(V),'--transport',str(T),'--transport-sha256',h(T),'--run-id',rid,'--run-label',label,'--out',str(out)];p=subprocess.run(cmd,capture_output=True,text=True);out.mkdir(exist_ok=True);(out/'command.json').write_text(json.dumps({'argv':cmd,'exitCode':p.returncode},indent=2)+'\n');(out/'stdout.json').write_text(p.stdout);(out/'stderr.txt').write_text(p.stderr);assert h(export)==eh
 d=json.loads((out/'report.json').read_bytes()) if (out/'report.json').exists() else {};return {'run':label,'exitCode':p.returncode,'semanticAdmission':d.get('semanticAdmission'),'captureCompleted':d.get('captureCompleted'),'cases':len(d.get('cases',[])),'reportSha256':h(out/'report.json') if (out/'report.json').exists() else None}
results=[]
with ThreadPoolExecutor(max_workers=3) as pool:
 for f in as_completed([pool.submit(run,item) for item in [(label, positives[label]['runId']) for label in sorted({x['run'] for x in v['vectors'] if '~' not in x['run']})]]):
  x=f.result();results.append(x);print(json.dumps(x),flush=True)
assert h(V)==vh
d={'standing':'Actual strong-owner outcomes over exact exported admitted Runs and exact requests/host observations. Capture completion is NOT response conformance, cursor portability, renderer parity, entire charter or application acceptance. Root substantive comparison required.','sourceManifestSha256':'8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155','vectorsSha256':vh,'runs':sorted(results,key=lambda x:x['run']),'allCaptured':all(x['captureCompleted'] is True for x in results),'cases':sum(x['cases'] for x in results),'rootBlindAssent':False};(O/'capture.json').write_text(json.dumps(d,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps(d),flush=True)
