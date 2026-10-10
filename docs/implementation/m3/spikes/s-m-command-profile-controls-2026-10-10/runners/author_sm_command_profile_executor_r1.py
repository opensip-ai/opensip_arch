from pathlib import Path
B=Path('/tmp/opensip-implementation');V=B/'sm-command-data-2026-10-10';s=(B/'sm-cargo-unit-context-2026-10-10/context_graph_execution.py').read_text()
s=s.replace('import json,hashlib,os,struct,dataclasses,sys','import json,hashlib,os,struct,dataclasses,sys,re')
parser=r'''
def parse_static_arguments(row,u):
 args=row.get('arguments')
 if not isinstance(args,list) or any(not isinstance(a,str) or '\0' in a for a in args):raise ValueError('static argument DATA shape')
 pairs={};profile=[];cfg=[];check_cfg=[];externs=[];i=0;source=None
 while i<len(args):
  a=args[i];i+=1
  if a in ['--crate-name','--crate-type','--out-dir','--target','--cfg','--check-cfg','--extern','-C','-L']:
   if i==len(args):raise ValueError('truncated static argument DATA')
   value=args[i];i+=1
   if a in ['--crate-name','--crate-type','--out-dir','--target']:
    if a in pairs:raise ValueError('duplicate static structural argument')
    pairs[a]=value
   elif a=='--cfg':cfg.append(value)
   elif a=='--check-cfg':check_cfg += [a,value]
   elif a=='--extern':
    alias,sep,path=value.partition('=')
    if not sep or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',alias) or not Path(path).is_absolute():raise ValueError('static extern DATA shape')
    externs.append(alias)
   elif a=='-L':
    if not value.startswith('dependency=') or not Path(value[len('dependency='):]).is_absolute():raise ValueError('outside experimental dependency search DATA')
   else:
    key,sep,v=value.partition('=')
    if not sep:raise ValueError('static codegen DATA shape')
    if key=='metadata':
     if 'metadata' in pairs or not re.fullmatch('[0-9a-f]+',v):raise ValueError('static metadata DATA shape')
     pairs['metadata']=v
    elif key=='incremental':
     if not Path(v).is_absolute():raise ValueError('static incremental DATA shape')
     pairs['incremental']=True
    elif key=='extra-filename':
     if not re.fullmatch('-[0-9a-f]+',v):raise ValueError('static artifact suffix DATA shape')
     pairs['extra-filename']=v;profile += [a,value]
    else:
     allowed={'opt-level':{'0','1','2','3','s','z'},'embed-bitcode':{'yes','no'},'debug-assertions':{'on','off'},'overflow-checks':{'on','off'},'panic':{'abort','unwind'},'debuginfo':{'0','1','2','line-directives-only','line-tables-only'},'split-debuginfo':{'off','packed','unpacked'},'strip':{'none','debuginfo','symbols'}}
     if key not in allowed or v not in allowed[key]:raise ValueError('outside explicit experimental static codegen DATA')
     profile += [a,value]
  elif a.startswith('--edition='):
   if 'edition' in pairs:raise ValueError('duplicate static edition')
   pairs['edition']=a[len('--edition='):]
  elif a.startswith('--emit='):
   if a!='--emit=dep-info,metadata':raise ValueError('outside metadata-only emission DATA')
   pairs['emit']='dep-info,metadata'
  elif a.startswith('--error-format=') or a.startswith('--json='):
   if a not in ['--error-format=json','--json=diagnostic-rendered-ansi,artifacts,future-incompat']:raise ValueError('outside static diagnostic DATA')
  elif a=='--cap-lints':
   if i==len(args) or args[i] not in ['allow','warn']:raise ValueError('outside static cap-lint DATA')
   profile += [a,args[i]];i+=1
  elif a.startswith('-'):raise ValueError('outside explicit experimental static command DATA')
  else:
   if source is not None:raise ValueError('duplicate static source DATA')
   source=a
 cwd=row['cwd'];canonical=os.path.normpath(source if source and Path(source).is_absolute() else str(Path(cwd)/str(source)))
 if canonical!=u['target']['src_path']:raise ValueError('static source graph join differs')
 name=row['constructedEnvironment'].get('CARGO_CRATE_NAME')
 if pairs.get('--crate-name')!=name or name!=u['target']['name']:raise ValueError('static crate name graph join differs')
 if pairs.get('--crate-type') not in ['lib','rlib'] or pairs['--crate-type'] not in u['target']['crate_types']:raise ValueError('static crate type graph join differs')
 if pairs.get('edition')!=u['target']['edition'] or pairs.get('--target')!=u['platform']:raise ValueError('static edition or platform join differs')
 if not Path(pairs.get('--out-dir','')).is_absolute() or 'metadata' not in pairs or pairs.get('emit')!='dep-info,metadata':raise ValueError('static output DATA shape')
 expected=['feature='+json.dumps(f,ensure_ascii=False) for f in u['features']]
 if sorted(cfg)!=sorted(expected):raise ValueError('static feature graph join differs')
 if sorted(externs)!=sorted(d['extern_crate_name'] for d in u['dependencies']) or len(set(externs))!=len(externs):raise ValueError('static extern alias graph join differs')
 return dict(core=pairs,profileArguments=profile,checkCfgArguments=check_cfg,capturedArguments=args)
'''
s=s.replace('\ndef execute_graph(',parser+'\ndef execute_graph(',1)
s=s.replace("contexts=context['units']","contexts=context['units'];parsed={}",1)
s=s.replace("  env=row['constructedEnvironment']", "  if type(row.get('staticCargoCommandConstructed')) is not bool:raise ValueError('static command standing DATA shape')\n  if not row['staticCargoCommandConstructed']:continue\n  env=row['constructedEnvironment']",1)
s=s.replace("  if row['capLintArguments'] not in [[],['--cap-lints','allow'],['--cap-lints','warn']]:raise ValueError('outside pinned Cargo cap-lint DATA shape')\n",'')
s=s.replace("  if not isinstance(path,str) or not Path(path).is_absolute() or str(Path(path))!=path:raise ValueError('supplied package cwd DATA shape')", "  if not isinstance(path,str) or not Path(path).is_absolute() or str(Path(path))!=path:raise ValueError('supplied package cwd DATA shape')\n  if u['target']['kind']==['lib'] and u['target']['crate_types'] in [['lib'],['rlib']] and u['mode']=='check':parsed[i]=parse_static_arguments(row,u)",1)
s=s.replace("  elif target['src_path'] not in names", "  elif not contexts[i]['staticCargoCommandConstructed']:blocked[i]='static-cargo-command-unavailable'\n  elif target['src_path'] not in names",1)
old="  target=u['target'];out=r/('lib'+target['name']+'.rmeta');argv=[wrapper_pin['path'],'--prepared-map',map_pin['path'],'--crate-type','lib','--crate-name',target['name'],'--edition',target['edition'],'--sysroot',str(sysroot),'--emit','metadata',target['src_path'],'-o',str(out),'-C',f'metadata=experiment_unit_{i}']"
assert old in s
new="  target=u['target'];plan=parsed[i];core=plan['core'];out=r/('lib'+target['name']+core.get('extra-filename','')+'.rmeta');argv=[wrapper_pin['path'],'--prepared-map',map_pin['path'],'--crate-type',core['--crate-type'],'--crate-name',target['name'],'--edition',target['edition'],'--sysroot',str(sysroot),'--emit',core['emit'],target['src_path'],'--out-dir',str(r),'-C','metadata='+core['metadata']]\n  argv += plan['profileArguments'] + plan['checkCfgArguments']\n  if core.get('incremental'):argv += ['-C','incremental='+str(r/'incremental')]"
s=s.replace(old,new,1)
s=s.replace("  argv += contexts[i]['capLintArguments']", "  # Actual static profile/check-cfg/cap args retained; source/output/search/extern paths rebound to checked prototype inputs.",1)
s=s.replace("contextPin=context_pin,actualConstructedPackageEnvironmentAndCwdUsed=True", "contextPin=context_pin,actualStaticCommandData=plan,staticProfileCheckCfgArgumentsApplied=True,sourceOutputSearchExternBindingsReplaced=True,completeRuntimeCommand=False,actualConstructedPackageEnvironmentAndCwdUsed=True")
s=s.replace('EXPERIMENTAL GRAPH-INDEXED METADATA ANALYSIS; NOT FULL NATIVE PROFILE','EXPERIMENTAL ACTUAL STATIC PROFILE ARGUMENT ANALYSIS WITH REBOUND PRIVATE IO; NOT FULL NATIVE PROFILE')
p=V/'command_profile_graph_execution.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s);print('New isolated static-profile argument executor authored; no controls or corpus use yet.')
