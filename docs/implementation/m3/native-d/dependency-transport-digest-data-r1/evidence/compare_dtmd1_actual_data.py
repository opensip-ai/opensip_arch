from pathlib import Path
import json,hashlib,types,subprocess,os,tempfile,copy
B=Path('/tmp/opensip-implementation');D=B/'dtmd1-data-2026-10-09';W=Path('/Users/sb/code/opensip-ai/opensip-dtmd1');A=W.parent/'opensip_arch';V=A/'docs/implementation/m3/snapshot-plan-c/dependency-transport-digest-r1';O=B/'sm-stage-volume-2026-10-09/actual-dependency-file-manifests';os.setpriority(os.PRIO_PROCESS,0,10)
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def load(n):m=types.ModuleType(n);exec(compile((V/'reference-encoders'/(n+'.py')).read_text(),n+'.py','exec'),m.__dict__);return m
R=load('accounting');I=load('independent_host_codec');deps=W/'target/debug/deps';libs=[]
for n in ['opensip_identity','serde_json']:
 ps=list(deps.glob('lib'+n+'-*.rlib'));assert len(ps)==1,(n,ps);libs.append(pin(ps[0]))
T=Path(tempfile.mkdtemp(prefix='opensip-dtmd1-compare-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip()));T.chmod(0o700);exe=T/'compare';E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip());cmd=['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','linker=/usr/bin/cc',str(D/'compare.rs'),'-L','dependency='+str(deps),'-o',str(exe)]
for n,p in zip(['opensip_identity','serde_json'],libs):cmd+=['--extern',n+'='+p['path']]
p=subprocess.Popen(cmd,env=E,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,p.pid);out,_=p.communicate();(D/'build.log').write_bytes(out);assert priority==10 and p.returncode==0,out.decode()
observations=json.loads((O/'observations.json').read_text());entries=[];inputs=[]
for row in observations['rows']:
 p=Path(row['fileManifest']['path']);assert pin(p)==row['fileManifest'];inputs.append(row['fileManifest'])
 for f in json.loads(p.read_text()):entries.append(dict(packageKey=row['packageKey'],**f))
assert len(entries)==7338
vectors=json.loads((V/'vectors.json').read_text())['vectors'];cases=[(v['name'],v['entries'],v['manifestSha256']) for v in vectors];cases.append(('actual-187-registry-7338-files',entries,None));cases.append(('actual-reversed-sequence',list(reversed(entries)),None));edge=copy.deepcopy(entries[:2]);edge[0]['byteLength']=2**64-1;cases.append(('uint64-max-inert-data',edge,None));cases.append(('duplicate-inert-data',[entries[0],entries[0]],None));rows=[]
for name,items,expected in cases:
 a=R.encode(items);b=I.encode(items);assert a==b;sha=hashlib.sha256(a).hexdigest()
 if expected is not None:assert sha==expected
 path=D/(name+'.json');path.write_text(json.dumps(items,indent=2)+'\n');p=subprocess.Popen([str(exe),str(path)],env=E,stdout=subprocess.PIPE,stderr=subprocess.PIPE);priority=os.getpriority(os.PRIO_PROCESS,p.pid);out,err=p.communicate();assert priority==10 and p.returncode==0,err.decode();(D/(name+'.stdout')).write_bytes(out);actual=json.loads(out);assert actual==dict(entries=len(items),cborBytes=len(a),cborHex=a.hex(),manifestSha256=sha);rows.append(dict(name=name,input=pin(path),entries=len(items),cborBytes=len(a),manifestSha256=sha,rustAndBothIndependentEncodersEqual=True,childNiceness=priority))
assert rows[3]['manifestSha256']!=rows[4]['manifestSha256'];report=dict(standing='ACTUAL PRIVATE PRODUCT DIGEST KERNEL/PYTHON ENCODER EQUALITY; NOT DEPENDENCY TRANSPORT OR SOURCE ADMISSION',compiler=pin(Path(cmd[0])),executable=pin(exe),linked=libs,sourcePins=[pin(W/'crates/host/src/dependency_transport_digest.rs'),pin(W/'crates/host/src/rust_scope_data.rs'),pin(V/'vectors.json')],retainedPackageFileManifests=inputs,packageManifestObservations=pin(O/'observations.json'),workloads=rows,actualRegistryPackages=187,actualRetainedFileObservations=7338,privateTMPDIR=str(T),TMPDIRMode='0700',parentAndChildrenNice10=True,sourceFileBytesReadBackEarlier=True,sourceFileBytesStreamed=False,actualDependencySourceSet=False,actualAcceptedTransportManifest=False,actualC2PlanOrKeys=False,sourceAdmission=False,fullSM=False);(D/'independent.json').write_text(json.dumps(report,indent=2)+'\n');print('7actual Rust/Python/Python equality cases, including all7338retained registry file observations and fulluint64; no transfer/admission claim')
