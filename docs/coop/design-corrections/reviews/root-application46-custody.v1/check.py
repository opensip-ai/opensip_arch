from pathlib import Path
import json,hashlib,tarfile,shutil
B=Path('/tmp/opensip-design-corrections');S=B/'application-stage.v46';L=Path('/Users/sb/code/opensip-ai/opensip_arch');R=Path(__file__).parent;dc='docs/coop/design-corrections/reviews/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mp=S/'application-subject.v46.json';digest=sha(mp);assert digest=='dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7';assert sha(L/dc/mp.name)==digest;m=json.loads(mp.read_text());members={mp.name:digest}
for k,base in [('files',S/'files'),('beforeImages',S/'before'),('support',S)]:
 for row in m[k]:
  p=base/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'];members[str(p.relative_to(S))]=row['sha256']
for row in m['files']:
 p=L/row['path'];assert (sha(p) if p.is_file() else None)==row['beforeSha256']
archive=L/dc/'application-source.v46.tar.gz'
with tarfile.open(archive,'r:gz') as t:
 actual={x.name:hashlib.sha256(t.extractfile(x).read()).hexdigest() for x in t.getmembers() if x.isfile()}
assert actual==members
report={'standing':'Root complete46manifest/archive/live-beforeimage byte audit; inventory scoped hashes are checked by prior root audit/newdelta and final applied verifier separately. No independent review outcome granted.','manifestSha256':digest,'archiveSha256':sha(archive),'archiveMembersVerified':len(members),'applicationFiles':len(m['files']),'beforeImages':len(m['beforeImages']),'supportFiles':len(m['support']),'liveBeforeImagesMatch':True,'passed':True}
(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(R,L/dc/R.name);print(json.dumps(report))
