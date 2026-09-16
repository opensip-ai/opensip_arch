"""R04 — consistency check of the COMPLETE successor review.json: structure preserved, corrections
actually applied, no stale contradictory prose left anywhere, obligations intact."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = json.load(open(os.path.join(BASE, 'review.json')))
OLD = json.load(open(os.path.join(V32, 'review.json')))
C = {}


def chk(name, ok, detail=''):
    C[name] = {'ok': bool(ok), 'detail': detail}
    print('%-56s %s %s' % (name, 'OK ' if ok else 'FAIL', detail if not ok else ''))
    return ok


# structure preserved
for k, n in (('fDispositions', 14), ('evaluationResidualDispositions', 30), ('arDispositions', 16),
             ('fwDispositions', 15), ('inheritedResidualDispositions', 27),
             ('scopedReviewOwnerDispositions', 5)):
    chk('map %s has %d rows' % (k, n), len(R[k]) == n, str(len(R[k])))
chk('107 dispositions total', sum(len(R[k]) for k in
    ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
     'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')) == 107)
chk('same row ids as the superseded record',
    all(sorted(R[k]) == sorted(OLD[k]) for k in
        ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
         'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')))
chk('verdict preserved', R['verdict'] == OLD['verdict'] == 'ACCEPT', R['verdict'])
chk('manifest sha is source32',
    R['subjectManifestSha256'] == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2')
chk('no new MUST / SHOULD', not R['newMustIssues'] and not R['newShouldIssues'])
chk('advisories preserved', len(R['advisories']) == len(OLD['advisories']))

# corrections applied
chk('RR32-01 DR-007 cites the v3 fault contract',
    any('evaluator-fault-contract.v3.md' in p for p in R['inheritedResidualDispositions']['DR-007']['currentOwnerFiles']))
# My first version of these two checks flat-matched the whole document and so flagged the
# INTENTIONAL quotations inside recordCorrection / rootFinding / evidence fields, which exist
# precisely to document what was wrong. Classify by JSON path instead (see r05-locate.json).
def occurrences(token):
    found = []

    def walk(o, path='$'):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + '/%d' % i)
        elif isinstance(o, str) and token in o:
            found.append(path)
    walk(R)
    return found


def stale_only(token):
    return [p for p in occurrences(token)
            if not any(t in p for t in ('recordCorrection', 'correctionsToMyOwnV32Record',
                                        'correctionsToMyOwnV31Record', 'rootFinding', 'evidence'))]


chk('RR32-01 no v1 fault-contract path outside documented quotations',
    not stale_only('evaluator-fault-contract.v1.md'),
    str(stale_only('evaluator-fault-contract.v1.md'))[:200])
chk('RR32-02 F-04 limits no longer say precedes structural custody',
    'precedes structural custody' not in R['fDispositions']['F-04']['limits'])
chk('RR32-02 no inverse wording outside documented quotations',
    not stale_only('precedes structural custody'),
    str(stale_only('precedes structural custody'))[:200])
chk('RR32-03 RES-EP13-13 no longer asserts a source28 session',
    'read fresh in that session' not in R['evaluationResidualDispositions']['RES-EP13-13']['readingStanding'])
chk('RR32-03 row states the truthful lineage',
    'no source28 review session' in R['evaluationResidualDispositions']['RES-EP13-13']['readingStanding'].lower()
    or 'NO source28 review session' in R['evaluationResidualDispositions']['RES-EP13-13']['readingStanding'])
r16 = {k: v for k, v in R['inheritedResidualDispositions'].items() if k.startswith('DR-011-R')}
chk('RR32-04 all 16 booleans true', all(v['ownerPathsResolveInFrozen32'] for v in r16.values()))
chk('RR32-04 all 16 booleans match actual membership',
    all(v['ownerPathsResolveInFrozen32'] == all(p in man for p in v['currentOwnerFiles'])
        for v in r16.values()))
chk('RR32-04 four rows regained their real owner',
    all(any(x in ' '.join(R['inheritedResidualDispositions'][rid]['currentOwnerFiles']) for x in [y])
        for rid, y in (('DR-011-R02', 'fact-identity-policy.v2.json'),
                       ('DR-011-R04', 'protocol3-transitions.v1.json'),
                       ('DR-011-R05', 'protocol3-transitions.v1.json'),
                       ('DR-011-R08', 'evaluator-fault-contract.v3.md'))))

# every owner path resolves
bad = []
for mp in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
           'scopedReviewOwnerDispositions'):
    for rid, row in R[mp].items():
        for p in row.get('currentOwnerFiles', []):
            if p not in man:
                bad.append(mp + '/' + rid + ':' + p)
for rid, row in R['evaluationResidualDispositions'].items():
    for p in row.get('currentOwnerSelectors', []):
        if p not in man:
            bad.append('eval/' + rid + ':' + p)
chk('every owner path across all rows resolves in frozen32', not bad, str(bad)[:200])

# standing intact
chk('TCB assessed once with 13 dependents',
    R['sharedAssumptionTCBSCOPE01']['dependentRowCount'] == 13
    and sum(1 for v in R['evaluationResidualDispositions'].values() if v['sharedAssumption']) == 13)
cu = R['crossUnitStanding']
chk('28 condition-2 obligations retained', cu['condition2ObligationsRetained'] == 28)
chk('32 gates unperformed, condition5 NOT MET',
    cu['qualificationGatesPerformed'] == 0 and cu['condition5'] == 'NOT MET')
chk('54 recovery cases unexecuted', cu['commitRecoveryCasesExecuted'] == 0)
chk('D9 successor still an assigned obligation', 'ASSIGNED' in cu['d9SuccessorObligation'].upper())
chk('30 residuals remain author PENDING',
    all(v['reviewStatus'] == 'PENDING' and v['independentGradeAwardedHere'] is None
        for v in R['evaluationResidualDispositions'].values()))
applied = [(mp, rid) for mp in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions',
                                'fwDispositions', 'inheritedResidualDispositions',
                                'scopedReviewOwnerDispositions')
           for rid, v in R[mp].items()
           if v['appliedByThisReview'] or v['finalApplicationOutcomeGranted']]
chk('every row appliedByThisReview=false and no outcome granted', not applied, str(applied)[:160])
g = R['grantsNothing']
chk('design-only grantsNothing preserved',
    g['grade'] is None and not g['activation'] and not g['implementationAuthorized']
    and not g['blindAcceptance'] and not g['architectureReady'])
chk('blind charter untouched', 'blindCharter' in cu and 'no consumer runtime' in cu['blindCharter'])

# receipts keep their ORIGINAL locations
s = json.dumps(R)
chk('original v31/v32 receipt locations cited, not relabelled',
    'claude-independent-design.v32/receipts' in s and 'claude-independent-design.v31/receipts' in s)
chk('correctionsToMyOwnV32Record present with evidence',
    len(R['correctionsToMyOwnV32Record']) >= 4
    and all('evidence' in c or 'rootStatement' in c for c in R['correctionsToMyOwnV32Record']))
chk('bounded probe qualifications recorded',
    'scopeQualification' in R['evidenceReceipts']['repairLawExecution']
    and 'evidenceQualification' in R['sourceChangeAssessment']
    ['change1_repairClosedWorldSelectionOwner']['cellOrdinalQuestionIRaisedAndResolved'])
chk('superseded record preserved unchanged',
    hashlib.sha256(open(os.path.join(V32, 'review.json'), 'rb').read()).hexdigest()
    == R['recordLineage']['supersededRecord']['sha256'])

fails = [k for k, v in C.items() if not v['ok']]
print('\n%d checks, %d failures' % (len(C), len(fails)))
print('FAILURES:', fails)
json.dump({'checks': C, 'failures': fails},
          open(os.path.join(BASE, 'receipts', 'r04-consistency.json'), 'w'), indent=1)
print('wrote r04-consistency.json')
