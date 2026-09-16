"""p05 <variant>: discrimination controls on a hybrid regular copy of v2 work/edited (never the edited tree itself).

Each variant restores v1 bytes or applies one asserted mutation, runs only the affected owner validator, and checks
that exactly the expected controls fail. Reports: receipts/p05-<variant>[.rN]/; trees: work/hybrid-<variant>[.rN]/.
"""
import json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
V1 = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1/work/edited')
PY = '/tmp/opensip-architecture-review-env/bin/python'
FND = 'docs/coop/design-corrections/foundation/'
SEC = 'docs/coop/design-corrections/security/'
MODEL = FND + 'run_termination_model.v1.py'
COMP = 'run-termination:host-composition-boundary'
NEW_JOINS = {'wrong-inventory-otherwise-admitted', 'receipt-inventory-missing-a-published-object', 'wrong-execution-plan-otherwise-admitted',
             'stage-count-not-the-execution-plans', 'stages-completed-beyond-stage-count', 'first-failed-stage-outside-the-execution-plan'}


def off(line):
    return (MODEL, line, line.split('if ', 1)[0] + 'if False:\n')


VARIANTS = {
    'v1-model': {'restore': [MODEL], 'run': 'semantic', 'faultLabels': NEW_JOINS},
    'inventory-join-disabled': {'mutate': [off('    if receipt["inventoryDigest"] != M.commit_inventory(run_id, objects, blobs)[1]:\n')],
                                'run': 'semantic', 'faultLabels': {'wrong-inventory-otherwise-admitted', 'receipt-inventory-missing-a-published-object'}},
    'execution-plan-join-disabled': {'mutate': [off('    if binding["executionPlanId"] != execution_plan_id:\n')],
                                     'run': 'semantic', 'faultLabels': {'wrong-execution-plan-otherwise-admitted'}},
    'stage-count-join-disabled': {'mutate': [off('    if binding["stageCount"] != len(stages):\n')],
                                  'run': 'semantic', 'faultLabels': {'stage-count-not-the-execution-plans'}},
    'stage-progress-join-disabled': {'mutate': [(MODEL, '        _refuse("RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH")\n', '        pass\n')],
                                     'run': 'semantic', 'faultLabels': {'stages-completed-beyond-stage-count', 'first-failed-stage-outside-the-execution-plan'}},
    'v1-dispatch': {'restore': [SEC + 'carrier-dispatch.v3.json'], 'run': 'carrier',
                    'failPrefixes': ('source38 absent-carrier', 'source37 scenario: absent carrier'),
                    'mustFail': ('source38 absent-carrier totality', 'source38 absent-carrier law',
                                 'source37 scenario: absent carrier: an association (grantGeneration 1)')},
    'v1-prose': {'restore': [SEC + 'carrier-format.v3.md', 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
                             'docs/v2/architecture/commit-recovery-readonly.v3.md'], 'run': 'carrier',
                 'failPrefixes': ('source38 absent-carrier prose', 'source37 route: readOnlyRecovery/unknown-custody'),
                 'mustFail': ('source38 absent-carrier prose', 'source37 route: readOnlyRecovery/unknown-custody is exactly one S12 row')},
}

variant = sys.argv[1]
spec = VARIANTS[variant]
n, out = 1, BASE / 'receipts' / ('p05-' + variant)
while out.exists():
    n += 1
    out = BASE / 'receipts' / ('p05-%s.r%d' % (variant, n))
tree = BASE / 'work' / ('hybrid-' + variant + ('' if n == 1 else '.r%d' % n))
out.mkdir(parents=True)
shutil.copytree(BASE / 'work' / 'edited' / 'docs', tree / 'docs', copy_function=shutil.copy2)
changed = []
for rel in spec.get('restore', []):
    shutil.copy2(V1 / rel, tree / rel)
    changed.append({'restoredFromV1': rel})
for rel, old, new in spec.get('mutate', []):
    text = (tree / rel).read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise SystemExit('mutation anchor count %d in %s: %r' % (text.count(old), rel, old))
    (tree / rel).write_text(text.replace(old, new), encoding='utf-8')
    changed.append({'mutated': rel, 'anchor': old.strip()})
result = {'variant': variant, 'tree': str(tree), 'changed': changed}
if spec['run'] == 'semantic':
    p = subprocess.run([PY, '-I', '-B', str(tree / FND / 'check-semantic-replay.v3.py'), '--output', str(out)],
                       capture_output=True, text=True, timeout=3000, cwd=str(out))
    rep = json.loads((out / 'grok-native-replay.v1.json').read_text()) if (out / 'grok-native-replay.v1.json').exists() else {}
    rows = rep.get('checks', [])
    fail_rows = {r['case'] for r in rows if r.get('faults')} | set(rep.get('blocked', []))
    labels = set()
    for r in rows:
        if r.get('case') == COMP:
            labels = {f.split(':', 1)[0] for f in r.get('faults', [])}
    result.update(exit=p.returncode, failRows=sorted(fail_rows), faultLabels=sorted(labels), stderrTail=p.stderr[-1500:])
    ok = p.returncode != 0 and fail_rows == {COMP} and labels == spec['faultLabels']
else:
    p = subprocess.run([PY, '-I', '-B', str(tree / SEC / 'check-integrated-carrier.v1.py'), '--source', str(tree),
                        '--report', str(out / 'carrier.json')], capture_output=True, text=True, timeout=3000, cwd=str(out))
    rep = json.loads((out / 'carrier.json').read_text()) if (out / 'carrier.json').exists() else {}
    failed = [c['check'] for c in rep.get('checks', []) if not c['pass']]
    result.update(exit=p.returncode, passed=rep.get('passed'), failed=rep.get('failed'), failedChecks=failed, stderrTail=p.stderr[-1500:])
    ok = (p.returncode != 0 and bool(failed) and all(f.startswith(spec['failPrefixes']) for f in failed)
          and all(any(f.startswith(m) for f in failed) for m in spec['mustFail']))
result['expectationMet'] = ok
(out / 'result.json').write_text(json.dumps(result, indent=1) + '\n')
print(json.dumps(result, indent=1)[:8000])
sys.exit(0 if ok else 1)
