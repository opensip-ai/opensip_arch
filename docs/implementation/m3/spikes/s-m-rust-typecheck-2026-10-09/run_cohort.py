from pathlib import Path,PurePosixPath
import os,sys,json,time,hashlib,subprocess,tempfile,stat,statistics,datetime,struct,tomllib
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';SYS=C/'g2-rust-1.95/sysroot';build=json.loads((B/'build.json').read_text());EXE=Path(build['executable']);assert hashlib.sha256(EXE.read_bytes()).hexdigest()==build['sha256'];sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
from store import verify
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=m['counts']['rust']['medium']['devIds'];assert len(ids)==7 and all(not entries[i]['heldOut']for i in ids);overlay=next(w for w in m['workspaces']if w['id']=='mr-rs-medium-serde-json');assert overlay['heldOut']is False and all(not entries[i]['heldOut']for i in overlay['memberIds']);D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=D/'opensip-lanes.lock';owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned Rust measurement lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']];T=Path(tempfile.mkdtemp(prefix='opensip-sm-rust-cohort-',dir=D));T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));
 if 'HOME'in os.environ:env['HOME']=os.environ['HOME']
 for key in ['LANG','LC_ALL','TZ']:
  if key in os.environ:env[key]=os.environ[key]
 sets=[dict(id=i,virtualRoot=str(C/'t2-corpus-c8cc48e1/store'/entries[i]['treeDigest']['value']),members=[dict(entry=i,prefix='')])for i in ids];sets.append(dict(id=overlay['id'],virtualRoot=str(C/'t2-corpus-c8cc48e1/workspaces'/overlay['id']),members=[dict(entry=x['entry'],prefix=x['mount']+'/')for x in overlay['overlay']['members']],overlayDefinition=overlay['overlay'],overlayDigest=overlay['overlayDigest']));results=[]
 for workload in sets:
  id_=workload['id'];virtualRoot=Path(workload['virtualRoot']);files={};rows=[];excluded=[];verifications=[]
  for member in workload['members']:
   entry=entries[member['entry']];root=C/'t2-corpus-c8cc48e1/store'/entry['treeDigest']['value'];verifications.append(dict(id=entry['id'],verified=verify(root,entry),commit=entry['commit']));prefix=member['prefix']
   if prefix:assert (virtualRoot/prefix.rstrip('/')).is_symlink()and (virtualRoot/prefix.rstrip('/')).resolve()==root.resolve()
   for directory,dirs,names in os.walk(root,followlinks=False):
    for name in list(dirs):
     p=Path(directory)/name
     if p.is_symlink():excluded.append(dict(path=prefix+str(p.relative_to(root)),kind='symlink-directory'));dirs.remove(name)
    for name in names:
     p=Path(directory)/name;info=p.lstat();rel=prefix+str(p.relative_to(root))
     if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
     fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
     with os.fdopen(fd,'rb')as f:
      before=os.fstat(f.fileno());assert(info.st_dev,info.st_ino)==(before.st_dev,before.st_ino);data=f.read();after=os.fstat(f.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)and len(data)==info.st_size
     assert rel not in files;files[rel]=data;rows.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
  rows.sort(key=lambda r:r['path'].encode());encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))
  for row in rows:
   name=str(virtualRoot/row['path']).encode();data=files[row['path']];encoded+=struct.pack('>Q',len(name))+name+struct.pack('>Q',len(data))+data
  mp=T/(id_+'-source-map.bin');mp.write_bytes(encoded);mp.chmod(0o400);mapDigest=hashlib.sha256(encoded).hexdigest();documents={};skipped=[]
  for path,data in files.items():
   if PurePosixPath(path).name=='Cargo.toml':
    try:documents[path]=tomllib.loads(data.decode('utf8'))
    except (UnicodeError,tomllib.TOMLDecodeError)as e:skipped.append(dict(manifest=path,reason='declarative-manifest-unreadable',exceptionType=type(e).__name__))
  roots=[]
  for path,doc in sorted(documents.items()):
   package=doc.get('package');base=PurePosixPath(path).parent
   if not isinstance(package,dict):skipped.append(dict(manifest=path,reason='no-package-declaration'));continue
   lib=doc.get('lib',{});source=lib.get('path','src/lib.rs')if isinstance(lib,dict)else None
   if not isinstance(source,str):skipped.append(dict(manifest=path,reason='nonstring-library-path'));continue
   logical=Path(os.path.normpath(str(base/source))).as_posix()
   if logical not in files or ('lib'not in doc and package.get('autolib')is False):skipped.append(dict(manifest=path,reason='no-retained-declared-library-root',candidate=logical));continue
   edition=package.get('edition','2015');editionOrigin=path
   if isinstance(edition,dict)and edition.get('workspace')is True:
    candidates=[]
    if isinstance(package.get('workspace'),str):candidates=[Path(os.path.normpath(str(base/package['workspace']/'Cargo.toml'))).as_posix()]
    else:
     cursor=base
     while True:
      candidates.append((cursor/'Cargo.toml').as_posix())
      if cursor==cursor.parent:break
      cursor=cursor.parent
    edition=None
    for candidate in candidates:
     value=documents.get(candidate,{}).get('workspace',{}).get('package',{}).get('edition')
     if isinstance(value,str):edition=value;editionOrigin=candidate;break
   name=lib.get('name',str(package.get('name','')).replace('-','_'));types='proc-macro'if lib.get('proc-macro')is True else ','.join(lib.get('crate-type',['lib']));features=doc.get('features',{});defaults=features.get('default',[])if isinstance(features,dict)else [];selected=set();todo=list(defaults)if isinstance(defaults,list)else []
   while todo:
    value=todo.pop()
    if not isinstance(value,str)or '/'in value or value.startswith('dep:')or value in selected:continue
    selected.add(value);more=features.get(value,[])
    if isinstance(more,list):todo.extend(more)
   if not isinstance(edition,str):skipped.append(dict(manifest=path,reason='unresolved-workspace-edition'));continue
   roots.append(dict(manifest=path,root=logical,packageName=package.get('name'),crateName=name,crateTypes=types,edition=edition,editionOrigin=editionOrigin,localDefaultFeatureLabels=sorted(selected),buildScriptPresent=(base/'build.rs').as_posix()in files or isinstance(package.get('build'),str),buildScriptExecuted=False,dependencyExternsSupplied=False))
  inventory=dict(id=id_,selection='every retained Cargo.toml package with explicit/default retained library root; direct rustc local-default-feature cohort, not Cargo workspace or native profile',virtualRoot=str(virtualRoot),sourceMapSha256=mapDigest,sourceMapBytes=len(encoded),files=rows,nonregularExcluded=excluded,members=verifications,libraryRoots=roots,skippedManifests=skipped,overlay=workload.get('overlayDefinition'),overlayDigest=workload.get('overlayDigest'));(B/f'{id_}-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n');samples=[];stable=None
  for n in range(10):
   rootResults=[];wholeStart=time.monotonic_ns()
   for ordinal,root in enumerate(roots):
    output=T/(id_+'-'+str(n)+'-'+str(ordinal));output.mkdir(mode=0o700);out=B/f'{id_}-{n}-{ordinal}.stdout';err=B/f'{id_}-{n}-{ordinal}.stderr';cmd=['/usr/bin/nice','-n','10',str(EXE),'--prepared-map',str(mp),'--crate-type',root['crateTypes'],'--crate-name',root['crateName'],'--edition',root['edition'],'--sysroot',str(SYS),'--emit','metadata',str(virtualRoot/root['root']),'--out-dir',str(output)]
    for feature in root['localDefaultFeatureLabels']:cmd+=['--cfg','feature='+json.dumps(feature,ensure_ascii=False)]
    start=time.monotonic_ns()
    with out.open('wb')as o,err.open('wb')as e:
     child=subprocess.Popen(cmd,cwd=T,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
    elapsed=time.monotonic_ns()-start;events=[json.loads(line)for line in out.read_text().splitlines()if line.startswith('{')];assert not list(output.iterdir());output.rmdir();rootResults.append(dict(rootOrdinal=ordinal,manifest=root['manifest'],exitCode=child.returncode,afterExpansionReached=any(e['event']=='after_expansion'for e in events),afterAnalysisReachedSuccessfully=any(e['event']=='after_analysis'for e in events),events=events,wholeProcessNanos=elapsed,rssNative=int(usage.ru_maxrss),rssUnit='bytes',stdout=str(out),stderr=str(err)))
   elapsed=time.monotonic_ns()-wholeStart;shape=[{k:v for k,v in q.items()if k not in ['wholeProcessNanos','rssNative','stdout','stderr']}for q in rootResults]
   if stable is None:stable=shape
   else:assert shape==stable,(id_,n,'compiler phase/exit drift')
   samples.append(dict(ordinal=n,warmup=n<3,totalRootSetNanos=elapsed,libraryRoots=rootResults));print(id_,n,'roots',len(roots),'after-analysis',sum(q['afterAnalysisReachedSuccessfully']for q in rootResults),'ns',elapsed,flush=True)
  values=[q['totalRootSetNanos']for q in samples if not q['warmup']];results.append(dict(id=id_,heldOut=False,inventory=inventory,stablePhaseShape=stable,runs=samples,medianRootSetNanos=statistics.median(values),maxRootSetNanos=max(values),SM4PlaceholderFilled=False,SM11PlaceholderFilled=False));mp.unlink();(B/'progress.json').write_text(json.dumps(dict(standing='UNREVIEWED PRELIMINARY DIRECT-RUSTC CONFIGURED LIBRARY COHORT',workloads=results),indent=2)+'\n')
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY DIRECT-RUSTC LIBRARY COHORT; MISSING DEPENDENCY/BUILD/PROC-MACRO CONTEXT EXPLICIT',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),platformVersion=subprocess.check_output(['/usr/bin/sw_vers']).decode(),workloads=results,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,HOMEUnchanged=True,CARGO_HOME='/Users/sb/.cargo',CARGORun=False,repositoryBuildOrProcMacroOrPackageScriptExecuted=False,dependencyExternsSupplied=False,buildOutputInvented=False,RUSTC_BOOTSTRAPAnalyzedInputs=False,sourceMapBoundaryOnlyNotFullFilesystemConfinement=True,sourceAdmissionClaimed=False,wholeWorkspaceProfileSelected=False,SM4PlaceholderFilled=False,SM11PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False);(B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('Rust library cohort complete',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
