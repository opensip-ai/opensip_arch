"""S09 — meaningful report invariants, not counts. Each one is a claim that could actually be false:
current assertions against the rows' own changed-owner arrays, current-vs-historical package receipt
consistency, and the required-cell bridge cause checked against the retained measurement AND the
frozen source rule. Fails loudly."""
import hashlib, json, os, re

V2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
C, bad = {}, []


def chk(name, cond, detail=''):
    C[name] = bool(cond)
    print('%-58s %s %s' % (name, 'OK ' if cond else 'FAIL', detail))
    if not cond:
        bad.append(name)


N = json.load(open(os.path.join(V2, 'review.json')))
O1 = json.load(open(os.path.join(V1, 'review.json')))
O33 = json.load(open(os.path.join(V33, 'review.json')))
MD = open(os.path.join(V2, 'review.md'), encoding='utf-8').read()
man = json.load(open(MAN))
manp = {f['path'] for f in man['files']}
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
DELTA = set([c['path'] for c in p01['changed']] + [a['path'] for a in p01['added']])
MAPS = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16,
        'fwDispositions': 15, 'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5}
FIELD = {'fDispositions': ('currentBasisOn33', 'priorBasisOn32')}

print('--- subject and preserved records ---')
drift = sum(1 for f in man['files']
            if not os.path.isfile(os.path.join(SRC, f['path']))
            or hashlib.sha256(open(os.path.join(SRC, f['path']), 'rb').read()).hexdigest() != f['sha256'])
chk('frozen33 immutable: 12,899 files, 0 drift', len(manp) == 12899 and drift == 0, 'drift=%d' % drift)
chk('v33 report preserved byte-identical',
    hashlib.sha256(open(os.path.join(V33, 'review.json'), 'rb').read()).hexdigest() ==
    '800465853d626f49cdbaf48af2066b6a8e3e65f364d2a21a9263ab88a2eb0b90' and
    hashlib.sha256(open(os.path.join(V33, 'review.md'), 'rb').read()).hexdigest() ==
    'f2f8a871ffaaee1c76aefb3b70bc30f9a65144fc85191e657ee9d103c03e77f3')
chk('v1 report preserved byte-identical',
    hashlib.sha256(open(os.path.join(V1, 'review.json'), 'rb').read()).hexdigest() ==
    'ad0457bc1e01ac3090335d20b95dedd54dee72a340adf047706c0fc89419c40d' and
    hashlib.sha256(open(os.path.join(V1, 'review.md'), 'rb').read()).hexdigest() ==
    'f4015f0ee268a74c807b3d469f4c7aade89e08c3317b62871c784b9f691feb1c')

print('\n--- INVARIANT 1: every current assertion agrees with its own changed-owner array ---')
DENY = [r"none of this row's owner files is in my derived", r'nothing in my derived 32->33 delta touches',
        r'is (?:not|neither) in my 32->33 delta', r'is not in my derived 32->33 delta',
        r'neither .{0,60} nor .{0,60} is in my 32->33 delta', r'not in my 32->33 delta']
# A row satisfies this invariant by NAMING the changed owner path or by AFFIRMATIVELY describing the
# change. Silence or denial fails. The describing class is legitimate and is censused separately in
# $.changedOwnerRowAudit rather than cosmetically rewritten.
DESCRIBE = (r'OWNER CHANGED|owner bytes CHANGED|IS in my 18-file delta|the native chapter is|'
            r'changed and was re-read|native chapter changed|native chapter edit|native chapter now agrees|'
            r'composition contract changed|composition change|composition delta|CHANGED in 32->33|'
            r'the new law|the execution law now|now states explicitly|strengthened on 33|'
            r'more precisely on 33|required-execution bridge|in the 32->33 delta')
