"""Retain public final-review runtime outputs; never overwrite history or grant acceptance.
The launcher already discards private content before writing public-events/result.
Only documented runtime trees are considered; private/session directories are excluded
by path BEFORE their file bytes are read. Exact candidate26 copies are deduplicated.
"""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest();raw=a.manifest.read_bytes();assert sha(raw)==a.manifest_sha256;subject=json.loads(raw);snapshot=Path(subject['snapshotRoot']);known={}
for row in subject['files']:
 b=(snapshot/row['path']).read_bytes();assert sha(b)==row['sha256'] and len(b)==row['bytes'];known.setdefault(row['sha256'],row['path'])
rt=a.runtime.resolve();dest=a.repo/'docs/coop/design-corrections/reviews'/rt.name;dest.mkdir(exist_ok=True)
assert (rt/'process-completion.json').is_file() and (rt/'result.json').is_file(), 'Incomplete process needs an explicitly partial retainer'
completion=json.loads((rt/'process-completion.json').read_bytes());result=json.loads((rt/'result.json').read_bytes());assert completion['exitCode']==0 and result.get('is_error') is not True, 'Non-completion must retain incomplete standing explicitly'
assert not (dest/'final-public-artifact-manifest.json').exists(), 'Do not reretain completed evidence'
private_dirs={'.claude','.grok','.git','__pycache__','compaction','compaction_checkpoints','terminal'}
private_names={'chat_history.jsonl','chat_history.jsonl.lock','events.jsonl','updates.jsonl','updates.jsonl.lock','system_prompt.txt','response.raw.json'}
rows=[];excluded=[]
for f in sorted(rt.rglob('*')):
 rel=f.relative_to(rt)
 if any(x in private_dirs for x in rel.parts) or f.name in private_names:
  excluded.append(rel.as_posix());continue
 if not f.is_file():continue
 assert not f.is_symlink(), 'Unexpected runtime symlink: '+str(rel)
 b=f.read_bytes();h=sha(b);r={'runtimePath':rel.as_posix(),'sha256':h,'bytes':len(b)}
 # Keep actual input custody distinct from authored outputs; both are public.
 if h in known and len(rel.parts)>1:
  r['sameAsSubjectPath']=known[h]
 else:
  q=dest/'runtime-evidence'/rel;q.parent.mkdir(parents=True,exist_ok=True)
  if q.exists():assert q.read_bytes()==b,'Preserve differing retained file: '+str(q)
  else:q.write_bytes(b)
  r['retainedPath']=q.relative_to(dest).as_posix()
 rows.append(r)
# Convenient primary reports retain exact authored bytes, never final-response substitution.
for name in ['review.md','review.json','output/blind-review.md','output/blind-review.json']:
 f=rt/name
 if f.is_file():
  q=dest/Path(name).name
  if q.exists():assert q.read_bytes()==f.read_bytes()
  else:q.write_bytes(f.read_bytes())
d={'standing':'Exact public reviewer evidence retained; root substantive assessment still required. No review or application acceptance inferred.','runtime':str(rt),'actualSessionId':result['session_id'],'subjectManifestSha256':a.manifest_sha256,'subjectManifestPath':str(a.manifest),'deduplication':'sameAsSubjectPath resolves through the exact verified frozen manifest/archive. No modified file deduplicated.','files':rows,'excludedPathsBeforeReadingBytes':excluded,'processExitCode':completion['exitCode'],'resultIsError':result.get('is_error')};(dest/'final-public-artifact-manifest.json').write_text(json.dumps(d,indent=2)+'\n');print('Retained public runtime',rt.name,len(rows),'files',sum('retainedPath' in r for r in rows),'stored, rest exact subject duplicates')
