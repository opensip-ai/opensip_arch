"""P09 — independently verify on FINAL33 that the optional missing-result / candidate path is
reachable and closes without a required execution deficiency, and that candidate refs exist only
when an envelope exists. Root's assessment is bound to source32 and an author draft; this is 33."""
import json, os, re, subprocess

PY = '/tmp/opensip-architecture-review-env/bin/python'
KIT = '/tmp/opensip-design-corrections/claude-independent-design.v33/disposable/kit33'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
p = os.path.join(KIT, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True, cwd=os.path.dirname(p))
d = json.loads(r.stdout)
cases = d['cases']
R = {'sourceVersion': 'final frozen33', 'totalCases': len(cases)}


def rows(pred):
    return [c for c in cases if pred(c)]


opt = rows(lambda c: 'optional' in c['case'])
R['optionalCases'] = [{'case': c['case'], 'result': c['result'],
                       'derivedAccountStates': c.get('derivedAccountStates'),
                       'derivedOutcomeStates': c.get('derivedOutcomeStates'),
                       'deficiencyCauses': c.get('deficiencyCauses'),
                       'fullRunVerdict': (c.get('fullRun') or {}).get('verdict'),
                       'fullRunId': (c.get('fullRun') or {}).get('runId'),
                       'fullRunCausePairs': (c.get('fullRun') or {}).get('executionCausePairs')}
                      for c in opt]
print('=== optional-path cases on final33 (%d) ===' % len(opt))
for x in R['optionalCases']:
    print('\n%s' % x['case'])
    print('   result=%s outcomes=%s' % (x['result'], json.dumps(x['derivedOutcomeStates'])))
    print('   accountStates=%s' % json.dumps(x['derivedAccountStates']))
    print('   deficiencyCauses=%s' % json.dumps(x['deficiencyCauses']))
    if x['fullRunId']:
        print('   FULL RUN %s verdict=%s causes=%s'
              % (x['fullRunId'][:34], x['fullRunVerdict'], json.dumps(x['fullRunCausePairs'])))

R['optionalFullRunClosesWithoutRequiredDeficiency'] = any(
    x['fullRunId'] and x['fullRunVerdict'] == 'pass' and x['fullRunCausePairs'] == []
    for x in R['optionalCases'])
print('\noptional path reaches a FULL RUN that closes pass with no execution deficiency:',
      R['optionalFullRunClosesWithoutRequiredDeficiency'])

cand = rows(lambda c: 'candidate' in c['case'])
R['candidateCases'] = [{'case': c['case'], 'result': c['result'], 'refusals': c.get('refusals'),
                        'derivedOutcomeStates': c.get('derivedOutcomeStates')} for c in cand]
print('\n=== candidate cases on final33 (%d) ===' % len(cand))
for x in R['candidateCases']:
    print('   %-56s %-7s %s' % (x['case'][:56], x['result'], json.dumps(x['refusals'])[:90]))
R['requiredCandidateAbsentEnvelopeRefuses'] = any(
    x['case'] == 'required-candidate-absent-envelope-still-refuses' and x['result'] == 'REFUSE'
    for x in R['candidateCases'])
R['extraCandidateRefWithoutOutcomeRefuses'] = any(
    'extra-candidate-ref' in x['case'] and x['result'] == 'REFUSE' for x in R['candidateCases'])
print('\nrequired candidate with NO envelope refuses           :', R['requiredCandidateAbsentEnvelopeRefuses'])
print('candidate ref without a matching outcome refuses      :', R['extraCandidateRefWithoutOutcomeRefuses'])
R['candidateRefsOnlyWhenEnvelopeExists'] = (R['requiredCandidateAbsentEnvelopeRefuses']
                                            and R['extraCandidateRefWithoutOutcomeRefuses'])

R['assessment'] = (
    'On FINAL33 the optional path is full-Run reachable: '
    'full-run-optional-unselected-and-optional-unsupported-close-without-execution-deficiency is an '
    'admitted Run with verdict pass and an EMPTY executionCausePairs, so an optional unselected or '
    'unsupported cell closes without owing a required execution deficiency. The candidate leg is '
    'controlled in both directions: a required cell with no retained envelope refuses '
    'EXECUTION_INPUTS_CANDIDATE_REQUIRED before the bridge, and a candidate ref without a matching '
    'outcome refuses, so candidate refs exist only when an envelope exists. Root\'s own reachability '
    'assessment is bound to source32 and an author draft; this verification is on final33 and does '
    'not depend on it. These remain reference fixtures, not provider qualification.')
print('\n' + R['assessment'])
json.dump(R, open(os.path.join(OUT, 'p09-optional33.json'), 'w'), indent=1, default=str)
print('\nwrote p09-optional33.json')
