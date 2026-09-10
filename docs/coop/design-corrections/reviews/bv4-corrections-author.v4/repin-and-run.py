"""Measured TEMPORARY repin + one completed-source development suite, in a FRESH disposable copy.

These repinned bytes are a DEVELOPMENT INSTRUMENT, not accepted pin evidence: the pins exist so
the checkers will run at all, and root runs the six actual pinned commands after integration.
Every earlier run directory is left untouched.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

SESSION = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
PY_BIN = '/tmp/opensip-architecture-review-env/bin/python'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

dest = SESSION / 'disposable' / sys.argv[1]
assert not dest.exists(), 'refusing to overwrite an existing run directory: %s' % dest
shutil.copytree(SESSION / 'work', dest / 'work')
root = dest / 'work'
dc = root / 'docs/coop/design-corrections'

changed = sorted(str(p.relative_to(root)) for p in root.rglob('*')
                 if p.is_file() and (SESSION / 'before-images' / p.name).exists()
                 and sha(p) != sha(SESSION / 'before-images' / p.name))
repins = []
for manifest, key in [(dc / 'foundation/source-pins.v1.json', 'files'),
                      (dc / 'workflows/source-pins.v1.json', 'files'),
                      (dc / 'native/source-pins.v2.json', 'pins')]:
    doc = json.loads(manifest.read_text())
    hit = 0
    for row in doc[key]:
        if row['path'] in changed:
            new = sha(root / row['path'])
            if new != row['sha256']:
                repins.append({'manifest': str(manifest.relative_to(root)), 'path': row['path'],
                               'pinnedSha256': row['sha256'], 'temporarySha256': new})
                row['sha256'] = new
                hit += 1
    if hit:
        manifest.write_text(json.dumps(doc, indent=2) + '\n')

SUITE = ['foundation/check-foundation.py', 'foundation/check-identity.py',
         'foundation/check-product-quality.py', 'foundation/check-product-configuration.py',
         'foundation/check-array-orders.py', 'workflows/check_workflows.v1.py',
         'native/check_native_evidence.v2.py']
results = []
for script in SUITE:
    proc = subprocess.run([PY_BIN, '-I', '-B', Path(script).name], cwd=dc / Path(script).parent,
                          capture_output=True, text=True)
    tail = [l for l in (proc.stdout + proc.stderr).strip().split('\n') if l.strip()][-1:]
    results.append({'script': script, 'exitCode': proc.returncode, 'lastLine': tail[0] if tail else ''})
    print(script, proc.returncode, tail[0] if tail else '')

report = {'disposableRoot': str(dest), 'changedFilesInThisCopy': changed,
          'temporaryRepinEntries': repins, 'temporaryRepinCount': len(repins),
          'results': results, 'allExitZero': all(r['exitCode'] == 0 for r in results)}
(SESSION / 'logs' / (sys.argv[1] + '.json')).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'repins': len(repins), 'allExitZero': report['allExitZero']}))
