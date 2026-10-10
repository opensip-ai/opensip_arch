from pathlib import Path
b=Path('/tmp/opensip-implementation');v=b/'sm-cargo-unit-context-2026-10-10';base=b/'sm-graph-typecheck-2026-10-10/graph_execution.py';dest=v/'context_graph_execution.py';assert not dest.exists();s=base.read_text().replace('def execute_graph(graph,map_pin,output_root,wrapper_pin,sysroot,cwd):','def execute_graph(graph,map_pin,output_root,wrapper_pin,sysroot,cwd,context_pin):')
needle=" checked(wrapper_pin);names=map_names(checked(map_pin));root=Path(output_root)"
replacement=''' context=json.loads(checked(context_pin));units_input=graph['units']
 if context.get('version')!=1 or len(context.get('units',[]))!=len(units_input):raise ValueError('supplied context population differs')
 contexts=context['units']
 for i,(u,row) in enumerate(zip(units_input,contexts)):
  if row['index']!=i or type(row['index']) is not int:raise ValueError('supplied context index differs')
  for field,key in [('packageId','pkg_id'),('target','target'),('profile','profile'),('platform','platform'),('mode','mode'),('features','features')]:
   if row[field]!=u[key]:raise ValueError('supplied context graph join differs')
  env=row['constructedEnvironment']
  if not isinstance(env,dict) or any(not isinstance(k,str) or not k or '=' in k or '\\0' in k or not isinstance(value,str) or '\\0' in value for k,value in env.items()):raise ValueError('supplied environment DATA shape')
  if row['capLintArguments'] not in [[],['--cap-lints','allow'],['--cap-lints','warn']]:raise ValueError('outside pinned Cargo cap-lint DATA shape')
  path=row['cwd']
  if not isinstance(path,str) or not Path(path).is_absolute() or str(Path(path))!=path:raise ValueError('supplied package cwd DATA shape')
 checked(wrapper_pin);names=map_names(checked(map_pin));root=Path(output_root)'''
assert needle in s;s=s.replace(needle,replacement,1)
s=s.replace("  # Empty environment is deliberate prototype context; missing Cargo/package/build context remains failure.","  # Actual constructed package env/cwd/cap-lint DATA; full command/profile remains incomplete.\n  argv += contexts[i]['capLintArguments']\n  checked(context_pin)")
s=s.replace('cwd=str(cwd),environment={}','cwd=contexts[i][\'cwd\'],environment=contexts[i][\'constructedEnvironment\']')
s=s.replace("fullCargoProfileEnvironment=False);results.append(record)","fullCargoProfileEnvironment=False,packageContextData=contexts[i],contextPin=context_pin,actualConstructedPackageEnvironmentAndCwdUsed=True);results.append(record)")
s=s.replace('emptyChildEnvironment=True,','emptyChildEnvironment=False,constructedPackageEnvironmentAndCwdUsed=True,contextPin=context_pin,actualCompleteCargoProfile=False,')
dest.write_text(s);print('Prepared isolated new context-using executor; accepted graph executor unchanged')
