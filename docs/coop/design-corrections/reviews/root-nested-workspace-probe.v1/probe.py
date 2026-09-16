from pathlib import Path
import importlib.util,json,hashlib
B=Path('/tmp/opensip-design-corrections');O=Path(__file__).parent;S=B/'candidate-subject.v39';p=S/'docs/coop/design-corrections/native/native_evidence_model.v2.py';sp=importlib.util.spec_from_file_location('root_nested_workspace',p);N=importlib.util.module_from_spec(sp);sp.loader.exec_module(N)
marker=lambda w:{'sha256':'a'*64,'isCargoWorkspace':w}
cases=[('ordinary-workspace',{'Cargo.toml':marker(True),'pkg/Cargo.toml':marker(False)},None),('nested-workspace-leaf',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True)},None),('nested-workspace-with-package',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True),'nested/pkg/Cargo.toml':marker(False)},None),('explicit-inner-workspace',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True),'nested/pkg/Cargo.toml':marker(False)},['nested'])]
rows=[]
for name,markers,roots in cases:
 r={'name':name,'markers':markers,'explicitRoots':roots}
 try:r['output']=N.discover_units(markers,explicit_workspace_roots=roots);r['raised']=False
 except Exception as e:r.update(raised=True,exceptionType=type(e).__name__,reason=str(e))
 rows.append(r)
d={'standing':'Root independently authored standalone discovery reference probe, trusted marker observations/no real Cargo or operational host invocation. Records observed outcomes without claiming compiler behavior or product qualification.','sourceManifestSha256':'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009','modelSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':rows};(O/'report.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps([{'name':r['name'],'raised':r['raised'],'exception':r.get('exceptionType')}for r in rows]))
