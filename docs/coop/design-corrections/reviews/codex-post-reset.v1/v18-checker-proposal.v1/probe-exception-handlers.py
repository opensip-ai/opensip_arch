"""Execute the actual ten exception-handler bodies under controlled refusals.

This isolates reference-harness reporting, not product admission. An absent expected
refusal, a deliberate null, a matching named detail and a wrong named detail must
remain distinguishable. The exact extracted handlers, including their continue,
run unmodified inside a one-iteration loop; no reimplementation of the comparison.
"""
from pathlib import Path
import ast,copy,json,hashlib,types
HERE=Path(__file__).resolve().parent
rel='docs/coop/design-corrections/workflows/check_workflows.v1.py'
paths={'before':HERE/'checker.before.py','proposal':HERE/'proposal'/rel}
class Refusal(Exception):
 def __init__(self,detail):self.detail=detail;self.error_code='CONFIG.INVALID';self.remedy='controlled-probe-reason'
results=[]
for label,path in paths.items():
 source=path.read_text();handlers=[]
 for n in ast.walk(ast.parse(source)):
  if not isinstance(n,ast.ExceptHandler):continue
  keys={c.args[0].value for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='get' and c.args and isinstance(c.args[0],ast.Constant) and c.args[0].value in ('refusal','recoverRefusal')}
  if not keys:continue
  assert len(keys)==1;handlers.append((n,next(iter(keys))))
 assert len(handlers)==10
 for handler,key in sorted(handlers,key=lambda r:r[0].lineno):
  # The handler body is copied verbatim. Its try invokes an injected exception;
  # its outer loop preserves the original continue semantics.
  h=copy.deepcopy(handler)
  t=ast.Try(body=[ast.Raise(exc=ast.Name(id='injected',ctx=ast.Load()),cause=None)],handlers=[h],orelse=[],finalbody=[])
  module=ast.Module(body=[ast.For(target=ast.Name(id='_once',ctx=ast.Store()),iter=ast.List(elts=[ast.Constant(value=0)],ctx=ast.Load()),body=[t],orelse=[])],type_ignores=[])
  ast.fix_missing_locations(module);code=compile(module,str(path),'exec')
  cases=[('unexpected-null',{},None,False),('unexpected-named',{},'wrong',False),('expected-null',{key:None},None,True),('expected-named',{key:'right'},'right',True),('wrong-named',{key:'right'},'wrong',False)]
  for name,exp,detail,want in cases:
   observed=[]
   def check(cid,ok,*reason):observed.append({'id':cid,'passed':bool(ok),'reason':reason})
   env={'M':types.SimpleNamespace(Refusal=Refusal),'injected':Refusal(detail),'check':check,'cid':'controlled','case':{'id':'controlled','expect':exp},'exp':exp}
   exec(code,env);assert len(observed)==1,(label,handler.lineno,name,observed)
   results.append({'version':label,'handlerLine':handler.lineno,'expectedKey':key,'control':name,'expectedPass':want,'actualPass':observed[0]['passed'],'matchesExpected':observed[0]['passed']==want})
report={'standing':'Controlled execution of exact exception-handler bodies; synthetic exceptions, not full workflow/model or host-enforcement evidence. The before-image must expose ten false passes and the proposal must eliminate those while preserving forty other controls per version.','sourceSha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'rows':results,'mismatches':{k:[r for r in results if r['version']==k and not r['matchesExpected']] for k in paths}}
assert len(report['mismatches']['before'])==10 and all(r['control']=='unexpected-null' for r in report['mismatches']['before'])
assert not report['mismatches']['proposal']
q=HERE/'exception-handler-results.json';assert not q.exists();q.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'executedControls':len(results),'beforeFalsePasses':len(report['mismatches']['before']),'proposalMismatches':len(report['mismatches']['proposal'])}))
