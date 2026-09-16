"""PROBE I — run the two planning checkers in --check mode (never --write) inside the
verified disposable copy, so no frozen byte can be rewritten, and confirm the frozen
snapshot is unchanged afterwards."""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
KIT = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
PY = '/tmp/opensip-architecture-review-env/bin/python'
man = {r['path']: r for r in json.load(open(MAN))['files']}

# the operations scripts and the v25 manifest are needed in the copy
EXTRA = ['docs/operations/check_implementation_planning.py',
         'docs/operations/check_repository_file_inventory.py',
         'docs/coop/design-corrections/reviews/candidate-subject.v25.json']
for rel in EXTRA:
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        print('absent from subject:', rel)
        continue
    h = hashlib.sha256(open(s, 'rb').read()).hexdigest()
    assert man[rel]['sha256'] == h, rel
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if not os.path.isfile(d):
        shutil.copy2(s, d)

jobs = [
    ('check_repository_file_inventory.py', ['--check']),
    ('check_implementation_planning.py', ['--source', SRC, '--check']),
    ('check_implementation_planning.py', ['--source', KIT, '--check']),
]
for name, args in jobs:
    p = os.path.join(KIT, 'docs/operations', name)
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                       cwd=KIT, timeout=1800)
    print('=== %s %s -> rc=%d' % (name, ' '.join(a if not a.startswith('/') else '<path>' for a in args), r.returncode))
    print((r.stdout or '')[-1400:])
    if r.returncode != 0:
        print('--- stderr ---')
        print((r.stderr or '')[-1600:])

# confirm the FROZEN snapshot is still byte-identical
bad = 0
for rel in ('docs/v2/architecture/14-repository-and-module-layout.md',
            'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
            'docs/v2/architecture/repository-file-inventory.v1.json',
            'docs/v2/architecture/implementation-coverage.v1.json'):
    h = hashlib.sha256(open(os.path.join(SRC, rel), 'rb').read()).hexdigest()
    if h != man[rel]['sha256']:
        bad += 1
        print('FROZEN MUTATED:', rel)
print('frozen planning documents unchanged:', bad == 0)
