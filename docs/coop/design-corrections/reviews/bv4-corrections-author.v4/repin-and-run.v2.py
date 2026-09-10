"""Measured TEMPORARY repin + one completed-source development suite, in a FRESH disposable copy.

The repinned bytes are a DEVELOPMENT INSTRUMENT, not accepted pin evidence: they exist only so the
checkers will consent to run at all. Root runs the six actual pinned commands after integration.
No earlier run directory is reused: this refuses to start if its destination already exists.

v2 of the runner. v1 (disposable/suite-final-v4a, logs/suite-final-v4a.json) is retained and failed:
it detected changed files by BASENAME against before-images/, which is a mirrored tree, so it
measured zero repins, and it invoked the checkers without their required --report argument.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

SESSION = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
PY_BIN = '/tmp/opensip-architecture-review-env/bin/python'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

MANIFEST = json.loads((SESSION / 'root-input/candidate-subject.v14.json').read_text())
FROZEN = {r['path']: r['sha256'] for r in MANIFEST['files']}

dest = SESSION / 'disposable' / sys.argv[1]
assert not dest.exists(), 'refusing to overwrite an existing run directory: %s' % dest
shutil.copytree(SESSION / 'work', dest / 'work')
root, reports = dest / 'work', dest / 'reports'
reports.mkdir()
dc = root / 'docs/coop/design-corrections'

# what this copy actually changes against frozen v14, measured, not asserted
changed = sorted(p for p, h in FROZEN.items() if sha(root / p) != h)
added = sorted(str(p.relative_to(root)) for p in root.rglob('*')
               if p.is_file() and str(p.relative_to(root)) not in FROZEN)
deleted = sorted(p for p in FROZEN if not (root / p).exists())
assert not added and not deleted, (added, deleted)

repins = []
for manifest, key in [(dc / 'foundation/source-pins.v1.json', 'files'),
                      (dc / 'workflows/source-pins.v1.json', 'files'),
                      (dc / 'native/source-pins.v2.json', 'pins')]:
    doc = json.loads(manifest.read_text())
    hit = 0
    for row in doc[key]:
        if row['path'] in changed and row['sha256'] != sha(root / row['path']):
            repins.append({'manifest': str(manifest.relative_to(root)), 'path': row['path'],
                           'frozenSha256': row['sha256'], 'temporarySha256': sha(root / row['path'])})
            row['sha256'] = sha(root / row['path'])
            hit += 1
    if hit:
        manifest.write_text(json.dumps(doc, indent=2) + '\n')
        print('repinned %d entries in %s' % (hit, manifest.relative_to(root)))

SUITE = ['foundation/check-foundation.py', 'foundation/check-identity.py',
         'foundation/check-product-quality.py', 'foundation/check-product-configuration.py',
         'foundation/check-array-orders.py', 'workflows/check_workflows.v1.py',
         'native/check_native_evidence.v2.py']
results = []
for script in SUITE:
    name = Path(script).name
    report = reports / (name.replace('.py', '') + '.json')
    proc = subprocess.run([PY_BIN, '-I', '-B', name, '--report', str(report)],
                          cwd=dc / Path(script).parent, capture_output=True, text=True)
    lines = [l for l in (proc.stdout + proc.stderr).strip().split('\n') if l.strip()]
    results.append({'script': script, 'exitCode': proc.returncode,
                    'lastLine': lines[-1][:400] if lines else '',
                    'report': str(report.relative_to(dest))})
    print(script, proc.returncode, (lines[-1][:200] if lines else ''))

out = {'disposableRoot': str(dest), 'runner': 'repin-and-run.v2.py',
       'changedFilesVsFrozenV14': changed, 'additions': added, 'deletions': deleted,
       'temporaryRepinEntries': repins, 'temporaryRepinCount': len(repins),
       'results': results, 'allExitZero': all(r['exitCode'] == 0 for r in results)}
(SESSION / 'logs' / (sys.argv[1] + '.json')).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'changed': len(changed), 'repins': len(repins), 'allExitZero': out['allExitZero']}))
