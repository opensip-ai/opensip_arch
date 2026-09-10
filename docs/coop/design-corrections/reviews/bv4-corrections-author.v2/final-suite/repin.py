"""TEMPORARY measured repin inside a DISPOSABLE copy, so the reference check scripts can execute at
all. This is a development experiment: it is NOT accepted pin evidence, and the released source
keeps its original (now intentionally stale) pin manifests."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(sys.argv[1])
MANIFESTS=[('docs/coop/design-corrections/foundation/source-pins.v1.json','files'),
           ('docs/coop/design-corrections/native/source-pins.v2.json','pins')]
changed=[]
for manifest,key in MANIFESTS:
    p=ROOT/manifest;raw=p.read_text();d=json.loads(raw)
    for item in d[key]:
        f=ROOT/item['path']
        if not f.is_file():continue
        actual=hashlib.sha256(f.read_bytes()).hexdigest()
        if actual!=item['sha256']:
            changed.append({'manifest':manifest,'path':item['path'],'was':item['sha256'],'now':actual})
            item['sha256']=actual
    p.write_text(json.dumps(d,indent=2)+('\n' if raw.endswith('\n') else ''))
print(json.dumps({'repinned':len(changed),'entries':changed},indent=1))
