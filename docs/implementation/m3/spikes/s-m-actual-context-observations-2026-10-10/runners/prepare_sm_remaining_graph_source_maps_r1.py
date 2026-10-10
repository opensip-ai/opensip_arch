from pathlib import Path
import os,json,hashlib,stat,struct,tempfile
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';V=B/'sm-graph-typecheck-2026-10-10';dest=V/'remaining-graph-source-maps-r1.json';assert not dest.exists()
O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
def checked(path,row=None):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read()
  z=os.fstat(fd);assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 finally:os.close(fd)
 if row:assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 return raw
def pin(p):raw=checked(p);return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
receipt_path=D/'corpus-graph-attempts-r61.json';receipt=json.loads(checked(receipt_path));results=[]
for entry in receipt['results']:
 if not entry.get('graph') or entry['ordinal']==3:continue
 assert entry['outcome']['success'];graph=json.loads(checked(Path(entry['graph']['path']),entry['graph']));packet=json.loads(checked(Path(entry['packet']['path']),entry['packet']));member=Path(packet['memberRoot']);registry=Path(entry['packet']['root'])/'home/registry/src';assert member.is_absolute() and registry.is_absolute()
 for f in packet['originalFiles']:checked(member/f['path'],f)
 root=Path(tempfile.mkdtemp(prefix=f'opensip-sm-graph-map-{entry["ordinal"]}-',dir=O));root.chmod(0o700);rows=[];excluded=[];names=set();chunks=[]
 for base,origin in [(member,'exact owned T2 source copy plus separately generated experimental locks'),(registry,'Cargo-expanded experimental registry source; not native authenticated source')]:
  assert base.is_dir() and not base.is_symlink()
  for directory,dirs,files in os.walk(base,followlinks=False):
   dirs.sort()
   for name in list(dirs):
    p=Path(directory)/name
    if p.is_symlink():excluded.append(dict(path=str(p),kind='symlink-directory'));dirs.remove(name)
   for name in sorted(files):
    p=Path(directory)/name
    if not stat.S_ISREG(p.lstat().st_mode):excluded.append(dict(path=str(p),kind='nonregular'));continue
    raw=checked(p);assert str(p) not in names;names.add(str(p));nb=str(p).encode();chunks.append(struct.pack('>Q',len(nb))+nb+struct.pack('>Q',len(raw))+raw);rows.append(dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),origin=origin))
 assert all(u['target']['src_path'] in names for u in graph['units'])
 for f in packet['originalFiles']:checked(member/f['path'],f)
 encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(chunks);path=root/'source-map.bin';path.write_bytes(encoded);path.chmod(0o400)
 result=dict(id=entry['id'],ordinal=entry['ordinal'],graph=entry['graph'],packet=entry['packet'],sourceMap=pin(path),files=sorted(rows,key=lambda r:r['path']),excluded=excluded,sourceContentBytes=sum(r['bytes'] for r in rows),preparedFiles=len(rows),graphUnits=len(graph['units']),graphRoots=graph['roots'],sourceRoots=[str(member),str(registry)],root=str(root),cwd=packet['project'],allGraphSourceRootsPresent=True,originalRegularBytePinsReobserved=True,expandedRegistrySourceAuthentication=False,wholeNativeSourceProfile=False,actualCorpusTypecheck=False,nativeAdmission=False,completeStatisticalSet=False,physicalPeakScratchMeasured=False,SMComplete=False)
 results.append(result);print(dict(ordinal=entry['ordinal'],graphUnits=len(graph['units']),preparedFiles=len(rows),mapBytes=len(encoded),excluded=len(excluded)),flush=True)
 report=dict(standing='UNREVIEWED ADDITIONAL PREPARED EXPERIMENTAL GRAPH SOURCE MAPS; NO COMPILER USE',dependencyDataReceipt=pin(receipt_path),results=results,fullCargoProfileEnvironment=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n')
assert len(results)==6
