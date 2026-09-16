"""W05: G4 - the retain suite's required distinct fresh report paths, refusal BEFORE
execution, and an independent re-measurement of the 69 retain + 35 envelope controls in
disposable copies, with ID preservation checked against my own v2 measured run.
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
V2SCRATCH = Path('/tmp/opensip-design-corrections/claude-application-tools-review.v2/scratch')
REF = '/tmp/opensip-architecture-review-env/bin/python'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
TOOLS = ['check-review-envelope.v2.py', 'check-retain-public.v1.py', 'coverage_contract.py',
         'review_envelope.py', 'retain_public.py',
         'retain-application-review.successor.v1.py',
         'launch-application-review.successor.v1.py']
LEGACY = 'public-custody-before-compaction.v1'
out = {}


def fresh_copy(prefix):
    d = Path(tempfile.mkdtemp(prefix=prefix))
    for n in TOOLS:
        shutil.copyfile(INPUTS / n, d / n)
    shutil.copytree(INPUTS / LEGACY, d / LEGACY)
    return d


def inputs_hashes(d):
    h = {n: sha(d / n) for n in TOOLS}
    for p in sorted((d / LEGACY).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            h[LEGACY + '/' + p.relative_to(d / LEGACY).as_posix()] = sha(p)
    return h


# ---------------- G4 argument contract ----------------
g4 = []
d = fresh_copy('opensip-g4-args-')
suite = str(d / 'check-retain-public.v1.py')


def attempt(ident, args, expect_refuse, watch=()):
    before = {p.name for p in d.iterdir()}
    r = subprocess.run([REF, '-I', '-B', suite] + args, capture_output=True, text=True, cwd=str(d))
    after = {p.name for p in d.iterdir()}
    created = sorted(after - before)
    refused = r.returncode != 0
    g4.append({'id': ident, 'expected': 'REFUSE' if expect_refuse else 'RUN',
               'observed': 'REFUSE' if refused else 'RUN',
               'asExpected': refused is expect_refuse,
               'filesCreated': created,
               'watchedNotCreated': [w for w in watch if w not in created],
               'detail': (r.stderr.strip().splitlines() or [''])[-1][:140]})
    return created


attempt('no-args-refuses', [], True)
attempt('report-only-refuses', ['--report', str(d / 'r1.json')], True, watch=['r1.json'])
attempt('envelope-report-only-refuses', ['--envelope-report', str(d / 'e1.json')], True,
        watch=['e1.json'])
attempt('same-path-for-both-refuses',
        ['--report', str(d / 'same.json'), '--envelope-report', str(d / 'same.json')], True,
        watch=['same.json'])
# positive: two distinct fresh paths
created = attempt('distinct-fresh-paths-run',
                  ['--report', str(d / 'ok-report.json'),
                   '--envelope-report', str(d / 'ok-envelope.json')], False)
# overwrite refusal, and it must refuse BEFORE executing: the fresh envelope path must
# NOT be created when the report path already exists.
attempt('existing-report-refuses-before-executing',
        ['--report', str(d / 'ok-report.json'),
         '--envelope-report', str(d / 'never-created.json')], True,
        watch=['never-created.json'])
attempt('existing-envelope-report-refuses-before-executing',
        ['--report', str(d / 'never-created-2.json'),
         '--envelope-report', str(d / 'ok-envelope.json')], True,
        watch=['never-created-2.json'])
out['G4_argumentContract'] = g4

# static: the guards precede imports and any suite body
src_lines = (INPUTS / 'check-retain-public.v1.py').read_text().splitlines()
guard_lines = [i + 1 for i, l in enumerate(src_lines)
               if l.startswith('assert args.report') or l.startswith('assert not args.report')]
first_import_here = next(i + 1 for i, l in enumerate(src_lines) if l.startswith('HERE ='))
first_exec = next(i + 1 for i, l in enumerate(src_lines) if l.startswith('R = load_mod'))
out['G4_guardPlacement'] = {'guardAssertLines': guard_lines,
                            'moduleSetupLine': first_import_here,
                            'firstSuiteExecutionLine': first_exec,
                            'guardsPrecedeAllExecution': max(guard_lines) < first_import_here < first_exec}

# ---------------- independent re-measurement ----------------
meas = {}
d2 = fresh_copy('opensip-g4-measure-')
before_h = inputs_hashes(d2)
rep = d2 / 'retain-report.json'
env_from_retain = d2 / 'retain-envelope-report.json'
r = subprocess.run([REF, '-I', '-B', str(d2 / 'check-retain-public.v1.py'),
                    '--report', str(rep), '--envelope-report', str(env_from_retain)],
                   capture_output=True, text=True, cwd=str(d2))
retain_report = json.loads(rep.read_text()) if rep.is_file() else None
retain_env = json.loads(env_from_retain.read_text()) if env_from_retain.is_file() else None

d3 = fresh_copy('opensip-g4-measure-env-')
envrep = d3 / 'envelope-report.json'
r2 = subprocess.run([REF, '-I', '-B', str(d3 / 'check-review-envelope.v2.py'),
                     '--report', str(envrep)], capture_output=True, text=True, cwd=str(d3))
env_report = json.loads(envrep.read_text()) if envrep.is_file() else None
after_h = inputs_hashes(d2)

meas['retainSuite'] = {
    'exitCode': r.returncode, 'stdout': r.stdout.strip()[:220],
    'passed': retain_report['passed'], 'failed': retain_report['failed'],
    'controlCount': len(retain_report['checks']),
    'existing40Passed': retain_report['existing40Passed'],
    'existing40Count': retain_report['existing40Count'],
    'existing40Failed': retain_report['existing40Failed'],
    'uniqueIds': len({c['id'] for c in retain_report['checks']}),
    'actualApplicationPerformed': retain_report['actualApplicationPerformed'],
    'testedRealPrivateCliContents': retain_report['testedRealPrivateCliContents'],
}
meas['retainEmbeddedEnvelopeReport'] = {
    'passed': retain_env['passed'], 'failed': retain_env['failed'],
    'controlCount': len(retain_env['checks']),
    'allIdsPrefixedV1': all(c['id'].startswith('v1-') for c in retain_env['checks']),
}
meas['envelopeSuite'] = {
    'exitCode': r2.returncode, 'stdout': r2.stdout.strip()[:220],
    'passed': env_report['passed'], 'failed': env_report['failed'],
    'controlCount': len(env_report['checks']),
    'existing20Passed': env_report['existing20Passed'],
    'existing20Count': env_report['existing20Count'],
    'uniqueIds': len({c['id'] for c in env_report['checks']}),
}
meas['toolInputsUnchangedAcrossRun'] = [k for k in before_h if before_h[k] != after_h[k]]

# ID preservation vs my own v2 measured run
v2_retain = V2SCRATCH / 'tool-validation/check-retain-public.v2.report.json'
v2_env = V2SCRATCH / 'tool-validation/current-envelope.json'
pres = {}
if v2_retain.is_file():
    old = [c['id'] for c in json.loads(v2_retain.read_text())['checks']]
    new = [c['id'] for c in retain_report['checks']]
    pres['retain'] = {'v2Count': len(old), 'v3Count': len(new),
                      'idsRemoved': [x for x in old if x not in new],
                      'idsAdded': [x for x in new if x not in old],
                      'orderIdentical': old == new}
if v2_env.is_file():
    old = [c['id'] for c in json.loads(v2_env.read_text())['checks']]
    new = [c['id'] for c in env_report['checks']]
    pres['envelope'] = {'v2Count': len(old), 'v3Count': len(new),
                        'idsRemoved': [x for x in old if x not in new],
                        'idsAdded': [x for x in new if x not in old],
                        'orderIdentical': old == new}
meas['idPreservationVsMyV2Run'] = pres

# Historical pinned report remains history, byte-identical to the manifest entry.
pinned = INPUTS / 'check-retain-public.v2.report.json'
meas['historicalPinnedReport'] = {
    'sha256': sha(pinned),
    'manifestSha256': next(x['sha256'] for x in json.loads(
        (HERE.parent / 'input-manifest.json').read_text())['files']
        if x['path'] == 'check-retain-public.v2.report.json'),
    'freshRetainReportSha256': sha(rep),
    'freshEqualsPinned': sha(rep) == sha(pinned),
}
out['G4_measurement'] = meas

(HERE / 'w05_g4.result.json').write_text(json.dumps(out, indent=2) + '\n')
bad = [x['id'] for x in g4 if not x['asExpected']]
watch = [(x['id'], x['filesCreated']) for x in g4 if x['expected'] == 'REFUSE' and x['filesCreated']]
print('G4 argument contract:', len(g4), 'cases,', len(g4) - len(bad), 'as expected, unexpected=', bad)
print('refusal cases that still created files:', watch)
print('guard placement:', json.dumps(out['G4_guardPlacement']))
print()
print(json.dumps(meas, indent=2))
