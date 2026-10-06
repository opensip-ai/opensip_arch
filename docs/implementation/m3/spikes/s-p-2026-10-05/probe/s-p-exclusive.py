import argparse,datetime,hashlib,json,os,pathlib,shutil,subprocess,tempfile,time
args=argparse.ArgumentParser();args.add_argument('--rust-input',type=pathlib.Path,required=True);args.add_argument('--ts-input',type=pathlib.Path,required=True);args=args.parse_args()
p=pathlib.Path('/tmp/opensip-implementation/s-p-acquisition');source=p/'verified-probe-source';old=json.loads((p/'probe-results-final.json').read_text());rust=pathlib.Path(old['rustSysroot']);node=pathlib.Path(old['node']);ts=pathlib.Path(old['typescriptDirectory']);darwin=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip();lock=pathlib.Path(darwin)/'opensip-lanes.lock';created=False
while not created:
 try:lock.mkdir();created=True
 except FileExistsError:print('Waiting for the owned lane directory to become available.',flush=True);time.sleep(15)
try:
 # A process outside the lane protocol must finish; do not kill it.
 processes=subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True)
 active=[line.strip() for line in processes.splitlines() if line.split() and pathlib.Path(line.split()[-1]).name=='cargo']
 if active:raise RuntimeError('An active build exists outside the owned lane. Retry after it finishes.')
 started=datetime.datetime.now(datetime.UTC).isoformat();out=pathlib.Path(tempfile.mkdtemp(prefix='opensip-s-p-exclusive-',dir=darwin));os.chmod(out,0o700)
 for f in source.iterdir():shutil.copyfile(f,out/f.name)
 env=dict(os.environ);env.update(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(out),DYLD_LIBRARY_PATH=str(rust/'lib')+':'+str(rust/'lib/rustlib/aarch64-apple-darwin/lib'));env.pop('RUSTC_BOOTSTRAP',None)
 sdk=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip();commands=[]
 def run(label,cmd,child=env):
  r=subprocess.run(['/usr/bin/nice','-n','10',*map(str,cmd)],env=child,cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/(label+'.log')).write_text(r.stdout);commands.append({'label':label,'command':list(map(str,cmd)),'exitCode':r.returncode,'output':r.stdout});print(json.dumps({'label':label,'exitCode':r.returncode}),flush=True);return r
 r=run('rustc-version',[rust/'bin/rustc','-vV']);assert r.returncode==0
 binary=out/'callbacks';r=run('rust-driver-build',[rust/'bin/rustc','--edition','2024','--sysroot',rust,'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc',out/'callbacks.rs','-o',binary],dict(env,SDKROOT=sdk,RUSTC_BOOTSTRAP='1'));assert r.returncode==0 and not r.stdout
 def rust_run(label,file):return run(label,[binary,'--crate-type','lib','--edition','2024','--sysroot',rust,'--emit','metadata',file,'--out-dir',out])
 r=rust_run('rust-own-positive',out/'own_input.rs');assert r.returncode==0 and 'after_analysis' in r.stdout
 r=rust_run('rust-own-negative',out/'own_invalid.rs');assert r.returncode!=0 and 'E0308' in r.stdout and 'after_analysis' not in r.stdout
 # Exact selected module inspected before invoking this script; no scripts,
 # proc-macro dependencies or extern metadata supplied to the probe compiler.
 r=rust_run('rust-t2-module',args.rust_input);assert r.returncode==0 and 'after_analysis' in r.stdout
 r=run('node-version',[node,'--version']);assert r.returncode==0
 def ts_run(label,file):return run(label,[node,out/'typescript_probe.cjs',ts/'lib/typescript.js',file])
 r=ts_run('typescript-own-positive',out/'own_input.ts');assert r.returncode==0 and not json.loads(r.stdout)['diagnostics']
 r=ts_run('typescript-own-negative',out/'own_invalid.ts');assert r.returncode!=0 and any(d['code']==2322 for d in json.loads(r.stdout)['diagnostics'])
 r=ts_run('typescript-t2-source',args.ts_input);t2=json.loads(r.stdout);assert t2['createProgramAvailable'] and any(pathlib.Path(f).resolve()==args.ts_input.resolve() for f in t2['sourceFiles'])
 files=[]
 for f in sorted(out.iterdir()):
  if f.is_file():raw=f.read_bytes();files.append({'path':str(f),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 result={'standing':'PRELIMINARY S-P FEASIBILITY PROBE, NOT S-M / Q6 / PRODUCTION','directory':str(out),'rustSysroot':str(rust),'node':str(node),'typescriptDirectory':str(ts),'sdkRoot':sdk,'commands':commands,'probeFiles':files,'inputFiles':[{'path':str(f),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in (args.rust_input,args.ts_input)],'lane':{'path':str(lock),'ownedByThisProcess':True,'startedAt':started,'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'otherBuildsBeforeStart':active,'nice':10},'rustCallbacksPassed':True,'typescriptApiPassed':True,'bootstrapForProbeWrapperCompilationOnly':True,'bootstrapForAnalyzedInputs':False,'repositoryCodeExecuted':False,'T1ProducerRan':False,'T1FixtureCompiled':False,'confinementClaimed':False,'productQualification':False,'productionToolchainSelected':False,'typescriptT2DiagnosticsDisclosed':t2['diagnostics']}
 assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists();(p/'exclusive-probe-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'report':str(p/'exclusive-probe-results.json'),'rustCallbacksPassed':True,'typescriptApiPassed':True,'typescriptT2DiagnosticCount':len(t2['diagnostics'])}),flush=True)
finally:
 if created:lock.rmdir()
