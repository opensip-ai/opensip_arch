import sys,struct,json,hashlib,time
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
print('ready',flush=True);start=time.monotonic_ns();manifest=json.loads(frame());assert isinstance(manifest,list)
paths=[r['path']for r in manifest];assert paths==sorted(set(paths),key=lambda x:x.encode('utf8'))
total=0;frames=1
for row in manifest:
 left=row['bytes'];assert type(left)is int and left>=0;h=hashlib.sha256()
 while left:
  part=frame();frames+=1
  if not part or len(part)>left:raise ValueError('invalid content frame length')
  h.update(part);left-=len(part);total+=len(part)
 if h.hexdigest()!=row['sha256']:raise ValueError('content digest mismatch')
if f.read(1):raise ValueError('trailing bytes')
print(json.dumps(dict(rows=len(manifest),contentBytes=total,frames=frames,receiverNanos=time.monotonic_ns()-start,allDigestsVerified=True)),flush=True)
