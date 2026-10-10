from pathlib import Path
import os,json,hashlib,struct,tempfile,sys,dataclasses
B=Path(__file__).resolve().parent;SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');build=json.loads((B/'build.json').read_bytes());exe=Path(build['executable']);assert hashlib.sha256(exe.read_bytes()).hexdigest()==build['sha256'];assert not(B/'controls.json').exists();D=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');root=Path(tempfile.mkdtemp(prefix='opensip-sm-metadata-controls-',dir=D));root.chmod(0o700);sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/quality');from root_observation import observe_root
os.setpriority(os.PRIO_PROCESS,0,10);records=[]
def run(name,crate,files,features=(),externs=()):
 r=root/name;r.mkdir(mode=0o700);virtual=r/'virtual';virtual.mkdir(mode=0o700);rows=sorted((str(virtual/k),v) for k,v in files.items());encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))
 for k,data in rows:
  n=k.encode();encoded+=struct.pack('>Q',len(n))+n+struct.pack('>Q',len(data))+data
 mp=r/'source-map.bin';mp.write_bytes(encoded);mp.chmod(0o400);out=r/('lib'+crate+'.rmeta');argv=[str(exe),'--prepared-map',str(mp),'--crate-type','lib','--crate-name',crate,'--edition','2024','--sysroot',str(SYS),'--emit','metadata',str(virtual/'lib.rs'),'-o',str(out)]
 for f in features:argv += ['--cfg','feature='+json.dumps(f)]
 for alias,path in externs:argv += ['--extern',alias+'='+str(path)]
 stdout=os.open(r/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(r/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:observed=observe_root(argv,cwd=str(virtual),environment={},stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=30_000_000_000)
 finally:os.close(stdout);os.close(stderr)
 events=[json.loads(x) for x in (r/'stdout.log').read_text().splitlines() if x.startswith('{')];success=observed.returncode==0 and any(x['event']=='after_analysis' for x in events) and out.is_file()
 records.append(dict(name=name,argv=argv,map=dict(path=str(mp),bytes=len(encoded),sha256=hashlib.sha256(encoded).hexdigest()),root=str(r),observation=dataclasses.asdict(observed),events=events,analysisAndMetadataSuccess=success,metadata=dict(path=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest()) if out.exists() else None,sourceAuthentication=False,nativeAdmission=False));return success,out,events
success,dep,_=run('dependency-metadata','depunit',{'lib.rs':b'pub fn value() -> u8 { 7 }\n'});assert success
success,_,_=run('renamed-extern-typecheck','rootunit',{'lib.rs':b'pub fn value() -> u8 { renamed_dep::value() }\n'},externs=[('renamed_dep',dep)]);assert success
success,_,_=run('extern-type-error','badroot',{'lib.rs':b'pub fn value() -> bool { renamed_dep::value() }\n'},externs=[('renamed_dep',dep)]);assert not success
success,_,_=run('missing-extern','missingroot',{'lib.rs':b'pub fn value() -> u8 { absent_dep::value() }\n'});assert not success
success,_,_=run('actual-feature-cfg','featured',{'lib.rs':b'#[cfg(not(feature="selected"))] compile_error!("feature absent"); pub fn value() {}\n'},features=['selected']);assert success
marker=root/'outside-marker';marker.write_bytes(b'OUTSIDE_MARKER_BYTES_NOT_A_SOURCE_MEMBER');markerpin=hashlib.sha256(marker.read_bytes()).hexdigest();source=('pub const VALUE: &str = include_str!('+json.dumps(str(marker))+');\n').encode();success,_,events=run('denied-source-read','deniedroot',{'lib.rs':source});assert not success;assert hashlib.sha256(marker.read_bytes()).hexdigest()==markerpin
result=dict(standing='ACTUAL FIRSTPARTY API CONTROLS; NOT CORPUS OR FULL NATIVE ADMISSION',controlsPassed=6,compilerChildren=6,root=str(root),results=records,emptyChildEnvironment=True,EOFStandardInput=True,explicitOwnedOutputs=True,bareRustcWrapperBuild=True,callerPrototypeTimeoutSecondsNotLaw=30,repositoryCodeExecuted=False,procMacroOrBuildScriptExecuted=False,sourceMapBoundaryOnlyNotFullFilesystemConfinement=True,sourceAuthentication=False,typecheckControlsOnly=True,corpusRun=False,completeStatisticalSet=False,nativeAdmission=False,SMComplete=False);(B/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print('Six firstparty controls pass: metadata dependency plus renamed extern typecheck; actual type error/missing extern/feature/source-map denial retained. No corpus run.',flush=True);assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
