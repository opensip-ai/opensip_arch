from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib,statistics
# Sized SM-9 complete replay series r2: the ROWS-TRANSPORT VARIANT of the closed release replay driver (7635c002...,
# built from the git-archive export of product 37581132 with the accepted lock and recipe) over the rows form of each
# labelled synthetic lower-bound packet. Series r1 (the closed e82a4e2f image) is retained: it refused every selected
# packet over the product canonical 4 MiB MAX_BYTES (first at 678) while parsing the whole packet as one document.
# Same recipe as r1 and the accepted run_release_set.py: 3 warmups + 7 runs, priority 10, lane held for the whole set.
os.setpriority(os.PRIO_PROCESS,0,10);parent_nice=os.getpriority(os.PRIO_PROCESS,0);assert parent_nice==10
H=Path(__file__).resolve().parent;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
V=Path('/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13')
pin=json.loads((V/'build-release.json').read_text());binary=Path(pin['executable'])
def check_binary():raw=binary.read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']=='7635c002b2ed877f89582360b6eae54e8de1a6c91811a4f188b083919609fc24'
conv={json.loads(l)['sourceSha256']:json.loads(l) for l in (V/'convert.log').read_text().splitlines()}
packets=json.loads((H/'sized-packets-r1.json').read_text());dest=H/'sized-replay-results-r2.json';assert not dest.exists();home=os.environ.get('HOME')
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for replay measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-sized-replay-r2-',dir=D)).resolve();T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for k in ['HOME','LANG','LC_ALL','TZ']:
  if k in os.environ:env[k]=os.environ[k]
 sets=[]
 for count in sorted(int(c) for c in packets['packets']):
  row=packets['packets'][str(count)];sel=Path(row['path']);assert hashlib.sha256(sel.read_bytes()).hexdigest()==row['sha256'];c=conv[row['sha256']];assert c['sourceSha256']==row['sha256'] and c['reassemblesEqual'] is True
  packet=Path(c['rows']);raw=packet.read_bytes();assert len(raw)==c['bytes'] and hashlib.sha256(raw).hexdigest()==c['sha256'];check_binary();runs=[]
  for n in range(10):
   out=H/f'replay-r2-{count}-{n}.stdout';err=H/f'replay-r2-{count}-{n}.stderr';start=time.monotonic_ns()
   with out.open('wb') as o,err.open('wb') as e:
    child=subprocess.Popen([str(binary),str(packet)],cwd=T,env=env,stdout=o,stderr=e);child_nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert child_nice==10;_,status,usage=os.wait4(child.pid,0);code=os.waitstatus_to_exitcode(status)
   end=time.monotonic_ns();assert code==0,(count,n,err.read_text());r=json.loads(out.read_text());assert r['fullReplayPassed'] is True and r['findings']==count;rss=int(usage.ru_maxrss);assert 0<=rss<2**64
   r.update(ordinal=n,observedChildNiceness=child_nice,warmup=n<3,wholeProcessNanos=end-start,rssNative=rss,rssUnit='bytes',rssBytes=rss);runs.append(r)
  values=[r['completeReplayNanos'] for r in runs if not r['warmup']];assert hashlib.sha256(packet.read_bytes()).hexdigest()==c['sha256'];check_binary()
  sets.append(dict(count=count,packet=row,rows=c,runs=runs,medianReplayNanos=statistics.median(values),maxReplayNanos=max(values),medianWholeProcessNanos=statistics.median(r['wholeProcessNanos'] for r in runs if not r['warmup'])))
  dest.write_text(json.dumps(dict(standing='UNREVIEWED PRELIMINARY SIZED NATIVE COMPLETE REPLAY (ROWS-TRANSPORT VARIANT); LABELLED SYNTHETIC LOWER-BOUND GRAPHS; NOT COMPILER FACT VOLUMES',binary=pin,sizes=packets['sizes'],sets=sets,
       host='lead macOS preliminary, not D12',TMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,observedParentNiceness=parent_nice,resetLabel='fresh process per sample; no page-cache record; no Q0 9.2 cold label claimed',
       SM9LowerBoundOnly=True,SM9FigureComplete=False,FComputed=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False),indent=2)+'\n')
  print(count,'median ms',statistics.median(values)/1e6,flush=True)
finally:
 if owned:lock.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
