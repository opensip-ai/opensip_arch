from pathlib import Path
import os,json,hashlib,struct,tempfile,sys,time,dataclasses
B=Path('/tmp/opensip-implementation');V=B/'sm-cargo-unit-context-2026-10-10';BASE=B/'sm-graph-typecheck-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'bin-dependency-control-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10);sys.path.insert(0,str(V));sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality');from bin_context_graph_execution import execute_graph;from root_observation import observe_root
root=Path(tempfile.mkdtemp(prefix='opensip-sm-bin-dependency-control-',dir=O));root.chmod(0o700);project=root/'project';(project/'src').mkdir(parents=True);(project/'dep/src').mkdir(parents=True);(project/'Cargo.toml').write_text("[package]\nname='binary-with-dependency'\nversion='3.4.5'\nedition='2024'\n[dependencies]\nrenamed={package='dependency',path='dep'}\n");(project/'dep/Cargo.toml').write_text("[package]\nname='dependency'\nversion='1.2.3'\nedition='2024'\n");(project/'src/main.rs').write_text('fn main(){panic!("original fixture application must not execute");}\n');(project/'dep/src/lib.rs').write_text('compile_error!("original fixture source must not compile");\n')
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
originals=[]
for p in sorted(project.rglob('*')):
 if p.is_file():r=pin(p);r['path']=p.relative_to(project).as_posix();originals.append(r)
observation=root/'collector';observation.mkdir(mode=0o700);pp=root/'packet.json';pp.write_text(json.dumps(dict(observationRoot=str(observation),project=str(project),memberRoot=str(project),originalFiles=originals,configuration=None,overlayLinks=[],preserveOriginalLock=False),indent=2)+'\n');image=V/'check-target/debug/deps/cargo-820b7793ee1bc124';imagepin=pin(image);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME')
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for binary-dependency firstparty control lane',flush=True);time.sleep(5)
 env=dict(os.environ);env.update(TMPDIR=str(root),OPENSIP_EXPERIMENT_GRAPH_PACKET=str(pp));out=os.open(root/'collector.stdout',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);err=os.open(root/'collector.stderr',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:obs=observe_root([str(image),'util::context::experimental_unit_context::collect_explicit_experimental_corpus_graph','--exact','--ignored','--nocapture'],cwd=str(V/'producer'),environment=env,stdout_fd=out,stderr_fd=err,timeout_nanos=300_000_000_000)
 finally:os.close(out);os.close(err)
 outcome=json.loads((observation/'experiment-outcome.json').read_bytes());assert obs.returncode==0 and outcome['success'] and pin(image)==imagepin;graph=json.loads((observation/'unit-graph.json').read_bytes());assert len(graph['units'])==2;ctx=observation/'unit-context-data.json';build=json.loads((BASE/'build.json').read_bytes());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);cases=[]
 for name,main in [('actual-renamed-library-into-binary',b'fn main(){let _:u8=renamed::value();panic!("synthetic application must not execute");}'),('real-binary-type-error',b'fn main(){let _:bool=renamed::value();}')]:
  files={u['target']['src_path']:(b'pub fn value()->u8{7}' if u['target']['kind']==['lib'] else main) for u in graph['units']};raw=b'OPSMRUST1\0'+struct.pack('>Q',len(files))
  for source,content in sorted(files.items()):nb=source.encode();raw+=struct.pack('>Q',len(nb))+nb+struct.pack('>Q',len(content))+content
  mp=root/(name+'.map');mp.write_bytes(raw);r=execute_graph(graph,pin(mp),root/name,wrapper,build['sysroot'],root,pin(ctx));assert r['compilerChildren']==2;rr=r['rootResults'][0]
  if name.startswith('actual'):assert rr['standing']=='analysis-completed-binary' and rr['metadata'] is None and not rr['reusableLibraryMetadata']
  else:assert rr['standing']=='incomplete' and not rr['analysisCompleted']
  cases.append(dict(name=name,result=r,syntheticMap=pin(mp)))
 report=dict(standing='ACTUAL FIRSTPARTY CARGO BIN/LIB GRAPH; SYNTHETIC MAP TYPECHECK CONTROLS; NO APP/CORPUS USE',root=str(root),compiledCargoImage=imagepin,collectorRootInformational=dataclasses.asdict(obs),compilerQueries=len(list((observation/'queries').glob('query-*.arguments'))),graph=pin(observation/'unit-graph.json'),context=pin(ctx),controlsPassed=2,compilerChildren=4,cases=cases,applicationExecuted=False,actualCorpusUse=False,fullCargoProfileEnvironment=False,completeCompilerCommand=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n');print('Two bin/library controls pass/four compiler children; actual renamed edge and real binary type error, no main execution',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
