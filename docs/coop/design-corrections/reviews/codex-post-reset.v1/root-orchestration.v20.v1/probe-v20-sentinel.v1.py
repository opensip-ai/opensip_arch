"""Targeted exact-helper control: success must differ from every Refusal detail.
Executes only the shipped helper AST with deliberately injected return/refusal inputs;
not an adopt_baseline invocation or a sealed Run test.
"""
from pathlib import Path
import ast,json,importlib.util,sys,hashlib
B=Path('/tmp/opensip-design-corrections/v20-final-source.v2');D=B/'work/docs/coop/design-corrections';p=D/'foundation/check-identity.py';mod=ast.parse(p.read_text())
nodes=[n for n in mod.body if (isinstance(n,ast.FunctionDef) and n.name=='_adopt_scope_detail') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_NO_REFUSAL' for t in n.targets))];assert len(nodes)==2
s=importlib.util.spec_from_file_location('workflow',D/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);sys.modules[s.name]=W;s.loader.exec_module(W)
ns={'W':W};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns);rows=[]
def run(name,fn,expected):
 ns['_adopt']=fn
 actual=ns['_adopt_scope_detail']([], {}) is ns['_NO_REFUSAL'];assert actual is expected
 rows.append({'id':name,'successPredicate':actual,'expected':expected,'passed':True})
run('ordinary-success-return',lambda *_:{},True)
run('success-may-return-none',lambda *_:None,True)
for detail in [None,'CONFIG.INVALID','BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER','BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH']:
 def refused(*_,detail=detail):raise W.Refusal('CONFIG.INVALID',detail,'probe')
 run('actual-Refusal-detail-'+str(detail),refused,False)
def crash(*_):raise ValueError('probe-unexpected-error')
ns['_adopt']=crash
try:ns['_adopt_scope_detail']([],{})
except ValueError as e:assert str(e)=='probe-unexpected-error';rows.append({'id':'unexpected-error-propagates','passed':True})
else:raise AssertionError('unexpected error swallowed')
r={'standing':'Exact final helper AST under explicit injected behavior; not product invocation/adopt_baseline functional or full Run evidence.','sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':rows,'passed':len(rows),'failed':0};(B/'root-sentinel.v1.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
