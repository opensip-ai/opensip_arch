from pathlib import Path
import os,json,stat,hashlib,tempfile,subprocess,shutil
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-large-original-context-census-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'deno-sqlite-short-paths-packet-r1.json';assert not dest.exists()
def checked(p,r):
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 with os.fdopen(fd,'rb') as f:
  a=os.fstat(f.fileno());assert stat.S_ISREG(a.st_mode);raw=f.read();z=os.fstat(f.fileno());assert(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'];return raw
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
prior_path=V/'actual-other-large-workspace-attempts-r10.json';prior=json.loads(prior_path.read_bytes());before=next(r for r in prior['results']if r['ordinal']==27);assert before['outcome']['success'];old=json.loads(checked(Path(before['packet']['path']),before['packet']));root=Path(tempfile.mkdtemp(prefix='opensip-ds-',dir=O));root.chmod(0o700);member=root/'p';member.mkdir(mode=0o700)
for row in old['originalFiles']:
 raw=checked(Path(old['memberRoot'])/row['path'],row);p=member/row['path'];p.parent.mkdir(parents=True,exist_ok=True);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,'wb')as f:f.write(raw)
 checked(p,row)
observation=root/'o';observation.mkdir(mode=0o700);home=observation/'home';home.mkdir(mode=0o700);template_ref=old['registryTemplateMetadata'];template=json.loads(checked(Path(template_ref['path']),template_ref));registry=Path(template['templateRoot']);subprocess.run(['/bin/cp','-cR',str(registry),str(home/'registry')],check=True)
for row in old['registryFiles']:checked(home/'registry'/row['path'],row)
assert not(home/'registry/src').exists();relproject=Path(old['project']).relative_to(Path(old['memberRoot']));config=old['configuration'];relconfig=Path(config['path']).relative_to(Path(old['memberRoot']));newconfig=dict(config,path=str(member/relconfig));checked(Path(newconfig['path']),newconfig)
packet=dict(old,observationRoot=str(observation),project=str(member/relproject),memberRoot=str(member),configuration=newconfig)
if packet['originalLock']:
 r=packet['originalLock'];rel=Path(r['path']).relative_to(Path(old['memberRoot']));packet['originalLock']=dict(r,path=str(member/rel));checked(Path(packet['originalLock']['path']),packet['originalLock'])
assert packet['originalFiles']==old['originalFiles'] and packet['preserveOriginalLock']==old['preserveOriginalLock'];p=observation/'packet.json';p.write_text(json.dumps(packet,indent=2)+'\n');entry=dict(**pin(p),id='poly-very-large-deno',ordinal=27,root=str(observation),originalRelativeManifest='tests/sqlite_extension/Cargo.toml');receipt=dict(standing='NEW SHORTER PRIVATE DENO SQLITE SOURCE/CACHE LAYOUT WITH ALL ORIGINAL FILE PINS RETAINED; NO COLLECTOR/COMPILER RUN',privateTMPDIR=str(root),packets=[entry],unavailableBeforeCollector=[],previousAttempts=pin(prior_path),originalFilePinsRetained=True,originalFiles=len(old['originalFiles']),originalRegularSourceCopy=str(member),onlyPrivateAbsoluteLayoutChanged=True,registryTemplateMetadata=template_ref,generatedPreviousExperimentalLockCopied=False,originalByteContentChanged=False,descriptorBoundChanged=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(receipt,indent=2)+'\n');shutil.copyfile(dest,C/'continuation-preserved'/V.name/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name);print('Prepared all',len(old['originalFiles']),'original Deno files in shorter private layout')
