"""Compare X4-F2's X9 regression run sets with the accepted X9-6 evidence
(arch crash-matrix-x9/evidence/3d2d5b5…/: its lead-1 run files and both
targets' matrix.json), run by run, and with each other. X4-F1's compare.py,
with the host selection empty (law X4T r12 item 13: the host set runs its
census alone, under a prefix that matches no row).

Per run, compared exactly: verdict, postState.normalizedSha256, the ladder,
notApplicable, and every child's role, ordinal, exit, lastHeld, outcome and
trace {records, sha256}; timingGuard is checked present-or-absent only. Per
target and set: the census and the kill set. The product commit,
worktreeClean and releaseAbsence are expected to differ and are reported."""
import json
import os
import sys

W = '/Users/sb/code/opensip-ai/opensip-x4f2'
S = '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f2'
E = ('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/crash-matrix-x9/evidence/'
     '3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f')
NONE = 'X4F2-NO-ROW'


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
        prefixes = open(f'{S}/x9/rows-{target}.txt').read().split(',')
        wanted = set() if prefixes == [NONE] else set(prefixes)
        evidence_matrix = load(f'{E}/{target}/matrix.json')
        t = {'selected': len(wanted), 'runs': {}, 'census': {}, 'killSet': {},
             'timingGuardMs': {}, 'product': {}, 'matrixRuns': {}}
        for s in sets:
            out = f'{W}/target/opensip-x9/{s}-{target}'
            matrix = load(f'{out}/matrix.json')
            runs_dir = f'{out}/runs'
            names = sorted(p[:-5] for p in os.listdir(runs_dir) if p.endswith('.json')) \
                if os.path.isdir(runs_dir) else []
            if set(names) != wanted:
                report['differences'].append(
                    f'{s}-{target}: run set {sorted(set(names) ^ wanted)} differs from the selection')
            if len(matrix['runs']) != len(wanted):
                report['differences'].append(f'{s}-{target}: matrix.json lists {len(matrix["runs"])} runs')
            t['matrixRuns'][s] = len(matrix['runs'])
            same_census = matrix['census'] == evidence_matrix['census']
            t['census'][s] = {'equalToEvidence': same_census,
                              'trace': matrix['census']['trace'],
                              'points': len(matrix['census']['points'])}
            if not same_census:
                report['differences'].append(f'{s}-{target}: census differs from the evidence')
            same_kills = matrix['killSet'] == evidence_matrix['killSet']
            t['killSet'][s] = {'equalToEvidence': same_kills, 'points': len(matrix['killSet'])}
            if not same_kills:
                report['differences'].append(f'{s}-{target}: kill set differs from the evidence')
            t['product'][s] = matrix['product']
            for n in names:
                ours = load(f'{runs_dir}/{n}.json')
                theirs = load(f'{E}/{target}/runs/{n}.json')
                a, b = run_view(ours), run_view(theirs)
                entry = t['runs'].setdefault(n, {'normalizedSha256': b['normalizedSha256'],
                                                 'verdict': b['verdict'],
                                                 'childTraces': [c['trace']['sha256'] for c in b['children']],
                                                 'equal': {}})
                entry['equal'][s] = a == b
                if a != b:
                    diff = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
                    report['differences'].append({'set': s, 'target': target, 'run': n, 'diff': diff})
                if 'timingGuard' in ours:
                    t['timingGuardMs'].setdefault(s, {})[n] = ours['timingGuard']['monotonicMs']
        t['evidenceProduct'] = evidence_matrix['product']
        report['targets'][target] = t
    report['identical'] = not report['differences']
    json.dump(report, sys.stdout, indent=1, sort_keys=True)
    print()
    return 0 if report['identical'] else 1


sys.exit(main(sys.argv[1:]))
