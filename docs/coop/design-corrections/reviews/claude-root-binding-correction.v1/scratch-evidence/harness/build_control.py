import sys,json,hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
sys.path.insert(0,S+'/helpers_pkg')
from helpers import runs, ts_pilot
g=ts_pilot.build_ts_run()
exp=g['store'].export()
raw=json.dumps(exp,indent=2,sort_keys=True)+chr(10)
open(S+'/output/evidence/fcontrols/ts-lawful.store.json','w').write(raw)
print('runId',g['runId'])
print('sha',hashlib.sha256(raw.encode()).hexdigest())
print('objects',len(exp['objectTable']))
