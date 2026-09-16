"""Q04 — per-row audit of the corrected baseline for the source34 carry-forward:
  * current34 owner arrays derived from the two manifests (not prose)
  * stale legacy readingStanding strings: a string that claims 'unchanged' while the row's own
    32->33 changed-owner array is non-empty, or claims 'changed/read' while that array is empty
  * a compact subject summary per row, so cross-owner consequences of the atom law are chosen by
    reading each row, not by keyword luck."""
import json, os, re

B2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
V = json.load(open(os.path.join(B2, 'review.json')))
q00 = json.load(open(os.path.join(OUT, 'q00-custody.json')))
m34 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
m33 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v33.json')))['files']}
DELTA34 = {c['path'] for c in q00['delta']['changed']}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
CLAIMS_UNCHANGED = re.compile(r'unchanged', re.I)
CLAIMS_CHANGED = re.compile(r'changed (?:cited )?owner|re-read', re.I)
R = {'rows': {}, 'staleReadingStanding': []}
for mp in MAPS:
    for rid, row in V[mp].items():
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        ch33 = row.get('ownerFilesChangedIn32to33')
        if ch33 is None:
            ch33 = row.get('ownerSelectorsChangedIn32to33')
        rs = row.get('readingStanding')
        stale = None
        if isinstance(rs, str):
            if CLAIMS_UNCHANGED.search(rs) and ch33:
                stale = 'claims unchanged owners but its own 32->33 changed array is non-empty: %s' % ch33
            elif CLAIMS_CHANGED.search(rs) and ch33 == []:
                stale = 'claims a changed owner but its own 32->33 changed array is empty'
        if isinstance(rs, str) and re.search(r'source32 review', rs) and ch33:
            stale = stale or 'names an inherited source32 reading for a row whose owner changed in 33'
        summary = {k: str(row.get(k))[:150] for k in ('area', 'title', 'severity', 'disposition',
                                                     'dispositionOn33', 'evidence') if row.get(k) is not None}
        R['rows'][mp + '/' + rid] = {
            'owners': paths,
            'ownersAllIn34': all(p in m34 for p in paths),
            'ownerFilesChangedIn33to34': sorted(p for p in paths if p in DELTA34),
            'ownerFilesUnchangedIn33to34': sorted(p for p in paths if p in m34 and p not in DELTA34),
            'ownerBytesEqual33and34': all(m33.get(p) == m34.get(p) for p in paths),
            'changed32to33': ch33, 'readingStanding': rs, 'stale': stale, 'summary': summary,
            'currentStatusOn33': str(row.get('currentStatusOn33') or row.get('currentBasisOn33'))[:220]}
        if stale:
            R['staleReadingStanding'].append({'row': mp + '/' + rid, 'readingStanding': rs, 'why': stale})
print('stale legacy readingStanding strings: %d' % len(R['staleReadingStanding']))
for s in R['staleReadingStanding']:
    print('   %-46s %s' % (s['row'], s['why'][:120]))
print('\nrows with any owner changed 33->34:',
      [k for k, v in R['rows'].items() if v['ownerFilesChangedIn33to34']])
print('rows whose owners all resolve in 34 with equal bytes 33/34:',
      sum(1 for v in R['rows'].values() if v['ownersAllIn34'] and v['ownerBytesEqual33and34']), 'of', len(R['rows']))
print('\n=== subject summaries (for cross-owner consequence selection) ===')
for k, v in R['rows'].items():
    s = v['summary']
    label = s.get('title') or s.get('area') or ''
    print('%-46s | %-70s | %s' % (k, label[:70], v['currentStatusOn33'][:110].replace('\n', ' ')))
json.dump(R, open(os.path.join(OUT, 'q04-rows.json'), 'w'), indent=1, default=str)
print('wrote q04-rows.json')
