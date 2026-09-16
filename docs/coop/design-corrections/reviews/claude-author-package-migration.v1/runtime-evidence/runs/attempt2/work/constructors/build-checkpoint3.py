"""Author-assisted reference checkpoint, not blind acceptance.

PORTABLE SUCCESSOR. Declared inputs only: --source (reference source root), --package (author
package root supplying the bundled helpers and export transport), --out (fresh output dir),
optional --helpers overlay. No historical ROOT/output helpers path, no sibling source25 and no
external check-blind13 transport is consulted. Construction logic below is byte-identical to
the historical entry point.
"""
from pathlib import Path
import copy,importlib.util,json,sys,tomllib,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
import author_portable as AP
_a=AP.arguments('Author-assisted reference checkpoint, not blind acceptance.')
SOURCE=_a.source;PACKAGE=_a.package;OUTROOT=AP.fresh_out(_a.out)
F=AP.foundation(SOURCE)
AP.load_helpers(PACKAGE,_a.helpers,kit=_a.kit,out=OUTROOT)
from helpers import runs
out=OUTROOT/'checkpoint3';out.mkdir()
graph=runs.build_ts_run();export=graph['store'].export()
(out/'ts.store.json').write_text(json.dumps(export,indent=2,sort_keys=True)+'\n')
claim=[{'name':'author-ts','path':'ts.store.json','runId':graph['runId']}]
(out/'claims.json').write_text(json.dumps(claim,indent=2)+'\n')
print(json.dumps({'standing':'Author-assisted construction only; no admission claim','runId':graph['runId'],'objects':len(export['objectTable'])}))
AP.write_provenance(_a)
