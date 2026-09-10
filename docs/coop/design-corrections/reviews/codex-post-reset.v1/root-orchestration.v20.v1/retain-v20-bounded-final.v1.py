from pathlib import Path
import json,hashlib,argparse,shutil
ap=argparse.ArgumentParser();ap.add_argument('name');a=ap.parse_args()
base=Path('/tmp/opensip-design-corrections');src=base/a.name
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dest=root/'docs/coop/design-corrections/reviews'/a.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((src/'response.json').read_text());proc=json.loads((src/'process.json').read_text())
assert receipt['is_error'] is False and receipt['subtype']=='success'
sid=receipt['session_id'];assert receipt.get('subagent_stats',{}).get('spawned',0)==0
assert not dest.exists();dest.mkdir()
rows=[]
for f in sorted(src.rglob('*')):
 if not f.is_file() or any(x in f.relative_to(src).parts for x in ['__pycache__','work','disposable','patchcheck','.venv','.venv312','.probe-venv']):continue
 assert not f.is_symlink();rel=f.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,q)
 assert sha(q)==sha(f);rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
blocks=[];seen=set();promptMatched=False;firstUser=None
for log in Path('/Users/sb/.claude/projects').glob('*/'+sid+'.jsonl'):
 for line in log.read_text().splitlines():
  d=json.loads(line);m=d.get('message',{});cs=m.get('content',[])
  if d.get('type')=='user' and m.get('role')=='user' and isinstance(cs,str):
   if firstUser is None:firstUser=cs
   if cs==(src/'prompt.txt').read_text():promptMatched=True
  if not isinstance(cs,list):continue
  for z in cs:
   if isinstance(z,dict) and z.get('type') in ['tool_use','tool_result']:
    k=json.dumps([d.get('uuid'),z],sort_keys=True)
    if k not in seen:seen.add(k);blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':z})
assert promptMatched and firstUser==(src/'prompt.txt').read_text(), 'Fresh exact initial prompt not verified'
blocks.sort(key=lambda v:v['timestamp'] or '')
p=dest/'public-tool-blocks.json';p.write_text(json.dumps(blocks,indent=2)+'\n')
custody={'standing':'Verbatim actual Claude bounded coauthor/assessment output. Full work/, disposable copies and virtual environments excluded; exact changed source and any separately needed reports are retained through additional custody. Exact changed source must be retained separately before integration; no independent acceptance or readiness authority is inferred.','sessionId':sid,'turns':receipt['num_turns'],'models':list(receipt['modelUsage']),'firstPromptMatched':True,'files':rows,'publicToolBlocks':{'count':len(blocks),'sha256':sha(p)},'privateThinkingRetained':False}
(dest/'custody.json').write_text(json.dumps(custody,indent=2)+'\n')
print(json.dumps({'name':a.name,'sessionId':sid,'files':len(rows),'publicBlocks':len(blocks)}))
