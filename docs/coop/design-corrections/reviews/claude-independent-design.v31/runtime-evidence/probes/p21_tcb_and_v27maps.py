"""PROBE 21 (v31) — re-decide the TCB-SCOPE-01 dependent set on CURRENT bytes by reading each
row's reasoning, and load my v27 maps so every row can be re-decided for 31 (never copied)."""
import json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
V27 = '/tmp/opensip-design-corrections/claude-independent-design.v27'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
items = {i['id']: i for i in era['items']}
declared = era['sharedReviewDependencies'][0]['dependentResidualIds']
R = {'declared': declared}

# the three rows my v27 keyword pass disagreed on, re-read on current bytes
print('=== rows whose TCB dependence I decide by reading, not by keyword ===')
for rid in ('RES-EP13-13', 'IR-EP13-NB-02', 'IR-EP13-NB-06'):
    it = items[rid]
    print('\n--- %s (declared dependent: %s) ---' % (rid, rid in declared))
    print('  correction: %s' % str(it.get('sourceCorrection'))[:300])
    print('  rationale : %s' % str(it.get('rationale'))[:300])
    print('  limits    : %s' % str(it.get('limits'))[:220])
    R.setdefault('readRows', {})[rid] = {k: it.get(k) for k in
                                         ('sourceCorrection', 'rationale', 'limits')}

# does any NON-declared row rest on the same move?
nondeclared = [i for i in era['items'] if i['id'] not in declared]
R['nonDeclaredCount'] = len(nondeclared)
print('\n=== non-declared rows: does the disposition rest on the TCB move? ===')
for i in nondeclared:
    txt = (str(i.get('sourceCorrection')) + ' ' + str(i.get('rationale'))).lower()
    rests = ('same-process' in txt or 'hostile' in txt or 'tcb' in txt
             or 'trusted' in txt and 'evaluator' in txt)
    print('  %-16s restsOnTcbLanguage=%-5s  %s' % (i['id'], rests,
                                                   str(i.get('sourceCorrection'))[:95]))
    R.setdefault('nonDeclaredScan', {})[i['id']] = rests

# ---- my v27 maps ----
v27 = json.load(open(os.path.join(V27, 'review.json')))
R['v27Verdict'] = v27['verdict']
R['v27Sha256Note'] = 'root assessment pins my v27 review at 4cb03aa8438c07757bb67ee0fc8435fe1feae561ebb320b4b13d9451acc32ad2'
for key in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
            'scopedReviewOwnerDispositions', 'fDispositions', 'evaluationResidualDispositions'):
    v = v27.get(key)
    R.setdefault('v27MapSizes', {})[key] = len(v) if v else 0
print('\nv27 map sizes:', json.dumps(R.get('v27MapSizes')))
R['v27Advisories'] = [a['id'] for a in v27.get('advisories', [])]
R['v27NewMust'] = v27.get('newMustIssues')
R['v27NewShould'] = v27.get('newShouldIssues')
print('v27 advisories:', R['v27Advisories'], '| must:', len(R['v27NewMust']), '| should:', len(R['v27NewShould']))

# the v27 rows whose CURRENT scope/basis fields root flagged as stale (RR27-02/03/04)
FLAGGED = ['AR-09', 'AR-14', 'AR-15', 'FW-06', 'DR-001', 'DR-006', 'DR-009', 'DR-011-R10', 'DR-202',
           'AR-01', 'FW-01', 'FW-02', 'FW-10', 'DR-003', 'DR-004', 'DR-005', 'DR-008', 'DR-011-R06',
           'DR-204']
out = {}
for key in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
            'scopedReviewOwnerDispositions'):
    for rid, row in (v27.get(key) or {}).items():
        if rid in FLAGGED:
            out[rid] = {'map': key, 'scope': row.get('scope'), 'basis': str(row.get('basis'))[:260],
                        'ownerBytesChangedIn27': row.get('ownerBytesChangedIn27'),
                        'owningSection': row.get('owningSection'),
                        'v26IssuesNowResolved': row.get('v26IssuesNowResolved')}
R['v27FlaggedRows'] = out
print('\nrows root flagged for stale current fields (%d):' % len(out))
for rid, r in sorted(out.items()):
    print('  %-12s %-32s scope=%s' % (rid, str(r['map'])[:32], str(r['scope'])[:90]))

json.dump(R, open(os.path.join(OUT, 'p21-tcb-v27maps.json'), 'w'), indent=1, default=str)
print('\nwrote p21-tcb-v27maps.json')
