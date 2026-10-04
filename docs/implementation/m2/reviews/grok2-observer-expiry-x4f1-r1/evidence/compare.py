"""Compare X4-F1's X9 regression run sets with the accepted X9-6 evidence
(arch crash-matrix-x9/evidence/3d2d5b5…/, the lead-1 run files and both
targets' matrix.json census), and with each other.

Per run, compared exactly: verdict, postState.normalizedSha256, the ladder,
notApplicable, and every child's role, ordinal, exit, lastHeld, outcome and
trace {records, sha256}; timingGuard is checked present-or-absent only (the
law excludes its value from repetition comparison). Per target: the census
points and census trace. Product commit and worktreeClean are expected to
differ (the subject is an uncommitted diff on 3e64266) and are reported."""
import json
import os
import sys

W = '/Users/sb/code/opensip-ai/opensip-x4f1'
S = '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1'
E = ('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/crash-matrix-x9/evidence/'
     '3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f')


def load(path):
    with open(path) as f:
        return json.load(f)


def child_view(c):
    return {k: c.get(k) for k in ('role', 'ordinal', 'exit', 'lastHeld', 'outcome', 'trace')}


def run_view(r):
    return {
        'verdict': r['verdict'],
        'normalizedSha256': r['postState']['normalizedSha256'],
        'ladder': r['ladder'],
        'notApplicable': r.get('notApplicable'),
        'children': [child_view(c) for c in r['children']],
        'timingGuardPresent': 'timingGuard' in r,
    }


def main(sets):
    report = {'sets': sets, 'targets': {}, 'differences': []}
    for target in ('storage', 'host'):
        wanted = set(open(f'{S}/rows-{target}.txt').read().split(','))
        evidence_matrix = load(f'{E}/{target}/matrix.json')
        t = {'runs': {}, 'census': {}, 'timingGuardMs': {}}
        for s in sets:
            out = f'{W}/target/opensip-x9/{s}-{target}'
            matrix = load(f'{out}/matrix.json')
            names = sorted(p[:-5] for p in os.listdir(f'{out}/runs') if p.endswith('.json'))
            if set(names) != wanted:
                report['differences'].append(
                    f'{s}-{target}: run set {sorted(set(names) ^ wanted)} differs from the selection')
            same_census = matrix['census'] == evidence_matrix['census']
            t['census'][s] = {'equalToEvidence': same_census,
                              'trace': matrix['census']['trace'],
                              'points': len(matrix['census']['points'])}
            if not same_census:
                report['differences'].append(f'{s}-{target}: census differs from the evidence')
            if matrix['killSet'] != evidence_matrix['killSet']:
                report['differences'].append(f'{s}-{target}: kill set differs from the evidence')
            t['product'] = matrix['product']
            for n in names:
                ours = load(f'{out}/runs/{n}.json')
                theirs = load(f'{E}/{target}/runs/{n}.json')
                a, b = run_view(ours), run_view(theirs)
                entry = t['runs'].setdefault(n, {'normalizedSha256': b['normalizedSha256'],
                                                 'childTraces': [c['trace']['sha256'] for c in b['children']],
                                                 'equal': {}})
                entry['equal'][s] = a == b
                if a != b:
                    diff = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
                    report['differences'].append({'set': s, 'target': target, 'run': n, 'diff': diff})
                if 'timingGuard' in ours:
                    t['timingGuardMs'].setdefault(s, {})[n] = ours['timingGuard']['monotonicMs']
        report['targets'][target] = t
    report['identical'] = not report['differences']
    json.dump(report, sys.stdout, indent=1, sort_keys=True)
    print()
    return 0 if report['identical'] else 1


sys.exit(main(sys.argv[1:]))
