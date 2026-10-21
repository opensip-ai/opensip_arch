from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'candidate-suites-r2';B.mkdir(exist_ok=False);P=Path('/Users/sb/code/opensip-ai/opensip-rust3-send-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
pins=json.loads((F/'mutation-owning-r2/report.json').read_text())['sourcePins']
def verify():
 for pin in pins:assert hashlib.sha256((P/pin['path']).read_bytes()).hexdigest()==pin['sha256']
verify()
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components','-p','opensip-identity'],cwd=P,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')];bins={j['target']['name']:j for j in rows};fixture=Path(bins['supervisor_fixture']['executable']);component=Path(bins['opensip_components']['executable']);(component.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
base=json.loads((F/'base-r1/report.json').read_text());report=dict(standing='Unaccepted complete4b current candidate components/identity suites; no unit acceptance/production qualification',sourcePins=pins,baseReport=str(F/'base-r1/report.json'),runs=[],fixture=dict(path=str(fixture),sha256=hashlib.sha256(fixture.read_bytes()).hexdigest()),cargoTarget=str(F/'target'),isolatedCandidateWorktree=str(P),productQualification=False)
for name,count in [('opensip_components',362),('opensip_identity',86)]:
 row=bins[name];binary=Path(row['executable']);r=subprocess.run([str(binary)],cwd=P,env=E,capture_output=True);log=r.stdout+r.stderr;(B/(name+'.log')).write_bytes(log);failure=re.findall(r'^test (.+) \.\.\. FAILED$',log.decode(errors='replace'),re.M);base_run=next(x for x in base['runs']if x['name']==name)
 report['runs'].append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M),failureSet=failure,baseFailureSet=base_run['failureSet'],failureSetsEqual=failure==base_run['failureSet'],binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=row['fresh']));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0 and f'{count} passed; 0 failed'.encode()in r.stdout and failure==base_run['failureSet']
verify();report['allPassed']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('CURRENT4b CANDIDATE362/86 PASS; BASE318/86 EMPTY FAILURE SETS EQUAL; NO UNIT ACCEPTANCE')
