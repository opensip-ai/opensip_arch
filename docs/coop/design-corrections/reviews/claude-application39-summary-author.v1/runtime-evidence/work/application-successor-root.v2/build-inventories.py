"""Prepare scoped current inventory/classification and generated catalog in a staged package.
No historical manifest is repinned. Run only after the other staged files are complete.
"""
import argparse,json,hashlib,re,posixpath,importlib.util
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--files',type=Path,required=True);p.add_argument('--application-version',required=True);a=p.parse_args();root=a.root.resolve();files=a.files.resolve()
invrel='docs/operations/document-inventory.v1.json';clsrel='docs/operations/document-classification.v1.json'
inv=json.loads((root/invrel).read_text());classification=json.loads((root/clsrel).read_text());rows={r['path']:r for r in inv['files']};classes={r['path']:r['classification'] for r in classification['files']}
def read(rel):return (files/rel) if (files/rel).exists() else root/rel
paths={str(p.relative_to(files)) for p in files.rglob('*') if p.is_file()}
for base in ['docs/coop/design-corrections','docs/coop/architecture-depth-review','docs/coop/fallow-review','docs/coop/unified-design-review','docs/v2/contracts/product-v1']:
 paths.update(str(p.relative_to(root)) for p in (root/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
# Mutable operational guide and later external binding evidence are outside this frozen accounting scope.
exclude={invrel,clsrel,'docs/coop/design-corrections/reviews/NEXT-REVIEW.md','docs/coop/design-corrections/application-activation.v1.json'}
paths={p for p in paths if p not in exclude and not p.startswith('docs/coop/design-corrections/reviews/application-review.'+a.application_version+'/') and p!='docs/coop/design-corrections/reviews/application-subject.'+a.application_version+'.json'}
for rel in sorted(paths):
 data=read(rel).read_bytes();row=dict(rows.get(rel,{'path':rel,'referencedByCount':0,'referencedBy':[]}));row['sha256']=hashlib.sha256(data).hexdigest();row['referenceAccountingScope']='D-372 scoped content refresh; historical inbound-reference samples preserved. currentNavigationReferences is a separate sample from this applied documentation set.';rows[rel]=row
 if rel.startswith('docs/v2/contracts/product-v1/') or rel=='docs/coop/design-corrections/current-source-map.proposed.md':classes[rel]='current/architecture'
 elif rel in ['README.md','docs/START-HERE.md','docs/catalog/README.md','docs/catalog/current-design.md']:classes[rel]='current/navigation'
 elif rel.startswith('docs/v2/architecture/'):classes[rel]='current/architecture'
 elif rel.startswith('docs/operations/') and rel.endswith('.py'):classes[rel]='evidence/units'
 elif rel.startswith('docs/coop/design-corrections/'):classes[rel]='evidence/artifacts'
 elif rel not in classes:classes[rel]='evidence/historical-or-misc'
# Known links from staged current Markdown and the scoped current architecture inputs, without an exhaustive repository rescan.
links={}
for pth in sorted(paths):
 if not pth.endswith('.md') or (not (files/pth).exists() and classes.get(pth) != 'current/architecture'):continue
 for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)\s]+)\)',read(pth).read_text()):
  if ':' in target.split('#')[0]:continue
  target=target.split('#')[0]
  if not target:continue
  dest=posixpath.normpath(posixpath.join(posixpath.dirname(pth),target))
  if dest in rows:links.setdefault(dest,set()).add(pth)
for rel,refs in links.items():rows[rel]['currentNavigationReferences']=sorted(refs)
change={'decision':'D-372','scope':'Exact staged current documents plus correction/design/review evidence existing at application-content freeze. Final independent application review, external activation, application manifest and mutable resume guide are deliberately outside this cutoff and are bound separately by D-372. No exhaustive repository/reference rescan or historical acceptance authentication is claimed.','contentPaths':sorted(paths),'excludedPaths':sorted(exclude),'lateEvidencePrefix':'docs/coop/design-corrections/reviews/application-review.'+a.application_version+'/'}
for data in (inv,classification):
 data.setdefault('workingTreeDeltaHistory',[]).append(data.get('workingTreeDelta',{}));data['workingTreeDelta']=change
inv['generatedFrom']='Original tracked inventory plus explicit D-370/D-371/D-372 scoped current working-tree changes'
def write():
 inv['files']=[rows[k] for k in sorted(rows)];inv['fileCount']=len(rows);inv['pinnedOrMentionedCount']=sum(r.get('referencedByCount',0)>0 for r in rows.values())
 classification['files']=[dict(row,classification=classes.get(row['path'],'evidence/historical-or-misc')) for row in inv['files']];classification['counts']=dict(sorted(Counter(r['classification'] for r in classification['files']).items()))
 for rel,data in [(invrel,inv),(clsrel,classification)]:
  q=files/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(data,indent=2)+'\n')
write()
gen=files/'docs/operations/generate-current-design-catalog.py';spec=importlib.util.spec_from_file_location('catalog_generator',gen);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rel='docs/catalog/current-design.md';q=files/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(module.render(classification));rows[rel]['sha256']=hashlib.sha256(q.read_bytes()).hexdigest();write()
assert q.read_text()==module.render(classification)
print(json.dumps({'scopedContentPaths':len(paths),'inventoryRows':len(rows),'currentArchitectureRows':classification['counts']['current/architecture']}))
