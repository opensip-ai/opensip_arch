from pathlib import Path
import json,hashlib,subprocess,os
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');S=B/'sm-large-context-controls-r1-stage';V=B/'sm-original-rustflags-2026-10-10';assert not V.exists();source=json.loads((S/'source.json').read_bytes())
for row in source['finalSourcePins']:
 raw=(Path(source['isolatedProducer'])/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
V.mkdir();subprocess.run(['/bin/cp','-cR',source['isolatedProducer'],str(V/'producer')],check=True);subprocess.run(['/bin/cp','-cR',str(B/'sm-large-context-2026-10-10/check-target'),str(V/'check-target')],check=True)
(V/'preparation.json').write_text(json.dumps(dict(standing='ISOLATED EXACT FROZEN PARENT COPY; PARENT REVIEW PENDING; NO ACTUAL CORPUS USE',parentSubject=dict(path=str(S/'subject.json'),bytes=(S/'subject.json').stat().st_size,sha256=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest()),parentSourcePins=source['finalSourcePins'],parentImage=source['compiledCargoImage'],sourceFiles=len(source['finalSourcePins']),collectorRoots=0,compilerChildren=0,nativeAdmission=False,SMComplete=False),indent=2)+'\n')
print('Isolated original-rustflags candidate prepared; frozen parent left unchanged.')
