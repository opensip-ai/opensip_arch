from pathlib import Path
import os,json,hashlib,tempfile,stat,sys,time,struct,copy,dataclasses
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-framed-bin-profile-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'controls-r1.json';assert not dest.exists();st=json.loads((C/'CURRENT-STATE.json').read_bytes())
for field,stage,review in [('SMFramedAnalysisControlsPublication','sm-framed-analysis-controls-r1-stage','grok-sm-framed-analysis-controls-r1'),('SMBinContextControlsPublication','sm-bin-context-controls-r1-stage','grok-sm-bin-context-controls-r1'),('SMOriginalRustflagsControlsPublication','sm-original-rustflags-controls-r1-stage','grok-sm-original-rustflags-controls-r1')]:
 pub=st[field];r=json.loads((B/'reviews'/review/'review.json').read_bytes());assert r['verdict']=='ACCEPT' and r['requiredFindings']==[] and r['subjectManifestSha256']==pub['subjectManifest']['sha256']==hashlib.sha256((B/stage/'subject.json').read_bytes()).hexdigest()
source=json.loads((B/'sm-original-rustflags-controls-r1-stage/source.json').read_bytes());closed=json.loads((B/'sm-framed-analysis-2026-10-10/build.json').read_bytes());wrapper=dict(path=closed['executable'],bytes=closed['bytes'],sha256=closed['sha256'])
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def checked(p,row):assert {k:pin(p)[k] for k in ['bytes','sha256']}=={k:row[k] for k in ['bytes','sha256']}
for f in source['finalSourcePins']:checked(Path(source['isolatedProducer'])/f['path'],f)
checked(Path(source['compiledCargoImage']['path']),source['compiledCargoImage']);checked(Path(wrapper['path']),wrapper)
root=Path(tempfile.mkdtemp(prefix='opensip-sm-framed-bin-profile-controls-',dir=O));root.chmod(0o700);project=root/'project';(project/'src').mkdir(parents=True);(project/'.cargo').mkdir();(project/'Cargo.toml').write_text('[package]\nname="framed-original-profile"\nversion="1.0.0"\nedition="2024"\n[lib]\nname="original_library"\n[[bin]]\nname="hyphenated-app"\npath="src/main.rs"\n[lints.rust]\nunexpected_cfgs={level="deny",check-cfg=["cfg(tokio_unstable)"]}\n');(project/'src/lib.rs').write_text('compile_error!("fixture must never compile in static collector");\n');(project/'src/main.rs').write_text('compile_error!("fixture must never compile in static collector");\n');cfg=project/'.cargo/config.toml';cfg.write_text('[env]\nMACOSX_DEPLOYMENT_TARGET="12.0"\nCARGO_WORKSPACE_DIR={value="",relative=true}\n[target.aarch64-apple-darwin]\nrustflags=["-Cforce-frame-pointers=yes","-C","force-unwind-tables=yes","-C","symbol-mangling-version=v0","-C","link-args=-Wl,-undefined,dynamic_lookup","-Aunknown_lints"]\n[target.\'cfg(all())\']\nrustflags=["--cfg","tokio_unstable","-Aclippy::all"]\n')
originals=[]
for p in sorted(project.rglob('*')):
 if p.is_file():row=pin(p);row['path']=p.relative_to(project).as_posix();originals.append(row)
