from pathlib import Path
import json,hashlib,subprocess,os
B=Path('/tmp/opensip-implementation');V=B/'sm-command-data-2026-10-10';PARENT=B/'sm-unit-context-controls-r1-stage';src=json.loads((PARENT/'source.json').read_bytes());assert not V.exists();V.mkdir()
for row in src['finalSourcePins']:
 b=(Path(src['isolatedProducer'])/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
subprocess.run(['/bin/cp','-cR',src['isolatedProducer'],str(V/'producer')],check=True)
subprocess.run(['/bin/cp','-cR',str(B/'sm-cargo-unit-context-2026-10-10/check-target'),str(V/'check-target')],check=True)
for row in src['finalSourcePins']:
 b=(V/'producer'/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
(V/'preparation.json').write_text(json.dumps(dict(parentProducer=src['isolatedProducer'],parentSourcePins=src['finalSourcePins'],parentImage=src['compiledCargoImage'],copiedRegularPins=len(src['finalSourcePins']),controlsRun=False,actualCorpusUse=False,nativeAdmission=False,SMComplete=False),indent=2)+'\n');print('New isolated producer/check target prepared; accepted producer remains unchanged.')
