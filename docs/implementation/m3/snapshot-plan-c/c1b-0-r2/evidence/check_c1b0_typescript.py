"""C1b-0's TypeScript lanes with the two package copies accepted. Before the binding, tools/check_typescript.py's own
design approval refuses the candidate for exactly the pre-binding reason the preflight records ('generation source is
not selected by accepted design'), before any TypeScript runs. This wrapper runs the product's check_typescript.check
unchanged, with only its verify_design's generation_sources and admission_sources given the package's identity-v3 and
admission-registry copies as accepted (what the C1b-0 successor's binding adds; check_c1b0_preflight.py's widening), so
the regenerated report.ts is actually type-checked. Usage: check_c1b0_typescript.py --root <worktree> --architecture
<arch> --node <node> --lane <lane>."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-c1b0'
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r2'
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
added = {c['path']: c for c in (pin(A, PRE + '/product/schemas/sources/identity-v3.schema.json'), pin(A, PRE + '/admission-registry.json'))}
assert (A / (PRE + '/product/schemas/sources/identity-v3.schema.json')).read_bytes() == (W / 'schemas/sources/identity-v3.schema.json').read_bytes()
spec = importlib.util.spec_from_file_location('c1b0_check_typescript', W / 'tools/check_typescript.py'); ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
real_spec = importlib.util.spec_from_file_location
class Loader:
    def __init__(self, inner): self.inner = inner
    def create_module(self, s): return self.inner.create_module(s)
    def exec_module(self, module):
        self.inner.exec_module(module)
        for name in ('generation_sources', 'admission_sources'):
            original = getattr(module, name)
            def bound(architecture, implementation, accepted, original=original):
                assert not set(added) & set(accepted)
                return original(architecture, implementation, {**accepted, **added})
            setattr(module, name, bound)
def widened(name, location, *a, **k):
    s = real_spec(name, location, *a, **k)
    if name == 'design_preflight' and Path(location).resolve() == (W / 'tools/verify_design.py').resolve():
        s.loader = Loader(s.loader)
    return s
importlib.util.spec_from_file_location = widened
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--architecture', type=Path, required=True)
parser.add_argument('--node', type=Path, required=True)
parser.add_argument('--lane', required=True)
result = ct.check(parser.parse_args())
print(json.dumps(dict(result, packageCopiesAccepted=sorted(added))))
sys.exit(0 if result['passed'] else 1)
