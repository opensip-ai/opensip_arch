from pathlib import Path
import datetime,json
B=Path('/tmp/opensip-design-corrections/consumer-b.v7/output');proc=json.loads((B/'process.json').read_text());start=datetime.datetime.fromisoformat(proc['startedAt']).timestamp();found=[]
for p in Path('/Users/sb/.claude/projects').glob('*/*.jsonl'):
 if p.stat().st_mtime<start:continue
 with p.open() as f:
  for i,line in enumerate(f):
   if i>=30:break
   d=json.loads(line);m=d.get('message',{})
   if m.get('role')!='user':continue
   c=m.get('content',[]);text=c if isinstance(c,str) else '\n'.join(v.get('text','') for v in c if isinstance(v,dict) and v.get('type')=='text')
   if str(B) in text and proc['parentSubjectSha256'] in text:found.append({'sessionId':p.stem,'logPath':str(p)});break
assert len(found)==1,found
p=B/'session-discovery.json'
if p.exists():assert json.loads(p.read_text())==found[0]
else:p.write_text(json.dumps(found[0],indent=2)+'\n')
print(json.dumps(found[0]))
