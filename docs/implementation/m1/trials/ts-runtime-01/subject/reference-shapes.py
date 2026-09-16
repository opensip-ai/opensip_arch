from pathlib import Path
import json,importlib.util
root=Path('/Users/sb/code/opensip-ai/opensip_arch');here=Path(__file__).parent
path=root/'docs/implementation/m1/metadata-v2/check_metadata.py';spec=importlib.util.spec_from_file_location('meta',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);reference,registry,documents=module.load(root)
refs=list(json.loads(Path('/tmp/opensip-implementation/m1-full-generator-trial-01/source-map.json').read_bytes())['selectedTargets'])
values=[None,True,False,0,1,-1,2**64-1,-2**63,'','x','closure2:'+'a'*64,[],[0],[{},{}],{},dict(schemaVersion=1),dict(kind='symbol'),dict(name='x'),dict(class_='success')]
rows=[]
for ref in refs:
 validator=reference.ExactValidator({'$ref':ref},registry=registry)
 for i,value in enumerate(values):
  rows.append(dict(ref=ref,valueIndex=i,valid=validator.is_valid(value)))
(here/'reference-shapes.json').write_text(json.dumps(dict(values=values,cases=rows),indent=2)+'\n');print(len(rows),'shape cases')
