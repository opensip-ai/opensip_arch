"""R04 — justified suite and planning runs on FROZEN source36 (same method as my source35 r04). Root's reference
execution ran on the mutable successor tree; this runs the frozen bytes. Report-writing checkers run in a disposable
hash-verified copy; the pinned launcher reads frozen36 directly with output directed into this runtime.
Frozen36 drift is measured after. Nothing here is acceptance of root's receipts."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit36')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v36.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {'interpreter': PY + ' -I -B'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


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
print('disposable kit36: %d files, %d byte-equal to frozen36' % (copied, verified), flush=True)
assert copied == verified
DC = os.path.join(KIT, 'docs/coop/design-corrections')
SDC = os.path.join(SRC, 'docs/coop/design-corrections')
JOBS = [
    ('check-atoms', os.path.join(DC, 'foundation/check-atoms.v1.py'), [], DC + '/foundation',
     'own bytes changed (+6 totality controls, one docstring); owns the changed atom law; atom_model, contract and registry changed', 1800),
    ('evaluator3-launcher', os.path.join(SDC, 'foundation/run-evaluator3-checks.py'), ['--out', os.path.join(OUT, 'evaluator3-launcher36')],
     SDC + '/foundation', 'evaluator3 pin ledger re-digested; atoms, replay, execution-inputs, composition and projection children consume atom_model/registry', 9900),
    ('foundation-reference', os.path.join(DC, 'foundation/run-reference-checks.py'),
     ['--report', os.path.join(OUT, 'foundation36.json'), '--report-dir', os.path.join(OUT, 'foundation36')], DC + '/foundation',
     'foundation pins re-digested; evaluator-projection-registry owner changed', 3600),
    ('integration', os.path.join(DC, 'check-integration.py'), ['--report', os.path.join(OUT, 'integration36.json')], DC,
     'all five pin ledgers re-digested', 900),
    ('native', os.path.join(DC, 'native/check_native_evidence.v2.py'), [], DC + '/native',
     'native pins re-digested; atom totality reads native sufficiency_v2 and DEPENDS_ON', 900),
    ('security', os.path.join(DC, 'security/check-security-lifecycle.v1.py'), ['--report', os.path.join(OUT, 'security36.json')],
     DC + '/security', 'security pins re-digested', 900),
    ('workflows-reference', os.path.join(DC, 'workflows/run-reference-checks.py'), ['--report', os.path.join(OUT, 'workflows36.json')],
     DC + '/workflows', 'workflows pins and workflows-report re-digested; workflows/query models import atom_model', 900),
]
rows = []
for name, p, args, cwd, why, tmo in JOBS:
    t0 = time.time()
    cmd = [PY, '-I', '-B', p] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=tmo)
        rc, so, se, to = r.returncode, r.stdout or '', r.stderr or '', False
    except subprocess.TimeoutExpired:
        rc, so, se, to = None, '', '', True
    open(os.path.join(OUT, 'suite36-%s.stdout' % name), 'w').write(so)
    open(os.path.join(OUT, 'suite36-%s.stderr' % name), 'w').write(se)
    tail = so.strip().splitlines()[-1:] or ['']
    rel = os.path.relpath(p, KIT if p.startswith(KIT) else SRC)
    rows.append({'name': name, 'command': cmd, 'cwd': cwd, 'checkerSha256': sha(p), 'checkerEqualsFrozen36': sha(p) == man[rel]['sha256'],
                 'justification': why, 'returncode': rc, 'timedOut': to, 'seconds': round(time.time() - t0, 1),
                 'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(se.encode()).hexdigest(),
                 'lastLine': tail[0][-240:], 'stderrTail': se[-700:] if rc else ''})
    print('%-22s rc=%-4s %7.1fs  %s' % (name, rc, rows[-1]['seconds'], tail[0][-120:]), flush=True)
R['jobs'] = rows
lr = os.path.join(OUT, 'evaluator3-launcher36', 'report.json')
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
    open(os.path.join(OUT, 'planning36-%s.stdout' % name), 'w').write(rr.stdout or '')
    open(os.path.join(OUT, 'planning36-%s.stderr' % name), 'w').write(rr.stderr or '')
    tail = (rr.stdout or '').strip().splitlines()[-1:] or ['']
    plan_rows.append({'checker': name, 'command': [PY, '-I', '-B', p] + args, 'checkerSha256': sha(p), 'returncode': rr.returncode,
                      'stdoutSha256': hashlib.sha256((rr.stdout or '').encode()).hexdigest(),
                      'lastLine': tail[0][-240:], 'stderrTail': (rr.stderr or '')[-500:] if rr.returncode else ''})
    print('%-40s rc=%-3d %s' % (name, rr.returncode, tail[0][-120:]), flush=True)
R['planningGroups'] = plan_rows
R['disposableFilesRewrittenByCheckers'] = [rel for rel, f in man.items() if os.path.isfile(os.path.join(KIT, rel)) and sha(os.path.join(KIT, rel)) != f['sha256']]
wr = 'docs/coop/design-corrections/workflows/workflows-report.v1.json'
R['regeneratedWorkflowsReportEqualsFrozen36'] = sha(os.path.join(KIT, wr)) == man[wr]['sha256']
R['frozen36DeviationsAfterRuns'] = sum(1 for rel, f in man.items() if sha(os.path.join(SRC, rel)) != f['sha256'])
R['allJobsExitZero'] = all(x['returncode'] == 0 for x in rows + plan_rows)
ca = os.path.join(OUT, 'suite36-check-atoms.stdout')
try:
    j = json.load(open(ca))
    R['checkAtoms'] = {k: j.get(k) for k in ('standing', 'ok', 'passed', 'failed')}
except Exception as ex:  # noqa: BLE001
    R['checkAtoms'] = {'parseError': str(ex), 'tail': open(ca).read()[-400:]}
print('\ncheck-atoms:', R['checkAtoms'], '| rewritten:', R['disposableFilesRewrittenByCheckers'],
      '| report equal:', R['regeneratedWorkflowsReportEqualsFrozen36'], '| frozen36 drift:', R['frozen36DeviationsAfterRuns'],
      '| all exit 0:', R['allJobsExitZero'])
json.dump(R, open(os.path.join(OUT, 'r04-suites.json'), 'w'), indent=1, default=str)
print('wrote r04-suites.json')
