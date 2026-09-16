"""W04: G3 - the freeze current-tool receipt guard.

BOUNDED SCOPE: the full application root is absent, so this builds a minimal synthetic
stage/root that satisfies freeze's earlier preconditions and then exercises the NEW block
(freeze-application.py:44-57). This is a guard-level execution, NOT an end-to-end freeze of
a real application package, and is reported as such.

On every refusal we assert that NO freeze output exists: no before/ image tree, no stage
manifest, no retained manifest, no source archive.
"""
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
REF = '/tmp/opensip-architecture-review-env/bin/python'
FREEZE = INPUTS / 'freeze-application.py'
DC = 'docs/coop/design-corrections/'
VER = 't1'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows = []


def wj(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + '\n')
    return p


def build(base, mutate=None):
    base = Path(base)
    root, stage = base / 'root', base / 'stage'
    files, support = stage / 'files', stage / 'support'
    (root / DC / 'reviews').mkdir(parents=True)

    # Prerequisite reviews in the live root.
    dr = wj(root / DC / 'reviews/design.json',
            {'verdict': 'ACCEPT', 'newMustIssues': [], 'newShouldIssues': []})
    br = wj(root / DC / 'reviews/blind.json',
            {'verdict': 'ACCEPT-RECONSTRUCTABLE', 'newMustIssues': [], 'newShouldIssues': []})

    # Staged documentation content (kept tiny).
    (files / 'docs').mkdir(parents=True)
    (files / 'docs/x.md').write_text('synthetic staged doc\n')
    fin = files / DC / 'finalize-application.v1.py'
    fin.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(INPUTS / 'finalize-application.v1.py', fin)
    wj(files / DC / 'application.v1.json', {
        'implementationAuthorized': False, 'qualificationClaimed': False,
        'applicationSubject': {'path': DC + 'reviews/application-subject.' + VER + '.json'},
        'designSubject': {'path': DC + 'reviews/design-subject.json', 'sha256': 'a' * 64},
        'independentDesignReview': {'path': DC + 'reviews/design.json', 'sha256': sha(dr)},
        'freshBlindConsumerReview': {'path': DC + 'reviews/blind.json', 'sha256': sha(br)},
    })

    # Support prerequisites that precede the new block.
    support.mkdir(parents=True, exist_ok=True)
    wj(support / 'staged-reference-checks.v1.json',
       {'commands': [{'name': f'c{i}', 'exitCode': 0} for i in range(7)]})
    wj(support / 'native-recording-delta.v1.json', {'ok': True})
    wj(support / 'application-link-assessment.v1.json', {'unexplainedFailures': [], 'paths': []})
    wj(support / 'finalizer-selftest.v1.json',
       {'failed': [], 'actualApplicationPerformed': False, 'sourceSha256': sha(fin)})

    # The two current-tool sources and their two executed reports.
    for name in ('check-review-envelope.v2.py', 'check-retain-public.v1.py'):
        shutil.copyfile(INPUTS / name, support / name)
    rep_env = wj(support / 'current-current-envelope.json',
                 {'passed': 35, 'failed': [], 'actualApplicationPerformed': False})
    rep_ret = wj(support / 'current-check-retain-public.v2.report.json',
                 {'passed': 69, 'failed': [], 'actualApplicationPerformed': False})
    receipt = {
        'standing': 'Executed current synthetic tooling checks.',
        'sourceFiles': [
            {'path': n, 'sha256': sha(support / n), 'bytes': (support / n).stat().st_size}
            for n in ('check-review-envelope.v2.py', 'check-retain-public.v1.py')],
        'runs': [
            {'command': [REF, '-I', '-B', 'tool-validation/check-review-envelope.v2.py',
                         '--report', 'x'], 'exitCode': 0,
             'report': 'current-current-envelope.json', 'reportSha256': sha(rep_env)},
            {'command': [REF, '-I', '-B', 'tool-validation/check-retain-public.v1.py',
                         '--report', 'x', '--envelope-report', 'y'], 'exitCode': 0,
             'report': 'current-check-retain-public.v2.report.json', 'reportSha256': sha(rep_ret)},
        ],
        'actualApplicationPerformed': False,
    }
    if mutate:
        mutate(receipt, support)
    wj(support / 'current-application-tool-checks.v1.json', receipt)
    return root, stage


