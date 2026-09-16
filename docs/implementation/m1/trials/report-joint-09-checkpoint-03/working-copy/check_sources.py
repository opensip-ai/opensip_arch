"""Check composed schema syntax and every reference against pinned source bytes.

This does not execute semantic models, admit report fixtures or qualify sources.
"""
from pathlib import Path
import hashlib
import json
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012

HERE=Path(__file__).resolve().parent
subjects=json.loads((HERE/'input-subjects.json').read_text())['subjects']
pins={}
for subject in subjects:
    manifest=Path(subject['manifest']).read_bytes()
    assert hashlib.sha256(manifest).hexdigest()==subject['manifestSha256']
    entries={r['path']:r for r in json.loads(manifest)['files']}
    for name in ['source-pins.json','input-pins.json']:
        if name not in entries:continue
        path=Path(subject['subject'])/name;raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==entries[name]['sha256']
        for row in json.loads(raw).get('files',[]):
            if row['path'] in pins:assert row['sha256']==pins[row['path']]['sha256'],row['path']
            pins[row['path']]=row
schemas={};paths={};duplicates=[]
for row in pins.values():
    if not row['path'].endswith('.json'):continue
    raw=Path(row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
    value=json.loads(raw)
    if not isinstance(value,dict) or not isinstance(value.get('$id'),str) or '$schema' not in value:continue
    uri=value['$id']
    if uri in schemas and value!=schemas[uri]:
        duplicates.append({'uri':uri,'earlier':paths[uri],'other':row['path']})
        continue
    schemas[uri]=value;paths[uri]=row['path']
composition=json.loads((HERE/'composition-result.json').read_text())
overrides=[]
for row in composition['outputs']:
    raw=(HERE/row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
    value=json.loads(raw)
    if value['$id'] in schemas:overrides.append({'uri':value['$id'],'prior':paths[value['$id']],'selected':row['path']})
    schemas[value['$id']]=value;paths[value['$id']]=row['path']
registry=Registry().with_resources((uri,Resource(contents=doc,specification=DRAFT202012)) for uri,doc in schemas.items())
problems=[];references=0


def visit(value,base,path):
    global references
    if isinstance(value,list):
        for i,v in enumerate(value):visit(v,base,path+'/'+str(i))
    elif isinstance(value,dict):
        if isinstance(value.get('$id'),str):base=value['$id']
        if isinstance(value.get('$ref'),str):
            references+=1
            try:registry.resolver(base).lookup(value['$ref'])
            except Exception as exc:problems.append({'schema':base,'path':path,'ref':value['$ref'],'error':type(exc).__name__})
        for k,v in value.items():visit(v,base,path+'/'+k)


for doc in schemas.values():
    Draft202012Validator.check_schema(doc)
    visit(doc,doc['$id'],'')
result={'standing':'Root schema syntax/reference inventory only; not semantic admission or selected source closure',
        'schemaDocuments':len(schemas),'composedDocuments':len(composition['outputs']),'referencesChecked':references,
        'unresolved':problems,'inheritedSameIdDifferentDocuments':duplicates,'explicitComposedOverrides':overrides,
        'schemaSources':[{'uri':uri,'path':paths[uri],'sha256':hashlib.sha256((Path(paths[uri]) if Path(paths[uri]).is_absolute() else HERE/paths[uri]).read_bytes()).hexdigest()} for uri in schemas],
        'passed':not problems and all(any(x['uri']==d['uri'] for x in overrides) for d in duplicates)}
(HERE/'source-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'documents':len(schemas),'references':references,'unresolved':len(problems),'inheritedCollisions':len(duplicates),'passed':result['passed']}))
raise SystemExit(0 if result['passed'] else 1)
