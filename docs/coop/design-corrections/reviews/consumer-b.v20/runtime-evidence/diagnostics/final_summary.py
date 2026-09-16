"""Print the final reconciliation summary from the exported bytes only."""
import hashlib
import json
import os

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'


def J(rel):
    with open(os.path.join(OUT, rel), encoding='utf-8') as fh:
        return json.load(fh)


def sha(rel):
    with open(os.path.join(OUT, rel), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


d = J('blind-review.json')
v = J('verify-all.json')
h = J('helper-corrections.json')
s = J('requirement-status.json')

print('verdict                 : %s' % d['verdict'])
print('command                 : %s' % d['fromScratchCommand']['command'])
print('stages                  : declared %s / recorded %s / failed %s'
      % (v['declaredStageCount'], v['stagesRecorded'],
         sum(1 for st in v['stages'] if st.get('exit'))))
print('kit                     : %s / %s rows verified, manifest %s'
      % (d['inputKit']['filesVerifiedPass'], d['inputKit']['fileCount'],
         d['inputKit']['subjectManifestSha256'][:16]))
delta = d['inputKit']['measuredDeltaAgainstThePriorDisclosedKit']
print('measured delta          : %s unchanged / %s changed / %s added / %s withdrawn'
      % (delta['unchangedCount'], delta['changedCount'], delta['addedCount'],
         len(delta.get('withdrawn') or [])))
print('ancestry                : %s' % ' -> '.join(d['sameOriginAncestry']))
print('requirement status      : %s'
      % ', '.join('%s %s' % kv for kv in sorted(d['requirementStatus']['counts'].items())))
print('MUST / SHOULD / advisory: %s / %s / %s'
      % (len(d['newMustIssues']), len(d['newShouldIssues']), len(d['advisories'])))
print('helper rows / open      : %s / %s %s'
      % (len(h['helperCorrections']), len(h['openHelperFailuresOnAClaimedPositive']),
         h['openHelperFailuresOnAClaimedPositive']))
print('helper record consumerId: %s' % h['consumerId'])
print('history standing        : %s' % d['standing']['historyStanding'])
print('label provenance        : %s' % d['standing']['generationLabelProvenance']['verdict'])
print('artifact digest rows    : %s' % len(d['retainedArtifactDigests']))
print('complete positives      : %s'
      % ', '.join('%s(%s checks)' % (p.get('runLabel') or p.get('label'),
                                     p.get('closure', {}).get('checksPassed'))
                  for p in d['claimedCompletePositives']))
print('query surface           : %s ops, %s checks, %s refusals, %s controls'
      % (J('query/indep-query-surface.json')['operationCount'],
         len(J('query/indep-query-surface.json')['checks']),
         len(J('query/indep-query-surface.json')['refusals']),
         len(J('query/indep-query-surface.json')['negativeControls'])))
print('mutation surface        : %s checks, %s refusals, %s controls'
      % (len(J('vectors/indep-mutation-surface.json')['checks']),
         len(J('vectors/indep-mutation-surface.json')['refusals']),
         len(J('vectors/indep-mutation-surface.json')['negativeControls'])))
print('blind-review.md  sha256 : %s' % sha('blind-review.md'))
print('blind-review.json sha256: %s' % sha('blind-review.json'))
