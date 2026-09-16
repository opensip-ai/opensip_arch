from pathlib import Path
import json,hashlib,tarfile,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O=B/'root-final45-custody.v1';assert not O.exists()
H=lambda b:hashlib.sha256(b).hexdigest()
receipt=json.loads((L/'candidate-freeze.v45.json').read_bytes())
mp=L/'candidate-subject.v45.json';raw=mp.read_bytes();assert H(raw)==receipt['manifestSha256'];m=json.loads(raw);S=Path(m['snapshotRoot'])
parent=L/'candidate-subject.v44.json';assert H(parent.read_bytes())==m['parentManifestSha256']=='e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b'
prior=json.loads(parent.read_bytes());previous={r['path']:r for r in prior['files']};members={r['path']:r for r in m['files']}
assert len(members)==m['fileCount']==len(m['files']) and set(previous)<=set(members)
assert sum(r['bytes'] for r in members.values())==m['totalBytes']
for subject,rows in [(S,members),(Path(prior['snapshotRoot']),previous)]:
 for rel,r in rows.items():
  q=subject/rel;assert not q.is_symlink() and q.is_file();b=q.read_bytes();assert H(b)==r['sha256'] and len(b)==r['bytes'],str(q)
assert {p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}==set(members)
archive=L/'candidate-source.v45.tar.gz';assert H(archive.read_bytes())==receipt['archiveSha256']
seen=set()
with tarfile.open(archive,'r:gz') as tar:
 for entry in tar:
  assert entry.isfile() and entry.name in members and entry.name not in seen
  r=members[entry.name];data=tar.extractfile(entry).read();assert H(data)==r['sha256'] and len(data)==entry.size==r['bytes'];seen.add(entry.name)
assert seen==set(members)
pin_count=0
for n in ['foundation/source-pins.v1.json','native/source-pins.v2.json','security/source-pins.v1.json','workflows/source-pins.v1.json','foundation/evaluator3-source-pins.v1.json']:
 d=json.loads((S/'docs/coop/design-corrections'/n).read_bytes())
 for r in d.get('files',d.get('pins',[])):
  assert members[r['path']]['sha256']==r['sha256'];pin_count+=1
report={'standing':'Exact frozen snapshot, archive members, unchanged parent44, inherited paths and all five pin ledgers verified. No design/application acceptance.','manifestSha256':H(raw),'archiveSha256':H(archive.read_bytes()),'fileCount':len(members),'totalBytes':m['totalBytes'],'changed':sum(members[p]['sha256']!=previous[p]['sha256'] for p in previous),'added':len(set(members)-set(previous)),'removed':0,'allMembersAndPinsVerified':True,'pinRowsVerified':pin_count}
O.mkdir();(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps(report))
