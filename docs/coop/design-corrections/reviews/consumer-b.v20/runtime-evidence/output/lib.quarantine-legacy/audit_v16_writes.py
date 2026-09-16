"""Census of every file of a PRIOR generation that this v17 session wrote.

The boundary is PERSISTED on first measurement, because a boundary recomputed from a file this
session keeps rewriting would silently shrink the census to zero on the next run -- which is
exactly the kind of self-referential measurement this origin is supposed to refuse.

The known set is also persisted. Later runs re-measure and assert that nothing OUTSIDE the
recorded set is newer than the boundary, so a NEW write fails the run while the two already
disclosed writes stay disclosed.
"""
import json
import os
import time

BASE = '/tmp/opensip-design-corrections'
OUT = BASE + '/consumer-b.v18/output'
REC = OUT + '/notes/prior-generation-writes.json'

# the boundary: the v16 generation's LAST OWN artifact is not usable (this session overwrote
# two v16 files), so the boundary recorded at first measurement is kept verbatim.
BOUNDARY_UTC = '2026-09-12T11:40:00Z'
KNOWN = [
    'consumer-b.v16/output/helper-corrections.json',
    'consumer-b.v16/output/notes/siblings-untouched.json',
]

boundary = time.mktime(time.strptime(BOUNDARY_UTC, '%Y-%m-%dT%H:%M:%SZ')) \
    - time.timezone if time.daylight == 0 else \
    time.mktime(time.strptime(BOUNDARY_UTC, '%Y-%m-%dT%H:%M:%SZ')) - time.altzone

rows, unexpected = {}, []
for gen in ('consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16'):
    root = os.path.join(BASE, gen)
    hits = []
    for d, _dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            try:
                m = os.stat(p).st_mtime
            except OSError:
                continue
            if m >= boundary:
                rel = p.replace(BASE + '/', '')
                hits.append({'path': rel,
                             'mtimeUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                       time.gmtime(m))})
                if rel not in KNOWN:
                    unexpected.append(rel)
    rows[gen] = sorted(hits, key=lambda r: r['path'])

doc = {
    'standing': __doc__,
    'boundaryUtc': BOUNDARY_UTC,
    'knownDisclosedWrites': KNOWN,
    'measured': rows,
    'unexpectedWrites': sorted(set(unexpected)),
    'totalMeasured': sum(len(v) for v in rows.values()),
    'disclosure': (
        'These writes were made before this origin\'s own prior-generation control caught the '
        'defect (helper-corrections.json row V17-D8). Their pre-existing bytes were not '
        'retained and are not claimed to be restorable. No prior Run export, review file, '
        'requirement status, checkpoint or vector was written.'),
}
os.makedirs(OUT + '/notes', exist_ok=True)
with open(REC, 'w') as f:
    json.dump(doc, f, indent=1)
for gen, hits in rows.items():
    print('%-16s measured=%d %s' % (gen, len(hits), [h['path'] for h in hits]))
print('known disclosed: %d | unexpected: %s' % (len(KNOWN), doc['unexpectedWrites']))
assert not doc['unexpectedWrites'], doc['unexpectedWrites']
