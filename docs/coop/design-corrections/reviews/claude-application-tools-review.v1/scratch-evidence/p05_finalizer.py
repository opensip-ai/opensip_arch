"""P05: re-execute shipped disposable suites against the frozen inputs, plus extra
before-image / activation-ordering cases the shipped selftest does not cover.

Nothing is written outside scratch and per-case temporary directories.
All ACCEPT strings here are SYNTHETIC and are not project review evidence.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
REF = '/tmp/opensip-architecture-review-env/bin/python'
FINALIZER = INPUTS / 'finalize-application.v1.py'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
out = {}

# ---- A: shipped finalizer selftest, unmodified source, report into scratch ----
rep = HERE / 'finalizer-selftest.rerun.json'
r = subprocess.run([REF, '-I', '-B', str(INPUTS / 'check-finalizer.py'),
                    '--source', str(FINALIZER), '--report', str(rep)],
                   capture_output=True, text=True, cwd=str(HERE))
out['checkFinalizer'] = {'returncode': r.returncode, 'stdout': r.stdout.strip(),
                         'stderr': r.stderr.strip()[:300]}
if rep.is_file():
    d = json.loads(rep.read_text())
    out['checkFinalizer'].update(passed=d['passed'], failed=d['failed'],
                                 sourceSha256=d['sourceSha256'],
                                 sourceMatchesInput=d['sourceSha256'] == sha(FINALIZER),
                                 actualApplicationPerformed=d['actualApplicationPerformed'])

# ---- B: shipped envelope suite, run from a scratch COPY (it writes beside itself) ----
env_dir = HERE / 'envelope-suite-copy'
if env_dir.exists():
    shutil.rmtree(env_dir)
env_dir.mkdir()
for n in ('check-review-envelope.v2.py', 'review_envelope.py', 'coverage_contract.py'):
    shutil.copyfile(INPUTS / n, env_dir / n)
r2 = subprocess.run([REF, '-I', '-B', str(env_dir / 'check-review-envelope.v2.py')],
                    capture_output=True, text=True, cwd=str(env_dir))
out['checkReviewEnvelope'] = {'returncode': r2.returncode, 'stdout': r2.stdout.strip(),
                              'stderr': r2.stderr.strip()[:300],
                              'reportWrittenBesideSource': (env_dir / 'check-review-envelope.v2.report.json').is_file()}

# ---- C: extra before-image / activation cases ----
spec = importlib.util.spec_from_file_location('finalizer', FINALIZER)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
rows = []


def setup(base):
    root, pkg = base / 'root', base / 'pkg'
    (pkg / 'files/docs').mkdir(parents=True)
    (root / 'docs').mkdir(parents=True)
    (root / 'docs/current.md').write_text('existing user work\n')
    (pkg / 'files/docs/current.md').write_text('reviewed synthetic after image\n')
    (pkg / 'files/docs/new.md').write_text('new synthetic document\n')
    entries = []
    for rel in ['docs/current.md', 'docs/new.md']:
        p, live = pkg / 'files' / rel, root / rel
        entries.append({'path': rel, 'sha256': sha(p), 'bytes': p.stat().st_size,
                        'beforeSha256': sha(live) if live.exists() else None})
    mr, rr = 'docs/manifest.json', 'docs/review.json'
    mp = pkg / 'manifest.json'
    mp.write_text(json.dumps({'standing': 'SYNTHETIC TEST ONLY', 'implementationAuthorized': False,
                              'retainedManifestPath': mr, 'retainedReviewPath': rr,
                              'files': entries}))
    mh = sha(mp)
    rp = pkg / 'review.json'
    rp.write_text(json.dumps({'standing': 'SYNTHETIC TEST ONLY', 'verdict': 'ACCEPT',
                              'subjectManifestSha256': mh, 'newMustIssues': [], 'newShouldIssues': []}))
    (root / mr).write_bytes(mp.read_bytes())
    (root / rr).write_bytes(rp.read_bytes())
    return [root, pkg, mp, mh, rp, sha(rp)]


def inv(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob('*') if p.is_file()}


def neg(label, mutate, note=''):
    with tempfile.TemporaryDirectory(prefix='opensip-beforeimage-') as td:
        args = setup(Path(td))
        mutate(args)
        before = inv(args[0])
        caught = ''
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                F.apply(*args)
        except Exception as e:  # noqa: BLE001
            caught = f'{type(e).__name__}: {e}'[:140]
        after = inv(args[0])
        act = (args[0] / 'docs/coop/design-corrections/application-activation.v1.json').exists()
        rows.append({'id': label, 'refused': bool(caught), 'writesAfterRefusal': before != after,
                     'activationWritten': act, 'note': note, 'detail': caught})


neg('absent-at-freeze-but-live-file-appeared-with-foreign-bytes',
    lambda a: (a[0] / 'docs/new.md').write_text('user created this after review\n'),
    'beforeSha256 None but live now exists with other bytes')
neg('present-at-freeze-but-live-file-deleted',
    lambda a: (a[0] / 'docs/current.md').unlink(),
    'beforeSha256 set but live now absent')
neg('live-target-is-a-symlink',
    lambda a: ((a[0] / 'docs/current.md').unlink(),
               (a[0] / 'docs/current.md').symlink_to(a[0].parent / 'elsewhere.md')),
    'symlinked live path')
neg('retained-manifest-copy-tampered',
    lambda a: (a[0] / 'docs/manifest.json').write_text('{"tampered":true}'),
    'custody copy must match')
neg('staged-file-missing',
    lambda a: (a[1] / 'files/docs/new.md').unlink(),
    'staged after-image absent')
neg('manifest-claims-implementationAuthorized',
    lambda a: (a[2].write_text(json.dumps({**json.loads(a[2].read_text()),
                                           'implementationAuthorized': True})),
               a.__setitem__(3, sha(a[2]))),
    'implementation authorization must never be honoured')

# positive: activation is written strictly last and only once
with tempfile.TemporaryDirectory(prefix='opensip-activation-') as td:
    args = setup(Path(td))
    root = args[0]
    with contextlib.redirect_stdout(io.StringIO()):
        F.apply(*args, check_only=True)
    act_path = root / 'docs/coop/design-corrections/application-activation.v1.json'
    check_only_clean = not act_path.exists()
    with contextlib.redirect_stdout(io.StringIO()):
        F.apply(*args)
    applied = all((root / r).read_bytes() == (args[1] / 'files' / r).read_bytes()
                  for r in ['docs/current.md', 'docs/new.md'])
    receipt = json.loads(act_path.read_text())
    second = ''
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            F.apply(*args)
    except AssertionError as e:
        second = str(e)[:100]
    rows.append({'id': 'activation-written-last-and-never-replaced',
                 'refused': bool(second), 'writesAfterRefusal': False,
                 'activationWritten': True,
                 'note': f'checkOnlyLeftNoActivation={check_only_clean} applied={applied} '
                         f'implAuthorized={receipt["implementationAuthorized"]} '
                         f'qualClaimed={receipt["qualificationClaimed"]}',
                 'detail': second})

out['beforeImageAndActivation'] = rows
(HERE / 'p05_finalizer.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'beforeImageAndActivation'}, indent=2))
for r in rows:
    print(('ok  ' if r['refused'] and not r['writesAfterRefusal'] else 'CHECK'),
          r['id'], '| refused:', r['refused'], '| wrote:', r['writesAfterRefusal'],
          '| activation:', r['activationWritten'], '|', r['detail'] or r['note'])
