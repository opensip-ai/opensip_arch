from pathlib import Path
import os,json,hashlib,stat,struct,tempfile,shutil
# Derived from prepare_sm_actual_smithy_http_fuzz_original_source_map_r1.py / the Deno SQLite short-path preparer.
# One map per successful graph in Smithy r11 and original-hierarchy r9 receipts. Every regular member/registry row is kept;
# the closed driver's descriptor (driver.rs sha256 43315ea6...) and row bounds are computed BEFORE writing any map.
# A graph over a bound is recorded unavailable-before-launch; nothing is trimmed and no bound changes.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';V=B/'sm-framed-bin-profile-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');dest=V/'actual-deno-root-smithy-runtime-source-maps-r1.json';assert not dest.exists()
O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');DESCRIPTOR_BOUND=4<<20;ROW_BOUND=100000;CONTENT_BOUND=8<<30
assert hashlib.sha256((B/'sm-framed-analysis-2026-10-10/driver.rs').read_bytes()).hexdigest()=='43315ea6b81bd9b7a41174c1db41d50423b557ab6877be77db724ec96a7b75aa'
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
 return 2+sum(len(json.dumps(dict(bytes=r['bytes'],path=r['path'],sha256=r['sha256']),separators=(',',':'),ensure_ascii=False).encode()) for r in rows)+max(len(rows)-1,0)
receipts=[D/'actual-other-large-workspace-attempts-r13.json',D/'actual-smithy-original-workspace-attempts-r12.json'];results=[];unavailable=[]
for receipt_path in receipts:
 receipt=json.loads(checked(receipt_path))
 for entry in receipt['results']:
  if not entry.get('graph'):continue
  assert entry['outcome']['success'];graph=json.loads(checked(Path(entry['graph']['path']),entry['graph']));packet=json.loads(checked(Path(entry['packet']['path']),entry['packet']));member=Path(packet['memberRoot']);registry=Path(entry['packet']['root'])/'home/registry/src';assert member.is_absolute() and registry.is_absolute()
  for f in packet['originalFiles']:checked(member/f['path'],f)
  rows=[];excluded=[];names=set();chunks=[]
  for base,origin in [(member,'exact owned T2 source copy; original pinned lock retained'),(registry,'Cargo-expanded experimental registry source; not native authenticated source')]:
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
  missing_roots=[u['target']['src_path'] for u in graph['units'] if u['target']['src_path'] not in names]
  descriptor=descriptor_bytes(rows);content=sum(r['bytes'] for r in rows)
  common=dict(id=entry['id'],ordinal=entry['ordinal'],originalRelativeManifest=entry['originalRelativeManifest'],receipt=pin(receipt_path),graph=entry['graph'],packet=entry['packet'],unitCommandData=entry['unitCommandData'],graphUnits=len(graph['units']),graphRoots=graph['roots'],preparedFiles=len(rows),sourceContentBytes=content,preparedDescriptorBytes=descriptor,preparedDescriptorBoundBytes=DESCRIPTOR_BOUND,graphSourceRootsAbsentFromMap=missing_roots,excluded=excluded)
  if descriptor>DESCRIPTOR_BOUND or len(rows)>ROW_BOUND or content>CONTENT_BOUND:
   unavailable.append(dict(common,standing='unavailable-before-launch',reason='closed driver descriptor/row/content bound exceeded; no trimming or bound change'));print(dict(ordinal=entry['ordinal'],unavailable=True,descriptor=descriptor,rows=len(rows)),flush=True);continue
  for f in packet['originalFiles']:checked(member/f['path'],f)
  root=Path(tempfile.mkdtemp(prefix=f'opensip-sm-graph-map-{entry["ordinal"]}-',dir=O));root.chmod(0o700)
  encoded=b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(chunks);path=root/'source-map.bin';path.write_bytes(encoded);path.chmod(0o400)
  checked(Path(entry['unitCommandData']['path']),entry['unitCommandData'])
  results.append(dict(common,sourceMap=pin(path),files=sorted(rows,key=lambda r:r['path']),sourceRoots=[str(member),str(registry)],root=str(root),cwd=packet['project'],descriptorCheckedBeforeLaunch=True,descriptorBoundChanged=False,sourcesTrimmed=False,originalRegularBytePinsReobserved=True,expandedRegistrySourceAuthentication=False,wholeNativeSourceProfile=False,actualCorpusTypecheck=False,nativeAdmission=False,completeStatisticalSet=False,physicalPeakScratchMeasured=False,SMComplete=False))
  print(dict(ordinal=entry['ordinal'],units=len(graph['units']),files=len(rows),mapBytes=len(encoded),descriptor=descriptor,missingRoots=len(missing_roots)),flush=True)
report=dict(standing='ORIGINAL DENO ROOT / SMITHY RUST-RUNTIME GRAPH SOURCE MAPS; DESCRIPTOR CHECKED BEFORE LAUNCH; UNREVIEWED; NO COMPILER USE',dependencyDataReceipts=[pin(r) for r in receipts],results=results,unavailableBeforeLaunch=unavailable,fullCargoProfileEnvironment=False,nativeAdmission=False,SMComplete=False);dest.write_text(json.dumps(report,indent=2)+'\n')
shutil.copyfile(dest,C/'continuation-preserved'/D.name/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name)
