from pathlib import Path
import json,hashlib,subprocess,importlib.util,datetime
B=Path('/tmp/opensip-design-corrections');F=B/'closure-kind-successor.v1/docs/coop/design-corrections/foundation'
OUT=B/'closure-kind-root-review.v1';OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('parser',B/'check-blind12-exported-graphs.v1.py');M=load('identity',F/'identity-model.v3.py')
src=B/'consumer-b.v12-team-other-runs-corrections.v6/output/runs/ts.store.json'
objects,blobs=P.decode_store(src.read_bytes(),M);rid='run3:26dd437679e894c1cf01d5fb4b94de66bc15cc4ce8c8aaf26b3864144bc60164'
try:M.open_run_closure(objects[rid][1],objects,blobs)
except M.C.AdmissionError as e:
 assert str(e)=='CLOSURE_FIELD_KIND:import.producerClosure:provider',str(e)
 measured={'result':'REFUSE','detail':str(e)}
else:raise AssertionError('Prior wrong import producer still admitted')
(OUT/'exact-prior-import-refusal.json').write_text(json.dumps({'standing':'Exact historical consumer bytes tested against isolated reference correction. Not consumer acceptance or blind-team input.','exportSha256':sha(src),'runId':rid,'modelSha256':sha(F/'identity-model.v3.py'),**measured},indent=2)+'\n')
command=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(F/'check-replay.v3.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(command,capture_output=True,text=True,timeout=600)
(OUT/'full-replay.stdout.json').write_text(r.stdout);(OUT/'full-replay.stderr').write_text(r.stderr)
report=json.loads(r.stdout) if r.returncode==0 else None
receipt={'command':command,'startedAt':started,'exitCode':r.returncode,'reportPassed':report.get('passed') if report else None,'reportedControls':report.get('count') if report else None,'standing':'Scoped root reference check, unsealed whole-source pins; not independent review or product qualification.','sourceFiles':[{'path':n,'sha256':sha(F/n)} for n in ['identity-model.v3.py','evaluator_graph_fixture.v3.py','closure_field_kind_controls.v3.py','check-replay.v3.py']]}
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
raise SystemExit(r.returncode)
