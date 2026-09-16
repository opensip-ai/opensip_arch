"""output/progress.v20.json -- written from the artifacts that exist right now."""
import collections
import json

OUT = '/tmp/opensip-design-corrections/consumer-b.' + 'v20' + '/output'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def main():
    cust = J('notes/v20-input-custody.json') or {}
    runs = J('runs/all-runs-summary.json') or []
    gaps = J('vectors/phase10-design-gaps.json') or {}
    helpers = J('helper-corrections.json') or {}
    verify = J('verify-all.json') or {}
    status = J('requirement-status.json') or {}
    hist = J('notes/v20-history-standing.json') or {}
    area3 = J('vectors/indep-execution-inputs.json') or {}
    ei_ctl = J('vectors/execution-inputs-negative-controls.json') or {}
    qs = J('query/indep-query-surface.json') or {}
    ms = J('vectors/indep-mutation-surface.json') or {}
    counts = collections.Counter(v['status'] for v in status.values())
    doc = {
        'consumerId': 'consumer-b.' + 'v20',
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'sameOriginAncestry': ['consumer-b' + '.v14', 'consumer-b' + '.v15',
                               'consumer-b' + '.v16', 'consumer-b' + '.v17',
                               'consumer-b' + '.v18', 'consumer-b' + '.v19',
                               'consumer-b' + '.v20'],
        'notANewOrigin': ('a continuation of the SAME blind origin. No earlier generation is '
                          'retroactively accepted by this one, and no root verdict is known.'),
        'inputCustody': {
            'manifestSha256': (cust.get('claim1_manifestOwnBytes') or {}).get('measured'),
            'declaredParentBinding': (cust.get('claim2_declaredParentBinding')
                                      or {}).get('declared'),
            'rowsVerified': (cust.get('claim3_everyRowVerified') or {}).get('filesVerified'),
            'measuredDelta': {k: (cust.get('claim4_normativeDeltaMeasuredHere') or {}).get(k)
                              for k in ('unchangedCount', 'changedCount', 'addedCount',
                                        'changed')},
            'suppliedInventoryVerified': (cust.get('claim5_suppliedInventoryVerified')
                                          or {}).get('result'),
        },
        'newNormativeWorkThisGeneration': {
            'executionInputsReconciliation': [
                'applicability is the published FIRST-MATCH precedence keyed on the cell matrix '
                'state, with unsupported-typed ahead of both unavailable tokens',
                'sourceUniverse is the binding coordinate for EVERY applicability (external join)',
                'the owed accounts and the cross-source carrier order come from the matrix '
                'relations array AS AUTHORED',
                'the carrier is the first source ACTUALLY CARRYING a typed pair; pure missing '
                'work is explicitly (null, null) and never provider-unavailable',
                'an UNSUPPORTED-TYPED cell may lawfully have returned Coverage its account does '
                'not name, and such an account is ANSWERED',
                'the required-execution bridge is per SOURCE, per the new composition table, and '
                'a required unsupported-typed cell contributes even when its row is complete'],
            'area3Independent': {'refusals': area3.get('totalRefusals'),
                                 'perRunChecksPassed': {k: v.get('passed') for k, v
                                                        in (area3.get('runs') or {}).items()},
                                 'controls': len(ei_ctl.get('controls') or [])},
            'querySurface': {'operations': qs.get('operationCount'),
                             'checks': len(qs.get('checks') or []),
                             'refusals': len(qs.get('refusals') or []),
                             'controls': len(qs.get('negativeControls') or [])},
            'mutationSurface': {'checks': len(ms.get('checks') or []),
                                'refusals': len(ms.get('refusals') or []),
                                'controls': len(ms.get('negativeControls') or [])},
        },
        'runs': runs,
        'requirementStatus': dict(counts),
        'designGaps': {'must': len(gaps.get('newMustIssues') or []),
                       'should': len(gaps.get('newShouldIssues') or []),
                       'advisories': len(gaps.get('advisories') or []),
                       'stillOpen': [s['id'] for s in (gaps.get('newShouldIssues') or [])]},
        'fromScratch': {
            'declaredStageCount': verify.get('declaredStageCount'),
            'stagesRecordedWhenThisStageRan': len(verify.get('stages') or []),
            'allStagesPassed': verify.get('allStagesPassed'),
            'standing': ('verify-all.json is rewritten after every stage; this record is written '
                         'by the progress stage, which runs before the final reconciliation '
                         'stage.')},
        'historyStanding': {'state': hist.get('state'),
                            'carriedDisclosure': (
                                hist.get('carriedDisclosure_generation16NoteOverwrites')
                                or {}).get('status'),
                            'generationsModifiedThisSession': (
                                (hist.get('measuredC_priorGenerations') or {})
                                .get('generationsModifiedDuringThisSession'))},
        'openHelperFailures': helpers.get('openHelperFailuresOnAClaimedPositive'),
        'verdict': (J('blind-review.json') or {}).get('verdict'),
        'noProductChange': ('no product implementation, kit edit, repository mutation, commit, '
                            'push, real repair, baseline adoption or product qualification'),
    }
    with open(OUT + '/progress.v20.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    print('progress.v20.json written | verdict %s | status %s | stages %s | openHelpers %s'
          % (doc['verdict'], dict(counts), doc['fromScratch'], doc['openHelperFailures']))


main()
