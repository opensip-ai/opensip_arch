import sys,struct,json,hashlib,time
# U-2c SM-7 receiver VARIANT: the accepted receiver.py snapshot phase unchanged, then a dependency-source phase: one
# canonical DependencySourceSetV1 descriptor frame, then per descriptor package one canonical file-manifest frame
# ([{path, contentSha256, byteLength}]) and its content frames. Every content digest and each package's file count and
# total bytes are checked against the manifest and descriptor. Frames are u32 big-endian length, <= 1 MiB.
CAP=1048576
f=sys.stdin.buffer
def exact(n):
 out=bytearray()
 while len(out)<n:
  part=f.read(n-len(out))
  if not part:raise ValueError('truncated frame')
  out.extend(part)
 return bytes(out)
def frame():
 n=struct.unpack('>I',exact(4))[0]
 if n>CAP:raise ValueError('oversized frame')
 return exact(n)
def content(rows,size_key,digest_key):
 global frames,total
 for row in rows:
  left=row[size_key];assert type(left)is int and left>=0;h=hashlib.sha256()
  while left:
   part=frame();frames+=1
   if not part or len(part)>left:raise ValueError('invalid content frame length')
   h.update(part);left-=len(part);total+=len(part)
  if h.hexdigest()!=row[digest_key]:raise ValueError('content digest mismatch')
print('ready',flush=True);start=time.monotonic_ns();manifest=json.loads(frame());assert isinstance(manifest,list);frames=1;total=0
paths=[r['path']for r in manifest];assert paths==sorted(set(paths),key=lambda x:x.encode('utf8'))
content(manifest,'bytes','sha256');snapshotBytes=total
descriptor=json.loads(frame());frames+=1;assert descriptor['language']=='rust' and descriptor['completeness']['state']=='complete';depFiles=0
for p in descriptor['packages']:
 rows=json.loads(frame());frames+=1;paths=[r['path']for r in rows];assert paths==sorted(set(paths),key=lambda x:x.encode('utf8'))
 assert len(rows)==p['fileCount'] and sum(r['byteLength']for r in rows)==p['totalBytes']
 content(rows,'byteLength','contentSha256');depFiles+=len(rows)
if f.read(1):raise ValueError('trailing bytes')
print(json.dumps(dict(rows=len(manifest),contentBytes=snapshotBytes,dependencyPackages=len(descriptor['packages']),dependencyFiles=depFiles,dependencyBytes=total-snapshotBytes,frames=frames,receiverNanos=time.monotonic_ns()-start,allDigestsVerified=True)),flush=True)
