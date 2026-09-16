"""R05 — final consistency check of the corrected record. Fails loudly rather than quietly passing."""
import hashlib, json, os, re

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
C = {}
bad = []


def chk(name, cond, detail=''):
    C[name] = bool(cond)
    print('%-52s %s %s' % (name, 'OK ' if cond else 'FAIL', detail))
    if not cond:
        bad.append(name)


N = json.load(open(os.path.join(BASE, 'review.json')))
O = json.load(open(os.path.join(V33, 'review.json')))
MD = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
man = json.load(open(MAN))
man_paths = {f['path'] for f in man['files']}

# 1. subject still immutable
drift = sum(1 for f in man['files']
            if not os.path.isfile(os.path.join(SRC, f['path']))
            or hashlib.sha256(open(os.path.join(SRC, f['path']), 'rb').read()).hexdigest() != f['sha256'])
chk('frozen33 files', len(man_paths) == 12899, str(len(man_paths)))
chk('frozen33 manifest digest', hashlib.sha256(open(MAN, 'rb').read()).hexdigest() ==
    '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299')
chk('frozen33 drift after all work', drift == 0, str(drift))

# 2. superseded record untouched
chk('old review.json preserved byte-identical',
    hashlib.sha256(open(os.path.join(V33, 'review.json'), 'rb').read()).hexdigest() ==
    '800465853d626f49cdbaf48af2066b6a8e3e65f364d2a21a9263ab88a2eb0b90')
chk('old review.md preserved byte-identical',
    hashlib.sha256(open(os.path.join(V33, 'review.md'), 'rb').read()).hexdigest() ==
    'f2f8a871ffaaee1c76aefb3b70bc30f9a65144fc85191e657ee9d103c03e77f3')

# 3. all 107 rows, counts, flags
MAPS = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16,
        'fwDispositions': 15, 'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5}
FIELD = {'fDispositions': ('currentBasisOn33', 'priorBasisOn32')}
tot = 0
flags_ok = priors_ok = standing_ok = hist_ok = 0
for mp, n in MAPS.items():
    chk('map %s has %d rows' % (mp, n), len(N[mp]) == n, str(len(N[mp])))
    chk('map %s ids identical to source33 record' % mp, list(N[mp]) == list(O[mp]))
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in N[mp].items():
        tot += 1
        if row.get('appliedByThisReview') is False and row.get('finalApplicationOutcomeGranted') is False:
            flags_ok += 1
        if row.get(pf) == O[mp][rid].get(pf):
            priors_ok += 1
        if row.get('currentFieldStandingOn33'):
            standing_ok += 1
        if '[HISTORY:' in str(row.get(fld) or ''):
            hist_ok += 1
chk('total rows = 107', tot == 107, str(tot))
chk('both authority flags false on every row', flags_ok == 107, str(flags_ok))
chk('every prior field byte-identical to source33 record', priors_ok == 107, str(priors_ok))
chk('every row carries currentFieldStandingOn33', standing_ok == 107, str(standing_ok))
chk('every current field carries the HISTORY pointer', hist_ok == 107, str(hist_ok))

# 4. no stale source32 fact left in any CURRENT field (history clause excluded)
STALE = [r'\b277\b', r'12,?898', r'frozen32', r'snapshot32', r'implementation-normative-inputs\.v3',
         r'31->32', r'\bon 32\b', r'against frozen32']
hits = []
for mp in MAPS:
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in N[mp].items():
        txt = re.sub(r'\[HISTORY:[^\]]*\]', '', str(row.get(fld) or ''))
        for pat in STALE:
            m = re.search(pat, txt, re.I)
            if m:
                hits.append((mp + '/' + rid, pat, txt[max(0, m.start() - 70):m.start() + 90]))
chk('no stale 32-era fact in any current field', not hits, str(hits[:3]))

# 5. owner/delta arrays still match the actual 18-file delta
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
DELTA = set([c['path'] for c in p01['changed']] + [a['path'] for a in p01['added']])
chk('derived delta is 18 files', len(DELTA) == 18, str(len(DELTA)))
chk('delta32to33 block still says 1/0/17/18',
    (N['delta32to33']['added'], N['delta32to33']['removed'], N['delta32to33']['changed'],
     N['delta32to33']['touched']) == (1, 0, 17, 18))
ownermaps = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
             'scopedReviewOwnerDispositions', 'evaluationResidualDispositions')
arr_bad = []
for mp in ownermaps:
    for rid, row in N[mp].items():
        ch = row.get('ownerFilesChangedIn32to33')
        un = row.get('ownerFilesUnchangedIn32to33')
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors')
        if ch is None:
            continue
        paths = [p if isinstance(p, str) else p.get('path') for p in (own or [])]
        paths = [p.split('#')[0] for p in paths if isinstance(p, str)]
        if set(ch) - DELTA:
            arr_bad.append((mp + '/' + rid, 'changed-array not a subset of the delta', sorted(set(ch) - DELTA)))
        if un is not None and set(un) & DELTA:
            arr_bad.append((mp + '/' + rid, 'unchanged-array intersects the delta', sorted(set(un) & DELTA)))
        if un is not None and own is not None and set(ch) | set(un) != set(paths):
            arr_bad.append((mp + '/' + rid, 'changed+unchanged != owner set', paths))
        miss = [p for p in paths if p not in man_paths]
        if miss:
            arr_bad.append((mp + '/' + rid, 'owner path not in frozen33', miss))
