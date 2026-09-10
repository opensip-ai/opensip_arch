"""Mechanical audit coverage; no semantic completeness or independent acceptance claim."""
import argparse, hashlib, json, re
from pathlib import Path
from jsonschema import Draft202012Validator
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=a.source; d=root/'docs/coop/design-corrections'; product=root/'docs/v2/contracts/product-v1'
prose=sorted(product.glob('*.md'))+sorted((d/'foundation').glob('*contract*.md'))+sorted((d/'workflows').glob('*contract*.md'))
links=[];missing=[];rows=[]
for f in prose:
 b=f.read_bytes();s=b.decode();rows.append({'path':str(f.relative_to(root)),'sha256':hashlib.sha256(b).hexdigest(),'lines':len(s.splitlines())})
 for ref in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',s):
  if ref.startswith(('http:','https:','#','mailto:')):continue
  target=(f.parent/ref.split('#')[0]).resolve();r={'source':str(f.relative_to(root)),'reference':ref,'exists':target.exists()};links.append(r)
  if not r['exists']:missing.append(r)
schemas=sorted(set(d.glob('foundation/*schema*.json'))|set(d.glob('native/*schema*.json'))|set(d.glob('security/*schema*.json'))|set(d.glob('workflows/schemas/**/*.json')))
checked=[];errors=[]
for f in schemas:
 try:
  doc=json.loads(f.read_text());Draft202012Validator.check_schema(doc)
  checked.append({'path':str(f.relative_to(root)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 except Exception as e:errors.append({'path':str(f.relative_to(root)),'error':str(e)[:500]})
result={'standing':'AUTHOR mechanical scan; includes retained schema profiles, not evidence of semantic correctness or selected-major equivalence','prose':rows,'linksChecked':len(links),'missingLinks':missing,'schemasChecked':checked,'schemaErrors':errors}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'proseFiles':len(rows),'links':len(links),'missing':missing,'schemaFiles':len(checked),'schemaErrors':errors}))
