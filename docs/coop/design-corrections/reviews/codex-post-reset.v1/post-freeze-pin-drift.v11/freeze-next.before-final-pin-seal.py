"""Freeze a new correction subject without overwriting any earlier evidence."""
from pathlib import Path
import argparse, hashlib, json, shutil, tarfile
p=argparse.ArgumentParser()
for name in ('previous','version','previous-sha','author-session'):p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path.cwd();dc=root/'docs/coop/design-corrections';reviews=dc/'reviews';tmp=Path('/tmp/opensip-design-corrections')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldp=reviews/('candidate-subject.'+a.previous+'.json');assert sha(oldp)==a.previous_sha;old=json.loads(oldp.read_text())
for row in old['files']:
    source=Path(old['snapshotRoot'])/row['path'];assert sha(source)==row['sha256'] and source.stat().st_size==row['bytes'],row['path']
manifest=reviews/('candidate-subject.'+a.version+'.json');archive=reviews/('candidate-source.'+a.version+'.tar.gz');snapshot=tmp/('candidate-subject.'+a.version)
assert not manifest.exists() and not archive.exists() and not snapshot.exists()
paths={row['path'] for row in old['files']}
for base in (dc,root/'docs/v2/contracts/product-v1'):
    for path in base.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and not path.name.endswith('.tar.gz') and path!=manifest:paths.add(str(path.relative_to(root)))
snapshot.mkdir();rows=[]
for rel in sorted(paths):
    source=root/rel;assert source.is_file() and not source.is_symlink();raw=source.read_bytes();target=snapshot/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    rows.append({'path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
data={'standing':'FROZEN CORRECTED CANDIDATE FOR FRESH INDEPENDENT REVIEW; NO ACCEPTANCE','authors':['actual Claude coauthor session '+a.author_session,'Codex; earlier mixed authors retained with original custody'],'predecessorManifestSha256':a.previous_sha,'snapshotRoot':str(snapshot),'files':rows,'fileCount':len(rows),'totalBytes':sum(r['bytes'] for r in rows),'reviewPending':True,'applicationPending':True}
manifest.write_text(json.dumps(data,indent=2)+'\n')
with tarfile.open(archive,'w:gz') as tar:
    for row in rows:tar.add(snapshot/row['path'],arcname=row['path'],recursive=False)
print(json.dumps({'manifest':str(manifest),'sha256':sha(manifest),'files':len(rows),'bytes':data['totalBytes']}))
