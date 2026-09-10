"""Read-only polling of public blind output files; preserve observed intermediate versions.
Observed file bytes are not necessarily final files or successful executed programs. Never feeds
anything into the blind kit/output and never reads private reasoning/session-log content.
"""
from pathlib import Path
import datetime,time,json,hashlib
src=Path('/tmp/opensip-design-corrections/consumer-b.v7/output');dest=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/blind-v7-observed-versions.v1');dest.mkdir(exist_ok=False);(dest/'blobs').mkdir();entries=[];seen=set();deadline=time.monotonic()+6*3600
while time.monotonic()<deadline:
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for p in sorted(src.rglob('*')):
  if p.is_symlink() or not p.is_file() or p.suffix not in ('.py','.json','.md') or '__pycache__' in p.parts:continue
  try:bb=p.read_bytes()
  except FileNotFoundError:continue
  if not bb:continue
  digest=hashlib.sha256(bb).hexdigest();rel=str(p.relative_to(src));key=(rel,digest)
  if key in seen:continue
  seen.add(key);q=dest/'blobs'/digest
  if not q.exists():q.write_bytes(bb)
  entries.append({'path':rel,'sha256':digest,'bytes':len(bb),'observedAt':now})
 (dest/'observations.json').write_text(json.dumps({'standing':__doc__,'source':str(src),'observations':entries},indent=2)+'\n')
 try:response=json.loads((src/'response.json').read_text())
 except (FileNotFoundError,json.JSONDecodeError):response=None
 if response and 'is_error' in response:
  (dest/'finished.json').write_text(json.dumps({'finishedAt':now,'reason':'Actual CLI receipt completed','sessionId':response.get('session_id'),'isError':response['is_error'],'versions':len(entries)},indent=2)+'\n');break
 time.sleep(10)
else:(dest/'finished.json').write_text(json.dumps({'reason':'Six-hour observation deadline','versions':len(entries)},indent=2)+'\n')
