from pathlib import Path
import os,json,hashlib,subprocess,tempfile
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'handoff-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-rust3-send-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
expected=['crates/components/src/provider_protocol/rust3/receive.rs','crates/components/src/provider_protocol/rust3/receive_tests.rs']
assert sorted(subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=W,text=True).splitlines())==expected
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p)for p in expected]],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
pins=[dict(path=p,bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in expected];report=dict(standing='UNACCEPTED4b raw-candidate handoff prelude only; full builders/schedule/sender/participant still required',sourcePins=pins,runs=[],unitAccepted=False,productQualification=False)
for name,args in [('rust3-tests',[R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','rust3']),('component-lib-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','--lib','--','-D','warnings'])]:
 with (B/(name+'.log')).open('wb')as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 report['runs'].append(dict(name=name,exitCode=r.returncode));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0,name
assert b'46 passed; 0 failed'in(B/'rust3-tests.log').read_bytes()
assert all(hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']for p in pins)
report.update(allPassed=True,rust3Tests=46,newHandoffControls=3);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('UNACCEPTED4b HANDOFF46RUST3/CLIPPY PASS; REST OF4b STILL OWED')
