"""Path-only adaptation of /tmp/opensip-design-corrections/root-nested-workspace-probe.v1/probe.py.

Differences from root's probe, and only these: the native model path and the report path are arguments (root's probe
read the frozen39 snapshot and wrote report.json next to itself). The cases, marker constructor, call and recorded
fields are byte-for-byte root's. Usage: root_adapted.py SOURCE_ROOT REPORT_JSON
"""
from pathlib import Path
import importlib.util, json, hashlib, sys
S = Path(sys.argv[1]); OUT = Path(sys.argv[2])
p = S / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'; sp = importlib.util.spec_from_file_location('root_nested_workspace', p); N = importlib.util.module_from_spec(sp); sp.loader.exec_module(N)
marker=lambda w:{'sha256':'a'*64,'isCargoWorkspace':w}
cases=[('ordinary-workspace',{'Cargo.toml':marker(True),'pkg/Cargo.toml':marker(False)},None),('nested-workspace-leaf',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True)},None),('nested-workspace-with-package',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True),'nested/pkg/Cargo.toml':marker(False)},None),('explicit-inner-workspace',{'Cargo.toml':marker(True),'nested/Cargo.toml':marker(True),'nested/pkg/Cargo.toml':marker(False)},['nested'])]
rows=[]
for name,markers,roots in cases:
 r={'name':name,'markers':markers,'explicitRoots':roots}
 try:r['output']=N.discover_units(markers,explicit_workspace_roots=roots);r['raised']=False
 except Exception as e:r.update(raised=True,exceptionType=type(e).__name__,reason=str(e))
 rows.append(r)
d={'standing':'Path-only adaptation of root\'s standalone discovery reference probe (model and report paths are arguments); trusted marker observations, no real Cargo or operational host invocation.','sourceRoot':str(S),'modelSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':rows}
OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps([{'name':r['name'],'raised':r['raised'],'exception':r.get('exceptionType')}for r in rows]))
