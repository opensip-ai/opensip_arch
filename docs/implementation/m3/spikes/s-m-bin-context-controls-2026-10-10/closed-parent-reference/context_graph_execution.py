from pathlib import Path
import json,hashlib,os,struct,dataclasses,sys
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

def execute_graph(graph,map_pin,output_root,wrapper_pin,sysroot,cwd,context_pin):
 # Supplied graph/map/runtime locations are experimental input, never native capabilities.
 context=json.loads(checked(context_pin));units_input=graph['units']
 if context.get('version')!=1 or len(context.get('units',[]))!=len(units_input):raise ValueError('supplied context population differs')
 contexts=context['units']
 for i,(u,row) in enumerate(zip(units_input,contexts)):
  if row['index']!=i or type(row['index']) is not int:raise ValueError('supplied context index differs')
  for field,key in [('packageId','pkg_id'),('target','target'),('profile','profile'),('platform','platform'),('mode','mode'),('features','features')]:
   if row[field]!=u[key]:raise ValueError('supplied context graph join differs')
  env=row['constructedEnvironment']
  if not isinstance(env,dict) or 'HOME' in env or any(not isinstance(k,str) or not k or '=' in k or '\0' in k or not isinstance(value,str) or '\0' in value for k,value in env.items()):raise ValueError('supplied environment DATA shape')
  if row['capLintArguments'] not in [[],['--cap-lints','allow'],['--cap-lints','warn']]:raise ValueError('outside pinned Cargo cap-lint DATA shape')
  path=row['cwd']
  if not isinstance(path,str) or not Path(path).is_absolute() or str(Path(path))!=path:raise ValueError('supplied package cwd DATA shape')
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
  target=u['target'];out=r/('lib'+target['name']+'.rmeta');argv=[wrapper_pin['path'],'--prepared-map',map_pin['path'],'--crate-type','lib','--crate-name',target['name'],'--edition',target['edition'],'--sysroot',str(sysroot),'--emit','metadata',target['src_path'],'-o',str(out),'-C',f'metadata=experiment_unit_{i}']
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
  argv += contexts[i]['capLintArguments']
  checked(context_pin)
  checked(wrapper_pin);checked(map_pin);stdout=os.open(r/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(r/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  try:observation=observe_root(argv,cwd=contexts[i]['cwd'],environment=contexts[i]['constructedEnvironment'],stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=30_000_000_000)
  finally:os.close(stdout);os.close(stderr)
  events=[json.loads(x) for x in (r/'stdout.log').read_text().splitlines() if x.startswith('{')];success=observation.returncode==0 and any(e['event']=='after_analysis' for e in events) and out.is_file()
  if success:raw=out.read_bytes();artifacts[i]=dict(path=str(out),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  record=dict(index=i,standing='analysis-and-metadata-completed' if success else 'incomplete',compilerLaunched=True,argv=argv,suppliedExterns=supplied_externs,transitiveMetadataSearchInputs=search_inputs,observationInformational=dataclasses.asdict(observation),events=events,metadata=artifacts.get(i),graphFeatures=u['features'],graphPlatform=u['platform'],fullCargoProfileEnvironment=False,packageContextData=contexts[i],contextPin=context_pin,actualConstructedPackageEnvironmentAndCwdUsed=True);results.append(record);(r/'result.json').write_text(json.dumps(record,indent=2)+'\n')
 result=dict(version=1,standing='EXPERIMENTAL GRAPH-INDEXED METADATA ANALYSIS; NOT FULL NATIVE PROFILE',unitResults=results,rootResults=[next(x for x in results if x['index']==i) for i in roots],compilerChildren=sum(x['compilerLaunched'] for x in results),sourceMapPin=map_pin,wrapperPin=wrapper_pin,emptyChildEnvironment=False,constructedPackageEnvironmentAndCwdUsed=True,contextPin=context_pin,actualCompleteCargoProfile=False,callerPrototypeTimeoutSecondsNotLaw=30,procMacroBuildScriptOrApplicationExecuted=False,fullCargoProfileEnvironment=False,sourceMapBoundaryOnlyNotFullFilesystemConfinement=True,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False)
 (root/'result.json').write_text(json.dumps(result,indent=2)+'\n');return result
