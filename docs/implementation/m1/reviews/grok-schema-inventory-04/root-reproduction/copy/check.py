from pathlib import Path
import json,re
D=Path(__file__).resolve().parent
read=lambda n:json.loads((D/n).read_bytes())
a=read('parent.json');b=read('candidate.json');r=read('successor.json')
assert a.keys()==b.keys()
assert all(a[k]==b[k] for k in a if k not in ['standing','files'])
x={v['path']:v for v in a['files']};y={v['path']:v for v in b['files']}
assert len(x)==len(a['files'])==202 and len(y)==len(b['files'])==246
assert list(y)==sorted(y) and all(y[k]==v for k,v in x.items())
added=set(y)-set(x)
expected={v['implementationPath'] for v in read('source-map.json')['sources']}|{v['implementationPath'] for v in read('auxiliary-input-map.json')['inputs']}|{'schemas/source-map.json'}
assert added==expected==set(r['addedFiles']) and len(added)==44
for p in added:
 row=y[p];path=Path(p)
 assert row['package']=='shared-assets' and row['role'] in ['model','registry','configuration']
 assert not row['generated'] and row['standing']=='proposed' and row['description'].strip()
 assert p.startswith('schemas/') and '..' not in path.parts and not path.is_absolute()
 assert re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.schema)?\.json',path.name)
assert r['parentArtifactBytesUnchanged'] and r['inheritedRowsEqualByValue']
print(json.dumps({'passed':True,'inheritedRows':202,'addedRows':44,'packageCount':len(b['packages']),'packagePolicyUnchanged':True,'sourceSelectionApproved':False,'productImplemented':False}))
