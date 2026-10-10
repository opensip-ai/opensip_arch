"""Outside-product dependency-only fragment; supplied retained records are not admission."""
import hashlib,types
from snapshot_receiver import uint,exact,path,digest,HarnessRefusal
MAX_ENTRIES=1_000_000
MAX_PACKAGES=4096
MAX_TOTAL_BYTES=8589934592
MAX_CHUNK_BYTES=1048576
class Receiver:
 def __init__(self,encoder,set_id,expected):
  self.encode=encoder;self.set_id=set_id;self.expected=expected;self.state='manifest';self.files={};self.entries=[];self.position=0;self.chunk_index=0;self.current=bytearray();self.total=0;self.chunks=0
 def manifest(self,value):
  try:
   if self.state!='manifest':raise HarnessRefusal('manifest phase')
   exact(value,['dependencySourceSetId','entries','manifestSha256'])
   if value['dependencySourceSetId']!=self.set_id:raise HarnessRefusal('set association')
   digest(value['manifestSha256']);entries=value['entries']
   if type(entries) is not list or len(entries)>MAX_ENTRIES:raise HarnessRefusal('entry bound')
   if hashlib.sha256(self.encode(entries)).hexdigest()!=value['manifestSha256']:raise HarnessRefusal('DT-MD1 entries digest')
   seen=set();packages=set();declared=0
   for row in entries:
    exact(row,['packageKey','path','byteLength','contentSha256']);pkg=row['packageKey'];p=path(row['path']);length=uint(row['byteLength']);digest(row['contentSha256'])
    if type(pkg) is not str or not pkg.startswith('pkg1-'):raise HarnessRefusal('NKC package spelling')
    digest(pkg[5:]);key=(pkg,p)
    if key in seen or self.expected.get(key)!=(length,row['contentSha256']):raise HarnessRefusal('membership/duplicate')
    if any((pkg,'/'.join(p.split('/')[:i])) in self.expected for i in range(1,len(p.split('/')))):raise HarnessRefusal('VFS ancestor collision')
    seen.add(key);packages.add(pkg);declared+=length
    if declared>MAX_TOTAL_BYTES or len(packages)>MAX_PACKAGES:raise HarnessRefusal('dependency aggregate bound')
   if seen!=set(self.expected):raise HarnessRefusal('complete membership')
   self.entries=[dict(r) for r in entries];self.manifest_sha=value['manifestSha256'];self.state='chunks';self._empty()
  except Exception:self.state='failed';raise
 def _empty(self):
  while self.position<len(self.entries) and self.entries[self.position]['byteLength']==0:
   row=self.entries[self.position]
   if row['contentSha256']!=hashlib.sha256(b'').hexdigest():raise HarnessRefusal('empty digest')
   self.files[(row['packageKey'],row['path'])]=b'';self.position+=1
 def chunk(self,value):
  try:
   if self.state!='chunks' or self.position>=len(self.entries):raise HarnessRefusal('chunk phase')
   exact(value,['dependencySourceSetId','packageKey','path','chunkIndex','byteOffset','bytes']);row=self.entries[self.position]
   if value['dependencySourceSetId']!=self.set_id or value['packageKey']!=row['packageKey'] or value['path']!=row['path'] or uint(value['chunkIndex'])!=self.chunk_index or uint(value['byteOffset'])!=len(self.current):raise HarnessRefusal('chunk association/order')
   raw=value['bytes']
   if type(raw) is not bytes or not 1<=len(raw)<=MAX_CHUNK_BYTES:raise HarnessRefusal('chunk bytes')
   if len(raw)>row['byteLength']-len(self.current) or self.total+len(raw)>MAX_TOTAL_BYTES or self.chunks==2**64-1 or self.chunk_index==2**64-1:raise HarnessRefusal('chunk aggregate')
   self.current.extend(raw);self.total+=len(raw);self.chunks+=1;self.chunk_index+=1
   if len(self.current)==row['byteLength']:
    if hashlib.sha256(self.current).hexdigest()!=row['contentSha256']:raise HarnessRefusal('file digest')
    self.files[(row['packageKey'],row['path'])]=bytes(self.current);self.current=bytearray();self.position+=1;self.chunk_index=0;self._empty()
  except Exception:self.state='failed';raise
 def seal(self,value):
  try:
   if self.state!='chunks' or self.position!=len(self.entries) or self.current:raise HarnessRefusal('incomplete dependency')
   exact(value,['dependencySourceSetId','manifestSha256','entryCount','totalBytes','totalChunkCount'])
   for key in ['entryCount','totalBytes','totalChunkCount']:uint(value[key])
   expected=dict(dependencySourceSetId=self.set_id,manifestSha256=self.manifest_sha,entryCount=len(self.entries),totalBytes=self.total,totalChunkCount=self.chunks)
   if value!=expected:raise HarnessRefusal('seal association/aggregates')
   self.state='accepted'
   mounted={'.opensip/deps/v2/'+pkg+'/'+p:raw for (pkg,p),raw in self.files.items()}
   return dict(expected),types.MappingProxyType(mounted)
  except Exception:self.state='failed';raise
