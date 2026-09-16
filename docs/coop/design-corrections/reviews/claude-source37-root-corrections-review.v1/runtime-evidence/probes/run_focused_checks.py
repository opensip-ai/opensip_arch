"""Sequentially run the focused checks of this bounded review (each via run_env.py, failures preserved):
1-3. the three changed owning checkers, individually (no group runner, no pin regeneration);
4-5. current planning checkers in --check mode against the overlay copy (binding consequence).
"""
import json, subprocess, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OV = RT + '/work/source37-overlay'
W = OV + '/docs/coop/design-corrections/workflows'
RUNS = [
    ('check-query-projection.v3', W, [W + '/check-query-projection.v3.py', '--report', RT + '/receipts/runs/check-query-projection.v3.report.json']),
    ('check_workflows.v1', W, [W + '/check_workflows.v1.py', '--report', RT + '/receipts/runs/check_workflows.v1.report.json']),
    ('check-workflow-projection.v3', W, [W + '/check-workflow-projection.v3.py']),
    ('check_implementation_planning', OV, [OV + '/docs/operations/check_implementation_planning.py', '--source', OV, '--check']),
    ('check_repository_file_inventory', OV, [OV + '/docs/operations/check_repository_file_inventory.py', '--check']),
]
summary = []
for name, cwd, argv in RUNS:
    p = subprocess.run(['python3', RT + '/probes/run_env.py', name, cwd, '--'] + argv, capture_output=True, text=True)
    first = p.stdout.splitlines()[0] if p.stdout else ''
    summary.append({'name': name, 'runner': first})
    print(p.stdout[-2500:])
    print(p.stderr[-800:])
json.dump(summary, open(RT + '/receipts/runs/focused-summary.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
