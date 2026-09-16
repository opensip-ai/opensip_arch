import sys,os,json,hashlib,shutil
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
PKGDIR=S+'/helpers_succ'
if os.path.isdir(PKGDIR): shutil.rmtree(PKGDIR)
shutil.copytree(S+'/helpers_pkg',PKGDIR)
shutil.copy2(S+'/output/files/helpers-successor/ts_pilot.py',PKGDIR+'/helpers/ts_pilot.py')
sys.path.insert(0,PKGDIR)
from helpers import ts_pilot
g=ts_pilot.build_ts_run()
exp=g['store'].export()
raw=json.dumps(exp,indent=2,sort_keys=True)+chr(10)
sha=hashlib.sha256(raw.encode()).hexdigest()
ref=open(S+'/output/evidence/fcontrols/ts-lawful-default.store.json').read()
refsha=hashlib.sha256(ref.encode()).hexdigest()
print('successor runId ',g['runId'])
print('successor sha   ',sha)
print('predecessor sha ',refsha)
print('BYTE-IDENTICAL  ',sha==refsha)
json.dump({'successorRunId':g['runId'],'successorExportSha256':sha,'predecessorExportSha256':refsha,'byteIdentical':sha==refsha},open(S+'/output/evidence/fcontrols/successor-equivalence.json','w'),indent=1)
