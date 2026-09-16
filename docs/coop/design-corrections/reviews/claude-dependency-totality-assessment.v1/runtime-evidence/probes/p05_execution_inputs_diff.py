"""P05 — p03 found check-execution-inputs.v1.py stdout differs between the successor kit and the remedy kit
(both exit 0). Discriminate a remedy effect from run-to-run nondeterminism: diff the two retained stdouts
at JSON-path level, then rerun the checker TWICE on the unpatched successor kit and TWICE on the remedy kit."""
import hashlib, json, os, subprocess

BASE = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
RC = os.path.join(BASE, 'receipts')
PY = '/tmp/opensip-architecture-review-env/bin/python'
CHK = 'check-execution-inputs.v1.py'
R = {}


def paths(a, b, p='$', out=None):
    out = [] if out is None else out
    if type(a) != type(b):
        out.append((p, a, b))
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((p + '.' + k, a.get(k, '<absent>'), b.get(k, '<absent>')))
            else:
                paths(a[k], b[k], p + '.' + k, out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((p + '[len]', len(a), len(b)))
        for n, (x, y) in enumerate(zip(a, b)):
            paths(x, y, '%s[%d]' % (p, n), out)
    elif a != b:
        out.append((p, a, b))
    return out


texts = {k: open(os.path.join(RC, 'p03-%s-%s.stdout' % (k, CHK))).read() for k in ('successor', 'remedy')}
try:
    js = {k: json.loads(v) for k, v in texts.items()}
    diffs = paths(js['successor'], js['remedy'])
    R['p03JsonPathDiffs'] = [{'path': p, 'successor': str(a)[:300], 'remedy': str(b)[:300]} for p, a, b in diffs[:60]]
    R['p03DiffCount'] = len(diffs)
except Exception as ex:  # noqa: BLE001
    R['parseError'] = str(ex)
    import difflib
    R['p03LineDiff'] = list(difflib.unified_diff(texts['successor'].splitlines(), texts['remedy'].splitlines(), lineterm='', n=0))[:80]
print('p03 differing JSON paths:', R.get('p03DiffCount'))
for d in R.get('p03JsonPathDiffs', [])[:25]:
    print('  %s\n     successor: %s\n     remedy   : %s' % (d['path'], d['successor'][:160], d['remedy'][:160]))

reruns = {}
for label in ('successor', 'remedy'):
    fdir = os.path.join(BASE, 'disposable', 'kit-' + label, 'docs/coop/design-corrections/foundation')
    outs = []
    for n in range(2):
        r = subprocess.run([PY, '-I', '-B', os.path.join(fdir, CHK)], capture_output=True, text=True, cwd=fdir, timeout=3600)
        open(os.path.join(RC, 'p05-%s-run%d.stdout' % (label, n)), 'w').write(r.stdout)
        outs.append({'returncode': r.returncode, 'stdoutSha256': hashlib.sha256(r.stdout.encode()).hexdigest()})
    reruns[label] = outs
R['reruns'] = reruns
R['successorRunToRunIdentical'] = reruns['successor'][0]['stdoutSha256'] == reruns['successor'][1]['stdoutSha256']
R['remedyRunToRunIdentical'] = reruns['remedy'][0]['stdoutSha256'] == reruns['remedy'][1]['stdoutSha256']
a = json.load(open(os.path.join(RC, 'p05-successor-run0.stdout')))
b = json.load(open(os.path.join(RC, 'p05-successor-run1.stdout')))
R['successorRunToRunDiffPaths'] = [p for p, _, _ in paths(a, b)][:40]
c = json.load(open(os.path.join(RC, 'p05-remedy-run0.stdout')))
R['successorVsRemedyDiffPathsSameRound'] = [p for p, _, _ in paths(a, c)][:40]
R['diffPathsOnlyExplainedByNondeterminism'] = set(R['successorVsRemedyDiffPathsSameRound']) <= set(R['successorRunToRunDiffPaths']) if R['successorRunToRunDiffPaths'] else None
print('reruns:', reruns)
print('successor run-to-run identical:', R['successorRunToRunIdentical'], '| remedy run-to-run identical:', R['remedyRunToRunIdentical'])
print('successor run0 vs run1 differing paths:', R['successorRunToRunDiffPaths'][:10])
print('successor vs remedy (same round) differing paths:', R['successorVsRemedyDiffPathsSameRound'][:10])
print('successor-vs-remedy differences fully explained by nondeterminism:', R['diffPathsOnlyExplainedByNondeterminism'])
json.dump(R, open(os.path.join(RC, 'p05-execution-inputs-diff.json'), 'w'), indent=1, default=str)
print('wrote p05-execution-inputs-diff.json')
