"""Codex B2B0REF-3 and B2B0REF-4 reproductions, run against the r2 and the r3 reference (review support, not a subject member)."""
import importlib.util, json, sys
from pathlib import Path
A = Path(sys.argv[1]); out = {}
sys.path.insert(0, str(Path(sys.argv[2]) / 'tools/contracts/python-packages'))
spec = importlib.util.spec_from_file_location('chk', Path(__file__).parent / 'check.py'); chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
rel = '/'.join('d' for _ in range(257))
cases = {'B2B0REF-3 .opensip with vcs': chk.inp(chk.tree(files=['package.json'], dirs=['.opensip'], vcs=['.opensip']), explicitProject='/h/w'),
         'B2B0REF-4 opensip.json at depth 257': chk.inp(chk.tree(dirs=[rel], files=['package.json', rel + '/opensip.json']), explicitProject='/h/w')}
for label, path in [('r2', 'r2-archive/discovery_scan_reference.py'), ('r3', 'discovery_scan_reference.py')]:
    spec = importlib.util.spec_from_file_location('ref_' + label, Path(__file__).parent / path); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
    slm, rule = ref.load(A)
    for name, i in cases.items():
        r = ref.current(slm, rule, i)[0]['provenance']
        out['%s %s' % (label, name)] = dict(nestedRepositories=r['nestedRepositories'], nestedProjects=[p[:40] + '...' if len(p) > 40 else p for p in r['nestedProjects']])
print(json.dumps(out, indent=1))
