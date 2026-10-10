from pathlib import Path
import os,json,hashlib,struct,tempfile,sys,time,dataclasses
B=Path('/tmp/opensip-implementation');V=B/'sm-cargo-unit-context-2026-10-10';BASE=B/'sm-graph-typecheck-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'bin-context-control-r2.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10);sys.path.insert(0,str(V));sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality');from bin_context_graph_execution import execute_graph;from root_observation import observe_root
root=Path(tempfile.mkdtemp(prefix='opensip-sm-bin-context-control-',dir=O));root.chmod(0o700);project=root/'project';(project/'src').mkdir(parents=True);source=b'fn main(){panic!("application must never execute");}\n';(project/'src/main.rs').write_bytes(source);(project/'Cargo.toml').write_text("[package]\nname='hyphenated-binary'\nversion='3.4.5'\nedition='2024'\n")
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
originals=[]
for p in sorted(project.rglob('*')):
 if p.is_file():row=pin(p);row['path']=p.relative_to(project).as_posix();originals.append(row)
observation=root/'collector';observation.mkdir(mode=0o700);packet=dict(observationRoot=str(observation),project=str(project),memberRoot=str(project),originalFiles=originals,configuration=None,overlayLinks=[],preserveOriginalLock=False);pp=root/'packet.json';pp.write_text(json.dumps(packet,indent=2)+'\n');image=V/'check-target/debug/deps/cargo-820b7793ee1bc124';imagepin=pin(image);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME')
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for binary firstparty control lane',flush=True);time.sleep(5)
 env=dict(os.environ);env.update(TMPDIR=str(root),OPENSIP_EXPERIMENT_GRAPH_PACKET=str(pp));out=os.open(root/'collector.stdout',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);err=os.open(root/'collector.stderr',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);argv=[str(image),'util::context::experimental_unit_context::collect_explicit_experimental_corpus_graph','--exact','--ignored','--nocapture']
 try:result=observe_root(argv,cwd=str(V/'producer'),environment=env,stdout_fd=out,stderr_fd=err,timeout_nanos=300_000_000_000)
 finally:os.close(out);os.close(err)
 outcome=json.loads((observation/'experiment-outcome.json').read_bytes());assert result.returncode==0 and outcome['success'];assert pin(image)==imagepin
 graph=json.loads((observation/'unit-graph.json').read_bytes());ctx=observation/'unit-context-data.json';assert len(graph['units'])==1 and graph['units'][0]['target']['kind']==['bin'];assert (project/'src/main.rs').read_bytes()==source
 name=graph['units'][0]['target']['src_path'].encode();program=b'const _:()=assert!(env!("CARGO_PKG_VERSION").as_bytes()[0]==b\'3\');fn main(){panic!("synthetic application must never execute");}'
 encoded=b'OPSMRUST1\0'+struct.pack('>Q',1)+struct.pack('>Q',len(name))+name+struct.pack('>Q',len(program))+program;mp=root/'synthetic.map';mp.write_bytes(encoded);build=json.loads((BASE/'build.json').read_bytes());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);execution=execute_graph(graph,pin(mp),root/'binary-analysis',wrapper,build['sysroot'],root,pin(ctx));report=dict(standing='FIRSTPARTY BINARY THROUGH-ANALYSIS CONTROL; SYNTHETIC MAP/NO APPLICATION EXECUTION; UNREVIEWED',root=str(root),actualCargoImage=imagepin,collectorRootInformational=dataclasses.asdict(result),collectorOutcome=outcome,compilerQueries=len(list((observation/'queries').glob('query-*.arguments'))),graph=pin(observation/'unit-graph.json'),context=pin(ctx),result=execution,syntheticMap=pin(mp),originalFixtureSourcePreserved=True,applicationExecuted=False,actualCorpusUse=False,completeCompilerCommand=False,fullCargoProfileEnvironment=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n');assert execution['compilerChildren']==1 and execution['rootResults'][0]['standing']=='analysis-completed-binary' and execution['rootResults'][0]['metadata'] is None and execution['rootResults'][0]['reusableLibraryMetadata'] is False;print('Actual firstparty Cargo binary graph and synthetic through-analysis complete, empty emission file not reusable library metadata; main not executed',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
