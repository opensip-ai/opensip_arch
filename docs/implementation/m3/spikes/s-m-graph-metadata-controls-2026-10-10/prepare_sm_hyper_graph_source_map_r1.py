from pathlib import Path
import os,json,hashlib,stat,struct,tempfile
os.setpriority(os.PRIO_PROCESS,0,10);B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';V=B/'sm-graph-typecheck-2026-10-10';dest=V/'hyper-source-map-preparation-r1.json';assert not dest.exists();receipt=json.loads((D/'corpus-graph-attempts-r31.json').read_bytes());entry=next(x for x in receipt['results'] if x['id']=='rs-medium-hyper');assert entry['outcome']['success'];graph=json.loads(Path(entry['graph']['path']).read_bytes());assert graph['version']==1 and len(graph['units'])==7 and entry['expansionUnavailableUnitIndices']==[];packet=json.loads(Path(entry['packet']['path']).read_bytes());member=Path(packet['memberRoot']);registry=Path(entry['packet']['root'])/'home/registry/src';assert member.is_absolute() and registry.is_absolute();O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');root=Path(tempfile.mkdtemp(prefix='opensip-sm-hyper-graph-map-',dir=O));root.chmod(0o700)
def checked(path,row=None):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read()
  z=os.fstat(fd);assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 finally:os.close(fd)
 if row:assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 return raw
for f in packet['originalFiles']:checked(member/f['path'],f)
rows=[];excluded=[];chunks=[];names=set()
for base,origin in [(member,'exact owned T2 hyper source copy plus separately generated experimental lock'),(registry,'Cargo-expanded experimental registry source, not authenticated native source')]:
 assert base.is_dir() and not base.is_symlink()
 for directory,dirs,files in os.walk(base,followlinks=False):
  for name in list(dirs):
   p=Path(directory)/name
   if p.is_symlink():excluded.append(dict(path=str(p),kind='symlink-directory'));dirs.remove(name)
  for name in sorted(files):
   p=Path(directory)/name;info=p.lstat()
   if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=str(p),kind='nonregular'));continue
   raw=checked(p);assert str(p) not in names;names.add(str(p));namebytes=str(p).encode();chunks.append(struct.pack('>Q',len(namebytes))+namebytes+struct.pack('>Q',len(raw))+raw);rows.append(dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),origin=origin))
for u in graph['units']:assert u['target']['src_path'] in names
encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(chunks);path=root/'source-map.bin';path.write_bytes(encoded);path.chmod(0o400);assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256(encoded).digest()
result=dict(standing='UNREVIEWED PREPARED EXPERIMENTAL HYPER GRAPH SOURCE MAP; NO COMPILER USE',graph=entry['graph'],packet=entry['packet'],originalManifestEntry='rs-medium-hyper',sourceMap=dict(path=str(path),bytes=len(encoded),sha256=hashlib.sha256(encoded).hexdigest()),files=sorted(rows,key=lambda r:r['path']),excluded=excluded,sourceContentBytes=sum(r['bytes'] for r in rows),preparedFiles=len(rows),graphUnits=7,graphRoots=graph['roots'],sourceRoots=[str(member),str(registry)],root=str(root),allGraphSourceRootsPresent=True,originalRegularBytePinsReobserved=True,expandedRegistrySourceAuthentication=False,wholeNativeSourceProfile=False,actualCorpusTypecheck=False,corpusRun=False,nativeAdmission=False,completeStatisticalSet=False,physicalPeakScratchMeasured=False,SMComplete=False);dest.write_text(json.dumps(result,indent=2)+'\n');print({'preparedFiles':len(rows),'sourceContentBytes':result['sourceContentBytes'],'sourceMapBytes':len(encoded),'graphUnits':7,'excludedNonregular':len(excluded),'corpusRun':False})
