from pathlib import Path
import importlib.util,json,hashlib
S=Path('/tmp/opensip-design-corrections/target-provider-return-successor.v1/docs/coop/design-corrections/foundation')
spec=importlib.util.spec_from_file_location('root_provider_return_fixture',S/'check-provider-attribution-return.v2.py');T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
fid=T.fact2('1');record=T.sidecar(fid,'file:src/a.ts',evaluation='src/a.ts');envelope=T.envelope([record]);rows=[]
for origin in ['provider-return','host-internal']:
 try:
  r=T.M.admit_provider_attribution_return(envelope,facts={fid:T.imports_fact(fid)},origin=origin,**T.kw());rows.append({'origin':origin,'result':'ADMIT','status':r['status'],'capturedRefs':r['hostDerivedRefs']})
 except Exception as exc:rows.append({'origin':origin,'result':'REFUSE','type':type(exc).__name__,'reason':str(exc)})
report={'standing':'Actual standalone provider-return admission helper on author synthetic maps, not an admitted Plan/stage/Run or whole evaluator result. Exact same structurally valid envelope across origins.','modelSha256':hashlib.sha256((S/'provider_attribution_return_model.v2.py').read_bytes()).hexdigest(),'results':rows}
Path(__file__).with_name('report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
