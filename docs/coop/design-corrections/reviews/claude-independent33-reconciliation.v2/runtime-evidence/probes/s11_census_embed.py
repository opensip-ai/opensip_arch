"""S11 — embed the changed-owner transparency census in the record itself, so the report carries the
audit rather than only the probe. Distinguishes rows that NAME the changed owner path from rows that
DESCRIBE the change in prose, and asserts none denies it."""
import hashlib, json, os, re

V2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
P = os.path.join(V2, 'review.json')
N = json.load(open(P))
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
DENY = [r"none of this row's owner files is in my derived", r'nothing in my derived 32->33 delta touches',
        r'is (?:not|neither) in my 32->33 delta', r'is not in my derived 32->33 delta',
        r'neither .{0,60} nor .{0,60} is in my 32->33 delta', r'not in my 32->33 delta']
DESCRIBE = (r'OWNER CHANGED|owner bytes CHANGED|IS in my 18-file delta|the native chapter is|'
            r'changed and was re-read|native chapter changed|native chapter edit|native chapter now agrees|'
            r'composition contract changed|composition change|composition delta|CHANGED in 32->33|'
            r'the new law|the execution law now|now states explicitly|strengthened on 33|'
            r'more precisely on 33|required-execution bridge|in the 32->33 delta')
named, described, denying, silent = [], [], [], []
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in N[mp].items():
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        if not ch:
            continue
        key = mp + '/' + rid
        txt = str(row.get(fld) or '')
        names = any(os.path.basename(p) in txt or p in txt for p in ch)
        desc = bool(re.search(DESCRIBE, txt))
        deny = [p for p in DENY if re.search(p, txt, re.I)]
        if deny and not (names or desc):
            denying.append(key)
        elif names:
            named.append(key)
        elif desc:
            described.append(key)
        else:
            silent.append(key)
N['changedOwnerRowAudit'] = {
    'standing': ('every row whose owner bytes changed 32->33, audited against its OWN changed-owner '
                 'array. This is the invariant that the count-based check in reconciliation v1 did not '
                 'test, and it is the one that let the eight defective rows through.'),
    'changedOwnerRows': len(named) + len(described) + len(denying) + len(silent),
    'rowsNamingTheChangedOwnerPath': sorted(named),
    'rowsDescribingTheChangeWithoutNamingThePath': sorted(described),
    'rowsDenyingTheirOwnChange': sorted(denying),
    'rowsSilentAboutTheirOwnChange': sorted(silent),
    'note': ('rows in the DESCRIBING class state the change and its effect in prose — for example AR-12 '
             '"the native chapter now agrees with execution-inputs §5", FW-03 "the native chapter edit '
             'is the execution-account alignment described under AR-12", DR-011-R01 "the execution law '
             'now states explicitly…". They are accurate as written, so they were left alone rather '
             'than cosmetically rewritten to repeat the path.')}
assert not denying and not silent, (denying, silent)
json.dump(N, open(P, 'w'), indent=1, default=str)
print('changed-owner rows       :', N['changedOwnerRowAudit']['changedOwnerRows'])
print('  naming the path        :', len(named))
print('  describing the change  :', len(described), sorted(described))
print('  denying                :', denying)
print('  silent                 :', silent)
print('sha256:', hashlib.sha256(open(P, 'rb').read()).hexdigest())
