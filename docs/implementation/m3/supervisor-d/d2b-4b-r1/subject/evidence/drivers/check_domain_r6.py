from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'domain-r6';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-rust3-send-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
paths=['crates/components/src/provider_protocol/rust3.rs','crates/components/src/provider_protocol/rust3/send.rs','crates/components/src/provider_protocol/rust3/send/schedule.rs','crates/components/src/provider_protocol/rust3/send/domain.rs','crates/components/src/provider_protocol/rust3/send/domain_tests.rs','crates/components/src/provider_protocol/rust3/schema_work.rs']
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p)for p in paths]],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
pins=[dict(path=p,bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in paths]
with(B/'tests.log').open('wb')as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','provider_protocol::rust3'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
log=(B/'tests.log').read_text();report=dict(standing='UNACCEPTED4b fresh host domain reconstruction and private schedule mechanisms; full Plan builders/sender/participant and warning-denied whole-unit checks remain required',sourcePins=pins,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',log,re.M),warnings=re.findall(r'^warning:.*$',log,re.M),unitAccepted=False,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0 and '55 passed; 0 failed'in log
assert all(hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']for p in pins)
report.update(allPassed=True,rust3ModuleTests=55,newDomainControls=6,full4bImplemented=False);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PRIVATE DOMAIN55RUST3 PASS; FULL4b/WARNING-DENIED CHECKS NOT COMPLETE')