chk('all owner/delta arrays consistent with the 18-file delta', not arr_bad, str(arr_bad[:3]))
chk('DR-204 owners now name layer4',
    'docs/v2/architecture/implementation-normative-inputs.v4.json'
    in N['scopedReviewOwnerDispositions']['DR-204']['currentOwnerFiles'])

# 6. verdict, obligations, advisories, ledger
chk('verdict still ACCEPT', N['verdict'] == 'ACCEPT', N['verdict'])
cu = N['crossUnitStanding']
chk('28 condition-2 obligations retained', cu['condition2ObligationsRetained'] == 28)
chk('32 gates, 0 performed, condition 5 NOT MET',
    cu['qualificationGates'] == 32 and cu['qualificationGatesPerformed'] == 0 and cu['condition5'] == 'NOT MET')
chk('54 recovery cases, 0 executed',
    cu['commitRecoveryCases'] == 54 and cu['commitRecoveryCasesExecuted'] == 0)
chk('D9 obligation names DR-007 and DR-011-R08',
    'DR-007' in cu['d9SuccessorObligation'] and 'DR-011-R08' in cu['d9SuccessorObligation'])
chk('TCB-SCOPE-01 joint reopening over 13 rows',
    len(N['sharedAssumptionTCBSCOPE01'].get('dependentRows') or
        N['sharedAssumptionTCBSCOPE01'].get('dependentResidualIds') or []) == 13,
    str(list(N['sharedAssumptionTCBSCOPE01'])))
pend = sum(1 for r in N['evaluationResidualDispositions'].values()
           if str(r.get('independentGradeAwardedHere')).lower() in ('false', 'none', 'null', 'pending'))
chk('no residual graded here (30 pending)', pend == 30, str(pend))
gn = N['grantsNothing']
chk('grantsNothing all false/none',
    gn['grade'] is None and not gn['architectureReady'] and not gn['activation']
    and not gn['implementationAuthorized'] and not gn['blindAcceptance']
    and not gn['finalApplicationOutcomeGranted'] and not gn['commitOrPush'])
chk('advisories A-9 A-10 A-11 present', [a['id'] for a in N['advisories']] == ['A-9', 'A-10', 'A-11'])
chk('ledger carries all five items',
    [i['id'] for i in N['correctionLedgerR33REC']['items']] ==
    ['R33-REC-01', 'R33-REC-02', 'R33-REC-03', 'R33-REC-04', 'R33-REC-05'])
chk('every ledger item has evidence + selectors',
    all(i.get('evidence') and i.get('affectedSelectors') for i in N['correctionLedgerR33REC']['items']))

# 7. the withdrawn claims are actually gone, and the corrections are actually present
body = json.dumps(N)
chk('overclaim phrase no longer asserted as a finding',
    'not forced to execute a provider to close' not in
    json.dumps(N['sourceChangeAssessment']['executionInputsLaw']['requestVersusSelectionVersusDisclosure']
               ['assessment']))
chk('full-Run binding now cites line 751',
    '751' in N['sourceChangeAssessment']['executionInputsLaw']['fullRunColumn']['digestBindingExactSelector'])
chk('helper-unit standing named in the correction',
    'helper-unit' in N['sourceChangeAssessment']['executionInputsLaw']['fullRunColumn']['correctionR33REC03'])
chk('SOURCE_ORDER stated at whole-cell level',
    'SOURCE_ORDER' in N['sourceChangeAssessment']['executionInputsLaw']['mixedTypedAndUntypedSources']
    ['wholeCellCrossSourceOrder'])
chk('new full-Run control runId recorded',
    'run3:a6a17e18de4555538b55defc75925113ff96946403316e322eeeb5a3c1de189a' in body)
chk('control standing declared as root-authored, independently executed',
    'root-authored control' in body and 'NOT a new independent consumer implementation' in body)
chk('p09 error preserved, not erased',
    any('p09' in str(x) for x in N['evidenceReceipts']['failedOrImpreciseProbesPreserved']))

# 8. md/json agreement on the load-bearing numbers
for tok in ('12,899', '305/305', '18', '107', '28', '32', '54', 'run3:a6a17e18', '751',
            'helper-unit', 'DR-011-R08', 'ACCEPT'):
    chk('md states %r' % tok, tok in MD)
chk('md carries the ledger section', '## 7. Correction ledger' in MD)
chk('md states the remaining blocker', '## 8. Remaining blocker' in MD)

C['reviewJsonSha256'] = hashlib.sha256(open(os.path.join(BASE, 'review.json'), 'rb').read()).hexdigest()
C['reviewMdSha256'] = hashlib.sha256(open(os.path.join(BASE, 'review.md'), 'rb').read()).hexdigest()
C['checksRun'] = len([k for k in C if isinstance(C[k], bool)])
C['failed'] = bad
print('\nchecks run: %d | failed: %d' % (C['checksRun'], len(bad)))
print('review.json sha256:', C['reviewJsonSha256'])
print('review.md   sha256:', C['reviewMdSha256'])
json.dump(C, open(os.path.join(BASE, 'receipts', 'r05-consistency.json'), 'w'), indent=1, default=str)
print('wrote r05-consistency.json')
