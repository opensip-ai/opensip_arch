from pathlib import Path
import argparse,json,hashlib,tarfile
p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--sha256',required=True);p.add_argument('--archive',type=Path,required=True);p.add_argument('--archive-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();raw=a.manifest.read_bytes();assert sha(raw)==a.sha256;m=json.loads(raw);root=Path(m['snapshotRoot']);rows={r['path']:r for r in m['files']};assert len(rows)==len(m['files'])
for rel,r in rows.items():
 q=root/rel;assert q.is_file() and not q.is_symlink();data=q.read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'],rel
assert {str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}==set(rows)
assert sha(a.archive.read_bytes())==a.archive_sha256
seen=set()
with tarfile.open(a.archive,'r:gz') as tf:
 for member in tf:
  if member.isdir():continue
  assert member.isfile() and member.name not in seen,member.name
  rel=member.name.removeprefix('./');assert rel in rows,rel;data=tf.extractfile(member).read();r=rows[rel];assert len(data)==r['bytes'] and sha(data)==r['sha256'],rel;seen.add(rel)
assert seen==set(rows)
result={'standing':'Exact snapshot and archive custody only. No acceptance or qualification.','manifestSha256':a.sha256,'archiveSha256':a.archive_sha256,'files':len(rows),'totalBytes':sum(r['bytes'] for r in rows.values()),'snapshotAndArchiveVerified':True}
(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
