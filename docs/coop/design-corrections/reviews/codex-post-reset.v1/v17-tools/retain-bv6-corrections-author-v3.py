"""Retain completed actual blind-v6 correction coauthor and all source-copy deltas. Not independent assent."""
from pathlib import Path
import argparse,json,hashlib,shutil,os
p=argparse.ArgumentParser();p.add_argument('--copy-root',action='append',required=True);a=p.parse_args()
root=Path.cwd();dc=root/'docs/coop/design-corrections';src=Path('/tmp/opensip-design-corrections/bv6-corrections-author.v3');dest=dc/'reviews/bv6-corrections-author.v3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=dc/'reviews/candidate-subject.v16.json';expected=sha(mp);assert json.loads((src/'process.json').read_text())['parentSubjectSha256']==expected
m=json.loads(mp.read_text());base={r['path']:r for r in m['files']};snapshot=Path(m['snapshotRoot'])
def verify():
 actual={str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
 assert actual==set(base)
 for rel,r in base.items():assert sha(snapshot/rel)==r['sha256'] and (snapshot/rel).stat().st_size==r['bytes'],rel
verify();response=json.loads((src/'response.json').read_text());assert response.get('is_error') is False
session=response['session_id'];assert session=='4b48ccdd-92fb-4f92-9db2-ac8942f796d6'
review=json.loads((src/'handoff.json').read_text());assert isinstance(review,dict)
assert (src/'handoff.md').is_file()
assert '--resume' in json.loads((src/'process.json').read_text())['command']
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
assert all(str(p.relative_to(src)) not in {'codex-source-copy-accounts.json','tool-calls.json','codex-retention-custody.json'} for p in capture), 'Root custody filename collision: choose distinct names before retaining'
for p in sorted(capture):
 rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);digest=sha(p);shutil.copyfile(p,q);assert sha(q)==digest==sha(p);rows.append({'path':str(rel),'sha256':digest,'bytes':q.stat().st_size})
(dest/'codex-source-copy-accounts.json').write_text(json.dumps(scans,indent=2)+'\n')
(dest/'tool-calls.json').write_text(json.dumps(blocks,indent=2)+'\n')
verify();name='codex-retention-custody.json' if (dest/'custody.json').exists() else 'custody.json'
(dest/name).write_text(json.dumps({'standing':'Actual resumed Claude correction coauthor retained verbatim. No root source assent, independent acceptance, readiness or product qualification inferred.','source':str(src),'sessionId':session,'files':rows,'subjectCustody':{'manifestPath':str(mp.relative_to(root)),'manifestSha256':expected,'fileCount':len(base),'beforeRetentionVerified':True,'afterRetentionVerified':True,'undeclaredFiles':[]},'sourceCopyAccounts':{'path':'codex-source-copy-accounts.json','sha256':sha(dest/'codex-source-copy-accounts.json'),'method':'Every named source copy fully inventoried against immutable v16; unchanged files reconstructible from verified base, all changed/added bytes retained and deletions explicit. All files outside named copies retained verbatim, including failed attempts and partial before-images. This mathematical base does not claim a reviewer originally constructed every copy from v16.'},'toolBlocks':{'path':'tool-calls.json','sha256':sha(dest/'tool-calls.json'),'count':len(blocks),'selection':'Exact public tool_use/tool_result from the entire same actual session through this completed follow-up (includes original v1 and resumed v2 turns; not all blocks are new v3 work); LF-only JSONL parsing, no private thinking retained.'}},indent=2)+'\n')
print(json.dumps({'sessionId':session,'technicalAssentReported':review.get('technicalAssent'),'retainedFiles':len(rows),'copyRoots':list(scans),'publicToolBlocks':len(blocks)},indent=2))
