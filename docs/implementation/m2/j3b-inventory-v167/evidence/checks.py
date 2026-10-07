import datetime,hashlib,json,os,pathlib,re,subprocess,tempfile,time
product=pathlib.Path('/tmp/opensip-implementation/j3b-authoring/product');arch=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch');root=pathlib.Path('/tmp/opensip-implementation/j3b-qualification-preparation-r3');darwin=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());lock=darwin/'opensip-lanes.lock'
metadata=json.loads((root/'qualification-input.json').read_text());head=metadata['temporaryQualificationCommit'];assert metadata['explicitTemporaryCommitAuthorization'] is True and metadata['mainUnmodified'] is True
env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR='/tmp/opensip-implementation/j3b-authoring/target',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/cc',AR='/usr/bin/ar',RANLIB='/usr/bin/ranlib',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE','RUSTC_BOOTSTRAP','OPENSIP_X9_RUN_SET','OPENSIP_X9_CENSUS_ONLY','OPENSIP_X9_ROWS','OPENSIP_X9_RELEASE_ABSENCE']:env.pop(key,None)
scratch=pathlib.Path(tempfile.mkdtemp(prefix='opensip-j3b-qualified-',dir=darwin));scratch.chmod(0o700);env['TMPDIR']=str(scratch)
rows=[];owned=False

def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=product,env=env,text=True).strip()
def clean():
 snapshot=json.loads(pathlib.Path('/tmp/opensip-implementation/j3b-source-freeze-r3/source-snapshot.json').read_text())
 for member in snapshot['files']:
  raw=(product/member['path']).read_bytes();assert len(raw)==member['bytes'] and hashlib.sha256(raw).hexdigest()==member['sha256'],'frozen source changed: '+member['path']
 for repository,expected in [(pathlib.Path('/Users/sb/code/opensip-ai/opensip'),snapshot['productBase']),(arch,snapshot['architectureBase'])]:
  actual=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=repository,env=env,text=True).strip();assert actual==expected,'main repository HEAD changed'
  subprocess.run(['/usr/bin/git','diff','--quiet','HEAD','--'],cwd=repository,env=env,check=True)
 assert git('rev-parse','HEAD')==head,'product HEAD changed'
 assert git('status','--porcelain')=='','product worktree changed'
 assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
def pin(path):
 raw=path.read_bytes();return {'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def save():
 (root/'progress.json').write_text(json.dumps({'standing':'ACTIVE ISOLATED J3B VERIFICATION; NO MATRIX PASS YET','productCommit':head,'scratch':str(scratch),'commands':rows,'installationAbsent':True,'private413Read':False,'laneOwned':owned},indent=2)+'\n')
def acquire(label):
 global owned
 assert not owned
 while not owned:
  try:lock.mkdir();owned=True
  except FileExistsError:print('Waiting for the lane: '+label,flush=True);time.sleep(15)
 save();clean()
def release():
 global owned
 if owned:lock.rmdir();owned=False;save()
def busy():
 names={'cargo','rustc','cargo-clippy','clippy-driver','cc','clang','clang++','ar','ld'}
 return [line for line in subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True).splitlines() if line.split() and (pathlib.Path(line.split()[-1]).name in names or re.search(r'/deps/[A-Za-z0-9_]+-[0-9a-f]{16}$',line.split()[-1]))]
def quiet(label):
 while True:
  active=busy()
  if not active:break
  print('Waiting for idle compilers/tests: '+label,flush=True);time.sleep(15)
