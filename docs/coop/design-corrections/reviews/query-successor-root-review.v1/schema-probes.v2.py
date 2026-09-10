"""Root schema-only probes against the in-progress query successor. No graph admission claim."""
from pathlib import Path
import copy,hashlib,importlib.util,json
ROOT=Path('/tmp/opensip-design-corrections/query-successor.v1')
W=ROOT/'docs/coop/design-corrections/workflows'
spec=importlib.util.spec_from_file_location('query_root_workflow',W/'workflow_projection_model.v3.py')
P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
qpath=W/'schemas/evaluator3/graph-query.schema.json';raw=qpath.read_bytes();schema=json.loads(raw);U=schema['$id'];rows=[]
def probe(name,selector,value,want):
 try:P.validate_profile(U+'#/$defs/'+selector,value);actual=True;error=None
 except Exception as exc:actual=False;error=type(exc).__name__+': '+str(exc).splitlines()[0]
 rows.append({'id':name,'admitted':actual,'expectedAdmission':want,'passed':actual==want,'error':error})
common=json.loads((W/'schemas/evaluator3/common.schema.json').read_text())
pattern=common['$defs']['ProjectId']['pattern']
assert pattern == r"^prj1-[0-9a-f]{64}(?![\s\S])"
prj='prj1-'+('a'*64)
endpoint={'universe':'b'*64,'kind':'symbol','nativeSubjectId':'src/a.ts#caller'}
base={'schemaFamily':'opensip.product.query','schemaMajor':3,'projectId':prj,'view':{'runId':'run3:'+('c'*64)},'operation':'graph.neighbors','params':{'relation':'calls','minResolution':'resolved-callee','direction':'outgoing','endpoint':endpoint},'completeness':'required','page':{'size':1}}
probe('closed-neighbors-request','GraphQueryRequestV1',base,True)
for name,mut in [('missing-endpoint',lambda x:x['params'].pop('endpoint')),('unrelated-baseline-param',lambda x:x['params'].update(baselineId='baseline2:'+('d'*64))),('path-only-endpoint',lambda x:x['params'].update(endpoint='src/a.ts')),('unsupported-query-major',lambda x:x.update(schemaMajor=2))]:
 x=copy.deepcopy(base);mut(x);probe(name,'GraphQueryRequestV1',x,False)
for op in schema['$defs']['Operation']['enum']:
 if op.startswith('graph.'):continue
 x=copy.deepcopy(base);x['operation']=op;x['params']={};probe('non-graph-retained-params:'+op,'GraphQueryRequestV1',x,True)
context={'projectId':prj,'resolvedView':base['view'],'factViewDigests':[],'availability':'retained','truncated':False,'totalItems':0,'countBasis':'exact','traversalCoverage':'complete','visitedNodes':0,'producedItems':0,'advisory':False,'evidence':{'coverageIds':[],'scopeIds':[],'deficiencyCitations':[],'resolutionLimitations':[]}}
probe('concrete-graph-context','GraphOperationResponseContext',context,True)
for name,mut in [('unresolved-latest-response',lambda x:x.update(resolvedView={'latest':True})),('graph-advisory-true',lambda x:x.update(advisory=True)),('missing-evidence-disclosure',lambda x:x.pop('evidence')),('missing-count-basis',lambda x:x.pop('countBasis'))]:
 x=copy.deepcopy(context);mut(x);probe(name,'GraphOperationResponseContext',x,False)
assert qpath.read_bytes()==raw,'Schema changed during probe run'
report={'standing':'Schema-only root probes of in-progress exact bytes; no complete Run/traversal/evidence admission or independent acceptance','schemaSha256':hashlib.sha256(raw).hexdigest(),'projectIdPattern':pattern,'checks':rows,'passed':all(x['passed'] for x in rows)}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'checks':len(rows),'failures':[r for r in rows if not r['passed']]}));raise SystemExit(not report['passed'])
