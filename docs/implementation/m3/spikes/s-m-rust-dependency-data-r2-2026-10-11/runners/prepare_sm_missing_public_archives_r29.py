from pathlib import Path
import os,json,hashlib,re,urllib.request,urllib.error,ssl,concurrent.futures
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';indexes=D/'missing-public-index-inputs-r29';receipt=json.loads((indexes/'receipt.json').read_bytes());target=D/'missing-public-archive-inputs-r29';assert not target.exists();target.mkdir(mode=0o700)
ca=Path('/etc/ssl/cert.pem');assert ca.is_file();context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);context.load_verify_locations(cafile=str(ca));assert context.check_hostname and context.verify_mode==ssl.CERT_REQUIRED
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
items=[]
for index in receipt['inputs']:
 raw=Path(index['path']).read_bytes();assert len(raw)==index['bytes'] and hashlib.sha256(raw).hexdigest()==index['sha256']
 for line in raw.splitlines():
  row=json.loads(line);name=row['name'];version=row['vers'];assert name==index['name'] and re.fullmatch(r'[a-z0-9_-]+',name) and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?',version) and re.fullmatch(r'[a-f0-9]{64}',row['cksum']);items.append((index,row))
assert len(items)==sum(i['publishedVersionRecords'] for i in receipt['inputs'])
# All retained version records are inputs; Cargo chooses later. No alias/version winner guessed.
def acquire(item):
 index,row=item;name=row['name'];version=row['vers'];url=f'https://static.crates.io/crates/{name}/{name}-{version}.crate';path=target/(name+'-'+version+'.crate');assert not path.exists()
 client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=context));request=urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1'})
 record=dict(name=name,version=version,url=url,expectedSuppliedIndexChecksum=row['cksum'],indexInput=dict(path=index['path'],bytes=index['bytes'],sha256=index['sha256']),sourceAuthentication=False,nativeAdmission=False)
 try:
  with client.open(request,timeout=30) as response:
   assert response.status==200 and response.geturl()==url;raw=response.read()
  digest=hashlib.sha256(raw).hexdigest();match=digest==row['cksum'];retained=path if match else path.with_name(path.name+'.mismatch-response');retained.write_bytes(raw)
  record.update(success=match,path=str(retained),bytes=len(raw),sha256=digest,wholeSuppliedChecksumMatch=match,registryCacheIntake=False)
 except Exception as exc:record.update(success=False,errorType=type(exc).__name__,httpStatus=exc.code if isinstance(exc,urllib.error.HTTPError) else None,registryCacheIntake=False)
 return record
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
 for r in executor.map(acquire,items):
  results.append(r);print('Anonymous public archive retained',r['name'],r['version'],'checksumMatch',r['success'],flush=True)
  (target/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
output=dict(standing='ACTUAL ANONYMOUS PUBLIC ARCHIVE PREPARATION; SUPPLIED INDEX CONSISTENCY ONLY',indexReceipt=dict(path=str(indexes/'receipt.json'),bytes=(indexes/'receipt.json').stat().st_size,sha256=hashlib.sha256((indexes/'receipt.json').read_bytes()).hexdigest()),tlsCA=dict(path=str(ca),bytes=ca.stat().st_size,sha256=hashlib.sha256(ca.read_bytes()).hexdigest()),archives=results,recordsRequested=len(items),successfulWholeChecksumMatches=sum(r['success'] for r in results),bytes=sum(r.get('bytes',0) for r in results),publicAcquisitionPerformed=True,requestsAnonymous=True,proxyAuthCookieHandlersAbsent=True,redirectsRefused=True,credentialsRead=False,userCargoHomeRead=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(output,indent=2)+'\n');print('Public archive preparation finished',output['successfulWholeChecksumMatches'],'whole supplied checksum matches',output['bytes'],'bytes',flush=True)
