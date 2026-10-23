from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re,resource
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'repaired-workspace-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip');A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
FD=Path('/tmp/opensip-implementation/doctor-source-guard-repair-2026-10-21');FP=Path('/tmp/opensip-implementation/platform-fd3-test-repair-2026-10-21')
d=json.loads((FD/'integration-r3.json').read_text());p=json.loads((FP/'integration-r1.json').read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=W,text=True).strip()
assert git('rev-parse','HEAD')==d['productCode']and not git('status','--porcelain')
assert subprocess.run(['git','merge-base','--is-ancestor',p['productCode'],d['productCode']],cwd=W).returncode==0
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'base-components-target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
report=dict(standing='Fresh accepted-main whole-workspace verification after independently accepted doctor and descriptor test repairs',productCode=d['productCode'],architecture=d['architecture'],sourceTree=git('rev-parse','HEAD^{tree}'),priorFailuresRetained=str(F/'receiver-final-owning-r3/report.json'),runs=[],productQualification=False,entireProjectComplete=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
save()
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','--workspace'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,'Compile failure is not runtime proof'
rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')];bins={j['target']['name']:j for j in rows};binary=Path(bins['opensip_components']['executable']);fixture=Path(bins['supervisor_fixture']['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n');report['fixtureBinding']=dict(binary=str(binary),fixture=str(fixture),fixtureSha256=hashlib.sha256(fixture.read_bytes()).hexdigest());save()
for name,args in [('workspace-tests',[R+'cargo','test','--locked','--offline','--workspace','--no-fail-fast']),('workspace-clippy',[R+'cargo','clippy','--locked','--offline','--workspace','--all-targets','--','-D','warnings']),('operability-source',['python3','-I','-B','tools/check_operability.py','source','--repository',str(W)]),('design-verifier',['python3','-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)]),('diff-check',['git','diff','--check'])]:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb')as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 output=(B/(name+'.log')).read_text(errors='replace');report['runs'].append(dict(name=name,exitCode=r.returncode,testSummaries=re.findall(r'^test result:.*$',output,re.M),failedTestNames=re.findall(r'^test (.+) \.\.\. FAILED$',output,re.M),abortEvidence=[line for line in output.splitlines()if any(w in line for w in ['SIGABRT','signal: 6','IO Safety violation','process didn\'t exit successfully'])]));save()
assert git('rev-parse','HEAD')==report['productCode']and git('rev-parse','HEAD^{tree}')==report['sourceTree']and not git('status','--porcelain')
report.update(owningLaneComplete=True,allPassed=all(x['exitCode']==0 for x in report['runs']),workspaceTestsPassed=report['runs'][0]['exitCode']==0,workspaceClippyPassed=report['runs'][1]['exitCode']==0);save();print('WORKSPACE LANE TERMINAL; inspect report, prior failures retained; no product qualification')
