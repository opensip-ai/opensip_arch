"""D2b-0's design preflight and admission-only assertions (LD-D2B0-A). Read-only; executes no generator or product code.
1. verify_design on the candidate with the current lock refuses for exactly one reason, the unbound admission registry
   copy ('admission source is not selected by accepted design'), as RCA-1's candidate did before its binding.
2. The same verify_design, with only that copy added to the accepted set (what the D2b-0 successor's binding adds),
   passes: generation sources unchanged, admission sources (52) and aliases verified.
3. Admission-only: every generator input and output, the Cargo manifests and the census receipt are the base's bytes,
   and the census's reference binding (generator-closure.json) is unchanged, so the blind receipt stays current.
Usage: check_d2b0_preflight.py <output json>."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys, os
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'; W = A.parent / 'opensip-d2b0'
PRE = 'docs/implementation/m3/supervisor-d/d2b-0-r1'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
spec = importlib.util.spec_from_file_location('d2b0_verify_design', W / 'tools/verify_design.py'); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
assert (W / 'tools/verify_design.py').read_bytes() == (P / 'tools/verify_design.py').read_bytes()
lock = v.decode((W / 'design-lock.json').read_bytes()); assert (W / 'design-lock.json').read_bytes() == (P / 'design-lock.json').read_bytes()
out = {}
try:
    v.verify(A, lock, W); out['unboundRefusal'] = None
except v.DesignError as error:
    out['unboundRefusal'] = str(error)
copy = pin(A, PRE + '/admission-registry.json')
assert json.loads((W / 'schemas/admission-source-map.json').read_bytes())['registryArchitectureSource'] == copy
assert (A / copy['path']).read_bytes() == (W / 'schemas/admission-registry.json').read_bytes()
original = v.admission_sources
def bound(architecture, implementation, accepted):
    assert copy['path'] not in accepted
    return original(architecture, implementation, {**accepted, copy['path']: copy})
v.admission_sources = bound
result = v.verify(A, lock, W); v.admission_sources = original
out['withCopyAccepted'] = dict(passed=result['passed'], generationSources=result['generationSources'], admissionSources=result['admissionSources'])
base = v.verify(A, lock, P)
out['base'] = dict(passed=base['passed'], generationSources=base['generationSources'], admissionSources=base['admissionSources'])
# Admission-only (LD-D2B0-A): the generator's inputs and outputs, the manifests, the census receipt.
registry = json.loads((P / 'schemas/registry.json').read_bytes()); closure = json.loads((P / 'tools/contracts/generator-closure.json').read_bytes())
same = ['schemas/registry.json', 'tools/contracts/generator-closure.json'] + [r['path'] for r in closure['files']] + [r['path'] for r in registry['recipes'][0]['outputs']]
same += ['Cargo.toml', 'Cargo.lock', 'crates/identity/Cargo.toml', 'crates/host/Cargo.toml', 'crates/storage/Cargo.toml',
         'crates/security/src/custody/discovery_census_held_out.json', 'tools/security/discovery_census.py']
# Ignored pinned closure inputs (node_modules, python-packages) are not in the worktree; only the tracked ones exist to differ.
tracked = set(subprocess.check_output(['/usr/bin/git', 'ls-files'], cwd=P, env=E).decode().splitlines())
ignored = sorted(p for p in set(same) if p not in tracked); assert all(p.startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/')) for p in ignored)
assert not any((W / p).exists() for p in ignored)
differs = sorted(p for p in set(same) - set(ignored) if (W / p).read_bytes() != (P / p).read_bytes())
changed = sorted(subprocess.check_output(['/usr/bin/git', 'diff', '--name-only'], cwd=W, env=E).decode().split()
                 + subprocess.check_output(['/usr/bin/git', 'ls-files', '--others', '--exclude-standard'], cwd=W, env=E).decode().split())
expected = sorted(['crates/host/src/schema_sources.rs', 'crates/host/tests/admission_tests.rs', 'crates/identity/src/schema.rs', 'crates/identity/src/schema_registry.rs', 'crates/storage/src/schema_sources.rs',
                   'schemas/admission-registry.json', 'schemas/admission-source-map.json',
                   'schemas/sources/rust-subject-scope-v1.schema.json', 'schemas/sources/symbol-census-v1.schema.json'])
out.update(admissionOnly=dict(generatorInputsOutputsManifestsReceiptChecked=len(set(same)) - len(ignored), ignoredPinnedInputsAbsent=len(ignored), differing=differs,
                              changedPaths=changed, changedPathsExpected=changed == expected))
ok = (out['unboundRefusal'] == 'admission source is not selected by accepted design' and out['withCopyAccepted']['passed']
      and out['withCopyAccepted']['admissionSources']['sourcesVerified'] == out['base']['admissionSources']['sourcesVerified'] + 2
      and out['withCopyAccepted']['generationSources'] == out['base']['generationSources'] and not differs and changed == expected)
out['passed'] = ok
Path(sys.argv[1]).write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, sort_keys=True)); sys.exit(0 if ok else 1)