def outputs_present(root, stage):
    return {
        'beforeTree': (stage / 'before').exists(),
        'stageManifest': (stage / ('application-subject.' + VER + '.json')).exists(),
        'retainedManifest': (root / DC / 'reviews' / ('application-subject.' + VER + '.json')).exists(),
        'sourceArchive': (root / DC / 'reviews' / ('application-source.' + VER + '.tar.gz')).exists(),
    }


def case(ident, expect, mutate=None):
    with tempfile.TemporaryDirectory(prefix='opensip-g3-') as td:
        root, stage = build(td, mutate)
        r = subprocess.run([REF, '-I', '-B', str(FREEZE), '--root', str(root),
                            '--stage', str(stage), '--version', VER],
                           capture_output=True, text=True, cwd=td)
        outs = outputs_present(root, stage)
        ok = r.returncode == 0
        any_out = any(outs.values())
        rows.append({
            'id': ident, 'expected': expect, 'observed': 'FROZE' if ok else 'REFUSED',
            'asExpected': ok is (expect == 'FROZE'),
            'freezeOutputs': outs,
            'noOutputOnRefusal': (not ok and not any_out) or ok,
            'detail': (r.stderr.strip().splitlines() or [''])[-1][:150]})


# ---- positive control ----
case('positive-valid-receipt-freezes', 'FROZE')

# ---- missing ----
def drop_receipt(rec, support):
    rec['__drop__'] = True
with tempfile.TemporaryDirectory(prefix='opensip-g3-missing-') as td:
    root, stage = build(td)
    (stage / 'support/current-application-tool-checks.v1.json').unlink()
    r = subprocess.run([REF, '-I', '-B', str(FREEZE), '--root', str(root),
                        '--stage', str(stage), '--version', VER],
                       capture_output=True, text=True, cwd=td)
    outs = outputs_present(root, stage)
    rows.append({'id': 'missing-current-tool-receipt-refuses', 'expected': 'REFUSED',
                 'observed': 'FROZE' if r.returncode == 0 else 'REFUSED',
                 'asExpected': r.returncode != 0, 'freezeOutputs': outs,
                 'noOutputOnRefusal': not any(outs.values()),
                 'detail': (r.stderr.strip().splitlines() or [''])[-1][:150]})

# ---- shape / count / naming ----
case('one-run-only-refuses', 'REFUSED',
     lambda rec, s: rec.__setitem__('runs', rec['runs'][:1]))
case('three-runs-refuses', 'REFUSED',
     lambda rec, s: rec.__setitem__('runs', rec['runs'] + [copy.deepcopy(rec['runs'][0])]))
case('wrong-suite-name-refuses', 'REFUSED',
     lambda rec, s: rec['runs'][1]['command'].__setitem__(3, 'tool-validation/some-other-suite.py'))
case('both-runs-same-suite-refuses', 'REFUSED',
     lambda rec, s: rec['runs'][1]['command'].__setitem__(
         3, 'tool-validation/check-review-envelope.v2.py'))
case('duplicate-sourceFiles-path-refuses', 'REFUSED',
     lambda rec, s: rec.__setitem__(
         'sourceFiles', rec['sourceFiles'] + [dict(rec['sourceFiles'][0])]))
case('receipt-claims-application-performed-refuses', 'REFUSED',
     lambda rec, s: rec.__setitem__('actualApplicationPerformed', True))

# ---- drift ----
case('sourceFile-sha-drift-refuses', 'REFUSED',
     lambda rec, s: rec['sourceFiles'][0].__setitem__('sha256', 'f' * 64))
case('sourceFile-bytes-drift-refuses', 'REFUSED',
     lambda rec, s: rec['sourceFiles'][0].__setitem__('bytes', 1))
case('sourceFile-content-drift-on-disk-refuses', 'REFUSED',
     lambda rec, s: (s / 'check-review-envelope.v2.py').write_text('# tampered\n'))
case('missing-sourceFile-refuses', 'REFUSED',
     lambda rec, s: (s / 'check-retain-public.v1.py').unlink())
