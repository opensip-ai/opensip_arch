from pathlib import Path,PurePosixPath
import os,subprocess,tarfile,tomllib,hashlib,json,concurrent.futures,posixpath,time
B=Path(__file__).resolve().parent;os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10
s=json.loads((B/'source-receipt.json').read_text());root=Path(s['originalRoot']);lock=tomllib.loads((root/'Cargo.lock').read_text());packages=[p for p in lock['package']if p.get('source','').startswith('registry+')];assert len(packages)==507;assert not[p for p in lock['package']if p.get('source','').startswith('git+')]
archives=B/'registry-archives';archives.mkdir(exist_ok=True);vendor=B/'vendor';vendor.mkdir(exist_ok=True)
def one(p):
 name=p['name']+'-'+p['version'];archive=archives/(name+'.crate');dst=vendor/name;url='https://static.crates.io/crates/'+p['name']+'/'+name+'.crate'
 if not archive.exists():
  temp=archives/(name+'.part');r=subprocess.run(['/usr/bin/curl','--silent','--show-error','--fail','--location','--proto','=https','--tlsv1.2','--retry','3','--connect-timeout','20','--max-time','180','--output',str(temp),url],stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert r.returncode==0,(name,r.stderr.decode());temp.rename(archive)
 raw=archive.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['checksum'],name
 checksum=dst/'.cargo-checksum.json'
 if not checksum.exists():
  assert not dst.exists(),name
  with tarfile.open(archive,'r:gz')as t:
   members=t.getmembers()
   for m in members:
    path=PurePosixPath(m.name);assert path.parts[0]==name and not path.is_absolute()and '..'not in path.parts;assert m.isfile()or m.isdir(),(name,m.name,m.type)
   t.extractall(vendor,members=members,filter='data')
  files={}
  for f in sorted(dst.rglob('*')):
   assert not f.is_symlink()
   if f.is_file()and f.name!='.cargo-checksum.json':files[f.relative_to(dst).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
  checksum.write_text(json.dumps(dict(files=files,package=p['checksum']),sort_keys=True)+'\n')
 document=json.loads(checksum.read_text());assert document['package']==p['checksum'];assert all(hashlib.sha256((dst/f).read_bytes()).hexdigest()==h for f,h in document['files'].items());return dict(name=p['name'],version=p['version'],source=p['source'],url=url,archiveBytes=len(raw),archiveSha256=p['checksum'],vendorPath=str(dst),regularFiles=len(document['files']),checksumManifestSha256=hashlib.sha256(checksum.read_bytes()).hexdigest())
rows=[];start=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
 futures=[pool.submit(one,p)for p in packages]
 for future in concurrent.futures.as_completed(futures):
  rows.append(future.result())
  if len(rows)%25==0:print('Verified locked registry sources',len(rows),'of',len(packages),flush=True)
rows.sort(key=lambda r:(r['name'],r['version']));report=dict(standing='UNREVIEWED LOCK-CHECKSUM VERIFIED REGISTRY SOURCE PREPARATION; NO BUILD/EXECUTION/PROFILE ADMISSION',upstreamCommit=s['upstreamCommit'],lockSha256=hashlib.sha256((root/'Cargo.lock').read_bytes()).hexdigest(),packages=rows,elapsedSeconds=time.monotonic()-start,observedParentNiceness=10,cargoInvoked=False,dependencyCodeExecuted=False,compatibleProducerImplemented=False,sourceProfilePublished=False,productQualification=False);(B/'locked-vendor-receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('All507 exactlocked sources verified and prepared for offline producer build; no Cargo invoked.',flush=True)
