"""C1b-0's design preflight (adapted from D2b-0's check_d2b0_preflight.py). Read-only; executes no generator or product
code.
1. verify_design on the candidate with the current lock refuses for exactly one of the two pre-binding reasons: the
   package's identity-v3 copy is not yet a selected generation or admission source, or its admission-registry copy is
   not, as RCA-1's and D2b-0's candidates refused before their binding.
2. The same verify_design, with only those two package copies added to the accepted set (what the C1b-0 successor's
   binding adds), passes, with the same generation-source and admission-source counts as the base: S4 re-pins one
   source and adds none.
3. The changed paths are exactly the expected set.
Usage: check_c1b0_preflight.py <output json>."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys, os
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'; W = A.parent / 'opensip-c1b0'
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r2'; ID3 = 'schemas/sources/identity-v3.schema.json'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
spec = importlib.util.spec_from_file_location('c1b0_verify_design', W / 'tools/verify_design.py'); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
assert (W / 'tools/verify_design.py').read_bytes() == (P / 'tools/verify_design.py').read_bytes()
lock = v.decode((W / 'design-lock.json').read_bytes()); assert (W / 'design-lock.json').read_bytes() == (P / 'design-lock.json').read_bytes()
REFUSALS = ('generation source is not selected by accepted design', 'admission source is not selected by accepted design')
out = {}
try:
    v.verify(A, lock, W); out['unboundRefusal'] = None
except v.DesignError as error:
    out['unboundRefusal'] = str(error)
copies = [pin(A, PRE + '/product/' + ID3), pin(A, PRE + '/admission-registry.json')]
assert (A / copies[0]['path']).read_bytes() == (W / ID3).read_bytes()
assert (A / copies[1]['path']).read_bytes() == (W / 'schemas/admission-registry.json').read_bytes()
for m in ('schemas/source-map.json', 'schemas/admission-source-map.json'):
    rows = [r for r in json.loads((W / m).read_bytes())['sources'] if r['implementationPath'] == ID3]
    assert len(rows) == 1 and rows[0]['architectureSource'] == copies[0], m
assert json.loads((W / 'schemas/admission-source-map.json').read_bytes())['registryArchitectureSource'] == copies[1]
added = {c['path']: c for c in copies}
originals = (v.generation_sources, v.admission_sources)
def widen(f):
    def bound(architecture, implementation, accepted):
        assert not set(added) & set(accepted)
        return f(architecture, implementation, {**accepted, **added})
    return bound
v.generation_sources, v.admission_sources = widen(originals[0]), widen(originals[1])
result = v.verify(A, lock, W); v.generation_sources, v.admission_sources = originals
out['withCopiesAccepted'] = dict(passed=result['passed'], generationSources=result['generationSources'], admissionSources=result['admissionSources'])
base = v.verify(A, lock, P)
out['base'] = dict(passed=base['passed'], generationSources=base['generationSources'], admissionSources=base['admissionSources'])
changed = sorted(subprocess.check_output(['/usr/bin/git', 'diff', '--name-only'], cwd=W, env=E).decode().split()
                 + subprocess.check_output(['/usr/bin/git', 'ls-files', '--others', '--exclude-standard'], cwd=W, env=E).decode().split())
expected = sorted(['apps/report/src/generated/report.ts', 'crates/contracts/src/generated/identity.rs', 'crates/evaluator/src/run_links.rs',
                   'crates/host/src/schema_sources.rs', 'crates/identity/src/schema_registry.rs', 'schemas/admission-registry.json',
                   'schemas/admission-source-map.json', 'schemas/registry.json', 'schemas/source-map.json', ID3,
                   'tools/contracts/generator-closure.json', 'tools/contracts/options.json',
                   # r2 (Codex C1B0-R1-RF-1): the two census records whose held-out rendering the batch's opening changes.
                   'crates/security/src/custody/discovery_census.json', 'crates/security/src/snapshot_ledger_census.json'])
out.update(changedPaths=changed, changedPathsExpected=changed == expected)
ok = (out['unboundRefusal'] in REFUSALS and out['withCopiesAccepted']['passed']
      and out['withCopiesAccepted']['generationSources'] == out['base']['generationSources']
      and out['withCopiesAccepted']['admissionSources'] == out['base']['admissionSources'] and changed == expected)
out['passed'] = ok
Path(sys.argv[1]).write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, sort_keys=True)); sys.exit(0 if ok else 1)
