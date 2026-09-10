import pathlib,json,hashlib,collections,sys
name=sys.argv[1]
role=sys.argv[2]
assert role in ("independent-design-review", "blind-consumer", "independent-application-review")
base=pathlib.Path('/tmp/opensip-design-corrections')
tmp=base/name
root=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch')
out=root/'docs/coop/design-corrections/reviews'/tmp.name
out.mkdir(exist_ok=False)
proc=json.loads((tmp/'process.json').read_text())
assert 'coauthor' not in proc.get('standing','').lower()
assert proc.get('freshSession') is True and '--resume' not in proc['command']
raw=json.loads((tmp/'response.raw.json').read_text())
assert raw['stopReason'] in ('end_turn','cancelled')
safe={k:raw[k] for k in ['text','stopReason','sessionId','requestId','usage','num_turns','modelUsage'] if k in raw}
(out/'response.public.json').write_text(json.dumps(safe,indent=2)+'\n')
(out/'assessment.md').write_text(safe['text']+'\n')
for n in ['prompt.txt','process.json','stderr.log']:(out/n).write_bytes((tmp/n).read_bytes())
(out/'retainer.py').write_bytes(pathlib.Path(__file__).read_bytes())
from urllib.parse import quote
command=json.loads((tmp/'process.json').read_text())['command']
cwd=pathlib.Path(command[command.index('--cwd')+1]).resolve()
source=pathlib.Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/raw['sessionId']/'chat_history.jsonl'
rows=[json.loads(x) for x in source.read_text().split('\n')[:-1] if x]
prompt=(tmp/'prompt.txt').read_text().strip()
def user_text(j):
 if j.get('type')!='user':return ''
 c=j.get('content',[])
 return '\n'.join(x.get('text','') for x in c if isinstance(x,dict) and x.get('type')=='text') if isinstance(c,list) else str(c)
starts=[i for i,j in enumerate(rows) if prompt in user_text(j)]
assert len(starts)==1,starts
start=starts[0];end=next((i for i in range(start+1,len(rows)) if '<user_query>' in user_text(rows[i])),len(rows))
public=[];names=collections.Counter();models=set()
for j in rows[start+1:end]:
 if j['type']=='assistant':
  public.append({k:j[k] for k in ['type','content','tool_calls','model_id'] if k in j})
  if j.get('model_id'):models.add(j['model_id'])
  for t in j.get('tool_calls',[]):names[t['name']]+=1
 elif j['type']=='tool_result':public.append({k:j[k] for k in ['type','tool_call_id','content'] if k in j})
(out/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(j,ensure_ascii=False)+'\n' for j in public))
(out/'session-account.json').write_text(json.dumps({'sessionId':raw['sessionId'],'models':sorted(models),'numTurns':raw['num_turns'],'toolCalls':dict(names),'publicBlocks':len(public),'promptFoundExactlyOnce':True,'standing':'Actual Grok '+role+' from a fresh session. Public transcript custody only; substantive verdict and exact subject binding require separate assessment.','completed':raw['stopReason']=='end_turn','stopReason':raw['stopReason']},indent=2)+'\n')
c=[]
for p in sorted(out.iterdir()):
 if p.is_file():
  b=p.read_bytes();c.append({'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(out/'custody.json').write_text(json.dumps({'files':c},indent=2)+'\n')
print(json.dumps({'out':str(out),'toolCalls':dict(names),'turns':raw['num_turns']},indent=2))
