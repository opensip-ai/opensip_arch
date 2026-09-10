"""DRAFT SDK courier reference. Physical local files; no product/journal qualification."""
import hashlib,importlib.util,os,re,stat
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('broker_v3_bootstrap',P/'broker-bootstrap.model.v3.py');B=importlib.util.module_from_spec(s);s.loader.exec_module(B)
s=importlib.util.spec_from_file_location('courier_control_contract',P/'control-completion.check.v5.py');CONTROL=importlib.util.module_from_spec(s);s.loader.exec_module(CONTROL)
MAX_RESULT=16*1024*1024;MAX_SPAWN=64*1024*1024
REF=re.compile(r'rr:([0-9a-f]{32}):([0-9a-f]{64}):(0|[1-9][0-9]{0,7})\Z')
class CourierFailure(Exception):pass
class WriteHandle:__slots__=()
class ReadHandle:__slots__=()
def fail(reason):raise CourierFailure(reason)
def sha(data):return hashlib.sha256(data).hexdigest()
def exact_write(fd,data):
 view=memoryview(data)
 while view:
  n=os.write(fd,view)
  if n<=0:fail('STAGE.SHORT_WRITE')
  view=view[n:]
def file_read(fd,size):
 # Capacity is admitted before allocation. Never read a file-sized unbounded
 # buffer first and only afterwards compare against a limit.
 parts=[];remaining=size
 while remaining:
  chunk=os.read(fd,min(remaining,65536))
  if not chunk:fail('RESULT.INTEGRITY')
  parts.append(chunk);remaining-=len(chunk)
 if os.read(fd,1):fail('RESULT.INTEGRITY')
 return b''.join(parts)
def directory(path):
 fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
 st=os.fstat(fd)
 if st.st_uid!=os.geteuid() or stat.S_IMODE(st.st_mode)!=0o700:
  os.close(fd);fail('RESULT.SCRATCH_NOT_OWNED')
 return fd
