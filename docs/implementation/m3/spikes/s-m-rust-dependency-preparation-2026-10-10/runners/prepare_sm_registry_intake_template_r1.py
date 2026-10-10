from pathlib import Path
import os,json,hashlib,stat
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';m=json.loads((D/'public-registry-cache-copy-r1.json').read_bytes());source=Path(m['ownedCache']);target=source.parent/'registry-intake-template-r1';assert not target.exists();target.mkdir(mode=0o700)
control=B/'sm-offline-registry-controls-r1-stage/actual-control-roots/2/control.json';c=json.loads(control.read_bytes());assert c['sourceAuthentication'] is False and c['indexRecords']==11110
archives={x['path']:x for x in c['archiveRows']};assert len(archives)==234
rows=[]
for r in m['files']:
 rel=Path(r['path'])
 if rel.parts[0] not in ['index','cache']:continue
 assert all(x not in ['.','..'] for x in rel.parts)
 fd=os.open(source/rel,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read()
  after=os.fstat(fd);assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
 finally:os.close(fd)
 assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
 if rel.parts[0]=='cache':
  a=archives[r['path']];assert a['bytes']==len(raw) and a['sha256']==r['sha256'] and a['expectedChecksums']==[r['sha256']]
 dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True);fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,'wb') as f:f.write(raw)
 copied=dest.read_bytes();assert copied==raw;rows.append(r)
assert not (target/'src').exists();result=dict(standing='UNREVIEWED VERIFIED INPUT COPY; NO RESOLVER OR NATIVE SOURCE AUTHENTICATION',sourceMetadata=dict(path=str(D/'public-registry-cache-copy-r1.json'),bytes=(D/'public-registry-cache-copy-r1.json').stat().st_size,sha256=hashlib.sha256((D/'public-registry-cache-copy-r1.json').read_bytes()).hexdigest()),exactCargoParserControl=dict(path=str(control),bytes=control.stat().st_size,sha256=hashlib.sha256(control.read_bytes()).hexdigest()),sourceRoot=str(source),templateRoot=str(target),files=rows,bytes=sum(r['bytes'] for r in rows),archives=234,expandedSourcesCopied=False,sourceAuthentication=False,corpusResolutionRun=False,publicAcquisitionPerformed=False,nativeAdmission=False,SMComplete=False)
(D/'registry-intake-template-r1.json').write_text(json.dumps(result,indent=2)+'\n');print({'copiedFiles':len(rows),'bytes':result['bytes'],'archives':234,'expandedSourcesCopied':False,'corpusResolutionRun':False})