def run(label,cmd,nice=10,extra=None,expected=0):
 assert owned;clean();quiet(label);subenv=dict(env);subenv.update(extra or {})
 started=datetime.datetime.now(datetime.UTC).isoformat();print('START '+label,flush=True)
 with (root/(label+'.log')).open('w') as out:result=subprocess.run(['/usr/bin/nice','-n',str(nice),*cmd],cwd=product,env=subenv,stdout=out,stderr=subprocess.STDOUT)
 rows.append({'label':label,'command':cmd,'nice':nice,'extraEnvironment':extra or {},'startedAt':started,'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'exitCode':result.returncode,'expectedExitCode':expected});save();print(json.dumps(rows[-1]),flush=True);clean();assert result.returncode==expected,label+' failed; see retained log'
def python(label,args,nice=10):run(label,['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',*args],nice)
def target_args(package,target):return ['cargo','test','--locked','--offline','-p',package,'--features','crash-matrix','--test',target,'x9_6_matrix','--','--exact','--test-threads=1']
try:
 clean();assert git('merge-base','--is-ancestor','43ea32a6419c961cec1e0ba30d7dd791acbd7f49',head)==''
 required={'storage':product/'crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json','host':product/'crates/host/tests/fixtures/crash-matrix/required-runs.v1.json'}
 for name,expected in [('storage',403),('host',102)]:
  data=json.loads(required[name].read_text());actual=len(data['runs']);assert actual==expected,(name,actual)
 import importlib.util
 spec=importlib.util.spec_from_file_location('selected_checker',product/'tools/check_crash_matrix.py');selected_checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(selected_checker)
 for fixture in required.values():selected_checker.load(fixture)
 acquire('complete serial library controls')
 run('complete-feature-library-controls',['cargo','test','--locked','--offline','-p','opensip-security','-p','opensip-storage','-p','opensip-host','-p','opensip-platform','--features','crash-matrix','--lib','--','--test-threads=1'])
 python('checker-controls',['-m','unittest','discover','-s','tools/tests','-p','test_check_crash_matrix.py'])
 release()
 acquire('release absence')
 run('release-build',['cargo','build','--release','--locked','--offline','-p','opensip-cli'])
 python('release-scan',['tools/check_crash_matrix.py','release-absence','--repository',str(product),'--binary',str(pathlib.Path('/tmp/opensip-implementation/j3b-authoring/target/release/opensip'))])
 scan=json.loads((root/'release-scan.log').read_text());assert scan['passed'] and scan['found']==[]
 for package in ['storage','host']:
  label=package+'-release-guard';run(label,['cargo','build','--release','--locked','--offline','-p','opensip-'+package,'--features','crash-matrix'],expected=101)
  assert 'the crash-matrix feature is test-only' in (root/(label+'.log')).read_text(),label+' lacks the expected compile guard'
 absence={**scan,'featureBuildRefused':True,'features':[],'profile':'release'};(root/'release-absence.json').write_text(json.dumps(absence,sort_keys=True,separators=(',',':')))
 release()
 targets=[('storage','opensip-storage','commit_tests'),('host','opensip-host','commit_matrix_tests')]
 prefix='codex-j3b-isolated-attempt3-'+head[:12]
 acquire('census-only set')
 for name,package,target in targets:
  tag=prefix+'-census-'+name;out=product/'target/opensip-x9'/tag;assert not out.exists(),str(out)
  run(name+'-census',target_args(package,target),0,{'OPENSIP_X9_RUN_SET':tag,'OPENSIP_X9_CENSUS_ONLY':'1'})
  census=json.loads((out/'census.json').read_text());reference=json.loads((arch/'docs/implementation/m2/reviews/grok2-x3c3-r1/evidence/census'/ (name+'-census.json')).read_text());assert census['points']==reference['points'],name+' point names/counts/order differ; STOP'
  predicted=product/'target/opensip-x9'/('j3b-unfrozen-census-20261006-'+name)
  traces=sorted(predicted.glob('census-trace*.txt'));assert traces,'missing predicted per-part census'
  assert {p.name for p in out.glob('census-trace*.txt')}=={p.name for p in traces},'census part names differ'
  for trace in traces:
   def sequence(path):
    points=[]
    for line in path.read_text().splitlines():
     fields=line.split('|')
     if len(fields)>=4 and fields[0].isdigit() and fields[1].isdigit():points.append(tuple(fields[:4]))
     elif len(fields)>=5 and fields[1].isdigit() and fields[2].isdigit():points.append(tuple(fields[:5]))
    return points
   expected_sequence=sequence(trace);assert expected_sequence,'empty predicted point sequence'
   assert sequence(out/trace.name)==expected_sequence,name+' per-part point sequence differs; STOP'
  shutil_marker={'path':str(out),'census':pin(out/'census.json'),'exactAcceptedPointNamesCountsAndOrder':True};(root/(name+'-census-match.json')).write_text(json.dumps(shutil_marker,indent=2)+'\n')
 release()
 sets={name:[] for name,_,_ in targets}
 for repetition in [1,2]:
  acquire('whole lead set '+str(repetition))
  for name,package,target in targets:
   tag=prefix+'-r'+str(repetition)+'-'+name;out=product/'target/opensip-x9'/tag;assert not out.exists(),str(out)
   run('lead-r'+str(repetition)+'-'+name,target_args(package,target),0,{'OPENSIP_X9_RUN_SET':tag,'OPENSIP_X9_RELEASE_ABSENCE':str(root/'release-absence.json')});sets[name].append(str(out))
  release()
 acquire('real two-target check')
 args=['tools/check_crash_matrix.py','check','--repository',str(product),'--commit',head]
 for name,_,_ in targets:args+=['--target',name,str(required[name]),*sets[name]]
 python('matrix-check',args,0);report=json.loads((root/'matrix-check.log').read_text());assert report['matrixPass'] is True
 release();clean();save();(root/'qualification.json').write_text(json.dumps({'standing':'ISOLATED J3B MATRIX VERIFICATION COMPLETE; NO SOURCE ACCEPTANCE OR MAIN INTEGRATION','productCommit':head,'commands':rows,'scratch':str(scratch),'sets':sets,'matrixCheck':pin(root/'matrix-check.log'),'releaseAbsence':pin(root/'release-absence.json'),'matrixPass':True,'installationAbsent':True,'private413Read':False,'RWIntegrated':False,'J4aTouched':False,'providerLaunched':False,'productQualification':False},indent=2)+'\n');print('ALL CHECKS PASSED; EVIDENCE REVIEW PENDING',flush=True)
finally:release()
