"""P03 — run the suites whose inputs changed 32->33, in a disposable exact verified copy.
Each run is justified by a changed input; unchanged passing suites are not repeated."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit33')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
delta = json.load(open(os.path.join(OUT, 'p01-delta.json')))
CH = {c['path'] for c in delta['changed']} | {a['path'] for a in delta['added']}
R = {'changedPaths': sorted(CH)}

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
print('disposable copy: %d files, %d byte-equal to frozen33' % (copied, verified))
assert copied == verified

DC = os.path.join(KIT, 'docs/coop/design-corrections')
JOBS = [
    ('foundation/check-execution-inputs.v1.py', [], 'own bytes changed +40923; owns the new execution law controls'),
    ('foundation/check-replay.v3.py', [], 'evaluator_graph_fixture.v3.py changed +9123'),
    ('foundation/check-enumeration.v1.py', ['--stdout', '--receipt', OUT + '/enum33.receipt.json',
                                            '--hashes', OUT + '/enum33.hashes.json'],
     'enumeration-contract.v1.md changed +1844'),
    ('foundation/check-identity.py', ['--report', OUT + '/identity33.json'],
     'evaluator-composition-contract.v3.md changed +2442'),
    ('native/check_native_evidence.v2.py', [], 'native-evidence.md changed +1175'),
    ('check-integration.py', ['--report', OUT + '/integration33.json'], 'cross-owner links changed'),
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
                       cwd=os.path.dirname(p), timeout=7200)
    tail = (r.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': rel, 'justification': why, 'returncode': r.returncode,
                 'seconds': round(time.time() - t0, 1), 'lastLine': tail[0][-240:],
                 'stderrTail': (r.stderr or '')[-600:] if r.returncode else ''})
    print('%-46s rc=%-3d %7.1fs  %s' % (rel.split('/')[-1], r.returncode, time.time() - t0,
                                        tail[0][-110:]))
    if r.returncode:
        print('   STDERR:', (r.stderr or '')[-800:])
R['jobs'] = rows
R['allExitZero'] = all(x.get('returncode') == 0 for x in rows)
print('\nall changed-input suites exit 0:', R['allExitZero'])

dev = sum(1 for rel, f in man.items()
          if not os.path.isfile(os.path.join(SRC, rel))
          or hashlib.sha256(open(os.path.join(SRC, rel), 'rb').read()).hexdigest() != f['sha256'])
R['frozenDeviationsAfterRuns'] = dev
print('frozen33 deviations after runs:', dev)
json.dump(R, open(os.path.join(OUT, 'p03-suites.json'), 'w'), indent=1, default=str)
print('wrote p03-suites.json')
