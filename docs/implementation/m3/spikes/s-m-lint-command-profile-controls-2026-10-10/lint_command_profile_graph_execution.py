from pathlib import Path
import json,hashlib,os,struct,dataclasses,sys,re
sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality')
from root_observation import observe_root

def checked(row):
 p=Path(row['path']);raw=p.read_bytes()
 if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('supplied whole pin differs')
 return raw

def map_names(raw):
 if not raw.startswith(b'OPSMRUST1\0'):raise ValueError('private map header')
 at=10
 def number():
  nonlocal at
  if at+8>len(raw):raise ValueError('private map truncated')
  n=struct.unpack('>Q',raw[at:at+8])[0];at+=8;return n
 count=number();names=set()
 if count>len(raw)//16:raise ValueError('private map count inconsistent')
 for _ in range(count):
  n=number()
  if n>len(raw)-at:raise ValueError('private map name truncated')
  name=raw[at:at+n].decode('utf8');at+=n;p=Path(name)
  if not p.is_absolute() or str(p)!=name or any(x in ['.','..'] for x in p.parts) or name in names:raise ValueError('noncanonical or duplicate private source name')
  names.add(name);n=number()
  if n>len(raw)-at:raise ValueError('private map content truncated')
  at+=n
 if at!=len(raw):raise ValueError('private map trailing bytes')
 return names

def parse_static_arguments(row,u):
 args=row.get('arguments')
 if not isinstance(args,list) or any(not isinstance(a,str) or '\0' in a for a in args):raise ValueError('static argument DATA shape')
 pairs={};profile=[];cfg=[];check_cfg=[];externs=[];i=0;source=None
 while i<len(args):
  a=args[i];i+=1
  if a in ['--crate-name','--crate-type','--out-dir','--target','--cfg','--check-cfg','--extern','-C','-L','--warn','--deny','--allow','--forbid']:
   if i==len(args):raise ValueError('truncated static argument DATA')
   value=args[i];i+=1
   if a in ['--crate-name','--crate-type','--out-dir','--target']:
    if a in pairs:raise ValueError('duplicate static structural argument')
    pairs[a]=value
   elif a in ['--warn','--deny','--allow','--forbid']:
    if not re.fullmatch('[a-z0-9_:]+',value):raise ValueError('outside explicit lint argument DATA shape')
    profile += [a,value]
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
  elif any(a.startswith(flag+'=') for flag in ['--warn','--deny','--allow','--forbid']):
   if not re.fullmatch('[a-z0-9_:]+',a.split('=',1)[1]):raise ValueError('outside explicit joined lint argument DATA shape')
   profile.append(a)
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