viol, changed_rows, inherit_on_changed, both_clauses = [], [], [], []
named_rows, described_rows = [], []
for mp in MAPS:
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in N[mp].items():
        key = mp + '/' + rid
        txt = str(row.get(fld) or '')
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        if '[HISTORY:' in txt and '[INHERITED:' in txt:
            both_clauses.append(key)
        if ch:
            changed_rows.append(key)
            if '[INHERITED:' in txt:
                inherit_on_changed.append(key)
            names = any(os.path.basename(p) in txt or p in txt for p in ch)
            ack = bool(re.search(DESCRIBE, txt))
            denies = [p for p in DENY if re.search(p, txt, re.I)]
            if denies and not (names or ack):
                viol.append({'row': key, 'changed': ch, 'denials': denies, 'text': txt[:180]})
            elif not (names or ack):
                viol.append({'row': key, 'changed': ch, 'why': 'silent about its own change',
                             'text': txt[:180]})
            elif names:
                named_rows.append(key)
            else:
                described_rows.append(key)
chk('no changed-owner row denies or is silent about its own change', not viol, json.dumps(viol[:2])[:260])
aud = N['changedOwnerRowAudit']
chk('embedded changed-owner audit matches a live recount',
    sorted(aud['rowsNamingTheChangedOwnerPath']) == sorted(named_rows)
    and sorted(aud['rowsDescribingTheChangeWithoutNamingThePath']) == sorted(described_rows)
    and aud['rowsDenyingTheirOwnChange'] == [] and aud['rowsSilentAboutTheirOwnChange'] == [],
    '%d named / %d described' % (len(named_rows), len(described_rows)))
chk('changed-owner rows counted = 21', len(changed_rows) == 21, str(len(changed_rows)))
chk('no INHERITED clause on a changed-owner row', not inherit_on_changed, str(inherit_on_changed))
chk('no row carries both HISTORY and INHERITED', not both_clauses, str(both_clauses))
# inheritance is only claimed where owners are byte-verified unchanged AND resolve in frozen33
badinh = []
for mp in MAPS:
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in N[mp].items():
        if '[INHERITED:' not in str(row.get(fld) or ''):
            continue
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        res = row.get('ownerPathsResolveInFrozen33') or row.get('ownerSelectorsResolveInFrozen33')
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = [p.split('#')[0] for p in own if isinstance(p, str)]
        if ch != [] or res is not True or any(p not in manp for p in paths) or \
                any(p in DELTA for p in paths):
            badinh.append(mp + '/' + rid)
chk('INHERITED only where owners verified unchanged and resolve', not badinh, str(badinh[:3]))
chk('the 8 corrected rows all name their changed owner',
    all(any(os.path.basename(p) in str(N[m][r].get('currentStatusOn33'))
            for p in (N[m][r].get('ownerFilesChangedIn32to33') or
                      N[m][r].get('ownerSelectorsChangedIn32to33') or []))
        for m, r in (('arDispositions', 'AR-13'), ('fwDispositions', 'FW-01'), ('fwDispositions', 'FW-02'),
                     ('fwDispositions', 'FW-04'), ('fwDispositions', 'FW-10'),
                     ('inheritedResidualDispositions', 'DR-011-R03'),
                     ('inheritedResidualDispositions', 'DR-011-R05'),
                     ('inheritedResidualDispositions', 'DR-011-R08'))))
chk('DR-007 left unchanged from v1 (assessed, not a defect)',
    N['inheritedResidualDispositions']['DR-007']['currentStatusOn33'] ==
    O1['inheritedResidualDispositions']['DR-007']['currentStatusOn33'])

print('\n--- INVARIANT 2: current vs historical package receipt consistency ---')
ap = N['evidenceReceipts']['authorPackage']
chk('authorPackage current status agrees with authorPackageReview',
    'COMPLETE' in ap['status'].upper() and 'COMPLETE' in N['authorPackageReview']['status'].upper()
    and 'INCOMPLETE' not in ap['status'].upper())
chk('current pointer binds the READY root input digest',
    ap['currentMeasurement']['rootInputSha256'] ==
    N['authorPackageReview']['rootInputConsumed']['readyVersionSha256'])
chk('pending digest appears ONLY under the historical label',
    ap['historicalP11']['rootInputSha256'] == '5ac4a3ec6af9cf169713dd0e7e54a7d46e6230b7d61de7e4692118acc8d1b785'
    and json.dumps(ap['currentMeasurement']).find('5ac4a3ec') == -1
    and 'HISTORICAL' in ap['historicalP11']['standing'].upper())
