from pathlib import Path
import json,tomllib,hashlib,os,subprocess,concurrent.futures,urllib.parse,datetime
B=Path(__file__).resolve().parent;N=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');A=B/'axum-locked-inputs';A.mkdir();(A/'archives').mkdir();(A/'index').mkdir();os.setpriority(os.PRIO_PROCESS,0,10)
meta=json.loads((B/'t2-metadata-census.json').read_text());tmp=Path(meta['privateTMPDIR']);lock=tmp/'rs-medium-axum/Cargo.lock';raw=lock.read_bytes();v=tomllib.loads(raw.decode());assert v['version'] in [3,4];packages=[]
for p in v['package']:
 source=p.get('source','')
 if not source:continue
 assert source=='registry+https://github.com/rust-lang/crates.io-index',source
 assert 'checksum' in p and len(p['checksum'])==64 and all(c in '0123456789abcdef' for c in p['checksum'])
 for field in ['name','version']:assert p[field] and '/' not in p[field] and '\\' not in p[field] and p[field] not in ['.','..']
 packages.append(dict(name=p['name'],version=p['version'],source=source,checksum=p['checksum']))
assert len(packages)==234
reused={p.stem:p for p in (N/'registry-archives').glob('*.crate')}
# Prior archive filenames are checksum-based; reuse only by verified bytes.
for p in (N/'registry-archives').iterdir():
 if p.is_file():reused[hashlib.sha256(p.read_bytes()).hexdigest()]=p

def fetch(url,path):
 out=path.with_suffix(path.suffix+'.part');child=subprocess.run(['/usr/bin/curl','--fail','--location','--silent','--show-error','--retry','3','--output',str(out),url],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if child.returncode:raise RuntimeError((url,child.stderr.decode()[:2000]))
 out.rename(path)

def archive(p):
 dest=A/'archives'/(p['checksum']+'.crate');url='https://static.crates.io/crates/'+urllib.parse.quote(p['name'],safe='')+'/'+urllib.parse.quote(p['name']+'-'+p['version'],safe='')+'.crate';reuse=reused.get(p['checksum'])
 if reuse:dest.write_bytes(reuse.read_bytes())
 else:fetch(url,dest)
 raw=dest.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['checksum'],p
 return dict(**p,archive=str(dest),bytes=len(raw),sha256=p['checksum'],url=url,reusedPriorPinnedProducerArchive=bool(reuse))

names=sorted(set(p['name'] for p in packages))
def index(name):
 lower=name.lower();prefix='1' if len(lower)==1 else '2' if len(lower)==2 else '3/'+lower[0] if len(lower)==3 else lower[:2]+'/'+lower[2:4];path=A/'index'/(name+'.jsonl');url='https://index.crates.io/'+prefix+'/'+lower;fetch(url,path);raw=path.read_bytes();lines=[json.loads(x) for x in raw.splitlines() if x];selected=[]
 for p in [p for p in packages if p['name']==name]:
  matches=[x for x in lines if x['name']==name and x['vers']==p['version']];assert len(matches)==1,(name,p['version']);assert matches[0]['cksum']==p['checksum'];selected.append(dict(version=p['version'],checksum=p['checksum']))
 return dict(name=name,path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),url=url,indexRelativePath=prefix+'/'+lower,lockedRowsVerified=selected)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 archives=list(pool.map(archive,packages));print('234 raw locked archives checksum-verified',flush=True);indexes=list(pool.map(index,names));print(len(indexes),'official index files retained and locked version/checksum joins verified',flush=True)
report=dict(standing='PUBLIC ORIGINAL AXUM LOCK-PINNED SOURCE PREPARATION ONLY; NO NATIVE SOURCE ADMISSION OR REPOSITORY EXECUTION',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),originalLock=dict(path=str(lock),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),version=v['version']),packages=archives,indexFiles=indexes,originalPackageTuplesPreserved=True,lockedChecksumsVerified=True,sourceTreesNotYetExtracted=True,generatedLockfile=False,CargoRun=False,repositoryCodeExecuted=False,sourceAdmission=False,fullSM=False)
(A/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('Axum source preparation receipt complete',flush=True)
