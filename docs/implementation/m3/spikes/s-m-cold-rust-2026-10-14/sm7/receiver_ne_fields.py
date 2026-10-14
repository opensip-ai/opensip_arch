import sys,struct,json,hashlib,time
# U-2c SM-7 receiver VARIANT r3 (Codex SM-U2C-R1-RF-01): the accepted receiver.py snapshot phase (checks factored into
# content(), not verbatim), then the dependency-source phase with every NE section 9.2 field (JSON headers; no CBOR or
# protocol conformance claimed):
# - DependencySourceManifest {dependencySourceSetId, manifestSha256, entries[{packageKey, path, byteLength, contentSha256}]}
#   in one frame <= maxFramePayloadBytes 64 MiB. NE describes manifestSha256 as the digest of the manifest frame as sent,
#   which a frame cannot contain about itself; this variant's representation (lead decision, disclosed): SHA-256 of the
#   canonical JSON of the manifest payload with the manifestSha256 member omitted. The receiver recomputes it.
# - DependencySourceChunk {dependencySourceSetId, packageKey, path, chunkIndex, byteOffset, bytes}: frame payload =
#   u32 BE header length + canonical JSON header (the five non-bytes fields) + raw bytes (1..1 MiB, <= the entry's
#   remaining bytes). chunkIndex and byteOffset are per entry from 0 and must be contiguous; chunks follow manifest order;
#   a zero-length entry has no chunk (as the accepted snapshot phase).
# - DependencySourceSeal {dependencySourceSetId, manifestSha256, entryCount, totalBytes, totalChunkCount} must equal the
#   receiver's computation; the response echoes it (DependencySourceAccepted).
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
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
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
rawm=frame(FRAME);dm=json.loads(rawm)
if set(dm)!={'dependencySourceSetId','manifestSha256','entries'}:raise ValueError('manifest fields')
sid=dm['dependencySourceSetId'];entries=dm['entries'];digest=hashlib.sha256(can(dict(dependencySourceSetId=sid,entries=entries))).hexdigest()
if dm['manifestSha256']!=digest:raise ValueError('manifest digest mismatch')
if len(entries)>1000000:raise ValueError('too many entries')
keys=[];seen=set()
for e in entries:
 if set(e)!={'packageKey','path','byteLength','contentSha256'} or (e['packageKey'],e['path'])in seen:raise ValueError('manifest entry')
 seen.add((e['packageKey'],e['path']))
 if not keys or keys[-1]!=e['packageKey']:
  if e['packageKey']in keys:raise ValueError('package keys not grouped')
  keys.append(e['packageKey'])
if len(keys)>4096 or sum(e['byteLength']for e in entries)>8589934592:raise ValueError('limits')
depChunks=0;depBytes=0
for e in entries:
 left=e['byteLength'];assert type(left)is int and left>=0;h=hashlib.sha256();index=0;offset=0
 while left:
  payload=frame(FRAME);hl=struct.unpack('>I',payload[:4])[0];header=json.loads(payload[4:4+hl]);data=payload[4+hl:]
  if header!=dict(dependencySourceSetId=sid,packageKey=e['packageKey'],path=e['path'],chunkIndex=index,byteOffset=offset):raise ValueError('chunk header')
  if not data or len(data)>CAP or len(data)>left:raise ValueError('invalid chunk length')
  h.update(data);left-=len(data);offset+=len(data);index+=1;depChunks+=1;depBytes+=len(data)
 if h.hexdigest()!=e['contentSha256']:raise ValueError('content digest mismatch')
seal=json.loads(frame(CAP));mine=dict(dependencySourceSetId=sid,manifestSha256=digest,entryCount=len(entries),totalBytes=depBytes,totalChunkCount=depChunks)
if seal!=mine:raise ValueError('seal mismatch')
if f.read(1):raise ValueError('trailing bytes')
print(json.dumps(dict(rows=len(manifest),contentBytes=snapBytes,snapshotFrames=1+snapChunks,dependencyPackages=len(keys),dependencyManifestFrameBytes=len(rawm),dependencyFrames=2+depChunks,frames=1+snapChunks+2+depChunks,accepted=seal,receiverNanos=time.monotonic_ns()-start,allDigestsVerified=True,allChunkHeadersVerified=True)),flush=True)
