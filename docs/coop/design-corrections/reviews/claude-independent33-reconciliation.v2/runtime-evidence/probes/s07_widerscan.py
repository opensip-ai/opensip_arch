"""S07 — my own wider check, beyond root's seven: does ANY changed-owner row's current text assert
that its owners are not in the delta, under any phrasing? Root named seven; I test all 21."""
import json, os, re

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
V = json.load(open(os.path.join(V1, 'review.json')))
R = {}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
NEG = [r"none of this row's owner files is in my derived", r'nothing in my derived 32->33 delta touches',
       r'is (?:not|neither) in my 32->33 delta', r'is not in my derived 32->33 delta',
       r'neither .{0,60} nor .{0,60} is in my 32->33 delta', r'not in my 32->33 delta']
rows = []
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in V[mp].items():
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        if not ch:
            continue
        txt = str(row.get(fld) or '')
        neg = [p for p in NEG if re.search(p, txt, re.I)]
        rows.append({'row': mp + '/' + rid, 'changed': ch, 'negations': neg, 'text': txt})
R['changedOwnerRows'] = rows
print('changed-owner rows: %d' % len(rows))
flag = [r for r in rows if r['negations']]
R['rowsAssertingNoChange'] = [r['row'] for r in flag]
print('rows whose CURRENT text denies a delta touch: %d' % len(flag))
for r in flag:
    print('\n--- %-46s changed=%s' % (r['row'], r['changed']))
    print('    matched: %s' % r['negations'])
    print('    text   : %s' % r['text'][:300].replace('\n', ' '))
print('\n=== the other changed-owner rows, for contrast ===')
for r in rows:
    if not r['negations']:
        print('  %-46s %s' % (r['row'], r['text'][:130].replace('\n', ' ')))
rootseven = ['arDispositions/AR-13', 'fwDispositions/FW-01', 'fwDispositions/FW-02',
             'fwDispositions/FW-04', 'inheritedResidualDispositions/DR-011-R03',
             'inheritedResidualDispositions/DR-011-R05', 'inheritedResidualDispositions/DR-011-R08']
R['beyondRootsSeven'] = sorted(set(R['rowsAssertingNoChange']) - set(rootseven))
print('\nrows I flag BEYOND root\'s seven:', R['beyondRootsSeven'])
json.dump(R, open(os.path.join(OUT, 's07-widerscan.json'), 'w'), indent=1, default=str)
print('wrote s07-widerscan.json')
