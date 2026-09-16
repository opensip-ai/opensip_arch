"""Q07 — justified suite and planning runs on source34. Every job is tied to a file in my derived
33->34 delta or to a direct consumer of one. Checkers that write reports run in a disposable,
hash-verified copy; the pinned evaluator3 launcher runs against the frozen snapshot with output
directed into this runtime (it reads, it does not write source). Frozen drift is measured after."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v34'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit34')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {'interpreter': PY + ' -I -B', 'startedUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or rel.startswith('docs/coop/design-corrections/reviews/'):
        continue
    s = os.path.join(SRC, rel)
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    verified += sha(d) == man[rel]['sha256']
for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md', 'workflows-author-feedback.v1.md'):
    rel = 'docs/coop/design-corrections/reviews/' + n
    if rel in man:
        d = os.path.join(KIT, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(SRC, rel), d)
        copied += 1
        verified += sha(d) == man[rel]['sha256']
R['disposableCopied'], R['disposableVerified'] = copied, verified
print('disposable kit34: %d files, %d byte-equal to frozen34' % (copied, verified), flush=True)
assert copied == verified
DC = os.path.join(KIT, 'docs/coop/design-corrections')
SDC = os.path.join(SRC, 'docs/coop/design-corrections')
JOBS = [
    ('check-atoms', os.path.join(DC, 'foundation/check-atoms.v1.py'), [], DC + '/foundation',
     'own bytes changed +19049; owns the controls for the changed atom law (atom_model +1925, contract +13125)', 1800),
    ('evaluator3-launcher', os.path.join(SDC, 'foundation/run-evaluator3-checks.py'),
     ['--out', os.path.join(OUT, 'evaluator3-launcher34')], SDC + '/foundation',
     'evaluator3-source-pins.v1.json re-digested for the three atom owners; its atoms and full-replay children consume atom_model.v1.py', 9900),
    ('foundation-reference', os.path.join(DC, 'foundation/run-reference-checks.py'),
     ['--report', os.path.join(OUT, 'foundation34.json'), '--report-dir', os.path.join(OUT, 'foundation34')],
     DC + '/foundation', 'foundation/source-pins.v1.json re-digested', 3600),
    ('integration', os.path.join(DC, 'check-integration.py'), ['--report', os.path.join(OUT, 'integration34.json')],
     DC, 'all five pin ledgers re-digested; integration cross-checks the ledgers', 900),
    ('native', os.path.join(DC, 'native/check_native_evidence.v2.py'), [], DC + '/native',
     'native/source-pins.v2.json re-digested; native sufficiency_v2 is the owner atom_model calls', 900),
    ('security', os.path.join(DC, 'security/check-security-lifecycle.v1.py'),
     ['--report', os.path.join(OUT, 'security34.json')], DC + '/security', 'security/source-pins.v1.json re-digested', 900),
    ('workflows-reference', os.path.join(DC, 'workflows/run-reference-checks.py'),
     ['--report', os.path.join(OUT, 'workflows34.json')], DC + '/workflows',
     'workflows/source-pins.v1.json and workflows-report.v1.json re-digested; workflows/query models import atom_model', 900),
]
rows = []
for name, p, args, cwd, why, tmo in JOBS:
    t0 = time.time()
    cmd = [PY, '-I', '-B', p] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=tmo)
        rc, so, se, to = r.returncode, r.stdout or '', r.stderr or '', False
    except subprocess.TimeoutExpired as e:
        rc, so, se, to = None, (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), '', True
    open(os.path.join(OUT, 'suite34-%s.stdout' % name), 'w').write(so)
    open(os.path.join(OUT, 'suite34-%s.stderr' % name), 'w').write(se)
    tail = so.strip().splitlines()[-1:] or ['']
    row = {'name': name, 'command': cmd, 'cwd': cwd, 'checkerSha256': sha(p),
           'checkerEqualsFrozen34': sha(p) == man[os.path.relpath(p, KIT if p.startswith(KIT) else SRC)]['sha256'],
           'justification': why, 'returncode': rc, 'timedOut': to, 'seconds': round(time.time() - t0, 1),
           'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(), 'lastLine': tail[0][-240:],
           'stderrTail': se[-700:] if rc else ''}
    rows.append(row)
    print('%-22s rc=%-4s %7.1fs  %s' % (name, rc, row['seconds'], tail[0][-120:]), flush=True)
    if rc:
        print('   STDERR:', se[-900:], flush=True)
R['jobs'] = rows

lr = os.path.join(OUT, 'evaluator3-launcher34', 'report.json')
if os.path.isfile(lr):
    d = json.load(open(lr))
    R['launcherReport'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'),
                           'changedOrMissing': d.get('changedOrMissing', []),
                           'children': [{'name': c.get('name'), 'exitCode': c.get('exitCode')} for c in d.get('checks', [])]}
    print('launcher: sourcePinsValid=%s passed=%s children=%d nonzero=%s' % (
        d.get('sourcePinsValid'), d.get('passed'), len(d.get('checks', [])),
        [c.get('name') for c in d.get('checks', []) if c.get('exitCode') != 0]), flush=True)

plan_rows = []
for name, args in (('check_repository_file_inventory.py', ['--check']),
                   ('check_implementation_planning.py', ['--source', SRC, '--check'])):
    p = os.path.join(KIT, 'docs/operations', name)
    t0 = time.time()
    rr = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True, cwd=KIT, timeout=3600)
    tail = (rr.stdout or '').strip().splitlines()[-1:] or ['']
    plan_rows.append({'checker': name, 'command': [PY, '-I', '-B', p] + args, 'checkerSha256': sha(p),
                      'returncode': rr.returncode, 'seconds': round(time.time() - t0, 1),
                      'lastLine': tail[0][-240:], 'stderrTail': (rr.stderr or '')[-500:] if rr.returncode else ''})
    print('%-40s rc=%-3d %s' % (name, rr.returncode, tail[0][-120:]), flush=True)
R['planningGroups'] = plan_rows

kit_changed = []
for rel, f in man.items():
    k = os.path.join(KIT, rel)
    if os.path.isfile(k) and sha(k) != f['sha256']:
        kit_changed.append(rel)
R['disposableFilesRewrittenByCheckers'] = kit_changed
wr = 'docs/coop/design-corrections/workflows/workflows-report.v1.json'
R['regeneratedWorkflowsReportEqualsFrozen34'] = sha(os.path.join(KIT, wr)) == man[wr]['sha256']
dev = sum(1 for rel, f in man.items()
          if not os.path.isfile(os.path.join(SRC, rel)) or sha(os.path.join(SRC, rel)) != f['sha256'])
R['frozen34DeviationsAfterRuns'] = dev
R['allJobsExitZero'] = all(x['returncode'] == 0 for x in rows) and all(x['returncode'] == 0 for x in plan_rows)
print('\ndisposable files rewritten by checkers:', kit_changed, flush=True)
print('regenerated workflows-report equals frozen34 bytes:', R['regeneratedWorkflowsReportEqualsFrozen34'])
print('frozen34 deviations after all runs:', dev)
print('all jobs exit 0:', R['allJobsExitZero'])
json.dump(R, open(os.path.join(OUT, 'q07-suites.json'), 'w'), indent=1, default=str)
print('wrote q07-suites.json')
