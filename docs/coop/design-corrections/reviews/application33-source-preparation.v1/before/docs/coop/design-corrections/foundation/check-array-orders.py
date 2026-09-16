"""Cross-schema collection admission checks; reference evidence, not product qualification."""
from pathlib import Path
import argparse, copy, importlib.util, json
HERE=Path(__file__).resolve().parent; DC=HERE.parent
spec=importlib.util.spec_from_file_location('array_canonical',HERE/'canonical.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
rows=[]
def check(name,ok):
    rows.append({'id':name,'passed':bool(ok)})
def admitted(schema,value):
    try:C.validate(schema,value);return True
    except Exception:return False
def arrays(node,path=''):
    if isinstance(node,dict):
        t=node.get('type')
        if t=='array' or isinstance(t,list) and 'array' in t:yield path,node
        for key,value in node.items():yield from arrays(value,path+'/'+key)
    elif isinstance(node,list):
        for i,value in enumerate(node):yield from arrays(value,path+'/'+str(i))

files=[*sorted(p for p in HERE.glob('*.json') if 'schema' in p.name),DC/'native/native-evidence.schemas.v2.json',DC/'security/security-lifecycle.schemas.v1.json',*sorted((DC/'workflows/schemas').glob('*.json'))]
coverage=[]
for path in files:
    found=list(arrays(json.loads(path.read_text())))
    missing=[pointer for pointer,node in found if 'x-opensip-order' not in node]
    invalid=[pointer for pointer,node in found if 'x-opensip-order' in node and not admitted({'type':'array','x-opensip-order':node['x-opensip-order']},[])]
    rel=str(path.relative_to(DC));check(rel+':all-array-laws-declared',not missing);check(rel+':all-annotations-recognized',not invalid)
    coverage.append({'path':rel,'arrays':len(found),'missing':missing,'invalid':invalid})

# Raw UTF-8 order and canonical JSON order differ for escaped characters.
raw_order=['\n','!'];json_order=['!','\n']
utf8={'type':'array','items':{'type':'string'},'x-opensip-order':'utf8'}
canon=dict(utf8,**{'x-opensip-order':'canonical-set'})
check('utf8-positive-distinguishes-json-escaping',admitted(utf8,raw_order) and not admitted(utf8,json_order))
check('canonical-set-positive-distinguishes-raw-utf8',admitted(canon,json_order) and not admitted(canon,raw_order))
canonical_order=dict(canon,**{'x-opensip-order':'canonical-order'})
check('canonical-order-retains-observed-duplicates',admitted(canonical_order,['a','a','b']) and not admitted(canonical_order,['b','a','a']) and not admitted(canon,['a','a','b']))
check('utf8-duplicate-refuses',not admitted(utf8,['a','a']))
by={'type':'array','x-opensip-order':{'by':['name']}}
records=[{'a':'z','name':'a'},{'a':'a','name':'z'}]
check('field-order-is-not-canonical-object-order',admitted(by,records) and not admitted(by,list(reversed(records))))
check('field-order-duplicate-key-different-payload-refuses',not admitted(by,[{'name':'a','payload':1},{'name':'a','payload':2}]))
pair={'type':'array','x-opensip-order':{'by':['name','version']}}
check('tuple-order-uses-secondary-field',admitted(pair,[{'name':'a','version':'1'},{'name':'a','version':'2'}]) and not admitted(pair,[{'name':'a','version':'2'},{'name':'a','version':'1'}]))
check('field-order-missing-or-nontext-key-refuses',not admitted(by,[{}]) and not admitted(by,[{'name':1}]))
for i,order in enumerate([{'by':[]},{'by':['name','name']},{'by':['name'],'descending':True},{'by':'name'},'guessed-order']):
    check('invalid-order-definition-'+str(i),not admitted({'type':'array','x-opensip-order':order},[]))
tokens=['x','(',')','x'];seq={'type':'array','x-opensip-order':'sequence'}
check('ordered-repeated-tokens-retained',admitted(seq,tokens) and C.canonical(tokens)!=C.canonical(list(reversed(tokens))))

# Exercise actual native host admission, including its stable refusal projection.
spec=importlib.util.spec_from_file_location('array_native',DC/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
fixtures=json.loads((DC/'native/native-cases.v2.json').read_text())['fixtures'];ctx=fixtures['tsNativeContext'];trees=fixtures['tsClosureTrees']
check('native-context-valid-original-admits',not N.admit_native_context('typescript',ctx,trees)['refusals'])
for field,subject in [('libSelection','lib-selection-order'),('standardLibraryComponentDigests','stdlib-component-order')]:
    bad=copy.deepcopy(ctx);bad['toolchain'][field].reverse();result=N.admit_native_context('typescript',bad,trees)
    check('native-context-reversed-'+field,'native.native-context-field-mismatch:'+subject in result['refusals'])
    bad=copy.deepcopy(ctx);bad['toolchain'][field].append(copy.deepcopy(bad['toolchain'][field][0]));result=N.admit_native_context('typescript',bad,trees)
    check('native-context-duplicate-'+field,bool(result['refusals']))
bad=copy.deepcopy(ctx);bad['configProjection']['configGraphPaths'].reverse()
check('native-context-config-graph-order-refuses',bool(N.admit_native_context('typescript',bad,trees)['refusals']))

# Selected custom config names and repeated extends are ordinary configuration shapes.
graph={'schemaVersion':1,'entryConfigPath':'tsconfig.build.json','nodes':[
 {'path':'a.json','contentSha256':'a'*64,'kind':'other','extendsResolved':[]},
 {'path':'b.json','contentSha256':'b'*64,'kind':'other','extendsResolved':[]},
 {'path':'tsconfig.build.json','contentSha256':'c'*64,'kind':'other','extendsResolved':['a.json','b.json','a.json']}]}
check('config-custom-entry-and-repeated-edges-admit',N.typescript_config_origin(graph)=='tsconfig' and not N.typescript_config_graph_faults(graph) and bool(N.typescript_config_graph_digest(graph)))
changed=copy.deepcopy(graph);changed['nodes'][-1]['extendsResolved']=['a.json','b.json']
check('config-repeated-edge-affects-identity',N.typescript_config_graph_digest(graph)!=N.typescript_config_graph_digest(changed))
changed['nodes'][-1]['extendsResolved']=['b.json','a.json','a.json']
check('config-base-precedence-affects-identity',N.typescript_config_graph_digest(graph)!=N.typescript_config_graph_digest(changed))

p=argparse.ArgumentParser();p.add_argument('--report',required=True);a=p.parse_args()
result={'passed':all(r['passed'] for r in rows),'checks':rows,'coverage':coverage,'productQualification':False}
Path(a.report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(rows),'passed':sum(r['passed'] for r in rows),'failed':[r['id'] for r in rows if not r['passed']]}));raise SystemExit(not result['passed'])
