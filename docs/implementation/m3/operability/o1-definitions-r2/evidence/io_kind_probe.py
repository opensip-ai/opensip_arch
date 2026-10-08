from pathlib import Path
import subprocess,os,json,tempfile,time,re
B=Path('/tmp/opensip-implementation/o1-definition-r1-authoring');D=Path('/tmp/opensip-implementation/o1-definition-r1-stage/docs/implementation/m3/operability/o1-definitions-r1');sdk=Path(subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip());header=sdk/'usr/include/sys/errno.h';text=header.read_text();values={}
for name in ['EACCES','ENOSPC','EIO']:
 m=re.search(r'^#define\s+'+name+r'\s+(\d+)\b',text,re.M);assert m,name;values[name]=int(m.group(1))
code='''fn main() {
    let _ = std::io::ErrorKind::StorageFull;
    for (name, raw) in [VALUES] {
        let error = std::io::Error::from_raw_os_error(raw);
        println!("{}:{}:{:?}:{}", name, raw, error.kind(), error.raw_os_error().is_some());
    }
}
'''.replace('VALUES',','.join('("'+k+'",'+str(v)+')' for k,v in values.items()));f=B/'io-kind-probe.rs';f.write_text(code);darwin=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=darwin/'opensip-lanes.lock';private=Path(tempfile.mkdtemp(prefix='opensip-o1-definition-io-',dir=darwin));os.chmod(private,0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',SDKROOT=str(sdk),TMPDIR=str(private));owned=False
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for the existing lane owner.',flush=True);time.sleep(5)
try:
 binary=private/'io-kind-probe';result=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','linker=/usr/bin/clang',str(f),'-o',str(binary)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert result.returncode==0,result.stdout.decode();r=subprocess.run(['/usr/bin/nice','-n','10',str(binary)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert r.returncode==0;runs=[dict(zip(['errnoName','rawValue','stdlibKind','hasRawErrno'],line.split(':'))) for line in r.stdout.decode().splitlines()];assert len(runs)==3;assert next(v for v in runs if v['errnoName']=='EACCES')['stdlibKind']=='PermissionDenied';assert next(v for v in runs if v['errnoName']=='ENOSPC')['stdlibKind']=='StorageFull';report=dict(standing='CURRENT DARWIN SDK/STDLIB API OBSERVATION ONLY; no new operability mapping, native analysis, OpenSIP code/test or qualification',rows=runs,linuxObservations=0,stderrFormatted=False,rawErrorFormatted=False,productQualification=False);(D/'evidence/io-kind-probe.json').write_text(json.dumps(report,indent=2)+'\n');(D/'evidence/io-kind-probe.rs').write_text(code);print(json.dumps(report,indent=2))
finally:
 if owned:lock.rmdir()
