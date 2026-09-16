"""Export + fresh-process replay + tamper controls for every claimed complete positive Run,
bound to the v15 kit. One driver so no Run is silently skipped.

    python3 run.py all_runs.py [export|replay|controls|all]
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'
PY = '/tmp/opensip-architecture-review-env/bin/python'

RUNS = [
    ('run_syntax_code_full', 'syntax-code',
     'R-RUN-SYNTAX-CODE,R-RUN-NO-COMPILER-UNIT,R-RUN-FILE-FACT-INVENTORY,'
     'R-RUN-CLONES-L0-AND-NORMALIZED,R-RUN-CLONES-CUSTODY'),
    ('run_ts_full', 'typescript',
     'R-RUN-TS,R-RUN-TS-NODE-MODULES,R-RUN-TS-CONFIG-DEPS,R-RUN-NONCEMPTY-CONTEXT,'
     'R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC,R-IMPORTED-PAYLOAD-IN-GRAPH,'
     'R-JS-CLONE-BODY-THROUGH-TS,R-NATIVE-PREIMAGE-JOINS'),
    ('run_rust_full', 'rust',
     'R-RUN-RUST,R-RUN-RUST-MIXED-EDITION,R-RUN-RUST-TARGET-EDITION,R-RUN-RUST-BODY-DIALECT,'
     'R-RUN-RUST-SAME-FILE-TWO-EDITIONS,R-RUN-RUST-HASH-MARKER,R-RUN-RUST-LARGE-EDITION-MAP,'
     'R-RUN-RUST-VERSION-COMPONENT,R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE,'
     'R-RUN-NONCEMPTY-CONTEXT,R-NATIVE-PREIMAGE-JOINS'),
    ('run_rust_partial', 'rust-partial',
     'R-RUN-RUST-PARTIAL-EMPTY-CLONES,R-CLONE-DEFICIENCY-PAIRING'),
    ('run_syntax_data', 'syntax-data',
     'R-RUN-SYNTAX-DATA,R-RUN-UNAVAILABLE-SEMANTIC,R-RUN-UNSUPPORTED-GRAMMAR'),
]


def sh(args):
    p = subprocess.run([PY, '-I', '-B'] + args, capture_output=True, text=True, cwd=HERE)
    return p.returncode, p.stdout, p.stderr


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    summary = []
    for mod, label, ids in RUNS:
        if not os.path.exists(os.path.join(HERE, mod + '.py')):
            summary.append({'run': label, 'status': 'MODULE_ABSENT'})
            print('%-14s MODULE ABSENT (%s.py)' % (label, mod))
            continue
        row = {'run': label, 'module': mod, 'requirementIds': ids.split(',')}
        if mode in ('export', 'all'):
            rc, so, se = sh([os.path.join(HERE, 'export_run.py'), mod, label, ids])
            row['export'] = {'exit': rc, 'stdout': so.strip().splitlines()[-4:],
                             'stderr': se.strip().splitlines()[-6:] if rc else []}
            print('%-14s export exit=%d  %s' % (label, rc,
                                                (so.strip().splitlines() or [''])[-1][:100]))
        if mode in ('replay', 'all'):
            store = OUT + '/runs/%s.store.json' % label
            rc, so, se = sh([os.path.join(HERE, 'replay_run.py'), store])
            lines = so.strip().splitlines()
            row['replay'] = {'exit': rc, 'stdout': lines,
                             'stderr': se.strip().splitlines()[-6:] if rc else []}
            v = [x for x in lines if x.startswith('replay')]
            print('%-14s replay exit=%d  %s' % (label, rc, (v or [''])[0][:90]))
        if mode in ('controls', 'all'):
            store = OUT + '/runs/%s.store.json' % label
            rc, so, se = sh([os.path.join(HERE, 'run_controls.py'), store, label])
            lines = so.strip().splitlines()
            row['tamperControls'] = {'exit': rc, 'lastLine': lines[-1] if lines else '',
                                     'stderr': se.strip().splitlines()[-6:] if rc else []}
            print('%-14s controls exit=%d  %s' % (label, rc, (lines[-1] if lines else '')[:80]))
        summary.append(row)
    with open(OUT + '/runs/all-runs-summary.json', 'w') as f:
        json.dump(summary, f, indent=1)
    bad = [r['run'] for r in summary
           if r.get('status') == 'MODULE_ABSENT'
           or any(r.get(k, {}).get('exit', 0) for k in ('export', 'replay', 'tamperControls'))]
    print()
    print('runs with a nonzero stage or an absent module:', bad)
    sys.exit(1 if bad else 0)


main()
