from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections'); L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
mp=L/'candidate-subject.v35.json'; raw=mp.read_bytes(); assert hashlib.sha256(raw).hexdigest()=='eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85'
m=json.loads(raw); src=B/'candidate-subject.v35'; dest=B/'dependency-scope-successor.v1/source'; assert not dest.exists(); dest.mkdir(parents=True)
rows=[]
for f in m['files']:
 p=src/f['path']; raw=p.read_bytes(); assert hashlib.sha256(raw).hexdigest()==f['sha256'],f['path']
 q=dest/f['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);assert hashlib.sha256(q.read_bytes()).hexdigest()==f['sha256'];rows.append({'path':f['path'],'sha256':f['sha256'],'bytes':len(raw)})
r={'standing':'Exact mutable authoring copy of frozen35 only. No source36 freeze, acceptance or application.','parentSubjectSha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'source':str(src),'destination':str(dest),'filesVerified':len(rows),'bytesVerified':sum(r['bytes'] for r in rows)}
(B/'root-source36-preparation.v1/copy-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
