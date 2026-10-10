from pathlib import Path
import os,json,stat,hashlib,subprocess
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-identity');P=W.parent/'opensip';A=W.parent/'opensip_arch';D=Path('/tmp/opensip-implementation/rust3-identity-materialization-r1');os.setpriority(os.PRIO_PROCESS,0,10)
j=json.loads((W/'tools/typescript-lanes.json').read_bytes());copied=[]
for row in j['files']:
    target=W/row['path'];src=P/row['path']
    if target.exists():
        raw=target.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path'];continue
    raw=src.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
    assert row['path'].startswith('tools/typescript-boundary/node_modules/'),row['path']
    st=src.lstat();assert stat.S_ISREG(st.st_mode);fd=os.open(src,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    with os.fdopen(fd,'rb') as stream:
        before=os.fstat(stream.fileno());data=stream.read();after=os.fstat(stream.fileno());assert (st.st_dev,st.st_ino)==(before.st_dev,before.st_ino);assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    assert data==raw;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);target.chmod(stat.S_IMODE(st.st_mode));copied.append(row)
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
cmd=['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/check_typescript.py','--root',str(W),'--architecture',str(A),'--node','/Users/sb/.nvm/versions/node/v24.16.0/bin/node','--lane','report']
with (D/'report-lane.log').open('wb') as out:
    child=subprocess.Popen(cmd,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT);assert os.getpriority(os.PRIO_PROCESS,child.pid)==10;code=child.wait()
(D/'report-lane-check.json').write_text(json.dumps(dict(command=cmd,exitCode=code,passed=code==0,exactPinnedIgnoredInputsCopied=len(copied),HOMEOverride=False,sourceApprovalClaimed=False,qualification=False),indent=2)+'\n')
print('Report TypeScript lane exit',code,flush=True)
if code:print((D/'report-lane.log').read_text()[-3500:])
