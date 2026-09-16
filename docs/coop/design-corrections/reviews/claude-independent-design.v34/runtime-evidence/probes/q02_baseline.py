"""Q02 — baseline audit. Verify the corrected source33 record, then map every row's owners onto the
INDEPENDENT 33->34 delta, and find stale legacy readingStanding strings."""
import hashlib, json, os, re

B2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
q00 = json.load(open(os.path.join(OUT, 'q00-custody.json')))
R = {}
R['baselineJsonSha256'] = hashlib.sha256(open(os.path.join(B2, 'review.json'), 'rb').read()).hexdigest()
R['baselineMdSha256'] = hashlib.sha256(open(os.path.join(B2, 'review.md'), 'rb').read()).hexdigest()
R['baselineMatches'] = R['baselineJsonSha256'] == '89f4bd73ea4168286102c90d02020f2ee514a52e81280d186d05b78a3b6c4533'
print('baseline json sha matches:', R['baselineMatches'], '| md sha:', R['baselineMdSha256'])
V = json.load(open(os.path.join(B2, 'review.json')))
m34 = {f['path'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
DELTA = {c['path'] for c in q00['delta']['changed']}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
R['counts'] = {mp: len(V[mp]) for mp in MAPS}
print('counts:', R['counts'], 'total', sum(R['counts'].values()))

rows, touched, unres, stale = [], [], [], []
for mp in MAPS:
    for rid, row in V[mp].items():
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        hit = sorted(p for p in paths if p in DELTA)
        miss = [p for p in paths if p not in m34]
        rs = row.get('readingStanding')
        rows.append({'row': mp + '/' + rid, 'owners': paths, 'ownersIn34Delta': hit, 'unresolved34': miss,
                     'readingStanding': rs})
        if hit:
            touched.append(mp + '/' + rid)
        if miss:
            unres.append((mp + '/' + rid, miss))
        if isinstance(rs, str) and not re.search(r'33|34', rs):
            stale.append((mp + '/' + rid, rs))
R['rows'] = rows
R['rowsWithOwnerIn34Delta'] = touched
R['rowsWithUnresolvedOwner34'] = unres
R['readingStandingWithoutVersion'] = stale
print('\nrows whose owners hit the 34 delta (%d):' % len(touched))
for t in touched:
    print('   ', t, [p.split('/')[-1] for p in next(r for r in rows if r['row'] == t)['ownersIn34Delta']])
print('\nrows with an owner path NOT in manifest34 (%d):' % len(unres))
for u in unres[:20]:
    print('   ', u)
print('\nreadingStanding values (distinct):')
dist = {}
for r in rows:
    dist.setdefault(str(r['readingStanding']), []).append(r['row'])
for k, v in sorted(dist.items(), key=lambda x: -len(x[1])):
    print('  %3d  %s' % (len(v), k[:150]))
print('\nreadingStanding strings with NO version token (%d):' % len(stale))
for s in stale:
    print('   ', s[0], '|', s[1][:140])
# rows that mention atoms anywhere (cross-owner consequence candidates)
atomish = []
for mp in MAPS:
    for rid, row in V[mp].items():
        b = json.dumps(row)
        if re.search(r'atom|attestation|incoming|outgoing|search', b, re.I):
            atomish.append(mp + '/' + rid)
R['rowsMentioningAtomOrSearch'] = atomish
print('\nrows mentioning atom/attestation/incoming/outgoing/search (%d): %s' % (len(atomish), atomish))
R['tcb'] = V['sharedAssumptionTCBSCOPE01']
R['crossUnit'] = V['crossUnitStanding']
json.dump(R, open(os.path.join(OUT, 'q02-baseline.json'), 'w'), indent=1, default=str)
print('wrote q02-baseline.json')
