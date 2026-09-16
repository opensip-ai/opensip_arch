"""p03 <variant>: discrimination controls on a hybrid regular copy of work/edited (never the edited tree itself).

Each variant restores baseline bytes or applies one asserted mutation, runs only the owner validator it concerns,
and checks that exactly the expected controls fail. Reports: receipts/p03-<variant>[.rN]/. Hybrid trees:
work/hybrid-<variant>[.rN]/ (regular copies, disposable).
"""
import json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
PY = '/tmp/opensip-architecture-review-env/bin/python'
FND = 'docs/coop/design-corrections/foundation/'
SEC = 'docs/coop/design-corrections/security/'
MODEL = FND + 'run_termination_model.v1.py'
COMP = 'run-termination:host-composition-boundary'
OUTSIDE = {'operational-required-delivery-after-commit', 'operational-host-invariant', 'interrupted-before-settle',
           'request-rejected-ephemeral-authority'}
VARIANTS = {
    'model-baseline': {'restore': [MODEL], 'run': 'semantic', 'failRows': {COMP}, 'faultLabels': None},
    'detail-law-disabled': {'mutate': [(MODEL, '        if detail["code"] != want:\n', '        if False:\n')], 'run': 'semantic',
                            'failRows': {COMP},
                            'faultLabels': {'unrelated-host-invariant-detail', 'unrelated-query-detail', 'unrelated-doctor-detail',
                                            'work-budget-detail-without-retained-work-budget',
                                            'work-budget-detail-when-work-budget-is-secondary',
                                            'closure-detail-without-installation-observation', 'closure-detail-over-budget-primary',
                                            'detail-on-verdict-run'}},
    'attempt-join-disabled': {'mutate': [(MODEL, '    if receipt["executionId"] != terminating["executionId"]:\n', '    if False:\n')],
                              'run': 'semantic', 'failRows': {COMP}, 'faultLabels': {'run-committed-by-another-attempt'}},
    'execution-id-law-disabled': {'mutate': [(MODEL, '    if execution_id is not None and execution_id != terminating["executionId"]:\n'
                                                     '        _refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")\n    want =',
                                              '    if False:\n        _refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")\n    want =')],
                                  'run': 'semantic', 'failRows': {COMP},
                                  'faultLabels': {'earlier-retried-attempt-attribution', 'foreign-attempt-attribution'}},
    'outside-forced-through-derivation': {'mutate': [(MODEL, '    if candidate.get("class") in OUTSIDE_ANALYSIS_PROJECTION:\n'
                                                             '        return {"standing": "outside-analysis-projection", '
                                                             '"owner": OUTSIDE_ANALYSIS_PROJECTION[candidate["class"]]}\n', '')],
                                          'run': 'semantic', 'failRows': {COMP}, 'faultLabels': OUTSIDE},
    'dispatch-baseline': {'restore': [SEC + 'carrier-dispatch.v3.json'], 'run': 'carrier',
                          'failPrefixes': ('source38 ADV38-02', 'source37 scenario: ADV38-02'),
                          'mustFail': ('source38 ADV38-02 map', 'source38 ADV38-02 law',
                                       'source37 scenario: ADV38-02: an association (grantGeneration 1)')},
    'prose-baseline': {'restore': [SEC + 'carrier-format.v3.md', 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
                                   'docs/v2/architecture/commit-recovery-readonly.v3.md'], 'run': 'carrier',
                       'failPrefixes': ('source38 ADV38-02 prose', 'source38 ADV38-03 prose'),
                       'mustFail': ('source38 ADV38-02 prose', 'source38 ADV38-03 prose')},
}

variant = sys.argv[1]
spec = VARIANTS[variant]
n, out = 1, BASE / 'receipts' / ('p03-' + variant)
while out.exists():
    n += 1
    out = BASE / 'receipts' / ('p03-%s.r%d' % (variant, n))
tree = BASE / 'work' / ('hybrid-' + variant + ('' if n == 1 else '.r%d' % n))
out.mkdir(parents=True)
shutil.copytree(BASE / 'work' / 'edited' / 'docs', tree / 'docs', copy_function=shutil.copy2)
changed = []
for rel in spec.get('restore', []):
    shutil.copy2(BASE / 'work' / 'baseline' / rel, tree / rel)
    changed.append({'restored': rel})
for rel, old, new in spec.get('mutate', []):
    text = (tree / rel).read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise SystemExit('mutation anchor count %d in %s' % (text.count(old), rel))
    (tree / rel).write_text(text.replace(old, new), encoding='utf-8')
    changed.append({'mutated': rel, 'anchor': old[:80]})
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
    ok = p.returncode != 0 and fail_rows == spec['failRows'] and (spec['faultLabels'] is None or labels == spec['faultLabels'])
    if spec['faultLabels'] is None:
        comp = [r for r in rows if r.get('case') == COMP]
        ok = ok and bool(comp) and bool(comp[0].get('faults'))
else:
    p = subprocess.run([PY, '-I', '-B', str(tree / SEC / 'check-integrated-carrier.v1.py'), '--source', str(tree),
                        '--report', str(out / 'carrier.json')], capture_output=True, text=True, timeout=3000, cwd=str(out))
    rep = json.loads((out / 'carrier.json').read_text()) if (out / 'carrier.json').exists() else {}
    failed = [c['check'] for c in rep.get('checks', []) if not c['pass']]
    result.update(exit=p.returncode, passed=rep.get('passed'), failed=rep.get('failed'), failedChecks=failed,
                  stderrTail=p.stderr[-1500:])
    ok = (p.returncode != 0 and bool(failed) and all(f.startswith(spec['failPrefixes']) for f in failed)
          and all(any(f.startswith(m) for f in failed) for m in spec['mustFail']))
result['expectationMet'] = ok
(out / 'result.json').write_text(json.dumps(result, indent=1) + '\n')
print(json.dumps(result, indent=1)[:8000])
sys.exit(0 if ok else 1)
