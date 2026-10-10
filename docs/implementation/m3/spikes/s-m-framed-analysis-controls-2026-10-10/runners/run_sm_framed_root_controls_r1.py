from pathlib import Path
import os,json,hashlib,struct,tempfile,time,sys,dataclasses
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-framed-analysis-2026-10-10';sys.path.insert(0,str(V));from framed_root_observation import observe_framed_root
O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';root=Path(tempfile.mkdtemp(prefix='opensip-sm-framed-root-controls-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');assert not (V/'root-controls-r1.json').exists();build=json.loads((V/'build.json').read_bytes());image=build['executable'];records=[]
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def map_bytes(text):name=b'/synthetic/main.rs';return b'OPSMRUST1\0'+struct.pack('>Q',1)+struct.pack('>Q',len(name))+name+struct.pack('>Q',len(text))+text
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary framed root control lane',flush=True);time.sleep(5)
 for name in ['successful-framed-library','real-type-error','owned-root-timeout','actual-launch-error','corrupt-map-pin-before-launch']:
  r=root/name;r.mkdir(mode=0o700);mp=r/'source.map';mp.write_bytes(map_bytes(b'pub fn f()->u8 { "bad" }' if name=='real-type-error' else b'pub fn f()->u8 { 1 }'));map_pin=pin(mp);out=r/'libcontrol.rmeta';argv=[image,'--prepared-map-framed-stdin','--crate-type','lib','--crate-name','control','--edition','2024','--sysroot',str(SYS),'--emit','metadata','/synthetic/main.rs','-o',str(out)];timeout=30_000_000_000
  if name=='owned-root-timeout':argv=[PY,'-I','-B','-c','import time; print(\'{"event":"transfer_ready"}\',flush=True); time.sleep(10)'];timeout=100_000_000
  if name=='actual-launch-error':argv=[str(root/'absent-image')]
  if name=='corrupt-map-pin-before-launch':map_pin=dict(map_pin,sha256='0'*64)
  stdout=os.open(r/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(r/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);observation=None;refused=False
  try:
   try:observation=observe_framed_root(argv,cwd=root,environment={'TMPDIR':str(root)},stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=timeout,map_pin=map_pin)
   except AssertionError:
    assert name=='corrupt-map-pin-before-launch';refused=True
  finally:os.close(stdout);os.close(stderr)
  events=[json.loads(line) for line in (r/'stdout.log').read_bytes().splitlines()];after=[e for e in events if e['event']=='after_analysis']
  if name=='successful-framed-library':assert observation.returncode==0 and out.is_file() and len(after)==1 and 0<observation.worker_ready_elapsed_nanos<observation.map_wire_verified_elapsed_nanos<=observation.map_decode_complete_elapsed_nanos<=observation.root_reaped_elapsed_nanos and after[0]['analysisElapsedNanos']>0
  elif name=='real-type-error':assert observation.returncode!=0 and not out.exists() and not after and observation.map_wire_verified_elapsed_nanos is not None
  elif name=='owned-root-timeout':assert observation.timed_out and observation.returncode==-9 and observation.root_reaped_elapsed_nanos>0 and observation.rss_native is not None and observation.worker_ready_elapsed_nanos is not None
  elif name=='actual-launch-error':assert observation.pid is None and observation.launch_errno==2 and observation.root_reaped_elapsed_nanos is None and observation.rss_native is None
  else:assert refused and observation is None and (r/'stdout.log').read_bytes()==b''
  records.append(dict(name=name,argv=argv,sourceMap=pin(mp),suppliedMapPin=map_pin,observation=dataclasses.asdict(observation) if observation else None,refusedBeforeLaunch=refused,events=events,metadata=pin(out) if out.exists() else None));print(dict(control=name,returncode=observation.returncode if observation else None,refusedBeforeLaunch=refused),flush=True)
 (V/'root-controls-r1.json').write_text(json.dumps(dict(root=str(root),controlsPassed=5,childProcesses=3,compilerInvocations=2,completedAnalyses=1,ownedTimeoutChildren=1,launchErrors=1,prelaunchPinRefusals=1,records=records,source=pin(V/'framed_root_observation.py'),actualCorpusUse=False,wholeTreeSettlement=False,physicalPeakScratchMeasured=False,SMComplete=False),indent=2)+'\n')
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
