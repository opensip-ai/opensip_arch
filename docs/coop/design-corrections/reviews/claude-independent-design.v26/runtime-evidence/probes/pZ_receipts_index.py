"""Index every receipt this review produced, with its own digest."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v26'
rows = []
for root in ('receipts', 'probes'):
    d = os.path.join(BASE, root)
    for dp, dn, fn in os.walk(d):
        for f in sorted(fn):
            p = os.path.join(dp, f)
            b = open(p, 'rb').read()
            rows.append({'path': os.path.relpath(p, BASE), 'bytes': len(b),
                         'sha256': hashlib.sha256(b).hexdigest()})
rows.sort(key=lambda r: r['path'])
json.dump({'standing': 'independent review artefacts produced by this fresh origin only',
           'count': len(rows), 'files': rows},
          open(os.path.join(BASE, 'receipts', 'INDEX.json'), 'w'), indent=1)
for r in rows:
    print('%-58s %8d %s' % (r['path'], r['bytes'], r['sha256'][:16]))
print('total', len(rows))
