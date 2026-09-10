from pathlib import Path
import os,json,hashlib,shutil
root=Path.cwd();base=Path('/tmp/opensip-design-corrections');src=base/'v18-checker-coauthor.v1';dest=root/'docs/coop/design-corrections/reviews/v18-checker-coauthor.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());response=load(src/'response.json');process=load(src/'process.json');assert response['is_error'] is False and response['session_id']==process['sessionId'];assert not dest.exists()
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v17.json';m=load(mp);assert sha(mp)==process['sourceParentManifestSha256'];snapshot=Path(m['snapshotRoot']);manifest={r['path']:r for r in m['files']}
for rel,row in manifest.items():assert sha(snapshot/rel)==row['sha256'] and (snapshot/rel).stat().st_size==row['bytes']
copies=[Path(x) for x in ['work','work-injected/frozen','work-injected/proposed']];capture=[];accounts={}
for cp in copies:
 assert (src/cp).is_dir();actual={}
 for p in sorted((src/cp).rglob('*')):
  assert not p.is_symlink()
  if p.is_file():actual[str(p.relative_to(src/cp))]={'sha256':sha(p),'bytes':p.stat().st_size}
 unchanged=[];changed=[];added=[]
 for rel,row in actual.items():
  if rel in manifest and all(row[k]==manifest[rel][k] for k in ('sha256','bytes')):unchanged.append(rel)
  else:
   (changed if rel in manifest else added).append({'path':rel,**row,'beforeSha256':manifest.get(rel,{}).get('sha256')});capture.append(src/cp/rel)
 accounts[str(cp)]={'standing':'Explicitly partial disposable source copy; reviews intentionally omitted except three named feedback files. Missing inventory is recorded, not a claim all7671 were copied. Changed/added bytes retained; unchanged bytes reconstruct from verified frozen17.','actualFiles':len(actual),'unchangedFiles':unchanged,'changedFiles':changed,'addedFiles':added,'omittedFiles':sorted(set(manifest)-set(actual))}
for d,dirs,files in os.walk(src):
 dp=Path(d)
 for n in list(dirs):
  if (dp/n).relative_to(src) in copies:dirs.remove(n)
 for n in files:capture.append(dp/n)
assert len(capture)==len(set(capture));dest.mkdir();rows=[]
for p in sorted(capture):
 assert not p.is_symlink();rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(p)==sha(q);rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
log=Path(load(base/'bv6-corrections-author.v6/session-discovery.json')['logPath']);assert log.stem==response['session_id'];blocks=[]
for line in log.read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 if (d.get('timestamp') or '')<process['startedAt'].replace('+00:00','Z'):continue
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
for name,value in [('codex-source-copy-accounts.json',accounts),('codex-public-tool-blocks.json',blocks)]:assert not (dest/name).exists();(dest/name).write_text(json.dumps(value,indent=2)+'\n')
(dest/'codex-retention-custody.json').write_text(json.dumps({'standing':'Verbatim actual source-coauthor review and source-copy delta custody; not independent acceptance.','sessionId':response['session_id'],'files':rows,'baseManifestSha256':sha(mp),'baseFilesVerified':len(manifest),'sourceCopyAccounts':{'path':'codex-source-copy-accounts.json','sha256':sha(dest/'codex-source-copy-accounts.json')},'publicToolBlocks':{'path':'codex-public-tool-blocks.json','sha256':sha(dest/'codex-public-tool-blocks.json'),'count':len(blocks),'selection':'Timestamp at/after this coauthor process start; exact public tool_use/tool_result; no private thinking.'}},indent=2)+'\n');print(json.dumps({'files':len(rows),'publicBlocks':len(blocks),'copies':{k:{'actual':v['actualFiles'],'changed':len(v['changedFiles']),'added':len(v['addedFiles']),'omitted':len(v['omittedFiles'])} for k,v in accounts.items()}}))
