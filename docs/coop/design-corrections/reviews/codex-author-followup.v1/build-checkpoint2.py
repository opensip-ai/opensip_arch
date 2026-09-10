"""Author-assisted reference checkpoint, not blind acceptance."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'output'))
from helpers import runs
out=ROOT/'checkpoint2';out.mkdir()
graph=runs.build_ts_run();export=graph['store'].export()
(out/'ts.store.json').write_text(json.dumps(export,indent=2,sort_keys=True)+'\n')
claim=[{'name':'author-ts','path':'ts.store.json','runId':graph['runId']}]
(out/'claims.json').write_text(json.dumps(claim,indent=2)+'\n')
print(json.dumps({'standing':'Author-assisted construction only; no admission claim','runId':graph['runId'],'objects':len(export['objectTable'])}))
