from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'successor-mutations-r1';B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
source=W/'crates/components/src/provider_protocol/rust3/receive.rs';original=source.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
mutations=[dict(name='reference-scope-reconstruction-removed',old='if field(d, "subjectScope") != Some(scope) {',new='if false && field(d, "subjectScope") != Some(scope) {',test='reference_receiver_refuses_unreconstructed_count_scope_and_domain'),dict(name='exact-capability-token-echo-removed',old='if field(f, "capabilities") != field(hello, "expectedCapabilities")',new='if false && field(f, "capabilities") != field(hello, "expectedCapabilities")',test='census_each_optional_token_mismatch_refuses_at_hello_before_open_or_source')]
report=dict(standing='UNACCEPTED candidate compiled runtime guard mutations; not full4c review or qualification',originalSourceSha256=sha(original),runs=[],allKilled=False,sourceRestored=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 for m in mutations:
  assert source.read_bytes()==original;old=m['old'].encode();assert original.count(old)==1;changed=original.replace(old,m['new'].encode());source.write_bytes(changed);D=B/m['name'];D.mkdir();(D/'mutated-receive.rs').write_bytes(changed)
  c=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','--no-run','--message-format=json'],cwd=W,env=E,capture_output=True);(D/'artifacts.jsonl').write_bytes(c.stdout);(D/'build.log').write_bytes(c.stderr);assert c.returncode==0
  rows=[j for l in c.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_components'];assert len(rows)==1 and not rows[0]['fresh'];binary=Path(rows[0]['executable'])
  c=subprocess.run([str(binary),m['test'],'--nocapture'],cwd=W,env=E,capture_output=True);log=c.stdout+c.stderr;(D/'tests.log').write_bytes(log);text=log.decode(errors='replace');failures=re.findall(r'^test (.+) \.\.\. FAILED$',text,re.M)
  run=dict(name=m['name'],sourceSha256=sha(changed),binary=str(binary),binarySha256=sha(binary.read_bytes()),freshlyCompiled=True,exitCode=c.returncode,failureSet=failures,summaries=re.findall(r'^test result:.*$',text,re.M),killed=c.returncode!=0 and len(failures)==1 and m['test'] in failures[0]);report['runs'].append(run);save();assert run['killed'];source.write_bytes(original)
finally:
 source.write_bytes(original);report['sourceRestored']=source.read_bytes()==original;save()
assert report['sourceRestored'];report['allKilled']=all(r['killed']for r in report['runs'])and len(report['runs'])==2;save();assert report['allKilled'];print('Both mandatory freshcompiled runtime guard mutations KILLED; exact production source restored. Restored full owning/Clippy run still required.')
