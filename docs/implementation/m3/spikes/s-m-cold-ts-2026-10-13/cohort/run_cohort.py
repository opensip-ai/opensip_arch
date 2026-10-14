from pathlib import Path
import os,sys,json,time,hashlib,subprocess,tempfile,stat,statistics,datetime,re,shutil
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';NODE=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node');TS=C/'sm-tools-2026-10-09/typescript/package/lib/typescript.js';sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
from store import verify
import sys as _s;_s.path.insert(0,str(Path(__file__).resolve().parent.parent));import cold_reset as _cr
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=m['counts']['tsjs']['medium']['devIds'];assert len(ids)==6 and all(not entries[i]['heldOut']for i in ids);closure=json.loads((P/'tools/contracts/generator-closure.json').read_text());raw=NODE.read_bytes();assert len(raw)==closure['toolchain']['node']['bytes']and hashlib.sha256(raw).hexdigest()==closure['toolchain']['node']['sha256'];assert hashlib.sha256(TS.read_bytes()).hexdigest()=='569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39'
DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned measurement lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']];T=Path(tempfile.mkdtemp(prefix='opensip-sm-ts-cohort-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T));env.pop('NODE_OPTIONS',None);env.pop('NODE_PATH',None);results=[];libraries=[]
 for p in sorted(TS.parent.iterdir()):
  if p.name.endswith('.d.ts')and p.is_file()and not p.is_symlink():raw=p.read_bytes();libraries.append(dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 for id_ in ids:
  entry=entries[id_];root=C/'t2-corpus-c8cc48e1/store'/entry['treeDigest']['value'];verified=verify(root,entry);sealed=T/id_;sealed.mkdir(mode=0o700);rows=[];excluded=[]
  for directory,dirs,files in os.walk(root,followlinks=False):
   for name in list(dirs):
    p=Path(directory)/name
    if p.is_symlink():excluded.append(dict(path=str(p.relative_to(root)),kind='symlink-directory'));dirs.remove(name)
   for name in files:
    p=Path(directory)/name;info=p.lstat();rel=str(p.relative_to(root))
    if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);dest=sealed/str(len(rows));h=hashlib.sha256();count=0
    with os.fdopen(fd,'rb')as f,dest.open('xb')as out:
     before=os.fstat(f.fileno());assert(info.st_dev,info.st_ino)==(before.st_dev,before.st_ino)
     while part:=f.read(1048576):h.update(part);out.write(part);count+=len(part)
     after=os.fstat(f.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)and count==info.st_size
    dest.chmod(0o400);rows.append(dict(path=rel,bytes=count,sha256=h.hexdigest(),sealed=str(dest)))
  rows.sort(key=lambda r:r['path'].encode());configs=[r['path']for r in rows if re.fullmatch(r'tsconfig(?:\..*)?\.json',Path(r['path']).name)];configInput=dict(id=id_,virtualRoot=str(root),files=rows,libraries=libraries,configurations=configs);inp=sealed/'input.json';inp.write_text(json.dumps(configInput,indent=2)+'\n');(B/'evidence'/f'{id_}-input-inventory.json').write_text(json.dumps(dict(id=id_,virtualRoot=str(root),files=[{k:r[k]for k in ['path','bytes','sha256']}for r in rows],libraries=libraries,configurations=configs,nonregularExcluded=excluded),indent=2)+'\n');samples=[];stable=None
  for n in range(10):
   _cr.reset(env,T)
   out=B/'evidence'/f'{id_}-{n}.stdout.json';err=B/'evidence'/f'{id_}-{n}.stderr';start=time.monotonic_ns()
   with out.open('wb')as o,err.open('wb')as e:
    child=subprocess.Popen(['/usr/bin/nice','-n','10',str(NODE),'--no-addons',str(B/'cohort.cjs'),str(TS),str(inp)],cwd=T,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   end=time.monotonic_ns();assert child.returncode==0,(id_,err.read_text());observed=json.loads(out.read_text());shape=[{k:v for k,v in c.items()if k not in ['calls','elapsedNanos','maxPublicCompilerCall']}for c in observed['configurations']]
   if stable is None:stable=shape
   else:assert shape==stable,(id_,n,'configured semantic drift')
   rss=int(usage.ru_maxrss);assert 0<=rss<2**64;samples.append(dict(ordinal=n,warmup=n<3,wholeProcessNanos=end-start,rssNative=rss,rssUnit='bytes',rssBytes=rss,exitCode=0,stdout=str(out),stderr=str(err)));print(id_,n,'configs',len(configs),'whole ns',end-start,flush=True)
  values=[q['wholeProcessNanos']for q in samples if not q['warmup']];results.append(dict(id=id_,heldOut=False,treeDigest=entry['treeDigest']['value'],commit=entry['commit'],treeVerified=verified,regularRows=len(rows),nonregularExcluded=excluded,configurationCount=len(configs),configuredShape=stable,runs=samples,medianWholeProcessNanos=statistics.median(values),maxWholeProcessNanos=max(values)));shutil.rmtree(sealed);(B/'progress.json').write_text(json.dumps(dict(standing='UNREVIEWED PRELIMINARY PARTIAL CONFIGURATION COHORT',workloads=results),indent=2)+'\n')
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY SEALED CONFIGURATION COHORT; NOT FULL WORKSPACE OR SM2/SM8',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),platformVersion=subprocess.check_output(['/usr/bin/sw_vers']).decode(),workloads=results,TMPDIR=str(T),TMPDIRMode='0700',ownedLane=str(LOCK),laneHeldForEntireSet=True,nice=10,nodeVersion='24.16.0',typescriptVersion='6.0.3',dependencyTreePinned=False,nonregularSnapshotPolicySelected=False,wholeWorkspaceProfileSelected=False,fullWorkspaceSemanticsClaimed=False,SM2PlaceholderFilled=False,SM8PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False,repositoryCodeExecuted=False,heldOutSourceInspected=False)
 (B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('configuration cohort complete',flush=True)
 _cr.write(B)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
