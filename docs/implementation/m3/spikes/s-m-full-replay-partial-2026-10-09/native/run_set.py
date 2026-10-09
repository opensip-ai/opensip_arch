from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib,statistics
os.setpriority(os.PRIO_PROCESS,0,10)
parent_nice=os.getpriority(os.PRIO_PROCESS,0)
assert parent_nice==10
B=Path(__file__).resolve().parent;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for native replay measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-native-set-',dir=D)).resolve();T.chmod(0o700);pin=json.loads((B/'build.json').read_text());binary=Path(pin['executable']);raw=binary.read_bytes();assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'];packet=B/'packet-193-selected.json';packet_sha=hashlib.sha256(packet.read_bytes()).hexdigest();env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for k in ['HOME','LANG','LC_ALL','TZ']:
  if k in os.environ:env[k]=os.environ[k]
 rows=[]
 for n in range(10):
  out=B/f'native-193-{n}.stdout';err=B/f'native-193-{n}.stderr';start=time.monotonic_ns()
  with out.open('wb')as o,err.open('wb')as e:
   child=subprocess.Popen([str(binary),str(packet)],cwd=T,env=env,stdout=o,stderr=e);child_nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert child_nice==10;_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
  end=time.monotonic_ns();assert child.returncode==0,(n,err.read_text());row=json.loads(out.read_text());assert row['fullReplayPassed']is True and row['findings']==193;rss=int(usage.ru_maxrss);assert 0<=rss<2**64;row.update(ordinal=n,observedChildNiceness=child_nice,warmup=n<3,wholeProcessNanos=end-start,rssNative=rss,rssUnit='bytes',rssBytes=rss,exitCode=0);rows.append(row);assert len({(r['objects'],r['blobs'],r['findings'])for r in rows})==1
  values=[r['completeReplayNanos']for r in rows if not r['warmup']];report=dict(standing='UNREVIEWED PRELIMINARY NATIVE FULL REPLAY193SYNTHETIC SOURCES/FINDINGS; NO FULLSM9 OR QUALIFICATION',runs=rows,medianReplayNanos=statistics.median(values)if values else None,maxReplayNanos=max(values)if values else None,synthetic=True,profile='current product replay owner,unoptimizeddebugmeasurementdriver',sizing='193distinct configured files in acceptednapi-rs exploratorycohort; synthetic1fact/1finding perfile; not realcompilerfactvolumes',packetSha256=packet_sha,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,observedParentNiceness=parent_nice,nicenessEstablishedBy="Explicit parent setpriority/readback10 before subprocess; direct child readback10 immediately after Popen; no extra nice adjustment",SM9PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False)
  (B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(f'native complete replay{n+1}/10: {row["completeReplayNanos"]}ns,{row["findings"]}reconstructedfindings',flush=True)
 assert hashlib.sha256(packet.read_bytes()).hexdigest()==packet_sha and hashlib.sha256(binary.read_bytes()).hexdigest()==pin['sha256']
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
