import importlib.util,sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections'
sp=importlib.util.spec_from_file_location('bc',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
out={}
for label,kw in [('resolved-match',dict(resolved=True,has_match=True)),('resolved-nomatch',dict(resolved=True,has_match=False))]:
    run,objects,blobs=f.build(**kw)
    out[label]=f.M.close_run(run,objects,blobs)
out['nativeModelSha256']=hashlib.sha256((dc/'native/native_evidence_model.v2.py').read_bytes()).hexdigest()
out['identityModelSha256']=hashlib.sha256((dc/'foundation/identity-model.py').read_bytes()).hexdigest()
print(json.dumps(out,indent=1))
