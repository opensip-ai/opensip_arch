"""Prospective 468a generation: run the selected pipeline on the prepared worktree.

The public entry point is not used because the candidate architecture source is
not yet a selected design input; this is unselected development generation only.
It checks every closure pin and the build receipt first and never writes the product.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib, importlib.util, json
P = Path('/Users/sb/code/opensip-ai/opensip-468a')
OUT = Path('/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/468a/gen-candidate')
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
closure = json.loads((P / 'tools/contracts/generator-closure.json').read_text())
pinned = {}
for row in closure['files']:
    raw = (P / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
    pinned[row['path']] = raw
registry = json.loads((P / 'schemas/registry.json').read_text())
recipe = registry['recipes'][0]
assert recipe['generatorClosureSha256'] == hashlib.sha256((P / 'tools/contracts/generator-closure.json').read_bytes()).hexdigest()
assert set(recipe['sourceSha256s']) == {r['sourceSha256'] for r in registry['sources']}
toolchain = json.loads(pinned['tools/contracts/toolchain.json'])['executables']
assert toolchain == closure['toolchain']
load(P / 'tools/contracts/adapter.py', 'adapter468a').validate_build_receipt(json.loads(pinned['tools/contracts/build-receipt.json']), pinned, toolchain['generator'])
pipeline = load(P / 'tools/contracts/pipeline.py', 'pipeline468a')
args = SimpleNamespace(root=P, output=OUT, node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),
    generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01/opensip-contract-generator'),
    python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
result = pipeline.run(args, selected_closure=closure['files'], provenance={
    'registrySha256': hashlib.sha256((P / 'schemas/registry.json').read_bytes()).hexdigest(), 'generatorClosureSha256': recipe['generatorClosureSha256']})
root = OUT / result['outputRoot']
changed = []
for row in recipe['outputs']:
    new = (root / row['path']).read_bytes(); old = (P / row['path']).read_bytes()
    if new != old: changed.append({'path': row['path'], 'before': {'bytes': len(old), 'sha256': hashlib.sha256(old).hexdigest()}, 'after': {'bytes': len(new), 'sha256': hashlib.sha256(new).hexdigest()}})
summary = {'passed': result['passed'], 'outputs': len(recipe['outputs']), 'changed': changed, 'productWritten': False,
           'standing': 'Unselected prospective development generation for 468a; not selection, drift acceptance or release qualification.'}
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
