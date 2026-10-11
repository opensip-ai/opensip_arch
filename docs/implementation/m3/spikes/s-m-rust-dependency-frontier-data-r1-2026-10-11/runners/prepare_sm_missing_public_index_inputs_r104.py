from pathlib import Path
import os,json,re,hashlib,urllib.request,urllib.error,ssl
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';target=D/'missing-public-index-inputs-r104';assert not target.exists();target.mkdir(mode=0o700)
source=D/'corpus-graph-frontier-input-r104.json';results=json.loads(source.read_bytes());missing={}
for r in results['results']:
 e=(r.get('outcome') or {}).get('error')
 if not e:continue
 m=re.fullmatch(r'no matching package named `([A-Za-z0-9_-]+)` found',e.splitlines()[0]) or re.fullmatch(r'failed to download `([A-Za-z0-9_-]+) v([^`]+)`: attempting to make an HTTP request, but --offline was specified',e.splitlines()[0]) or re.fullmatch(r'failed to select a version for `([A-Za-z0-9_-]+)`[.]?',e.splitlines()[0]);assert m,e
 name=m[1];assert name.isascii() and name==name.lower();missing.setdefault(name,[]).append({'ordinal':r['ordinal'],'id':r['id'],'diagnosticFirstLine':e.splitlines()[0]})
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
# Explicit no proxies, no auth/cookies/client certificate. Only supplied public HTTPS URLs.
client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
records=[]
for name in sorted(missing):
 suffix='1/'+name if len(name)==1 else '2/'+name if len(name)==2 else '3/'+name[0]+'/'+name if len(name)==3 else name[:2]+'/'+name[2:4]+'/'+name
 url='https://index.crates.io/'+suffix;request=urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1','Accept':'application/json'})
 with client.open(request,timeout=30) as response:
  assert response.status==200 and response.geturl()==url;raw=response.read()
 rows=[json.loads(line) for line in raw.splitlines() if line];assert rows
 for row in rows:
  assert row['name']==name and re.fullmatch(r'[0-9a-f]{64}',row['cksum']) and isinstance(row['vers'],str)
 assert len({row['vers'] for row in rows})==len(rows)
 path=target/(name+'.jsonl');path.write_bytes(raw);records.append(dict(name=name,url=url,path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),publishedVersionRecords=len(rows),observedOfflineFailures=missing[name],sourceAuthentication=False,nativeAdmission=False))
 print('Anonymous retained public index',name,len(rows),'version records',len(raw),'bytes',flush=True)
receipt=dict(standing='ACTUAL ANONYMOUS PUBLIC INDEX PREPARATION; NO CARGO INTAKE OR SOURCE ADMISSION',failureSource=dict(path=str(source),bytes=source.stat().st_size,sha256=hashlib.sha256(source.read_bytes()).hexdigest()),inputs=records,publicAcquisitionPerformed=True,requestsAnonymous=True,proxyAuthCookieHandlersAbsent=True,redirectsRefused=True,credentialsRead=False,userCargoHomeRead=False,archivesDownloaded=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Public index input preparation finished; no version winner or native source authority selected',flush=True)
