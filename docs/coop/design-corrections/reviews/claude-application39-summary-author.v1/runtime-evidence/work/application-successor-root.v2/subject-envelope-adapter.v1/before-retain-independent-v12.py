"""Retain a completed actual independent review, tool evidence and frozen-source custody."""
from pathlib import Path
import argparse,json,hashlib,shutil
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--manifest-sha',required=True);a=p.parse_args()
root=Path.cwd();dc=root/'docs/coop/design-corrections';src=Path('/tmp/opensip-design-corrections')/('post-reset-review.'+a.version);dest=dc/'reviews'/src.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=dc/'reviews'/('candidate-subject.'+a.version+'.json');assert sha(manifest)==a.manifest_sha;m=json.loads(manifest.read_text());snapshot=Path(m['snapshotRoot'])
def verify():
 for row in m['files']:
  p=snapshot/row['path'];assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
 paths={str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
 assert paths=={r['path'] for r in m['files']},paths-{r['path'] for r in m['files']}
verify()
response=json.loads((src/'response.json').read_text());assert response.get('is_error') is False,'Retain an interrupted response separately; this path requires completed review'
review=json.loads((src/'review.json').read_text());assert review['subject']['manifestSha256']==a.manifest_sha
session=response['session_id'];assert session not in ('5dec928a-6357-4726-9ea8-49a3079fb726','f360faba-3928-4c74-8b5a-0c1e07114222')
logs=list(Path('/Users/sb/.claude/projects').glob('*/'+session+'.jsonl'));assert len(logs)==1
blocks=[]
for line in logs[0].read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 for b in d.get('message',{}).get('content',[]):
  if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d.get('timestamp'),'messageUuid':d.get('uuid'),'block':b})
assert blocks and not dest.exists();dest.mkdir();rows=[];excluded=[]
for p in sorted(src.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(src)
 disposable=any(x.startswith('scratch') or x in ('verify','work','__pycache__') for x in rel.parts)
 if (disposable and not p.name.startswith('custody-')) or 'copies' in rel.parts:excluded.append(str(rel));continue
 q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size,'origin':'Codex launch prompt/metadata' if p.name in ('prompt.txt','process.json') else 'Verbatim actual Claude independent review output'})
work_delta=[];expected={r['path']:r for r in m['files']}
if (src/'work').is_dir():
 for p in sorted((src/'work').rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts:continue
  rel=str(p.relative_to(src/'work'));digest=sha(p)
  # Review v8 uses work/copy as its exact subject copy, with independent work/runs logs.
  subject_rel=rel[len('copy/'):] if rel.startswith('copy/') else rel
  # v10's p01/p02 harness copies subject/docs to work/copy; retain changed deltas using its actual paths.
  if rel.startswith('copy/') and subject_rel not in expected and 'docs/'+subject_rel in expected:subject_rel='docs/'+subject_rel
  for prefix in ('root/','tamper/','instr/'):
   if rel.startswith(prefix) and rel[len(prefix):] in expected:subject_rel=rel[len(prefix):]
  for prefix,base in (('image-v9/','docs/coop/design-corrections/'),('image-v10/','docs/coop/design-corrections/'),('v9copy/','docs/coop/design-corrections/foundation/')):
   if rel.startswith(prefix) and base+rel[len(prefix):] in expected:subject_rel=base+rel[len(prefix):]
  if subject_rel in expected and digest==expected[subject_rel]['sha256']:continue
  q=dest/'work'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
  work_delta.append({'path':rel,'subjectPath':subject_rel if subject_rel in expected else None,'capturedPath':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
copies_delta=[];copy_bases=[]
if (src/'copies').is_dir():
 copy_roots=[]
 for entry in sorted((src/'copies').iterdir()):
  if not entry.is_dir():continue
  if entry.name in ('discriminate','reach','identity','identity2'):copy_roots.extend(p for p in sorted(entry.iterdir()) if p.is_dir())
  else:copy_roots.append(entry)
 for copy_root in copy_roots:
  version=copy_root.name.removeprefix('subject-')
  base_path=dc/'reviews'/('candidate-subject.'+version+'.json')
  if not base_path.is_file() and (copy_root/'docs/coop/design-corrections/foundation/identity-model.py').is_file():base_path=manifest
  base=json.loads(base_path.read_text()) if base_path.is_file() else None
  base_files={r['path']:r for r in base['files']} if base else {}
  actual_paths={str(p.relative_to(copy_root)) for p in copy_root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
  if base:copy_bases.append({'path':str(copy_root.relative_to(src)),'baseManifestPath':str(base_path.relative_to(root)),'baseManifestSha256':sha(base_path),'removedFromBase':sorted(set(base_files)-actual_paths)})
  for p in sorted(copy_root.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts:continue
   rel=str(p.relative_to(copy_root));digest=sha(p)
   if rel in base_files and digest==base_files[rel]['sha256'] and p.stat().st_size==base_files[rel]['bytes']:continue
   q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
   copies_delta.append({'path':str(p.relative_to(src)),'subjectPath':rel if rel in base_files else None,'capturedPath':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
 # Non-directory independent outputs in copies/ are not assumed to be disposable source images.
 for p in sorted((src/'copies').rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and not any(p.is_relative_to(base) for base in copy_roots):
   q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);copies_delta.append({'path':str(p.relative_to(src)),'capturedPath':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
tools=dest/'tool-calls.json';tools.write_text(json.dumps(blocks,indent=2)+'\n')
verify()
retention_name='codex-retention-custody.json' if (dest/'custody.json').exists() else 'custody.json'
(dest/retention_name).write_text(json.dumps({'standing':'Verbatim actual Claude fresh independent design/reference review; substantive verdict retains its exact scope. No readiness or qualification inferred.','source':str(src),'sessionId':session,'files':rows,'toolBlocks':{'path':'tool-calls.json','sha256':sha(tools),'count':len(blocks),'selection':'Exact tool_use/tool_result blocks from this fresh session; LF-only parsing, no private thinking retained.'},'subjectCustody':{'manifestPath':str(manifest.relative_to(root)),'manifestSha256':a.manifest_sha,'fileCount':len(m['files']),'beforeRetentionVerified':True,'afterRetentionVerified':True,'undeclaredFiles':[]},'disposableWorkDelta':{'baseManifestSha256':a.manifest_sha,'sourceRoot':str(src/'work'),'files':work_delta,'meaning':'Final disposable review-work tree delta over exact frozen subject; unchanged copied sources excluded. Changed sources and independently authored outputs retain original work/ relative paths so review links resolve. Probe sources/tool calls retain intermediate actions.'},'disposableCopiesDelta':{'bases':copy_bases,'files':copies_delta,'meaning':'Observed copies/subject-vN roots are reconstructed from the exact named frozen base manifest plus retained changed/new bytes and removed-path list. Full subject-shaped copies are represented mathematically against the named frozen base, including every actual removed path; this representation does not claim that base was the reviewer original runtime input. Probes retain actual construction/overlays. Unknown copy layouts retained in full. Original reviewer paths preserved.'},'excludedDisposableFiles':excluded},indent=2)+'\n')
print(session,review.get('verdict',review.get('overallVerdict')),len(rows),'output files',len(blocks),'tool blocks','subject files',len(m['files']))
