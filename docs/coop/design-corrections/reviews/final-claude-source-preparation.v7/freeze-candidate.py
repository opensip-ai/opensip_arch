"""Freeze integrated design/reference bytes only; no acceptance or activation."""
from pathlib import Path
import argparse,json,hashlib,tarfile
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--parent-sha256',required=True);p.add_argument('--version',type=int,required=True);p.add_argument('--snapshots',type=Path,required=True);p.add_argument('--records',type=Path,required=True);a=p.parse_args()
sha=lambda raw:hashlib.sha256(raw).hexdigest()
raw=a.parent.read_bytes();assert sha(raw)==a.parent_sha256;parent=json.loads(raw)
T=a.source.resolve();snapshot=a.snapshots/f'candidate-subject.v{a.version}';mf=a.records/f'candidate-subject.v{a.version}.json';archive=a.records/f'candidate-source.v{a.version}.tar.gz';receipt=a.records/f'candidate-freeze.v{a.version}.json'
assert not any(p.exists() for p in [snapshot,mf,archive,receipt])
paths={r['path'] for r in parent['files']}
# The isolated source is the explicit assembly, not the mutable live repo.
for f in T.rglob('*'):
 if f.is_file() and '__pycache__' not in f.parts and '.git' not in f.parts:paths.add(f.relative_to(T).as_posix())
assert all((T/r).is_file() for r in paths),'Parent dependency lost'
for n in ['foundation/source-pins.v1.json','native/source-pins.v2.json','security/source-pins.v1.json','workflows/source-pins.v1.json','foundation/evaluator3-source-pins.v1.json']:
 d=json.loads((T/'docs/coop/design-corrections'/n).read_bytes())
 for r in d.get('files',d.get('pins',[])):assert r['path'] in paths and sha((T/r['path']).read_bytes())==r['sha256'],(n,r['path'])
rows=[];snapshot.mkdir(parents=True)
for rel in sorted(paths):
 assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
 raw=(T/rel).read_bytes();out=snapshot/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
 rows.append({'path':rel,'sha256':sha(raw),'bytes':len(raw)})
d={'standing':'Frozen combined OpenSIP design/reference/planning successor. No acceptance, readiness, product implementation or activation is inferred.','authors':['Codex','actual Claude','actual Grok (inherited candidate25)'],'requiredReviewer':'Fresh independent actual Claude origin; separate new blind consumer under original charter','parentManifestSha256':a.parent_sha256,'snapshotRoot':str(snapshot),'files':rows,'fileCount':len(rows),'totalBytes':sum(r['bytes'] for r in rows),'reviewPending':True,'newBlindConsumerPending':True,'applicationPending':True,'implementationAuthorized':False}
mf.write_text(json.dumps(d,indent=2)+'\n')
with tarfile.open(archive,'w:gz') as t:
 for r in rows:t.add(snapshot/r['path'],arcname=r['path'],recursive=False)
for r in rows:assert sha((snapshot/r['path']).read_bytes())==r['sha256']
x={'manifestPath':str(mf),'manifestSha256':sha(mf.read_bytes()),'archivePath':str(archive),'archiveSha256':sha(archive.read_bytes()),'fileCount':len(rows),'totalBytes':d['totalBytes']};receipt.write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
