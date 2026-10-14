# U-2b entry 8: derived from the U-2b script of the same name (only input/output names changed).
from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,stat
# U-2b step 4: the accepted check_axum_dependency_sources.py audit (s-m-axum-metadata-2026-10-09) looped over every
# resolved U-2b entry: each registry package's Cargo-extracted tree must equal its lock-checksummed archive byte for
# byte (.cargo-ok recorded as operational). Writes u2b-source-audits/<slug>.json.
W=Path(__file__).resolve().parent;att=json.loads((W/'u2b-metadata-attempts-entry8.json').read_text());O=W/'u2b-source-audits';assert not O.exists();O.mkdir();summary=[]
for a in att['attempts']:
 if a['exitCode']!=0:summary.append(dict(entry=a['entry'],slug=a['slug'],audited=False,reason='metadata resolution incomplete (attempt retained)'));continue
 m=json.loads(Path(a['metadata']['path']).read_text());r=json.loads(Path(a['receipt']['path']).read_text());lock={(p['name'],p['version']):p for p in r['packages']};rows=[]
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
 v=dict(standing='UNREVIEWED ACTUAL RESOLVED REGISTRY SOURCE BYTE EQUALITY AGAINST ORIGINAL LOCK CHECKSUM ARCHIVES (U-2b)',entry=a['entry'],registryPackages=len(rows),sourceFiles=sum(len(x['regularFiles']) for x in rows),rows=rows,completePackageArchiveEquality=True,sourceCodeExecuted=False,buildScriptsExecuted=False,proceduralMacrosExecuted=False,sourceAdmission=False,fullSM=False)
 (O/f"{a['slug']}.json").write_text(json.dumps(v,indent=2)+'\n');summary.append(dict(entry=a['entry'],slug=a['slug'],audited=True,registryPackages=len(rows),sourceFiles=v['sourceFiles']));print(a['entry'],len(rows),v['sourceFiles'],flush=True)
(W/'u2b-source-audits-entry8.json').write_text(json.dumps(dict(entries=summary),indent=1)+'\n')