def execute_graph(graph,map_pin,output_root,wrapper_pin,sysroot,cwd,context_pin):
 # Supplied graph/map/runtime locations are experimental input, never native capabilities.
 context=json.loads(checked(context_pin));units_input=graph['units']
 if context.get('version')!=1 or len(context.get('units',[]))!=len(units_input):raise ValueError('supplied context population differs')
 contexts=context['units'];parsed={}
 for i,(u,row) in enumerate(zip(units_input,contexts)):
  if row['index']!=i or type(row['index']) is not int:raise ValueError('supplied context index differs')
  for field,key in [('packageId','pkg_id'),('target','target'),('profile','profile'),('platform','platform'),('mode','mode'),('features','features')]:
   if row[field]!=u[key]:raise ValueError('supplied context graph join differs')
  if type(row.get('staticCargoCommandConstructed')) is not bool:raise ValueError('static command standing DATA shape')
  if not row['staticCargoCommandConstructed']:continue
  env=row['constructedEnvironment']
  if not isinstance(env,dict) or 'HOME' in env or any(not isinstance(k,str) or not k or '=' in k or '\0' in k or not isinstance(value,str) or '\0' in value for k,value in env.items()):raise ValueError('supplied environment DATA shape')
  path=row['cwd']
  if not isinstance(path,str) or not Path(path).is_absolute() or str(Path(path))!=path:raise ValueError('supplied package cwd DATA shape')
  if u['target']['kind']==['lib'] and u['target']['crate_types'] in [['lib'],['rlib']] and u['mode']=='check':parsed[i]=parse_static_arguments(row,u)
 checked(wrapper_pin);names=map_names(checked(map_pin));root=Path(output_root)
 if not root.is_absolute() or root.exists():raise ValueError('fresh explicit output root required')
 units=graph['units'];roots=graph['roots']
 if graph['version']!=1 or not isinstance(units,list) or not isinstance(roots,list):raise ValueError('private graph shape')
 def index(i):
  if type(i) is not int or not 0<=i<len(units):raise ValueError('private graph index')
 for i in roots:index(i)
 dependencies=[];blocked={}
 for i,u in enumerate(units):
  deps=u['dependencies'];edges=[]
  if not isinstance(deps,list) or not isinstance(u['features'],list) or any(not isinstance(f,str) for f in u['features']):raise ValueError('private graph value shape')
  for d in deps:index(d['index']);edges.append(d['index'])
  dependencies.append(edges);target=u['target']
  if target['kind']!=['lib'] or target['crate_types'] not in [['lib'],['rlib']]:blocked[i]='expansion-or-target-kind-unavailable'
  elif u['mode']!='check' or target['edition'] not in ['2015','2018','2021','2024'] or u['platform'] not in [None,'aarch64-apple-darwin']:blocked[i]='outside-explicit-experimental-target-context'
  elif not contexts[i]['staticCargoCommandConstructed']:blocked[i]='static-cargo-command-unavailable'
  elif target['src_path'] not in names:blocked[i]='missing-prepared-source-root'
 order=[];remaining=set(range(len(units)))
 while remaining:
  ready=sorted(i for i in remaining if all(d in order for d in dependencies[i]))
  if not ready:raise ValueError('private graph cycle before launch')
  order.extend(ready);remaining.difference_update(ready)
 for i in order:
  if any(d in blocked for d in dependencies[i]):blocked[i]='transitive-expansion-or-context-unavailable'
 root.mkdir(mode=0o700);artifacts={};results=[]
 for i in order:
  u=units[i];r=root/f'unit-{i}';r.mkdir(mode=0o700)
  if i in blocked:results.append(dict(index=i,standing='unavailable',reason=blocked[i],compilerLaunched=False));continue
  if any(d not in artifacts for d in dependencies[i]):results.append(dict(index=i,standing='incomplete',reason='dependency-analysis-or-metadata-incomplete',compilerLaunched=False));continue
  target=u['target'];plan=parsed[i];core=plan['core'];out=r/('lib'+target['name']+core.get('extra-filename','')+'.rmeta');argv=[wrapper_pin['path'],'--prepared-map',map_pin['path'],'--crate-type',core['--crate-type'],'--crate-name',target['name'],'--edition',target['edition'],'--sysroot',str(sysroot),'--emit',core['emit'],target['src_path'],'--out-dir',str(r),'-C','metadata='+core['metadata']]
  argv += plan['profileArguments'] + plan['checkCfgArguments']
  if core.get('incremental'):argv += ['-C','incremental='+str(r/'incremental')]
  if u['platform'] is not None:argv+=['--target',u['platform']]
  for f in u['features']:argv+=['--cfg','feature='+json.dumps(f,ensure_ascii=False)]
  supplied_externs=[]
  for d in u['dependencies']:
   artifact=artifacts[d['index']];checked(artifact);argv+=['--extern',d['extern_crate_name']+'='+artifact['path']];supplied_externs.append(dict(alias=d['extern_crate_name'],index=d['index'],artifact=artifact))
  closure=set(dependencies[i]);pending=list(closure)
  while pending:
   d=pending.pop()
   for child in dependencies[d]:
    if child not in closure:closure.add(child);pending.append(child)
  search_inputs=[]
  for d in sorted(closure):
   artifact=artifacts[d];checked(artifact);argv += ['-L','dependency='+str(Path(artifact['path']).parent)];search_inputs.append(dict(index=d,artifact=artifact))
  # Actual constructed package env/cwd/cap-lint DATA; full command/profile remains incomplete.
  # Actual static profile/check-cfg/cap args retained; source/output/search/extern paths rebound to checked prototype inputs.
  checked(context_pin)
  checked(wrapper_pin);checked(map_pin);stdout=os.open(r/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(r/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  try:observation=observe_root(argv,cwd=contexts[i]['cwd'],environment=contexts[i]['constructedEnvironment'],stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=30_000_000_000)
  finally:os.close(stdout);os.close(stderr)
  events=[json.loads(x) for x in (r/'stdout.log').read_text().splitlines() if x.startswith('{')];success=observation.returncode==0 and any(e['event']=='after_analysis' for e in events) and out.is_file()
  if success:raw=out.read_bytes();artifacts[i]=dict(path=str(out),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  record=dict(index=i,standing='analysis-and-metadata-completed' if success else 'incomplete',compilerLaunched=True,argv=argv,suppliedExterns=supplied_externs,transitiveMetadataSearchInputs=search_inputs,observationInformational=dataclasses.asdict(observation),events=events,metadata=artifacts.get(i),graphFeatures=u['features'],graphPlatform=u['platform'],fullCargoProfileEnvironment=False,packageContextData=contexts[i],contextPin=context_pin,actualStaticCommandData=plan,staticProfileCheckCfgArgumentsApplied=True,sourceOutputSearchExternBindingsReplaced=True,completeRuntimeCommand=False,actualConstructedPackageEnvironmentAndCwdUsed=True);results.append(record);(r/'result.json').write_text(json.dumps(record,indent=2)+'\n')
 result=dict(version=1,standing='EXPERIMENTAL ACTUAL STATIC PROFILE ARGUMENT ANALYSIS WITH REBOUND PRIVATE IO; NOT FULL NATIVE PROFILE',unitResults=results,rootResults=[next(x for x in results if x['index']==i) for i in roots],compilerChildren=sum(x['compilerLaunched'] for x in results),sourceMapPin=map_pin,wrapperPin=wrapper_pin,emptyChildEnvironment=False,constructedPackageEnvironmentAndCwdUsed=True,contextPin=context_pin,actualCompleteCargoProfile=False,callerPrototypeTimeoutSecondsNotLaw=30,procMacroBuildScriptOrApplicationExecuted=False,fullCargoProfileEnvironment=False,sourceMapBoundaryOnlyNotFullFilesystemConfinement=True,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False)
 (root/'result.json').write_text(json.dumps(result,indent=2)+'\n');return result
