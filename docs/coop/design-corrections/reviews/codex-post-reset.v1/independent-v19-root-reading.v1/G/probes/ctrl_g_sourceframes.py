"""Concrete counterexample for the _SOURCE_FRAMES derivation advisory. Disposable copy only."""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC=ROOT/'docs/coop/design-corrections'
DOC=json.loads((DC/'native/protocol3-transitions.v1.json').read_text())
spec=importlib.util.spec_from_file_location('nem',DC/'native/native_evidence_model.v2.py')
N=importlib.util.module_from_spec(spec);sys.modules['nem']=N;spec.loader.exec_module(N)
R=[]
def ck(i,d,g,w): R.append({'id':i,'desc':d,'pass':g==w,'observed':g,'expected':w})

BEFORE_LITERAL={'OpenUniverse','SnapshotManifest','SnapshotFileChunk','DependencySourceManifest',
                'DependencySourceChunk','PreparedOutputManifest','PreparedOutputChunk'}
ck('G1:today-correct','TODAY the derived set equals the pre-v19 literal',
   sorted(N._SOURCE_FRAMES),sorted(BEFORE_LITERAL))
ck('G2:only-one-plural','exactly one stateUpdates entry uses the plural onFrames form',
   sum(1 for u in DOC['stateUpdates'] if 'onFrames' in u),1)
ck('G3:that-entry-sets-sourceBytes','and that entry is the sourceBytesSent one',
   [u for u in DOC['stateUpdates'] if 'onFrames' in u][0]['sets'].startswith('sourceBytesSent'),True)
# The drift control published beside it is `{f for u in stateUpdates for f in u.get('onFrames',())}
# == N._SOURCE_FRAMES`, which is the SAME expression the model uses. Show it has no discriminating
# power: perturb the document and the control still holds while the derived set changes.
doc2=json.loads(json.dumps(DOC))
doc2['stateUpdates'].append({'onFrames':['Cancel'],'sets':'someFutureFlag = true'})
derived2={f for u in doc2['stateUpdates'] for f in u.get('onFrames',())}
ck('G4:control-is-tautological',
   'a hypothetical future plural entry silently widens the set while the published drift control '
   'still holds, because both sides evaluate the same expression',
   [derived2==({f for u in doc2["stateUpdates"] for f in u.get("onFrames",())}),
    sorted(derived2)!=sorted(BEFORE_LITERAL),'Cancel' in derived2],[True,True,True])
ck('G5:no-independent-binding',
   'no control binds _SOURCE_FRAMES to an independent authority (a literal, a schema enum or the '
   'sets-text of the entry)',
   'sourceBytesSent' in (DC/'foundation/check-identity.py').read_text().split('_SOURCE_FRAMES')[0][-400:],
   False)
f=[r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-g.json').write_text(
  json.dumps({'controls':len(R),'failed':len(f),'failures':f,'results':R},indent=1))
print('CTRL-G controls=%d failed=%d'%(len(R),len(f)))
for x in f: print('  FAIL',x['id'],x['desc'],x['observed'],x['expected'])
