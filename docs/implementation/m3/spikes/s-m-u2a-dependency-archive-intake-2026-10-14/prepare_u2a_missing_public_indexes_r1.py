from pathlib import Path
import os,json,re,hashlib,urllib.request,ssl
# U-2a (S-M report plan r3, D-2): anonymous public index preparation for the crates.io names that the eight generated Rust
# locks (the medium workloads other than axum; the overlay's two entries) pin but whose archives template r116 lacks.
# Recipe: the accepted prepare_sm_hierarchy_missing_public_indexes_r7.py fetch (anonymous HTTPS, no proxy/auth/cookies,
# redirects refused); names are lock-derived (lead decision 2026-10-10), not diagnostic-derived. No Cargo, no intake.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');W=B/'sm-dependency-source-sets-2026-10-14';target=W/'missing-public-index-inputs-u2a';assert not target.exists();target.mkdir(mode=0o700)
C=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
T=json.loads((B/'sm-experimental-dependency-preparation-2026-10-10/registry-intake-template-r116.json').read_bytes());arch={os.path.basename(f['path']) for f in T['files'] if f['path'].startswith('cache/')}
LOCKS={'poly-medium-napi-rs':C/'poly-medium-napi-rs/Cargo.lock','rs-medium-aws-lambda-rust-runtime':C/'rs-medium-aws-lambda-rust-runtime/Cargo.lock','rs-medium-hyper':C/'rs-medium-hyper/Cargo.lock','rs-medium-serde':C/'rs-medium-serde/Cargo.lock','rs-medium-serde-json':C/'rs-medium-serde-json/Cargo.lock','rs-medium-tokio':C/'rs-medium-tokio/Cargo.lock','mr-rs-medium-serde-json/rs-medium-serde':C/'mr-rs-medium-serde-json/rs-medium-serde/Cargo.lock','mr-rs-medium-serde-json/rs-medium-serde-json':C/'mr-rs-medium-serde-json/rs-medium-serde-json/Cargo.lock'}
need={};locks=[]
for wid,p in LOCKS.items():
 raw=p.read_bytes();locks.append(dict(workload=wid,path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 for b in raw.decode().split('\n[[package]]\n')[1:]:
  f=dict(re.findall(r'^(name|version|source|checksum) = "([^"]*)"$',b,re.M))
  if f.get('source')=='registry+https://github.com/rust-lang/crates.io-index' and f"{f['name']}-{f['version']}.crate" not in arch:need.setdefault(f['name'],[]).append(dict(workload=wid,lockedVersion=f['version'],lockedChecksum=f.get('checksum')))
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
records=[]
for name in sorted(need):
 assert name.isascii() and name==name.lower()
 suffix='1/'+name if len(name)==1 else '2/'+name if len(name)==2 else '3/'+name[0]+'/'+name if len(name)==3 else name[:2]+'/'+name[2:4]+'/'+name
 url='https://index.crates.io/'+suffix;request=urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1','Accept':'application/json'})
 with client.open(request,timeout=30) as response:
  assert response.status==200 and response.geturl()==url;raw=response.read()
 rows=[json.loads(line) for line in raw.splitlines() if line];assert rows
 for row in rows:assert row['name']==name and re.fullmatch(r'[0-9a-f]{64}',row['cksum']) and isinstance(row['vers'],str)
 assert len({row['vers'] for row in rows})==len(rows)
 for n in need[name]:assert any(r['vers']==n['lockedVersion'] and r['cksum']==n['lockedChecksum'] for r in rows),(name,n)
 path=target/(name+'.jsonl');path.write_bytes(raw);records.append(dict(name=name,url=url,path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),publishedVersionRecords=len(rows),lockedBy=need[name],sourceAuthentication=False,nativeAdmission=False))
 print('index',name,len(rows),flush=True)
receipt=dict(standing='ACTUAL ANONYMOUS PUBLIC INDEX PREPARATION (U-2a); LOCK-DERIVED NAMES; NO CARGO INTAKE OR SOURCE ADMISSION',locks=locks,templateR116=dict(path=str(B/'sm-experimental-dependency-preparation-2026-10-10/registry-intake-template-r116.json')),inputs=records,missingLockedArchives=sum(len(v) for v in need.values()),publicAcquisitionPerformed=True,requestsAnonymous=True,proxyAuthCookieHandlersAbsent=True,redirectsRefused=True,credentialsRead=False,userCargoHomeRead=False,archivesDownloaded=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('names',len(records),'missing locked archives',receipt['missingLockedArchives'],'version records',sum(r['publishedVersionRecords'] for r in records))
