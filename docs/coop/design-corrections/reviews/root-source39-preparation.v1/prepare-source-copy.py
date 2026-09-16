from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');MF=L/'candidate-subject.v38.json';h=lambda b:hashlib.sha256(b).hexdigest();assert h(MF.read_bytes())=='2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5';m=json.loads(MF.read_bytes());S=Path(m['snapshotRoot']);O=B/'consumer24-corrections-successor.v1/source';assert not O.exists();O.mkdir(parents=True)
for r in m['files']:
 p=S/r['path'];raw=p.read_bytes();assert not p.is_symlink() and len(raw)==r['bytes'] and h(raw)==r['sha256'];q=O/r['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};assert actual=={r['path'] for r in m['files']}
for r in m['files']:assert h((O/r['path']).read_bytes())==r['sha256']
record={'standing':'Exact source38 copy only for prospective consumer24 design corrections. No correction, successor freeze, review acceptance or product implementation yet.','parentManifestSha256':h(MF.read_bytes()),'source':str(O),'filesVerified':len(m['files']),'bytes':m['totalBytes'],'unexpectedFiles':[],'sourceChanged':False};R=B/'root-source39-preparation.v1';(R/'copy-verification.json').write_text(json.dumps(record,indent=2)+'\n');D=L/R.name;D.mkdir(exist_ok=True)
for name in ['prepare-source-copy.py','copy-verification.json']:shutil.copy2(R/name,D/name)
print(json.dumps(record))
