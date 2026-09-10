"""Read-only final input-pin seal check; never changes a report, pin, source or grade."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.root.resolve();assert not a.out.exists();rows=[];bad=[]
for unit,name,key in [('foundation','source-pins.v1.json','files'),('security','source-pins.v1.json','pins'),('native','source-pins.v2.json','pins'),('workflows','source-pins.v1.json','files')]:
 rel='docs/coop/design-corrections/'+unit+'/'+name;mp=r/rel;d=json.loads(mp.read_text())
 for x in d[key]:
  path=r/x['path'];b=path.read_bytes() if path.is_file() else None;observed=hashlib.sha256(b).hexdigest() if b is not None else None;match=observed==x['sha256'] and ('bytes' not in x or b is not None and len(b)==x['bytes']);row={'ledger':rel,'path':x['path'],'pinnedSha256':x['sha256'],'observedSha256':observed,'matches':match};rows.append(row)
  if not match:bad.append(row)
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps({'standing':'Codex read-only final pin check against exact current bytes; no product qualification or acceptance.','root':str(r),'pinsChecked':len(rows),'mismatches':bad,'passed':not bad},indent=2)+'\n');print(json.dumps({'pinsChecked':len(rows),'mismatches':bad,'passed':not bad}));raise SystemExit(bool(bad))
