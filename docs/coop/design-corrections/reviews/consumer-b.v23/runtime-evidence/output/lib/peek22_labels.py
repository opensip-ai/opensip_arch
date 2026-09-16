"""Read-only: the label keys and typed-object prefixes of one exported store. Writes nothing."""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
label = sys.argv[1] if len(sys.argv) > 1 else 'typescript'
st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
print('export top-level keys:', sorted(doc.keys()))
pref = collections.Counter(t.split(':', 1)[0] for t in st.objects)
print('object prefixes:', dict(pref))
labs = collections.Counter(k.split(':', 1)[0] for k in st.labels)
print('label prefixes :', dict(labs))
for k in sorted(st.labels):
    if 'universe' in k or 'context' in k:
        b = st.get_blob(st.labels[k])
        head = b[:300].decode('utf-8', 'replace') if b else None
        print('  %s -> %s' % (k[:80], head))
wit = next(iter(k for k in st.labels if k.startswith('witness')), None)
print('a witness label:', wit)
