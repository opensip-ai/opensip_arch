"""V05: F8 - execute the bounded 'current tool check' block exactly as prepare-validation.py
does (lines 86-109), in a disposable copy. F9 - the --report contract of the envelope suite,
and the residual in-place report behaviour of check-retain-public.v1.py.

The full application root is unavailable, so the F8 block is extracted verbatim-equivalent
rather than run through prepare-validation.py end to end. That scope limit is stated.
"""
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
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
out = {}

CURRENT_TOOLS = ['check-review-envelope.v2.py', 'check-retain-public.v1.py',
                 'coverage_contract.py', 'review_envelope.py', 'retain_public.py',
                 'retain-application-review.successor.v1.py',
                 'launch-application-review.successor.v1.py']
LEGACY = 'public-custody-before-compaction.v1'

# ---------------- F8: bounded re-execution of the current tools ----------------
work = HERE / 'tool-validation'
if work.exists():
    shutil.rmtree(work)
work.mkdir()
tool_inputs = []
for name in CURRENT_TOOLS:
    src = INPUTS / name
    shutil.copyfile(src, work / name)
    tool_inputs.append({'path': name, 'sha256': sha(src), 'bytes': src.stat().st_size})
shutil.copytree(INPUTS / LEGACY, work / LEGACY)
for src in sorted((INPUTS / LEGACY).rglob('*')):
    if src.is_file() and '__pycache__' not in src.parts:
        tool_inputs.append({
            'path': LEGACY + '/' + src.relative_to(INPUTS / LEGACY).as_posix(),
            'sha256': sha(src), 'bytes': src.stat().st_size,
            'standing': 'historical counterexample fixture, not current implementation'})

runs = []
for name, extra, report_name in [
    ('check-review-envelope.v2.py', ['--report', str(work / 'current-envelope.json')], 'current-envelope.json'),
    ('check-retain-public.v1.py', [], 'check-retain-public.v2.report.json'),
]:
    cmd = [REF, '-I', '-B', str(work / name)] + extra
    r = subprocess.run(cmd, cwd=str(work), capture_output=True, text=True)
    rp = work / report_name
    rep = json.loads(rp.read_text()) if rp.is_file() else None
    runs.append({'tool': name, 'exitCode': r.returncode,
                 'stdout': r.stdout.strip()[:300], 'stderr': r.stderr.strip()[:200],
                 'reportWritten': rp.is_file(),
                 'passed': rep.get('passed') if rep else None,
                 'failed': rep.get('failed') if rep else None,
                 'reportSha256': sha(rp) if rp.is_file() else None})
unchanged = [row['path'] for row in tool_inputs if sha(work / row['path']) != row['sha256']]
out['F8'] = {'toolInputsHashed': len(tool_inputs), 'runs': runs,
             'toolsChangedTheirOwnInputs': unchanged,
             'allExitZero': all(x['exitCode'] == 0 for x in runs),
             'noFailures': all(not x['failed'] for x in runs)}

# ---------------- F9: --report contract of the envelope suite ----------------
f9 = []
env_copy = HERE / 'f9-envelope'
if env_copy.exists():
    shutil.rmtree(env_copy)
env_copy.mkdir()
for n in ('check-review-envelope.v2.py', 'review_envelope.py', 'coverage_contract.py'):
    shutil.copyfile(INPUTS / n, env_copy / n)

# (a) --report is required
r = subprocess.run([REF, '-I', '-B', str(env_copy / 'check-review-envelope.v2.py')],
                   capture_output=True, text=True, cwd=str(env_copy))
f9.append({'id': 'report-arg-required', 'passed': r.returncode != 0,
           'detail': r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else ''})
# (b) writes only to the named path; nothing beside the source
before = {p.name for p in env_copy.iterdir()}
tgt = env_copy / 'chosen-report.json'
r = subprocess.run([REF, '-I', '-B', str(env_copy / 'check-review-envelope.v2.py'),
                    '--report', str(tgt)], capture_output=True, text=True, cwd=str(env_copy))
after = {p.name for p in env_copy.iterdir()}
f9.append({'id': 'writes-only-named-report', 'passed': r.returncode == 0 and tgt.is_file()
           and (after - before) == {'chosen-report.json'},
           'detail': 'new files: ' + str(sorted(after - before))})
# (c) refuses to overwrite an existing report (preserves prior evidence)
r = subprocess.run([REF, '-I', '-B', str(env_copy / 'check-review-envelope.v2.py'),
                    '--report', str(tgt)], capture_output=True, text=True, cwd=str(env_copy))
f9.append({'id': 'refuses-overwriting-prior-report', 'passed': r.returncode != 0,
           'detail': (r.stderr.strip().splitlines() or [''])[-1][:140]})

# (d) residual: check-retain-public.v1.py has no --report and writes fixed names into HERE.
#     Demonstrated ONLY in a disposable copy that carries a stand-in pinned report.
res = HERE / 'f9-retain-inplace'
if res.exists():
    shutil.rmtree(res)
res.mkdir()
for n in CURRENT_TOOLS:
    shutil.copyfile(INPUTS / n, res / n)
shutil.copytree(INPUTS / LEGACY, res / LEGACY)
pinned = res / 'check-retain-public.v2.report.json'
shutil.copyfile(INPUTS / 'check-retain-public.v2.report.json', pinned)
pinned_sha_before = sha(pinned)
r = subprocess.run([REF, '-I', '-B', str(res / 'check-retain-public.v1.py')],
                   capture_output=True, text=True, cwd=str(res))
pinned_sha_after = sha(pinned)
f9.append({'id': 'retain-suite-overwrites-pinned-report-in-place',
           'passed': None,
           'observed': 'OVERWRITTEN' if pinned_sha_before != pinned_sha_after else 'preserved',
           'detail': f'exit={r.returncode} before={pinned_sha_before[:12]} after={pinned_sha_after[:12]}'})
out['F9'] = f9

(HERE / 'v05_f8_f9.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out['F8'], indent=2))
print()
for x in f9:
    print(('ok  ' if x.get('passed') else ('--  ' if x.get('passed') is None else 'DIFF')),
          x['id'], '|', x.get('observed', ''), '|', x['detail'])
