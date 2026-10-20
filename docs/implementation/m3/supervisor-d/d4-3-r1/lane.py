from pathlib import Path
import os,subprocess,json,hashlib,tempfile,re,time
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;O=F/'lane-r1';O.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d4-3-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';T=Path(tempfile.mkdtemp(prefix='opensip-d4-3-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(O/'target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['RUST_TEST_THREADS','GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
paths=['crates/host/src/invocation.rs','crates/host/src/invocation_tests.rs'];pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths};rows=[];suites={};mutations=[];base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip();assert base=='3c02526e5fc6e3de83eec8abf04ecdb669a6ca11'
def save():(O/'report.json').write_text(json.dumps(dict(standing='UNREVIEWED D4-3 LANE; NO UNIT ACCEPTANCE',productBase=base,sourcePins=pins,privateTMPDIR=str(T),parallelism='default libtest; no serial override',rows=rows,suites=suites,mutations=mutations),indent=2)+'\n')
def run(name,args,root=W):
 with (O/(name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=root,env=E,stdout=log,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,exitCode=r.returncode,passed=r.returncode==0));save();print(name,r.returncode,flush=True);return r.returncode
flags=['-p','opensip-host','-p','opensip-components']
for label,repo in [('base',P),('candidate',W)]:
 print(label,'BUILD',flush=True);build=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json',*flags],cwd=repo,env=E,capture_output=True);(O/(label+'-build.log')).write_bytes(build.stderr);(O/(label+'-artifacts.jsonl')).write_bytes(build.stdout);assert build.returncode==0,build.stderr[-3000:]
 binaries={};fixture=None
 for line in build.stdout.splitlines():
  try:j=json.loads(line)
  except ValueError:continue
  if j.get('reason')!='compiler-artifact' or not j.get('executable'):continue
  if j['target']['name']=='supervisor_fixture':fixture=Path(j['executable'])
  if j['target']['name'] in ['opensip_components','opensip_host'] and j['profile']['test']:binaries[j['target']['name']]=Path(j['executable'])
 assert fixture and len(binaries)==2
 for name,binary in sorted(binaries.items()):
  (binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n');name=label+'-'+name;print(name,'RUN',flush=True);started=time.monotonic()
  with (O/(name+'.log')).open('wb') as log:r=subprocess.run([str(binary)],cwd=repo,env=E,stdout=log,stderr=subprocess.STDOUT)
  text=(O/(name+'.log')).read_text(errors='replace');summaries=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',text);assert summaries,text[-1000:];summary=summaries[-1];failure_section=text.rsplit('\nfailures:\n',1)[-1].split('\ntest result:')[0];failed=sorted({line.strip() for line in failure_section.splitlines() if line.startswith('    ') and ' ' not in line.strip()}) if int(summary[1]) else [];assert len(failed)==int(summary[1]),(summary,failed)
  suites[name]=dict(exitCode=r.returncode,passed=int(summary[0]),failed=failed,ignored=int(summary[2]),elapsedSeconds=time.monotonic()-started,binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest());save();print(name,suites[name],flush=True)
for pkg,added in [('opensip_host',2),('opensip_components',0)]:
 old=suites['base-'+pkg];new=suites['candidate-'+pkg];assert new['failed']==old['failed'] and new['passed']==old['passed']+added,(pkg,old,new)
for name,args in [('clippy',[R+'cargo','clippy','--locked','--offline',*flags,'--all-targets','--','-D','warnings']),('doctests',[R+'cargo','test','--locked','--offline','--doc',*flags]),('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets']),('format',[R+'rustfmt','--edition','2024','--check',*paths]),('environment',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v']),('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)]),('operability-lock',[PY,'-I','-B','tools/check_operability.py','lock','--repository',str(W)]),('design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])]:assert run(name,args)==0,name
# A source pin is allowed by the accepted plan to catch replacement wildcards;
# appending one is separately refused by the function's deny lint.
p=W/paths[0];raw=p.read_bytes();match=b'''    match request {
        AnalysisRequest::Default => None,
        AnalysisRequest::Analyze => None,
        AnalysisRequest::AnalyzeEphemeral => None,
    }''';assert raw.count(match)==1
changes=[('append-wildcard',raw.replace(match,match[:-5]+b'        _ => None,\n    }'),'compile','unreachable pattern'),('replace-with-wildcard',raw.replace(match,b'    match request { _ => None }'),'runtime','request_classification_is_exhaustive_and_precedes_token_handover'),('skip-classification',raw.replace(b'if let Some(first) = request_excluded_form(&admitted)',b'if let Some(first) = None::<RequestExcludedClass>'),'runtime','request_classification_is_exhaustive_and_precedes_token_handover'),('new-flag-carrier',raw.replace(b'    pub(crate) allow_backup_custody: bool,',b'    pub(crate) allow_backup_custody: bool,\n    pub(crate) policy_grant: bool,'),'compile','pattern does not mention field')]
for name,changed,kind,marker in changes:
 assert changed!=raw
 try:
  p.write_bytes(changed);args=[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib']
  if kind=='compile':args+=['--no-run']
  else:args+=['invocation::tests::request_classification_is_exhaustive_and_precedes_token_handover','--','--exact','--nocapture']
  with (O/('mutation-'+name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT)
  text=(O/('mutation-'+name+'.log')).read_text(errors='replace');caught=r.returncode!=0 and marker in text and ('0 passed; 1 failed' in text if kind=='runtime' else 'could not compile' in text)
  mutations.append(dict(name=name,kind=kind,exitCode=r.returncode,caught=caught));save();print(name,kind,caught,flush=True)
 finally:p.write_bytes(raw)
 assert caught,name
assert run('restored-focused',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','invocation::tests::','--','--nocapture'])==0
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==sha for p,sha in pins.items())
print('D4-3 LANE DONE',flush=True)
