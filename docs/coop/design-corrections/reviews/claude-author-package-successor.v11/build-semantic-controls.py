"""Author mutation controls; exact independent owner execution follows separately.

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
_a=AP.arguments('Author mutation controls; exact independent owner execution follows separately.',extra=[('--positive',dict(required=True,type=Path,help='directory holding the FRESHLY REMINTED positive checkpoint3 (claims.json + ts.store.json) that these controls must be derived from'))])
SOURCE=_a.source;PACKAGE=_a.package;OUTROOT=AP.fresh_out(_a.out)
F=AP.foundation(SOURCE)
AP.load_helpers(PACKAGE,_a.helpers,kit=_a.kit,out=OUTROOT)
from helpers import store,order
src=_a.positive.resolve()
claims=json.loads((src/'claims.json').read_text())
raw=json.loads((src/'ts.store.json').read_text())
out=OUTROOT/'semantic-controls1';out.mkdir();result=[]
for mutation in ['severity','unrelated-scope','collapsed-deficiencies']:
 st=store.load_export(copy.deepcopy(raw));rid=claims[0]['runId'];run=copy.deepcopy(st.objects[rid])
 eid=run['evidenceId'];evidence=copy.deepcopy(st.objects[eid]);sid=run['evaluationSealId'];seal=copy.deepcopy(st.objects[sid]);pid=evidence['proofBundleId'];proof=copy.deepcopy(st.objects[pid])
 if mutation=='severity':
  fid=proof['findingIds'][0];finding=copy.deepcopy(st.objects[fid]);assert finding['severity']=='error';finding['severity']='note';newfid=st.put_canonical_record('finding',finding)
  proof['findingIds']=order.cset([newfid if x==fid else x for x in proof['findingIds']])
  for rr in proof['ruleResults']:rr['findingIds']=order.cset([newfid if x==fid else x for x in rr['findingIds']])
 elif mutation=='unrelated-scope':
  pp=proof['predicateProofs'][0];scope=next(i for i in st.objects if i.startswith('scope2:') and i not in pp['scopeIds']);pp['scopeIds']=order.cset(pp['scopeIds']+[scope])
 else:
  assert len(proof['executionDeficiencies'])==2
  first,second=proof['executionDeficiencies'];first['inputRefs']=order.cset(first['inputRefs']+second['inputRefs']);proof['executionDeficiencies']=[first]
 newpid=st.put_canonical_record('proof-bundle',proof)
 evidence['proofBundleId']=newpid;evidence['findingIds']=proof['findingIds'];neweid=st.put_canonical_record('semantic-evidence',evidence)
 seal['proofBundleId']=newpid;seal['evidenceId']=neweid;newsid=st.put_canonical_record('evaluation-seal',seal)
 run['evaluationSealId']=newsid;run['evidenceId']=neweid;newrid=st.put_canonical_record('run',run)
 for old in [rid,eid,sid,pid]:del st.objects[old]
 st.meta.update(runId=newrid,proofId=newpid)
 name=mutation+'.store.json';(out/name).write_text(json.dumps(st.export(),indent=2,sort_keys=True)+'\n')
 result.append({'name':mutation,'path':name,'runId':newrid})
(out/'claims.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
AP.write_provenance(_a)
