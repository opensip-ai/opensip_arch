from pathlib import Path
import importlib.util,json,hashlib,itertools
b=Path('/tmp/opensip-implementation/discovery-pruning-reference-authoring')
def model(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=model('dd_old',b/'discovery-defaults.original.py');new=model('dd_new',b/'discovery-defaults.pruning-r1.py');rows=[]
def add(label,call,args,expected,kwargs=None):
 kwargs=kwargs or {};before=getattr(old,call)(*args,**kwargs);after=getattr(new,call)(*args,**kwargs)
 def plain(v):
  if isinstance(v,set):return sorted(v)
  if isinstance(v,tuple):return list(v)
  return v
 assert plain(after)==plain(expected),(label,after,expected)
 rows.append(dict(label=label,function=call,args=args,kwargs=kwargs,before=plain(before),after=plain(after),expected=plain(expected),changed=plain(before)!=plain(after)))
for root in ['', 'workspace']:
 pre=root+'/' if root else ''
 for segment in ['node_modules','.git','.hg','.svn','.jj']:
  add(pre+'target-before-'+segment,'classify_path',[pre+'target/'+segment+'/pkg/file',[root]],(pre+'target','cargo-build-output'))
  add(pre+segment+'-before-target','classify_path',[pre+segment+'/target/pkg/file',[root,pre+segment]],(pre+segment,'dependency-tree' if segment=='node_modules' else 'vcs-tree'))
  add(pre+'ordinary-target-no-parent-marker-'+segment,'classify_path',[pre+'src/target/'+segment+'/file',[root]],(pre+'src/target/'+segment,'dependency-tree' if segment=='node_modules' else 'vcs-tree'))
 add(pre+'plain-target','classify_path',[pre+'target/debug/file',[root]],(pre+'target','cargo-build-output'))
 add(pre+'unrooted-target','classify_path',[pre+'packages/target/index.ts',[root]],None)
 add(pre+'substring-target','classify_path',[pre+'targetish/node_modulesish/file',[root]],None)
 markers=[pre+'Cargo.toml',pre+'target/dependency/Cargo.toml',pre+'node_modules/pkg/Cargo.toml',pre+'.git/Cargo.toml',pre+'src/Cargo.toml']
 for i,perm in enumerate([markers,list(reversed(markers)),markers[2:]+markers[:2]]):
  add(pre+'cargo-root-pruned-marker-order-'+str(i),'cargo_roots_from_markers',[perm],{root,pre+'src'})
 add(pre+'missing-parent-is-normal-source','cargo_roots_from_markers',[[pre+'target/inner/Cargo.toml']],{pre+'target/inner'})
# Full supplied marker inventory, explicitly not a filesystem/native census.
markers=['Cargo.toml','target/Cargo.toml']+['target/node_modules/pkg'+str(i)+'/package.json' for i in range(4200)]
expected=dict(unitDirs=[''],prunedTrees=[dict(path='target',reason='cargo-build-output',markerCount=None,markerCountBasis='not-enumerated')],refusal=None)
add('4200-nested-installed-markers-one-outer-cargo-anchor','enumerate_units',[markers],expected,dict(observed_directories=['target','target/node_modules'],marker_inventory_basis='not-enumerated'))
add('4200-nested-installed-markers-observed-inventory','enumerate_units',[markers],dict(unitDirs=[''],prunedTrees=[dict(path='target',reason='cargo-build-output',markerCount=4201,markerCountBasis='observed-inventory')],refusal=None))
# Existing non-Cargo dependency counting and cap semantics unchanged.
markers=['package.json']+['node_modules/p'+str(i)+'/package.json' for i in range(4200)]
add('4200-installed-markers-remain-one-dependency-anchor','enumerate_units',[markers],dict(unitDirs=[''],prunedTrees=[dict(path='node_modules',reason='dependency-tree',markerCount=4200,markerCountBasis='observed-inventory')],refusal=None))
for n in [4096,4097]:
 markers=['p'+str(i)+'/package.json' for i in range(n)];result=new.enumerate_units(markers);assert result==old.enumerate_units(markers)
 assert (len(result['unitDirs'])==n and result['refusal'] is None) if n==4096 else (result['unitDirs']==[] and result['refusal']==dict(detail='WORKSPACE_UNIT_LIMIT',unitCount=n,limit=4096))
 rows.append(dict(label='first-party-cap-'+str(n),changed=False,count=n,result=dict(unitCount=len(result['unitDirs']),refusal=result['refusal'])))
# Other entrypoints keep their exact source AST and controls.
import ast
oldtree=ast.parse((b/'discovery-defaults.original.py').read_text());newtree=ast.parse((b/'discovery-defaults.pruning-r1.py').read_text())
o={x.name:ast.dump(x,include_attributes=False) for x in oldtree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))};q={x.name:ast.dump(x,include_attributes=False) for x in newtree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))};changed=sorted(k for k in o if o[k]!=q[k]);assert changed==['cargo_roots_from_markers','classify_path'];assert o.keys()==q.keys()
assert [ast.dump(x,include_attributes=False) for x in oldtree.body if not isinstance(x,(ast.FunctionDef,ast.ClassDef))] == [ast.dump(x,include_attributes=False) for x in newtree.body if not isinstance(x,(ast.FunctionDef,ast.ClassDef))]
for value,wanted in [('.',''),('a/b/','a/b'),('packages/target','packages/target')]:assert new.normalize_explicit_root(value)==old.normalize_explicit_root(value)==wanted
report=dict(passed=True,controls=len(rows),changedControls=sum(x['changed'] for x in rows),changedFunctions=changed,rows=rows,nativeCensus=False,qualification=False,productEdited=False,fullB2aComplete=False)
(b/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
