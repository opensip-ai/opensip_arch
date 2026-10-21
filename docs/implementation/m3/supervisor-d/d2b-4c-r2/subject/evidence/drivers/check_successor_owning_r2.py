from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'successor-owning-r2';B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());assert all(p.endswith(('.rs','.json'))for p in paths)
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
def save(v):(B/'report.json').write_text(json.dumps(v,indent=2)+'\n')
r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p)for p in paths if p.endswith('.rs')]],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
pins=[dict(path=p,bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in paths]
r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','--no-run','--message-format=json'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout)
report=dict(standing='UNACCEPTED partial4c census request/response and reference context; complete successor replays, controls/mutations/fullunit review remain owed',sourcePins=pins,buildExitCode=r.returncode,unitAccepted=False,productQualification=False);save(report);assert r.returncode==0
rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_components'];assert len(rows)==1;row=rows[0];binary=Path(row['executable']);report.update(binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=row['fresh'])
r=subprocess.run([str(binary),'provider_protocol::rust3','--nocapture'],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/'tests.log').write_bytes(log);text=log.decode(errors='replace');report.update(exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',text,re.M),failureSet=re.findall(r'^test (.+) \.\.\. FAILED$',text,re.M));save(report);assert r.returncode==0
assert all(hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']for p in pins)
assert '115 passed; 0 failed' in text
report['scopedControlsPassed']=True;save(report)
with(B/'clippy.log').open('wb')as out: lint=subprocess.run([R+'cargo','clippy','--locked','--offline','-p','opensip-components','--all-targets','--','-D','warnings'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
report.update(clippyExitCode=lint.returncode);save(report);assert lint.returncode==0
report['allPassed']=True;save(report);print('115Rust3 owning tests + component alltargetClippy PASS; remaining replay/accounting/classification, mutations/fullunit review still owed.')
