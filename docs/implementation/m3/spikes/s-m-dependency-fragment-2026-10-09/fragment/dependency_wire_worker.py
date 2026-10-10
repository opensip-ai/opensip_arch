"""Caller-selected dependency phase only; no handshake/Universe/Plan/import admission."""
from pathlib import Path
import types,sys,json,hashlib,time,importlib.util
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
def load(name):
 m=types.ModuleType(name);exec(compile((B/(name+'.py')).read_text(),name+'.py','exec'),m.__dict__);return m
A=load('accounting');F=load('frame_codec');S=load('dependency_receiver')
model=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py');spec=importlib.util.spec_from_file_location('native_model',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
descriptor=json.loads(Path(sys.argv[1]).read_text());file_dir=Path(sys.argv[2]);report=Path(sys.argv[3]);set_id=M.dependency_source_set_identity(descriptor);expected={};packages=[]
for pkg in descriptor['packages']:
 if pkg['acquisition']['descriptorId'] is not None:raise S.HarnessRefusal('NIJ-1 null self-reference')
 package_key='pkg1-'+hashlib.sha256(M.C.canonical([pkg['name'],pkg['version'],pkg['sourceId']])).hexdigest();rows=json.loads((file_dir/(package_key+'.json')).read_text());M.validate_native('DependencyFileManifestV1',rows)
 files={r['path']:dict(sha256=r['contentSha256'],byteLength=r['byteLength']) for r in rows}
 if len(files)!=len(rows) or M.file_manifest_identity(files)!=pkg['fileManifestSha256'] or len(files)!=pkg['fileCount'] or sum(f['byteLength'] for f in files.values())!=pkg['totalBytes']:raise S.HarnessRefusal('retained package file manifest join')
 for p,f in files.items():expected[(package_key,p)]=(f['byteLength'],f['sha256'])
 packages.append(package_key)
reader=F.Reader(sys.stdin.buffer,A.encode);receiver=S.Receiver(A.encode,set_id,expected);sequence=0;started=time.monotonic_ns();echo=None
while echo is None:
 env,retained=reader.next();S.exact(env,['protocolMajor','direction','sequence','frameType','payload'])
 if type(env['protocolMajor']) is not int or env['protocolMajor']!=3 or env['direction']!='host-to-worker' or S.uint(env['sequence'])!=sequence:raise S.HarnessRefusal('envelope association')
 sequence+=1
 if sequence>2**64:raise S.HarnessRefusal('sequence overflow')
 kind=env['frameType'];payload=env['payload']
 if kind=='DependencySourceManifest':receiver.manifest(payload)
 elif kind=='DependencySourceChunk':receiver.chunk(payload)
 elif kind=='DependencySourceSeal':echo,files=receiver.seal(payload)
 else:raise S.HarnessRefusal('dependency-only fragment frame type')
response=dict(protocolMajor=3,direction='worker-to-host',sequence=0,frameType='DependencySourceAccepted',payload=echo);sys.stdout.buffer.write(F.frame(response,A.encode));sys.stdout.buffer.flush()
if sys.stdin.buffer.read(1):raise S.HarnessRefusal('bytes after dependency fragment')
report.write_text(json.dumps(dict(standing='ACTUAL DEPENDENCY-ONLY FRAGMENT; NOT WHOLE PROTOCOL OR SOURCE/IMPORT ADMISSION',accepted=echo,workerRederivedDependencySourceSetId=set_id,packages=len(packages),immutableVfsFiles={p:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for p,raw in files.items()},wholeFragmentNanos=time.monotonic_ns()-started,receivedFrames=reader.frames,receivedPayloadBytes=reader.payload_bytes,sourceAdmission=False,selectedImportWrapperConstructed=False,actualC2PlanOrKeys=False,protocolConformance=False,fullSM=False),indent=2)+'\n')
