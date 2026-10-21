from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-route-mutants-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());original={p:(W/p).read_bytes()for p in paths}
def pin(p,b):return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
core='crates/components/src/session_factory.rs';spec='crates/components/src/session_factory/spec.rs';test='session_factory::tests::'
cases=[
 ('native-budget-mapped-to-corrupt','crates/host/src/launch_recheck.rs','TreeReadFailure::Budget(budget) => RecheckFailure::Budget(budget),','TreeReadFailure::Budget(_budget) => RecheckFailure::Corrupt(CorruptCause::Association),','launch_recheck::tests::actual_factory_one_short_native_open_and_read_keep_budget_route'),
 ('native-io-mapped-to-corrupt','crates/host/src/launch_recheck.rs','TreeReadFailure::Io { call, error } => RecheckFailure::Io { call, error },','TreeReadFailure::Io { .. } => RecheckFailure::Corrupt(CorruptCause::Association),','launch_recheck::tests::actual_native_factory_preserves_corruption_and_read_io_routes'),
]

report=dict(standing='D4-4 native adapter compiled runtime mapping mutants, witnessed through actual factory. Provider-spoken controls and complete-unit review remain owed. Compile failure is never a kill. Mutable target binaries are not archived executables.',sourcePins=[pin(p,b)for p,b in original.items()],cases=[],allKilled=False,sourceRestored=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def build(out):
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p','opensip-host'],cwd=W,env=E,capture_output=True);(out/'build.log').write_bytes(r.stderr);(out/'artifacts.jsonl').write_bytes(r.stdout)
 assert r.returncode==0,'Compile failure does not establish mutation kill: '+str(out)
 rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_host'];assert len(rows)==1;return rows[0]
save()
try:
 for name,path,before,after,witness in cases:
  assert all((W/p).read_bytes()==b for p,b in original.items());base=original[path].decode();assert base.count(before)==1,(name,base.count(before));mutated=base.replace(before,after,1).encode();out=B/name;out.mkdir();(out/'mutated-source.rs').write_bytes(mutated)
  row=dict(name=name,target=path,before=pin(path,original[path]),mutated=pin(path,mutated),witness=witness,killed=False);report['cases'].append(row);save()
  try:
   (W/path).write_bytes(mutated);artifact=build(out);assert artifact['fresh']is False;binary=Path(artifact['executable']);row.update(compilerArtifactCached=False,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest());r=subprocess.run([str(binary),witness,'--exact'],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(out/'runtime.log').write_bytes(log);row.update(exitCode=r.returncode,failureSet=re.findall(r'^test (.+) \.\.\. FAILED$',log.decode(errors='replace'),re.M),summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M));row['killed']=r.returncode==101 and row['failureSet']==[witness]and b'0 passed; 1 failed'in log;save();assert row['killed'],name
  finally:
   (W/path).write_bytes(original[path]);row['targetRestored']=(W/path).read_bytes()==original[path];save()
  assert all((W/p).read_bytes()==b for p,b in original.items());print('COMPILED RUNTIME KILL '+name,flush=True)
 report['allKilled']=len(report['cases'])==2 and all(row['killed']for row in report['cases'])
finally:
 for p,b in original.items():assert (W/p).read_bytes()==b,p
 report['sourceRestored']=True;save()
# Recompile and rerun the restored current owning controls, never leave the
# last mutant executable as the only observed test artifact at this target.
out=B/'restored';out.mkdir();artifact=build(out);binary=Path(artifact['executable']);r=subprocess.run([str(binary),'launch_recheck::tests'],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(out/'runtime.log').write_bytes(log);report['restored']=dict(exitCode=r.returncode,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=artifact['fresh'],summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M),allPassed=r.returncode==0 and b'9 passed; 0 failed'in log);save();assert report['allKilled']and report['sourceRestored']and report['restored']['allPassed'];print('BOTH NATIVE ROUTE MUTANTS KILLED; EXACT SOURCES RESTORED; CURRENT9OWNING CONTROLS PASS',flush=True)
