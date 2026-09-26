"""Build results.json: positive runs, negative matrix vs macOS 26 runs 03/04, pins."""
from pathlib import Path
import hashlib, json, subprocess

BASE = Path('/Users/sb/opensip-deps/confinement-reprobe-01')
OLD = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/reviews/generator-confinement-01/logs')
REAL = Path('/Users/sb/code/opensip-ai/opensip')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    raw = Path(p).read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


# Rows whose value is informational (host identity/runtime detail), not a grant decision.
INFO = {'allowedInputRead', 'envKeys', 'openDescriptors', 'hostname', 'userInfo', 'cpuCount'}


def norm(v):
    if isinstance(v, dict) and 'ALLOWED' in v:
        inner = v['ALLOWED']
        return 'ALLOWED' if inner not in ('EPERM', 'RAN') else ('RAN' if inner == 'RAN' else 'EPERM(child)')
    return v


def matrix_rows(neg):
    probe = json.loads(neg['probe']['stdout'])
    rows = {('probe', k): v for k, v in probe.items()}
    rows[('parent', 'listenerObserved')] = neg['listenerObserved']
    rows[('parent', 'hardlinkSameInodeInScratch')] = any(e['sameInodeAsCanary'] for e in neg['confinedScratchEntries'].values())
    rows[('parent', 'symlinkInScratch')] = any(e['symlink'] for e in neg['confinedScratchEntries'].values())
    for k in ('canaryUnchanged', 'forbiddenTmpAbsent', 'inputsUntouched', 'generatorOutsideWriteCreated'):
        rows[('parent', k)] = neg[k]
    rows[('generator', 'outsideInputRoot')] = neg['generatorOutsideRead']['exitCode']
    rows[('generator', 'outsideOutputRoot')] = neg['generatorOutsideWrite']['exitCode']
    rows[('sandbox-exec', 'undeclaredBinSh')] = neg['undeclaredExec']['exitCode']
    return rows


old = {n: json.loads((OLD / f'results-run-0{n}.json').read_bytes())['negative'] for n in (3, 4)}
new = {n: json.loads((BASE / f'negative-{n}/results.json').read_bytes()) for n in (1, 2)}
old_rows = {n: matrix_rows(v) for n, v in old.items()}
new_rows = {n: matrix_rows(v['negative']) for n, v in new.items()}
keys = list(dict.fromkeys([*old_rows[3], *new_rows[1]]))
matrix, changed = [], []
for key in keys:
    o3, o4 = old_rows[3].get(key, 'n/a'), old_rows[4].get(key, 'n/a')
    n1, n2 = new_rows[1].get(key, 'n/a'), new_rows[2].get(key, 'n/a')
    info = key[1] in INFO
    same = norm(o3) == norm(n1) == norm(n2) == norm(o4)
    row = {'kind': key[0], 'row': key[1], 'macos26_run03': o3, 'macos26_run04': o4, 'macos27_run1': n1, 'macos27_run2': n2,
           'informational': info, 'newRow': o3 == 'n/a', 'confinedResultChanged': (not same) and not info and o3 != 'n/a'}
    if key[0] == 'probe':
        c = json.loads(new[1]['negative']['probeUnconfinedControl']['stdout']).get(key[1], 'n/a')
        row['macos27_unconfinedControl'] = c
        row['macos26_unconfinedControl'] = json.loads(old[3]['probeUnconfinedControl']['stdout']).get(key[1], 'n/a')
    if row['confinedResultChanged'] or (info and not same):
        changed.append(row)
    matrix.append(row)
ctrl = new[1]['negative']
controls = {'generatorOutsideInputRootUnconfined': ctrl['generatorOutsideReadControl']['exitCode'],
            'generatorOutsideOutputRootUnconfined': ctrl['generatorOutsideWriteControl']['exitCode'],
            'generatorOutsideOutputCreatedUnconfined': ctrl['generatorOutsideWriteControlCreated'],
            'binShUnconfined': [ctrl['undeclaredExecControl']['exitCode'], ctrl['undeclaredExecControl']['stdout'].strip()],
            'controlListenerObserved': ctrl['controlListenerObserved'], 'controlWritesCreated': ctrl['controlWritesCreated'],
            'controlScratchEntries': ctrl['controlScratchEntries']}

