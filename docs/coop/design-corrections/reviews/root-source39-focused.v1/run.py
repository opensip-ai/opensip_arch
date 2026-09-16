from pathlib import Path
import concurrent.futures, hashlib, json, subprocess, time
O=Path(__file__).parent
S=Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
DC=S/'docs/coop/design-corrections'
PY='/tmp/opensip-architecture-review-env/bin/python'
jobs=[('native-corrections','foundation/check-native-consumer24-corrections.v1.py',[]),
      ('semantic','foundation/check-semantic-replay.v3.py',['--output',str(O/'semantic')]),
      ('carrier','security/check-integrated-carrier.v1.py',['--source',str(S),'--report',str(O/'carrier/report.json')])]
def run(job):
    name,script,args=job;d=O/name;d.mkdir(exist_ok=False)
    command=[PY,'-I','-B',str(DC/script)]+args
    (d/'command.json').write_text(json.dumps({'argv':command,'cwd':str(d)}))
    start=time.time()
    try:
        p=subprocess.run(command,cwd=d,capture_output=True,timeout=3000)
        code,stdout,stderr=p.returncode,p.stdout,p.stderr
    except subprocess.TimeoutExpired as exc:
        code,stdout,stderr=None,exc.stdout or b'',exc.stderr or b''
    (d/'stdout.txt').write_bytes(stdout);(d/'stderr.txt').write_bytes(stderr)
    row={'name':name,'exitCode':code,'seconds':time.time()-start,
         'stdoutSha256':hashlib.sha256(stdout).hexdigest(),'stderrSha256':hashlib.sha256(stderr).hexdigest()}
    (d/'exit.json').write_text(json.dumps(row,indent=2)+'\n');print(name,code,flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:rows=list(e.map(run,jobs))
(O/'summary.json').write_text(json.dumps({'standing':'Focused combined mutable-source reference checks. No global pin-valid check or acceptance.', 'source':str(S),'checks':rows,'passed':all(r['exitCode']==0 for r in rows)},indent=2)+'\n')
raise SystemExit(not all(r['exitCode']==0 for r in rows))
