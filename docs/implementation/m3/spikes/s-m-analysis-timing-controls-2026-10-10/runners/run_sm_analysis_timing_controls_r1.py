from pathlib import Path
import json,hashlib,os,sys,tempfile,struct,time,dataclasses
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-analysis-timing-2026-10-10';dest=V/'controls-r1.json';assert not dest.exists();build=json.loads((V/'build.json').read_bytes());image=Path(build['executable']);assert len(image.read_bytes())==build['bytes'] and hashlib.sha256(image.read_bytes()).hexdigest()==build['sha256'];sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality');from root_observation import observe_root
O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');root=Path(tempfile.mkdtemp(prefix='opensip-sm-analysis-time-controls-',dir=O));root.chmod(0o700);outside=root/'outside-canary.bin';outside.write_bytes(b'firstparty disk canary must stay outside prepared map');main='/synthetic/main"β.rs';payload='/synthetic/payload.bin';lane=O/'opensip-lanes.lock';owned=False;records=[];home=os.environ.get('HOME')
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def prepared(rows):
 rows=sorted(rows.items(),key=lambda r:r[0].encode());return b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(struct.pack('>Q',len(n.encode()))+n.encode()+struct.pack('>Q',len(b))+b for n,b in rows)
programs=[('quoted-unicode-text-and-binary-read',{main:b'pub fn answer()->usize{include_bytes!("payload.bin").len()}',payload:b'abcd'},True),('real-type-error',{main:b'pub fn answer()->u8{"wrong"}'},False),('existing-disk-file-denied',{main:('pub const DATA:&[u8]=include_bytes!(r#"'+str(outside)+'"#);').encode()},False)]
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary analysis instrumentation control lane',flush=True);time.sleep(5)
 for n,(name,rows,success) in enumerate(programs):
  r=root/name;r.mkdir(mode=0o700);mp=r/'source.map';mp.write_bytes(prepared(rows));output=r/'libcontrol.rmeta';argv=[str(image),'--prepared-map',str(mp),'--crate-type','lib','--crate-name','control','--edition','2024','--sysroot',build['sysroot'],'--emit','metadata',main,'-o',str(output),'-C','metadata=timed_control_'+str(n)];out=os.open(r/'stdout',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);err=os.open(r/'stderr',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  try:obs=observe_root(argv,cwd=r,environment={'TMPDIR':str(root)},stdout_fd=out,stderr_fd=err,timeout_nanos=30_000_000_000)
  finally:os.close(out);os.close(err)
  events=[json.loads(line) for line in (r/'stdout').read_text().splitlines()];assert events[0]['event']=='analysis_span_started' and events[0]['mapDecodingExcluded'] and events[0]['instrumentationIncluded'];reads=[e for e in events if e['event']=='prepared_source_read'];assert any(e['normalizedPath']==main and e['contentBytes']==len(rows[main]) and not e['binary'] and e['preparedMapEntryPresent'] for e in reads);analyses=[e for e in events if e['event']=='after_analysis'];assert (obs.returncode==0)==success
  if success:
   assert len(analyses)==1 and 0<analyses[0]['analysisElapsedNanos']<=obs.root_reaped_elapsed_nanos and output.stat().st_size>0;assert any(e['normalizedPath']==payload and e['contentBytes']==4 and e['binary'] and e['preparedMapEntryPresent'] for e in reads);assert (r/'stderr').read_bytes()==b''
  else:assert not output.exists() and obs.returncode!=0 and (r/'stderr').stat().st_size>0
  if name=='existing-disk-file-denied':assert any(e['normalizedPath']==str(outside) and not e['preparedMapEntryPresent'] and e['contentBytes'] is None for e in reads)
  records.append(dict(name=name,successExpected=success,argv=argv,sourceMap=pin(mp),rootObservation=dataclasses.asdict(obs),events=events,metadata=pin(output) if output.exists() else None))
 report=dict(standing='NEW FIRSTPARTY TIMED THROUGH-ANALYSIS AND PREPARED SOURCE OBSERVATION CONTROLS; UNREVIEWED; NO CORPUS',root=str(root),controlsPassed=3,compilerChildren=3,records=records,compiledImage=dict(path=str(image),bytes=build['bytes'],sha256=build['sha256']),driverSource=pin(V/'driver.rs'),acceptedParentSource=pin(B/'sm-graph-typecheck-2026-10-10/driver.rs'),mapDecodingExcludedFromAnalysisInterval=True,observerInstrumentationIncluded=True,metadataSysrootRuntimeReadsSealed=False,actualCorpusUse=False,repositoryCodeExecuted=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n');print('Three new timing/read controls pass; one successful analysis interval plus actual type and read-boundary failures retained.',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
