"""p06: expectations over p02 (batteries + actual checker), p03 (root probe) and p04 (semantic replay). Reads receipts only.

The unrelated oc2 policy-test grammar failure is expected in EVERY checker run and is never counted as a pass.
Output: receipts/p06-compare.json.
"""
import json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1')
R = BASE / 'receipts'
load = lambda n: json.loads((R / n).read_text())
OC2 = 'oc2-owner-string-expression-case-is-policy-imperative-key-refused'
NEW_NEGATIVE = {
    'oc1-same-retained-closure-and-plan-with-another-run3-id-refuses-before-descriptor',
    'oc1-admitted-dyn-run-id-over-the-positive-run-closure-refuses-before-descriptor',
    'oc1-positive-run-id-over-the-admitted-dyn-run-closure-refuses-before-descriptor',
    'oc1-admitted-neg-run-id-over-the-positive-run-closure-refuses-before-descriptor',
    'oc1-positive-run-id-over-the-admitted-neg-run-closure-refuses-before-descriptor',
    'oc1-each-selection-instance-view-declares-its-own-unavailability-class',
    'oc1-declared-missing-retained-subject-maps-typed-for-a-reference-instance-view',
    'oc1-foreign-same-name-exception-from-matched-findings-propagates-as-the-same-object',
    'oc1-an-undeclared-view-raising-a-separate-owner-instance-class-is-not-normalized',
}
checks = {}


def ck(name, ok, detail=None):
    checks[name] = {'ok': bool(ok), **({'detail': detail} if detail is not None else {})}


base, src, hyb = load('p02-baseline.json'), load('p02-source.json'), load('p02-hybrid-baseline-owner.json')
ck('baseline checker: 795 checks, exit 1, only the unrelated oc2 failure', base['checker']['count'] == 795 and base['checker']['exit'] == 1
   and base['checker']['failed'] == [OC2], base['checker']['failed'])
new_ids = {c['id'] for c in json.loads((R / 'p02-source-checker-stdout.json').read_text())['results']} - \
          {c['id'] for c in json.loads((R / 'p02-baseline-checker-stdout.json').read_text())['results']}
ck('edited checker: exactly 19 new controls, all pass; exit 1 only for the unrelated oc2 failure',
   src['checker']['count'] == 814 and len(new_ids) == 19 and src['checker']['exit'] == 1 and src['checker']['failed'] == [OC2],
   {'count': src['checker']['count'], 'new': sorted(new_ids), 'failed': src['checker']['failed']})
ck('hybrid (baseline owner files + edited checker): fails exactly oc2 + the 9 new negative controls',
   set(hyb['checker']['failed']) == NEW_NEGATIVE | {OC2} and hyb['checker']['count'] == 814,
   {'failed': hyb['checker']['failed'], 'details': hyb['checker']['failedDetails']})
ck('edited checker loaded from the edited tree; hybrid from the hybrid tree',
   src['checker']['loadedChecker'].startswith(str((BASE / 'work/source').resolve())) and hyb['checker']['loadedChecker'].startswith(str((BASE / 'work/hybrid-baseline-owner').resolve())))
for label, doc in (('baseline', base), ('source', src)):
    f = doc['facts']
    ck('%s facts: cw_pos re-admitted by a separate close_run, identifier equal, reference selection separate, dyn and neg share the Plan and re-admit' % label,
       f['closeRunEqualsAdapterRunId'] and f['identifierEqualsAdapterRunId'] and f['referenceSelectionIsASeparateModuleInstance']
       and f['runsSharingThePosPlan'] == ['dyn', 'neg'] and f['secondRun']['closeRunReadmits'] and f['secondRun']['evidenceDiffers'], f)
C = {c['label']: c for c in src['calls']}
B = {c['label']: c for c in base['calls']}
refuse = lambda c, calls, cause=None: c['outcome'] == 'REFUSE' and c['errorCode'] == 'REQUEST.PRECONDITION_FAILED' and c['detail'] == 'REPAIR.EVIDENCE_RUN_UNAVAILABLE' and c['sharedBuilderCalls'] == calls and c['cause'] == cause
exact = lambda c: c['outcome'] == 'PROPAGATE' and c['exactObject'] is True
ck('edited: lawful preview ADMIT names the actual run id, identical plan to baseline',
   C['lawful']['outcome'] == 'ADMIT' and C['lawful']['evidenceRunId'] == src['facts']['runs']['pos']['runId'] and C['lawful']['repairPlanId'] == B['lawful']['repairPlanId'])
ck('edited: arbitrary wrong run3 id refuses before any descriptor (baseline ADMIT)',
   refuse(C['same-retained-closure-and-plan-arbitrary-wrong-run3-id'], 0) and B['same-retained-closure-and-plan-arbitrary-wrong-run3-id']['outcome'] == 'ADMIT')
