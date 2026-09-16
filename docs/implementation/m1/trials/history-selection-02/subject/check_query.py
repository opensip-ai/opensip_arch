"""Actual unchanged close_run owner exercise over synthetic retained evidence.

No compiler, signed release, product store or operational receipt qualification.
"""
import ast,copy,hashlib,importlib.machinery,importlib.util,json,tempfile,types
from pathlib import Path
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012
HERE=Path(__file__).resolve().parent
ARCH=Path('/Users/sb/code/opensip-ai/opensip_arch')
pins=json.loads((HERE/'input-pins.json').read_bytes())['files'];raws={};by_path={}
for pin in pins:
 b=Path(pin['path']).read_bytes();assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],pin['path'];raws[pin['role']]=b;by_path[pin['path']]=b
scratch=Path(tempfile.mkdtemp(prefix='opensip-history02-query-'))
for rel in json.loads((HERE/'fixture-owner-files.json').read_bytes())['files']:
 target=scratch/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(by_path[str(ARCH/rel)])
# Never consume adjacent .pyc for copied owner sources. Imports outside this
# scratch tree remain the declared Python reference environment, not this proof.
original_get_code=importlib.machinery.SourceFileLoader.get_code
compiled=[]
def owned_source_code(loader,fullname):
 path=Path(loader.path).resolve()
 if path.is_relative_to(scratch.resolve()):
  rel=str(path.relative_to(scratch.resolve()));b=path.read_bytes();assert b==by_path[str(ARCH/rel)];compiled.append(rel);return compile(b,str(path),'exec')
 return original_get_code(loader,fullname)
importlib.machinery.SourceFileLoader.get_code=owned_source_code

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
F=load('history_fixture',scratch/'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py')
R=load('history_replay',scratch/'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py')
helper=ast.parse(raws['fixture-helper']);node=next(n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name=='positive_run')
ns={'copy':copy};exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned-positive-run-fixture-helper','exec'),ns)
run,objects,blobs,graph=ns['positive_run'](F,R)
M=R.M;rid=M.close_run(run,objects,blobs);pid=run['projectId']
Q=types.ModuleType('history_query_candidate');exec(compile((HERE/'query_history.py').read_bytes(),str(HERE/'query_history.py'),'exec'),Q.__dict__)
C=M.C
query=json.loads((HERE/'graph-query.history-candidate.schema.json').read_bytes())
documents=[query,json.loads(raws['common']),json.loads(raws['identity-schema']),json.loads(raws['invocation'])]
registry=Registry().with_resources((d['$id'],Resource(contents={k:v for k,v in d.items() if k!='$schema'},specification=DRAFT202012)) for d in documents)
def validate(value):C.validate({'$ref':query['$id']+'#/$defs/GraphQueryResponseV1'},value,registry)
result={'kind':'analysis','authority':'authoritative','runId':rid,'planId':run['planId'],'verdict':objects[run['evaluationSealId']][1]['verdict'],'requiredCoverage':'satisfied','durability':'committed','deficiency':'none','secondaryDeficiencies':[]}
source={'state':'retained','run':run,'objects':objects,'blobs':blobs,'result':result}
rows=[]
def check(name,fn,expected=None):
 try:
  value=fn();passed=expected is None;observed='returned'
 except Exception as exc:
  observed=type(exc).__name__+':'+str(exc).split('\n')[0][:180];passed=expected is not None and isinstance(exc,expected)
 rows.append({'id':name,'passed':passed,'observed':observed});assert passed,(name,observed)
 return value if expected is None else None
response=check('actual-close-run-typed-result',lambda:Q.run_show(pid,rid,source,M,validate))
check('consumer-exact-join',lambda:Q.admit_response(response,pid,rid,validate))
check('wrong-requested-run',lambda:Q.run_show(pid,'run3:'+'f'*64,source,M,validate),Q.QueryHistorySourceRefusal)
check('wrong-project',lambda:Q.run_show('prj1-'+'f'*64,rid,source,M,validate),Q.QueryHistorySourceRefusal)
bad=copy.deepcopy(source);bad['result']['planId']='plan2:'+'0'*64
check('wrong-receipt-plan',lambda:Q.run_show(pid,rid,bad,M,validate),Q.QueryHistorySourceRefusal)
bad=copy.deepcopy(source);bad['result']['verdict']='fail' if result['verdict']!='fail' else 'pass'
check('wrong-receipt-verdict',lambda:Q.run_show(pid,rid,bad,M,validate),Q.QueryHistorySourceRefusal)
for state in ['expired','purged','corrupt','unavailable']:
 out=check('availability-'+state,lambda state=state:Q.run_show(pid,rid,{'state':'unavailable','availability':state},M,validate));assert out['context']['availability']==state and out['items']==[]
bad=copy.deepcopy(response);bad['items']=[{'arbitrary':'not typed'}]
check('untyped-run-show-item-refused',lambda:validate(bad),C.ValidationError)
bad=copy.deepcopy(response);bad['items'][0]['projectId']='prj1-'+'f'*64
check('consumer-wrong-item-project',lambda:Q.admit_response(bad,pid,rid,validate),Q.QueryHistorySourceRefusal)
bad=copy.deepcopy(source);bad['blobs'].pop(objects[run['planId']][1]['policyDigest'])
out=check('lost-retained-byte-exercises-owner',lambda:Q.run_show(pid,rid,bad,M,validate));assert out['context']['availability'] in ['unavailable','corrupt'] and not out['items'], 'lost-retained-byte-exercises-owner'
# An unrecognized failure is an operational defect, never a retained-corrupt label.
class BrokenOwner:
 EvidenceUnavailable=M.EvidenceUnavailable;CompleteReplayMismatch=M.CompleteReplayMismatch;C=M.C
 @staticmethod
 def close_run(*args):raise RuntimeError('sentinel-host-fault')
check('unknown-owner-exception-not-downgraded',lambda:Q.run_show(pid,rid,source,BrokenOwner,validate),RuntimeError)
(HERE/'query-check-result.json').write_text(json.dumps({'standing':'Root02 actual unchanged close_run reference over synthetic evidence. Receipt fields remain a host fixture, not product custody.','runId':rid,'projectId':pid,'groups':len(rows),'rows':rows,'compiledOwnerSourcePaths':sorted(set(compiled)),'scratch':str(scratch),'pins':len(pins),'allPassed':all(r['passed'] for r in rows)},indent=2)+'\n')
print(json.dumps({'groups':len(rows),'allPassed':True,'runId':rid}))
