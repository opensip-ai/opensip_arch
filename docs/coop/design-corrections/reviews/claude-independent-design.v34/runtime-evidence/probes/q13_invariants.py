"""Q13 — meaningful invariants over the source34 review. Each asserts a claim that could be false:
row assertions against manifests, readingStanding against owner bytes, the MUST against its receipts,
table/package/suite/planning claims against their receipts, obligations and authority flags, and the
MD against the JSON."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
RC = os.path.join(BASE, 'receipts')
B2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
C, bad = {}, []


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def chk(name, cond, detail=''):
    C[name] = bool(cond)
    print('%-70s %s %s' % (name[:70], 'OK ' if cond else 'FAIL', str(detail)[:120]))
    if not cond:
        bad.append(name)


J = json.load(open(os.path.join(BASE, 'review.json')))
MD = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
BL = json.load(open(os.path.join(B2, 'review.json')))
rc = lambda n: json.load(open(os.path.join(RC, n)))
q00, q01, q04, q05, q06, q07, q08, q09, q10, q11, q12 = (rc(n) for n in (
    'q00-custody.json', 'q01-diffs.json', 'q04-rows.json', 'q05-atomlaw.json', 'q06-followups.json', 'q07-suites.json',
    'q08-package11.json', 'q09-subject-universe.json', 'q10-reach-and-rows.json', 'q11-default-reach.json', 'q12-package-delta.json'))
man34 = json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))
m34 = {f['path']: f['sha256'] for f in man34['files']}
m33 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v33.json')))['files']}
DELTA = {p for p in m34 if m33.get(p) != m34[p]} | {p for p in m33 if p not in m34}
MAPS = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16, 'fwDispositions': 15,
        'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5}

print('--- subject and history ---')
drift = sum(1 for f in man34['files'] if sha(os.path.join(S34, f['path'])) != f['sha256'])
chk('frozen34 immutable after all work (12,899 rows, 0 drift)', len(m34) == 12899 and drift == 0, drift)
chk('independent delta recomputed from manifests = 9 files', len(DELTA) == 9 and J['delta33to34']['changed'] == 9
    and {c['path'] for c in J['delta33to34']['changedFiles']} == DELTA)
for label, path, want in (
        ('v33 report', '/tmp/opensip-design-corrections/claude-independent-design.v33/review.json', '800465853d626f49cdbaf48af2066b6a8e3e65f364d2a21a9263ab88a2eb0b90'),
        ('reconciliation v1', '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/review.json', 'ad0457bc1e01ac3090335d20b95dedd54dee72a340adf047706c0fc89419c40d'),
        ('reconciliation v2 baseline', os.path.join(B2, 'review.json'), '89f4bd73ea4168286102c90d02020f2ee514a52e81280d186d05b78a3b6c4533')):
    chk('%s preserved byte-identical' % label, sha(path) == want)

print('\n--- rows: history preserved, owner arrays from manifests, reading standing from bytes ---')
tot = hist_ok = arr_bad = rs_bad = flags = 0
stale_expected = set()
for mp, n in MAPS.items():
    chk('map %s has %d rows with baseline ids' % (mp, n), list(J[mp]) == list(BL[mp]) and len(J[mp]) == n)
    for rid, row in J[mp].items():
        tot += 1
        base = BL[mp][rid]
        if all(row.get(k) == v for k, v in base.items() if k not in ('appliedByThisReview', 'finalApplicationOutcomeGranted')):
            hist_ok += 1
        if row.get('appliedByThisReview') is False and row.get('finalApplicationOutcomeGranted') is False:
            flags += 1
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        if paths:
            ch, un = row.get('ownerFilesChangedIn33to34'), row.get('ownerFilesUnchangedIn33to34')
            if set(ch) != {p for p in paths if p in DELTA} or set(un) != {p for p in paths if p not in DELTA} \
                    or row.get('ownerPathsResolveInFrozen34') is not all(p in m34 for p in paths):
                arr_bad += 1
            equal = all(m33.get(p) == m34.get(p) for p in paths)
            if 'INHERITED ON EXACT BYTES' in (row.get('readingStandingOn34') or '') and not equal:
                rs_bad += 1
        if not row.get('currentStatusOn34') or not row.get('readingStandingOn34'):
            rs_bad += 1
        ch32 = base.get('ownerFilesChangedIn32to33')
        if ch32 is None:
            ch32 = base.get('ownerSelectorsChangedIn32to33')
        rs = base.get('readingStanding')
        if isinstance(rs, str) and ((re.search('unchanged', rs, re.I) and ch32) or
                                    (re.search(r'changed (?:cited )?owner|re-read', rs, re.I) and ch32 == [])):
            stale_expected.add(mp + '/' + rid)
chk('107 rows', tot == 107, tot)
chk('every baseline field of every row preserved verbatim', hist_ok == 107, hist_ok)
chk('both authority flags false on every row', flags == 107, flags)
chk('current34 owner arrays equal manifest recomputation on every owner-bearing row', arr_bad == 0, arr_bad)
chk('INHERITED ON EXACT BYTES claimed only where owner digests are equal 33/34; every row has current34 fields', rs_bad == 0, rs_bad)
got_stale = {k for mp in MAPS for k in [mp + '/' + r for r, row in J[mp].items() if row.get('readingStandingLegacyCorrectionOn34')]}
chk('legacy readingStanding corrections = independently recomputed stale set (9)', got_stale == stale_expected and len(got_stale) == 9,
    sorted(stale_expected ^ got_stale))
chk('no legacy readingStanding string edited', all(J[mp][r].get('readingStanding') == BL[mp][r].get('readingStanding') for mp in MAPS for r in BL[mp]))
chk('F-04 / F-09 source-law owners byte-equal 33/34 as their inherited text claims',
    J['fDispositions']['F-04']['subjectOwnerBytesEqual33and34'] and J['fDispositions']['F-09']['subjectOwnerBytesEqual33and34'])
pk = [r for r, row in J['fDispositions'].items() if row.get('statusChangeOn34') == 'RE-VERIFIED-ON-PACKAGE11']
chk('package-borne F rows cite package11 (311 / 38f7ce94) and never package10 figures as current',
    all('311/311' in J['fDispositions'][r]['currentStatusOn34'] and '38f7ce94' in J['fDispositions'][r]['currentStatusOn34']
        and '305/305' not in J['fDispositions'][r]['currentStatusOn34'] for r in pk) and len(pk) == 11, pk)
cons = {mp + '/' + r for mp in MAPS for r, row in J[mp].items() if row.get('statusChangeOn34') not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE11')}
chk('cross-owner consequence rows are exactly AR-12, FW-08, FW-06, DR-009, AR-16',
    cons == {'arDispositions/AR-12', 'fwDispositions/FW-08', 'fwDispositions/FW-06', 'inheritedResidualDispositions/DR-009', 'arDispositions/AR-16'}, sorted(cons))
chk('the two reopened rows cite MUST-34-01', all('MUST-34-01' in J[m][r]['currentStatusOn34'] for m, r in (('arDispositions', 'AR-12'), ('fwDispositions', 'FW-08'))))

print('\n--- MUST-34-01 against its receipts ---')
m = J['newMustIssues'][0]
cs = q09['cases']
chk('MUST: incoming none=true / exists=false with no cause when U is unbound and U2 evidenced',
    cs['U1-unbound__U2-same-family-fully-evidenced']['incoming/none']['value'] == 'true'
    and cs['U1-unbound__U2-same-family-fully-evidenced']['incoming/exists']['value'] == 'false'
    and cs['U1-unbound__U2-same-family-fully-evidenced']['incoming/none']['causes'] == [])
chk('MUST discriminator: binding U without evidence makes incoming unknown',
    cs['U1-bound-but-unevidenced__U2-same-family-fully-evidenced']['incoming/none']['value'] == 'indeterminate')
chk('MUST discriminator: no binding anywhere is unknown; outgoing on the same inputs is unknown',
    cs['U1-unbound__no-references-binding-anywhere']['incoming/none']['value'] == 'indeterminate'
    and cs['U1-unbound__U2-same-family-fully-evidenced']['outgoing/none']['value'] == 'indeterminate')
chk('MUST pre-existing claim equals frozen33 measurement', q10['identicalOn33'] is True and 'identicalOn33 = True' in m['preExisting'])
chk('MUST default-profile unreachability claim equals q11', q11['defaultReachable'] is False and 'NOT reachable' in m['reachability']['defaultProfile'])
chk('MUST narrowed plan passes enumeration-plan schema as claimed', q09['enumerationPlanSchema']['narrowedPlanErrors'] == [])
chk('verdict CHANGES_REQUIRED iff a MUST exists', (J['verdict'] == 'CHANGES_REQUIRED') == bool(J['newMustIssues']))

print('\n--- atom-law, table, package, suites, planning claims against receipts ---')
tab = J['sourceChangeAssessment']['atomCompletenessLaw']['branches']['searchAccountingTable']
chk('table: 21 admitted cells, zero disagreements, matches q05',
    tab['G1']['admitted'] == 21 == sum(1 for r in q05['G-table'] if r['admission'] == 'ADMIT') and not tab['G1']['disagreements'])
chk('qualification matrix: 16 combinations, 8 admitted', tab['G3qualificationMatrix']['combinations'] == 16 and tab['G3qualificationMatrix']['admitted'] == 8)
chk('all q05 controls either pass or are recorded probe errors (F4, H3) and H3/E5 were rerun passing',
    set(q05['failed']) == {'F4-untagged-shared-scope-owed-to-every-contributor', 'H3-separate-processes-with-hash-seeded-map-order'}
    and all(c['passed'] for c in q06['cases']))
e1 = [c for c in q05['cases'] if c['id'].startswith('E1')][0]['observed']
chk('fold-ordering discrimination claim: 34 single result, 33 multiple (E1, E2, H3)',
    all(v['distinct34'] == 1 for v in e1.values()) and any(v['distinct33'] > 1 for v in e1.values())
    and q06['H3']['summary']['34']['distinctDigests'] == 1 and q06['H3']['summary']['33']['distinctDigests'] > 1)
chk('no retained Run reaches incoming/attestation branches, as claimed',
    q08['anyRunReachesChangedAtomBranches']['incomingEndpointAtoms'] is False and q08['anyRunReachesChangedAtomBranches']['incomingSearchRecords'] == 0)
ap = J['authorPackageReview']
chk('package claims equal q08/q12', ap['members']['verified'] == 311 == q08['verified'] and q08['allThirteenAsExpected']
    and q08['queryChecks'] == 7 and q08['allExportsEqualPackage10'] and q12['residualAssessment']['bindsFrozen34'])
chk('suite claims equal q07: all rc 0, check-atoms 81/0, launcher pins valid 16 children',
    q07['allJobsExitZero'] and J['suites']['checkAtoms']['passed'] == 81 and J['suites']['checkAtoms']['failed'] == 0
    and q07['launcherReport']['sourcePinsValid'] and len(q07['launcherReport']['children']) == 16
    and all(c['exitCode'] == 0 for c in q07['launcherReport']['children']))
pl = J['sourceChangeAssessment']['planning']
chk('layer4 retained claim equals q01 (file unchanged, 29/29 resolve, none in delta)',
    pl['layer4Retained'] and q01['layer4']['sha33'] == q01['layer4']['sha34'] and q01['layer4']['pins'] == 29
    and q01['layer4']['pinsResolveAgainst34'] == 29 and q01['layer4']['pinnedPathsInDelta'] == [])
chk('every receipt digest recorded in the JSON matches the file now',
    all(sha(os.path.join(RC, f)) == d for f, d in J['evidenceReceipts']['receipts'].items()))

print('\n--- obligations and grants ---')
cu = J['crossUnitStanding']
chk('28 / 32-with-0 / condition5 NOT MET / 54-with-0', cu['condition2ObligationsRetained'] == 28 and cu['qualificationGates'] == 32
    and cu['qualificationGatesPerformed'] == 0 and cu['condition5'] == 'NOT MET' and cu['commitRecoveryCases'] == 54 and cu['commitRecoveryCasesExecuted'] == 0)
chk('D9 obligation names DR-007 and DR-011-R08', 'DR-007' in cu['d9SuccessorObligation'] and 'DR-011-R08' in cu['d9SuccessorObligation'])
chk('TCB-SCOPE-01 one joint consequence over 13 rows, not closed',
    len(J['sharedAssumptionTCBSCOPE01']['dependentRows']) == 13 and 'not closed' in J['sharedAssumptionTCBSCOPE01']['statusOn34'])
chk('30 residuals PENDING, none graded', all(r.get('independentGradeAwardedHere') is None and r.get('reviewStatus') == 'PENDING'
                                             for r in J['evaluationResidualDispositions'].values()))
gn = J['grantsNothing']
chk('grants nothing', gn['grade'] is None and not any(gn[k] for k in ('architectureReady', 'activation', 'implementationAuthorized',
                                                                        'blindAcceptance', 'packageAcceptance', 'finalApplicationOutcomeGranted', 'commitOrPush')))
chk('advisories A-9 A-10 A-11 A-12 with statusOn34', [a['id'] for a in J['advisories']] == ['A-9', 'A-10', 'A-11', 'A-12']
    and all(a.get('statusOn34') for a in J['advisories']))

print('\n--- MD against JSON ---')
for tok in ('CHANGES_REQUIRED', 'MUST-34-01', 'A-12', '12,899', '736,798,408', '9 changed', '311/311', '81/81', '16/16',
            '375/375', '21 admitted', 'Layer4', 'retained', '54 recovery', 'DR-011-R08', 'DR-011-R12', 'nine', 'PENDING'):
    chk('md states %r' % tok, tok in MD)
chk('md never claims ACCEPT for source34', not re.search(r'Verdict:\s*\**ACCEPT', MD))
chk('md MUST table values equal q09', '**true** (no cause)' in MD and 'unknown (`missing-relation-coverage`)' in MD)

C['reviewJsonSha256'] = sha(os.path.join(BASE, 'review.json'))
C['reviewMdSha256'] = sha(os.path.join(BASE, 'review.md'))
C['checks'] = len([k for k, v in C.items() if isinstance(v, bool)])
C['failed'] = bad
print('\nchecks %d | failed %d %s' % (C['checks'], len(bad), bad))
print('review.json', C['reviewJsonSha256'])
print('review.md  ', C['reviewMdSha256'])
json.dump(C, open(os.path.join(RC, 'q13-invariants.json'), 'w'), indent=1)
