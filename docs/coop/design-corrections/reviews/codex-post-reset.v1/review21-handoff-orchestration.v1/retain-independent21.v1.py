"""Retain completed actual independent21 without duplicating its exact full source copy."""
from pathlib import Path
import hashlib,json,shutil

root=Path('/Users/sb/code/opensip-ai/opensip_arch')
src=Path('/tmp/opensip-design-corrections/post-reset-review.v21')
dest=root/'docs/coop/design-corrections/reviews/post-reset-review.v21'
manifest=root/'docs/coop/design-corrections/reviews/candidate-subject.v21.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(manifest)=='360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1'
m=json.loads(manifest.read_text());snapshot=Path(m['snapshotRoot'])
receipt=json.loads((src/'response.json').read_text())
assert receipt['is_error'] is False and receipt['subtype']=='success'
assert receipt['session_id']=='5256f644-14e4-41cb-93d5-fb19adf5a21b'
assert receipt.get('subagent_stats',{}).get('spawned',0)==0
for n in ('review.json','review.md'):assert (src/n).is_file()
assert not dest.exists()
expected={x['path']:x for x in m['files']}
assert {str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}==set(expected)
for rel,row in expected.items():assert sha(snapshot/rel)==row['sha256'] and (snapshot/rel).stat().st_size==row['bytes']
dest.mkdir();files=[]
def retain(p,rel):
 assert not p.is_symlink()
 q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 assert sha(q)==sha(p)
 files.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
for p in sorted(src.rglob('*')):
 rel=p.relative_to(src)
 if not p.is_file() or rel.parts[0]=='work' or '__pycache__' in rel.parts:continue
 retain(p,rel)
copy_accounts=[]
for d in sorted((src/'work').iterdir()):
 if d.is_file():
  retain(d,d.relative_to(src));continue
 assert d.is_dir()
 base=d/'tree' if (d/'tree/docs').is_dir() else d
 if not (base/'docs').is_dir():
  # Discriminating mutation trees were intentionally removed by the review harness;
  # retain all actual remaining outputs and their reconstructing probe source.
  for p in sorted(d.rglob('*')):
   if p.is_file():retain(p,p.relative_to(src))
  continue
 if base!=d:
  for p in sorted(d.rglob('*')):
   if p.is_file() and not p.is_relative_to(base):retain(p,p.relative_to(src))
 disk={str(p.relative_to(base)):p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 missing=sorted(set(expected)-set(disk));unchanged=0;deltas=[]
 for rel,p in sorted(disk.items()):
  h=sha(p);before=expected.get(rel)
  if before and h==before['sha256'] and p.stat().st_size==before['bytes']:
   unchanged+=1;continue
  retain(p,Path('copy-deltas')/d.name/'after'/rel)
  if before:retain(snapshot/rel,Path('copy-deltas')/d.name/'before'/rel)
  deltas.append({'path':rel,'beforeSha256':before['sha256'] if before else None,'afterSha256':h,'bytes':p.stat().st_size})
 copy_accounts.append({'copy':str(base.relative_to(src/'work')),'unchanged':unchanged,'missing':missing,'deltas':deltas,'reconstruction':'Copy exact frozen source, apply retained copy-deltas and listed removals. Exact source root is recorded; no repeated unchanged source tree retained.'})
blocks=[];seen=set();first=None;matched=False
for log in Path('/Users/sb/.claude/projects').glob('*/'+receipt['session_id']+'.jsonl'):
 for line in log.read_text().splitlines():
  d=json.loads(line);msg=d.get('message',{});cs=msg.get('content',[])
  if d.get('type')=='user' and msg.get('role')=='user' and isinstance(cs,str):
   if first is None:first=cs
   if cs==(src/'prompt.txt').read_text():matched=True
  if not isinstance(cs,list):continue
  for b in cs:
   if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):
    key=json.dumps([d.get('uuid'),b],sort_keys=True)
    if key not in seen:seen.add(key);blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert matched and first==(src/'prompt.txt').read_text()
blocks.sort(key=lambda x:x['timestamp'] or '')
p=dest/'public-tool-blocks.json';p.write_text(json.dumps(blocks,indent=2)+'\n')
account={'standing':'Verbatim completed actual independent review evidence. No root assent, blind acceptance, application acceptance or implementation authority inferred.',
 'sessionId':receipt['session_id'],'turns':receipt['num_turns'],'models':list(receipt['modelUsage']),
 'subjectManifestSha256':sha(manifest),'frozenFilesVerified':len(expected),'files':files,
 'copies':copy_accounts,'firstPromptMatched':True,'publicToolBlocks':{'count':len(blocks),'sha256':sha(p)},'privateThinkingRetained':False}
(dest/'custody.json').write_text(json.dumps(account,indent=2)+'\n')
print(json.dumps({'sessionId':receipt['session_id'],'files':len(files),'publicBlocks':len(blocks),'copies':copy_accounts},indent=2))
