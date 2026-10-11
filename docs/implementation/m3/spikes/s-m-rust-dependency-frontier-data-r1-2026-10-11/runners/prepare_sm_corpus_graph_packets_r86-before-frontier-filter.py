from pathlib import Path
import os,json,tempfile,hashlib,stat
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');destination=D/'corpus-graph-packets-r86.json';assert not destination.exists()
plans=json.loads((D/'corpus-attempt-inputs-r1.json').read_bytes());originals=json.loads((D/'owned-corpus-copies-r1.json').read_bytes());inventory={r['id']:r for r in originals['workloads']};template=json.loads((D/'registry-intake-template-r86.json').read_bytes());source=Path(template['templateRoot']);private=Path(tempfile.mkdtemp(prefix='opensip-sm-corpus-graph-attempts-r86-',dir=O));private.chmod(0o700)
def read_checked(path,row):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
  z=os.fstat(fd);assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 finally:os.close(fd)
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'];return b
packets=[]
for row in plans['plans']:
 root=private/str(row['ordinal']);root.mkdir(mode=0o700);home=root/'home';home.mkdir(mode=0o700)
 for f in template['files']:
  data=read_checked(source/f['path'],f);dest=home/'registry'/f['path'];dest.parent.mkdir(parents=True,exist_ok=True);fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
  with os.fdopen(fd,'wb') as out:out.write(data)
  assert dest.read_bytes()==data
 assert not (home/'registry/src').exists()
 project=Path(row['manifest']['path']).parent;member=Path(row['originalMemberRoot']);original=inventory[row['id']]['files']
 for f in original:read_checked(member/f['path'],f)
 assert len(row['configuration'])<=1
 packet=dict(schemaVersion=1,workload=row['id'],manifestEntryOrdinal=row['ordinal'],observationRoot=str(root),project=str(project),memberRoot=str(member),originalFiles=original,configuration=row['configuration'][0] if row['configuration'] else None,overlayLinks=row['overlayLinks'],preserveOriginalLock=row['originalLock'] is not None,originalLock=row['originalLock'],registryTemplateMetadata=dict(path=str(D/'registry-intake-template-r86.json'),bytes=(D/'registry-intake-template-r86.json').stat().st_size,sha256=hashlib.sha256((D/'registry-intake-template-r86.json').read_bytes()).hexdigest()),registryFiles=template['files'],originalConfigurationPolicy='Only absence or exact observed NAPI runners accepted by cohort helper',sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
 path=root/'packet.json';path.write_text(json.dumps(packet,indent=2)+'\n');packets.append(dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),id=row['id'],ordinal=row['ordinal'],root=str(root)))
receipt=dict(standing='UNREVIEWED PREPARED ROUND 86 ATTEMPT PACKETS USING ACCEPTED PARAMETERIZED ENTRY AND SEPARATELY PINNED VALIDATED INPUTS',privateTMPDIR=str(private),mode='0700',packets=packets,originalManifestEntries=9,requiredWorkloads=8,privateRegistryCopies=9,physicalRegistryCopyBytes=9*template['bytes'],expandedSourceCopied=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
destination.write_text(json.dumps(receipt,indent=2)+'\n');print({'packets':len(packets),'registryCopies':9,'physicalRegistryCopyBytes':receipt['physicalRegistryCopyBytes'],'expandedSourceCopied':False,'corpusResolutionRun':False})
