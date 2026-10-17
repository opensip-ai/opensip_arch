"""C1b-0's generation (adapted from D2b-0b's run_d2b0b_generation.py, itself RCA-1's run_rust3_identity_generation_r1.py): the selected pipeline run over the
candidate's exact generator closure. Usage: run_d2b0b_generation.py <fresh output dir> <summary json> [--check] [--unpinned].
Without --check every output is written back to the worktree and each change recorded; with --check nothing is
written, and the run must reproduce the worktree's outputs byte for byte (the determinism and drift check). No HOME
override, no install or build. --unpinned (mutation detectors only) re-pins the closure from the current bytes in
memory, so a mutated input reaches the generator's own checks instead of the pin assertion."""
from pathlib import Path
from types import SimpleNamespace
import hashlib, importlib.util, json, os, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1b0'); O = Path(sys.argv[1]); S = Path(sys.argv[2]); CHECK = '--check' in sys.argv[3:]; UNPINNED = '--unpinned' in sys.argv[3:]
os.setpriority(os.PRIO_PROCESS, 0, 10)
def load(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def pin(p): b = p.read_bytes(); return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
closure = json.loads((W / 'tools/contracts/generator-closure.json').read_text()); registry = json.loads((W / 'schemas/registry.json').read_text())
recipe = registry['recipes'][0]
if UNPINNED:
    closure['files'] = [dict(path=r['path'], **pin(W / r['path'])) for r in closure['files']]
assert UNPINNED or recipe['generatorClosureSha256'] == pin(W / 'tools/contracts/generator-closure.json')['sha256']
assert UNPINNED or recipe['optionsSha256'] == pin(W / 'tools/contracts/options.json')['sha256']
assert set(recipe['sourceSha256s']) == {r['sourceSha256'] for r in registry['sources']}
for row in closure['files']: assert pin(W / row['path']) == {k: row[k] for k in ['bytes', 'sha256']}, row['path']
assert "'HOME':" not in (W / 'tools/contracts/pipeline.py').read_text()
pipeline = load(W / 'tools/contracts/pipeline.py', 'candidate_pipeline')
args = SimpleNamespace(root=W, output=O, node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),
                       generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),
                       python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
result = pipeline.run(args, selected_closure=closure['files'],
                      provenance=dict(registrySha256=pin(W / 'schemas/registry.json')['sha256'], generatorClosureSha256=recipe['generatorClosureSha256']))
root = O / result['outputRoot']; changed = []
assert sorted(r['path'] for r in result['outputs']) == sorted(r['path'] for r in recipe['outputs'])
for row in result['outputs']:
    p = W / row['path']; raw = (root / row['path']).read_bytes(); assert pin(root / row['path']) == {k: row[k] for k in ['bytes', 'sha256']}
    if p.read_bytes() != raw:
        changed.append(dict(path=row['path'], before=pin(p), after=pin(root / row['path'])))
        if not CHECK: p.write_bytes(raw)
S.write_text(json.dumps(dict(passed=result['passed'] and (not CHECK or not changed), check=CHECK, result=result, changed=changed,
                             standing='UNREVIEWED C1b-0 GENERATION (S4); NO SOURCE OR CONSUMER ADMISSION', HOMEOverride=False,
                             allChildrenPriorityInherited=10, actualQualification=False), indent=2) + '\n')
print('Generation', 'check' if CHECK else 'write', 'passed' if result['passed'] else 'FAILED', len(changed), 'outputs differ')
sys.exit(0 if result['passed'] and (not CHECK or not changed) else 1)
