"""Build fresh normative-only kit; no consumer launch, expected outputs or acceptance."""
from pathlib import Path
import argparse,json,hashlib,posixpath
p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--origin-standing',choices=['fresh','continuation'],required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--previous-kit-manifest',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=a.manifest.read_bytes();assert sha(raw)==a.manifest_sha256
members={r['path']:r for r in json.loads(raw)['files']}
old=json.loads(a.previous_kit_manifest.read_bytes());paths={r['path'] for r in old['files']}
paths.update(json.loads(Path(__file__).with_name('normative-additions.json').read_bytes()))
assert not a.out.exists();staged={};rows=[]
for rel in sorted(paths):
 assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
 assert '/reviews/' not in rel and Path(rel).suffix in ('.md','.json','.sql'),rel
 assert rel in members,rel
 raw=(a.snapshot/rel).read_bytes();r={'path':rel,'sha256':sha(raw),'bytes':len(raw)};assert r==members[rel],rel
 staged[rel]=raw;rows.append(r)
# Reject genuinely missing schema dependencies, resolving published non-URL ids first.
ids={}
def visit(v,fn):
 if isinstance(v,dict):
  fn(v)
  for x in v.values():visit(x,fn)
 elif isinstance(v,list):
  for x in v:visit(x,fn)
parsed={r:json.loads(b) for r,b in staged.items() if r.endswith('.json')}
for rel,obj in parsed.items():
 def collect(v):
  if '$id' in v:ids[v['$id']]=rel
 visit(obj,collect)
for rel,obj in parsed.items():
 def check(v):
  ref=v.get('$ref','');base=ref.split('#')[0]
  if not base or base in ids or base.startswith(('https:','http:','urn:')):return
  target=posixpath.normpath(posixpath.join(posixpath.dirname(rel),base));assert target in staged,(rel,ref,target)
 visit(obj,check)
a.out.mkdir(parents=True)
for rel,raw in staged.items():
 q=a.out/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
standing=('Exact normative subset for NEW actual Claude blind consumer' if a.origin_standing=='fresh' else 'Exact normative successor subset for continuation of the SAME originally fresh actual Claude blind origin')+'; no author models, executed controls, expected outputs, prior answers or verdicts in this subject. Planned recovery requirements and normative DDL are prescriptions, not executed evidence.'
d={'standing':standing,'parentSubjectSha256':a.manifest_sha256,'files':rows}
q=a.out/'consumer-input-manifest.json';q.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'files':len(rows),'kitManifestSha256':sha(q.read_bytes())}))
