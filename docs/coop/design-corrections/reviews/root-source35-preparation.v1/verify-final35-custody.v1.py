from pathlib import Path
import argparse,json,hashlib,tarfile
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--archive-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');mf=L/'candidate-subject.v35.json';archive=L/'candidate-source.v35.tar.gz';parent=L/'candidate-subject.v34.json';h=lambda b:hashlib.sha256(b).hexdigest()
assert not a.out.exists();a.out.mkdir(parents=True)
assert h(mf.read_bytes())==a.manifest_sha256 and h(archive.read_bytes())==a.archive_sha256
assert h(parent.read_bytes())=='bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
m=json.loads(mf.read_bytes());pm=json.loads(parent.read_bytes());assert m['parentManifestSha256']==h(parent.read_bytes())
rows={r['path']:r for r in m['files']};prior={r['path']:r for r in pm['files']};assert len(rows)==len(m['files'])==m['fileCount'];assert not set(prior)-set(rows)
S=Path(m['snapshotRoot']);actual={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()};assert actual==set(rows),(actual-set(rows),set(rows)-actual)
for rel,r in rows.items():
 p=S/rel;raw=p.read_bytes();assert not p.is_symlink();assert len(raw)==r['bytes'] and h(raw)==r['sha256'],rel
assert sum(r['bytes'] for r in rows.values())==m['totalBytes']
seen=[]
with tarfile.open(archive,'r:gz') as t:
 for member in t:
  assert member.isfile() and member.name in rows;seen.append(member.name);raw=t.extractfile(member).read();r=rows[member.name];assert member.size==r['bytes']==len(raw) and h(raw)==r['sha256'],member.name
assert len(seen)==len(set(seen))==len(rows) and set(seen)==set(rows)
changed=[{'path':rel,'beforeSha256':prior.get(rel,{}).get('sha256'),'afterSha256':r['sha256']} for rel,r in rows.items() if prior.get(rel,{}).get('sha256')!=r['sha256']]
report={'standing':'Root exact frozen source/archive/ancestry custody only; no acceptance or readiness.','manifestSha256':a.manifest_sha256,'archiveSha256':a.archive_sha256,'parentManifestSha256':h(parent.read_bytes()),'fileCount':len(rows),'totalBytes':m['totalBytes'],'everyManifestMemberVerified':True,'archiveEveryMemberVerified':True,'noExtraSnapshotFiles':True,'noParentOmission':True,'delta':changed,'rootAssent':False};(a.out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'verifiedFiles':len(rows),'bytes':m['totalBytes'],'deltaFiles':len(changed),'manifestSha256':a.manifest_sha256}))
