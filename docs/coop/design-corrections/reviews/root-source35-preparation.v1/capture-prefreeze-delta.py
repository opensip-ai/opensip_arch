from pathlib import Path
import hashlib,json,argparse
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
mf=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json');sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(mf.read_bytes())=='bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6';m=json.loads(mf.read_bytes());old={r['path']:r for r in m['files']};actual={}
assert not a.out.exists();a.out.mkdir()
for p in a.source.rglob('*'):
 if p.is_file():
  assert not p.is_symlink();b=p.read_bytes();actual[p.relative_to(a.source).as_posix()]={'sha256':sha(b),'bytes':len(b)}
added=sorted(set(actual)-set(old));removed=sorted(set(old)-set(actual));changed=[dict(path=k,beforeSha256=old[k]['sha256'],afterSha256=v['sha256'],beforeBytes=old[k]['bytes'],afterBytes=v['bytes']) for k,v in sorted(actual.items()) if k in old and v['sha256']!=old[k]['sha256']]
record=dict(standing='Complete measured prefreeze delta; no acceptance',parentManifestSha256=sha(mf.read_bytes()),source=str(a.source),fileCount=len(actual),totalBytes=sum(v['bytes'] for v in actual.values()),added=added,removed=removed,changed=changed)
(a.out/'delta.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2));assert not added and not removed
