"""MY OWN discriminating injection, not root's expected output.

`repair_preview` raises Refusal('REQUEST.PRECONDITION_FAILED', None, 'target fingerprint not in the
evidence Run', t) - a DETAIL-FREE refusal on a real product path. I take `preview-applicable`, a case
that expects SUCCESS and carries no `refusal` key, and override the evidence Run's findings to empty
so that refusal fires. Under the frozen checker `exp.get('refusal')` is None and `r.detail` is None,
so the check PASSES although an unexpected refusal occurred. Under the proposal it must FAIL.

Limit: this mutates the CASE CORPUS in a throwaway tree to force a real model refusal. It is a
harness-level injection, not evidence about any product Run, host or admission."""
import json, pathlib, shutil, subprocess, sys
BASE = pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v17')
OUT = pathlib.Path('/tmp/opensip-design-corrections/v18-checker-coauthor.v1')
PROPOSED = OUT.parent / 'v18-checker-proposal.v1/proposal/docs/coop/design-corrections/workflows/check_workflows.v1.py'
CASE_ID = 'preview-applicable'
results = {}
for label, checker in (('frozen', None), ('proposed', PROPOSED)):
    tree = OUT / 'work-injected' / label
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(['rsync', '-a', '--exclude=docs/coop/design-corrections/reviews/',
                    str(BASE) + '/', str(tree) + '/'], check=True)
    for p in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md',
              'workflows-author-feedback.v1.md'):
        s = BASE / 'docs/coop/design-corrections/reviews' / p
        d = tree / 'docs/coop/design-corrections/reviews' / p
        d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(s, d)
    cp = tree / 'docs/coop/design-corrections/workflows/workflow-cases.v1.json'
    doc = json.loads(cp.read_text())
    case = next(c for c in doc['repairScenario']['cases'] if c['id'] == CASE_ID)
    assert 'refusal' not in case['expect'], 'injection target must expect success'
    case['runOverride'] = {'findings': []}          # forces the detail-free refusal
    cp.write_text(json.dumps(doc, indent=2) + '\n')
    if checker:
        shutil.copy2(checker, tree / 'docs/coop/design-corrections/workflows/check_workflows.v1.py')
    rep = OUT / 'evidence' / ('report.injected.%s.json' % label)
    r = subprocess.run(['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B',
                        'check_workflows.v1.py', '--report', str(rep)],
                       cwd=str(tree / 'docs/coop/design-corrections/workflows'),
                       capture_output=True, text=True)
    data = json.loads(rep.read_text())
    failed = [f['id'] for f in data['failed']]
    results[label] = {'checks': data['checkCount'], 'passed': data['passed'],
                      'failedCount': len(failed),
                      'injectedCaseFailed': any(f == 'repair.' + CASE_ID for f in failed),
                      'failedIds': failed[:8]}
print(json.dumps({'standing': __doc__, 'injectedCase': CASE_ID,
                  'injection': "runOverride.findings = [] so the target fingerprint is absent from "
                               "the evidence Run, raising a detail-free refusal on a real path",
                  'results': results,
                  'discriminates': results['frozen']['injectedCaseFailed'] is False
                                   and results['proposed']['injectedCaseFailed'] is True},
                 indent=1))
