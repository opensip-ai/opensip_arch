from pathlib import Path
import argparse,json,hashlib,difflib
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
B=Path('/tmp/opensip-design-corrections');mf=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json')
raw=mf.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(raw)=='bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6';m=json.loads(raw);old={r['path']:r for r in m['files']};frozen=Path(m['snapshotRoot'])
assert (B/'claude-incoming-binding-author.v1/process-completion.json').is_file(),'Wait for source author completion'
assert not a.out.exists();a.out.mkdir(parents=True)
actual={p.relative_to(a.source).as_posix():p for p in a.source.rglob('*') if p.is_file()};removed=sorted(set(old)-set(actual));added=sorted(set(actual)-set(old));changed=[]
for rel in sorted(set(old)&set(actual)):
 raw=actual[rel].read_bytes();h=sha(raw)
 if h==old[rel]['sha256']:continue
 before=(frozen/rel).read_bytes();assert sha(before)==old[rel]['sha256'];row={'path':rel,'beforeSha256':sha(before),'afterSha256':h,'beforeBytes':len(before),'afterBytes':len(raw)};changed.append(row)
 for prefix,by in [('before',before),('after',raw)]:
  q=a.out/prefix/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(by)
 try:
  diff=''.join(difflib.unified_diff(before.decode().splitlines(True),raw.decode().splitlines(True),fromfile='frozen34/'+rel,tofile='author-successor/'+rel));q=a.out/'diffs'/(rel+'.diff');q.parent.mkdir(parents=True,exist_ok=True);q.write_text(diff)
 except UnicodeDecodeError:pass
owned={'docs/coop/design-corrections/foundation/'+n for n in ['atom-evaluation-contract.v1.md','atom_model.v1.py','check-atoms.v1.py']}
r={'standing':'Measured completed-author source delta before root pin sealing. No design acceptance or freeze. Unexpected changes require explicit review, never deletion or silent exemption.','parentManifestSha256':sha(mf.read_bytes()),'source':str(a.source),'parentFiles':len(old),'actualFiles':len(actual),'changed':changed,'added':added,'removed':removed,'outsideAuthorOwnedPaths':[r['path'] for r in changed if r['path'] not in owned]}
(a.out/'delta.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'changed':len(changed),'added':added,'removed':removed,'outsideAuthorOwnedPaths':r['outsideAuthorOwnedPaths']}))
