from pathlib import Path
import json,hashlib,datetime,shutil
b=Path('/tmp/opensip-design-corrections');repo=Path('/Users/sb/code/opensip-ai/opensip_arch');src=b/'v19-native-coauthor.v1';dest=repo/'docs/coop/design-corrections/reviews/v19-native-coauthor.v1';dest.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());h=load(src/'handoff.json');r=load(src/'response.json');p=load(src/'process.json');sid=r['session_id'];end=load(b/'v19-subject-coauthor.v1/process.json')['startedAt'];assert sid=='4b48ccdd-92fb-4f92-9db2-ac8942f796d6' and not r['is_error'];frozen=b/'candidate-subject.v18';manifest=load(repo/'docs/coop/design-corrections/reviews/candidate-subject.v18.json');mrows=manifest.get('files');assert isinstance(mrows,list);changed=[];checked=0
for row in mrows:
 rel=row['path'];s=src/'work'/rel;before=frozen/rel;assert sha(before)==row['sha256'];assert s.is_file();checked+=1
 if sha(s)!=row['sha256']:changed.append(rel)
new=[str(f.relative_to(src/'work')) for f in (src/'work').rglob('*') if f.is_file() and '__pycache__' not in f.parts and str(f.relative_to(src/'work')) not in {r['path'] for r in mrows}]
assert sorted(changed+new)==sorted(x['path'] for x in h['changedFiles']),(changed,new)
files=[]
def retain(f,rel):
 q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);assert not f.is_symlink();q.write_bytes(f.read_bytes());assert sha(q)==sha(f);files.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
for row in h['changedFiles']:
 f=src/'work'/row['path'];assert sha(f)==row['v19Sha256'];retain(f,Path('source')/row['path'])
for f in src.iterdir():
 if f.is_file():retain(f,Path(f.name))
for sub in ['out/probes','out/evidence']:
 for f in (src/sub).rglob('*'):
  if f.is_file() and '__pycache__' not in f.parts:retain(f,f.relative_to(src))
blocks=[];seen=set()
for log in Path('/Users/sb/.claude/projects').glob('*/'+sid+'.jsonl'):
 for line in log.read_text().splitlines():
  d=json.loads(line);at=d.get('timestamp','')
  if at<p['startedAt'][:19] or at>=end[:19]:continue
  for block in d.get('message',{}).get('content',[]):
   if isinstance(block,dict) and block.get('type') in ['tool_use','tool_result']:
    key=json.dumps([d.get('uuid'),block],sort_keys=True)
    if key not in seen:seen.add(key);blocks.append({'timestamp':at,'messageUuid':d.get('uuid'),'block':block})
blocks.sort(key=lambda x:x['timestamp']);(dest/'public-tool-blocks.json').write_text(json.dumps(blocks,indent=2)+'\n')
report={'standing':'Exact actual coauthor outputs/delta retained; unchanged full544MB beforecopy and disposable repinned trees omitted, reproducible against archived frozen18. Original evidence not edited. Root full handoff/source reading complete; final integration pending separate consistency/projection coauthors.','sessionId':sid,'turns':r['num_turns'],'verifiedFrozenParentFiles':checked,'changed':changed,'new':new,'files':files,'publicToolBlocks':len(blocks),'logEndExclusive':end,'privateThinkingRetained':False};(dest/'custody.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'files':len(files),'blocks':len(blocks),'verified':checked,'changed':changed,'new':new}))
