"""Retain the original independent reviewer's additive clarification, never overwrite history."""
from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();base=Path('/tmp/opensip-design-corrections');src=base/'post-reset-review.v17-clarification.v1';dest=root/'docs/coop/design-corrections/reviews/post-reset-review.v17-clarification.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
p=load(src/'process.json');r=load(src/'response.json');assert r.get('is_error') is False and r['session_id']==p['sessionId']=='e1b616a9-1419-46ed-8bfa-d768246973fc'
for n in ['clarification.json','clarification.md','review.json','review.md']:assert (src/n).is_file() and (src/n).stat().st_size>0
original=root/'docs/coop/design-corrections/reviews/post-reset-review.v17';assert sha(original/'review.json')==p['originalReviewSha256'];assert sha(original/'review.md')==p['originalMarkdownSha256']
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v17.json';assert sha(mp)==p['manifestSha256'];m=load(mp);snapshot=Path(m['snapshotRoot'])
for row in m['files']:
 q=snapshot/row['path'];assert sha(q)==row['sha256'] and q.stat().st_size==row['bytes']
assert not dest.exists();dest.mkdir();rows=[]
for q in sorted(src.rglob('*')):
 assert not q.is_symlink()
 if q.is_file():
  rel=q.relative_to(src);d=dest/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,d);assert sha(q)==sha(d);rows.append({'path':str(rel),'sha256':sha(d),'bytes':d.stat().st_size})
log=Path('/Users/sb/.claude/projects/-Users-sb-code-opensip-ai-opensip-arch')/(r['session_id']+'.jsonl');blocks=[]
for line in log.read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 if (d.get('timestamp') or '') < p['startedAt'].replace('+00:00','Z'):continue
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
tp=dest/'codex-clarification-public-tool-blocks.json';assert not tp.exists();tp.write_text(json.dumps(blocks,indent=2)+'\n');assert blocks
(dest/'codex-retention-custody.json').write_text(json.dumps({'standing':'Verbatim additive clarification of original independent source review, same actual Claude session. Original reports preserved. No Codex assent, blind/application/readiness acceptance inferred.','sessionId':r['session_id'],'source':str(src),'originalReview':{'path':str((original/'review.json').relative_to(root)),'sha256':p['originalReviewSha256']},'subjectManifestSha256':sha(mp),'frozenSourceFilesVerified':len(m['files']),'files':rows,'publicToolBlocks':{'path':tp.name,'sha256':sha(tp),'count':len(blocks),'selection':'Public tool_use/tool_result timestamp at or after clarification process start; no private thinking.'}},indent=2)+'\n');print(json.dumps({'files':len(rows),'publicBlocks':len(blocks),'sessionId':r['session_id']}))
