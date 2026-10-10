from pathlib import Path
import json,hashlib,subprocess,os,shutil
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');P=B/'sm-original-rustflags-2026-10-10';V=B/'sm-original-config-hierarchy-2026-10-10';assert not V.exists();checks=json.loads((P/'original-rustflags-checks-r2.json').read_bytes());assert checks['allPassed'];V.mkdir()
subprocess.run(['/bin/cp','-cR',str(P/'producer'),str(V/'producer')],check=True);subprocess.run(['/bin/cp','-cR',str(P/'check-target'),str(V/'check-target')],check=True)
parent=json.loads((P/'preparation.json').read_bytes());pins=[]
for row in parent['parentSourcePins']:
 old=(P/'producer'/row['path']).read_bytes();new=(V/'producer'/row['path']).read_bytes();assert old==new;pins.append(dict(path=row['path'],bytes=len(old),sha256=hashlib.sha256(old).hexdigest()))
receipt=dict(standing='ISOLATED EXACT PASSING ORIGINAL FLAG CANDIDATE COPY; PARENT REVIEW NOT YET SUBMITTED; NO CORPUS USE',parentProducer=str(P/'producer'),parentSourcePins=pins,sourceFiles=len(pins),collectorRoots=0,compilerChildren=0,nativeAdmission=False,SMComplete=False)
(V/'preparation.json').write_text(json.dumps(receipt,indent=2)+'\n');shutil.copyfile(Path(__file__),Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/continuation-preserved')/Path(__file__).name);print('Prepared isolated hierarchy candidate; prior candidates unchanged.')
