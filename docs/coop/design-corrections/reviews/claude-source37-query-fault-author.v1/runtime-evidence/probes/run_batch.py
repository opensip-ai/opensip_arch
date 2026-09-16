"""Sequentially run the affected owner checkers on one tree (each via run_check.py; failures preserved, no group runner).

usage: python3 run_batch.py TREE   (source37-pristine | source37-coauthor)
Affected owners: identity/replay/composition/fault carriers and every maintained close_run caller found by search,
plus the query owner. No global suite, pin regeneration, freeze or planning checker.
"""
import json, subprocess, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
TREE = sys.argv[1]
F = '{TREE}/docs/coop/design-corrections/foundation'
W = '{TREE}/docs/coop/design-corrections/workflows'
RUNS = [
    ('check-composition.v3', F, [F + '/check-composition.v3.py']),
    ('check-replay.v3', F, [F + '/check-replay.v3.py']),
    ('check-semantic-replay.v3', F, [F + '/check-semantic-replay.v3.py']),
    ('check-execution-replay.v3', F, [F + '/check-execution-replay.v3.py']),
    ('check-candidate-replay.v3', F, [F + '/check-candidate-replay.v3.py']),
    ('check-evaluator-faults.v3', F, [F + '/check-evaluator-faults.v3.py']),
    ('check-provider-attribution-return.v2', F, [F + '/check-provider-attribution-return.v2.py']),
    ('check-execution-inputs.v1', F, [F + '/check-execution-inputs.v1.py']),
    ('check-identity', F, [F + '/check-identity.py', '--report', '{RT}/receipts/runs/check-identity.' + TREE + '.report.json']),
    ('check-comparison-knowledge.v3', W, [W + '/check-comparison-knowledge.v3.py']),
    ('check-workflow-projection.v3', W, [W + '/check-workflow-projection.v3.py']),
]
if TREE == 'source37-pristine':
    RUNS.append(('check-query-projection.v3', W, [W + '/check-query-projection.v3.py', '--report',
                                                  '{RT}/receipts/runs/check-query-projection.v3.' + TREE + '.report.json']))
summary = []
for name, cwd, argv in RUNS:
    p = subprocess.run(['python3', RT + '/probes/run_check.py', name, TREE, cwd, '--'] + argv, capture_output=True, text=True)
    first = p.stdout.splitlines()[0] if p.stdout else ''
    try:
        row = json.loads(first)
    except ValueError:
        row = {'name': name, 'runnerError': (p.stdout + p.stderr)[-800:]}
    summary.append(row)
    print(json.dumps(row), flush=True)
json.dump(summary, open(RT + '/receipts/runs/batch-summary.' + TREE + '.json', 'w'), indent=1)
