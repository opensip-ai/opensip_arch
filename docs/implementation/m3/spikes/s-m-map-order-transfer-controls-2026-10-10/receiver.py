"""Outside-product framed source-map transfer probe, with no source execution or writes."""
import sys,struct,json,hashlib
MAX_FRAME=1<<20
MAX_ROWS=100_000
MAX_CONTENT=8<<30
MAX_DESCRIPTOR=4<<20

def exact(stream,n):
 out=bytearray()
 while len(out)<n:
  b=stream.read(n-len(out))
  if not b:raise ValueError('truncated input')
  out.extend(b)
 return bytes(out)
def frame(stream):
 n=struct.unpack('>I',exact(stream,4))[0]
 if not 0<n<=MAX_FRAME:raise ValueError('frame bound')
 return exact(stream,n)
class MapStream:
 def __init__(self,stream):self.stream=stream;self.buffer=b'';self.bytes=0;self.digest=hashlib.sha256();self.frames=0
 def read(self,n):
  out=bytearray()
  while len(out)<n:
   if not self.buffer:self.buffer=frame(self.stream);self.frames+=1
   take=min(n-len(out),len(self.buffer));b=self.buffer[:take];self.buffer=self.buffer[take:];out.extend(b);self.digest.update(b);self.bytes+=take
  return bytes(out)
 def u64(self):return struct.unpack('>Q',self.read(8))[0]
def receive(stream):
 header=json.loads(frame(stream).decode('utf8'));assert header['format']=='OPSMRUST1';assert type(header['bytes']) is int and header['bytes']>=18;assert isinstance(header['sha256'],str) and len(header['sha256'])==64
 data=MapStream(stream);assert data.read(10)==b'OPSMRUST1\0';count=data.u64()
 if count>MAX_ROWS:raise ValueError('inventory row bound')
 rows=[];total=0;seen=set();descriptor_size=2
 for _ in range(count):
  name_len=data.u64()
  if name_len>MAX_DESCRIPTOR:raise ValueError('descriptor path cannot fit')
  rawname=data.read(name_len);name=rawname.decode('utf8')
  if rawname in seen:raise ValueError('source map duplicate path')
  seen.add(rawname);length=data.u64();total+=length
  if total>MAX_CONTENT:raise ValueError('content total bound')
  digest=hashlib.sha256();left=length
  while left:
   b=data.read(min(left,MAX_FRAME));digest.update(b);left-=len(b)
  row=dict(path=name,bytes=length,sha256=digest.hexdigest());encoded=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();descriptor_size+=len(encoded)+(1 if rows else 0)
  if descriptor_size>MAX_DESCRIPTOR:raise ValueError('descriptor bound')
  rows.append(row)
 if data.buffer or stream.read(1):raise ValueError('trailing input')
 if data.bytes!=header['bytes'] or data.digest.hexdigest()!=header['sha256']:raise ValueError('whole map pin differs')
 rows.sort(key=lambda row:row['path'].encode('utf8'))
 descriptor=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert len(descriptor)==descriptor_size
 return dict(rows=count,contentBytes=total,mapBytes=data.bytes,mapSha256=data.digest.hexdigest(),descriptorBytes=len(descriptor),descriptorSha256=hashlib.sha256(descriptor).hexdigest(),contentFrames=data.frames,largestAllowedFrameBytes=MAX_FRAME,descriptorIdentity='EXPERIMENTAL ABSOLUTE PATH ROW ARRAY; NOT ADMITTED SNAPSHOT2',sourceAuthentication=False,nativeAdmission=False,repositoryCodeExecuted=False,sourceBytesWrittenToDisk=False,SMComplete=False)
if __name__=='__main__':
 try:print(json.dumps(receive(sys.stdin.buffer),sort_keys=True))
 except Exception as error:print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(2)