observation=root/'collector';observation.mkdir(mode=0o700);packet=dict(observationRoot=str(observation),project=str(project),memberRoot=str(project),originalFiles=originals,configuration=pin(cfg),overlayLinks=[],preserveOriginalConfiguration=True,preserveOriginalLock=False);pp=root/'packet.json';pp.write_text(json.dumps(packet,indent=2)+'\n');lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');records=[];sys.path.insert(0,str(V));from framed_bin_profile_graph_execution import execute_graph;sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality');from root_observation import observe_root
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary framed binary/profile controls lane',flush=True);time.sleep(5)
 env=dict(os.environ,TMPDIR=str(root),OPENSIP_EXPERIMENT_GRAPH_PACKET=str(pp));argv=[source['compiledCargoImage']['path'],'util::context::experimental_command_data::collect_explicit_experimental_corpus_graph','--exact','--ignored','--nocapture'];stdout=os.open(root/'collector.stdout',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(root/'collector.stderr',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:collector=observe_root(argv,cwd=source['isolatedProducer'],environment=env,stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=60_000_000_000)
 finally:os.close(stdout);os.close(stderr)
 outcome=json.loads((observation/'experiment-outcome.json').read_bytes());assert collector.returncode==0 and outcome['success'];graph=json.loads((observation/'unit-graph.json').read_bytes());context=json.loads((observation/'unit-command-data.json').read_bytes());assert len(graph['units'])==2 and len(graph['roots'])==2
 program_library=b'#![deny(unexpected_cfgs)]\n#[cfg(not(tokio_unstable))]compile_error!("original cfg missing");pub fn value()->u8{7}\n';program_binary=b'#![deny(unexpected_cfgs)]\n#[cfg(not(tokio_unstable))]compile_error!("original cfg missing");fn main(){let _:u8=original_library::value();std::fs::write("application-sentinel",b"must not execute").unwrap();}\n'
 def run(name,program,mutate=None,refuse=False):
  g=copy.deepcopy(graph);c=copy.deepcopy(context)
  if mutate:mutate(g,c)
  cp=root/(name+'.context.json');cp.write_text(json.dumps(c,indent=2)+'\n');raw=b'OPSMRUST1\0'+struct.pack('>Q',len(g['units']))
  for u in g['units']:
   source_name=u['target']['src_path'].encode();content=program_library if u['target']['kind']==['lib'] else program;raw+=struct.pack('>Q',len(source_name))+source_name+struct.pack('>Q',len(content))+content
  mp=root/(name+'.map');mp.write_bytes(raw);out=root/name
  try:result=execute_graph(g,pin(mp),out,wrapper,closed['sysroot'],root,pin(cp))
  except ValueError as e:
   assert refuse and not out.exists();records.append(dict(name=name,refusedBeforeLaunch=True,error=str(e),compilerChildren=0,context=pin(cp),syntheticMap=pin(mp)));return None
  assert not refuse
  for child in result['unitResults']:
   if child.get('compilerLaunched'):
    events=child['events'];wire=next(e for e in events if e['event']=='prepared_map_wire_verified');assert wire['mapSha256']==pin(mp)['sha256']
  assert not (project/'application-sentinel').exists();records.append(dict(name=name,result=result,context=pin(cp),syntheticMap=pin(mp)));return result
 result=run('framed-binary-original-config-and-library-join',program_binary);assert result['compilerChildren']==2;binary=next(r for r in result['unitResults'] if r['packageContextData']['target']['kind']==['bin']);library=next(r for r in result['unitResults'] if r['packageContextData']['target']['kind']==['lib']);assert library['reusableLibraryMetadata'] is True and library['metadata']['bytes']>0;assert binary['standing']=='analysis-completed-binary' and binary['analysisCompleted'] is True and binary['metadata'] is None and binary['reusableLibraryMetadata'] is False
 result=run('framed-binary-real-type-error',b'fn main(){let _:bool=original_library::value();}\n');assert result['compilerChildren']==2;assert next(r for r in result['rootResults'] if r['packageContextData']['target']['kind']==['bin'])['standing']=='incomplete'
 def wrong_name(g,c):
  row=next(r for r in c['units'] if r['target']['kind']==['bin']);row['constructedEnvironment']['CARGO_CRATE_NAME']='wrong';row['arguments'][row['arguments'].index('--crate-name')+1]='wrong'
 run('wrong-static-binary-crate-name',program_binary,wrong_name,True)
 run('operational-codegen-backend-refusal',program_binary,lambda g,c:c['units'][0]['arguments'].extend(['-Ccodegen-backend=/synthetic/never-read']),True)
 run('unregistered-feature-cfg-refusal',program_binary,lambda g,c:c['units'][0]['arguments'].extend(['--cfg','feature="forged"']),True)
 run('HOME-environment-refusal',program_binary,lambda g,c:c['units'][0]['constructedEnvironment'].update(HOME=str(root)),True)
 receipt=dict(standing='NEW SIX FRAMED BINARY AND ORIGINAL CONFIG PROFILE DATA CONTROLS; UNREVIEWED; NO ACTUAL CORPUS',root=str(root),controlsPassed=6,collectorRoots=1,collectorInformationQueries=len(list((observation/'queries').glob('query-*.arguments'))),compilerChildren=sum(r.get('result',{}).get('compilerChildren',0) for r in records),records=records,collectorObservationInformational=dataclasses.asdict(collector),collectorImage=source['compiledCargoImage'],executorPin=pin(V/'framed_bin_profile_graph_execution.py'),closedRootObserverPin=pin(V/'framed_root_observation.py'),closedWrapperPin=wrapper,originalFlagArgumentsAndCfgValuesPreserved=True,successfulBinaryNotReusableMetadata=True,closedSourcesAndImagesUnchanged=True,niceness=os.getpriority(os.PRIO_PROCESS,0),ownedLane=True,privateTMPDIR=str(root),HOMEUnchanged=os.environ.get('HOME')==home,newCargoSource=False,newRustWrapper=False,acceptedControlsRerun=False,actualCorpusUse=False,applicationExecuted=False,buildScriptOrProcMacroExecuted=False,fullCargoProfileEnvironment=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False);dest.write_text(json.dumps(receipt,indent=2)+'\n');print('Six framed binary/original profile controls passed',receipt['compilerChildren'],'analysis children',receipt['collectorInformationQueries'],'INFOqueries',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
