from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'receiver-rest-owning-r2';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR='/tmp/opensip-implementation/d2b4a-takeover-2026-10-21/target',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p) for p in paths if p.endswith(".rs")]],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
pins=[]
for path in paths:
 raw=(W/path).read_bytes();pins.append(dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
report=dict(standing='FULL D2B4A SOURCE OWNING CHECKS; INDEPENDENT FULL UNIT REVIEW/ACCEPTANCE REMAIN',sourcePins=pins,runs=[],unitAccepted=False,productQualification=False)
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','--workspace'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);
if r.returncode!=0:
 for line in r.stdout.splitlines():
  if line.startswith(b'{') and (j:=json.loads(line)).get('reason')=='compiler-message' and j['message']['level']=='error':print(j['message'].get('rendered'),flush=True)
 assert False,'compile failure is not runtime proof'
bins={j['target']['name']:j for l in r.stdout.splitlines() if l.startswith(b'{') and (j:=json.loads(l)).get('reason')=='compiler-artifact' and j.get('executable')};binary=Path(bins['opensip_components']['executable']);fixture=Path(bins['supervisor_fixture']['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n');report.update(binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),fixtureSha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
for name,args in [
 ('full-components',[str(binary)]),
 ('full-identity',[R+'cargo','test','--locked','--offline','-p','opensip-identity']),
 ('components-docs',[R+'cargo','test','--locked','--offline','-p','opensip-components','--doc']),
 ('full-operability',[R+'cargo','test','--locked','--offline','-p','opensip-operability','--lib']),
 ('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets']),
 ('workspace-clippy',[R+'cargo','clippy','--locked','--offline','--workspace','--all-targets','--','-D','warnings']),
 ('design-verifier',['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/verify_design.py','--architecture','../opensip_arch']),
 ('diff-check',['/usr/bin/git','diff','--check']),
]:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 output=(B/(name+'.log')).read_text(errors='replace');row=dict(name=name,exitCode=r.returncode)
 if name=='design-verifier':
  try:doc=json.loads(output);row['summary']={k:doc[k]for k in ['ok','status','errors','failures']if k in doc}
  except ValueError:row['summary']='nonJSON output'
 else:row['testSummaries']=re.findall(r'^test result:.*$',output,re.M)
 report['runs'].append(row);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,output[-2200:]if name!='design-verifier'else row['summary'])

for row in pins:assert hashlib.sha256((W/row['path']).read_bytes()).hexdigest()==row['sha256']
report['inheritedWorkspaceTestFailure']=str(F/'inherited-cli-source-guard-failure.json');report['workspaceTestsPassed']=False;report['allPassed']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('RECEIVER COMPILED; ACTUAL RUNTIME CONTROLS STILL REQUIRED',flush=True)
