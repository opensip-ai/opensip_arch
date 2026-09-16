import json,importlib.util
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('meta',root/'docs/implementation/m1/metadata-v2/check_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ref,registry,docs=m.load(root)
fx=ref.parse((root/'docs/implementation/m1/metadata-v2/fixtures.json').read_bytes())
eid='urn:opensip:product-v1:workflows:evaluator3:command-envelope:4'
v=ref.ExactValidator({'$ref':eid},registry=registry)
out=[dict(id=c['id'],shape=v.is_valid(c['value'])) for c in fx['cases']]
Path('meta43-py.json').write_text(json.dumps(out))
# v1 adapter comparison
spec1=importlib.util.spec_from_file_location('meta1',root/'docs/implementation/m1/metadata-v1/check_metadata.py');m1=importlib.util.module_from_spec(spec1);spec1.loader.exec_module(m1)
try:
    r1,reg1,_=m1.load(root); v1=r1.ExactValidator({'$ref':eid},registry=reg1)
    print('v1 diffs',[c['id'] for c,o in zip(fx['cases'],out) if v1.is_valid(c['value'])!=o['shape']])
except Exception as e: print('v1 load',type(e).__name__,e)
print(len(out))
