from pathlib import Path
import json,hashlib,subprocess,shutil,difflib
B=Path('/tmp/opensip-design-corrections'); O=Path(__file__).parent
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
A=B/'claude-nested-workspace-author.v1'; F=B/'candidate-subject.v39'; T=B/'source39-corrections-successor.v1/source'
H=lambda b:hashlib.sha256(b).hexdigest()
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
mf=L/'candidate-subject.v39.json';assert H(mf.read_bytes())=='f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'
m=json.loads(mf.read_bytes())
for r in m['files']:
 b=(F/r['path']).read_bytes();assert H(b)==r['sha256'] and len(b)==r['bytes'],r['path']
pub=L/A.name/'final-public-artifact-manifest.json';p=json.loads(pub.read_bytes())
for r in p['files']:
 q=pub.parent/r['retainedPath'] if 'retainedPath' in r else F/r['sameAsSubjectPath'];b=q.read_bytes()
 assert H(b)==r['sha256'] and len(b)==r['bytes'],str(q)
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0
assert not json.loads((A/'result.json').read_bytes()).get('is_error')
d=json.loads((A/'deltas/v1/delta-manifest.json').read_bytes());assert len(d['files'])==5
staged=[]
for r in d['files']:
 rel=r['path'];base=(F/rel).read_bytes();theirs=(A/'work/source'/rel).read_bytes();ours=(T/rel).read_bytes()
 assert H(base)==r['before']['sha256'] and H(theirs)==r['after']['sha256']
 for kind,b in [('base',base),('author',theirs),('before',ours)]:save(O/kind/rel,b)
 merge=subprocess.run(['git','merge-file','-p',str(O/'before'/rel),str(O/'base'/rel),str(O/'author'/rel)],capture_output=True)
 save(O/'merge-stderr'/rel,merge.stderr)
 save(O/'merge-raw'/rel,merge.stdout)
 resolution='clean git three-way merge'
 if merge.returncode==0:after=merge.stdout
 else:
  assert merge.returncode>0
  # Resolve only disjoint base-line edits and insertions at the same base boundary.
  # At a shared insertion boundary, preserve the entire root insertion then entire author insertion.
  lines=base.decode().splitlines(True); edits=[]
  for priority,side in enumerate([ours,theirs]):
   changed=side.decode().splitlines(True)
   for tag,i,j,k,l in difflib.SequenceMatcher(None,lines,changed,autojunk=False).get_opcodes():
    if tag!='equal':edits.append((i,j,priority,changed[k:l]))
  cursor=0;out=[]
  for i,j,priority,replacement in sorted(edits,key=lambda e:(e[0],e[1],e[2])):
   assert i>=cursor,('Overlapping substantive edit requires explicit resolution',rel,i,j,cursor)
   out.extend(lines[cursor:i]);out.extend(replacement);cursor=j
  out.extend(lines[cursor:]);after=''.join(out).encode()
  resolution='Disjoint base-line edits with same-boundary insertions preserved root then author; original git conflict retained'
 save(O/'after'/rel,after)
 save(O/'diffs'/(rel+'.diff'),''.join(difflib.unified_diff(ours.decode().splitlines(True),after.decode().splitlines(True),fromfile='before/'+rel,tofile='after/'+rel)).encode())
 staged.append({'path':rel,'beforeSha256':H(ours),'authorSha256':H(theirs),'afterSha256':H(after),'afterBytes':len(after),'merge':resolution})
# Check all before images again immediately before the first mutation.
for r in staged:assert H((T/r['path']).read_bytes())==r['beforeSha256']
for r in staged:(T/r['path']).write_bytes((O/'after'/r['path']).read_bytes())
native=(T/'docs/coop/design-corrections/native/native_evidence_model.v2.py').read_text()
assert 'mode = "js-allowjs" if m[marker].get("allowJs", True) else "ts-tsconfig"' in native
assert '"unitKind": TSJS_UNIT_KIND[mode]' in native
contract=(T/'docs/v2/contracts/product-v1/native-evidence.md').read_text()
assert 'Prerelease document revision and historical standing.' in contract
report={'standing':'Actual Claude nested Cargo author patch merged into mutable successor, preserving prior TS/JS, jsconfig and native history fixes. All original merge output and before images retained. Final pins, full checks and independent successor review pending; no acceptance/readiness.', 'frozen39FilesVerified':len(m['files']),'publicFilesVerified':len(p['files']),'publicManifestSha256':H(pub.read_bytes()),'reviewJsonSha256':H((A/'review.json').read_bytes()),'reviewMdSha256':H((A/'review.md').read_bytes()),'patchSha256':H((A/'deltas/v1/correction.patch').read_bytes()),'changes':staged}
save(O/'integration.json',(json.dumps(report,indent=2)+'\n').encode());shutil.copytree(O,L/O.name);print(json.dumps(report))
