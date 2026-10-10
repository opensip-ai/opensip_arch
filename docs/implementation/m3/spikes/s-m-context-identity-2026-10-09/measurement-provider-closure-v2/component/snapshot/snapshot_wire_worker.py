"""Outside-product snapshot-only measurement fragment, not a protocol provider.

Starts at a caller-selected snapshot phase. No handshake/Universe/Analyze/terminal
conformance or production source/custody claim. Does not execute source code.
"""
from pathlib import Path
import types,sys,json,hashlib,time
B=Path(__file__).resolve().parent

def load(name):
 m=types.ModuleType(name);exec(compile((B/(name+'.py')).read_text(),name+'.py','exec'),m.__dict__);return m
A=load('accounting');F=load('frame_codec');S=load('snapshot_receiver')
initial=int(sys.argv[1]);response_sequence=int(sys.argv[2]);report=Path(sys.argv[3]);S.uint(initial);S.uint(response_sequence)
reader=F.Reader(sys.stdin.buffer,A.encode);receiver=S.Receiver(A.encode);expected_sequence=initial;started=time.monotonic_ns();echo=None
while echo is None:
 envelope,retained=reader.next();S.exact(envelope,['protocolMajor','direction','sequence','frameType','payload'])
 if envelope['protocolMajor']!=3 or type(envelope['protocolMajor']) is not int or envelope['direction']!='host-to-worker' or S.uint(envelope['sequence'])!=expected_sequence:raise S.HarnessRefusal('envelope association')
 expected_sequence+=1
 if expected_sequence>2**64:raise S.HarnessRefusal('sequence overflow')
 kind=envelope['frameType'];payload=envelope['payload']
 if kind=='SnapshotManifest':receiver.manifest(payload)
 elif kind=='SnapshotFileChunk':receiver.chunk(payload)
 elif kind=='SnapshotSeal':echo,files,links=receiver.seal(payload)
 else:raise S.HarnessRefusal('snapshot fragment frame type')
response=dict(protocolMajor=3,direction='worker-to-host',sequence=response_sequence,frameType='SnapshotAccepted',payload=echo)
response_raw=F.frame(response,A.encode);sys.stdout.buffer.write(response_raw);sys.stdout.buffer.flush()
if sys.stdin.buffer.read(1):raise S.HarnessRefusal('bytes after snapshot fragment')
scope_started=time.monotonic_ns()
subjects=[]
for row in receiver.regular:
 if not row['path'].endswith('.rs') or row['byteLength']==0:continue
 preimage=dict(snapshotId=receiver.snapshot_id,path=row['path'],contentSha256=row['contentSha256'],byteLength=row['byteLength'])
 subject_id='rust-file:sha256:'+hashlib.sha256(b'opensip.rust-provider.subject.v2\0'+A.encode(preimage)).hexdigest()
 subjects.append(dict(subjectOrdinal=len(subjects),subjectId=subject_id,path=row['path'],startByte=0,endByte=row['byteLength']))
if not subjects:raise S.HarnessRefusal('empty Rust subject scope')
subject_cbor=A.encode(subjects);scope_sha=hashlib.sha256(b'opensip.rust-provider.subject-scope.v2\0'+subject_cbor).hexdigest();scope_nanos=time.monotonic_ns()-scope_started
result=dict(standing='ACTUAL SNAPSHOT-ONLY FRAMED HARNESS VALIDATION; NOT WHOLE PROTOCOL/SOURCE ADMISSION',accepted=echo,receivedPayloadBytes=reader.payload_bytes,receivedFrames=reader.frames,responseBytes=len(response_raw),files={p:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for p,raw in files.items()},symlinks={p:raw.hex() for p,raw in links.items()},wholeFragmentNanos=time.monotonic_ns()-started,productAdmission=False,protocolConformance=False,fullSM=False)
result.update(subjects=subjects,subjectCount=len(subjects),subjectScopeCommitment='sha256:'+scope_sha,subjectsCborBytes=len(subject_cbor),subjectsCborRawSha256=hashlib.sha256(subject_cbor).hexdigest(),scopeRebuildNanos=scope_nanos,actualC2PlanOrKeys=False,domainCommitmentMeasured=False,SM12FigureComplete=False)
report.write_text(json.dumps(result,indent=2)+'\n')
