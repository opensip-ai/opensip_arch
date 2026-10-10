from pathlib import Path
import os,subprocess,tempfile,time,json
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-identity');B=Path('/tmp/opensip-implementation/rust3-identity-materialization-r1/checks-r1');B.mkdir()
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
    try:lane.mkdir();owned=True
    except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
    T=Path(tempfile.mkdtemp(prefix='opensip-native-public-check-',dir=D));T.chmod(0o700)
    E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
    E.update(CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
    R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
    steps=[('fmt-host',[R+'rustfmt','--edition','2024','src/schema_sources.rs'],W/'crates/host'),('fmt-identity',[R+'rustfmt','--edition','2024','src/schema_registry.rs'],W/'crates/identity'),('identity-tests',[R+'cargo','test','--locked','--offline','-p','opensip-identity','--lib'],W),('host-tests',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib'],W),('host-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'],W),('identity-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-identity','--all-targets','--','-D','warnings'],W)]
    rows=[]
    for name,args,cwd in steps:
        print(name,'starting',flush=True)
        with (B/(name+'.log')).open('wb') as log:
            child=subprocess.Popen(args,cwd=cwd,env=E,stdout=log,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;code=child.wait()
        rows.append(dict(name=name,args=args,cwd=str(cwd),exitCode=code,niceness=priority));print(name,'exit',code,flush=True)
        if code:print((B/(name+'.log')).read_text()[-5000:],flush=True);break
    (B/'checks.json').write_text(json.dumps(dict(rows=rows,allPassed=len(rows)==len(steps) and all(r['exitCode']==0 for r in rows),privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True,installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists()),indent=2)+'\n')
finally:
    if owned:lane.rmdir()
