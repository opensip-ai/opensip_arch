from pathlib import Path
import argparse, json, hashlib, shutil, os, datetime
ap=argparse.ArgumentParser();ap.add_argument('--copy-root',action='append',required=True);args=ap.parse_args()
root=Path.cwd();src=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');dest=root/'docs/coop/design-corrections/reviews/bv4-corrections-author.v3'
assert not dest.exists(), 'Never overwrite retained evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v13.json'
assert sha(mp)=='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
m=json.loads(mp.read_text());base={r['path']:r for r in m['files']};base_root=Path(m['snapshotRoot'])
for rel,r in base.items():assert sha(base_root/rel)==r['sha256'] and (base_root/rel).stat().st_size==r['bytes'],rel
response=json.loads((src/'response.json').read_text());session='77758b10-d7ba-4868-9d42-ae0b13e84cb6'
assert response.get('is_error') is False and response['session_id']==session
handoff_path=src/'handoff.json';assert handoff_path.is_file(), 'Inspect actual final handoff layout before retention'
handoff=json.loads(handoff_path.read_text());assert handoff['sourceRoot']==str(src/'work')
assert (src/'handoff.md').is_file()
checkpoints=sorted(src.glob('review-ready*.json'))
assert checkpoints, 'No checkpoint evidence'
latest=max(checkpoints,key=lambda p:p.stat().st_mtime_ns)
feedback=src/latest.name.replace('review-ready','root-review')
fd=json.loads(feedback.read_text())
assert fd.get('technicalAssent') is True and fd['checkpointSha256']==sha(latest), 'Latest submitted bytes require actual root checkpoint assent'
ready=json.loads(latest.read_text())
for row in ready['delta']['aggregateVsFrozenV13']['changedFiles']+ready['delta']['aggregateVsFrozenV13']['additions']:
 assert sha(src/'work'/row['path'])==row['afterSha256'], 'Source edited after root checkpoint assent'

# Final caller must explicitly name every full disposable source copy. All other
# files, including partial before-images, probes and unsuccessful logs, are copied.
copies=[Path(x) for x in args.copy_root];assert Path('work') in copies and len(set(copies))==len(copies)
for p in copies:assert not p.is_absolute() and '..' not in p.parts and (src/p).is_dir()
for a in copies:
 for b in copies:assert a==b or a not in b.parents, 'Nested copy-root ambiguity'
scans={};capture=[]
for cp in copies:
 actual={}
 for p in sorted((src/cp).rglob('*')):
  assert not p.is_symlink(),str(p)
  if p.is_file():actual[str(p.relative_to(src/cp))]={'sha256':sha(p),'bytes':p.stat().st_size}
 unchanged=[];changed=[];added=[];deleted=[]
 for rel,r in actual.items():
  if rel in base and r=={k:base[rel][k] for k in ('sha256','bytes')}:unchanged.append(rel)
  else:
   row={'path':rel,**r,'beforeSha256':base.get(rel,{}).get('sha256')}
   (changed if rel in base else added).append(row);capture.append(src/cp/rel)
 for rel in base:
  if rel not in actual:deleted.append({'path':rel,'beforeSha256':base[rel]['sha256'],'beforeBytes':base[rel]['bytes']})
 scans[str(cp)]={'baseManifestSha256':sha(mp),'actualFiles':len(actual),'unchangedFiles':unchanged,'changedFiles':changed,'addedFiles':added,'deletedFiles':deleted}
assert not scans['work']['deletedFiles'],'Released source deletions require separate substantive assessment'
# Require exact author declared source delta, with no silent source/pin/report edits.
aggregate=handoff['delta']['aggregateVsFrozenV13']
assert not aggregate['deletions']
owned=aggregate['changedFiles']+aggregate['additions'];declared={r['path']:r for r in owned}
assert all(isinstance(r,dict) and 'path' in r and 'afterSha256' in r for r in owned), 'Inspect actual addition row shape before retention'
assert len(declared)==len(owned)
actual_delta={r['path']:r for r in scans['work']['changedFiles']+scans['work']['addedFiles']}
assert declared.keys()==actual_delta.keys(),(sorted(declared.keys()-actual_delta.keys()),sorted(actual_delta.keys()-declared.keys()))
contracts={'docs/v2/contracts/product-v1/'+n+'.md' for n in ('identity-and-evidence','native-evidence','workflows-and-surfaces','admission-and-qualification','security-and-lifecycle')}
for rel,r in actual_delta.items():
 assert declared[rel].get('beforeSha256')==r['beforeSha256'] and declared[rel]['afterSha256']==r['sha256'],rel
 assert rel in contracts or rel in {'docs/coop/design-corrections/public-detail-registry.v1.json','docs/coop/design-corrections/integration-host-model.py','docs/coop/design-corrections/check-integration.py'} or any(rel.startswith('docs/coop/design-corrections/'+u+'/') for u in ('foundation','native','workflows')),rel
 assert 'source-pins' not in rel and 'report' not in Path(rel).name and '/reviews/' not in rel,rel
