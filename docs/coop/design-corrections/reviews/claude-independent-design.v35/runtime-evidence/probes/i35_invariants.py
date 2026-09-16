"""I35 — meaningful invariants over the source35 review: row claims vs manifests and baseline, closure claims vs
the receipts that measured them, package/suite/planning/determinism claims vs receipts, obligations, and MD vs JSON."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
RC = os.path.join(BASE, 'receipts')
B34 = '/tmp/opensip-design-corrections/claude-independent-design.v34'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
C, bad = {}, []


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def chk(name, cond, detail=''):
    C[name] = bool(cond)
    print('%-72s %s %s' % (name[:72], 'OK ' if cond else 'FAIL', str(detail)[:110]))
    if not cond:
        bad.append(name)


J = json.load(open(os.path.join(BASE, 'review.json')))
MD = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
BL = json.load(open(os.path.join(B34, 'review.json')))
rc = lambda n: json.load(open(os.path.join(RC, n)))
r01, r02, r03, r04, r05, r06, r07, r08 = (rc(n) for n in ('r01-diffs.json', 'r02-must-matrix.json', 'r03-a12.json', 'r04-suites.json',
                                                           'r05-package12.json', 'r06-determinism.json', 'r07-followups.json', 'r08-rows.json'))
g = lambda R, cid: next(c for c in R['checks'] if c['id'] == cid)
man35 = json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))
m35 = {f['path']: f['sha256'] for f in man35['files']}
m34 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
DELTA = {p for p in m35 if m34.get(p) != m35[p]} | {p for p in m34 if p not in m35}
MAPS = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16, 'fwDispositions': 15,
        'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5}

print('--- subject and history ---')
chk('frozen35 immutable after all work', len(m35) == 12899 and sum(1 for f in man35['files'] if sha(os.path.join(S35, f['path'])) != f['sha256']) == 0)
chk('delta recomputed from manifests = 10 = JSON', len(DELTA) == 10 and {c['path'] for c in J['delta34to35']['changedFiles']} == DELTA)
for label, path, want in (('v34 review.json', B34 + '/review.json', 'c31f1c4779b8fa60385520009c73139d46572b29a7f22f251c5a0182a2a42bb3'),
                          ('v34 review.md', B34 + '/review.md', '72e4e1b04a0d3b905fbbf72b451fbfe7f0e4284c864c9517865ab27eff78c7fd'),
                          ('v33 review.json', '/tmp/opensip-design-corrections/claude-independent-design.v33/review.json', '800465853d626f49cdbaf48af2066b6a8e3e65f364d2a21a9263ab88a2eb0b90'),
                          ('reconciliation v2 review.json', '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/review.json', '89f4bd73ea4168286102c90d02020f2ee514a52e81280d186d05b78a3b6c4533')):
    chk('%s preserved byte-identical' % label, sha(path) == want)
chk('final root-later bytes equal frozen35', J['authorshipOfFinalBytes']['rootLater']['finalEqualsFrozen35'])

print('\n--- rows ---')
tot = hist = flags = arr_bad = rs_bad = 0
classes = {}
for mp, n in MAPS.items():
    chk('map %s: %d rows with baseline ids' % (mp, n), list(J[mp]) == list(BL[mp]) and len(J[mp]) == n)
    for rid, row in J[mp].items():
        tot += 1
        base = BL[mp][rid]
        if all(row.get(k) == v for k, v in base.items()):
            hist += 1
        if row.get('appliedByThisReview') is False and row.get('finalApplicationOutcomeGranted') is False:
            flags += 1
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        if paths and (set(row['ownerFilesChangedIn34to35']) != {p for p in paths if p in DELTA}
                      or set(row['ownerFilesUnchangedIn34to35']) != {p for p in paths if p not in DELTA}
                      or row['ownerPathsResolveInFrozen35'] is not all(p in m35 for p in paths)):
            arr_bad += 1
        if 'INHERITED ON EXACT BYTES' in row.get('readingStandingOn35', '') and paths and not all(m34.get(p) == m35.get(p) for p in paths):
            rs_bad += 1
        if not row.get('currentStatusOn35') or not row.get('readingStandingOn35'):
            rs_bad += 1
        classes[row['statusChangeOn35']] = classes.get(row['statusChangeOn35'], 0) + 1
chk('107 rows', tot == 107, tot)
chk('every baseline field (including all *On34 fields) preserved verbatim', hist == 107, hist)
chk('both authority flags false on every row', flags == 107, flags)
chk('35 owner arrays equal manifest recomputation', arr_bad == 0, arr_bad)
chk('INHERITED ON EXACT BYTES only where owner digests equal 34/35; all rows have 35 fields', rs_bad == 0, rs_bad)
chk('classes 91 inherited / 11 package12 / 5 cross-owner', classes.get('INHERITED') == 91 and classes.get('RE-VERIFIED-ON-PACKAGE12') == 11
    and sum(v for k, v in classes.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12')) == 5, classes)
cons = {mp + '/' + r: row['statusChangeOn35'] for mp in MAPS for r, row in J[mp].items() if row['statusChangeOn35'] not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12')}
chk('cross-owner rows are the same five as source34 with current statuses',
    cons == {'arDispositions/AR-12': 'RESTORED-ON-35-MUST-34-01-CLOSED', 'fwDispositions/FW-08': 'RESTORED-ON-35-MUST-34-01-CLOSED',
             'fwDispositions/FW-06': 'STRENGTHENED-HOLDS-ON-35-REMEASURED', 'inheritedResidualDispositions/DR-009': 'STRENGTHENED-HOLDS-ON-35-REMEASURED',
             'arDispositions/AR-16': 'STRENGTHENED-HOLDS-ON-35-REMEASURED'}, cons)
pk = [r for r, row in J['fDispositions'].items() if row['statusChangeOn35'] == 'RE-VERIFIED-ON-PACKAGE12']
chk('package F rows cite package12 (317/317, fb35036f), never package11 figures as current',
    len(pk) == 11 and all('317/317' in J['fDispositions'][r]['currentStatusOn35'] and 'fb35036f' in J['fDispositions'][r]['currentStatusOn35']
                          and '311/311' not in J['fDispositions'][r]['currentStatusOn35'] for r in pk))
leg = sorted(mp + '/' + r for mp in MAPS for r, row in J[mp].items() if row.get('readingStandingLegacyCorrectionOn34'))
chk('nine legacy corrections retained unchanged with a 35 status', leg == r08['legacyCorrections'] and len(leg) == 9
    and all(J[k.split('/')[0]][k.split('/')[1]].get('readingStandingLegacyCorrectionStatusOn35') for k in leg))

print('\n--- closures vs receipts ---')
res = {x['id']: x for x in J['resolvedIssues']}
chk('verdict ACCEPT iff no MUST and no SHOULD', (J['verdict'] == 'ACCEPT') == (not J['newMustIssues'] and not J['newShouldIssues']))
chk('MUST-34-01 CLOSED', res['MUST-34-01']['status'].startswith('CLOSED'))
chk('predictor matrix: 192 cell-ops, 0 mismatches (r02 M1)', g(r02, 'M1-incoming-equals-source35-prose-predictor-on-every-cell')['observed'] == {'cells': 192, 'mismatches': []})
chk('no incoming negative without available binding at U (r02 M2)', g(r02, 'M2-no-incoming-negative-without-an-available-binding-at-U')['passed'])
chk('outgoing 48 cells unchanged 34->35 (r07 M3b)', g(r07, 'M3b-outgoing-invariant-and-equal-corrected-predictor')['observed'] == {'cells': 48, 'changed34to35': [], 'mismatches': []})
m4 = g(r02, 'M4-34-to-35-change-is-exactly-I1')
chk('34->35 change is exactly I1: 92 = 28 value + 64 cause-only (r02 M4)', m4['passed'] and m4['observed'] == {'differingCellOps': 92, 'valueChanges': 28, 'causeOnly': 64})
k1 = g(r02, 'K1-known-matches-and-exceeded-bounds-survive-I1')['observed']
chk('known matches: unbound count<=2 unknown, count<=1 false; bound count<=2 true (r02 K1)',
    k1['unbound']['count<=2'] == 'indeterminate' and k1['unbound']['count<=1'] == 'false' and k1['unbound']['exists'] == 'true' and k1['bound']['count<=2'] == 'true')
p1obs = g(r02, 'P1-one-result-for-every-cell-provider-attestation-and-map-order')['observed']
chk('permutations: 240 / 1,440 / 240 orderings, one result each (r02 P1), and md states those counts',
    [v[0] for v in p1obs.values()] == [240, 1440, 240] and all(v[1] == 1 for v in p1obs.values()) and '240, 1,440 and 240' in MD)
c2b = g(r07, 'C2b-frozen34-carrier-bypasses-closed-on-35')['observed']
chk('A-12 carrier: 18 frozen34 bypasses closed; remaining = 6 dependency-fallback cases (r07 C2b)',
    c2b['closedCount'] == 18 and len(c2b['remaining']) == 6 and all(r[0] == 'dependency-pairing' for r in c2b['remaining']))
chk('A-12 scope-less/empty-scope boundaries and schema metadata-only (r03 E1, E2, S1, S2)',
    all(g(r03, c)['passed'] for c in ('E1-scopeless-and-empty-subject-scope-boundaries', 'E2-empty-subject-scope-never-contains-an-outgoing-subject',
                                      'S1-schema-change-is-metadata-only', 'S2-schema-metadata-now-states-carrier-and-no-untagged-fallback')))
a13 = [a for a in J['advisories'] if a['id'] == 'A-13'][0]
chk('A-13 healed cases equal r07 D1, same on frozen34', sorted(a13['healedCases']) == sorted(g(r07, 'D1-dependency-mapping-fallback-accepts-unselected-scopes-MEASURED')['observed']['healedWithoutValidMatchingScope'])
    and all(v['35'] == v['34'] for k, v in r07['dependencyMappingFallback'].items() if 'control' not in k) and a13['fallbackRowsSameOn34'])
chk('advisories A-9..A-13 each with statusOn35; A-12 closed', [a['id'] for a in J['advisories']] == ['A-9', 'A-10', 'A-11', 'A-12', 'A-13']
    and all(a.get('statusOn35') for a in J['advisories']) and J['advisories'][3]['statusOn35'].startswith('CLOSED'))

print('\n--- package, suites, determinism, planning ---')
ap = J['authorPackageReview']
chk('package12 claims equal r05', ap['members']['verified'] == 317 == r05['verified'] and r05['matchesDeclaredManifest'] and r05['allThirteenAsExpected']
    and r05['queryChecks'] == 7 and r05['allExportsEqualPackage11'] and r05['residualAssessment']['bindsFrozen35'] and r05['myGroupsIncludingReportDigestsMatchRoot'])
chk('suites equal r04: all exit 0, check-atoms 89/0, launcher 16 children rc 0, pins valid',
    r04['allJobsExitZero'] and J['suites']['checkAtoms']['passed'] == 89 and J['suites']['checkAtoms']['failed'] == 0
    and len(r04['launcherReport']['children']) == 16 and all(c['exitCode'] == 0 for c in r04['launcherReport']['children']) and r04['launcherReport']['sourcePinsValid'])
chk('determinism re-measured on frozen35 passes (r06)', r06['passed'] and r06['processes']['distinctDigests'] == 1 and r06['processes']['distinctOrders'] > 1)
chk('layer4 retained equals r01', J['sourceChangeAssessment']['planning']['layer4Retained'] and r01['layer4']['sha34'] == r01['layer4']['sha35']
    and r01['layer4']['pinsResolveAgainst35'] == 29 and not r01['layer4']['pinnedPathsInDelta'])
chk('receipt digests recorded equal files now', all(sha(os.path.join(RC, f)) == d for f, d in J['evidenceReceipts']['receipts'].items()))

print('\n--- obligations ---')
cu = J['crossUnitStanding']
chk('28 / 32-with-0 / condition5 NOT MET / 54-with-0 / D9', cu['condition2ObligationsRetained'] == 28 and cu['qualificationGates'] == 32 and cu['qualificationGatesPerformed'] == 0
    and cu['condition5'] == 'NOT MET' and cu['commitRecoveryCases'] == 54 and cu['commitRecoveryCasesExecuted'] == 0
    and 'DR-007' in cu['d9SuccessorObligation'] and 'DR-011-R08' in cu['d9SuccessorObligation'])
chk('TCB-SCOPE-01 13 rows, not closed', len(J['sharedAssumptionTCBSCOPE01']['dependentRows']) == 13 and 'not closed' in J['sharedAssumptionTCBSCOPE01']['statusOn35'])
chk('30 residuals PENDING, none graded', all(r.get('independentGradeAwardedHere') is None and r.get('reviewStatus') == 'PENDING' for r in J['evaluationResidualDispositions'].values()))
gn = J['grantsNothing']
chk('grants nothing', gn['grade'] is None and not any(gn[k] for k in ('architectureReady', 'activation', 'implementationAuthorized', 'blindAcceptance',
                                                                    'packageAcceptance', 'finalApplicationOutcomeGranted', 'commitOrPush')))
chk('C35-01 correction to my own source34 record present', any(c['id'] == 'C35-01' for c in J['correctionsToMyOwnPriorRecords']))

print('\n--- MD vs JSON ---')
for tok in ('Verdict: ACCEPT', 'MUST-34-01 is CLOSED', 'A-12 is CLOSED', 'A-13', '12,899', '736,823,249', '10 changed', '317/317', '89/89',
            '16/16', '375/375', '192', '91 inherited', '11 F rows', 'nine legacy', 'PENDING', 'DR-011-R08', 'C35-01', 'no application outcome',
            'NOT MET', '28', '54'):
    chk('md states %r' % tok, tok in MD)
chk('md does not present CHANGES_REQUIRED as the current verdict', not re.search(r'Verdict:\s*\**CHANGES_REQUIRED', MD))
C['reviewJsonSha256'] = sha(os.path.join(BASE, 'review.json'))
C['reviewMdSha256'] = sha(os.path.join(BASE, 'review.md'))
C['checks'] = len([v for v in C.values() if isinstance(v, bool)])
C['failed'] = bad
print('\nchecks %d | failed %d %s' % (C['checks'], len(bad), bad))
print('review.json', C['reviewJsonSha256'])
print('review.md  ', C['reviewMdSha256'])
json.dump(C, open(os.path.join(RC, 'i35-invariants.json'), 'w'), indent=1)
