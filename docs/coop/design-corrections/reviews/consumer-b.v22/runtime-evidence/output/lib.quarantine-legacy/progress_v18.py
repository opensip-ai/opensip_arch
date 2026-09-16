"""output/progress.v18.json -- written from the artifacts that exist right now."""
import json
import os
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def main():
    cust = J('notes/v17-input-custody.json') or {}
    runs = J('runs/all-runs-summary.json') or []
    gaps = J('vectors/phase10-design-gaps.json') or {}
    helpers = J('helper-corrections.json') or {}
    verify = J('verify-all.json') or {}
    status = J('requirement-status.json') or {}
    import collections
    counts = collections.Counter(v['status'] for v in status.values())
    doc = {
        'consumerId': 'consumer-b.v18',
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'sameOriginAncestry': ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16',
                               'consumer-b.v18'],
        'notANewOrigin': ('a continuation of the SAME blind origin. The preserved v16 '
                          'CHANGES_REQUIRED review is not retroactively accepted by this '
                          'continuation.'),
        'inputCustody': {
            'manifestSha256': cust.get('inputKit', {}).get('manifestSha256Measured'),
            'declaredParentBinding': cust.get('inputKit', {}).get(
                'parentSubjectSha256DeclaredInManifest'),
            'hashVerification': cust.get('inputKit', {}).get('hashVerification'),
            'normativeByteIdentityVsV16': cust.get('normativeByteIdentityAgainstV16', {}).get(
                'allDisclosedNormativeFilesByteIdentical'),
            'claimLimits': ('disclosed-file verification plus a DECLARED parent binding only; '
                            'the parent candidate is not held'),
        },
        'secondClauseToCodeAudit': {
            'areas': ['atom kind/endpoint admission', 'enumeration program binding and '
                      'inventories', 'unavailable bindings', 'coverage accounts and cell '
                      'outcomes', 'invocation step/result joins', 'repair preimage snapshot '
                      'condition', 'byte/frame/schema/semantic joins and fresh-process '
                      'reconstruction'],
            'newHelperOmissionsFound': [h['id'] for h in helpers.get('helperCorrections', [])
                                        if h['id'].startswith('V17-')],
            'findingsInOwnSealedGraphs': [
                'two of five graphs carried a malformed DISABLED rule hidden by the disabled '
                'outcome (ATOM_KIND_INCOMPATIBLE)',
                'four of five graphs declared a compiler/grammar-filtered FILE extent',
                'one graph narrowed an `inventory` cell to a consumer-chosen kind subset',
                'one graph had an unavailable cell with no extents and NO retained inventory',
                'the multi-step invocation used ONE-based stepIds, accounted no comparison '
                'result and carried no attempt derivation binding',
                'the "valid" repair descriptor asked to CREATE a path the selected snapshot '
                'already contained',
            ],
            'newControlFamilies': {
                'policyAdmission': 18,
                'enumerationContract': 8,
                'invocationJoins': 14,
                'repairSnapshotCondition': 4,
            },
        },
        'runs': runs,
        'requirementStatus': dict(counts),
        'designGaps': {'must': len(gaps.get('newMustIssues') or []),
                       'should': len(gaps.get('newShouldIssues') or []),
                       'advisories': len(gaps.get('advisories') or []),
                       'stillOpen': [s['id'] for s in (gaps.get('newShouldIssues') or [])],
                       'withdrawnThisGeneration': ['V16-A2']},
        'fromScratch': {'stages': len(verify.get('stages') or []),
                        'allStagesPassed': verify.get('allStagesPassed')},
        'priorGenerationWrites': J('notes/prior-generation-writes.json'),
        'verdict': (J('blind-review.json') or {}).get('verdict'),
        'noProductChange': ('no product implementation, repository mutation, commit, push, '
                            'real repair, baseline adoption or product qualification'),
        'stillOutstanding': [
            'V16-S1 and V16-S2 remain PENDING SOURCE-AUTHOR work; no new normative bytes were '
            'supplied this generation and no selector or glob law was invented to close them',
        ],
    }
    with open(OUT + '/progress.v18.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    print('progress.v18.json written | verdict %s | status %s | stages %s'
          % (doc['verdict'], dict(counts), doc['fromScratch']))


main()
