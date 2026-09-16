from pathlib import Path
import json,hashlib,difflib,shutil
B=Path('/tmp/opensip-design-corrections');prev=B/'dependency-scope-successor.v1/source';cur=B/'dependency-totality-successor.v1/source';out=B/'root-dependency-totality-author-only-delta.v1';assert not out.exists()
a=B/'claude-dependency-totality-author.v1';assert json.loads((a/'process-completion.json').read_bytes())['exitCode']==0
combined=json.loads((B/'root-dependency-totality-combined35-delta.v1/delta.json').read_bytes());assert not combined['added'] and not combined['removed'] and not combined['outsideAuthorOwnedPaths']
old=json.loads((B/'root-dependency-scope-author-delta.v1/delta.json').read_bytes());rows=[];out.mkdir()
for r in old['changed']:
 rel=r['path'];before=(prev/rel).read_bytes();after=(cur/rel).read_bytes();assert hashlib.sha256(before).hexdigest()==r['afterSha256']
 for kind,raw in [('before',before),('after',after)]:
  p=out/kind/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 p=out/'diffs'/(rel+'.diff');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='completed95/'+rel,tofile='totality-author/'+rel)))
 rows.append({'path':rel,'beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':hashlib.sha256(after).hexdigest(),'changed':before!=after})
(out/'delta.json').write_text(json.dumps({'standing':'Completed actual totality-author-only delta against exact95case predecessor. Combined35 outside-path scan separately verified; no root prose/pins yet.','files':rows},indent=2)+'\n');shutil.copytree(out,Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/out.name);print('Captured final totality-author-only delta',len(rows))
