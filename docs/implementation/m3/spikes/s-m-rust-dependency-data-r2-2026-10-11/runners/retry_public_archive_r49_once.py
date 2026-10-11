from pathlib import Path
import os,json,hashlib,ssl,urllib.request,urllib.error
os.setpriority(os.PRIO_PROCESS,0,10)
d=Path('/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r49');original=d/'receipt.json';raw=original.read_bytes();r=json.loads(raw);failed=[x for x in r['archives'] if not x['success']];assert len(failed)==1 and failed[0]['httpStatus']==500;old=failed[0];dest=d/'retry-1';assert not dest.exists();dest.mkdir(mode=0o700)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);context.load_verify_locations(cafile='/etc/ssl/cert.pem');client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=context));request=urllib.request.Request(old['url'],headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1'});new={k:v for k,v in old.items() if k not in ['success','errorType','httpStatus']}
try:
 with client.open(request,timeout=30) as response:
  assert response.status==200 and response.geturl()==old['url'];data=response.read()
 digest=hashlib.sha256(data).hexdigest();match=digest==old['expectedSuppliedIndexChecksum'];path=dest/(old['name']+'-'+old['version']+'.crate'+('' if match else '.mismatch-response'));path.write_bytes(data);new.update(success=match,path=str(path),bytes=len(data),sha256=digest,wholeSuppliedChecksumMatch=match)
except Exception as exc:new.update(success=False,errorType=type(exc).__name__,httpStatus=exc.code if isinstance(exc,urllib.error.HTTPError) else None)
(dest/'result.json').write_text(json.dumps(new,indent=2)+'\n');r['archives']=[new if x['name']==old['name'] and x['version']==old['version'] else x for x in r['archives']];r.update(originalFailureReceipt=dict(path=str(original),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),retryResultsRetained=True,successfulWholeChecksumMatches=sum(x['success'] for x in r['archives']),bytes=sum(x.get('bytes',0) for x in r['archives']));(d/'receipt-retry-1.json').write_text(json.dumps(r,indent=2)+'\n');print({'retrySuccess':new['success'],'successfulWholeChecksumMatches':r['successfulWholeChecksumMatches'],'recordsRequested':r['recordsRequested'],'bytes':r['bytes']})
