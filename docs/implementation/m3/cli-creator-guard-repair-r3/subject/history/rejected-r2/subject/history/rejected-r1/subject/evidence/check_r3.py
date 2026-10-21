from pathlib import Path
import os,subprocess,json,hashlib,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'owning-r3';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-cli-gate-repair');R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR='/tmp/opensip-implementation/cli-source-guard-repair-2026-10-21/target',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());path='apps/cli/tests/creator_commands_tests.rs'
r=subprocess.run([R+'rustfmt','--edition','2024',str(W/path)],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
raw=(W/path).read_bytes();report=dict(standing='TEST-ONLY CLI SOURCE GUARD REPAIR; NO PRIVATE/INSTALLATION READ OR CLI INVOCATION',source=dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),runs=[],unitAccepted=False,productQualification=False)
def compile(folder):
 folder.mkdir(exist_ok=True);r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-cli','--test','creator_commands_tests'],cwd=W,env=E,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout)
 if r.returncode!=0:
  for line in r.stdout.splitlines():
   if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-message'and j['message']['level']=='error':print(j['message'].get('rendered'),flush=True)
 assert r.returncode==0,'compile failure never counts as runtime evidence';rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='creator_commands_tests'];assert len(rows)==1;assert rows[0]['target']['src_path']==str(W/path);return Path(rows[0]['executable'])
binary=compile(B/'positive');report['binary']=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest());tests=['creator_commit_guard_keeps_storage_calls_and_limits_the_logging_exception','no_creator_gate_writer_pack_or_commit_symbol_reaches_the_binary_or_the_ingress']
for test in tests:
 r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);rawlog=r.stdout+r.stderr;(B/(test+'.log')).write_bytes(rawlog);report['runs'].append(dict(test=test,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',rawlog.decode(),re.M)));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0,rawlog.decode()
with (B/'cli-clippy.log').open('wb')as out:r=subprocess.run([R+'cargo','clippy','--locked','--offline','-p','opensip-cli','--all-targets','--','-D','warnings'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0,(B/'cli-clippy.log').read_text()[-2300:]
# A compile-valid guard weakening must fail at the explicit storage control.
old='.any(|identifier| identifier == "finalize")';assert raw.decode().count(old)==1;mutated=raw.decode().replace(old,'.any(|_identifier| false)');(W/path).write_text(mutated);error=None
try:
 binary=compile(B/'weakened-commit-guard');r=subprocess.run([str(binary),'--exact',tests[0]],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/'weakened-commit-guard/runtime.log').write_bytes(log);assert r.returncode!=0 and b'storage commit must remain forbidden' in log and b'0 passed; 1 failed'in log;report['mutant']=dict(compiled=True,runtimeExitCode=r.returncode,caught=True)
except BaseException as ex:error=ex
finally:
 (W/path).write_bytes(raw);assert hashlib.sha256((W/path).read_bytes()).hexdigest()==report['source']['sha256'];binary=compile(B/'restored-positive')
 for test in tests:
  r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);(B/'restored-positive'/(test+'.log')).write_bytes(r.stdout+r.stderr);assert r.returncode==0
 report['allRestored']=True
if error:raise error
report.update(allPassed=True,cliClippyPassed=True,newPaths=0,noProductionChanges=True);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('TWO PURE SOURCE GUARD CONTROLS/CLIPPY PASS; MUTANT COMPILED/CAUGHT/RESTORED; NO UNIT ACCEPTANCE',flush=True)
