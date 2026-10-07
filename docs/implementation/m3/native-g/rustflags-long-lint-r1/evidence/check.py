import ast,hashlib,json,re,subprocess,os
from pathlib import Path
b=Path(__file__).resolve().parent;a=Path('/Users/sb/code/opensip-ai/opensip_arch');parent=a/'docs/implementation/m3/native-g/rustflags-reference-r1/reference/native_evidence_model.v2.py'
names={'_CFG_RE','_LINT_RE','_ALLOWED_C','_ALLOWED_C_VALUES','rustflags_projection'}
def load(p):
 nodes=[]
 for n in ast.parse(p.read_text()).body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets):nodes.append(n)
  elif isinstance(n,ast.FunctionDef) and n.name in names:nodes.append(n)
 assert len(nodes)==5
 scope={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),scope);return scope['rustflags_projection']
old=load(parent);new=load(b/'native_evidence_model.v2.py');rows=[]
def control(label,flags,honored,stripped,changed=False):
 expected=dict(honored=honored,stripped=stripped,executableSelected=False);actual=new(flags,{'src'},{'closure'});prior=old(flags,{'src'},{'closure'});assert actual==expected,(label,actual,expected);assert (actual!=prior)==changed,(label,prior,actual)
 rows.append(dict(label=label,flags=flags,expected=expected,parent=prior,changed=changed))
prior_controls=json.loads((a/'docs/implementation/m3/native-g/rustflags-reference-r1/evidence/controls.json').read_text())
for row in prior_controls['rows']:
 x=row['expected'];control('r1-'+row['label'],row['flags'],x['honored'],x['stripped'])
for long in ['--allow','--warn','--deny','--forbid']:
 for value in ['dead_code','clippy::all','unused_variables']:
  f=long+'='+value;control('attached-'+f,[f],[f],[],True)
 for value in ['', 'Dead_Code','dead_code\n','dead code','dead-code','dead_code=extra']:
  f=long+'='+value;control('invalid-'+repr(f),[f],[],[dict(flag=f,reason='lint-syntax')],True)
 f=long+'=dead_code';control('order-'+long,[f,'@args','--cfg=feature'],[f,'--cfg=feature'],[dict(flag='@args',reason='response-file')],True)
control('unknown-long-lint',['--allows=dead_code'],[],[dict(flag='--allows=dead_code',reason='not-allowlisted')])
result=dict(passed=True,controls=len(rows),changedCounterexamples=sum(x['changed'] for x in rows),execution='Five AST-selected pure declarations only; no whole-model import',fullRustflagsConformance=False,productCodeUnchanged=True,qualification=False,rows=rows)
(b/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
