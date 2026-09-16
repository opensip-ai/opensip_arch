"""S00 — verify inputs, then test each of root's four R33-REC2 items against my ACTUAL v1 record and
the frozen33 source. Root evidence is assessed, not rubber-stamped.
"""
import hashlib, json, os, re

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
ROOT = '/tmp/opensip-design-corrections/root-independent33-reconciliation1-assessment.v1/assessment.json'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
os.makedirs(OUT, exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
R['v1JsonSha256'] = sha(os.path.join(V1, 'review.json'))
R['v1MdSha256'] = sha(os.path.join(V1, 'review.md'))
R['v1JsonMatchesRootQuote'] = R['v1JsonSha256'] == 'ad0457bc1e01ac3090335d20b95dedd54dee72a340adf047706c0fc89419c40d'
R['v1MdMatchesRootQuote'] = R['v1MdSha256'] == 'f4015f0ee268a74c807b3d469f4c7aade89e08c3317b62871c784b9f691feb1c'
R['manifestSha256'] = sha(MAN)
R['manifestMatches'] = R['manifestSha256'] == '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
print('v1 json/md match root quotes:', R['v1JsonMatchesRootQuote'], R['v1MdMatchesRootQuote'])
print('frozen33 manifest matches   :', R['manifestMatches'])

V = json.load(open(os.path.join(V1, 'review.json')))
MD = open(os.path.join(V1, 'review.md'), encoding='utf-8').read()
RT = json.load(open(ROOT))

# ---------------- R33-REC2-01: find the contradicting rows MYSELF, then compare with root ----------
print('\n=== R33-REC2-01: current text vs the row\'s own changed-owner array ===')
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
UNCHANGED_CLAIMS = [
    r"none of this row's owner files is in my derived 32->33 delta",
    r'nothing in my derived 32->33 delta touches',
    r'\bUnchanged on 33\b',
]
mine = []
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in V[mp].items():
        txt = str(row.get(fld) or '')
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = [s for s in (row.get('ownerSelectorsChangedIn32to33') or [])]
        claims_none = any(re.search(p, txt) for p in UNCHANGED_CLAIMS[:1])
        if ch and claims_none:
            mine.append({'row': mp + '/' + rid, 'changed': ch, 'field': fld})
R['contradictingRowsIFound'] = mine
rootrows = [r['row'] for r in RT['remaining'][0]['rows']]
R['rootClaimedRows'] = rootrows
R['myRowsMatchRoot'] = sorted(x['row'] for x in mine) == sorted(rootrows)
print('rows I found  :', sorted(x['row'] for x in mine))
print('rows root named:', sorted(rootrows))
print('exact agreement:', R['myRowsMatchRoot'])
# is there any OTHER row whose current text asserts unchanged while its own array says otherwise?
wider = []
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in V[mp].items():
        txt = str(row.get(fld) or '')
        ch = row.get('ownerFilesChangedIn32to33') or row.get('ownerSelectorsChangedIn32to33') or []
        if ch and re.search(r'\bUnchanged on 33\b', txt) and mp + '/' + rid not in [x['row'] for x in mine]:
            wider.append({'row': mp + '/' + rid, 'changed': ch, 'text': txt[:200]})
R['widerUnchangedPhrasingWithChangedOwners'] = wider
print('other rows saying "Unchanged on 33" with a non-empty changed array:', [w['row'] for w in wider])

# how much unique prior reasoning do the seven rows have?
for x in mine:
    mp, rid = x['row'].split('/')
    pf = 'priorBasisOn32' if mp == 'fDispositions' else 'priorStatusOn32'
    x['priorText'] = str(V[mp][rid].get(pf) or '')
    x['currentText'] = str(V[mp][rid].get(x['field']) or '')
    x['ownerFiles'] = V[mp][rid].get('currentOwnerFiles') or V[mp][rid].get('currentOwnerSelectors')
    x['unchangedOwners'] = V[mp][rid].get('ownerFilesUnchangedIn32to33')
    print('\n--- %s\n    changed : %s\n    prior   : %s' % (x['row'], x['changed'], x['priorText'][:220]))

# ---------------- R33-REC2-02 ----------------
print('\n=== R33-REC2-02: evidenceReceipts.authorPackage ===')
ap = V['evidenceReceipts'].get('authorPackage')
R['authorPackageReceiptActual'] = ap
R['authorPackageReviewStatus'] = V['authorPackageReview']['status']
print('evidenceReceipts.authorPackage :', json.dumps(ap, default=str)[:400])
print('authorPackageReview.status     :', R['authorPackageReviewStatus'])
R['REC2_02_contradictionConfirmed'] = (
    isinstance(ap, dict) and 'INCOMPLETE' in json.dumps(ap).upper()
    and 'COMPLETE' in V['authorPackageReview']['status'].upper())
print('contradiction confirmed        :', R['REC2_02_contradictionConfirmed'])

# ---------------- R33-REC2-03 ----------------
print('\n=== R33-REC2-03: required selected-U unsupported bridge cause ===')
R['mdBridgeSentence'] = [l for l in MD.splitlines() if 'bridges to an indeterminate Run' in l]
print('md sentence:', R['mdBridgeSentence'])
fr = json.dumps(V['sourceChangeAssessment']['executionInputsLaw'].get('fullRunColumn'), default=str)
R['fullRunColumnRows'] = V['sourceChangeAssessment']['executionInputsLaw']['fullRunColumn'].get('rows')
print('fullRunColumn.rows:', json.dumps(R['fullRunColumnRows'], default=str)[:900])
blob = json.dumps(V, default=str)
for key in ('full-run-required-unsupported-matrix-pair-bridge', 'required-cell-unsatisfied',
            'language-tier-unsupported', 'capability-missing'):
    idxs = [m.start() for m in re.finditer(re.escape(key), blob)]
    R['jsonMentions_' + key] = len(idxs)
    print('%-48s mentioned %d time(s) in my v1 json' % (key, len(idxs)))
json.dump(R, open(os.path.join(OUT, 's00-verify.json'), 'w'), indent=1, default=str)
print('\nwrote s00-verify.json')
