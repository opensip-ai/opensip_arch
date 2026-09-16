"""PROBE I3 (v27) — extract the F-01..F-14 findings from the author-package review prose.

The instruction named claude-author-package-review.v1/review.json; that file does not exist.
The directory holds review.md (65124 bytes) plus session metadata. The findings are spelled
"F-01".."F-14" there. This probe records that substitution honestly and dumps each row's
full statement text so every remedy can be assessed against snapshot27 bytes.
"""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-author-package-review.v1'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

raw = open(os.path.join(BASE, 'review.md'), 'rb').read()
md = raw.decode('utf-8')
print('review.md sha256:', hashlib.sha256(raw).hexdigest())
print('review.md bytes :', len(raw))
print('review.json exists:', os.path.isfile(os.path.join(BASE, 'review.json')))

ids = sorted(set(re.findall(r'\bF-\d\d\b', md)))
print('F ids present (%d):' % len(ids), ids)

# every mention, with enough context to read the statement
rows = {}
for m in re.finditer(r'\bF-\d\d\b', md):
    rows.setdefault(m.group(0), []).append(m.start())

recs = []
for fid in ids:
    positions = rows[fid]
    # the defining mention: the one whose line looks like a table row or a bolded statement
    chunks = []
    for p in positions:
        ls = md.rfind('\n', 0, p) + 1
        le = md.find('\n', p)
        if le < 0:
            le = len(md)
        chunks.append(md[ls:le])
    recs.append({'id': fid, 'mentions': len(positions), 'lines': chunks})
    print('\n===== %s  (%d mentions) =====' % (fid, len(positions)))
    for c in chunks:
        print('   ', c.strip()[:1000])

json.dump({'reviewMdSha256': hashlib.sha256(raw).hexdigest(),
           'reviewJsonExists': os.path.isfile(os.path.join(BASE, 'review.json')),
           'ids': ids, 'rows': recs},
          open(os.path.join(OUT, 'pI3-findingsF.json'), 'w'), indent=1)