chk('p11 preserved, not deleted', bool(ap['historicalP11'].get('receipt')) and
    ap['historicalP11']['status'] == 'INCOMPLETE')
chk('current package numbers equal the actual p12/p13 measurement',
    ap['currentMeasurement']['artifactManifestSha256'] ==
    '88c38b160e8b3af2702c0975271e10a765cd551b7245e8ac6f963887ef3551d2'
    and ap['currentMeasurement']['sourceFilesVerified'] == 12899
    and ap['currentMeasurement']['packageFilesVerified'] == 305
    and ap['currentMeasurement']['sourceManifestEqualsFrozen33'] is True)
# no OTHER current field may still assert an incomplete package
stale = []
for k, v in N['evidenceReceipts'].items():
    if k == 'authorPackage':
        continue
    if re.search(r'"status":\s*"INCOMPLETE"', json.dumps(v)):
        stale.append(k)
chk('no other evidence receipt asserts INCOMPLETE', not stale, str(stale))

print('\n--- INVARIANT 3: required-cell bridge cause matches source rule AND retained measurement ---')
rows = {r['case']: r for r in N['evidenceReceipts']['fullRunRows']}
mtx = rows['full-run-required-unsupported-matrix-pair-bridge']
chk('retained matrix case carries the MATRIX pair, not the fallback',
    ['language-tier-unsupported', 'capability-missing'] in [list(p) for p in mtx['causePairs']]
    and not any(p[0] == 'required-cell-unsatisfied' for p in mtx['causePairs']))
pure = [rows['full-run-empty-returned-partitions-bridge-required-cell-unsatisfied'],
        rows['full-run-census-missing-subjects-bridge-keeps-originating-coverage']]
chk('pure missing-work cases carry required-cell-unsatisfied',
    all(any(p[0] == 'required-cell-unsatisfied' for p in r['causePairs']) for r in pure))
mixed = rows['full-run-mixed-accounts-first-typed-pair']
chk('mixed case carries a typed cause AND the fallback in one Run',
    {p[0] for p in mixed['causePairs']} == {'budget-exhausted', 'required-cell-unsatisfied'})
# the source rule itself
CHK = os.path.join(SRC, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
L = open(CHK, encoding='utf-8').read().splitlines()
src = '\n'.join(L[713:721])
chk('bridge_cause returns the deficiency when registered', 'return deficiency' in src and 'registered' in src)
chk('bridge_cause falls back only for null / source-syntax-invalid',
    'in (None, "source-syntax-invalid")' in src and 'required-cell-unsatisfied' in src)
reg = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'))
                )['x-opensip-evaluator-deficiency-registry']['sources']['execution']
chk('language-tier-unsupported is a REGISTERED execution deficiency', 'language-tier-unsupported' in reg)
rule = N['sourceChangeAssessment']['executionInputsLaw']['requiredCellBridgeAndUniqueness']['exactCauseRule']
chk('JSON rule states registered->itself and null->fallback',
    'REGISTERED' in rule and 'source-syntax-invalid' in rule and '714-721' in rule)
# the MD must not ASSERT the v1 conflation. Quoting it as withdrawn is required, not forbidden, so
# every occurrence must sit inside a correction context.
occ = list(re.finditer(re.escape('bridges to an indeterminate Run through `required-cell-unsatisfied`'), MD))
chk('every MD occurrence of the withdrawn sentence is quoted as corrected',
    bool(occ) and all(re.search(r'my v1 MD said|corrected|dropping the null-deficiency precondition',
                                MD[max(0, m.start() - 320):m.end() + 160]) for m in occ),
    '%d occurrence(s)' % len(occ))
chk('MD states the matrix pair for the matrix case',
    'language-tier-unsupported' in MD and 'capability-missing' in MD)
chk('MD states the null-deficiency precondition',
    re.search(r'only.{0,40}`?null`?', MD) is not None and 'source-syntax-invalid' in MD)

