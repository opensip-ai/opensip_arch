"""Show the reference pruned-tree count's dependence on supplied observations."""
import argparse,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
s=importlib.util.spec_from_file_location('audit_discovery_defaults',a.source/'docs/coop/design-corrections/discovery-defaults.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[{'suppliedHiddenMarkerPaths':n,'result':m.enumerate_units(['package.json']+[f'node_modules/dep{i}/package.json' for i in range(n)])} for n in [0,1,4200]]
assert all(r['result']['unitDirs']==[''] for r in rows)
a.out.write_text(json.dumps({'standing':'AUTHOR observation; the instrument operates over supplied paths, not filesystem traversal. This does not prove that a production scanner violates custody.','observations':rows},indent=2)+'\n');print('Same selected root for 0/1/4200 supplied hidden markers; pruning provenance depends on supplied inventory.')
