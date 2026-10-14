import sys,struct,json,hashlib,time
# U-2c SM-7 receiver VARIANT r2: the accepted receiver.py snapshot phase unchanged (manifest frame and content frames,
# <= 1 MiB), then a dependency-source phase in NE section 3.2/9.2 order with JSON payloads (no CBOR conformance claimed):
# DependencySourceManifest {dependencySourceSetId, entries[{packageKey, path, byteLength, contentSha256}]} (one frame,
# <= maxFramePayloadBytes 64 MiB), raw content chunks <= maxDependencySourceChunkBytes 1 MiB, then DependencySourceSeal
# {dependencySourceSetId, manifestSha256, entryCount, totalBytes, totalChunkCount}. The seal must equal the receiver's own
# computation (manifestSha256 over the exact manifest frame bytes received); the response echoes it (DependencySourceAccepted).
CAP=1048576;FRAME=67108864;f=sys.stdin.buffer
def exact(n):
 out=bytearray()
 while len(out)<n:
  part=f.read(n-len(out))
  if not part:raise ValueError('truncated frame')
  out.extend(part)
 return bytes(out)
def frame(cap):
 n=struct.unpack('>I',exact(4))[0]
 if n>cap:raise ValueError('oversized frame')
 return exact(n)
def content(rows,size_key,digest_key):
 chunks=0;total=0
 for row in rows:
  left=row[size_key];assert type(left)is int and left>=0;h=hashlib.sha256()
  while left:
   part=frame(CAP);chunks+=1
   if not part or len(part)>left:raise ValueError('invalid content frame length')
   h.update(part);left-=len(part);total+=len(part)
  if h.hexdigest()!=row[digest_key]:raise ValueError('content digest mismatch')
 return chunks,total
print('ready',flush=True);start=time.monotonic_ns();manifest=json.loads(frame(CAP));assert isinstance(manifest,list)
paths=[r['path']for r in manifest];assert paths==sorted(set(paths),key=lambda x:x.encode('utf8'))
snapChunks,snapBytes=content(manifest,'bytes','sha256')
raw=frame(FRAME);dm=json.loads(raw);entries=dm['entries'];assert set(dm)=={'dependencySourceSetId','entries'} and len(entries)<=1000000
keys=[];seen=set()
for e in entries:
 assert set(e)=={'packageKey','path','byteLength','contentSha256'} and (e['packageKey'],e['path'])not in seen;seen.add((e['packageKey'],e['path']))
 if not keys or keys[-1]!=e['packageKey']:assert e['packageKey']not in keys;keys.append(e['packageKey'])
assert len(keys)<=4096 and sum(e['byteLength']for e in entries)<=8589934592
depChunks,depBytes=content(entries,'byteLength','contentSha256')
seal=json.loads(frame(CAP));mine=dict(dependencySourceSetId=dm['dependencySourceSetId'],manifestSha256=hashlib.sha256(raw).hexdigest(),entryCount=len(entries),totalBytes=depBytes,totalChunkCount=depChunks)
if seal!=mine:raise ValueError('seal mismatch')
if f.read(1):raise ValueError('trailing bytes')
print(json.dumps(dict(rows=len(manifest),contentBytes=snapBytes,snapshotFrames=1+snapChunks,dependencyPackages=len(keys),dependencyManifestBytes=len(raw),dependencyFrames=2+depChunks,frames=1+snapChunks+2+depChunks,accepted=seal,receiverNanos=time.monotonic_ns()-start,allDigestsVerified=True)),flush=True)
