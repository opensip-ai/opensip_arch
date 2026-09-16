from pathlib import Path
import json, hashlib, subprocess
R=Path('/tmp/opensip-design-corrections'); O=Path(__file__).parent; D=R/'consumer24-corrections-successor.v1/source'; B=R/'candidate-subject.v38'; A=R/'claude-consumer24-workflow-author.v2'
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=json.loads((A/'receipts/final-custody-and-diff.json').read_bytes())['changedFilesVsSource38']
pending=[]; conflicts=[]
for r in rows:
 p=r['path']; base=(B/p).read_bytes(); current=(D/p).read_bytes(); authored=(A/'work/source38-work'/p).read_bytes()
 assert sha(base)==r['source38Sha256'] and sha(authored)==r['v2Sha256']
 m=O/'merge-inputs'/p; m.parent.mkdir(parents=True,exist_ok=True)
 for suffix,b in [('base',base),('current',current),('authored',authored)]:Path(str(m)+'.'+suffix).write_bytes(b)
 if current==base: final=authored; mode='direct'
 else:
  proc=subprocess.run(['git','merge-file','-p',str(m)+'.current',str(m)+'.base',str(m)+'.authored'],capture_output=True)
  Path(str(m)+'.merged').write_bytes(proc.stdout);Path(str(m)+'.stderr').write_bytes(proc.stderr)
  if proc.returncode: conflicts.append(p);continue
  final=proc.stdout;mode='three-way'
 pending.append((p,current,final,mode))
if conflicts:
 (O/'conflicts.json').write_text(json.dumps(conflicts,indent=2)); print('CONFLICTS',conflicts);raise SystemExit(1)
report=[]
for p,b,f,mode in pending:
 assert (D/p).read_bytes()==b
 backup=O/'before'/p;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
 (D/p).write_bytes(f);report.append({'path':p,'beforeSha256':sha(b),'sha256':sha(f),'bytes':len(f),'mode':mode})
(O/'integration.json').write_text(json.dumps({'standing':'mutable author integration, not acceptance','files':report},indent=2)+'\n')
print('Integrated',len(report),'paths',[(r['path'],r['mode']) for r in report if r['mode']!='direct'])
