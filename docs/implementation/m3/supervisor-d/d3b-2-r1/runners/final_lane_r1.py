from pathlib import Path
import subprocess,os,json,tempfile,hashlib,re,time
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;O=F/'final-lane-r1';O.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
expected=json.loads((F/'complete-r2/report.json').read_text())['sourcePins'];negative=json.loads((F/'full-mutations-r1/report.json').read_text());assert negative['all22Caught'] and negative['restored'] and negative['sourcePins']==expected
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in expected.items())
for repo,sha in [(P,'09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9'),(A,'9e89627bef006ab33e1f1036898653e55c0d5fc1'),(W,'09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9')]:assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==sha
assert not subprocess.check_output(['git','status','--porcelain'],cwd=P,text=True).strip()
report={'standing':'D3b-2 COMPLETE CANDIDATE VERIFICATION; NO ACCEPTANCE OR QUALIFICATION IMPLIED','productBase':'09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9','architectureBase':'9e89627bef006ab33e1f1036898653e55c0d5fc1','sourcePins':expected,'rows':[],'suites':{},'targetsSeparated':True,'newPaths':[],'qualification':False}
def save(): (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def run(label,args,repo,env):
 print(label,flush=True);began=time.monotonic()
 with (O/(label+'.log')).open('wb') as log:r=subprocess.run(args,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
 report['rows'].append({'name':label,'exitCode':r.returncode,'passed':r.returncode==0,'seconds':time.monotonic()-began});save();assert r.returncode==0,(label,(O/(label+'.log')).read_text(errors='replace')[-5000:]);return (O/(label+'.log')).read_text(errors='replace')
for side,repo in [('base',P),('candidate',W)]:
 T=Path(tempfile.mkdtemp(prefix='opensip-d3b2-'+side+'-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);target=O/side/'target';target.mkdir(parents=True)
 E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(target),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
 report[side]={'repository':str(repo),'target':str(target),'privateTMPDIR':str(T),'TMPDIRMode':oct(T.stat().st_mode&0o777)}
 for key in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(key,None)
 E.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 print(side+'-fresh-build',flush=True)
 result=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components','-p','opensip-operability'],cwd=repo,env=E,capture_output=True);(O/(side+'-build.log')).write_bytes(result.stderr);(O/(side+'-artifacts.jsonl')).write_bytes(result.stdout);assert result.returncode==0,result.stderr[-5000:]
 bins={};fixture=None
 for line in result.stdout.splitlines():
  j=json.loads(line)
  if j.get('reason')!='compiler-artifact' or not j.get('executable'):continue
  name=j['target']['name']
  if name=='supervisor_fixture':fixture=Path(j['executable'])
  if name in ['opensip_components','opensip_operability'] and j['profile']['test']:
   crate='components' if name=='opensip_components' else 'operability';assert not j['fresh'] and j['target']['src_path']==str(repo/f'crates/{crate}/src/lib.rs');bins[name]=Path(j['executable'])
 assert fixture and len(bins)==2
 (bins['opensip_components'].parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
 for name,binary in bins.items():
  listing=subprocess.check_output([str(binary),'--list'],cwd=repo,env=E,text=True);(O/(side+'-'+name+'-list.log')).write_text(listing)
  if name=='opensip_components':assert listing.count('::d3b2_')==(48 if side=='candidate' else 0)
  if side=='candidate':
   output=run(side+'-'+name+'-new-controls',[str(binary),'d3b2_'],repo,E);assert re.search(r'test result: ok\. [1-9]\d* passed; 0 failed;',output)
  output=run(side+'-'+name,[str(binary)],repo,E);match=re.search(r'test result: ok\. (\d+) passed; (\d+) failed; (\d+) ignored;',output);assert match
  report['suites'][side+'-'+name]={'passed':int(match[1]),'failed':int(match[2]),'ignored':int(match[3]),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'path':str(binary)};save()
 for label,args in [
  ('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','-p','opensip-operability','--all-targets','--','-D','warnings']),
  ('doctests',[R+'cargo','test','--locked','--offline','--doc','-p','opensip-components','-p','opensip-operability']),
  ('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets']),
  ('environment',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v']),
  ('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(repo)]),
  ('operability-lock',[PY,'-I','-B','tools/check_operability.py','lock','--repository',str(repo)]),
  ('no-cgroup',[PY,'-I','-B',str(A/'docs/implementation/m3/supervisor-d/d3b-1-r3/evidence/runners/check_no_cgroup.py'),str(repo)]),
  ('design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(repo)]),
 ]:run(side+'-'+label,args,repo,E)
 if side=='candidate':
  paths=[p for p in expected if p.endswith('.rs')];run('candidate-format',[R+'rustfmt','--edition','2024','--check',*paths],repo,E)
 assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in expected.items())
for name,wanted in [('opensip_components',(194,241)),('opensip_operability',(95,96))]:
 assert tuple(report['suites'][side+'-'+name]['passed'] for side in ['base','candidate'])==wanted
 assert all(report['suites'][side+'-'+name]['failed']==0 and report['suites'][side+'-'+name]['ignored']==0 for side in ['base','candidate'])
assert not subprocess.check_output(['git','status','--porcelain'],cwd=P,text=True).strip()
paths=subprocess.check_output(['git','diff','--name-only'],cwd=W,text=True).splitlines();assert paths==sorted(expected)
assert not subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=W,text=True).strip()
for p in ['Cargo.toml','Cargo.lock',*subprocess.check_output(['git','ls-files','crates/*/Cargo.toml'],cwd=W,text=True).splitlines()]:assert (W/p).read_bytes()==(P/p).read_bytes()
closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",(W/'tools/security/discovery_census.py').read_text()));assert len(closure)==19 and not closure.intersection(paths)
assert all((W/p).read_bytes()==(P/p).read_bytes() for p in closure)
report['censusClosureUnchanged']=True;report['censusRun']=False;report['allPassed']=True;report['packageManifestsUnchanged']=True;report['productionMainGateStillPresent']='LadderUnavailable' in (P/'crates/components/src/supervisor.rs').read_text();report['candidateGateRemoved']=not any(token in (W/'crates/components/src/supervisor.rs').read_text() for token in ['LadderUnavailable','needs_d3b_ladders']);save();print('FINAL LANE PASS: base194/95, candidate241/96, all owning checks, exact source and closure preserved',flush=True)
