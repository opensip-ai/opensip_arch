from pathlib import Path
import os,subprocess,tempfile,hashlib,json
B=Path(__file__).resolve().parent;N=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');import sys
mode=sys.argv[1];assert mode in ['baseline','candidate'];target='metadata-source-target' if mode=='candidate' else 'baseline-target';deps=N/target/'debug/deps';os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-source-compare-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
args=['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','linker=/usr/bin/cc','-L','dependency='+str(deps)];pins=[]
for crate in ['cargo','anyhow','serde','serde_json']:
 files=list(deps.glob('lib'+crate+'-*.rlib'));assert len(files)==1;args+=['--extern',crate+'='+str(files[0])];raw=files[0].read_bytes();pins.append(dict(path=str(files[0]),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
native_search=[]
for output in sorted((N/target/'debug/build').glob('*/output')):
 for line in output.read_text().splitlines():
  for prefix in ['cargo:rustc-link-search=','cargo::rustc-link-search=']:
   if line.startswith(prefix):
    value=line[len(prefix):];args+=['-L',value];native_search.append(dict(output=str(output),value=value))
exe=B/('package-check-'+mode);args+=[str(B/'package_check.rs'),'-o',str(exe)]
with(B/('package-'+mode+'-build.log')).open('wb')as out:
 p=subprocess.Popen(args,cwd=T,env=E,stdout=out,stderr=subprocess.STDOUT);nice=os.getpriority(os.PRIO_PROCESS,p.pid);assert nice==10;code=p.wait()
if code:print((B/('package-'+mode+'-build.log')).read_text()[-6000:]);raise SystemExit(code)
with(B/('package-'+mode+'.stdout')).open('wb')as out,(B/('package-'+mode+'.stderr')).open('wb')as err:
 p=subprocess.Popen([str(exe),mode],cwd=T,env=E,stdout=out,stderr=err);run_nice=os.getpriority(os.PRIO_PROCESS,p.pid);assert run_nice==10;result=p.wait()
print((B/('package-'+mode+'.stdout')).read_text());print((B/('package-'+mode+'.stderr')).read_text());raw=exe.read_bytes();report=dict(standing='UNREVIEWED EXACT PINNED CARGO METADATA SOURCE SERIALIZATION VIEW PROPOSAL; NO PRODUCT USE/ADMISSION',upstreamCommit='f2d3ce0bd7f24a49f8f72d9000448f8838c4e850',modulePin=dict(path=str(B/'source_view.rs'),bytes=(B/'source_view.rs').stat().st_size,sha256=hashlib.sha256((B/'source_view.rs').read_bytes()).hexdigest()),metadataSourceViewPrototype=True,command=args,linked=pins,nativeSearchFromActualCandidateBuildOutputs=native_search,runtimePin=dict(path=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),buildExit=code,controlExit=result,controls=11,mode=mode,actualPackageSerializer=True,fixtureCodeExecuted=False,fullStartupGoverned=False,observedParentNiceness=10,observedBuildChildNiceness=nice,observedControlChildNiceness=run_nice,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,sourceAdmissionImplemented=False,completeSourceProfile=False,productQualification=False);(B/('package-'+mode+'-checks.json')).write_text(json.dumps(report,indent=2)+'\n');assert result==0
