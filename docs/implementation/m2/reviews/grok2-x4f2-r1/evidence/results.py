"""Summarise X4-F2's lane logs and X9 comparison into results.json."""
import json, re, sys
S = '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f2'
L = f'{S}/lanes'
def counts(name):
    p = f = 0; i = 0; bins = 0
    for line in open(f'{L}/{name}.log', errors='replace'):
        m = re.search(r'test result: (\w+)\. (\d+) passed; (\d+) failed; (\d+) ignored', line)
        if m:
            bins += 1; p += int(m[2]); f += int(m[3]); i += int(m[4])
    return {'passed': p, 'failed': f, 'ignored': i, 'binaries': bins}
summary = {}
for line in open(f'{L}/summary.txt'):
    m = re.match(r'(\S+) exit=(\d+) seconds=(\d+)', line)
    if m:
        summary[m[1]] = {'exit': int(m[2]), 'seconds': int(m[3])}
out = {'lanes': summary, 'tests': {n: counts(n) for n in ('new-tests', 'ws1', 'ws2', 'ws-doc', 'feature') if n in summary}}
try:
    c = json.load(open(f'{S}/x9/compare.json'))
    out['x9'] = {'identical': c['identical'], 'differences': len(c['differences']),
                 'targets': {t: {'runs': len(v['runs']), 'census': v['census'], 'killSet': v['killSet'],
                                 'matrixRuns': v['matrixRuns'],
                                 'timingGuardMs': {s: [min(x.values()), max(x.values()), len(x)] for s, x in v['timingGuardMs'].items()}}
                             for t, v in c['targets'].items()}}
except FileNotFoundError:
    pass
json.dump(out, sys.stdout, indent=1, sort_keys=True); print()