ck('edited: second admitted Run own preview ADMIT; both cross substitutions refuse before descriptor (baseline both ADMIT)',
   C['second-admitted-run-own-lawful-preview']['outcome'] == 'ADMIT'
   and C['second-admitted-run-own-lawful-preview']['repairPlanId'] == B['second-admitted-run-own-lawful-preview']['repairPlanId']
   and refuse(C['second-admitted-run-id-with-first-run-retained-closure-shared-plan'], 0)
   and refuse(C['first-run-id-with-second-admitted-run-retained-closure-shared-plan'], 0)
   and B['second-admitted-run-id-with-first-run-retained-closure-shared-plan']['outcome'] == 'ADMIT'
   and B['first-run-id-with-second-admitted-run-retained-closure-shared-plan']['outcome'] == 'ADMIT')
ck('edited: another Plan still refuses before descriptor', refuse(C['retained-closure-of-another-plan-still-refuses'], 0))
ck('edited: declared missing finding maps typed for both instances, cause is that instance class, before descriptor',
   refuse(C['declared-missing-finding-record-reference-instance-view'], 0, 'reference-selection-instance-class')
   and refuse(C['declared-missing-finding-record-owner-instance-view'], 0, 'owner-selection-instance-class'))
ck('edited: declared missing subject in the selector maps typed for both instances (baseline reference instance escaped untyped)',
   refuse(C['declared-missing-subject-records-selector-path-reference-instance-view'], 1, 'reference-selection-instance-class')
   and refuse(C['declared-missing-subject-records-selector-path-owner-instance-view'], 1, 'owner-selection-instance-class')
   and B['declared-missing-subject-records-selector-path-reference-instance-view']['outcome'] == 'PROPAGATE')
ck('edited: foreign same-name exception propagates as the exact object from both read sites (baseline misrouted matched_findings)',
   exact(C['foreign-same-name-exception-from-matched_findings']) and C['foreign-same-name-exception-from-matched_findings']['injectedCalled']
   and exact(C['foreign-same-name-exception-from-coverage_records']) and C['foreign-same-name-exception-from-coverage_records']['injectedCalled']
   and B['foreign-same-name-exception-from-matched_findings']['outcome'] == 'REFUSE')
ck('edited: host OSError propagates as the exact object', exact(C['host-oserror-from-matched_findings']))
ck('edited: undeclared stub raising a separate-instance class propagates (baseline normalized it by name)',
   exact(C['undeclared-stub-adapter-raising-the-reference-class']) and B['undeclared-stub-adapter-raising-the-reference-class']['outcome'] == 'REFUSE')
ck('author files stable during every battery', base['stable'] and src['stable'] and hyb['stable'])
rp_b, rp_s = load('p03-rootprobe-baseline.json'), load('p03-rootprobe-source.json')
rb = {c['label']: c for c in rp_b['report']['calls']}
rs = {c['label']: c for c in rp_s['report']['calls']}
root_report = json.loads(Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2/report.json').read_text())
ck('root probe on the baseline copy reproduces root report calls and checker stdout bytes',
   rp_b['report']['calls'] == root_report['calls'] and rp_b['checker']['stdoutSha256'] == json.loads((R / 'p00-copy.json').read_text())['rootInputs']['checker-stdout.json'])
ck('root probe on the edited tree: lawful ADMIT unchanged; wrong run id REFUSE unavailable; foreign same-name exception propagates (not a Refusal)',
   rs['lawful'] == rb['lawful']
   and rs['same-retained-closure-and-plan-but-wrong-run-id']['outcome'] == 'REFUSE'
   and rs['same-retained-closure-and-plan-but-wrong-run-id']['errorCode'] == 'REQUEST.PRECONDITION_FAILED'
   and rs['same-retained-closure-and-plan-but-wrong-run-id']['detail'] == 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'
   and rs['foreign-same-name-host-exception']['class'] == 'RetainedEvidenceUnavailable' and rs['foreign-same-name-host-exception']['errorCode'] is None
   and rp_s['report']['checkerExit'] == 1 and [c['id'] for c in rp_s['checker']['failed']] == [OC2], rs)
sb, ss = load('p04-semantic-baseline.json'), load('p04-semantic-source.json')
ck('semantic golden replay: baseline and edited pass, 31, none blocked',
   all(d['exit'] == 0 and d['passed'] is True and d['count'] == 31 and d['blocked'] == [] for d in (sb, ss)) and sb['checkerSha256'] == ss['checkerSha256'])
out = {'checks': checks, 'allOk': all(c['ok'] for c in checks.values())}
(R / 'p06-compare.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1)[:20000])
sys.exit(0 if out['allOk'] else 1)
