"""Execute only the real wrapper's pure receipt_ready AST; never import its module.
Usage: python -I -B this_file.py <new-results-json>
No wrapper top-level code, modes, corpus, cache, lane or worktree access.
"""
from pathlib import Path
import ast,hashlib,json,sys
EV=Path(__file__).resolve().parent
source=EV/'run_c1b_refresh_blind.py'
raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='6b71bdb38e4f372010e2136b7243e07bb04e537fa37f5f59933d0ab04a993eaf'
tree=ast.parse(raw)
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='receipt_ready']
assert len(functions)==1
fn=functions[0]
assert not fn.decorator_list
# Only this function is compiled; top-level wrapper statements are excluded.
namespace={}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source)+':receipt_ready','exec'),namespace)
vectors=EV/'receipt-decision-vectors.json'
cases=json.loads(vectors.read_text())['cases']
results=[]
for c in cases:
 observed=namespace['receipt_ready'](c['name'],c['receipt'],c['baseline'],c['bindings'])
 results.append(dict(case=c['case'],expected=c['expected'],observed=observed,passed=observed is c['expected']))
report=dict(standing='ACTUAL PURE WRAPPER PREDICATE, PUBLIC SYNTHETIC VECTORS',
 runnerSha256=hashlib.sha256(raw).hexdigest(),functionAstSha256=hashlib.sha256(ast.dump(fn,include_attributes=False).encode()).hexdigest(),
 vectorsSha256=hashlib.sha256(vectors.read_bytes()).hexdigest(),
 testSourceSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 cases=results,allPassed=all(r['passed'] for r in results),blindInvocations=0)
# Compile the actual blind loop, ordinary loop and eligibility assignment.
# All dependencies are in-memory fakes; no subprocess or filesystem operation is reachable.
from types import SimpleNamespace
import copy
blind_loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [getattr(e,'id',None) for e in n.target.elts]==['name','tool','receipt'])
ordinary_loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [getattr(e,'id',None) for e in n.target.elts]==['tool','modes'])
eligibility=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Subscript) and isinstance(v.slice,ast.Constant) and v.slice.value=='eligibleForPostRunReview' for v in n.targets))
def compiled(node):return compile(ast.Module(body=[node],type_ignores=[]),str(source)+':actual-branch','exec')
class MemoryPath:
 def __init__(self,name,store):self.name=name;self.store=store
 def __truediv__(self,part):return MemoryPath(self.name+'/'+str(part),self.store)
 def is_file(self):return self.name in self.store
 def read_bytes(self):return self.store[self.name]
 def write_text(self,value):self.store[self.name]=value.encode();return len(value)
def simulate(vector):
 store={};calls=[];ordinary_calls=[];receipt_cases=vector['blind']
 class FakeProcess:
  def run(self,args,**kwargs):
   assert kwargs['cwd'].name=='worktree'
   assert '--held-out-blind' in args or args[3] in ['discovery','companion','workspace']
   if '--held-out-blind' in args:
    name=args[3];spec=receipt_cases[name];calls.append(name)
    if spec['receipt'] is not None:store['worktree/'+name+'-receipt']=json.dumps(spec['receipt']).encode()
    return SimpleNamespace(returncode=spec['exitCode'],stdout='',stderr=spec['stderr'])
   tag=args[3]+args[4];ordinary_calls.append(tag)
   return SimpleNamespace(returncode=vector['ordinaryExits'].get(tag,0),stdout='',stderr='')
 baseline=vector['baseline'];ns=dict(namespace,W=MemoryPath('worktree',store),B=MemoryPath('output',store),subprocess=FakeProcess(),PY='synthetic-python',DISCOVERY='discovery',COMPANION='companion',WORKSPACE='workspace',D_RECEIPT='discovery-receipt',S_RECEIPT='companion-receipt',E={},args=[],row={},blind_ok=True,old={'discovery-receipt':baseline,'companion-receipt':baseline},frozen={'frozenBindings':{'discovery':baseline['bindings'],'companion':baseline['bindings']}},json=json,Path=Path,print=lambda *a,**k:None)
 exec(compiled(blind_loop),ns)
 ns['ordinary_ok']=False
 if ns['blind_ok']:
  ns['ordinary_ok']=True;exec(compiled(ordinary_loop),ns)
 ns['row']['worktreeChangesExactlyTheRunsFour']=vector['fourFiles']
 ns['comparison']=vector['comparison'];exec(compiled(eligibility),ns)
 return dict(blindInvocations=calls,ordinaryInvocations=ordinary_calls,blindOK=ns['blind_ok'],ordinaryOK=ns['ordinary_ok'],eligible=ns['row']['eligibleForPostRunReview'])
sequence_vectors=json.loads((EV/'receipt-sequence-vectors.json').read_text())['cases']
sequence_results=[]
for vector in sequence_vectors:
 observed=simulate(vector)
 sequence_results.append(dict(case=vector['case'],expected=vector['expected'],observed=observed,passed=observed==vector['expected']))
report.update(sequenceCases=sequence_results,sequenceVectorsSha256=hashlib.sha256((EV/'receipt-sequence-vectors.json').read_bytes()).hexdigest(),
 testedBranchesAstSha256=hashlib.sha256(''.join(ast.dump(n,include_attributes=False) for n in [blind_loop,ordinary_loop,eligibility]).encode()).hexdigest(),
 allPassed=report['allPassed'] and all(r['passed'] for r in sequence_results),
 invocationDisclosure='Synthetic invocation names only; real subprocess invocations 0; no wrapper import')
output=Path(sys.argv[1]);assert not output.exists();output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(cases=len(results),allPassed=report['allPassed'],blindInvocations=0)))
assert report['allPassed']
