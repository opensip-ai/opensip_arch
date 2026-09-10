"""Schema probes only: no graph engine, sealed Run, or product implementation.

These demonstrate admitted wire shapes, not that an authoritative query owner
accepts the corresponding semantics. Synthetic IDs are grammar-valid labels.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v25')
WF = ROOT / 'docs/coop/design-corrections/workflows/schemas'
sys.path.insert(0, str(ROOT / 'docs/coop/design-corrections/foundation'))
import canonical

docs = [json.loads(p.read_text()) for p in sorted((WF / 'evaluator3').glob('*.schema.json'))]
docs += [json.loads((WF / n).read_text()) for n in ['common.schema.json', 'imported-evidence.schema.json', 'policy-document.schema.json', 'policy-document.v2.schema.json', 'test-execution.schema.json']]
reg = Registry().with_resources((d['$id'], Resource(contents=d, specification=DRAFT202012)) for d in docs)
base = 'urn:opensip:product-v1:workflows:evaluator3:graph-query:3'
def admitted(selector, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': base + '#/$defs/' + selector}, registry=reg).validate(value)
        return {'schemaAdmitted': True}
    except Exception as exc:
        return {'schemaAdmitted': False, 'error': str(exc).splitlines()[0]}

q = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
     'projectId': 'prj1-' + '1' * 64, 'view': {'runId': 'run3:' + '2' * 64},
     'operation': 'graph.path', 'params': {'relation':'calls','minResolution':'resolved-callee','direction':'outgoing',
     'start':{'universe':'3'*64,'kind':'symbol','nativeSubjectId':'s:a'},
     'target':{'universe':'3'*64,'kind':'symbol','nativeSubjectId':'s:b'},'maxDepth':2},
     'completeness': 'required', 'page': {'size': 1}}
cx = {'projectId':q['projectId'],'resolvedView':q['view'],'factViewDigests':[],
      'availability':'retained','truncated':False,'totalItems':0,'countBasis':'exact',
      'traversalCoverage':'complete','visitedNodes':1,'producedItems':0,'advisory':False,
      'evidence':{'coverageIds':[],'scopeIds':[],'deficiencyCitations':[],'resolutionLimitations':[]}}
cases = [('complete-typed-path-request','GraphQueryRequestV1',q,True),
         ('complete-graph-response-context','GraphOperationResponseContext',cx,True)]
x=copy.deepcopy(q);x['params']={};cases.append(('path-without-endpoints','GraphQueryRequestV1',x,False))
x=copy.deepcopy(q);x['operation']='graph.neighbors';x['params']={'baselineId':'baseline2:'+'4'*64};cases.append(('neighbors-baseline-only','GraphQueryRequestV1',x,False))
x=copy.deepcopy(q);x['params']['start']='src/a.ts';x['params']['target']='src/b.ts';cases.append(('path-only-endpoints','GraphQueryRequestV1',x,False))
x=copy.deepcopy(cx);x['resolvedView']={'latest':True};cases.append(('unresolved-graph-response','GraphOperationResponseContext',x,False))
x=copy.deepcopy(cx);x['advisory']=True;cases.append(('advisory-graph-response','GraphOperationResponseContext',x,False))
x=copy.deepcopy(cx);del x['evidence'];cases.append(('missing-evidence-disclosure','GraphOperationResponseContext',x,False))
result={'standing':'bounded reconciliation schema probes; synthetic IDs, no Run or product execution',
        'schemaSha256':hashlib.sha256((WF/'evaluator3/graph-query.schema.json').read_bytes()).hexdigest(),
        'probes':[{'name':n,'selector':s,'value':v,'expectedSchemaAdmission':want,**admitted(s,v)} for n,s,v,want in cases]}
result['allExpected']=all(x['expectedSchemaAdmission']==x['schemaAdmitted'] for x in result['probes'])
Path(__file__).with_name('query-schema-reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'allExpected':result['allExpected'],'probes':len(cases)}))
