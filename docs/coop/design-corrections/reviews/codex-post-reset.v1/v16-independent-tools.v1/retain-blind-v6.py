"""Retain a completed actual fresh blind consumer, exact normative kit and its own code/results."""
from pathlib import Path
import argparse,hashlib,json,shutil
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--parent',required=True);a=p.parse_args();root=Path.cwd();dc=root/'docs/coop/design-corrections';src=Path('/tmp/opensip-design-corrections')/('consumer-b.'+a.version);dest=dc/'reviews'/src.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parent_path=dc/'reviews'/('candidate-subject.'+a.parent+'.json');parent_sha=sha(parent_path);parent=json.loads(parent_path.read_text());by_path={r['path']:r for r in parent['files']}
kit=src/'subject';inputs=json.loads((kit/'consumer-input-manifest.json').read_text());assert inputs['parentSubjectSha256']==parent_sha
response=json.loads((src/'output/response.json').read_text());assert response.get('is_error') is False,'Interrupted response must be retained separately'
review=json.loads((src/'output/blind-review.json').read_text());assert review.get('verdict',review.get('overallVerdict')) in ('ACCEPT-RECONSTRUCTABLE','CHANGES_REQUIRED','BLOCKED')
assert a.version=='v6' and a.parent=='v16', 'This prepared retainer is scoped to the actual accepted v16 parent and NEW v6 consumer'
assert '--resume' not in json.loads((src/'output/process.json').read_text())['command'], 'Blind must be fresh'
session=response['session_id'];assert session not in {'77758b10-d7ba-4868-9d42-ae0b13e84cb6','7954d0b3-0895-4506-ad06-08f320d35fe8','46ea25c0-21fc-4be6-9b57-61e46c61d64d','878e4b39-2d21-46b2-87bd-64f8d4db015f','4e3fe6be-4adf-46bc-b4d9-1b4c68349fe2','f6955666-0878-461a-a4e1-2ca2c4f5e824','04af6558-0b64-4a99-9fa4-0ca5ad653a27'}
design_response=json.loads((dc/'reviews'/('post-reset-review.'+a.parent)/'response.json').read_text());assert session!=design_response['session_id'] and session!='5dec928a-6357-4726-9ea8-49a3079fb726'
def verify():
 for row in inputs['files']:
  assert row==by_path[row['path']];q=kit/row['path'];assert sha(q)==row['sha256'] and q.stat().st_size==row['bytes']
  assert not row['path'].startswith('docs/coop/design-corrections/reviews/') and not row['path'].endswith('.py')
 actual={str(p.relative_to(kit)) for p in kit.rglob('*') if p.is_file()};assert actual=={r['path'] for r in inputs['files']}|{'consumer-input-manifest.json'}
verify();logs=list(Path('/Users/sb/.claude/projects').glob('*/'+session+'.jsonl'));assert len(logs)==1
blocks=[]
for line in logs[0].read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks and not dest.exists();dest.mkdir();files=[]
for p in sorted(src.rglob('*')):
 assert not p.is_symlink(), str(p)
 if not p.is_file() or '__pycache__' in p.parts:continue
 rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);digest=sha(p);shutil.copyfile(p,q);assert sha(q)==digest==sha(p)
 origin='Exact normative input bytes' if rel.parts[0]=='subject' else 'Verbatim actual Claude blind reconstruction/review evidence'
 if p.name in ('prompt.txt','process.json','consumer-input-manifest.json'):origin='Codex orchestration/input selection metadata'
 files.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size,'origin':origin})
tools=dest/'tool-calls.json';tools.write_text(json.dumps(blocks,indent=2)+'\n');verify()
(dest/'custody.json').write_text(json.dumps({'standing':'Actual fresh blind consumer evidence; substantive verdict and limitations retain their own scope. Normative kit and ALL independent reconstruction code/work output retained; no author model provided.','source':str(src),'sessionId':session,'differentFromDesignReviewer':design_response['session_id'],'parentSubjectSha256':parent_sha,'inputFileCount':len(inputs['files']),'inputsBeforeRetentionVerified':True,'inputsAfterRetentionVerified':True,'files':files,'toolBlocks':{'path':'tool-calls.json','sha256':sha(tools),'count':len(blocks),'selection':'Exact tool_use/tool_result blocks; LF-only JSONL parsing, no private thinking retained.'},'implementationAuthorized':False,'productQualification':False},indent=2)+'\n')
print(session,review.get('verdict',review.get('overallVerdict')),len(inputs['files']),'input files',len(files),'retained files',len(blocks),'tool blocks')
