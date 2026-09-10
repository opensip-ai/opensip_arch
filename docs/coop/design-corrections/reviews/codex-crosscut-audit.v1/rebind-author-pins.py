"""Rebind source pins in the isolated author copy, retaining exact deltas."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--copy',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();changes=[]
for rel in ['docs/coop/design-corrections/security/source-pins.v1.json','docs/coop/design-corrections/native/source-pins.v2.json']:
 f=a.copy/rel;old=f.read_bytes();d=json.loads(old)
 for row in d['pins']:
  target=a.copy/row['path'];actual=hashlib.sha256(target.read_bytes()).hexdigest()
  if actual!=row['sha256']:
   changes.append({'ledger':rel,'path':row['path'],'before':row['sha256'],'after':actual});row['sha256']=actual
 f.chmod(f.stat().st_mode|0o200);f.write_text(json.dumps(d,indent=2)+'\n')
a.out.write_text(json.dumps({'standing':'AUTHOR-ONLY pin rebinding; not independent review or source activation','changes':changes},indent=2)+'\n');print('Rebound',len(changes),'pins in isolated copy.')
