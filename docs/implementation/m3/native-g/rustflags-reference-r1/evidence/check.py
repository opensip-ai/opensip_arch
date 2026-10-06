import ast,hashlib,json,re
from pathlib import Path
b=Path(__file__).resolve().parent
parent=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py')
names={'_CFG_RE','_LINT_RE','_ALLOWED_C','_ALLOWED_C_VALUES','rustflags_projection'}
def load(p):
 tree=ast.parse(p.read_text()); nodes=[]
 for n in tree.body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets):nodes.append(n)
  elif isinstance(n,ast.FunctionDef) and n.name in names:nodes.append(n)
 assert len(nodes)==5
 scope={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),scope);return scope['rustflags_projection']
old=load(parent);new=load(b/'native_evidence_model.v2.py');rows=[]
def control(label,flags,honored,stripped,changed=False):
 result=new(flags,{'src'},{'closure'});expected={'honored':honored,'stripped':stripped,'executableSelected':False};assert result==expected,(label,result,expected)
 prior=old(flags,{'src'},{'closure'});assert (prior!=result)==changed,(label,prior,result)
 rows.append(dict(label=label,flags=flags,expected=expected,parent=prior,changed=changed))
for v in ['allow','warn','deny','forbid']:
 for flags in [[f'--cap-lints={v}'],['--cap-lints',v]]:control('named-cap-'+repr(flags),flags,flags,[])
for v in ['', 'other', 'ALLOW','allow\n']:
 control('inline-invalid-'+repr(v),['--cap-lints='+v],[],[{'flag':'--cap-lints='+v,'reason':'cap-lints-value'}],True)
 control('split-invalid-'+repr(v),['--cap-lints',v],[],[{'flag':'--cap-lints '+v,'reason':'cap-lints-value'}])
for flags in [['--cfg','feature'],['--cfg=feature'],['--cfg','feature="x"'],['-A','dead_code'],['-Adead_code'],['--warn','clippy::all'],['-C','opt-level=2'],['-Ctarget-feature=+sse2,-avx']]:control('unchanged-valid-'+repr(flags),flags,flags,[])
for flags,reason in [(['--cfg','feature\n'],'cfg-syntax'),(['--cfg=feature\n'],'cfg-syntax'),(['-A','dead_code\n'],'lint-syntax'),(['-Adead_code\n'],'not-allowlisted'),(['-C','opt-level=2\n'],'codegen-option-not-allowlisted'),(['-Copt-level=2\n'],'codegen-option-not-allowlisted')]:
 control('terminal-LF-'+repr(flags),flags,[],[{'flag':' '.join(flags),'reason':reason}],True)
for flags,reason in [(['@args'],'response-file'),(['--unknown'],'not-allowlisted'),(['-C','link-arg=-x'],'codegen-option-not-allowlisted'),(['--cfg'],'dangling'),(['--remap-path-prefix=outside=x'],'remap-from-outside-snapshot-or-closure')]:control('unchanged-refusal-'+repr(flags),flags,[],[{'flag':' '.join(flags),'reason':reason}])
for flags in [['--remap-path-prefix=src=virtual'],['--remap-path-prefix','closure=virtual']]:control('verified-path-'+repr(flags),flags,flags,[])
control('ordered-disclosures',['-Adead_code','@args','--cap-lints=other','--cfg=feature'],['-Adead_code','--cfg=feature'],[{'flag':'@args','reason':'response-file'},{'flag':'--cap-lints=other','reason':'cap-lints-value'}],True)
# Unresolved interior quoted cfg whitespace is explicitly unchanged, not repaired.
control('interior-space-remains-unresolved',['--cfg','feature="a b"'],['--cfg','feature="a b"'],[])
result=dict(passed=True,controls=len(rows),changedCounterexamples=sum(x['changed'] for x in rows),execution='AST-selected five pure declarations only; no whole-model import',fullRustflagsConformance=False,productCodeUnchanged=True,qualification=False,rows=rows)
(b/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
