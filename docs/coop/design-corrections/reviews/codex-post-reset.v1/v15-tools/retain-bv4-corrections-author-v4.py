"""Prepared v4 custody retainer. Inspect actual final shape/copy roots and source assent before execution."""
from pathlib import Path
import argparse,json,hashlib,shutil,os,datetime
p=argparse.ArgumentParser();p.add_argument('--copy-root',action='append',required=True);a=p.parse_args();root=Path.cwd();src=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4');dest=root/'docs/coop/design-corrections/reviews/bv4-corrections-author.v4';assert not dest.exists();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v14.json';expected='45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c';assert sha(mp)==expected;m=json.loads(mp.read_text());base={r['path']:r for r in m['files']};snap=Path(m['snapshotRoot'])
assert {str(p.relative_to(snap)) for p in snap.rglob('*') if p.is_file()}==set(base)
for rel,r in base.items():assert sha(snap/rel)==r['sha256'] and (snap/rel).stat().st_size==r['bytes'],rel
response=json.loads((src/'response.json').read_text());sid='77758b10-d7ba-4868-9d42-ae0b13e84cb6';assert response.get('is_error') is False and response['session_id']==sid
h=json.loads((src/'handoff.json').read_text());assert h['sourceRoot']==str(src/'work') and (src/'handoff.md').is_file();delta=h['delta']['againstFrozenV14'];assert not delta['additions'] and not delta['deletions'],'Inspect additions/deletions substantively and adapt retainer first'
ready=max(src.glob('review-ready*.json'),key=lambda p:p.stat().st_mtime_ns);feedback=ready.with_name(ready.name.replace('review-ready','root-review'));f=json.loads(feedback.read_text());assert f['technicalAssent'] is True and f['checkpointSha256']==sha(ready)
rd=json.loads(ready.read_text());assert rd['delta']['againstFrozenV14']['changedFiles']==delta['changedFiles'];owned={r['path']:r for r in delta['changedFiles']};assert len(owned)==len(delta['changedFiles'])
for rel,r in owned.items():
 assert r['beforeSha256']==base[rel]['sha256'] and sha(src/'work'/rel)==r['afterSha256'];assert sha(src/'before-images'/rel)==r['beforeSha256']
 assert rel.startswith('docs/v2/contracts/product-v1/') or rel=='docs/coop/design-corrections/public-detail-registry.v1.json' or any(rel.startswith('docs/coop/design-corrections/'+u+'/') for u in ['foundation','native','workflows']),rel
 assert '/reviews/' not in rel and 'source-pins' not in rel and 'report' not in Path(rel).name,rel
copies=[Path(x) for x in a.copy_root];assert Path('work') in copies and len(set(copies))==len(copies)
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
  if rel in base and all(r[k]==base[rel][k] for k in ['sha256','bytes']):unchanged.append(rel)
  else:(changed if rel in base else added).append({'path':rel,**r,'beforeSha256':base.get(rel,{}).get('sha256')});capture.append(src/cp/rel)
 deleted=[{'path':rel,'beforeSha256':r['sha256'],'beforeBytes':r['bytes']} for rel,r in base.items() if rel not in actual]
 scans[str(cp)]={'baseManifestSha256':expected,'actualFiles':len(actual),'unchangedFiles':unchanged,'changedFiles':changed,'addedFiles':added,'deletedFiles':deleted}
released=scans['work'];assert not released['addedFiles'] and not released['deletedFiles'];actual={r['path']:r for r in released['changedFiles']};assert actual.keys()==owned.keys()
for rel,r in actual.items():assert r['beforeSha256']==owned[rel]['beforeSha256'] and r['sha256']==owned[rel]['afterSha256']
for d,dirs,files in os.walk(src):
 dp=Path(d)
 for name in list(dirs):
  if (dp/name).relative_to(src) in copies:dirs.remove(name)
 for name in files:
  p=dp/name;assert not p.is_symlink();capture.append(p)
assert len(capture)==len(set(capture));start=json.loads((src/'process.json').read_text())['startedAt'];log=Path(json.loads((src/'session-discovery.json').read_text())['logPath']);assert log.stem==sid;blocks=[]
for line in log.read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 if not d.get('timestamp') or datetime.datetime.fromisoformat(d['timestamp'])<datetime.datetime.fromisoformat(start):continue
 c=d.get('message',{}).get('content',[])
 for b in c if isinstance(c,list) else []:
  if isinstance(b,dict) and b.get('type') in ['tool_use','tool_result']:blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks;dest.mkdir();rows=[]
for p in sorted(capture):
 rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);digest=sha(p);shutil.copy2(p,q);assert sha(q)==digest==sha(p);rows.append({'path':str(rel),'sha256':digest,'bytes':q.stat().st_size})
(dest/'source-copy-accounts.json').write_text(json.dumps(scans,indent=2)+'\n');(dest/'tool-calls.json').write_text(json.dumps(blocks,indent=2)+'\n')
(dest/'custody.json').write_text(json.dumps({'standing':'Actual Claude v4 coauthor follow-up, not independent acceptance. Fullcopy deltas against immutablev14 and exact publictools sincev4start; no private thinking.','source':str(src),'sessionId':sid,'startedAt':start,'baseManifest':{'path':str(mp.relative_to(root)),'sha256':expected},'files':rows,'sourceCopyAccounts':{'path':'source-copy-accounts.json','sha256':sha(dest/'source-copy-accounts.json'),'method':'Every named complete source copy inventoried; unchanged rows reconstructible from verified frozenv14, changed/added bytes retained and deletions explicit. All files outside fullcopies retained verbatim.'},'toolBlocks':{'path':'tool-calls.json','sha256':sha(dest/'tool-calls.json'),'count':len(blocks),'selection':'tool_use/tool_result since actualv4process.startedAt, LF-onlyJSONL; previous resumed-session turns excluded.'}},indent=2)+'\n');print(json.dumps({'retainedFiles':len(rows),'sourceChangedFiles':len(owned),'sourceCopyRoots':list(scans),'publicToolBlocks':len(blocks)},indent=2))
