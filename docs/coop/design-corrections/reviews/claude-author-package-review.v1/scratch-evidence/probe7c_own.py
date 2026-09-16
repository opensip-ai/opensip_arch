import json,base64
from pathlib import Path
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
rows=[
 ['lib','normalized-examples6/rust.store.json','6c50818b7f6d971ae875c229a987b6f667c893b1f87a3573eaf59d1415d8136d'],
 ['bin','rust-selection-examples1/rust-bin.store.json','d2f812383b8e43fe96b8892b8df9c020f8c5259caa7507fd380e39088b4eb81a'],
 ['lib-only','rust-selection-examples1/rust-lib-only.store.json','ea014cfbe740c5a375bbe6050b6ebd7a26027b598460a422f03865bfd00545e1']]
pay={}
for lab,store,hexd in rows:
    d=json.loads((PKG/store).read_text())
    b={}
    for k,v in d['blobs'].items(): b[k]=base64.b64decode(v)
    raw=b[hexd]
    i=raw.index(123)
    pay[lab]=json.loads(raw[i:])
for lab,store,hexd in rows:
    v=pay[lab]
    print('===',lab,'keys',sorted(v))
    print('   enumeration:',v.get('enumeration'))
    for o in v.get('ownership',[]):
        if 'shared.rs' in o.get('path',''): print('   SHARED row:',json.dumps(o,sort_keys=True))
    for u in v.get('units',[]):
        print('   unit:',json.dumps(u,sort_keys=True)[:250])
print()
keys=sorted(set(k for v in pay.values() for k in v))
for k in keys:
    vals={}
    for lab in pay: vals[lab]=json.dumps(pay[lab].get(k),sort_keys=True)
    if len(set(vals.values()))>1:
        print('DIFFERS',k)
        for lab in pay: print('   ',lab,'=',vals[lab][:550])
    else: print('same   ',k)
