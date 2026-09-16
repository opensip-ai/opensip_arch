"""Bind final integrated normative inputs, before planning layer and reference checks."""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args()
T=a.source.resolve();O=a.evidence.resolve();assert not O.exists();O.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def write(p,d):
 raw=p.read_bytes();new=(json.dumps(d,indent=2)+'\n').encode()
 if raw==new:return
 q=O/'before'/p.relative_to(T);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);p.write_bytes(new)
add=json.loads(Path(__file__).with_name('normative-additions.json').read_bytes())
assert all((T/r).is_file() for r in add),'Complete normative integration before binding'
# Four ordinary ledgers first; evaluator profile includes their final bytes.
ledgers=['foundation/source-pins.v1.json','native/source-pins.v2.json','security/source-pins.v1.json','workflows/source-pins.v1.json','foundation/evaluator3-source-pins.v1.json']
D=T/'docs/coop/design-corrections';result=[]
for n in ledgers:
 p=D/n;d=read(p);key='files' if 'files' in d else 'pins';rows={r['path']:dict(r) for r in d[key]};assert len(rows)==len(d[key])
 for rel in add+['docs/coop/design-corrections/security/check-carrier-v3.py','docs/coop/design-corrections/security/check-integrated-carrier.v1.py']:
  assert not rel.startswith('docs/v2/architecture/implementation-')
  rows.setdefault(rel,{'path':rel})
 for rel,row in rows.items():
  raw=(T/rel).read_bytes();row['sha256']=sha(raw)
  if 'bytes' in row:row['bytes']=len(raw)
 d[key]=[rows[k] for k in sorted(rows)];write(p,d);result.append({'path':str(p.relative_to(T)),'sha256':sha(p.read_bytes()),'files':len(rows)})
for n in ledgers:
 d=read(D/n)
 for row in d.get('files',d.get('pins',[])):assert sha((T/row['path']).read_bytes())==row['sha256'],(n,row['path'])
# Companion inputs have explicit source keys; no new responsibility population is invented.
p=T/'docs/v2/architecture/implementation-coverage.v1.json';d=read(p);known={r['path'] for r in d['sources'].values()}
for rel in add:
 if rel in known:continue
 key='incorporated:'+Path(rel).name;assert key not in d['sources'];raw=(T/rel).read_bytes();d['sources'][key]={'path':rel,'sha256':sha(raw),'bytes':len(raw)}
write(p,d)
(O/'binding.json').write_text(json.dumps({'standing':'Final integrated source pin preparation; no acceptance or readiness','ledgers':result,'addedNormativeInputs':add},indent=2)+'\n')
print('Bound5ledgers and incorporated planning sources; next rebind planning input layer')
