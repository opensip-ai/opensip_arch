"""output/progress.v19.json -- written from the artifacts that exist right now."""
import collections
import json

OUT = '/tmp/opensip-design-corrections/consumer-b.' + 'v19' + '/output'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def main():
    cust = J('notes/v19-input-custody.json') or {}
    runs = J('runs/all-runs-summary.json') or []
    gaps = J('vectors/phase10-design-gaps.json') or {}
    helpers = J('helper-corrections.json') or {}
    verify = J('verify-all.json') or {}
    status = J('requirement-status.json') or {}
    hist = J('notes/v19-history-standing.json') or {}
    counts = collections.Counter(v['status'] for v in status.values())
    area3 = J('vectors/indep-execution-inputs.json') or {}
    glob = J('vectors/glob-law.json') or {}
    sel = J('vectors/repair-closed-world-selection.json') or {}
    ei_ctl = J('vectors/execution-inputs-negative-controls.json') or {}
    doc = {
        'consumerId': 'consumer-b.' + 'v19',
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'sameOriginAncestry': ['consumer-b' + '.v14', 'consumer-b' + '.v15',
                               'consumer-b' + '.v16', 'consumer-b' + '.v17',
                               'consumer-b' + '.v18', 'consumer-b' + '.v19'],
        'notANewOrigin': ('a continuation of the SAME blind origin. No preserved earlier '
                          'CHANGES_REQUIRED review is retroactively accepted by this '
                          'continuation.'),
        'inputCustody': {
            'manifestSha256': (cust.get('claim1_manifestOwnBytes') or {}).get('measured'),
            'declaredParentBinding': (cust.get('claim2_declaredParentBinding')
                                      or {}).get('declared'),
            'rowsVerified': (cust.get('claim3_everyRowVerified') or {}).get('filesVerified'),
            'measuredNormativeDelta': {
                k: (cust.get('claim4_normativeDeltaVsThisOriginsOwnPriorCustody')
                    or {}).get(k)
                for k in ('unchangedCount', 'changedCount', 'addedCount', 'changed', 'added')},
            'claimLimits': ('disclosed-file verification plus a DECLARED parent binding only; '
                            'the parent subject is not held'),
        },
        'newNormativeWorkThisGeneration': {
            'S2_glob': {'disposition': glob.get('v16S2Disposition', '')[:160],
                        'requiredExamplesMeasured': glob.get('requiredExampleCount'),
                        'derivedProperties': glob.get('derivedPropertyCount'),
                        'failures': len(glob.get('failures') or [])},
            'S1_repairSelection': {
                'runsMeasured': [r['label'] for r in (sel.get('runs') or [])],
                'lawBranchControls': len(sel.get('lawBranchControls') or []),
                'lawBranchFailures': [r['branch'] for r in (sel.get('lawBranchControls') or [])
                                      if r.get('result') != 'PASS']},
        },
        'area3ExecutionInputs': {
            'independentDerivationRefusals': area3.get('totalRefusals'),
            'perRunChecksPassed': {k: v.get('passed')
                                   for k, v in (area3.get('runs') or {}).items()},
            'discriminatingControls': len((ei_ctl.get('controls') or [])),
            'controlsAllRefused': all(c.get('refused')
                                      for c in (ei_ctl.get('controls') or [])) or None,
        },
        'runs': runs,
        'requirementStatus': dict(counts),
        'designGaps': {'must': len(gaps.get('newMustIssues') or []),
                       'should': len(gaps.get('newShouldIssues') or []),
                       'advisories': len(gaps.get('advisories') or []),
                       'stillOpen': [s['id'] for s in (gaps.get('newShouldIssues') or [])],
                       'resolvedThisGeneration': [s.get('id') for s in
                                                  (gaps.get('resolvedByThisKit') or [])]},
        'fromScratch': {
            'declaredStageCount': verify.get('declaredStageCount'),
            'stagesRecordedWhenThisStageRan': len(verify.get('stages') or []),
            'allStagesPassed': verify.get('allStagesPassed'),
            'standing': ('verify-all.json is rewritten after every stage. This record is written '
                         'by the progress stage, which runs before the final reconciliation '
                         'stage, so it sees every preceding stage of the SAME run and not the '
                         'two that follow it. The completed run is recorded in verify-all.json '
                         'itself.')},
        'historyStanding': {'state': hist.get('state'),
                            'carriedDisclosure': (
                                hist.get('carriedDisclosure_generation16NoteOverwrites')
                                or {}).get('status'),
                            'generationsModifiedThisSession': (
                                (hist.get('measuredC_priorGenerations') or {})
                                .get('generationsModifiedDuringThisSession'))},
        'openHelperFailures': helpers.get('openHelperFailuresOnAClaimedPositive'),
        'verdict': (J('blind-review.json') or {}).get('verdict'),
        'noProductChange': ('no product implementation, repository mutation, commit, push, '
                            'real repair, baseline adoption or product qualification'),
    }
    with open(OUT + '/progress.v19.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    print('progress.v19.json written | verdict %s | status %s | stages %s | openHelpers %s'
          % (doc['verdict'], dict(counts), doc['fromScratch'], doc['openHelperFailures']))


main()
