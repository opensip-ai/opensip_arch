"""Prospective application pin delta; never alter accepted source or live files."""
from pathlib import Path
import hashlib,json
DC='docs/coop/design-corrections/'
DOCS={
 'docs/v2/architecture/03-configuration-and-security.md',
 'docs/v2/architecture/10-mvp-and-future-scope.md',
 'docs/v2/architecture/13-evidence-workflows-and-product-contracts.md',
}
BASE_PINS=[DC+'foundation/source-pins.v1.json',DC+'security/source-pins.v1.json',DC+'native/source-pins.v2.json',DC+'workflows/source-pins.v1.json']
CURRENT_PIN=DC+'foundation/evaluator3-source-pins.v1.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def prepare(snapshot,files):
 snapshot,files=Path(snapshot),Path(files)
 changed={str(p.relative_to(files)) for p in files.rglob('*') if p.is_file() and (not (snapshot/p.relative_to(files)).is_file() or sha(p)!=sha(snapshot/p.relative_to(files)))}
 # A pinned architecture chapter may only gain its separately reviewed opening
 # applicability paragraph. No removal or alteration of the inherited body.
 doc_deltas=[]
 for rel in sorted(DOCS):
  before=(snapshot/rel).read_text();after=(files/rel).read_text()
  first,tail=before.split('\n',1);assert after.startswith(first+'\n\n'),rel
  assert after.endswith(tail), 'Inherited architecture body changed: '+rel
  addition=after[len(first)+1:len(after)-len(tail)]
  assert addition.strip() and '\n\n' not in addition.strip(), 'Expected one opening applicability paragraph: '+rel
  assert 'D-372' in addition and ('application' in addition or 'contracts' in addition),rel
  doc_deltas.append({'path':rel,'beforeSha256':sha(snapshot/rel),'afterSha256':sha(files/rel),'addedOpeningParagraph':addition})
 manifests=[];intersections=[]
 for rel in BASE_PINS+[CURRENT_PIN]:
  original=json.loads((snapshot/rel).read_text());key='files' if 'files' in original else 'pins';rows=original[key]
  assert len({r['path'] for r in rows})==len(rows)
  expected=DOCS if rel in BASE_PINS else DOCS|set(BASE_PINS)
  actual={r['path'] for r in rows if r['path'] in changed}
  assert actual==expected, {'manifest':rel,'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)}
  deltas=[]
  for row in rows:
   path=row['path'];assert sha(snapshot/path)==row['sha256'], 'Accepted pin drift: '+path
   if path in expected:
    old=row['sha256'];row['sha256']=sha(files/path)
    deltas.append({'path':path,'beforeSha256':old,'afterSha256':row['sha256']})
    intersections.append({'manifest':rel,'path':path})
  target=files/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(original,indent=2)+'\n');changed.add(rel)
  manifests.append({'path':rel,'beforeSha256':sha(snapshot/rel),'afterSha256':sha(target),'entries':deltas})
 return {'standing':'Prospective application-only recording successor; accepted source and live tree untouched. All pinned semantic bytes remain accepted bytes.','sourceChanges':doc_deltas,'pinManifests':manifests,'intersections':intersections,'productContractModelSchemaChanges':False}
