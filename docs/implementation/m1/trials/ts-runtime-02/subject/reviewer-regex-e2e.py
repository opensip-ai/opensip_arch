import json,importlib.util
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('meta',root/'docs/implementation/m1/metadata-v2/check_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ref,registry,docs=m.load(root)
cr,ls,lf=chr(13),chr(0x2028),chr(10)
out={}
for s in ['a/../x','a'+cr+'/../../etc/passwd','a'+ls+'/../../x','..'+lf,'a/..'+lf,'ok/path']:
  for r in ['urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CanonicalPath','urn:opensip:product-v1:workflows:common#/$defs/LogicalPath','urn:opensip:product-v1:identity:v3#/$defs/LogicalPath']:
    out[r.split(':')[-1]+' '+json.dumps(s,ensure_ascii=False)]=ref.ExactValidator({'$ref':r},registry=registry).is_valid(s)
print(json.dumps(out,indent=1))
ts=json.load(open('regex-e2e-ts.json')); print('e2e diffs',[k for k in out if ts.get(k)!=out[k]])
for i,d in docs.items():
  def w(v,p):
    if isinstance(v,dict):
      if 'patternProperties' in v: print('patternProperties at',i+'#'+p,list(v['patternProperties']))
      for k,x in v.items(): w(x,p+'/'+k)
  w(d,'')
