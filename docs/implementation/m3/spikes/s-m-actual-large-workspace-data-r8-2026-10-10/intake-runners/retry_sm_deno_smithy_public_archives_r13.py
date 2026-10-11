from pathlib import Path
import os,json,hashlib,re,urllib.request,urllib.error,ssl
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';initial=D/'missing-public-archive-inputs-deno-smithy-r13/receipt.json';raw=initial.read_bytes();prior=json.loads(raw);out=D/'missing-public-archive-inputs-deno-smithy-r13-retry1';assert not out.exists();out.mkdir(mode=0o700);rows=[];retries=[]
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise RuntimeError('Anonymous public retry refuses redirects')
context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);context.load_verify_locations(cafile='/etc/ssl/cert.pem');client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=context))
for row in prior['archives']:
 if row['success']:rows.append(row);continue
 name=row['name'];version=row['version'];assert re.fullmatch(r'[A-Za-z0-9_-]+',name) and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?',version);url=f'https://static.crates.io/crates/{name}/{name}-{version}.crate';assert row['url']==url
 retry={k:v for k,v in row.items() if k not in ['errorType','httpStatus']};retry['historicalFailure']=row
 try:
  with client.open(urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1'}),timeout=30) as response:
   assert response.status==200 and response.geturl()==url;content=response.read()
  digest=hashlib.sha256(content).hexdigest();success=digest==row['expectedSuppliedIndexChecksum'];p=out/(name+'-'+version+'.crate'+('' if success else '.mismatch-response'));p.write_bytes(content);retry.update(success=success,path=str(p),bytes=len(content),sha256=digest,wholeSuppliedChecksumMatch=success,registryCacheIntake=False)
 except Exception as e:retry.update(success=False,errorType=type(e).__name__,httpStatus=e.code if isinstance(e,urllib.error.HTTPError) else None,registryCacheIntake=False)
 rows.append(retry);retries.append(retry);print(name,version,'freshRetryChecksumMatch',retry['success'],flush=True)
receipt=dict(prior,archives=rows,successfulWholeChecksumMatches=sum(r['success'] for r in rows),bytes=sum(r.get('bytes',0) for r in rows),historicalArchiveReceipt=dict(path=str(initial),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),retryRecords=retries,standing='NEW MERGED INPUT LIST AFTER FRESH ANONYMOUS RETRY; ORIGINAL HTTP FAILURE RECEIPT UNCHANGED')
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Retained initial failures and new retry receipt separately',receipt['successfulWholeChecksumMatches'],'of',receipt['recordsRequested']);assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
