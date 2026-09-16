"""Retain actual completed final application review and exact package custody; never apply."""
from pathlib import Path
import argparse,hashlib,json,shutil
p=argparse.ArgumentParser()
for name in ('root','stage'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--version',required=True);a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();dc=root/'docs/coop/design-corrections';src=stage.parent/('application-review.'+a.version);dest=dc/'reviews'/src.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=stage/('application-subject.'+a.version+'.json');manifest=json.loads(mp.read_text());digest=sha(mp)
assert sha(root/manifest['retainedManifestPath'])==digest
response=json.loads((src/'response.json').read_text());assert response.get('is_error') is False
review=json.loads((src/'review.json').read_text());assert review['subjectManifestSha256']==digest
assert review['verdict'] in ('ACCEPT','CHANGES_REQUIRED','BLOCKED')
app=json.loads((stage/'files/docs/coop/design-corrections/application.v1.json').read_text());session=response['session_id']
prior=[]
for field in ('independentDesignReview','freshBlindConsumerReview'):
 r=root/app[field]['path'];assert sha(r)==app[field]['sha256'];rr=json.loads((r.parent/'response.json').read_text());prior.append(rr['session_id'])
assert session not in prior+['5dec928a-6357-4726-9ea8-49a3079fb726']
def verify():
 for field,base in [('files',stage/'files'),('beforeImages',stage/'before'),('support',stage)]:
  for row in manifest[field]:
   rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
   q=base/rel;assert q.is_file() and sha(q)==row['sha256'] and q.stat().st_size==row['bytes'],str(q)
verify();assert not dest.exists();logs=list(Path('/Users/sb/.claude/projects').glob('*/'+session+'.jsonl'));assert len(logs)==1
blocks=[]
for line in logs[0].read_text().split('\n'):
 if not line:continue
 d=json.loads(line);content=d.get('message',{}).get('content',[])
 for b in content if isinstance(content,list) else []:
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks;dest.mkdir();rows=[]
# Retain independently authored outputs. Disposable copied packages are represented as
# exact deltas against their frozen source, plus the full tool history.
excluded=[];deltas=[]
for q in sorted(src.rglob('*')):
 if not q.is_file() or '__pycache__' in q.parts:continue
 rel=q.relative_to(src)
 if rel.parts[0] in ('work','scratch','verify'):
  sub=Path(*rel.parts[1:]);matches=[base/sub for base in (stage,root)]
  if any(x.is_file() and sha(x)==sha(q) for x in matches):excluded.append(str(rel));continue
  deltas.append(str(rel))
 t=dest/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,t);rows.append({'path':str(rel),'sha256':sha(t),'bytes':t.stat().st_size,'origin':'Codex orchestration metadata' if q.name in ('prompt.txt','process.json') else 'Verbatim actual Claude independent application review output'})
t=dest/'tool-calls.json';t.write_text(json.dumps(blocks,indent=2)+'\n');verify()
retention_name='codex-retention-custody.json' if (dest/'custody.json').exists() else 'custody.json'
(dest/retention_name).write_text(json.dumps({'standing':'Actual fresh independent application review; only its substantive exact-subject verdict grants scope. Retention does not apply documentation.','sessionId':session,'differentFromDesignAndBlindSessions':prior,'manifestSha256':digest,'packageRoot':str(stage),'packageBeforeAndAfterRetentionVerified':True,'files':rows,'toolBlocks':{'path':'tool-calls.json','sha256':sha(t),'count':len(blocks),'selection':'Exact tool_use/tool_result; LF-only JSONL; no private thinking retained.'},'excludedExactDisposableCopies':excluded,'retainedDisposableDeltas':deltas,'implementationAuthorized':False,'qualificationClaimed':False},indent=2)+'\n')
print(session,review['verdict'],len(rows),'outputs',len(blocks),'tool blocks')
