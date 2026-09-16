"""Preserve current joint work and clean-run evidence without changing predecessors."""
from pathlib import Path
import hashlib,json,shutil
H=Path(__file__).resolve().parent
clean=json.loads((H/'clean-staging-01.json').read_bytes());assert clean['passed']
evidence=H/'clean-staging-evidence-01';evidence.mkdir(exist_ok=False)
for p in Path(clean['directory']).iterdir():
 if p.is_file() and p.suffix in ('.json','.stdout','.stderr') and not p.name.endswith('.fixture.json'):shutil.copyfile(p,evidence/p.name)
p=H/'integration-status.json';d=json.loads(p.read_bytes());d['latestChecks']['cleanStaging']=clean;p.write_text(json.dumps(d,indent=2)+'\n')
p=H/'README.md';p.write_text(p.read_text()+'\n`clean-staging-01.json` passes all five verification phases after fresh initial\nregeneration; zero generated fixtures, schemas or models were copied in. The\ninitial source pins and all clean-run result/log files are preserved here.\nExternal frozen sources remain necessary; this is not sandbox qualification.\n')
D=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/report-joint-09-checkpoint-06');D.mkdir(exist_ok=False)
rows=[]
for p in sorted(H.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts:continue
 assert not p.is_symlink();rel=p.relative_to(H);raw=p.read_bytes();target=D/'working-copy'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 assert target.read_bytes()==raw
 rows.append({'path':str(rel),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
result={'standing':'Durable root work-in-progress checkpoint06; not a frozen review target, acceptance or implementation qualification','liveWorktree':str(H),'files':rows,'fileCount':len(rows),'bytes':sum(r['bytes'] for r in rows),'allCopiedBytesVerified':True,'next':'Rebase generation and codec onto inventory6 provenance, select final sources and obtain actual Claude review. L01/L02 and product implementation remain unfinished.'}
(D/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['fileCount','bytes','allCopiedBytesVerified']}))
