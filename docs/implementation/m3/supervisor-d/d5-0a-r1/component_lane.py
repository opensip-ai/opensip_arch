from pathlib import Path
import os,subprocess,json,sys,tempfile,hashlib,re,time
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
mode=sys.argv[1];assert mode in ('base','candidate')
repo=Path('/Users/sb/code/opensip-ai')/('opensip' if mode=='base' else 'opensip-d5-0-takeover');out=Path(__file__).parent/(sys.argv[2] if len(sys.argv)>2 else mode);out.mkdir(exist_ok=False)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()=='4453f529f532648fd7760e59e7ade90903446aaf'
r='/opt/homebrew/Cellar/rust/1.95.0/bin/';tmpbase=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip();tmp=Path(tempfile.mkdtemp(prefix='opensip-d5-'+mode+'-',dir=tmpbase));tmp.chmod(0o700)
env=dict(os.environ,PATH='/opt/homebrew/bin:'+r+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(out/'target'),CARGO=r+'cargo',RUSTC=r+'rustc',TMPDIR=str(tmp),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip())
env.pop('RUST_TEST_THREADS',None)
paths=['crates/components/src/supervisor.rs','crates/components/src/supervisor_tests.rs','crates/components/tests/supervisor_fixture.rs'];pins=[{'path':p,'sha256':hashlib.sha256((repo/p).read_bytes()).hexdigest()} for p in paths]
command=[r+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components']
print(mode,'BUILD',flush=True);build=subprocess.run(command,cwd=repo,env=env,capture_output=True);(out/'build-artifacts.jsonl').write_bytes(build.stdout);(out/'build.log').write_bytes(build.stderr);assert build.returncode==0,build.stderr[-3000:]
fixture=None;binary=None
for line in build.stdout.splitlines():
 try:record=json.loads(line)
 except ValueError:continue
 if record.get('reason')!='compiler-artifact' or not record.get('executable'):continue
 if record['target']['name']=='supervisor_fixture':fixture=Path(record['executable'])
 if record['target']['name']=='opensip_components' and record['profile']['test']:binary=Path(record['executable'])
assert fixture and binary
(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
report={'standing':'D5-0 WAITS DEVELOPMENT LANE ONLY; NOT UNIT ACCEPTANCE','mode':mode,'base':'4453f529f532648fd7760e59e7ade90903446aaf','repository':str(repo),'pins':pins,'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'fixtureSha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'parallelism':'libtest default; no RUST_TEST_THREADS override or serialization','privateTMPDIR':str(tmp),'runs':[]}
for index in range(1,2 if mode=='base' else 4):
 print(mode,'PARALLEL RUN',index,flush=True);started=time.monotonic()
 with (out/f'parallel-{index}.log').open('wb') as log:result=subprocess.run([str(binary)],cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
 text=(out/f'parallel-{index}.log').read_text(errors='replace');summaries=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',text);assert summaries,text[-2000:]
 failure_section=text.split('\nfailures:\n')[-1].split('\ntest result:')[0]
 failures=sorted(set(line.strip() for line in failure_section.splitlines() if line.startswith('    ') and ' ' not in line.strip())) if int(summaries[-1][1]) else []
 row={'run':index,'exitCode':result.returncode,'passed':int(summaries[-1][0]),'failed':int(summaries[-1][1]),'ignored':int(summaries[-1][2]),'failureSet':failures,'handshakeDeadlineInFailureOutput':'HandshakeDeadline' in text,'elapsedSeconds':time.monotonic()-started};report['runs'].append(row);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(row),flush=True)
for row in pins:assert row['sha256']==hashlib.sha256((repo/row['path']).read_bytes()).hexdigest(),'source changed during owning lane'
print('DONE',mode,flush=True)
