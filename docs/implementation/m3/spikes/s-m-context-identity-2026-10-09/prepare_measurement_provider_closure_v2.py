from pathlib import Path
import json,hashlib,importlib.util,sys,shutil,subprocess,os
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');D=B/'measurement-provider-closure-v2';D.mkdir();T=D/'component';T.mkdir();os.setpriority(os.PRIO_PROCESS,0,10)
def pin(p):
 r=p.read_bytes();return dict(path=str(p),bytes=len(r),sha256=hashlib.sha256(r).hexdigest())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
accepted=[]
for name in ['s-m-compiler-definition-join-2026-10-09']:
 q=A/'docs/implementation/m3/spikes'/name/'external-evidence-pins.json'
 j=json.loads(q.read_text()); accepted.extend(j['files'])
def accepted_pin(p):
 r=pin(p)
 if p.parent==B/'dependency-frame-fragment':
  q=A/'docs/implementation/m3/spikes/s-m-dependency-fragment-2026-10-09/fragment'/p.name;assert q.read_bytes()==p.read_bytes(), p
 elif p.name=='driver.rs':assert (A/'docs/implementation/m3/spikes/s-m-compiler-definition-join-2026-10-09/driver.rs').read_bytes()==p.read_bytes()
 else:assert any(Path(x['path']).resolve()==p.resolve() and x['bytes']==r['bytes'] and x['sha256']==r['sha256'] for x in accepted),r
 return r
files={}
for name in ['snapshot_wire_worker.py','snapshot_receiver.py','frame_codec.py','accounting.py']:
 files['snapshot/'+name]=B/'manifest-scope'/name
for name in ['dependency_wire_worker.py','dependency_receiver.py','frame_codec.py','snapshot_receiver.py','accounting.py']:
 p=B/'dependency-frame-fragment'/name;accepted_pin(p);files['dependency/'+name]=p
driver=B/'compiler-definition-join-observations';build=json.loads((driver/'build.json').read_text())
files['compiler/driver.rs']=driver/'driver.rs';assert pin(files['compiler/driver.rs'])['sha256']==build['sourceSha256'];accepted_pin(files['compiler/driver.rs'])
exe=Path(build['executable']);r=pin(exe);assert r['sha256']==build['sha256'] and r['bytes']==build['bytes'];accepted_pin(exe);files['compiler/driver']=exe
origins=[]
for rel,p in sorted(files.items()):
 q=T/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert pin(q)['sha256']==pin(p)['sha256'];origins.append(dict(componentPath=rel,original=pin(p)))
manifest=dict(componentId='measurement.rust-native-fragments',semanticVersion='0.2.0',protocolMajor=3,platform='aarch64-apple-darwin',standing='UNSIGNED OUTSIDE-PRODUCT RETAINED FRAGMENTS; NO SINGLE FULL NATIVE WORKER OR DELIVERY ADMISSION',phaseEntrypoints=dict(snapshot='snapshot/snapshot_wire_worker.py',dependency='dependency/dependency_wire_worker.py',compiler='compiler/driver'),repositoryExecution=False,runtimeInputs=dict(python=pin(Path('/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14').resolve()),rustContextObservations=pin(B/'rust-context-input-observations.json'),compilerBuild=pin(driver/'build.json'),validatorFilePins=pin(B/'dependency-frame-fragment/observations.json')),limitations=['phase-selected fragment package, not whole protocol','compiler observations not complete FA2 census or FactCandidates','no authenticated core import projections or signed Tool/source/owner admission','external interpreters/compiler libraries/sysroot/validator/model inputs retained separately, not claimed complete signed runtime package'])
write(T/'component-manifest.json',manifest)
tree=[pin(p)|dict(path=p.relative_to(T).as_posix()) for p in sorted(T.rglob('*')) if p.is_file()];assert len(tree)==12
closure=dict(schemaVersion=2,kind='provider',manifestDigest=pin(T/'component-manifest.json')['sha256'],tree=tree,semanticVersion=manifest['semanticVersion'],protocolMajor=manifest['protocolMajor'],platform=manifest['platform'])
model=A/'docs/coop/design-corrections/native/native_evidence_model.v2.py';spec=importlib.util.spec_from_file_location('native_model',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
identity=M.IM.identifier('closure',closure);write(D/'closure-descriptor.json',closure)
bridge=B/'hash_bridge';before=pin(bridge);child=subprocess.Popen([str(bridge),'closure',str(D/'closure-descriptor.json')],stdout=subprocess.PIPE,stderr=subprocess.PIPE);priority=os.getpriority(os.PRIO_PROCESS,child.pid);out,err=child.communicate();assert priority==10 and child.returncode==0,err;answer=json.loads(out);assert identity=='closure2:'+answer['identityDigest'];assert pin(bridge)==before;(D/'bridge.stdout').write_bytes(out);(D/'bridge.stderr').write_bytes(err)
old=json.loads((B/'measurement-provider-closure/observations.json').read_text());assert old['closureId']!=identity
write(D/'observations.json',dict(standing='UNREVIEWED NEW UNSIGNED FRAGMENT PACKAGE IDENTITY; NOT AN ADMITTED NATIVE WORKER',closureId=identity,previousClosureId=old['closureId'],previousClosureRetainedUnchanged=True,descriptor=pin(D/'closure-descriptor.json'),completeRetainedComponentFiles=len(tree),componentManifest=pin(T/'component-manifest.json'),originalBytes=origins,referenceModel=pin(model),productBridge=before,observedBridgeNiceness=priority,productIdentityAgrees=True,advisory=pin(Path('/tmp/opensip-implementation/reviews/grok-sm-plan-boundary-advisory-r2/review.json')),planSelectionConstructed=False,subjectScopeEnumeratorJoined=False,deliveryAdmitted=False,ToolAdmitted=False,ownerAdmitted=False,sourceAdmission=False,protocolConformance=False,fullSM=False))
print(identity,len(tree),'new exact retained component files; old closure untouched; no signed admission')