positive = []
for i in (1, 2):
    out = BASE / f'runs/positive-{i}'
    res = json.loads((out / 'result.json').read_bytes())
    sel = json.loads((out / 'selection-result.json').read_bytes())
    outputs = []
    for row in res['outputs']:
        newb = (out / 'assembly/output' / row['path']).read_bytes(); oldb = (REAL / row['path']).read_bytes()
        nl, ol = newb.split(b'\n'), oldb.split(b'\n')
        diff = [k + 1 for k in range(max(len(nl), len(ol))) if nl[k:k + 1] != ol[k:k + 1]]
        outputs.append({**row, 'checkedIn': {'bytes': len(oldb), 'sha256': hashlib.sha256(oldb).hexdigest()},
                        'identical': newb == oldb, 'differingLines': diff,
                        'matchesIgnoringProvenanceLines2to3': (nl[:1] + nl[3:]) == (ol[:1] + ol[3:]) if row['path'].endswith('report.ts') else newb == oldb})
    steps = {p.stem.replace('-profile', ''): sha(p) for p in sorted(out.glob('*-profile.sb'))}
    positive.append({'run': i, 'exitCode': 1, 'selectionResult': sel, 'pipelinePassed': res['passed'], 'outputs': outputs,
                     'inputClosure': res['inputClosure'], 'stepProfileSha256': steps,
                     'stepStderrBytes': {p.stem: p.stat().st_size for p in sorted(out.glob('*.stderr'))},
                     'bypassLog': json.loads((BASE / f'runs/bypass-log-{i}.json').read_bytes()) | {'B1_lfsPointerAccepted': 'see runs/bypass-log-%d.json' % i}})
agree = [o['sha256'] for o in positive[0]['outputs']] == [o['sha256'] for o in positive[1]['outputs']]

result = {
    'standing': 'Scratch-only macOS 27 re-probe; development pins only; not design acceptance, not release qualification',
    'host': subprocess.run(['/usr/bin/sw_vers'], capture_output=True, text=True).stdout,
    'uname': subprocess.run(['/usr/bin/uname', '-a'], capture_output=True, text=True).stdout.strip(),
    'positive': {'runs': positive, 'outputsAgreeAcrossRuns': agree,
                 'all8MatchCheckedInApartFromReportProvenance': all(o['matchesIgnoringProvenanceLines2to3'] for p in positive for o in p['outputs'])},
    'negative': {'matrix': matrix, 'rowsChangedOrDifferent': changed, 'unconfinedControls': controls,
                 'workUnchanged': [new[1]['workUnchanged'], new[2]['workUnchanged']],
                 'generatorGrantedPositiveControl': [new[n]['negative']['generatorGranted']['exitCode'] for n in (1, 2)],
                 'outputRootStillPresentAfterRenameAttempt': [new[n]['negative']['outputRootStillPresent'] for n in (1, 2)],
                 'runs': {n: str(BASE / f'negative-{n}/results.json') for n in (1, 2)}},
    'sandboxProfiles': {name: {'macos26': pin(BASE / f'sbdiff/{name}-macos26.sb'), 'macos27': pin(BASE / f'sbdiff/{name}-macos27.sb')}
                        for name in ('system', 'dyld')},
}
(BASE / 'results.json').write_text(json.dumps(result, indent=1) + '\n')
print(json.dumps({'agree': agree, 'all8': result['positive']['all8MatchCheckedInApartFromReportProvenance'],
                  'changed': [(r['kind'], r['row'], r['macos26_run03'], r['macos27_run1']) for r in changed],
                  'newRows': [(r['row'], r['macos27_run1'], r.get('macos27_unconfinedControl')) for r in matrix if r['newRow']],
                  'controls': controls}, indent=1, default=str))
