from pathlib import Path
import os,subprocess,tempfile,time,json,statistics,hashlib
os.setpriority(os.PRIO_PROCESS,0,10)
parent_nice=os.getpriority(os.PRIO_PROCESS,0)
assert parent_nice==10
B=Path(__file__).resolve().parent
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
    try:lock.mkdir();owned=True;break
    except FileExistsError:print('waiting for replay measurement lane',flush=True);time.sleep(5)
try:
    ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']]
    T=Path(tempfile.mkdtemp(prefix='opensip-sm-replay-',dir=D)).resolve();T.chmod(0o700);source=(B/'probe.py').read_bytes();runs=[]
    for n in range(10):
        tag=f'replay-193-{n}';env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),OPENSIP_SM_SYNTHETIC_COUNT='193',OPENSIP_SM_RUN_TAG=tag)
        for k in ['HOME','LANG','LC_ALL','TZ']:
            if k in os.environ:env[k]=os.environ[k]
        out=B/f'{tag}.stdout';err=B/f'{tag}.stderr'
        with out.open('wb')as o,err.open('wb')as e:
            child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(B/'probe.py')],cwd=T,env=env,stdout=o,stderr=e);child_nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert child_nice==10;_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
        assert child.returncode==0,(tag,err.read_text());row=json.loads((B/f'{tag}.json').read_text());assert row['syntheticSourceFiles']==row['findings']==193;rss=int(usage.ru_maxrss);assert 0<=rss<2**64;row.update(ordinal=n,observedChildNiceness=child_nice,warmup=n<3,exitCode=0,rssNative=rss,rssUnit='bytes',rssBytes=rss);runs.append(row)
        assert len({r['runId']for r in runs})==1
        values=[r['completeReplayNanos']for r in runs if not r['warmup']];result=dict(standing='UNREVIEWED LABELLED SYNTHETIC FULL REPLAY;193SOURCES193FINDINGS,SELECTED TS NAPI CONFIGURED SOURCE COUNT; NO FULLSM9',runs=runs,medianReplayNanos=statistics.median(values)if values else None,maxReplayNanos=max(values)if values else None,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,observedParentNiceness=parent_nice,nicenessEstablishedBy="Explicit parent setpriority/readback10 before subprocess; direct child readback10 immediately after Popen; no extra nice adjustment",synthetic=True,SM9PlaceholderFilled=False,SMComplete=False,effectiveL=False,productQualification=False)
        (B/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(f'replay sample {n+1}/10 complete; {row["completeReplayNanos"]} ns;193 actual reconstructed findings',flush=True)
    assert (B/'probe.py').read_bytes()==source
finally:
    if owned:lock.rmdir()
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
