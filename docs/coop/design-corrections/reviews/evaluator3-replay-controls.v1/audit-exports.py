import base64,hashlib,importlib.util,json,pathlib
root=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/evaluator3-replay-controls.v1')
p=root/'subject/docs/coop/design-corrections/foundation/identity-model.v3.py';s=importlib.util.spec_from_file_location('audited_model3',p);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
working=json.loads((root/'observed-working-report.json').read_text());reproduced=json.loads((root/'reproduced-report.json').read_text());working.pop('exportCount',None)
assert working==reproduced,'frozen subject did not reproduce exact working IDs/results'
expected={r['case']:r for r in reproduced['checks']};rows=[]
for p in sorted((root/'exports').glob('*.json')):
 d=json.loads(p.read_text());objects={k:(v['domain'],v['descriptor']) for k,v in d['objects'].items()};blobs={k:base64.b64decode(v,validate=True) for k,v in d['blobs'].items()}
 assert all(hashlib.sha256(v).hexdigest()==k for k,v in blobs.items()),p.name
 assert all(M.identifier(dom,v)==k for k,(dom,v) in objects.items()),p.name
 rid=M.open_run_closure(d['run'],objects,blobs)[0];want=expected[p.stem]['replay'];error=None
 try:admitted=M.close_run(d['run'],objects,blobs)
 except Exception as exc:error=str(exc)
 if isinstance(want,dict):assert error is None and admitted==want['runId'],(p.name,error)
 else:assert error=='EVALUATOR_COMPLETE_PROOF_REPLAY',(p.name,error)
 rows.append({'case':p.stem,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'allBlobsAndObjectsHashValid':True,'ownerClosure':'ADMIT','publicCloseRun':'REFUSE' if error else 'ADMIT','runId':rid,'detail':error})
assert set(expected)=={r['case'] for r in rows}
(root/'export-audit.json').write_text(json.dumps({'count':len(rows),'positiveAdmissions':sum(r['publicCloseRun']=='ADMIT' for r in rows),'semanticRefusals':sum(r['publicCloseRun']=='REFUSE' for r in rows),'exactFrozenReproduction':True,'rows':rows},indent=2)+'\n')
print({'exports':len(rows),'positiveAdmissions':sum(r['publicCloseRun']=='ADMIT' for r in rows),'semanticRefusals':sum(r['publicCloseRun']=='REFUSE' for r in rows)})
