"""I36 — invariants over review.json (and review.md when present) against the receipts and the source35 baseline.
Row preservation is checked field by field against the baseline; authority flags; counts; required obligations; md/json agreement."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
RC = os.path.join(BASE, 'receipts')
V35 = '/tmp/opensip-design-corrections/claude-independent-design.v35'
J = json.load(open(os.path.join(BASE, 'review.json')))
BL = json.load(open(os.path.join(V35, 'review.json')))
MD = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read() if os.path.isfile(os.path.join(BASE, 'review.md')) else None
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
MAPS = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16, 'fwDispositions': 15, 'inheritedResidualDispositions': 27,
        'scopedReviewOwnerDispositions': 5}
C, bad = {}, []


def chk(name, cond, obs=None):
    C[name] = {'passed': bool(cond), 'observed': obs}
    print('%-96s %s' % (name, 'OK' if cond else 'FAIL'))
    if not cond:
        bad.append(name)


chk('verdict ACCEPT, no MUST, no SHOULD', J['verdict'] == 'ACCEPT' and J['newMustIssues'] == [] and J['newShouldIssues'] == [])
chk('subject manifest sha is the frozen36 manifest', J['subjectManifestSha256'] == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235' and J['verifiedManifest'] is True)
chk('advisories A-9..A-15 in order', [a['id'] for a in J['advisories']] == ['A-9', 'A-10', 'A-11', 'A-12', 'A-13', 'A-14', 'A-15'])
chk('A-13 closed on 36', 'CLOSED' in J['advisories'][4]['statusOn36'] and any(x['id'] == 'A-13' and x['status'] == 'CLOSED ON SOURCE36' for x in J['resolvedIssues']))
chk('every focused totality finding has a status', {x['id'] for x in J['resolvedIssues']} >= {'TOT-%d' % i for i in range(1, 10)})
chk('MUST-34-01 history preserved with statusOn36', any(x['id'] == 'MUST-34-01' and 'statusOn36' in x for x in J['resolvedIssues']))
chk('map sizes 14/30/16/15/27/5 = 107', {mp: len(J[mp]) for mp in MAPS} == MAPS and J['dispositionCounts']['total'] == 107)
preserved, flags, fields36, legacy = True, True, True, 0
for mp in MAPS:
    for rid, row in J[mp].items():
        base = BL[mp][rid]
        for k, v in base.items():
            if k in ('appliedByThisReview', 'finalApplicationOutcomeGranted'):
                continue
            if row.get(k) != v:
                preserved = False
        if row.get('appliedByThisReview') is not False or row.get('finalApplicationOutcomeGranted') is not False:
            flags = False
        for f in ('statusChangeOn36', 'currentDispositionOn36', 'currentStatusOn36', 'readingStandingOn36', 'currentFieldStandingOn36',
                  'ownerFilesChangedIn35to36', 'ownerFilesUnchangedIn35to36'):
            if f not in row:
                fields36 = False
        if row.get('ownerFilesChangedIn35to36'):
            fields36 = False
        if row.get('readingStandingLegacyCorrectionOn34'):
            legacy += 1
            if 'readingStandingLegacyCorrectionStatusOn36' not in row:
                fields36 = False
chk('every baseline row field preserved verbatim (all *On33/*On34/*On35)', preserved)
chk('appliedByThisReview=false and finalApplicationOutcomeGranted=false on all 107', flags)
chk('every row carries explicit On36 disposition/reading fields; no owner changed 35->36', fields36)
chk('nine legacy reading corrections retained with statusOn36', legacy == 9 and J['readingStandingAudit']['count'] == 9 and 'statusOn36' in J['readingStandingAudit'])
cc = J['rowCarryForwardCounts36']
chk('carry-forward 36 derived: 91 inherited / 11 package13 / 5 cross-owner', (cc['inherited'], cc['packageReverified'], cc['crossOwner']) == (91, 11, 5))
chk('historical rowCarryForwardCounts (35) preserved', J['rowCarryForwardCounts'] == BL['rowCarryForwardCounts'])
cu = J['crossUnitStanding']
chk('cross-unit obligations 28 / 32 gates 0 performed / condition5 NOT MET / 54 recovery 0 executed / D9 DR-007 DR-011-R08',
    cu['condition2Obligations'] == 28 and cu['qualificationGates'] == 32 and cu['qualificationGatesPerformed'] == 0 and cu['condition5'] == 'NOT MET'
    and cu['commitRecoveryCases'] == 54 and cu['commitRecoveryCasesExecuted'] == 0 and 'DR-007' in cu['d9SuccessorObligation'] and 'DR-011-R08' in cu['d9SuccessorObligation'])
chk('TCB-SCOPE-01 over 13 rows retained', J['sharedAssumptionTCBSCOPE01']['dependentRowCount'] == 13 and 'statusOn36' in J['sharedAssumptionTCBSCOPE01'])
g = J['grantsNothing']
chk('grants nothing', g['architectureReady'] is False and g['activation'] is False and g['implementationAuthorized'] is False and g['blindAcceptance'] is False
    and g['packageAcceptance'] is False and g['finalApplicationOutcomeGranted'] is False and g['commitOrPush'] is False and g['grade'] is None)
chk('30 residual proposals PENDING, TCB 13 on package13', J['authorPackageReview']['residualAssessment']['grades'] == ['PENDING'] and J['authorPackageReview']['residualAssessment']['rows'] == 30
    and J['authorPackageReview']['residualAssessment']['tcbDependents'] == 13)
chk('package13: 13 cases both boundaries, 7 queries, exports equal package12, mixed 33/30', J['authorPackageReview']['thirteenCases']['allAsExpected']
    and J['authorPackageReview']['verifier']['queryChecks'] == 7 and J['authorPackageReview']['lineage']['exportsByteEqualPackage12Files']
    and J['authorPackageReview']['constructionProvenance']['mixed33TS30NormalizedRust'])
chk('planning layer4 retained 29 inputs; 198/20/320/54/0', J['sourceChangeAssessment36']['planning']['layer4']['pins'] == 29 and J['sourceChangeAssessment36']['planning']['populations']
    == {'paths': 198, 'packages': 20, 'coverageMappings': 320, 'plannedRecoveryCases': 54, 'executed': 0, 'milestones': 'M0-M6 (7)'})
chk('suites all exit 0, check-atoms 101, launcher 16, drift 0', J['suites']['allJobsExitZero'] and J['suites']['checkAtoms']['passed'] == 101
    and len(J['suites']['launcherReport']['children']) == 16 and J['suites']['frozen36DeviationsAfterRuns'] == 0)
chk('reachability standings do not claim closed enumeration, retained-Run reach or product', J['sourceChangeAssessment36']['reachabilityByStanding']['closedEnumeration'] == 'NOT RUN'
    and 'no retained Run reaches' in J['sourceChangeAssessment36']['reachabilityByStanding']['retainedRun'] and J['sourceChangeAssessment36']['reachabilityByStanding']['product'].startswith('NOT ESTABLISHED'))
chk('law derived before any semantic probe', J['lawDerivedBeforeTesting']['writtenBeforeAnySemanticProbe'])
chk('authorship overlap disclosed; no blind/application standing claimed', 'standingNotClaimed' in J['sessionIdentity']['overlapWithCandidateAuthorship']
    and 'finalBytesAreNotMine' in J['sessionIdentity']['overlapWithCandidateAuthorship'])
chk('C36-01 appended; earlier corrections preserved', [c['id'] for c in J['correctionsToMyOwnPriorRecords']] == ['C34-01', 'C35-01', 'C36-01'])
chk('probe errors: baseline preserved plus four new', J['probeErrorsPreserved'][:len(BL['probeErrorsPreserved'])] == BL['probeErrorsPreserved'] and len(J['probeErrorsPreserved']) == len(BL['probeErrorsPreserved']) + 4)
mismatch = [f for f, h in J['evidenceReceipts']['receipts'].items() if sha(os.path.join(RC, f)) != h]
chk('every cited receipt digest still matches', not mismatch, mismatch)
p01 = json.load(open(os.path.join(RC, 'p01-totality36.json')))
chk('p01 37 checks all passed; p03 15; p02 passed', not p01['failedChecks'] and len(p01['checks']) == 37
    and not json.load(open(os.path.join(RC, 'p03-history-runtime36.json')))['failedChecks'] and json.load(open(os.path.join(RC, 'p02-determinism36.json')))['passed'])
if MD is not None:
    for tok in ('**Verdict: ACCEPT**', 'a729406b', '7db498f0', '12,899', '736,854,701', 'A-13 is CLOSED', 'A-14', 'A-15', 'two-view', 'prototype', 'required-relation-missing',
                '101/101', '16/16', '375/375', '412', '323/323', '7/7', 'open_run_closure', 'close_run', '33', '30', '14 F, 30 evaluation residuals, 16 AR, 15 FW, 27 inherited, 5 scoped',
                '91', '11', '5 cross-owner', 'nine legacy', '28', '32', 'NOT MET', '54', 'DR-007', 'DR-011-R08', 'PENDING', 'TCB-SCOPE-01', 'layer4', '198', '20 packages', '320',
                'C36-01', 'not an independent acceptor', 'appliedByThisReview: false', 'finalApplicationOutcomeGranted: false', 'no application outcome'):
        chk('md states %r' % tok, tok in MD)
    for n in re.findall(r'receipts/([\w.\-]+\.json)', MD):
        if not os.path.isfile(os.path.join(RC, n)):
            chk('md cites existing receipt %s' % n, False)
C['failed'] = bad
C['reviewJsonSha256'] = sha(os.path.join(BASE, 'review.json'))
C['reviewMdSha256'] = sha(os.path.join(BASE, 'review.md')) if MD is not None else None
json.dump(C, open(os.path.join(RC, 'i36-invariants.json'), 'w'), indent=1, default=str)
print('\nchecks %d failed %d | review.json %s | review.md %s' % (len([v for v in C.values() if isinstance(v, dict)]), len(bad), C['reviewJsonSha256'], C['reviewMdSha256']))
