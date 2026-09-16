"""Re-execute pinned parent fixture constructions with new query/envelope producers.

This constructs synthetic fixtures; it is not migration/relabeling of retained
query responses, a native query executor or proof of Run custody.
"""
from pathlib import Path
import ast,copy,hashlib,json,types


def build(read_unit,model,schema):
    source=read_unit('report-projection','build_owner.py')
    constants={}
    for n in ast.parse(source).body:
        if isinstance(n,ast.Assign):
            for target in n.targets:
                if isinstance(target,ast.Name) and target.id in ['PROVENANCE','PANELS','ROOT_KEYS']:constants[target.id]=ast.literal_eval(n.value)
    assert set(constants)=={'PROVENANCE','PANELS','ROOT_KEYS'}
    constants['PROVENANCE']['document']=copy.deepcopy(schema['properties']['documentProvenance']['const'])
    budget={k:copy.deepcopy(v['const']) for k,v in schema['$defs']['BudgetProfileV1']['properties'].items()}
    owner=types.SimpleNamespace(**constants,budget=lambda:copy.deepcopy(budget))
    pins=json.loads(read_unit('report-projection','source-pins.json'))['files']
    row=next(r for r in pins if r['path']=='/tmp/opensip-implementation/m1-schema-witnesses-01/witnesses.json')
    raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    fixed=types.SimpleNamespace(read_bytes=lambda:raw)
    source=read_unit('report-projection','build_fixtures.py').decode()
    names={'h','pick','material','finding','resolution_for','exploration_budget','build_context'}
    nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    # New envelope7 is emitted from the same construction site. This is not
    # a generic old-envelope input adapter; seed material remains historical.
    for n in nodes:
        if n.name=='build_context':
            for item in ast.walk(n):
                if isinstance(item,ast.Dict):
                    keys=[k.value if isinstance(k,ast.Constant) else None for k in item.keys]
                    if 'schemaFamily' in keys and 'schemaMajor' in keys:
                        i=keys.index('schemaMajor');assert item.values[i].value==6;item.values[i]=ast.Constant(7)
    tree=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
    ns={'M':model,'OWNER':owner,'copy':copy,'hashlib':hashlib,'json':json,'WITNESSES':fixed,
        'ENV':'urn:opensip:product-v1:workflows:evaluator3:command-envelope:4','canonical':model.canonical,
        'AVAILABILITY':{'stepCount':0,'totalNoticeCount':0,'steps':[]}}
    exec(compile(tree,'pinned-report08-fixture-functions#query4-envelope7','exec'),ns)
    material=ns['material']();context=ns['build_context'](material)
    return context,material
