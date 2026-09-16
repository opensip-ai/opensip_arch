"""R04 — justified suite and planning runs on source35 (same method as source34 q07). Report-writing
checkers run in a disposable hash-verified copy; the pinned launcher reads frozen35 directly with output
directed into this runtime. Frozen drift measured after."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v35'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit35')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {'interpreter': PY + ' -I -B'}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or (rel.startswith('docs/coop/design-corrections/reviews/') and not any(
            rel.endswith(n) for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md', 'workflows-author-feedback.v1.md'))):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(os.path.join(SRC, rel), d)
    copied += 1
    verified += sha(d) == man[rel]['sha256']
R['disposableCopied'], R['disposableVerified'] = copied, verified
print('disposable kit35: %d files, %d byte-equal to frozen35' % (copied, verified), flush=True)
assert copied == verified
DC = os.path.join(KIT, 'docs/coop/design-corrections')
SDC = os.path.join(SRC, 'docs/coop/design-corrections')
JOBS = [
    ('check-atoms', os.path.join(DC, 'foundation/check-atoms.v1.py'), [], DC + '/foundation',
     'own bytes changed; owns I1 and carrier controls; atom_model and incoming-search schema changed', 1800),
    ('evaluator3-launcher', os.path.join(SDC, 'foundation/run-evaluator3-checks.py'), ['--out', os.path.join(OUT, 'evaluator3-launcher35')],
     SDC + '/foundation', 'evaluator3 pin ledger re-digested for four owners; atoms, replay and composition children consume atom_model', 9900),
    ('foundation-reference', os.path.join(DC, 'foundation/run-reference-checks.py'),
     ['--report', os.path.join(OUT, 'foundation35.json'), '--report-dir', os.path.join(OUT, 'foundation35')], DC + '/foundation',
     'foundation pins re-digested; incoming-search.schema owner changed', 3600),
    ('integration', os.path.join(DC, 'check-integration.py'), ['--report', os.path.join(OUT, 'integration35.json')], DC,
     'all five pin ledgers re-digested', 900),
    ('native', os.path.join(DC, 'native/check_native_evidence.v2.py'), [], DC + '/native',
     'native pins re-digested; the native subject-scope carrier is now reached for absent keys', 900),
    ('security', os.path.join(DC, 'security/check-security-lifecycle.v1.py'), ['--report', os.path.join(OUT, 'security35.json')],
     DC + '/security', 'security pins re-digested', 900),
    ('workflows-reference', os.path.join(DC, 'workflows/run-reference-checks.py'), ['--report', os.path.join(OUT, 'workflows35.json')],
     DC + '/workflows', 'workflows pins and workflows-report re-digested; workflows/query models import atom_model', 900),
]
rows = []
for name, p, args, cwd, why, tmo in JOBS:
    t0 = time.time()
    cmd = [PY, '-I', '-B', p] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=tmo)
        rc, so, se, to = r.returncode, r.stdout or '', r.stderr or '', False
    except subprocess.TimeoutExpired as e:
        rc, so, se, to = None, '', '', True
    open(os.path.join(OUT, 'suite35-%s.stdout' % name), 'w').write(so)
    open(os.path.join(OUT, 'suite35-%s.stderr' % name), 'w').write(se)
    tail = so.strip().splitlines()[-1:] or ['']
    rel = os.path.relpath(p, KIT if p.startswith(KIT) else SRC)
    rows.append({'name': name, 'command': cmd, 'cwd': cwd, 'checkerSha256': sha(p), 'checkerEqualsFrozen35': sha(p) == man[rel]['sha256'],
                 'justification': why, 'returncode': rc, 'timedOut': to, 'seconds': round(time.time() - t0, 1),
                 'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(), 'lastLine': tail[0][-240:], 'stderrTail': se[-700:] if rc else ''})
    print('%-22s rc=%-4s %7.1fs  %s' % (name, rc, rows[-1]['seconds'], tail[0][-120:]), flush=True)
R['jobs'] = rows
lr = os.path.join(OUT, 'evaluator3-launcher35', 'report.json')
if os.path.isfile(lr):
    d = json.load(open(lr))
    R['launcherReport'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'),
                           'changedOrMissing': d.get('changedOrMissing', []),
                           'children': [{'name': c.get('name'), 'exitCode': c.get('exitCode')} for c in d.get('checks', [])]}
    print('launcher pinsValid=%s passed=%s children=%d nonzero=%s' % (d.get('sourcePinsValid'), d.get('passed'), len(d.get('checks', [])),
                                                                     [c.get('name') for c in d.get('checks', []) if c.get('exitCode') != 0]), flush=True)
plan_rows = []
for name, args in (('check_repository_file_inventory.py', ['--check']), ('check_implementation_planning.py', ['--source', SRC, '--check'])):
    p = os.path.join(KIT, 'docs/operations', name)
    rr = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True, cwd=KIT, timeout=3600)
    tail = (rr.stdout or '').strip().splitlines()[-1:] or ['']
    plan_rows.append({'checker': name, 'command': [PY, '-I', '-B', p] + args, 'checkerSha256': sha(p), 'returncode': rr.returncode,
                      'lastLine': tail[0][-240:], 'stderrTail': (rr.stderr or '')[-500:] if rr.returncode else ''})
    print('%-40s rc=%-3d %s' % (name, rr.returncode, tail[0][-120:]), flush=True)
R['planningGroups'] = plan_rows
R['disposableFilesRewrittenByCheckers'] = [rel for rel, f in man.items() if os.path.isfile(os.path.join(KIT, rel)) and sha(os.path.join(KIT, rel)) != f['sha256']]
wr = 'docs/coop/design-corrections/workflows/workflows-report.v1.json'
R['regeneratedWorkflowsReportEqualsFrozen35'] = sha(os.path.join(KIT, wr)) == man[wr]['sha256']
R['frozen35DeviationsAfterRuns'] = sum(1 for rel, f in man.items() if sha(os.path.join(SRC, rel)) != f['sha256'])
R['allJobsExitZero'] = all(x['returncode'] == 0 for x in rows + plan_rows)
ca = os.path.join(OUT, 'suite35-check-atoms.stdout')
try:
    j = json.load(open(ca))
    R['checkAtoms'] = {k: j.get(k) for k in ('standing', 'ok', 'passed', 'failed')}
except Exception as ex:  # noqa: BLE001
    R['checkAtoms'] = {'parseError': str(ex)}
print('\ncheck-atoms:', R['checkAtoms'], '| rewritten:', R['disposableFilesRewrittenByCheckers'],
      '| report equal:', R['regeneratedWorkflowsReportEqualsFrozen35'], '| frozen35 drift:', R['frozen35DeviationsAfterRuns'],
      '| all exit 0:', R['allJobsExitZero'])
json.dump(R, open(os.path.join(OUT, 'r04-suites.json'), 'w'), indent=1, default=str)
print('wrote r04-suites.json')
