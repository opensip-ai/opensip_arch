from pathlib import Path
import json, hashlib, copy
W=Path('/Users/sb/code/opensip-ai/opensip-native-public')
D=Path('/tmp/opensip-implementation/native-publication-r1')
PRE='docs/implementation/m3/native-publication/native-common-materialization-r1'
changed={f'schemas/sources/common-v{v}.schema.json' for v in (1,3,4)}|{'schemas/sources/native-v2.schema.json'}
def write(p,j):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(j,indent=2)+'\n')
j=json.loads((W/'schemas/admission-registry.json').read_bytes());before=copy.deepcopy(j);rows=[]
for group in ('sources','aliases'):
    for row in j[group]:
        if row['sourcePath'] not in changed:continue
        raw=(W/row['sourcePath']).read_bytes()
        row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());rows.append({'group':group,**row})
for group in ('sources','aliases'):
    assert len(j[group])==len(before[group])
    for a,b in zip(before[group],j[group]):
        assert {k:v for k,v in a.items() if k not in ('bytes','sha256')}=={k:v for k,v in b.items() if k not in ('bytes','sha256')}
        if a['sourcePath'] not in changed:assert a==b
assert {r['sourcePath'] for r in rows}==changed
write(W/'schemas/admission-registry.json',j)
rel=PRE+'/admission-registry.json';raw=(W/'schemas/admission-registry.json').read_bytes()
(D/'architecture'/rel).write_bytes(raw)
m=json.loads((W/'schemas/admission-source-map.json').read_bytes())
m['registryArchitectureSource']={'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
write(W/'schemas/admission-source-map.json',m)
write(D/'admission-repin.json',{'changedRows':rows,'sourcesAndAliasesOtherwiseEqualByValue':True,'registryArchitectureSource':m['registryArchitectureSource']})
print('Re-pinned',len(rows),'admission source/alias rows; inherited values unchanged.')
