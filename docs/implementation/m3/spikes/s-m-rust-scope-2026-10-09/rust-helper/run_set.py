from pathlib import Path
import os,subprocess,tempfile,time,json,statistics,hashlib,shutil
B=Path(__file__).resolve().parent;S=B.parent;os.setpriority(os.PRIO_PROCESS,0,10);parent=os.getpriority(os.PRIO_PROCESS,0);assert parent==10
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for ordinary scope measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-rsd-scope-measure-',dir=D)).resolve();T.chmod(0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));build=json.loads((B/'build.json').read_text());exe=Path(build['runtimePin']['path']);assert hashlib.sha256(exe.read_bytes()).hexdigest()==build['runtimePin']['sha256'];module=Path(build['modulePin']['path']);assert hashlib.sha256(module.read_bytes()).hexdigest()==build['modulePin']['sha256'];expected=json.loads((S/'results.json').read_text());results=[]
 for w in expected['workloads']:
  input_path=S/(w['id']+'-input.json');packet=json.loads(input_path.read_text());assert packet['heldOut']is False;raw=input_path.read_bytes();shutil.copyfile(input_path,B/input_path.name);runs=[];shape=None
  for n in range(10):
   out=B/f'{w["id"]}-{n}.stdout';err=B/f'{w["id"]}-{n}.stderr'
   with out.open('wb')as o,err.open('wb')as e:
    child=subprocess.Popen([str(exe),str(input_path)],cwd=T,env=env,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   assert child.returncode==0 and err.read_bytes()==b'';row=json.loads(out.read_text());elapsed=row.pop('elapsedNanos');assert type(elapsed)is int and elapsed>0;shape=row if shape is None else shape;assert row==shape;reference=w['actors'][0]['shape'];assert all(row[k]==reference[k]for k in row);rss=int(usage.ru_maxrss);assert 0<rss<2**64;runs.append(dict(ordinal=n,warmup=n<3,elapsedNanos=elapsed,observedChildNiceness=priority,exitCode=0,rssNative=rss,rssUnit='bytes',rssBytes=rss))
  values=[r['elapsedNanos']for r in runs[3:]];results.append(dict(id=w['id'],subjectCount=shape['subjectCount'],shape=shape,inputPin=dict(path=input_path.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),runs=runs,medianNanos=statistics.median(values),maxNanos=max(values),measuredPeakProcessRssBytes=max(r['rssBytes']for r in runs[3:]),allFieldsMatchBothIndependentPythonImplementations=True));print(w['id'],shape['subjectCount'],'Rust exacthelper10children agree',flush=True)
 assert hashlib.sha256(exe.read_bytes()).hexdigest()==build['runtimePin']['sha256'];assert hashlib.sha256(module.read_bytes()).hexdigest()==build['modulePin']['sha256'];report=dict(standing='UNREVIEWED optimized actual candidate private Rust helper measurements; synthetic observations and illustrative keys, no operational worker',workloads=results,children=110,observedParentNiceness=parent,runtimePin=build['runtimePin'],modulePin=build['modulePin'],privateTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,HOMEUnchanged=True,actualAcceptedTransportManifest=False,actualNativeWorker=False,coverageKeysValidatedC2Values=False,SM12FigureComplete=False,SM12PlaceholderFilled=False,SM14FigureComplete=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False);(B/'results.json').write_text(json.dumps(report,indent=2)+'\n')
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
