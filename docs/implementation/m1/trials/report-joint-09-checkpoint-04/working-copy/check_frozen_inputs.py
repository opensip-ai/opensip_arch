"""Verify every frozen input member and declared external source pin."""
from pathlib import Path,PurePosixPath
import hashlib,json
HERE=Path(__file__).resolve().parent
inputs=json.loads((HERE/'input-subjects.json').read_bytes())['subjects']
external={};subjects=[]
def verify(path,row):
 raw=path.read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],str(path)
 return raw
for unit in inputs:
 manifest=Path(unit['manifest']).read_bytes();assert hashlib.sha256(manifest).hexdigest()==unit['manifestSha256']
 files=json.loads(manifest)['files'];assert len(files)==unit['entries']
 names=set()
 for row in files:
  rel=PurePosixPath(row['path']);assert not rel.is_absolute() and '..' not in rel.parts and str(rel)==row['path']
  assert row['path'] not in names;names.add(row['path'])
  raw=verify(Path(unit['subject'])/row['path'],row)
  if row['path'] in ['input-pins.json','source-pins.json']:
   for pin in json.loads(raw)['files']:
    if pin['path'] in external:assert (pin['sha256'],pin['bytes'])==(external[pin['path']]['sha256'],external[pin['path']]['bytes'])
    external[pin['path']]=pin
 subjects.append({'unit':unit['unit'],'members':len(files),'manifestSha256':unit['manifestSha256']})
for name in ['workflow-input-pins.json','supplemental-inputs.json']:
 for pin in json.loads((HERE/name).read_bytes())['files']:
  if pin['path'] in external:assert pin['sha256']==external[pin['path']]['sha256']
  external[pin['path']]=pin
for path,row in external.items():
 verify(Path(path),row)
 if 'subjectManifest' in row:
  manifest=Path(row['subjectManifest']);raw=manifest.read_bytes();assert hashlib.sha256(raw).hexdigest()==row['subjectManifestSha256']
  relative=str(Path(path).relative_to(manifest.with_suffix('')))
  member=next(r for r in json.loads(raw)['files'] if r['path']==relative)
  assert member['bytes']==row['bytes'] and member['sha256']==row['sha256']
# The local comparison snapshot is an exact copy, never a rewritten predecessor.
report=next(r for r in inputs if r['unit']=='report-projection')
for row in json.loads(Path(report['manifest']).read_bytes())['files']:verify(HERE/'parent-report08'/row['path'],row)
result={'standing':'Root frozen-byte integrity only; neither approval nor complete dynamic read closure','subjects':subjects,'members':sum(r['members'] for r in subjects),'externalSources':len(external),'externalFiles':[{'path':p,'sha256':r['sha256'],'bytes':r['bytes']} for p,r in sorted(external.items())],'parentSnapshotMembers':report['entries'],'passed':True}
(HERE/'frozen-input-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['members','externalSources','parentSnapshotMembers','passed']}))
