from pathlib import Path
import os,json,hashlib,subprocess
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-large-context-2026-10-10';S=B/'sm-command-data-controls-r1-stage';parent=json.loads((S/'source.json').read_bytes());assert not V.exists();V.mkdir()
def check(root,row):
 raw=(root/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
for row in parent['finalSourcePins']:check(Path(parent['isolatedProducer']),row)
subprocess.run(['/bin/cp','-cR',parent['isolatedProducer'],str(V/'producer')],check=True)
subprocess.run(['/bin/cp','-cR',str(B/'sm-command-data-2026-10-10/check-target'),str(V/'check-target')],check=True)
for row in parent['finalSourcePins']:check(V/'producer',row)
(V/'preparation.json').write_text(json.dumps(dict(standing='NEW ISOLATED EXACT CLOSED STATIC-COMMAND PRODUCER AND CHECK CACHE COPIES; NO AUTHORING OR BUILD YET',parentProducer=parent['isolatedProducer'],parentSourcePins=parent['finalSourcePins'],parentImage=parent['compiledCargoImage'],sourceFiles=len(parent['finalSourcePins']),closedParentUnchanged=True,collectorRoots=0,compilerChildren=0,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False),indent=2)+'\n');print('Prepared isolated exact3130-source-file producer plus cloned check cache; no formatter/Cargo/collector/compiler run.')
