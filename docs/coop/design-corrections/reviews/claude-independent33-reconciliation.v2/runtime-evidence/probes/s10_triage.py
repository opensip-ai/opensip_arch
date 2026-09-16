"""S10 — triage the two invariant failures honestly: is the record wrong, or is the check wrong?"""
import json, os, re

V2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
N = json.load(open(os.path.join(V2, 'review.json')))
MD = open(os.path.join(V2, 'review.md'), encoding='utf-8').read()
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
ACK = (r'OWNER CHANGED|owner bytes CHANGED|IS in my 18-file delta|the native chapter is|'
       r'changed and was re-read|native chapter changed|composition contract changed|'
       r'is in my derived delta|CHANGED in 32->33')
print('=== every changed-owner row, with what its current text actually says about the change ===')
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in N[mp].items():
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        if not ch:
            continue
        txt = str(row.get(fld) or '')
        names = any(os.path.basename(p) in txt or p in txt for p in ch)
        ack = bool(re.search(ACK, txt))
        mark = 'ok ' if (names or ack) else '>>>'
        print('\n%s %-46s names=%-5s ackPhrase=%-5s changed=%s'
              % (mark, mp + '/' + rid, names, ack, [os.path.basename(p) for p in ch]))
        print('    %s' % txt[:300].replace('\n', ' '))

print('\n\n=== MD occurrences of the withdrawn sentence, with context ===')
for m in re.finditer(re.escape('bridges to an indeterminate Run through `required-cell-unsatisfied`'), MD):
    lo, hi = max(0, m.start() - 320), min(len(MD), m.end() + 160)
    print('--- occurrence at %d ---' % m.start())
    print(MD[lo:hi].replace('\n', ' '))
    quoted = bool(re.search(r'my v1 MD said|corrected|dropping the null-deficiency precondition',
                            MD[lo:hi]))
    print('    quoted-as-corrected:', quoted)
