"""F8b step 5 (generation): run the selected pipeline on the prepared worktree with rebuild-02.

As 468a's run_generation468a.py: the public entry point cannot run until F8b is selected,
so this checks every closure pin, the registry recipe joins and the observed build receipt,
then calls pipeline.run with the selected closure. It never writes the product; the lead
copies report.ts afterwards. The work directory is kept for step 6's probe.
Usage: run_generation_f8b.py WORKTREE OUTPUT_DIR (OUTPUT_DIR must not exist)."""
from pathlib import Path
from types import SimpleNamespace
import hashlib, importlib.util, json, sys
P = Path(sys.argv[1]).resolve(strict=True); OUT = Path(sys.argv[2])
NODE = Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node')
GEN = Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator')
PY = Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python')
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
closure_raw = (P / 'tools/contracts/generator-closure.json').read_bytes(); closure = json.loads(closure_raw)
pinned = {}
for row in closure['files']:
    raw = (P / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
    pinned[row['path']] = raw
registry_raw = (P / 'schemas/registry.json').read_bytes(); registry = json.loads(registry_raw)
recipe = registry['recipes'][0]
assert recipe['generatorClosureSha256'] == hashlib.sha256(closure_raw).hexdigest()
assert set(recipe['sourceSha256s']) == {r['sourceSha256'] for r in registry['sources']}
toolchain = json.loads(pinned['tools/contracts/toolchain.json'])['executables']
assert toolchain == closure['toolchain'] and pin(GEN.read_bytes()) == {'bytes': toolchain['generator']['bytes'], 'sha256': toolchain['generator']['sha256']}
load(P / 'tools/contracts/adapter.py', 'adapter_f8b').validate_build_receipt(json.loads(pinned['tools/contracts/build-receipt.json']), pinned, toolchain['generator'])
pipeline = load(P / 'tools/contracts/pipeline.py', 'pipeline_f8b')
args = SimpleNamespace(root=P, output=OUT, node=NODE, generator=GEN, python=PY)
result = pipeline.run(args, selected_closure=closure['files'], provenance={
    'registrySha256': hashlib.sha256(registry_raw).hexdigest(), 'generatorClosureSha256': recipe['generatorClosureSha256']})
root = OUT / result['outputRoot']
changed, unchanged = [], []
for row in recipe['outputs']:
    new = (root / row['path']).read_bytes(); old = (P / row['path']).read_bytes()
    (changed if new != old else unchanged).append(row['path'])
    if new != old:
        nl, ol = new.split(b'\n'), old.split(b'\n')
        lines = [i + 1 for i in range(max(len(nl), len(ol))) if (nl[i] if i < len(nl) else None) != (ol[i] if i < len(ol) else None)]
        changed[-1] = {'path': row['path'], 'before': pin(old), 'after': pin(new), 'changedLines': lines}
summary = {'passed': result['passed'], 'generator': pin(GEN.read_bytes()), 'registry': pin(registry_raw), 'closure': pin(closure_raw),
           'outputs': len(recipe['outputs']), 'changed': changed, 'unchanged': sorted(unchanged), 'productWritten': False,
           'standing': 'Unselected prospective development generation for F8b with rebuild-02; not selection, drift acceptance or release qualification.'}
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
