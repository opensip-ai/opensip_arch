"""Compare J3a's two lead sets (storage and host, in full) with the accepted
X9-6 evidence (arch crash-matrix-x9/evidence/3d2d5b5…/: its lead-1 run files
and both targets' matrix.json), run by run. X4-F2's compare.py, with every
required run selected.

Per run, compared exactly: verdict, postState.normalizedSha256, the ladder,
notApplicable, and every child's role, ordinal, exit, lastHeld, outcome and
trace {records, sha256}; timingGuard is checked present-or-absent only (its
monotonic value is recorded, not compared). Per target: the run list against
the evidence's, the census and the kill set. The product commit,
worktreeClean and releaseAbsence are expected to differ and are reported."""
import json
import os
import sys

W = '/Users/sb/code/opensip-ai/opensip-j3a'
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
        evidence_matrix = load(f'{E}/{target}/matrix.json')
        evidence_runs = sorted(p[:-5] for p in os.listdir(f'{E}/{target}/runs') if p.endswith('.json'))
        t = {'evidenceRuns': len(evidence_runs), 'runs': {}, 'census': {}, 'killSet': {},
             'timingGuardMs': {}, 'product': {}, 'matrixRuns': {}, 'verdicts': {},
             'equalRuns': {}, 'differingRuns': {}}
        for s in sets:
            out = f'{W}/target/opensip-x9/{s}-{target}'
            matrix = load(f'{out}/matrix.json')
            runs_dir = f'{out}/runs'
            names = sorted(p[:-5] for p in os.listdir(runs_dir) if p.endswith('.json')) \
                if os.path.isdir(runs_dir) else []
            if names != evidence_runs:
                report['differences'].append(
                    f'{s}-{target}: run list differs from the evidence: {sorted(set(names) ^ set(evidence_runs))}')
            t['matrixRuns'][s] = len(matrix['runs'])
            if len(matrix['runs']) != len(evidence_matrix['runs']):
                report['differences'].append(f'{s}-{target}: matrix.json lists {len(matrix["runs"])} runs')
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
            verdicts = {}
            equal = 0
            for n in names:
                ours = load(f'{runs_dir}/{n}.json')
                verdicts[ours['verdict']] = verdicts.get(ours['verdict'], 0) + 1
                if n not in evidence_runs:
                    continue
                theirs = load(f'{E}/{target}/runs/{n}.json')
                a, b = run_view(ours), run_view(theirs)
                entry = t['runs'].setdefault(n, {'normalizedSha256': b['normalizedSha256'],
                                                 'verdict': b['verdict'], 'equal': {}})
                entry['equal'][s] = a == b
                if a == b:
                    equal += 1
                else:
                    diff = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
                    report['differences'].append({'set': s, 'target': target, 'run': n, 'diff': diff})
                if 'timingGuard' in ours:
                    t['timingGuardMs'].setdefault(s, {})[n] = ours['timingGuard'].get('monotonicMs')
            t['verdicts'][s] = verdicts
            t['equalRuns'][s] = equal
            t['differingRuns'][s] = len(names) - equal
        t['evidenceProduct'] = evidence_matrix['product']
        report['targets'][target] = t
    report['identical'] = not report['differences']
    json.dump(report, sys.stdout, indent=1, sort_keys=True)
    print()
    return 0 if report['identical'] else 1


sys.exit(main(sys.argv[1:]))
