"""p14: pure-corpus truth table for the guard, using the model's OWN detail-None refusal
(workflows_model.v1.py:1539, repair_preview: 'target fingerprint not in the evidence Run').
No model patching. Emptying run['findings'] via the case's runOverride trips it.

Expected semantics of the correction:
  A. no 'refusal' key   (case expects success)      -> OLD pass (FALSE PASS), NEW fail
  B. 'refusal': null    (deliberate null expected)  -> OLD pass, NEW pass  (must stay legal)
  C. 'refusal': 'NAMED' (wrong named expectation)   -> OLD fail, NEW fail  (negative preserved)
  D. untouched corpus                               -> OLD pass, NEW pass  (no regression)
"""
import copy, json, os, re, shutil, subprocess

BASE = '/tmp/opensip-design-corrections/post-reset-review.v18'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
OLD_CHECKER = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
               'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py')
D = 'docs/coop/design-corrections/workflows/'
PY = '/tmp/opensip-architecture-review-env/bin/python'
FAIL_RE = re.compile(r'^FAIL (\S+)(?: (.*))?$')
TARGET = 'preview-applicable'
CID = 'repair.preview-applicable'


def run(work, checker, tag):
    shutil.copyfile(checker, os.path.join(work, D, 'check_workflows.v1.py'))
    p = subprocess.run([PY, '-I', '-B', os.path.join(D, 'check_workflows.v1.py'),
                        '--report', os.path.join(D, 'workflows-report.%s.json' % tag)],
                       cwd=work, capture_output=True, text=True)
    fails = {m.group(1): m.group(2) for m in (FAIL_RE.match(l) for l in p.stdout.splitlines()) if m}
    return {'exit': p.returncode, 'fails': fails, 'crashed': 'Traceback' in p.stderr,
            'stderrTail': p.stderr[-200:]}


base_cases = json.load(open(os.path.join(FROZEN, D, 'workflow-cases.v1.json')))

VARIANTS = {
    'A-no-refusal-key': {'runOverride': {'findings': []}},
    'B-explicit-null': {'runOverride': {'findings': []}, 'expect_refusal': (True, None)},
    'C-wrong-named': {'runOverride': {'findings': []}, 'expect_refusal': (True, 'REPAIR.SOURCE_MOVED')},
    'D-untouched': {},
}

rows = []
for vname, spec in VARIANTS.items():
    cases = copy.deepcopy(base_cases)
    if spec:
        for c in cases['repairScenario']['cases']:
            if c['id'] == TARGET:
                if 'runOverride' in spec:
                    c['runOverride'] = spec['runOverride']
                if 'expect_refusal' in spec:
                    c['expect']['refusal'] = spec['expect_refusal'][1]
                break
    work = os.path.join(BASE, 'controls-v2', 'truth-' + vname)
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(FROZEN, work)
    json.dump(cases, open(os.path.join(work, D, 'workflow-cases.v1.json'), 'w'), indent=1)
    old, new = run(work, OLD_CHECKER, 'old'), run(work, os.path.join(FROZEN, D, 'check_workflows.v1.py'), 'new')
    old_fail = CID in old['fails']
    new_fail = CID in new['fails']
    rows.append({'variant': vname, 'oldCrashed': old['crashed'], 'newCrashed': new['crashed'],
                 'oldVerdictOnTarget': 'FAIL' if old_fail else 'PASS',
                 'newVerdictOnTarget': 'FAIL' if new_fail else 'PASS',
                 'oldTotalFails': len(old['fails']), 'newTotalFails': len(new['fails']),
                 'oldExit': old['exit'], 'newExit': new['exit'],
                 'newDetailShown': new['fails'].get(CID)})
    print('%-20s OLD=%-4s NEW=%-4s  oldFails=%-3d newFails=%-3d  oldExit=%s newExit=%s'
          % (vname, rows[-1]['oldVerdictOnTarget'], rows[-1]['newVerdictOnTarget'],
             len(old['fails']), len(new['fails']), old['exit'], new['exit']))

expected = {'A-no-refusal-key': ('PASS', 'FAIL'), 'B-explicit-null': ('PASS', 'PASS'),
            'C-wrong-named': ('FAIL', 'FAIL'), 'D-untouched': ('PASS', 'PASS')}
ok = all((r['oldVerdictOnTarget'], r['newVerdictOnTarget']) == expected[r['variant']] for r in rows)
print('\ntruthTableMatchesIntendedSemantics =', ok)
for r in rows:
    e = expected[r['variant']]
    print('  %-20s expected old=%s new=%s -> got old=%s new=%s %s'
          % (r['variant'], e[0], e[1], r['oldVerdictOnTarget'], r['newVerdictOnTarget'],
             'OK' if (r['oldVerdictOnTarget'], r['newVerdictOnTarget']) == e else 'MISMATCH'))
json.dump({'rows': rows, 'expected': expected, 'allMatch': ok},
          open(os.path.join(BASE, 'logs', 'p14-null-semantics.json'), 'w'), indent=1)
