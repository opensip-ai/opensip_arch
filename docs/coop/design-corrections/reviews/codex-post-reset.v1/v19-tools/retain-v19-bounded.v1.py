from pathlib import Path
import json,hashlib,datetime,argparse
ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('--end-before');a=ap.parse_args();b=Path('/tmp/opensip-design-corrections');r=Path('/Users/sb/code/opensip-ai/opensip_arch');src=b/a.name;dest=r/'docs/coop/design-corrections/reviews'/a.name;dest.mkdir(exist_ok=False);load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();receipt=load(src/'response.json');proc=load(src/'process.json');sid=receipt['session_id'];assert not receipt['is_error'] and sid==proc['sessionId'];rows=[]
for f in sorted(src.rglob('*')):
 if not f.is_file() or any(x in f.parts for x in ['__pycache__','disposable','.probe-venv']):continue
 rel=f.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);assert not f.is_symlink();q.write_bytes(f.read_bytes());assert sha(q)==sha(f);rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
blocks=[];seen=set()
for log in Path('/Users/sb/.claude/projects').glob('*/'+sid+'.jsonl'):
 for line in log.read_text().splitlines():
  d=json.loads(line);at=d.get('timestamp','')
  if at<proc['startedAt'][:19] or (a.end_before and at>=a.end_before[:19]):continue
  for z in d.get('message',{}).get('content',[]):
   if isinstance(z,dict) and z.get('type') in ['tool_use','tool_result']:
    k=json.dumps([d.get('uuid'),z],sort_keys=True)
    if k not in seen:seen.add(k);blocks.append({'timestamp':at,'messageUuid':d.get('uuid'),'block':z})
blocks.sort(key=lambda v:v['timestamp']);p=dest/'public-tool-blocks.json';p.write_text(json.dumps(blocks,indent=2)+'\n');(dest/'custody.json').write_text(json.dumps({'standing':'Exact actual bounded source coauthor outputs; no independent acceptance. Disposable unchanged copies excluded; probes/reports/failures preserved.','sessionId':sid,'turns':receipt['num_turns'],'files':rows,'publicToolBlocks':{'count':len(blocks),'sha256':sha(p)},'privateThinkingRetained':False,'logEndExclusive':a.end_before},indent=2)+'\n');print(json.dumps({'name':a.name,'files':len(rows),'publicToolBlocks':len(blocks)}))
