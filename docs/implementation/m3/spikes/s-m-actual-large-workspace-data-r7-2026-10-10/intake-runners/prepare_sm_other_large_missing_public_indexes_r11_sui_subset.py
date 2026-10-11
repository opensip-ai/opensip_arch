from pathlib import Path
import json,hashlib
# Subset receipt over the unchanged r11 public index files: names required by Sui Move (ordinal 32) only.
# Index bytes are not copied or edited; each input row is the r11 row verbatim (path/bytes/sha256 rechecked).
B=Path('/tmp/opensip-implementation');D=B/'sm-large-original-context-census-2026-10-10';source=D/'missing-public-index-inputs-other-large-r11/receipt.json';target=D/'missing-public-index-inputs-other-large-r11-sui';assert not target.exists();target.mkdir(mode=0o700)
def ref(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
full=json.loads(source.read_bytes());inputs=[]
for i in full['inputs']:
 if not any(x['ordinal']==32 for x in i['originalLockRequirements']+i['observedOfflineFailures']):continue
 raw=Path(i['path']).read_bytes();assert len(raw)==i['bytes'] and hashlib.sha256(raw).hexdigest()==i['sha256'];inputs.append(i)
receipt=dict(standing='SUBSET OF ACTUAL ANONYMOUS PUBLIC INDEX PREPARATION FOR SUI MOVE ORDINAL 32; UNCHANGED INDEX BYTES; NO CARGO INTAKE OR SOURCE ADMISSION',parentReceipt=ref(source),subsetOrdinal=32,inputs=inputs,publishedVersionRecords=sum(i['publishedVersionRecords'] for i in inputs),deferredDenoRootNames=len(full['inputs'])-len(inputs),closedIntakeNameShapeUnavailable=full['closedIntakeNameShapeUnavailable'],publicAcquisitionPerformed=False,archivesDownloaded=False,registryCacheModified=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(target/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(len(inputs),receipt['publishedVersionRecords'])
