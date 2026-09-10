"""Continue a genuinely fresh-origin review without relabelling a coauthor."""
from pathlib import Path
import argparse,json,hashlib,subprocess,datetime
p=argparse.ArgumentParser();p.add_argument('--origin',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--role',choices=['blind-consumer','independent-design-review','independent-application-review'],required=True);p.add_argument('--max-turns',type=int,default=120);p.add_argument('--reasoning-effort',choices=['high'],default='high');a=p.parse_args();assert 1 <= a.max_turns <= 240
origin=a.origin.resolve();previous=a.previous.resolve();out=a.out.resolve();proc=json.loads((origin/'process.json').read_text());prior=json.loads((previous/'response.raw.json').read_text())
assert proc['freshSession'] is True and '--resume' not in proc['command']
assert 'coauthor' not in proc.get('standing','').lower()
first=json.loads((origin/'response.raw.json').read_text());session=first['sessionId']
assert prior['sessionId']==session and prior['stopReason'] in ['end_turn','cancelled']
assert out.is_dir() and (out/'prompt.txt').is_file() and not (out/'process.json').exists()
cwd=proc['command'][proc['command'].index('--cwd')+1]
command=['/Users/sb/.grok/bin/grok','--cwd',cwd,'--resume',session,'--permission-mode','acceptEdits','--no-subagents','--disable-web-search','--reasoning-effort',a.reasoning_effort,'--max-turns',str(a.max_turns),'--output-format','json','--prompt-file',str(out/'prompt.txt')]
with (out/'response.raw.json').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:child=subprocess.Popen(command,stdout=stdout,stderr=stderr,start_new_session=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'process.json').write_text(json.dumps({'pid':child.pid,'command':command,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sessionId':session,'freshSession':False,'freshOrigin':{'path':str(origin),'processSha256':sha(origin/'process.json'),'sessionId':session},'previousContinuation':str(previous),'standing':'Actual Grok '+a.role+' continuation of verified fresh review origin; not a new session or automatic acceptance.'},indent=2)+'\n');print(child.pid)
