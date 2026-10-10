from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,stat
B=Path(__file__).resolve().parent;m=json.loads((B/'axum-resolved-metadata.json').read_text());r=json.loads((B/'axum-locked-inputs/receipt.json').read_text());lock={(p['name'],p['version']):p for p in r['packages']};rows=[]
for package in m['packages']:
 if package['source'] is None:continue
 assert package['source']=='registry+https://github.com/rust-lang/crates.io-index'
 source=lock[(package['name'],package['version'])];archive=Path(source['archive']);assert hashlib.sha256(archive.read_bytes()).hexdigest()==source['checksum'];root=Path(package['manifest_path']).parent;prefix=package['name']+'-'+package['version'];expected={}
 with tarfile.open(archive,'r:gz') as t:
  for member in t:
   path=PurePosixPath(member.name);assert not path.is_absolute() and path.parts[0]==prefix and all(x not in ('','..','.') for x in path.parts)
   if member.isdir():continue
   assert member.isfile(),('nonregular archive member',member.name)
   relative=PurePosixPath(*path.parts[1:]).as_posix();assert relative not in expected;raw=t.extractfile(member).read();expected[relative]=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 actual={};operational=[]
 for p in root.rglob('*'):
  info=p.lstat()
  if stat.S_ISDIR(info.st_mode):continue
  assert stat.S_ISREG(info.st_mode),('nonregular extraction',str(p));relative=p.relative_to(root).as_posix();raw=p.read_bytes()
  if relative=='.cargo-ok':operational.append(dict(path=relative,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()));continue
  actual[relative]=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 assert actual==expected,('extraction mismatch',prefix,set(expected)-set(actual),set(actual)-set(expected))
 rows.append(dict(packageId=package['id'],name=package['name'],version=package['version'],source=package['source'],archiveChecksum=source['checksum'],root=str(root),regularFiles=[dict(path=k,**actual[k]) for k in sorted(actual)],operationalFiles=operational))
v=dict(standing='UNREVIEWED ACTUAL RESOLVED REGISTRY SOURCE BYTE EQUALITY AGAINST ORIGINAL LOCK CHECKSUM ARCHIVES',registryPackages=len(rows),sourceFiles=sum(len(x['regularFiles']) for x in rows),rows=rows,completePackageArchiveEquality=True,sourceCodeExecuted=False,buildScriptsExecuted=False,proceduralMacrosExecuted=False,sourceAdmission=False,fullSM=False)
(B/'axum-dependency-source-audit.json').write_text(json.dumps(v,indent=2)+'\n');print(v['registryPackages'],'registry packages',v['sourceFiles'],'files all original archive bytes equal')
