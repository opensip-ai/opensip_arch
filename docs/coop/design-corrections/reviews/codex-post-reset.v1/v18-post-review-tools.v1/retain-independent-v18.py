"""Retain actual completed v18 review and every output/source-copy delta. Not assent."""
from pathlib import Path
import argparse,json,hashlib,shutil,os
p=argparse.ArgumentParser();p.add_argument('--copy-root',action='append',required=True);a=p.parse_args()
root=Path.cwd();dc=root/'docs/coop/design-corrections';src=Path('/tmp/opensip-design-corrections/post-reset-review.v18');dest=dc/'reviews/post-reset-review.v18'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=dc/'reviews/candidate-subject.v18.json';expected=sha(mp);assert json.loads((src/'process.json').read_text())['manifestSha256']==expected
m=json.loads(mp.read_text());base={r['path']:r for r in m['files']};snapshot=Path(m['snapshotRoot'])
def verify():
 actual={str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
 assert actual==set(base)
 for rel,r in base.items():assert sha(snapshot/rel)==r['sha256'] and (snapshot/rel).stat().st_size==r['bytes'],rel
verify();response=json.loads((src/'response.json').read_text());assert response.get('is_error') is False
session=response['session_id'];assert session not in {'e1b616a9-1419-46ed-8bfa-d768246973fc','4b48ccdd-92fb-4f92-9db2-ac8942f796d6','15922f81-214f-4262-9201-227218b75e99','543080e2-18a0-42f2-bfd7-29858aaed6bb','77758b10-d7ba-4868-9d42-ae0b13e84cb6','4e3fe6be-4adf-46bc-b4d9-1b4c68349fe2','46ea25c0-21fc-4be6-9b57-61e46c61d64d','878e4b39-2d21-46b2-87bd-64f8d4db015f','f6955666-0878-461a-a4e1-2ca2c4f5e824','04af6558-0b64-4a99-9fa4-0ca5ad653a27','7954d0b3-0895-4506-ad06-08f320d35fe8'}
review=json.loads((src/'review.json').read_text());values=[review.get('subjectManifestSha256')]
if isinstance(review.get('subject'),dict):values.append(review['subject'].get('manifestSha256'))
values=[v for v in values if v is not None];assert values and all(v==expected for v in values)
assert all(type(review.get(k)) is list for k in ('newMustIssues','newShouldIssues'))
assert '--resume' not in json.loads((src/'process.json').read_text())['command']
copies=[Path(x) for x in a.copy_root];assert len(set(copies))==len(copies)
for cp in copies:
 assert not cp.is_absolute() and '..' not in cp.parts and (src/cp).is_dir()
 for other in copies:assert cp==other or cp not in other.parents
scans={};capture=[]
for cp in copies:
 actual={}
 for p in sorted((src/cp).rglob('*')):
  assert not p.is_symlink()
  if p.is_file():actual[str(p.relative_to(src/cp))]={'sha256':sha(p),'bytes':p.stat().st_size}
 unchanged=[];changed=[];added=[]
 for rel,r in actual.items():
  if rel in base and all(r[k]==base[rel][k] for k in ('sha256','bytes')):unchanged.append(rel)
  else:
   (changed if rel in base else added).append({'path':rel,**r,'beforeSha256':base.get(rel,{}).get('sha256')});capture.append(src/cp/rel)
 scans[str(cp)]={'baseManifestSha256':expected,'actualFiles':len(actual),'unchangedFiles':unchanged,'changedFiles':changed,'addedFiles':added,'deletedFiles':[{'path':rel,'beforeSha256':r['sha256'],'beforeBytes':r['bytes']} for rel,r in base.items() if rel not in actual]}
for d,dirs,files in os.walk(src):
 dp=Path(d)
 for n in list(dirs):
  if (dp/n).relative_to(src) in copies:dirs.remove(n)
 for n in files:
  p=dp/n;assert not p.is_symlink();capture.append(p)
assert len(capture)==len(set(capture))
log=Path(json.loads((src/'session-discovery.json').read_text())['logPath']);assert log.stem==session;blocks=[]
for line in log.read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks and not dest.exists();dest.mkdir();rows=[]
for p in sorted(capture):
 rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);digest=sha(p);shutil.copyfile(p,q);assert sha(q)==digest==sha(p);rows.append({'path':str(rel),'sha256':digest,'bytes':q.stat().st_size})
assert not (dest/'codex-source-copy-accounts.json').exists() and not (dest/'codex-tool-calls.json').exists()
(dest/'codex-source-copy-accounts.json').write_text(json.dumps(scans,indent=2)+'\n')
(dest/'codex-tool-calls.json').write_text(json.dumps(blocks,indent=2)+'\n')
verify();name='codex-retention-custody.json' if (dest/'custody.json').exists() else 'custody.json'
(dest/name).write_text(json.dumps({'standing':'Actual fresh independent Claude v18 review retained verbatim. No Codex assent, blind acceptance, readiness or product qualification inferred.','source':str(src),'sessionId':session,'files':rows,'subjectCustody':{'manifestPath':str(mp.relative_to(root)),'manifestSha256':expected,'fileCount':len(base),'beforeRetentionVerified':True,'afterRetentionVerified':True,'undeclaredFiles':[]},'sourceCopyAccounts':{'path':'codex-source-copy-accounts.json','sha256':sha(dest/'codex-source-copy-accounts.json'),'method':'Every named complete source copy fully inventoried against immutable v18; unchanged files reconstructible from verified base, all changed/added bytes retained and deletions explicit. All files outside named copies retained verbatim, including failed attempts and partial before-images. This mathematical base does not claim a reviewer originally constructed every copy from v18.'},'toolBlocks':{'path':'codex-tool-calls.json','sha256':sha(dest/'codex-tool-calls.json'),'count':len(blocks),'selection':'Exact public tool_use/tool_result from the fresh session; LF-only JSONL parsing, no private thinking retained.'}},indent=2)+'\n')
print(json.dumps({'sessionId':session,'verdict':review.get('verdict',review.get('overallVerdict')),'retainedFiles':len(rows),'copyRoots':list(scans),'publicToolBlocks':len(blocks)},indent=2))
