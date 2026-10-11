from pathlib import Path
import os,json,hashlib,stat,struct,tempfile,shutil
# Derived from prepare_sm_actual_deno_sqlite_original_source_map_r1.py for the shorter private layout.
# Every original regular source row and every expanded registry row is retained; no source is trimmed.
# The closed driver's prepared descriptor (driver.rs sha256 43315ea6...) is precomputed and checked against its
# unchanged 4 MiB bound and 100000-row bound BEFORE the map is written or any compiler child can launch.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';V=B/'sm-framed-bin-profile-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');dest=V/'actual-deno-sqlite-short-paths-source-map-r1.json';assert not dest.exists()
O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');DESCRIPTOR_BOUND=4<<20;ROW_BOUND=100000
driver_source=B/'sm-framed-analysis-2026-10-10/driver.rs';assert hashlib.sha256(driver_source.read_bytes()).hexdigest()=='43315ea6b81bd9b7a41174c1db41d50423b557ab6877be77db724ec96a7b75aa'
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
def descriptor_bytes(rows):
 # Mirrors driver.rs: serde_json Map (sorted keys bytes/path/sha256), compact, comma-joined, plus two brackets.
 return 2+sum(len(json.dumps(dict(bytes=r['bytes'],path=r['path'],sha256=r['sha256']),separators=(',',':'),ensure_ascii=False).encode()) for r in rows)+max(len(rows)-1,0)
receipt_path=D/'actual-deno-sqlite-short-paths-collector-r1.json';receipt=json.loads(checked(receipt_path));results=[]
long_map=json.loads(checked(V/'actual-deno-sqlite-original-source-map-r1.json'))['results'][0];assert descriptor_bytes(long_map['files'])==4292558
for entry in receipt['results']:
 assert entry['outcome']['success'] and entry['graph'];graph=json.loads(checked(Path(entry['graph']['path']),entry['graph']));packet=json.loads(checked(Path(entry['packet']['path']),entry['packet']));member=Path(packet['memberRoot']);registry=Path(entry['packet']['root'])/'home/registry/src';assert member.is_absolute() and registry.is_absolute()
 for f in packet['originalFiles']:checked(member/f['path'],f)
 rows=[];excluded=[];names=set();chunks=[]
 for base,origin in [(member,'exact owned T2 source copy in shorter private layout; original pinned lock retained'),(registry,'Cargo-expanded experimental registry source; not native authenticated source')]:
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
 # Every long-layout row is present under the short layout with identical bytes; nothing trimmed.
 old_member,old_registry=long_map['sourceRoots'];translated=set()
 for r in long_map['files']:
  p=r['path'];n=str(member)+p[len(old_member):] if p.startswith(old_member+'/') else str(registry)+p[len(old_registry):]
  translated.add((n,r['bytes'],r['sha256']))
 assert translated=={(r['path'],r['bytes'],r['sha256']) for r in rows} and len(rows)==len(long_map['files'])
 descriptor=descriptor_bytes(rows);assert len(rows)<=ROW_BOUND and descriptor<=DESCRIPTOR_BOUND,('descriptor exceeds unchanged closed bound; do not launch',descriptor)
 for f in packet['originalFiles']:checked(member/f['path'],f)
 root=Path(tempfile.mkdtemp(prefix='opensip-dsm-',dir=O));root.chmod(0o700)
 encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(chunks);path=root/'source-map.bin';path.write_bytes(encoded);path.chmod(0o400)
 checked(Path(entry['unitCommandData']['path']),entry['unitCommandData'])
 result=dict(id=entry['id'],ordinal=entry['ordinal'],graph=entry['graph'],packet=entry['packet'],unitCommandData=entry['unitCommandData'],sourceMap=pin(path),files=sorted(rows,key=lambda r:r['path']),excluded=excluded,sourceContentBytes=sum(r['bytes'] for r in rows),preparedFiles=len(rows),graphUnits=len(graph['units']),graphRoots=graph['roots'],sourceRoots=[str(member),str(registry)],root=str(root),cwd=packet['project'],preparedDescriptorBytes=descriptor,preparedDescriptorBoundBytes=DESCRIPTOR_BOUND,previousLongLayoutDescriptorBytes=4292558,descriptorCheckedBeforeLaunch=True,descriptorBoundChanged=False,everyLongLayoutRowRetained=True,sourcesTrimmed=False,allGraphSourceRootsPresent=True,originalRegularBytePinsReobserved=True,expandedRegistrySourceAuthentication=False,wholeNativeSourceProfile=False,canonicalNativeSnapshotDescriptorMeasured=False,actualCorpusTypecheck=False,nativeAdmission=False,completeStatisticalSet=False,physicalPeakScratchMeasured=False,SMComplete=False)
 results.append(result);print(dict(ordinal=entry['ordinal'],graphUnits=len(graph['units']),preparedFiles=len(rows),mapBytes=len(encoded),descriptorBytes=descriptor,excluded=len(excluded)),flush=True)
assert len(results)==1 and results[0]['ordinal']==27
report=dict(standing='SHORTER-LAYOUT ORIGINAL DENO SQLITE WORKSPACE REGULAR SOURCE MAP; DESCRIPTOR CHECKED BEFORE LAUNCH; UNREVIEWED; NO COMPILER USE',dependencyDataReceipt=pin(receipt_path),results=results,fullCargoProfileEnvironment=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n')
shutil.copyfile(dest,C/'continuation-preserved'/D.name/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name)
