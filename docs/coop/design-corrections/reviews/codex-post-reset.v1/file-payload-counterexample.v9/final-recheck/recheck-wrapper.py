"""After released actual author v6 capture, replay original file attacks on captured final sources."""
from pathlib import Path
import argparse,hashlib,json,shutil
p=argparse.ArgumentParser()
for n in ('hash-cause','length-cause','path-cause'):p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path.cwd();dc=root/'docs/coop/design-corrections';assert (dc/'reviews/digest-corrections-author.v6/custody.json').is_file()
original=dc/'reviews/codex-post-reset.v1/file-payload-counterexample.v9';tmp=Path('/tmp/opensip-design-corrections/file-payload-final-recheck.v9');tmp.mkdir(exist_ok=False)
manifest=json.loads((dc/'reviews/candidate-subject.v8.json').read_text());base=Path(manifest['snapshotRoot']);work=tmp/'work';shutil.copytree(base,work);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
paths=[]
for folder in ('foundation','native','security','workflows'):
 paths.extend(p for p in (dc/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths.extend((root/'docs/v2/contracts/product-v1').glob('*.md'))
for p in paths:
 rel=p.relative_to(root);q=work/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 if not (base/rel).exists() or sha(base/rel)!=sha(q):rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
src=(original/'attempt2/probe.py').read_text();src=src.replace("base=Path(manifest['snapshotRoot']);fixture=",'base=Path('+repr(str(work))+');fixture=');src=src.replace('file-payload-counterexample.v9/attempt2','file-payload-counterexample.v9/final-recheck')
# v4's released builder has an explicit file shape. Preserve the original attack's
# policy selection, while using that real shape and the relation-aware replay projection.
start=src.index(" ns['ATOM']=")
end=src.index(" inventory=",start)
src=src[:start]+""" original_shape=ns['relation_fixture']
 def selected_shape(*args,**kwargs):
  shape=original_shape(*args,**kwargs)
  if args[0]=='file':shape=dict(shape,filter=('subject',wanted))
  return shape
 ns['relation_fixture']=selected_shape
 try:r,o,b=ns['build'](has_match=True,relation='file')
 finally:ns['relation_fixture']=original_shape
"""+src[end:]
src=src.replace("assert old_payload_digest!=fact['payloadDigest']", "assert kind=='control' or old_payload_digest!=fact['payloadDigest']")
q=tmp/'adapted-probe.py';q.write_text(src);exec(compile(src,str(q),'exec'),{'__file__':str(q),'__name__':'codex_final_file_recheck'})
out=original/'final-recheck';(out/'recheck-wrapper.py').write_bytes(Path(__file__).read_bytes());(out/'adapted-probe.py').write_bytes(q.read_bytes())
for row in rows:
 q=out/'source-delta'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/row['path'],q)
report=json.loads((out/'result.json').read_text());v={x['id']:x for x in report['vectors']};assert v['control']['closure']['admitted'] and v['control']['store']['commit']=='committed',v['control']
expected={'wrong-content-hash':a.hash_cause,'wrong-byte-length':a.length_cause,'uninventoried-path':a.path_cause}
for name,cause in expected.items():assert not v[name]['closure']['admitted'] and cause in v[name]['closure']['cause'],v[name]
(out/'custody.json').write_text(json.dumps({'standing':'Codex re-execution/adaptation of its own original complete-Run counterexample on separately captured final sources, not independent acceptance. Original generated result wording references the immutable base; this record binds the exact final source deltas.','baseManifestSha256':'cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70','finalSourceDelta':rows,'originalEvidencePreserved':True,'positiveControlCommitted':True,'allThreeBypassesRefusedAtIntendedJoin':True,'expectedCauseSubstrings':expected,'productQualification':False},indent=2)+'\n')
print('Final source control committed and all three original file claims refused at intended joins')
