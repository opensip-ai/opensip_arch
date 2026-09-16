"""S12 — back-test the REFINED invariant against the v1 record. A refinement that no longer catches
the defect it was written for is a weakened test, so this is checked, not assumed."""
import json, os, re

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
OUT = os.path.join(V2, 'receipts')
DENY = [r"none of this row's owner files is in my derived", r'nothing in my derived 32->33 delta touches',
        r'is (?:not|neither) in my 32->33 delta', r'is not in my derived 32->33 delta',
        r'neither .{0,60} nor .{0,60} is in my 32->33 delta', r'not in my 32->33 delta']
DESCRIBE = (r'OWNER CHANGED|owner bytes CHANGED|IS in my 18-file delta|the native chapter is|'
            r'changed and was re-read|native chapter changed|native chapter edit|native chapter now agrees|'
            r'composition contract changed|composition change|composition delta|CHANGED in 32->33|'
            r'the new law|the execution law now|now states explicitly|strengthened on 33|'
            r'more precisely on 33|required-execution bridge|in the 32->33 delta')
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}


def run(path):
    V = json.load(open(path))
    fails = []
    for mp in MAPS:
        fld = FIELD.get(mp, 'currentStatusOn33')
        for rid, row in V[mp].items():
            ch = row.get('ownerFilesChangedIn32to33')
            if ch is None:
                ch = row.get('ownerSelectorsChangedIn32to33')
            if not ch:
                continue
            txt = str(row.get(fld) or '')
            names = any(os.path.basename(p) in txt or p in txt for p in ch)
            desc = bool(re.search(DESCRIBE, txt))
            deny = [p for p in DENY if re.search(p, txt, re.I)]
            if not (names or desc):
                fails.append({'row': mp + '/' + rid, 'mode': 'denial' if deny else 'silence'})
    return fails


R = {}
R['v1Failures'] = run(os.path.join(V1, 'review.json'))
R['v2Failures'] = run(os.path.join(V2, 'review.json'))
EXPECT = sorted(['arDispositions/AR-13', 'fwDispositions/FW-01', 'fwDispositions/FW-02',
                 'fwDispositions/FW-04', 'fwDispositions/FW-10',
                 'inheritedResidualDispositions/DR-011-R03',
                 'inheritedResidualDispositions/DR-011-R05',
                 'inheritedResidualDispositions/DR-011-R08'])
got = sorted(f['row'] for f in R['v1Failures'])
R['v1FailureRows'] = got
R['catchesAllEightOnV1'] = got == EXPECT
R['cleanOnV2'] = R['v2Failures'] == []
print('refined invariant run against the v1 record — failures: %d' % len(got))
for f in R['v1Failures']:
    print('   %-46s %s' % (f['row'], f['mode']))
print('\ncatches exactly the eight defective rows on v1:', R['catchesAllEightOnV1'])
print('clean on the v2 record                        :', R['cleanOnV2'])
print('\nDR-007 correctly NOT flagged on either record :',
      'inheritedResidualDispositions/DR-007' not in got)
R['dr007NotFlagged'] = 'inheritedResidualDispositions/DR-007' not in got
json.dump(R, open(os.path.join(OUT, 's12-backtest.json'), 'w'), indent=1, default=str)
print('wrote s12-backtest.json')
