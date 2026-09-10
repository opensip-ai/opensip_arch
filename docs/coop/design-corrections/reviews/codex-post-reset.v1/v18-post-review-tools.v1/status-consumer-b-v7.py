from pathlib import Path
import json,datetime
b=Path('/tmp/opensip-design-corrections/consumer-b.v7/output');s=json.loads((b/'session-discovery.json').read_text());rows=[]
for line in Path(s['logPath']).read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 for c in d.get('message',{}).get('content',[]):
  if isinstance(c,dict) and c.get('type')=='tool_use':rows.append({'at':d.get('timestamp'),'tool':c['name'],'target':c['input'].get('file_path',c['input'].get('command',''))[:200]})
print(json.dumps({'now':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sessionId':s['sessionId'],'recentPublicTools':rows[-5:],'files':{p.name:p.stat().st_size for p in b.iterdir() if p.is_file()}},indent=2))
