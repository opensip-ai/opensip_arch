"""Private activation only, after genuine independent approval and root assent."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
LIVE = Path('/Users/sb/code/opensip-ai/opensip')
BASE = Path('/tmp/opensip-implementation/m1-bootstrap-activation-01')
ROOT = BASE / 'product'
PY = '/tmp/opensip-implementation/metadata-reference-env/bin/python'
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
NPM = '/Users/sb/.nvm/versions/node/v24.16.0/lib/node_modules/npm/bin/npm-cli.js'
SELECTION = ARCH / 'docs/implementation/m1/bootstrap-selection-v1'


def pin(relative):
    raw = (ARCH / relative).read_bytes()
    return {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def run(name, command, cwd=ROOT, env=None, expected=0, contains=None):
    with (BASE / (name + '.stdout')).open('wb') as out, (BASE / (name + '.stderr')).open('wb') as err:
        p = subprocess.run(command, cwd=cwd, env=env, stdout=out, stderr=err, timeout=600)
    records.append({'name': name, 'command': command, 'exitCode': p.returncode})
    (BASE / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
    assert p.returncode == expected, (name, p.returncode)
    stdout = (BASE / (name + '.stdout')).read_text()
    if contains is not None:
        assert contains in stdout + (BASE / (name + '.stderr')).read_text(), (name, contains)
    return stdout


# Missing or incomplete approval is an actual stop, never filled with fixtures.
review = json.loads((ARCH / 'docs/implementation/m1/reviews/grok-bootstrap-selection-v1/review.json').read_text())
assent = json.loads((ARCH / 'docs/implementation/m1/bootstrap-selection-v1-unit.json').read_text())
assert review['verdict'] == 'ACCEPT-DESIGN-UNIT' and review['requiredFindings'] == []
assert assent['status'] == 'ACCEPTED-DESIGN-UNIT' and assent['rootSubstantiveAssent'] is True
assert not BASE.exists()
BASE.mkdir()
records = []
shutil.copytree(LIVE, ROOT, ignore=shutil.ignore_patterns('.git', 'target', 'node_modules', 'python-packages', '__pycache__', 'dist'))
lock = json.loads((ROOT / 'design-lock.json').read_text())
old_pin = lock['inventorySuccessors'][-1]['candidate']
old = json.loads((ARCH / old_pin['path']).read_text())
for version in (7, 8):
    new_pin = pin(f'docs/implementation/m1/repository-file-inventory.v{version}.json')
    lock['inventorySuccessors'].append({
        'parent': lock['inventorySuccessors'][-1]['candidate'],
        'candidate': new_pin,
        'record': pin(f'docs/implementation/m1/tooling-inventory-v{version}/successor.json'),
        'review': pin(f'docs/implementation/m1/reviews/grok-tooling-inventory-v{version}/review.json'),
        'assent': pin(f'docs/implementation/m1/tooling-inventory-v{version}-unit.json'),
    })
new = json.loads((ARCH / new_pin['path']).read_text())
indices = {row['path']: i for i, row in enumerate(new['files'])}
for override in lock['inventoryPassageInheritance']:
    assert override['parent'] == old_pin
    name = old['files'][int(override['selector']['jsonPointer'].split('/')[2])]['path']
    override['parent'] = new_pin
    override['selector'] = {'jsonPointer': f'/files/{indices[name]}/description'}
lock['inventoryPassageInheritance'].sort(key=lambda r: (r['parent']['path'], json.dumps(r['selector'], sort_keys=True)))
lock['contractSuccessors'].append({
    'record': pin('docs/implementation/m1/bootstrap-selection-v1/successor.json'),
    'subjectManifest': pin('docs/implementation/m1/bootstrap-selection-v1-subject.json'),
    'review': pin('docs/implementation/m1/reviews/grok-bootstrap-selection-v1/review.json'),
    'assent': pin('docs/implementation/m1/bootstrap-selection-v1-unit.json'),
})
(ROOT / 'design-lock.json').write_text(json.dumps(lock, indent=2) + '\n')
mapping = json.loads((SELECTION / 'materialization-map.json').read_text())
for row in mapping['files']:
    raw = (ARCH / row['candidatePath']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    destination = ROOT / row['productPath']
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
run('verify', [PY, '-I', '-B', str(ROOT / 'tools/verify_design.py'), '--architecture', str(ARCH), '--implementation', str(ROOT)])
for name in ('user.npmrc', 'global.npmrc'):
    (BASE / name).write_text('')
for lane in ('apps/report', 'providers/typescript', 'tools/contracts', 'tools/typescript-boundary'):
    run('provision-' + lane.replace('/', '-'), [NODE, NPM, 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund', '--cache', '/tmp/opensip-implementation/m1-typescript-bootstrap-candidate-01/provision-cache', '--userconfig', str(BASE / 'user.npmrc'), '--globalconfig', str(BASE / 'global.npmrc')], cwd=ROOT / lane)
# These already provisioned Python bytes remain independently checked by generator closure.
shutil.copytree(LIVE / 'tools/contracts/python-packages', ROOT / 'tools/contracts/python-packages')
for row in json.loads((ROOT / 'tools/contracts/generator-closure.json').read_text())['files']:
    raw = (ROOT / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
wrapper = [PY, '-I', '-B', str(ROOT / 'tools/check_typescript.py'), '--architecture', str(ARCH), '--node', NODE]
clean = json.loads(run('public-clean', wrapper).strip().splitlines()[-1])
assert clean['passed'] is True and [r['lane'] for r in clean['lanes']] == ['report', 'provider', 'generator']
for lane in ('apps/report', 'providers/typescript'):
    run('compile-' + lane.replace('/', '-'), [NODE, str(ROOT / lane / 'node_modules/typescript/bin/tsc'), '--project', str(ROOT / lane / 'tsconfig.json')])
run('public-built', wrapper)
run('unknown-lane', wrapper + ['--lane', 'not-selected'], expected=1, contains='unknown selected lane')
poison = BASE / 'ambient-poison.cjs'
marker = BASE / 'ambient-executed'
poison.write_text('require("node:fs").writeFileSync(' + json.dumps(str(marker)) + ', "bad");\n')
env = dict(os.environ, NODE_OPTIONS='--require=' + str(poison), NODE_PATH=str(BASE / 'not-a-module-root'), ESBUILD_BINARY_PATH=str(BASE / 'not-an-esbuild-binary'))
run('ambient-overrides-removed', wrapper, env=env)
assert not marker.exists()


def changed(name, relative, transform, contains):
    target = ROOT / relative
    original = target.read_bytes()
    try:
        target.write_bytes(transform(original))
        run(name, wrapper, expected=1, contains=contains)
    finally:
        target.write_bytes(original)


changed('unselected-registry', 'tools/typescript-lanes.json', lambda raw: raw + b'\n', 'registry is not selected exactly once')
changed('changed-checker', 'tools/typescript-boundary/src/check.mjs', lambda raw: raw + b'\n// changed input\n', 'input bytes differ: tools/typescript-boundary/src/check.mjs')
changed('changed-own-entry', 'tools/check_typescript.py', lambda raw: raw + b'\n# changed input\n', 'input bytes differ: tools/check_typescript.py')
changed('browser-node-refusal', 'apps/report/src/help-view.ts', lambda raw: raw + b'\nimport "node:fs";\n', 'browser-node')
extra = ROOT / 'apps/report/src/unselected-probe.ts'
assert not extra.exists()
try:
    extra.write_text('export const unselected = 1;\n')
    run('undeclared-source', wrapper, expected=1, contains='undeclared-local')
finally:
    extra.unlink()
run('wrong-node', [*wrapper[:-1], '/usr/bin/true'], expected=1, contains='Node executable type/length differs')
run('final-clean', wrapper)
(BASE / 'receipt.json').write_text(json.dumps({
    'standing': 'Private actual-approved bootstrap activation; not product installation or M1',
    'genuineInventorySuccessors': len(lock['inventorySuccessors']),
    'genuineContractSuccessors': len(lock['contractSuccessors']),
    'commands': records,
    'ambientMarkerAbsent': not marker.exists(),
    'ownedInputs': len(mapping['files']),
}, indent=2) + '\n')
print('Actual-approved private bootstrap activation passed.')
