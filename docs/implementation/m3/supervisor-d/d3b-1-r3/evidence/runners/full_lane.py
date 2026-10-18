from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re,sys
W=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';F=Path(__file__).parent;B=Path('/tmp/opensip-implementation/d3b1-full-takeover-r1');B.mkdir(exist_ok=False)
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-full-',dir=D));T.chmod(0o700)
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(w,*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=w,env=E)
old=git(W,'rev-parse','HEAD').decode().strip();base=git(P,'rev-parse','HEAD').decode().strip();arch=git(A,'rev-parse','HEAD').decode().strip();edited=git(W,'diff','--name-only').decode().splitlines();assert len(edited)==13
for path in edited:assert git(W,'show',old+':'+path)==git(P,'show',base+':'+path),path
(B/'pre-rebase.patch').write_bytes(git(W,'diff','--binary'))
git(W,'switch','--detach',base)
assert git(W,'diff','--name-only').decode().splitlines()==edited
BW=W.parent/'opensip-d3b1-base-takeover';assert not BW.exists();git(P,'worktree','add','--detach',str(BW),base)
rows=[];suites={}
def save():
 (B/'checks.json').write_text(json.dumps(dict(standing='UNREVIEWED D3b-1 FULL LANE; NOT ACCEPTANCE',base=base,architectureBase=arch,originalDraftBase=old,worktree=str(W),baselineWorktree=str(BW),rows=rows,suites=suites,privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True,allRequiredRowsPassed=bool(rows) and all(r['passed'] for r in rows)),indent=2)+'\n')
def run(name,args,cwd=W):
 with (B/(name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=cwd,env=E,stdout=log,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,args=[str(x) for x in args],exitCode=r.returncode,passed=r.returncode==0));save();print(name,r.returncode,flush=True)
 return r.returncode
for path in edited:
 if path.endswith('.rs'):
  file=W/path
  file.write_bytes(subprocess.check_output([R+'rustfmt','--edition','2024','--emit','stdout'],input=file.read_bytes(),env=E,cwd=W))
# Each executable test target is run, including operability integration targets.
pkgs=['opensip-components','opensip-platform','opensip-operability'];flags=sum((['-p',p] for p in pkgs),[])
for label,root in [('base',BW),('candidate',W)]:
 args=[R+'cargo','test','--locked','--offline','--no-run','--message-format=json',*flags]
 r=subprocess.run(args,cwd=root,env=E,capture_output=True);(B/(label+'-build.log')).write_bytes(r.stderr);(B/(label+'-build-artifacts.jsonl')).write_bytes(r.stdout);assert r.returncode==0
 artifacts=[];fixture=None
 for raw in r.stdout.splitlines():
  try:m=json.loads(raw)
  except ValueError:continue
  if m.get('reason')!='compiler-artifact' or not m.get('executable'):continue
  if m['target']['name']=='supervisor_fixture':fixture=Path(m['executable']);continue
  if m['profile']['test'] and any(k in ['lib','test'] for k in m['target']['kind']):artifacts.append(m)
 assert fixture and len(artifacts)>=5
 for m in artifacts:
  binary=Path(m['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
  name=label+'-'+m['target']['name'];log=B/(name+'.log')
  with log.open('wb') as out:r=subprocess.run([str(binary),'--test-threads=1'],cwd=root,env=E,stdout=out,stderr=subprocess.STDOUT)
  text=log.read_text(errors='replace');summary=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',text);assert summary,(name,r.returncode)
  failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',text,re.M)));assert int(summary[-1][1])==len(failed),(name,failed,summary)
  suites[name]=dict(exitCode=r.returncode,passed=int(summary[-1][0]),failed=failed,ignored=int(summary[-1][2]),fixtureSha256=hashlib.sha256(fixture.read_bytes()).hexdigest());save();print(name,summary[-1],flush=True)
 run(label+'-doctests',[R+'cargo','test','--locked','--offline','--doc',*flags],root)
for name in [n for n in suites if n.startswith('candidate-')]:
 oldrow=suites[name.replace('candidate-','base-',1)];new=suites[name];rows.append(dict(name=name+'-comparison',passed=new['failed']==oldrow['failed'] and new['passed']>=oldrow['passed'],basePassed=oldrow['passed'],candidatePassed=new['passed'],inheritedFailures=oldrow['failed'],candidateFailures=new['failed']))
save()
run('clippy',[R+'cargo','clippy','--locked','--offline',*flags,'--all-targets','--','-D','warnings'])
run('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets'])
fmt=[]
for path in edited:
 if path.endswith('.rs'):
  original=git(P,'show',base+':'+path);current=(W/path).read_bytes();formatter=[R+'rustfmt','--edition','2024','--emit','stdout']
  fmt.append(dict(path=path,baseClean=subprocess.check_output(formatter,input=original,env=E)==original,candidateClean=subprocess.check_output(formatter,input=current,env=E)==current))
(B/'formatting.json').write_text(json.dumps(fmt,indent=2)+'\n');rows.append(dict(name='formatting',passed=all(x['baseClean'] and x['candidateClean'] for x in fmt)));save()
for name,args in [
 ('environment-exceptions',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v']),
 ('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)]),
 ('operability-lock',[PY,'-I','-B','tools/check_operability.py','lock','--repository',str(W)]),
 ('operability-enforcement-controls',[PY,'-I','-B','tools/tests/test_check_operability.py','-v']),
 ('operability-catalog-controls',[PY,'-I','-B','tools/tests/test_operability_catalog.py','-v']),
 ('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)]),
 ('no-cgroup',[PY,'-I','-B',str(F/'check_no_cgroup.py'),str(W)])]:run(name,args)
# Strict source closure and unchanged dependency manifests, no private census replay.
src=(W/'tools/security/discovery_census.py').read_text();closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",src));hit=sorted(closure&set(edited));rows.append(dict(name='census-closure-unchanged',passed=len(closure)>10 and not hit,closureCount=len(closure),intersectingChangedPaths=hit))
manifest_changes=[p for p in edited if p.endswith('Cargo.toml') or p=='Cargo.lock'];rows.append(dict(name='package-edges-unchanged',passed=not manifest_changes,changed=manifest_changes))
# Scanner mutation proves filename and negated cfg cannot bypass the guard.
p=W/'crates/components/src/supervisor_tests.rs';raw=p.read_bytes();p.write_bytes(raw+b'\n#[cfg(not(test))]\n// '+b'c'+b'group'+b' bypass canary\n')
try:
 r=subprocess.run([PY,'-I','-B',str(F/'check_no_cgroup.py'),str(W)],env=E,capture_output=True);(B/'no-cgroup-mutation.json').write_bytes(r.stdout);caught=r.returncode==1 and b'supervisor_tests.rs' in r.stdout
finally:p.write_bytes(raw)
rows.append(dict(name='no-cgroup-scanner-mutation',passed=caught));save()
assert git(P,'rev-parse','HEAD').decode().strip()==base and git(A,'rev-parse','HEAD').decode().strip()==arch
print('FULL LANE DONE',all(r['passed'] for r in rows),flush=True)
