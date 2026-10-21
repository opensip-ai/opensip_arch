from pathlib import Path
import os, subprocess, json, tempfile, hashlib, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
assert os.getpriority(os.PRIO_PROCESS,0)==10
W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-takeover');F=Path(__file__).parent;B=F/'initial-r3'
assert not B.exists();B.mkdir()
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
tmp=Path(tempfile.mkdtemp(prefix='opensip-d2b3c-initial-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));tmp.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(B/'target'),TMPDIR=str(tmp),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
paths=subprocess.check_output(['/usr/bin/git','diff','--name-only'],cwd=W,text=True).splitlines()+subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard'],cwd=W,text=True).splitlines()
rust=sorted(p for p in paths if p.endswith('.rs'))
with (B/'rustfmt.log').open('wb') as out:
 r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p) for p in rust]],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
# The accepted real-root controls require a fresh fixture binary and its hash.
build=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True)
(B/'build.log').write_bytes(build.stderr);(B/'artifacts.jsonl').write_bytes(build.stdout)
assert build.returncode==0, build.stderr[-5000:]
artifacts=[json.loads(line) for line in build.stdout.splitlines() if line.startswith(b'{')]
bins={j['target']['name']:j for j in artifacts if j.get('reason')=='compiler-artifact' and j.get('executable')}
binary=Path(bins['opensip_components']['executable']);fixture=Path(bins['supervisor_fixture']['executable'])
assert bins['opensip_components']['target']['src_path']==str(W/'crates/components/src/lib.rs')
(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
with (B/'focused.log').open('wb') as out:
 r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','provider_protocol::ts2','--','--test-threads=1'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
text=(B/'focused.log').read_text(errors='replace')
result=dict(standing='INITIAL RECOVERED SOURCE CHECK ONLY; NOT UNIT ACCEPTANCE',exitCode=r.returncode,sourcePins=pins,privateTMPDIR=str(tmp),TMPDIRMode='0700',freshTarget=True,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),fixture=str(fixture),failedTests=re.findall(r'^test (\S+) \.\.\. FAILED$',text,re.M),testSummaries=re.findall(r'^test result:.*$',text,re.M),archiveUntouched=True,productQualification=False)
(B/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