case('report-sha-drift-refuses', 'REFUSED',
     lambda rec, s: rec['runs'][0].__setitem__('reportSha256', 'f' * 64))
case('report-content-drift-on-disk-refuses', 'REFUSED',
     lambda rec, s: (s / 'current-current-envelope.json').write_text('{"failed":[]}\n'))
case('missing-report-refuses', 'REFUSED',
     lambda rec, s: (s / 'current-check-retain-public.v2.report.json').unlink())

# ---- substantive failure content ----
case('nonzero-exitCode-refuses', 'REFUSED',
     lambda rec, s: rec['runs'][0].__setitem__('exitCode', 1))
case('report-with-failures-refuses', 'REFUSED', lambda rec, s: None)  # replaced below
rows.pop()
with tempfile.TemporaryDirectory(prefix='opensip-g3-fail-') as td:
    root, stage = build(td)
    p = stage / 'support/current-current-envelope.json'
    p.write_text(json.dumps({'passed': 34, 'failed': ['some-control'],
                             'actualApplicationPerformed': False}, indent=2) + '\n')
    rec = json.loads((stage / 'support/current-application-tool-checks.v1.json').read_text())
    rec['runs'][0]['reportSha256'] = sha(p)
    wj(stage / 'support/current-application-tool-checks.v1.json', rec)
    r = subprocess.run([REF, '-I', '-B', str(FREEZE), '--root', str(root),
                        '--stage', str(stage), '--version', VER],
                       capture_output=True, text=True, cwd=td)
    outs = outputs_present(root, stage)
    rows.append({'id': 'report-with-failures-refuses-even-when-hash-matches',
                 'expected': 'REFUSED',
                 'observed': 'FROZE' if r.returncode == 0 else 'REFUSED',
                 'asExpected': r.returncode != 0, 'freezeOutputs': outs,
                 'noOutputOnRefusal': not any(outs.values()),
                 'detail': (r.stderr.strip().splitlines() or [''])[-1][:150]})
with tempfile.TemporaryDirectory(prefix='opensip-g3-app-') as td:
    root, stage = build(td)
    p = stage / 'support/current-check-retain-public.v2.report.json'
    p.write_text(json.dumps({'passed': 69, 'failed': [],
                             'actualApplicationPerformed': True}, indent=2) + '\n')
    rec = json.loads((stage / 'support/current-application-tool-checks.v1.json').read_text())
    rec['runs'][1]['reportSha256'] = sha(p)
    wj(stage / 'support/current-application-tool-checks.v1.json', rec)
    r = subprocess.run([REF, '-I', '-B', str(FREEZE), '--root', str(root),
                        '--stage', str(stage), '--version', VER],
                       capture_output=True, text=True, cwd=td)
    outs = outputs_present(root, stage)
    rows.append({'id': 'report-claiming-application-performed-refuses',
                 'expected': 'REFUSED',
                 'observed': 'FROZE' if r.returncode == 0 else 'REFUSED',
                 'asExpected': r.returncode != 0, 'freezeOutputs': outs,
                 'noOutputOnRefusal': not any(outs.values()),
                 'detail': (r.stderr.strip().splitlines() or [''])[-1][:150]})

# ---- path safety ----
case('sourceFiles-path-traversal-refuses', 'REFUSED',
     lambda rec, s: rec['sourceFiles'][0].__setitem__('path', '../files/docs/x.md'))
case('report-path-traversal-refuses', 'REFUSED',
     lambda rec, s: rec['runs'][0].__setitem__('report', '../../escape.json'))

bad = [r['id'] for r in rows if not r['asExpected']]
leaked = [r['id'] for r in rows if not r['noOutputOnRefusal']]
(HERE / 'w04_g3_freeze.result.json').write_text(json.dumps(rows, indent=2) + '\n')
print('G3 freeze guard:', len(rows), 'cases,', len(rows) - len(bad), 'as expected')
print('unexpected:', bad)
print('cases that produced freeze output despite refusing:', leaked)
for r in rows:
    print(('ok  ' if r['asExpected'] else 'DIFF'), '%-52s' % r['id'], r['observed'], '|', r['detail'])
