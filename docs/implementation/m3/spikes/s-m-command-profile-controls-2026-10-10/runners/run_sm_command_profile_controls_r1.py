from pathlib import Path
import os,json,hashlib,struct,tempfile,sys,time,copy
B=Path('/tmp/opensip-implementation');V=B/'sm-command-data-2026-10-10';BASE=B/'sm-graph-typecheck-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'command-profile-controls-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10);sys.path.insert(0,str(V));from command_profile_graph_execution import execute_graph
S=B/'sm-command-data-controls-r1-stage';fixtures=[]
for i in [0,2]:
 at=S/f'actual-controls/{i}/observation';fixtures.append(dict(context=json.loads((at/'unit-command-data.json').read_bytes()),graph=json.loads((at/'unit-graph.json').read_bytes())))
local,dep=fixtures;build=json.loads((BASE/'build.json').read_bytes());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);root=Path(tempfile.mkdtemp(prefix='opensip-sm-command-profile-controls-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');records=[]
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def run(name,fixture,programs,mutate=None,refusal=False):
 g=copy.deepcopy(fixture['graph']);c=copy.deepcopy(fixture['context'])
 if mutate:mutate(g,c)
 path=root/(name+'.context.json');path.write_text(json.dumps(c,indent=2)+'\n');files={u['target']['src_path']:programs[u['target']['name']] for u in g['units']};raw=b'OPSMRUST1\0'+struct.pack('>Q',len(files))
 for source,content in sorted(files.items()):n=source.encode();raw+=struct.pack('>Q',len(n))+n+struct.pack('>Q',len(content))+content
 mp=root/(name+'.map');mp.write_bytes(raw);out=root/name
 try:r=execute_graph(g,pin(mp),out,wrapper,build['sysroot'],root,pin(path))
 except ValueError as e:
  assert refusal and not out.exists();records.append(dict(name=name,refusedBeforeLaunch=True,error=str(e),compilerChildren=0,context=pin(path),syntheticMap=pin(mp)));return
 assert not refusal;records.append(dict(name=name,result=r,context=pin(path),syntheticMap=pin(mp)));return r
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary static profile control lane',flush=True);time.sleep(5)
 program=b'#![deny(unexpected_cfgs)]\n#[cfg(not(feature="chosen"))]compile_error!("feature missing");const _:()=assert!(cfg!(debug_assertions));const _:()=assert!(env!("CARGO_PRIMARY_PACKAGE").as_bytes()[0]==b\'1\');pub fn value()->u8{7}'
 r=run('actual-profile-feature-primary-package',local,{'command_profile':program});assert r['compilerChildren']==1 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
 r=run('actual-check-cfg-lint-refusal',local,{'command_profile':b'#![deny(unexpected_cfgs)]\n#[cfg(feature="not_declared")]pub fn nope(){}'});assert r['compilerChildren']==1 and r['rootResults'][0]['standing']=='incomplete'
 r=run('actual-renamed-library-primary-join',dep,{'command_app':b'const _:()=assert!(env!("CARGO_PRIMARY_PACKAGE").as_bytes()[0]==b\'1\');pub fn value()->u8{renamed::value()}','command_dependency':b'const _:()=assert!(option_env!("CARGO_PRIMARY_PACKAGE").is_none());pub fn value()->u8{7}'});assert r['compilerChildren']==2 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
 run('codegen-plugin-flag-prelaunch',local,{'command_profile':program},lambda g,c:c['units'][0]['arguments'].extend(['-Z','codegen-backend=/owned-prototype-unused']),True)
 def wrong_alias(g,c):
  r=next(row for row in c['units'] if row.get('constructedEnvironment',{}).get('CARGO_PKG_NAME')=='command-app');i=r['arguments'].index('--extern')+1;r['arguments'][i]='wrong='+r['arguments'][i].split('=',1)[1]
 run('wrong-extern-alias-prelaunch',dep,{'command_app':b'pub fn v(){}','command_dependency':b'pub fn value()->u8{7}'},wrong_alias,True)
 run('HOME-environment-prelaunch',local,{'command_profile':program},lambda g,c:c['units'][0]['constructedEnvironment'].update(HOME=str(root)),True)
 report=dict(standing='NEW FIRSTPARTY SYNTHETIC MAP CONTROLS APPLYING ACTUAL STATIC CARGO PROFILE ARGUMENT DATA; UNREVIEWED; NO CORPUS',root=str(root),controlsPassed=6,compilerChildren=sum(r.get('result',{}).get('compilerChildren',0) for r in records),records=records,executorPin=pin(V/'command_profile_graph_execution.py'),wrapperPin=wrapper,actualStaticProfileCheckCfgArgumentsApplied=True,operationalSourceOutputSearchExternBindingsReplaced=True,newCargoSource=False,newRustWrapper=False,actualCorpusUse=False,applicationExecuted=False,completeRuntimeCommand=False,fullCargoProfileEnvironment=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False);assert report['compilerChildren']==4;dest.write_text(json.dumps(report,indent=2)+'\n');print('Six actual static profile controls pass; four analysis children, no corpus/application use.',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
