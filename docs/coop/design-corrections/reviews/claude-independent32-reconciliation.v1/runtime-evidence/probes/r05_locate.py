"""R05 — locate every remaining occurrence by JSON PATH, to separate intentional quotation inside a
recordCorrection from a genuine stale clause."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
R = json.load(open(os.path.join(BASE, 'review.json')))
TOKENS = ('evaluator-fault-contract.v1.md', 'precedes structural custody')
hits = []


def walk(o, path='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
    elif isinstance(o, str):
        for t in TOKENS:
            if t in o:
                hits.append({'token': t, 'path': path, 'text': o[:260]})


walk(R)
for h in hits:
    intentional = ('recordCorrection' in h['path'] or 'correctionsToMyOwnV32Record' in h['path']
                   or 'rootFinding' in h['path'] or 'evidence' in h['path'])
    h['intentionalQuotation'] = intentional
    print('%-8s %-62s %s' % ('QUOTE' if intentional else 'STALE', h['path'][-62:], h['text'][:110]))
stale = [h for h in hits if not h['intentionalQuotation']]
print('\ntotal occurrences: %d | intentional quotations: %d | genuine stale: %d'
      % (len(hits), len(hits) - len(stale), len(stale)))
for s in stale:
    print('   STALE AT', s['path'])
    print('      ', s['text'][:240])
json.dump({'hits': hits, 'stale': stale},
          open(os.path.join(BASE, 'receipts', 'r05-locate.json'), 'w'), indent=1)
print('\nwrote r05-locate.json')
