from pathlib import Path
import os,json,re,hashlib,urllib.request,ssl
# Anonymous public inputs for the mixed-case intake variant controls: crates.io `Inflector` (needed by original Deno root and
# Smithy rust-runtime locks). Index URL uses Cargo's lowercased path; archive URLs keep the exact published name.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');R=B/'sm-public-intake-mixed-case-2026-10-11/inputs';assert not R.exists();(R/'index').mkdir(parents=True,mode=0o700);(R/'archives').mkdir(mode=0o700)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
ca=Path('/etc/ssl/cert.pem');context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);context.load_verify_locations(cafile=str(ca))
client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=context))
def get(url):
 with client.open(urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1'}),timeout=30) as r:
  assert r.status==200 and r.geturl()==url;return r.read()
name='Inflector';url='https://index.crates.io/in/fl/inflector';raw=get(url);rows=[json.loads(l) for l in raw.splitlines() if l]
assert rows and all(r['name']==name and re.fullmatch(r'[0-9a-f]{64}',r['cksum']) for r in rows) and len({r['vers'] for r in rows})==len(rows)
ip=R/'index'/(name+'.jsonl');ip.write_bytes(raw)
index_input=dict(name=name,url=url,path=str(ip),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),publishedVersionRecords=len(rows),sourceAuthentication=False,nativeAdmission=False)
index_receipt=R/'index'/'receipt.json';index_receipt.write_text(json.dumps(dict(standing='ACTUAL ANONYMOUS PUBLIC MIXED-CASE INDEX INPUT; NO INTAKE OR SOURCE ADMISSION',inputs=[index_input],publishedVersionRecords=len(rows),requestsAnonymous=True,redirectsRefused=True,credentialsRead=False,sourceAuthentication=False,nativeAdmission=False),indent=2)+'\n')
ref=lambda p:dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
archives=[]
for row in rows:
 v=row['vers'];u=f'https://static.crates.io/crates/{name}/{name}-{v}.crate';body=get(u);d=hashlib.sha256(body).hexdigest();ok=d==row['cksum'];p=R/'archives'/(f'{name}-{v}.crate'+('' if ok else '.mismatch-response'));p.write_bytes(body)
 archives.append(dict(name=name,version=v,url=u,expectedSuppliedIndexChecksum=row['cksum'],indexInput={k:index_input[k] for k in ['path','bytes','sha256']},success=ok,path=str(p),bytes=len(body),sha256=d,wholeSuppliedChecksumMatch=ok,registryCacheIntake=False,sourceAuthentication=False,nativeAdmission=False))
 print(name,v,ok,flush=True)
(R/'archives'/'receipt.json').write_text(json.dumps(dict(standing='ACTUAL ANONYMOUS PUBLIC MIXED-CASE ARCHIVE INPUTS; SUPPLIED INDEX CONSISTENCY ONLY',indexReceipt=ref(index_receipt),tlsCA=ref(ca),archives=archives,recordsRequested=len(rows),successfulWholeChecksumMatches=sum(a['success'] for a in archives),bytes=sum(a['bytes'] for a in archives),requestsAnonymous=True,redirectsRefused=True,credentialsRead=False,registryCacheModified=False,sourceAuthentication=False,nativeAdmission=False),indent=2)+'\n')
print('records',len(rows),'matches',sum(a['success'] for a in archives))
