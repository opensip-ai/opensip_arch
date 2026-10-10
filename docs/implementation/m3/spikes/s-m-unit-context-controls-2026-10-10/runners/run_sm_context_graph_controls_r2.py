from pathlib import Path
import os,json,hashlib,struct,tempfile,sys,re,time,copy
B=Path('/tmp/opensip-implementation');V=B/'sm-cargo-unit-context-2026-10-10';BASE=B/'sm-graph-typecheck-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'context-graph-controls-r2.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10);sys.path.insert(0,str(V));from context_graph_execution import execute_graph
build=json.loads((BASE/'build.json').read_bytes());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);roots=[Path(x) for x in re.findall(r'ACTUAL_UNIT_CONTEXT_CONTROL=(\S+)',(V/'unit-context-controls-r4.log').read_text())];assert len(roots)==4;fixtures=[]
for root in roots:
 at=root/'observation' if (root/'observation').exists() else root
 fixtures.append(dict(root=root,at=at,context=json.loads((at/'unit-context-data.json').read_bytes()),graph=json.loads((at/'unit-graph.json').read_bytes())))
local=next(x for x in fixtures if len(x['context']['units'])==1 and x['context']['units'][0]['constructedEnvironment']['CARGO_PKG_NAME']=='unit-context');registry=next(x for x in fixtures if any(r['constructedEnvironment']['CARGO_PKG_NAME']=='opensip-fixture-dep' for r in x['context']['units']));root=Path(tempfile.mkdtemp(prefix='opensip-sm-context-graph-controls-',dir=O));root.chmod(0o700);records=[];lane=O/'opensip-lanes.lock';owned=False
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def run(name,fixture,programs,mutate=None,refusal=False):
 g=copy.deepcopy(fixture['graph']);c=copy.deepcopy(fixture['context']);path=root/(name+'.context.json')
 if mutate:mutate(g,c)
 path.write_text(json.dumps(c,indent=2)+'\n');files={u['target']['src_path']:programs[u['target']['name']] for u in g['units']};encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(files))
 for source,content in sorted(files.items()):nb=source.encode();encoded+=struct.pack('>Q',len(nb))+nb+struct.pack('>Q',len(content))+content
 m=root/(name+'.map');m.write_bytes(encoded);out=root/name
 try:r=execute_graph(g,pin(m),out,wrapper,build['sysroot'],root,pin(path))
 except ValueError as e:
  assert refusal and not out.exists();records.append(dict(name=name,refusedBeforeLaunch=True,error=str(e),compilerChildren=0));return
 assert not refusal;records.append(dict(name=name,result=r));return r
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for isolated context compiler lane',flush=True);time.sleep(5)
 program=b'pub const VERSION:&str=env!("CARGO_PKG_VERSION");pub const NAME:&str=env!("CARGO_CRATE_NAME");const _:()=assert!(env!("CARGO_PKG_VERSION").as_bytes()[0]==b\'2\');const _:()=assert!(option_env!("HOME").is_none());'
 r=run('actual-package-environment',local,{'selected_lib':program});assert r['compilerChildren']==1 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
 r=run('actual-registry-cap-and-renamed-edge',registry,{'opensip_fixture_dep':b'#![deny(warnings)]\npub fn chosen()->u8{let unused=0;7}', 'app':b'pub fn value()->u8{renamed::chosen()}'});assert r['compilerChildren']==2 and r['rootResults'][0]['standing']=='analysis-and-metadata-completed'
 r=run('local-warning-denial-retained',local,{'selected_lib':b'#![deny(warnings)]\npub fn value()->u8{let unused=0;7}'});assert r['compilerChildren']==1 and r['rootResults'][0]['standing']=='incomplete'
 run('wrong-package-join-prelaunch',local,{'selected_lib':program},lambda g,c:c['units'][0].update(packageId='wrong'),True)
 run('wrong-index-prelaunch',local,{'selected_lib':program},lambda g,c:c['units'][0].update(index=1),True)
 run('invalid-env-prelaunch',local,{'selected_lib':program},lambda g,c:c['units'][0]['constructedEnvironment'].update({'BAD=KEY':'no'}),True)
 run('HOME-setting-prelaunch',local,{'selected_lib':program},lambda g,c:c['units'][0]['constructedEnvironment'].update({'HOME':str(root)}),True)
 report=dict(standing='NEW FIRSTPARTY SYNTHETIC SOURCE MAP CONTROLS WITH ACTUAL CARGO CONTEXT DATA; NO CORPUS USE',controlsPassed=7,compilerChildren=sum(x.get('result',{}).get('compilerChildren',0) for x in records),records=records,root=str(root),mapContentsSyntheticFirstparty=True,actualConstructedPackageEnvironmentCwdCapLintsUsed=True,closedWrapperUnchanged=True,closedGraphExecutorUnchanged=True,completeCompilerCommand=False,fullCargoProfileEnvironment=False,actualCorpusTypecheck=False,nativeAdmission=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,SMComplete=False);assert report['compilerChildren']==4;dest.write_text(json.dumps(report,indent=2)+'\n');print('Seven context controls pass/four compiler children; no corpus use',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
