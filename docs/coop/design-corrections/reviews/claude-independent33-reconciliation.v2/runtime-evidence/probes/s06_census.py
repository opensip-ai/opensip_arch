"""S06 — census before building: every evidenceReceipts entry checked for a stale CURRENT status, and
the owner-changed vs owner-unchanged split across the 107 rows (for explicit inheritance standing)."""
import json, os, re

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
V = json.load(open(os.path.join(V1, 'review.json')))
R = {}

print('=== evidenceReceipts entries, scanned for stale CURRENT status ===')
STALE = re.compile(r'INCOMPLETE|PENDING|not yet|no source33-bound|package9|unavailable', re.I)
R['evidenceReceiptFindings'] = {}
for k, v in V['evidenceReceipts'].items():
    s = json.dumps(v, default=str)
    hit = STALE.search(s)
    R['evidenceReceiptFindings'][k] = {'staleHit': hit.group(0) if hit else None, 'value': s[:300]}
    print('%-34s %-14s %s' % (k, hit.group(0) if hit else '-', s[:150]))

print('\n=== other places asserting an INCOMPLETE package status ===')
blob = json.dumps(V, indent=1, default=str).splitlines()
ctx = [l.strip()[:200] for l in blob if 'INCOMPLETE' in l]
R['incompleteMentions'] = ctx
for c in ctx:
    print('  ', c)

print('\n=== owner-changed vs owner-unchanged census ===')
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
cen = {'ownersChanged': [], 'ownersUnchangedVerified': [], 'noOwnerArray': []}
for mp in MAPS:
    for rid, row in V[mp].items():
        key = mp + '/' + rid
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        if ch is None:
            cen['noOwnerArray'].append(key)
        elif ch:
            cen['ownersChanged'].append(key)
        else:
            cen['ownersUnchangedVerified'].append(key)
R['census'] = {k: len(v) for k, v in cen.items()}
R['censusDetail'] = cen
print(json.dumps(R['census'], indent=1))
print('rows with a changed owner:', cen['ownersChanged'])
print('rows with no owner array :', cen['noOwnerArray'])

# do the unchanged rows really have byte-verified owners?
ver = 0
for key in cen['ownersUnchangedVerified']:
    mp, rid = key.split('/')
    row = V[mp][rid]
    if row.get('ownerPathsResolveInFrozen33') is True or row.get('ownerSelectorsResolveInFrozen33') is True:
        ver += 1
R['unchangedRowsWithResolveFlagTrue'] = ver
print('unchanged rows carrying a resolve-in-frozen33 flag = True:', ver, 'of', len(cen['ownersUnchangedVerified']))
json.dump(R, open(os.path.join(OUT, 's06-census.json'), 'w'), indent=1, default=str)
print('\nwrote s06-census.json')
