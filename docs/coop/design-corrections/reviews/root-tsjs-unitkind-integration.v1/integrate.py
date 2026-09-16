from pathlib import Path
import json,hashlib,subprocess,shutil,difflib
B=Path('/tmp/opensip-design-corrections'); O=Path(__file__).parent
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
A=B/'claude-tsjs-unitkind-author.v1'; F=B/'candidate-subject.v39'; T=B/'source39-corrections-successor.v1/source'
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
d=json.loads((A/'delta-manifest.json').read_bytes());assert len(d['changedFiles'])==5
staged=[]
for r in d['changedFiles']:
 rel=r['path'];base=(F/rel).read_bytes();theirs=(A/'work/source'/rel).read_bytes();ours=(T/rel).read_bytes()
 assert H(base)==r['before']['sha256'] and H(theirs)==r['after']['sha256']
 for kind,b in [('base',base),('author',theirs),('before',ours)]:save(O/kind/rel,b)
 merge=subprocess.run(['git','merge-file','-p',str(O/'before'/rel),str(O/'base'/rel),str(O/'author'/rel)],capture_output=True)
 save(O/'merge-stderr'/rel,merge.stderr);assert merge.returncode==0,(rel,merge.returncode,merge.stdout.decode())
 after=merge.stdout;save(O/'after'/rel,after)
 save(O/'diffs'/(rel+'.diff'),''.join(difflib.unified_diff(ours.decode().splitlines(True),after.decode().splitlines(True),fromfile='before/'+rel,tofile='after/'+rel)).encode())
 staged.append({'path':rel,'beforeSha256':H(ours),'authorSha256':H(theirs),'afterSha256':H(after),'afterBytes':len(after),'threeWayClean':True})
# Check all before images again immediately before the first mutation.
for r in staged:assert H((T/r['path']).read_bytes())==r['beforeSha256']
for r in staged:(T/r['path']).write_bytes((O/'after'/r['path']).read_bytes())
native=(T/'docs/coop/design-corrections/native/native_evidence_model.v2.py').read_text()
assert 'mode = "js-allowjs" if m[marker].get("allowJs", True) else "ts-tsconfig"' in native
assert '"unitKind": TSJS_UNIT_KIND[mode]' in native
contract=(T/'docs/v2/contracts/product-v1/native-evidence.md').read_text()
assert 'Prerelease document revision and historical standing.' in contract
report={'standing':'Bounded actual Claude author patch integrated with clean three-way merges into mutable successor. All root jsconfig and native history edits preserved. Final pins, full integration checks and independent frozen successor review pending; no acceptance/readiness.', 'frozen39FilesVerified':len(m['files']),'publicFilesVerified':len(p['files']),'publicManifestSha256':H(pub.read_bytes()),'reviewJsonSha256':H((A/'review.json').read_bytes()),'reviewMdSha256':H((A/'review.md').read_bytes()),'patchSha256':H((A/'correction.patch').read_bytes()),'changes':staged}
save(O/'integration.json',(json.dumps(report,indent=2)+'\n').encode());shutil.copytree(O,L/O.name);print(json.dumps(report))
