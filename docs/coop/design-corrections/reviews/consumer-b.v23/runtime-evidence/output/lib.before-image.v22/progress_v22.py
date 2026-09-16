"""output/progress.v22.json -- written from the artifacts that exist right now."""
import collections
import json

OUT = '/tmp/opensip-design-corrections/consumer-b.' + 'v22' + '/output'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def main():
    cust = J('notes/v22-input-custody.json') or {}
    gaps = J('vectors/phase10-design-gaps.json') or {}
    helpers = J('helper-corrections.json') or {}
    verify = J('verify-all.json') or {}
    status = J('requirement-status.json') or {}
    hist = J('notes/v22-history-standing.json') or {}
    atom = J('vectors/indep-atom-law.json') or {}
    audit = J('vectors/claimed-positive-audit.json') or {}
    counts = collections.Counter(v['status'] for v in status.values())
    doc = {
        'consumerId': 'consumer-b.' + 'v22',
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'sameOriginAncestry': ['consumer-b' + '.v14', 'consumer-b' + '.v15',
                               'consumer-b' + '.v16', 'consumer-b' + '.v17',
                               'consumer-b' + '.v18', 'consumer-b' + '.v19',
                               'consumer-b' + '.v20', 'consumer-b' + '.v22'],
        'generation21': 'prepared by the launcher and never run; no result exists',
        'notANewOrigin': ('a continuation of the SAME blind origin. No earlier generation is '
                          'retroactively accepted by this one, and no root verdict is known.'),
        'inputCustody': {
            'manifestSha256': (cust.get('claim1_manifestOwnBytes') or {}).get('measured'),
            'declaredParentBinding': (cust.get('claim2_declaredParentBinding') or {}).get('declared'),
            'rowsVerified': (cust.get('claim3_everyRowVerified') or {}).get('filesVerified'),
            'measuredDelta': {k: (cust.get('claim4_normativeDeltaMeasuredHere') or {}).get(k)
                              for k in ('unchangedCount', 'changedCount', 'addedCount', 'changed')},
            'custodyGaps': (cust.get('custody') or {}).get('custodyGaps')},
        'atomLaw': {'summary': atom.get('summary'),
                    'minResolutionCrossCheckCases': len(atom.get('minResolutionAtomLevelCrossCheck') or [])},
        'claimedPositiveAudit': {'counts': audit.get('counts'),
                                 'evidenceClassCounts': audit.get('evidenceClassCounts')},
        'requirementStatus': dict(counts),
        'designGaps': {'must': len(gaps.get('newMustIssues') or []),
                       'should': len(gaps.get('newShouldIssues') or []),
                       'advisories': len(gaps.get('advisories') or [])},
        'fromScratch': {'declaredStageCount': verify.get('declaredStageCount'),
                        'stagesRecordedWhenThisStageRan': len(verify.get('stages') or []),
                        'readOrderViolations': (verify.get('readOrderGuard') or {}).get('violations')},
        'historyStanding': {'state': hist.get('state'),
                            'generationsModifiedThisSession': (
                                (hist.get('measuredC_priorGenerations') or {})
                                .get('generationsModifiedDuringThisSession'))},
        'openHelperFailures': helpers.get('openHelperFailuresOnAClaimedPositive'),
        'verdict': (J('blind-review.json') or {}).get('verdict'),
        'noProductChange': ('no product implementation, kit edit, repository mutation, commit, '
                            'push, real repair, baseline adoption or product qualification'),
    }
    with open(OUT + '/progress.v22.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    print('progress.v22.json written | verdict %s | status %s | audit %s'
          % (doc['verdict'], dict(counts), doc['claimedPositiveAudit']['counts']))


main()