print('\n--- structural invariants carried forward ---')
tot = flags = priors1 = priors33 = 0
for mp, n in MAPS.items():
    chk('map %s has %d rows' % (mp, n), len(N[mp]) == n, str(len(N[mp])))
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in N[mp].items():
        tot += 1
        if row.get('appliedByThisReview') is False and row.get('finalApplicationOutcomeGranted') is False:
            flags += 1
        if row.get(pf) == O1[mp][rid].get(pf):
            priors1 += 1
        if row.get(pf) == O33[mp][rid].get(pf):
            priors33 += 1
chk('107 rows', tot == 107, str(tot))
chk('both authority flags false on every row', flags == 107, str(flags))
chk('prior fields identical to v1 AND to the source33 record', priors1 == 107 and priors33 == 107,
    '%d/%d' % (priors1, priors33))
arr = []
for mp in MAPS:
    for rid, row in N[mp].items():
        ch = row.get('ownerFilesChangedIn32to33')
        un = row.get('ownerFilesUnchangedIn32to33')
        own = row.get('currentOwnerFiles')
        if ch is None or un is None or own is None:
            continue
        if set(ch) - DELTA or set(un) & DELTA or set(ch) | set(un) != set(own) or any(p not in manp for p in own):
            arr.append(mp + '/' + rid)
chk('owner/delta arrays consistent with the 18-file delta', not arr, str(arr[:3]))
cu = N['crossUnitStanding']
chk('28 / 32-with-0 / condition5 NOT MET / 54-with-0 all carried',
    cu['condition2ObligationsRetained'] == 28 and cu['qualificationGates'] == 32
    and cu['qualificationGatesPerformed'] == 0 and cu['condition5'] == 'NOT MET'
    and cu['commitRecoveryCases'] == 54 and cu['commitRecoveryCasesExecuted'] == 0)
chk('D9 obligation still names DR-007 and DR-011-R08 as open',
    'DR-007' in cu['d9SuccessorObligation'] and 'DR-011-R08' in cu['d9SuccessorObligation'])
chk('TCB-SCOPE-01 still open over 13 rows, not closed here',
    len(N['sharedAssumptionTCBSCOPE01'].get('dependentRows') or []) == 13
    and N['sharedAssumptionTCBSCOPE01'].get('adjudicationOwner') is not None)
chk('no residual graded here',
    all(r.get('independentGradeAwardedHere') in (None, False, 'PENDING')
        for r in N['evaluationResidualDispositions'].values()))
gn = N['grantsNothing']
chk('grantsNothing unchanged and all false/none',
    gn == O1['grantsNothing'] and gn['grade'] is None and not gn['commitOrPush'])
chk('verdict still ACCEPT', N['verdict'] == 'ACCEPT', N['verdict'])
chk('ledger carries the four root items',
    [i['id'] for i in N['correctionLedgerR33REC2']['items']] ==
    ['R33-REC2-01', 'R33-REC2-02', 'R33-REC2-03', 'R33-REC2-04'])
chk('ledger records my own extra finding and the rejected pattern match',
    N['correctionLedgerR33REC2']['additionalDefectFoundByMe']['row'] == 'fwDispositions/FW-10'
    and N['correctionLedgerR33REC2']['rootPatternCheckedAndRejected']['row'] ==
    'inheritedResidualDispositions/DR-007')
chk('v1 ledger preserved alongside the new one', 'correctionLedgerR33REC' in N
    and len(N['correctionLedgerR33REC']['items']) == 5)
chk('MD states no new source defect and no source34',
    'No new source defect' in MD and 'no source34 is requested' in MD.replace('**', ''))

C['reviewJsonSha256'] = hashlib.sha256(open(os.path.join(V2, 'review.json'), 'rb').read()).hexdigest()
C['reviewMdSha256'] = hashlib.sha256(open(os.path.join(V2, 'review.md'), 'rb').read()).hexdigest()
C['checksRun'] = len([k for k in C if isinstance(C[k], bool)])
C['failed'] = bad
print('\nchecks run: %d | failed: %d' % (C['checksRun'], len(bad)))
print('review.json sha256:', C['reviewJsonSha256'])
print('review.md   sha256:', C['reviewMdSha256'])
json.dump(C, open(os.path.join(V2, 'receipts', 's09-invariants.json'), 'w'), indent=1, default=str)
print('wrote s09-invariants.json')
