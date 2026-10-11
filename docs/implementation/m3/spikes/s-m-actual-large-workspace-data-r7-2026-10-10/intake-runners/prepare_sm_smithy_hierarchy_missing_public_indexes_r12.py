from pathlib import Path
import os,json,re,hashlib,urllib.request,urllib.error,ssl,concurrent.futures
# Derived from prepare_sm_other_large_missing_public_indexes_r11.py for the Smithy r10 and original-hierarchy r8 failures.
# Lead decision 2026-10-10 (Claude): Cargo reports one missing name per offline attempt, so the remaining names are
# derived up front from the ORIGINAL pinned Cargo.lock of each failing r11 entry (crates.io packages whose exact locked
# archive is absent from template r10), together with the observed r11 diagnostics. Every published version of each
# name is still retained as input (the closed intake requires the whole version set); no version winner is guessed.
# Mixed-case names cannot pass the closed intake's lowercase name rule and are recorded unavailable, not renamed.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';target=D/'missing-public-index-inputs-smithy-hierarchy-r12';assert not target.exists();target.mkdir(mode=0o700)
sources=[D/'actual-smithy-original-workspace-attempts-r10.json',D/'actual-original-hierarchy-workspace-attempts-r8.json'];results=dict(results=[r for s in sources for r in json.loads(s.read_bytes())['results']]);missing={};nonDependencyUnavailable=[];closedIntakeNameShapeUnavailable=[]
template_path=D/'other-large-supplemental-registry-template-r11.json';template=json.loads(template_path.read_bytes());present={os.path.basename(f['path']) for f in template['files'] if f['path'].startswith('cache/')}
packets=dict(packets=[r['packet'] for r in results['results']])
def pinned(path,row):
 raw=Path(path).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
for r in results['results']:
 e=(r.get('outcome') or {}).get('error')
 if not e:continue
 if e.startswith('no matching package named `') and '\nlocation searched: crates.io index\n' not in e:nonDependencyUnavailable.append(dict(ordinal=r['ordinal'],id=r['id'],diagnosticFirstLine=e.splitlines()[0],reason='Local source package mismatch; not a crates.io missing dependency'));continue
 m=re.fullmatch(r'no matching package named `([A-Za-z0-9_-]+)` found',e.splitlines()[0]) or re.fullmatch(r'failed to download `([A-Za-z0-9_-]+) v([^`]+)`: attempting to make an HTTP request, but --offline was specified',e.splitlines()[0]) or re.fullmatch(r'failed to select a version for `([A-Za-z0-9_-]+)`[.]?',e.splitlines()[0])
 if not m:nonDependencyUnavailable.append(dict(ordinal=r['ordinal'],id=r['id'],diagnosticFirstLine=e.splitlines()[0]));continue
 name=m[1];assert name.isascii() and name==name.lower();missing.setdefault(name,dict(observedOfflineFailures=[],originalLockRequirements=[]))['observedOfflineFailures'].append({'ordinal':r['ordinal'],'id':r['id'],'diagnosticFirstLine':e.splitlines()[0]})
lockSources=[]
for entry in packets['packets']:
 packet=json.loads(pinned(entry['path'],entry));lock=packet['originalLock'];assert lock and packet['preserveOriginalLock']
 raw=pinned(lock['path'],lock).decode();lockSources.append(dict(ordinal=entry['ordinal'],id=entry['id'],originalLock=lock))
 blocks=raw.split('\n[[package]]\n')[1:]
 for block in blocks:
  fields=dict(re.findall(r'^(name|version|source|checksum) = "([^"]*)"$',block,re.M))
  if fields.get('source')!='registry+https://github.com/rust-lang/crates.io-index':continue
  name,version=fields['name'],fields['version']
  if f'{name}-{version}.crate' in present:continue
  requirement=dict(ordinal=entry['ordinal'],id=entry['id'],lockedVersion=version,lockedChecksum=fields.get('checksum'))
  if name!=name.lower():closedIntakeNameShapeUnavailable.append(dict(name=name,reason='Closed accepted intake admits lowercase index names only; not renamed or bypassed',**requirement));continue
  missing.setdefault(name,dict(observedOfflineFailures=[],originalLockRequirements=[]))['originalLockRequirements'].append(requirement)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):raise RuntimeError('Anonymous public preparation refuses redirects')
# Explicit no proxies, no auth/cookies/client certificate. Only supplied public HTTPS URLs.
def fetch(name):
 client=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
 suffix='1/'+name if len(name)==1 else '2/'+name if len(name)==2 else '3/'+name[0]+'/'+name if len(name)==3 else name[:2]+'/'+name[2:4]+'/'+name
 url='https://index.crates.io/'+suffix;request=urllib.request.Request(url,headers={'User-Agent':'OpenSIP-anonymous-experiment-preparation/1','Accept':'application/json'})
 with client.open(request,timeout=30) as response:
  assert response.status==200 and response.geturl()==url;raw=response.read()
 rows=[json.loads(line) for line in raw.splitlines() if line];assert rows
 for row in rows:
  assert row['name']==name and re.fullmatch(r'[0-9a-f]{64}',row['cksum']) and isinstance(row['vers'],str)
 assert len({row['vers'] for row in rows})==len(rows)
 for req in missing[name]['originalLockRequirements']:
  hit=[row for row in rows if row['vers']==req['lockedVersion']];assert len(hit)==1 and (req['lockedChecksum'] is None or hit[0]['cksum']==req['lockedChecksum']),('locked version/checksum absent from public index',name,req)
 path=target/(name+'.jsonl');path.write_bytes(raw)
 return dict(name=name,url=url,path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),publishedVersionRecords=len(rows),observedOfflineFailures=missing[name]['observedOfflineFailures'],originalLockRequirements=missing[name]['originalLockRequirements'],sourceAuthentication=False,nativeAdmission=False)
records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
 for record in executor.map(fetch,sorted(missing)):
  records.append(record);print('Anonymous retained public index',record['name'],record['publishedVersionRecords'],'version records',flush=True)
def ref(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
receipt=dict(standing='ACTUAL ANONYMOUS PUBLIC INDEX PREPARATION FROM OBSERVED SMITHY/HIERARCHY DIAGNOSTICS AND ORIGINAL PINNED LOCK REQUIREMENTS; NO CARGO INTAKE OR SOURCE ADMISSION',failureSources=[ref(s) for s in sources],retryPackets=packets['packets'],registryTemplate=ref(template_path),originalLockSources=lockSources,inputs=records,publishedVersionRecords=sum(r['publishedVersionRecords'] for r in records),nonDependencyUnavailable=nonDependencyUnavailable,closedIntakeNameShapeUnavailable=closedIntakeNameShapeUnavailable,lockDerivedNamesLeadDecision=True,publicAcquisitionPerformed=True,requestsAnonymous=True,proxyAuthCookieHandlersAbsent=True,redirectsRefused=True,credentialsRead=False,userCargoHomeRead=False,archivesDownloaded=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Public index input preparation finished',len(records),'names',receipt['publishedVersionRecords'],'version records; unavailable name shapes',len(closedIntakeNameShapeUnavailable),flush=True)
