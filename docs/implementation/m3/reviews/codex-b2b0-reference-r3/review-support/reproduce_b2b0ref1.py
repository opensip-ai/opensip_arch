"""Codex B2B0REF-1's two reproductions, run against the r1 and the r2 reference (review support, not a subject member)."""
import importlib.util, json, sys
from pathlib import Path
A = Path(sys.argv[1]); out = {}
sys.path.insert(0, str(Path(sys.argv[2]) / 'tools/contracts/python-packages'))
spec = importlib.util.spec_from_file_location('chk', Path(__file__).with_name('check.py')); chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
cases = {
    'repro-1 cwd below .opensip': chk.inp(chk.tree(dirs=['.opensip/hidden-repo'], files=['package.json', '.opensip/opensip.json'], vcs=['.opensip/hidden-repo']), explicitProject='/h/w', cwd='/h/w/.opensip/hidden-repo'),
    'repro-2 cwd in an unrelated sibling': chk.inp(chk.tree(dirs=['a/u', 'b/repo'], files=['a/u/package.json'], vcs=['b/repo']), explicitProject='/h/w', explicitJoins=['a/u'], cwd='/h/w/b/repo'),
}
for label, path in [('r1', 'r1-archive/discovery_scan_reference.py'), ('r2', 'discovery_scan_reference.py')]:
    spec = importlib.util.spec_from_file_location('ref_' + label, Path(__file__).parent / path); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
    slm, rule = ref.load(A)
    for name, i in cases.items():
        r = ref.current(slm, rule, i)
        out['%s %s' % (label, name)] = dict(status=r[0]['status'], nestedRepositories=r[0]['provenance']['nestedRepositories'])
print(json.dumps(out, indent=1))
