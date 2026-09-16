"""S03 — locate the one remaining 'read fresh in that session' occurrence by JSON path, to decide
whether it is a genuine contradictory claim or a documented quotation of the corrected wording."""
import json, os

V2 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2'
R = json.load(open(os.path.join(V2, 'review.json')))
hits = []


def walk(o, path='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
    elif isinstance(o, str) and 'read fresh in that session' in o:
        hits.append({'path': path, 'text': o})


walk(R)
for h in hits:
    documented = any(t in h['path'] for t in ('recordCorrection', 'correctionsToMyOwn',
                                              'rootFinding', 'evidence'))
    h['documentedQuotation'] = documented
    print('%-10s %s' % ('QUOTE' if documented else 'STALE', h['path']))
    print('    ', h['text'][:260])
stale = [h for h in hits if not h['documentedQuotation']]
print('\noccurrences: %d | documented quotations: %d | genuine stale: %d'
      % (len(hits), len(hits) - len(stale), len(stale)))
json.dump({'hits': hits, 'stale': stale},
          open(os.path.join(V2, 'receipts', 's03-locate.json'), 'w'), indent=1)
print('wrote s03-locate.json')
