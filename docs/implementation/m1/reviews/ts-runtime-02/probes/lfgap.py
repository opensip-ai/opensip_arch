import json,importlib.util
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('meta',root/'docs/implementation/m1/metadata-v2/check_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ref,registry,docs=m.load(root)
refs=['urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CanonicalPath','urn:opensip:product-v1:workflows:common#/$defs/LogicalPath','urn:opensip:product-v1:identity:v3#/$defs/LogicalPath','opensip.product.occupancy-companion.1#/$defs/LogicalPath']
vals=['a'+chr(10)+'/../../etc/passwd','a'+chr(10)+'/..','x'+chr(10)+'..'+chr(10)+'/y','a/..'+chr(10)+chr(10),'a'+chr(13)+chr(10)+'/../x','..','a/./b']
out=[[r,v,ref.ExactValidator({'$ref':r},registry=registry).is_valid(v)] for r in refs for v in vals]
json.dump(out,open('lfgap-py.json','w'))
print(json.dumps(out,ensure_ascii=True))
