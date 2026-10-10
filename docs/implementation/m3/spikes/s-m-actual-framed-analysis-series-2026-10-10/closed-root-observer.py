"""Caller-owned experimental framed stdin root; no whole-tree or peak qualification."""
from dataclasses import dataclass
import os,sys,stat,json,hashlib,struct,selectors,subprocess,time,signal
@dataclass(frozen=True)
class FramedRootObservation:
 pid:int|None
 returncode:int|None
 root_reaped_elapsed_nanos:int|None
 rss_native:int|None
 launch_errno:int|None
 timed_out:bool
 worker_ready_elapsed_nanos:int|None
 map_wire_verified_elapsed_nanos:int|None
 map_decode_complete_elapsed_nanos:int|None
 wire_bytes_written:int
 source_map_whole_sha256:str
def observe_framed_root(argv,*,cwd,environment,stdout_fd,stderr_fd,timeout_nanos,map_pin):
 assert sys.platform=='darwin' and type(timeout_nanos) is int and timeout_nanos>0
 assert type(argv) in [list,tuple] and argv and os.path.isabs(argv[0]) and all(type(a) is str and '\0' not in a for a in argv)
 assert type(environment) is dict and 'HOME' not in environment and all(type(k) is str and type(v) is str and k and '=' not in k and '\0' not in k and '\0' not in v for k,v in environment.items())
 fd=os.open(map_pin['path'],os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);source=os.fdopen(fd,'rb')
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode);h=hashlib.sha256();count=0
  while b:=source.read(1<<20):h.update(b);count+=len(b)
  assert count==map_pin['bytes'] and h.hexdigest()==map_pin['sha256'];source.seek(0)
 except BaseException:source.close();raise
 def frames():
  header=json.dumps(dict(format='OPSMRUST1',bytes=count,sha256=map_pin['sha256']),sort_keys=True,separators=(',',':')).encode();yield struct.pack('>I',len(header))+header
  streamed=hashlib.sha256();length=0
  while chunk:=source.read(1<<20):streamed.update(chunk);length+=len(chunk);yield struct.pack('>I',len(chunk))+chunk
  after=os.fstat(fd);assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns);assert length==count and streamed.hexdigest()==map_pin['sha256']
 start=time.monotonic_ns();child=None;reaped=False;ready=None;verified=None;decoded=None;written=0;timed_out=False;usage=None;returncode=None;reaped_ns=None;pending=None;output=bytearray();sel=selectors.DefaultSelector()
 try:
  try:child=subprocess.Popen(argv,cwd=cwd,env=environment,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr_fd,close_fds=True,start_new_session=True,bufsize=0)
  except OSError as e:return FramedRootObservation(None,None,None,None,e.errno,False,None,None,None,0,map_pin['sha256'])
  os.set_blocking(child.stdin.fileno(),False);os.set_blocking(child.stdout.fileno(),False);sel.register(child.stdout,selectors.EVENT_READ,'stdout');iterator=frames();stdout_eof=False
  while not reaped or not stdout_eof:
   remaining=timeout_nanos-(time.monotonic_ns()-start)
   if remaining<=0:
    timed_out=True
    if not reaped:
     os.kill(child.pid,signal.SIGKILL);pid,status,usage=os.wait4(child.pid,0);assert pid==child.pid;returncode=os.waitstatus_to_exitcode(status);reaped=True;reaped_ns=time.monotonic_ns()-start
    break
   for key,_ in sel.select(min(remaining/1e9,0.02)):
    if key.data=='stdin':
     if pending is None:
      try:pending=memoryview(next(iterator))
      except StopIteration:sel.unregister(child.stdin);child.stdin.close();continue
     try:n=os.write(child.stdin.fileno(),pending)
     except BlockingIOError:continue
     except BrokenPipeError:sel.unregister(child.stdin);child.stdin.close();continue
     assert n>0;written+=n;pending=pending[n:]
     if not pending:pending=None
    else:
     try:data=os.read(child.stdout.fileno(),1<<20)
     except BlockingIOError:continue
     if not data:sel.unregister(child.stdout);stdout_eof=True;continue
     view=memoryview(data)
     while view:n=os.write(stdout_fd,view);assert n>0;view=view[n:]
     output.extend(data)
     while b'\n' in output:
      line,_,tail=output.partition(b'\n');output=bytearray(tail);event=json.loads(line)
      if ready is None:
       assert event==dict(event='transfer_ready');ready=time.monotonic_ns()-start;sel.register(child.stdin,selectors.EVENT_WRITE,'stdin')
      elif event['event']=='prepared_map_wire_verified':
       assert event['mapSha256']==map_pin['sha256'] and event['mapBytes']==count;verified=time.monotonic_ns()-start
      elif event['event']=='analysis_span_started':decoded=time.monotonic_ns()-start
   if not reaped:
    try:pid,status,observed=os.wait4(child.pid,os.WNOHANG)
    except InterruptedError:continue
    if pid:assert pid==child.pid;usage=observed;returncode=os.waitstatus_to_exitcode(status);reaped=True;reaped_ns=time.monotonic_ns()-start
  child.returncode=returncode;assert usage is not None and type(usage.ru_maxrss) is int and 0<=usage.ru_maxrss<=2**64-1
  return FramedRootObservation(child.pid,returncode,reaped_ns,usage.ru_maxrss,None,timed_out,ready,verified,decoded,written,map_pin['sha256'])
 finally:
  if child is not None:
   if not reaped:
    os.kill(child.pid,signal.SIGKILL);os.wait4(child.pid,0)
   for stream in [child.stdin,child.stdout]:
    if not stream.closed:stream.close()
  sel.close();source.close()
