import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL

OUT = '/tmp/opensip-design-corrections/consumer-b.v16/output'
st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
c = CL.Closure(st)
rid = [t for t in st.objects if t.startswith('run3:')][0]
c.close_run(rid, 'peek')
rel = c.relreg['relations']['clones']
print('selector', rel['selector'])
print('bodyIdentityJoin', json.dumps(rel['bodyIdentityJoin'], indent=1)[:1200])
for fid, f in sorted(c.facts_seen.items()):
    if f['relation'] != 'clones':
        continue
    pay = c.canonical_record(f['payloadDigest'], B.RELATION_DOC, rel['selector'], 'PK')
    print('==', fid[:24], f['anchors'][0]['path'])
    print(json.dumps(pay, indent=1)[:800])
    break
print('--- languageVersionBinding')
print(json.dumps(c.dd.get('languageVersionBinding'), indent=1)[:1500])