# Independently measure this turn against released v2, including every unmodified path.
previous_root=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v2/work')
previous_files={str(p.relative_to(previous_root)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in previous_root.rglob('*') if p.is_file()}
final_files={str(p.relative_to(src/'work')):{'sha256':sha(p),'bytes':p.stat().st_size} for p in (src/'work').rglob('*') if p.is_file()}
assert previous_files.keys()<=final_files.keys(), 'Released deletions require explicit assessment'
turn_delta={rel:{'v2Sha256':previous_files.get(rel,{}).get('sha256'),'finalSha256':r['sha256']} for rel,r in final_files.items() if r!=previous_files.get(rel)}
turn_account=handoff['delta']['thisTurnVsV2'];assert not turn_account['deletions']
turn_rows=turn_account['changedFiles']+turn_account['additions']
assert all(isinstance(r,dict) and 'path' in r and 'finalSha256' in r for r in turn_rows), 'Inspect actual addition row shape before retention'
turn_declared={r['path']:r for r in turn_rows} 
assert len(turn_declared)==len(turn_rows)
assert turn_delta.keys()==turn_declared.keys(), 'This-turn source account differs'
for rel,r in turn_delta.items():
 assert all(turn_declared[rel].get(k)==v for k,v in r.items()),rel
# Traverse outside named full copies; never drop unrecognized scratch directories.
for d,dirs,files in os.walk(src):
 dp=Path(d)
 for name in list(dirs):
  if (dp/name).relative_to(src) in copies:dirs.remove(name)
 for name in files:
  p=dp/name;assert not p.is_symlink();capture.append(p)
assert len(capture)==len(set(capture))
started=json.loads((src/'process.json').read_text())['startedAt'];blocks=[]
logs=list(Path('/Users/sb/.claude/projects').glob('*/'+session+'.jsonl'));assert len(logs)==1
for line in logs[0].read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 if not d.get('timestamp') or datetime.datetime.fromisoformat(d['timestamp']) < datetime.datetime.fromisoformat(started):continue
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):
   blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks
# Everything validated before creating additive repository evidence.
dest.mkdir();files=[]
for p in sorted(capture):
 rel=p.relative_to(src);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);before=sha(p);shutil.copyfile(p,q);assert sha(q)==before==sha(p)
 files.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
(dest/'source-copy-accounts.json').write_text(json.dumps(scans,indent=2)+'\n')
(dest/'tool-calls.json').write_text(json.dumps(blocks,indent=2)+'\n')
(dest/'custody.json').write_text(json.dumps({'standing':'Actual Claude Bv4 correction coauthor follow-up v3; not independent acceptance or product qualification. Verbatim outputs retain any source adaptations indicated by public tools; no private thinking retained.','source':str(src),'sessionId':session,'startedAt':started,'baseManifest':{'path':str(mp.relative_to(root)),'sha256':sha(mp)},'files':files,'sourceCopyAccounts':{'path':'source-copy-accounts.json','sha256':sha(dest/'source-copy-accounts.json'),'method':'Each named full source copy inventoried completely against immutable v13. Exact changed/added bytes retained under original relative paths; deleted rows explicit; identical rows reconstructible from verified frozen base. Partial before-images and all other output files retained verbatim.'},'toolBlocks':{'path':'tool-calls.json','sha256':sha(dest/'tool-calls.json'),'count':len(blocks),'selection':'Public tool_use/tool_result since v3 process start only, LF-only JSONL parsing. Earlier v1/v2 session blocks are excluded from this follow-up account.'}},indent=2)+'\n')
print(json.dumps({'sessionId':session,'retainedFiles':len(files),'sourceChangedFiles':len(actual_delta),'publicToolBlocks':len(blocks),'copyRoots':list(scans),'thisTurnChangedFiles':len(turn_delta)},indent=2))
