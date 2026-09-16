"""P06 — run the checkers whose inputs changed 31->32, in a disposable exact verified copy.

Justification for running each: its own bytes changed, or a changed owner is in its input set.
Report writers run only in the disposable copy; the frozen snapshot is re-measured afterwards.
"""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit32')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or rel.startswith('docs/coop/design-corrections/reviews/'):
        continue
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
        verified += 1
for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md',
          'workflows-author-feedback.v1.md'):
    rel = 'docs/coop/design-corrections/reviews/' + n
    if rel in man:
        d = os.path.join(KIT, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(SRC, rel), d)
        copied += 1
        if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
            verified += 1
R['disposableCopied'], R['disposableVerified'] = copied, verified
print('disposable copy: %d files, %d byte-equal to frozen32' % (copied, verified))
assert copied == verified

DC = os.path.join(KIT, 'docs/coop/design-corrections')
JOBS = [
    ('workflows/check-workflow-projection.v3.py', [], 'own bytes changed (+45001) and it hosts the new repair controls'),
    ('foundation/check-atoms.v1.py', [], 'own bytes changed; carries the 30 glob vectors'),
    ('foundation/check-replay.v3.py', [], 'evaluator_graph_fixture.v3.py changed (default-off extension)'),
    ('workflows/check_workflows.v1.py', ['--report', OUT + '/workflows32.json'], 'workflows_model.v1/v3 and both repair schemas changed'),
    ('foundation/check-enumeration.v1.py', ['--stdout', '--receipt', OUT + '/enum32.receipt.json',
                                            '--hashes', OUT + '/enum32.hashes.json'],
     'enumeration owner is the new ownership source for the repair law'),
    ('check-integration.py', ['--report', OUT + '/integration32.json'], 'cross-owner links and chapter changes'),
]
rows = []
for rel, args, why in JOBS:
    p = os.path.join(DC, rel)
    if not os.path.isfile(p):
        rows.append({'checker': rel, 'error': 'not found'})
        print('MISSING', rel)
        continue
    t0 = time.time()
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                       cwd=os.path.dirname(p), timeout=5400)
    tail = (r.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': rel, 'justification': why, 'returncode': r.returncode,
                 'seconds': round(time.time() - t0, 1), 'lastLine': tail[0][-220:],
                 'stderrTail': (r.stderr or '')[-500:] if r.returncode else ''})
    print('%-44s rc=%-3d %6.1fs  %s' % (rel.split('/')[-1], r.returncode, time.time() - t0,
                                        tail[0][-110:]))
    if r.returncode:
        print('   STDERR:', (r.stderr or '')[-700:])
R['jobs'] = rows
R['allExitZero'] = all(x.get('returncode') == 0 for x in rows)
print('\nall changed-input checkers exit 0:', R['allExitZero'])

dev = 0
for rel, f in man.items():
    q = os.path.join(SRC, rel)
    if not os.path.isfile(q) or os.path.getsize(q) != f['bytes'] or \
       hashlib.sha256(open(q, 'rb').read()).hexdigest() != f['sha256']:
        dev += 1
R['frozenDeviationsAfterRuns'] = dev
print('frozen32 deviations after runs:', dev)
json.dump(R, open(os.path.join(OUT, 'p06-changedchecks.json'), 'w'), indent=1, default=str)
print('wrote p06-changedchecks.json')
