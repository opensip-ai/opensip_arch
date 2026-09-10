"""Freeze a new correction subject without overwriting any earlier evidence."""
from pathlib import Path
import argparse, hashlib, json, shutil, tarfile
p=argparse.ArgumentParser()
for name in ('previous','version','previous-sha','author-session'):p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path.cwd();dc=root/'docs/coop/design-corrections';reviews=dc/'reviews';tmp=Path('/tmp/opensip-design-corrections')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def verify_current_pins(base):
    # Recording edits can themselves be reference inputs. Validate after ALL edits, and again
    # against copied bytes, rather than relying on a successful command from an earlier tree.
    failures=[]
    for unit,name,key in [('foundation','source-pins.v1.json','files'),('security','source-pins.v1.json','pins'),('native','source-pins.v2.json','pins'),('workflows','source-pins.v1.json','files')]:
        ledger=base/'docs/coop/design-corrections'/unit/name
        for row in json.loads(ledger.read_text())[key]:
            source=base/row['path']
            if not source.is_file() or sha(source)!=row['sha256'] or ('bytes' in row and source.stat().st_size!=row['bytes']):failures.append({'ledger':str(ledger.relative_to(base)),'path':row['path']})
    assert not failures, ('Cannot freeze stale reference input pins',failures)
verify_current_pins(root)
summary=json.loads((dc/'validation-summary.v1.json').read_text())
assert summary['claudeFinalReview']=='PENDING-FROZEN-'+a.version.upper(), 'Pending review version must name this candidate'
assert summary['claudePriorReview']=='reviews/post-reset-review.'+a.previous+'/review.json', 'Prior review must name the completed predecessor'
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
verify_current_pins(snapshot)
data={'standing':'FROZEN CORRECTED CANDIDATE FOR FRESH INDEPENDENT REVIEW; NO ACCEPTANCE','authors':['actual Claude coauthor session '+a.author_session,'Codex; earlier mixed authors retained with original custody'],'predecessorManifestSha256':a.previous_sha,'snapshotRoot':str(snapshot),'files':rows,'fileCount':len(rows),'totalBytes':sum(r['bytes'] for r in rows),'reviewPending':True,'applicationPending':True}
manifest.write_text(json.dumps(data,indent=2)+'\n')
with tarfile.open(archive,'w:gz') as tar:
    for row in rows:tar.add(snapshot/row['path'],arcname=row['path'],recursive=False)
print(json.dumps({'manifest':str(manifest),'sha256':sha(manifest),'files':len(rows),'bytes':data['totalBytes']}))
