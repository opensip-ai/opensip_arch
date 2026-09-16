from pathlib import Path
import hashlib,json,tarfile
B=Path('/tmp/opensip-design-corrections');S=B/'application-stage.v45.2';R=Path(__file__).parent;L=Path('/Users/sb/code/opensip-ai/opensip_arch');dc='docs/coop/design-corrections/reviews/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
mp=S/'application-subject.v45.json';digest=sha(mp);assert digest=='948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757';assert sha(L/dc/mp.name)==digest;m=load(mp)
members={mp.name:digest}
for k,base in [('files',S/'files'),('beforeImages',S/'before'),('support',S)]:
 for row in m[k]:
  p=base/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'];members[str(p.relative_to(S))]=row['sha256']
archive=L/dc/'application-source.v45.tar.gz'
with tarfile.open(archive,'r:gz') as t:
 actual={x.name:hashlib.sha256(t.extractfile(x).read()).hexdigest() for x in t.getmembers() if x.isfile()}
assert actual==members
inv=load(S/'files/docs/operations/document-inventory.v1.json');by={r['path']:r for r in inv['files']};assert len(by)==inv['fileCount']==135218
for rel in inv['workingTreeDelta']['contentPaths']:
 p=S/'files'/rel
 if not p.exists():p=L/rel
 assert sha(p)==by[rel]['sha256'],rel
report={'standing':'Root independent full manifest/archive/scoped-inventory byte audit while fresh Claude application review proceeds. Does not award a review outcome.','manifestSha256':digest,'archiveSha256':sha(archive),'archiveMembersVerified':len(members),'applicationFiles':len(m['files']),'beforeImages':len(m['beforeImages']),'supportFiles':len(m['support']),'scopedInventoryPathsVerified':len(inv['workingTreeDelta']['contentPaths']),'inventoryTotalRows':len(by),'passed':True}
(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
