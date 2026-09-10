from pathlib import Path
import json,hashlib,shutil
R=Path.cwd();src=Path('/tmp/opensip-design-corrections/v21-evaluator-contract-assessment.v1');dest=R/'docs/coop/design-corrections/reviews'/src.name
response=json.loads((src/'response.json').read_text());assert not response['is_error'] and response['session_id']=='006a1d7b-0dff-4d8b-98ce-a5ba8abf6e1b' and not response['subagent_stats']['spawned'];assert not dest.exists();dest.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for p in sorted(src.rglob('*')):
 assert not p.is_symlink()
 if not p.is_file():continue
 q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(q)==sha(p);files.append({'path':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
log=Path(json.loads((src/'session-discovery.json').read_text())['logPath']);blocks=[];first=None
for line in log.read_text().split('\n'):
 if not line:continue
 x=json.loads(line);m=x.get('message',{});cs=m.get('content',[])
 if first is None and x.get('type')=='user' and isinstance(cs,str):first=cs
 for c in cs if isinstance(cs,list) else []:
  if isinstance(c,dict) and c.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':x.get('timestamp'),'messageUuid':x.get('uuid'),'block':c})
assert first==(src/'prompt.txt').read_text();q=dest/'tool-calls.json';q.write_text(json.dumps(blocks,indent=2)+'\n')
(dest/'custody.json').write_text(json.dumps({'standing':'Verbatim actual bounded Claude coauthor assessment. Not blind, source assent, independent acceptance or application. Read-scope and proposed remedies require root substantive assessment.','sessionId':response['session_id'],'actualModel':list(response['modelUsage']),'exactFirstPromptVerified':True,'files':files,'publicToolBlocks':{'path':q.name,'sha256':sha(q),'count':len(blocks)},'productImplementation':False},indent=2)+'\n')
print(dest,len(files),len(blocks),sha(dest/'assessment.json'),sha(dest/'assessment.md'))
