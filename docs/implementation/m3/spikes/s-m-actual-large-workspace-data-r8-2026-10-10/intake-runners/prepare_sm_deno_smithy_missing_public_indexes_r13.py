from pathlib import Path
import os,json,re,hashlib
# Index receipt for the Deno root (ordinal 25) and Smithy rust-runtime (ordinal 7) after template r12.
# Reuses the retained, pinned anonymous r11 index files for the 401 remaining lowercase Deno names, and the retained
# mixed-case `Inflector` index from the mixed-case variant inputs. Names are lock-derived (lead decision 2026-10-10).
# Intake of this receipt requires the separately reviewed mixed-case intake variant; the closed intake would refuse it.
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';target=D/'missing-public-index-inputs-deno-smithy-r13';assert not target.exists();target.mkdir(mode=0o700)
def ref(p):raw=Path(p).read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
t=json.loads((D/'other-large-supplemental-registry-template-r12.json').read_bytes());arch={os.path.basename(f['path']) for f in t['files'] if f['path'].startswith('cache/')}
r11=json.loads((D/'missing-public-index-inputs-other-large-r11/receipt.json').read_bytes());by={i['name']:i for i in r11['inputs']}
mixed=json.loads((B/'sm-public-intake-mixed-case-2026-10-11/inputs/index/receipt.json').read_bytes())['inputs'];assert [i['name'] for i in mixed]==['Inflector']
need={}
for receipt,ordinal in [(D/'other-large-workspace-retry-packets-r11.json',25),(D/'smithy-workspace-retry-packets-r10.json',7)]:
 entry=[e for e in json.loads(receipt.read_bytes())['packets'] if e['ordinal']==ordinal][0];packet=json.loads(Path(entry['path']).read_bytes());lock=packet['originalLock'];raw=Path(lock['path']).read_bytes();assert len(raw)==lock['bytes'] and hashlib.sha256(raw).hexdigest()==lock['sha256']
 for b in raw.decode().split('\n[[package]]\n')[1:]:
  f=dict(re.findall(r'^(name|version|source|checksum) = "([^"]*)"$',b,re.M))
  if f.get('source')=='registry+https://github.com/rust-lang/crates.io-index' and f"{f['name']}-{f['version']}.crate" not in arch:need.setdefault(f['name'],[]).append(dict(ordinal=ordinal,lockedVersion=f['version'],lockedChecksum=f.get('checksum')))
inputs=[]
for name in sorted(need):
 base=mixed[0] if name=='Inflector' else by[name];raw=Path(base['path']).read_bytes();assert len(raw)==base['bytes'] and hashlib.sha256(raw).hexdigest()==base['sha256']
 rows=[json.loads(l) for l in raw.splitlines() if l]
 for req in need[name]:
  hit=[r for r in rows if r['vers']==req['lockedVersion']];assert len(hit)==1 and (req['lockedChecksum'] is None or hit[0]['cksum']==req['lockedChecksum'])
 inputs.append(dict({k:base[k] for k in ['name','url','path','bytes','sha256','publishedVersionRecords']},originalLockRequirements=need[name],sourceAuthentication=False,nativeAdmission=False))
receipt=dict(standing='REUSED RETAINED ANONYMOUS PUBLIC INDEX INPUTS FOR DENO ROOT AND SMITHY RUST-RUNTIME; MIXED-CASE INTAKE VARIANT REQUIRED; NO INTAKE OR SOURCE ADMISSION',parentReceipts=[ref(D/'missing-public-index-inputs-other-large-r11/receipt.json'),ref(B/'sm-public-intake-mixed-case-2026-10-11/inputs/index/receipt.json')],registryTemplate=ref(D/'other-large-supplemental-registry-template-r12.json'),inputs=inputs,publishedVersionRecords=sum(i['publishedVersionRecords'] for i in inputs),mixedCaseNames=[i['name'] for i in inputs if i['name']!=i['name'].lower()],lockDerivedNamesLeadDecision=True,publicAcquisitionPerformed=False,archivesDownloaded=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(len(inputs),receipt['publishedVersionRecords'],receipt['mixedCaseNames'])
