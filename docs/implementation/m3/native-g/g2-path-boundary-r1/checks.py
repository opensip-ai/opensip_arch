"""Owned source path controls; no corpus or target repository input."""
import datetime,hashlib,json,os,pathlib,subprocess,tempfile,time
p=pathlib.Path('/Users/sb/code/opensip-ai/opensip')
e=pathlib.Path('/tmp/opensip-implementation/g2-path-boundary-authoring')
sysroot=pathlib.Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot')
darwin=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip())
lock=darwin/'opensip-lanes.lock';owned=False
while not owned:
    try:lock.mkdir();owned=True
    except FileExistsError:
        print('Waiting for build lane.',flush=True);time.sleep(15)
try:
    active=[s for s in subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True).splitlines() if s.split() and pathlib.Path(s.split()[-1]).name=='cargo']
    assert not active,active
    scratch=pathlib.Path(tempfile.mkdtemp(prefix='opensip-g2-path-boundary-',dir=darwin));scratch.chmod(0o700)
    namespace=scratch/'namespace';namespace.mkdir();(scratch/'output').mkdir()
    (scratch/'external.txt').write_text('OWNED_EXTERNAL_TEXT')
    (scratch/'external.bin').write_bytes(b'OWNED_EXTERNAL_BINARY')
    (scratch/'external.rs').write_text('pub fn value() -> u8 { 23 }')
    (namespace/'lib.rs').write_text('compile_error!("AMBIENT_ROOT_SHADOW");')
    (namespace/'helper.rs').write_text('compile_error!("AMBIENT_HELPER_SHADOW");')
    (namespace/'alias.rs').symlink_to(scratch/'external.rs')
    env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(scratch),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip(),DYLD_LIBRARY_PATH=str(sysroot/'lib')+':'+str(sysroot/'lib/rustlib/aarch64-apple-darwin/lib'))
    env.pop('RUSTC_BOOTSTRAP',None)
    rows=[]
    def run(label,cmd,child=env):
        result=subprocess.run(['/usr/bin/nice','-n','10',*map(str,cmd)],cwd=p,env=child,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (e/(label+'.log')).write_text(result.stdout)
        rows.append({'label':label,'command':list(map(str,cmd)),'exitCode':result.returncode})
        print(json.dumps(rows[-1]),flush=True)
        return result
    binary=scratch/'path-driver'
    build=run('wrapper-build',[sysroot/'bin/rustc','--edition','2024','--sysroot',sysroot,'-D','warnings','-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc',e/'path-driver.rs','-o',binary],dict(env,RUSTC_BOOTSTRAP='1'))
    assert build.returncode==0,build.stdout
    controls=[]
    for mode in ('root-shadow','absolute-text','escape-binary','path-module','disk-symlink'):
        result=run(mode,[binary,namespace,sysroot,mode])
        if mode=='root-shadow':assert result.returncode==0 and result.stdout=='SEALED_AFTER_ANALYSIS\n',result.stdout
        else:
            assert result.returncode!=0 and 'SEALED_AFTER_ANALYSIS' not in result.stdout,result.stdout
            assert 'couldn\'t read' in result.stdout or 'file not found' in result.stdout,result.stdout
        assert 'AMBIENT_ROOT_SHADOW' not in result.stdout and 'AMBIENT_HELPER_SHADOW' not in result.stdout
        assert not list((scratch/'output').iterdir()),'no analysis/codegen outputs'
        controls.append({'mode':mode,'expected':'AFTER_ANALYSIS' if mode=='root-shadow' else 'SOURCE_REFUSAL_BEFORE_AFTER_ANALYSIS','observedAsExpected':True,'outputDirectoryEmpty':True})
    assert (namespace/'alias.rs').is_symlink() and (namespace/'alias.rs').resolve()==(scratch/'external.rs').resolve()
    assert (namespace/'lib.rs').read_text()=='compile_error!("AMBIENT_ROOT_SHADOW");'
    assert (namespace/'helper.rs').read_text()=='compile_error!("AMBIENT_HELPER_SHADOW");'
    assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
    pins=[]
    for rel in ('providers/rust/src/sealed_vfs.rs','providers/rust/src/compiler_adapter.rs'):
        raw=(p/rel).read_bytes();pins.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    artifacts=[]
    for path in (binary,sysroot/'bin/rustc',e/'path-driver.rs'):
        raw=path.read_bytes();artifacts.append({'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    report={'standing':'G2 OWNED SOURCE PATH BOUNDARY AUTHORING CONTROLS ONLY','commands':rows,'controls':controls,'sourcePins':pins,'artifacts':artifacts,'scratch':str(scratch),'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'laneOwned':True,'nice':10,'repositoryCodeExecuted':False,'corpusSourceUsed':False,'T1ProducerRan':False,'providerLaunchAuthorized':False,'confinementClaimed':False,'metadataSealed':False,'fullG2Complete':False,'productQualification':False}
    (e/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
finally:
    if owned:lock.rmdir()