class BrokerSDK:
 """Host-wired constructor and synchronous transport simulate Promise ordering.
 Public provider methods are only writeHostState/readProject and opaque arrays.
 """
 def __init__(self,environment,send,first_control_seq=1):
  self._send=send;self._next=first_control_seq;self._registry={};self._spent=set();self._pending={};self._result_ids=set();self._received=0;self._root=None;self._stage=None;self.trace=[]
  value=environment.pop(B.KEY,None)
  for k in list(environment):
   if k not in B.FIXED:del environment[k]
  if value is None:fail('BOOTSTRAP.MISSING')
  descriptor=B.parse(value)
  try:
   if descriptor['handles']:
    self._root=directory(descriptor['resultScratchRoot']);self.trace.append('open-result-directory')
    self._stage=os.open('stage',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self._root);st=os.fstat(self._stage)
    if st.st_uid!=os.geteuid() or stat.S_IMODE(st.st_mode)!=0o700:fail('STAGE.DIRECTORY_NOT_OWNED')
   for entry in descriptor['handles']:
    handle=WriteHandle() if entry['effectClass']=='HE-1' else ReadHandle();self._registry[handle]=dict(entry)
  except BaseException:
   self.close();raise
  self.hostStateWriteHandles=tuple(h for h in self._registry if type(h) is WriteHandle)
  self.projectReadHandles=tuple(h for h in self._registry if type(h) is ReadHandle)
 def close(self):
  for k in ['_stage','_root']:
   fd=getattr(self,k,None)
   if fd is not None:os.close(fd);setattr(self,k,None)
  self._registry.clear();self._pending.clear()
 def _lookup(self,h,kind):
  if type(h) is not kind or h not in self._registry:fail('SDK.UNKNOWN_LOCAL_HANDLE')
  if h in self._spent:fail('SDK.WRITE_HANDLE_ALREADY_USED')
  return self._registry[h]
 def _ref(self,ref):
  match=REF.fullmatch(ref) if isinstance(ref,str) else None
  if not match:fail('RESULT.REF_GRAMMAR')
  rid,digest,size=match.groups();size=int(size)
  if size>MAX_RESULT:fail('RESULT.OVER_CAP')
  return rid,digest,size
 def _exchange(self,h,entry):
  if not 1<=self._next<=9007199254740991:fail('SDK.SEQUENCE_EXHAUSTED')
  seq=self._next;self._next+=1;self._pending[seq]=(h,entry['effectClass'],entry['commitClass']);self.trace.append('request:'+str(seq))
  body={k:entry[k] for k in ['effectClass','authorizationRef','operationRef']}
  response=self._send(seq,body)
  if not isinstance(response,dict) or set(response)!={'type','body'} or response['type'] not in ['effectResult','refusal']:fail('SDK.INVALID_RESPONSE')
  envelope={'type':response['type'],'body':response['body'],'seq':1,'controlMajor':1}
  try:
   CONTROL.numbers(envelope)
   if not CONTROL.VALIDATORS[response['type']].is_valid(envelope):fail('SDK.INVALID_RESPONSE')
   CONTROL.utf8_bounds(envelope,CONTROL.SCHEMAS[response['type']])
  except (CONTROL.Refusal,RecursionError):fail('SDK.INVALID_RESPONSE')
  # The transport binding must perform ordinary control-schema/state/direction
  # validation before this private outcome dispatch. It is not a provider callback.
  if response.get('type')=='refusal':
   b=response.get('body',{})
   if set(b)-{'family','decisionClass','detail'} or b.get('family')!='RF-6' or b.get('decisionClass') not in ['PR-'+str(i) for i in range(1,10)]:fail('SDK.INVALID_REFUSAL')
   self._pending.pop(seq);self.close();return {'kind':'REFUSED','decisionClass':b['decisionClass']},None
  b=response.get('body',{})
  if response.get('type')!='effectResult' or b.get('requestSeq')!=seq or self._pending.get(seq)!=(h,entry['effectClass'],entry['commitClass']):fail('RESULT.REQUEST_SEQ_MISMATCH')
  if b.get('commitClass')!=entry['commitClass']:fail('RESULT.COMMIT_CLASS_MISMATCH')
  if not all(type(b.get(k)) is int and 1<=b[k]<=9007199254740991 for k in ['decisionSeq','outcomeSeq']) or b['decisionSeq']>=b['outcomeSeq']:fail('RESULT.OUTCOME_SEQUENCE')
  if b.get('effectOutcome') not in ['COMPLETED','FAILED','INDETERMINATE']:fail('RESULT.EFFECT_OUTCOME')
  self._pending.pop(seq)
  if b['effectOutcome']!='COMPLETED':return {'kind':b['effectOutcome'],'commitClass':b['commitClass']},None
  return None,b
 def writeHostState(self,handle,data):
  entry=self._lookup(handle,WriteHandle)
  if not isinstance(data,(bytes,bytearray,memoryview)):fail('SDK.BYTES_REQUIRED')
  if isinstance(data,memoryview) and (data.itemsize!=1 or data.ndim!=1):fail('SDK.BYTES_REQUIRED')
  if len(data)>MAX_RESULT:fail('STAGE.OVER_CAP')
  data=bytes(data);name=entry['authorizationRef'][3:]+'.bin';self._spent.add(handle)
  fd=None
  try:
   fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600,dir_fd=self._stage);self.trace.append('stage-create')
   exact_write(fd,data);os.fsync(fd);self.trace.append('stage-sync')
  except OSError as e:raise CourierFailure('STAGE.IO') from e
  finally:
   if fd is not None:os.close(fd);self.trace.append('stage-close')
  result,outcome=self._exchange(handle,entry)
  if result is not None:return result
  rid,digest,size=self._ref(outcome.get('resultRef'))
  if size!=len(data) or digest!=sha(data):fail('RESULT.RECEIPT_MISMATCH')
  self.trace.append('receipt-only-no-file-read')
  return {'kind':'COMPLETED','commitClass':outcome['commitClass']}
 def readProject(self,handle):
  entry=self._lookup(handle,ReadHandle);result,outcome=self._exchange(handle,entry)
  if result is not None:return result
  rid,digest,size=self._ref(outcome.get('resultRef'))
  if rid in self._result_ids:fail('RESULT.REPLAYED_ID')
  if self._received+size>MAX_SPAWN:fail('RESULT.SPAWN_CAP_EXCEEDED')
  st=os.fstat(self._root)
  if st.st_uid!=os.geteuid() or stat.S_IMODE(st.st_mode)!=0o700:fail('RESULT.SCRATCH_NOT_OWNED')
  fd=None
  try:
   # NONBLOCK makes FIFO/device replacement a controlled admission refusal;
   # regular files are unaffected. No source/project path is ever opened here.
   fd=os.open(rid+'.bin',os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK,dir_fd=self._root);self.trace.append('result-open')
   st=os.fstat(fd)
   if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or st.st_uid!=os.geteuid() or st.st_size!=size:fail('RESULT.FILE_NOT_ADMITTED')
   data=file_read(fd,size)
  except FileNotFoundError as e:raise CourierFailure('RESULT.ABSENT') from e
  except OSError as e:raise CourierFailure('RESULT.IO') from e
  finally:
   if fd is not None:os.close(fd)
  if sha(data)!=digest:fail('RESULT.INTEGRITY')
  self._received+=size;self._result_ids.add(rid);return {'kind':'COMPLETED','bytes':data}

class ReferenceResultPublisher:
 """Single host writer for physical HE-2 result publication, design only.
 Caller has already proved exact sealed membership and both grant scopes.
 """
 def __init__(self,root_fd):self.root_fd=root_fd;self.charged_bytes=0;self.events=[]
 def publish(self,result_id,data):
  if re.fullmatch('[0-9a-f]{32}',result_id) is None:fail('RESULT.ID')
  if len(data)>MAX_RESULT or self.charged_bytes+len(data)>MAX_SPAWN:
   self.events.append('FAILED-BEFORE-PUBLICATION');return {'effectOutcome':'FAILED'}
  # Reservation is monotonic for this spawn, including uncertain publication;
  # no automatic reuse following an I/O failure.
  self.charged_bytes+=len(data);self.events.append('CAP-CHARGED')
  temp=result_id+'.pending';name=result_id+'.bin';fd=None
  try:
   try:os.stat(name,dir_fd=self.root_fd,follow_symlinks=False)
   except FileNotFoundError:pass
   else:fail('RESULT.ID_REUSED')
   fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o400,dir_fd=self.root_fd);exact_write(fd,data);os.fsync(fd);os.close(fd);fd=None
   os.rename(temp,name,src_dir_fd=self.root_fd,dst_dir_fd=self.root_fd);os.fsync(self.root_fd);self.events.append('PUBLISHED')
  finally:
   if fd is not None:os.close(fd)
  return {'effectOutcome':'COMPLETED','resultRef':'rr:'+result_id+':'+sha(data)+':'+str(len(data))}
