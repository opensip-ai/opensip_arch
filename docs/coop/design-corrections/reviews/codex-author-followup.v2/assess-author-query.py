from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
rows={r['name']:r for r in json.loads((ROOT/'query-checks1/observations.json').read_text())};checks=[]
def check(name,condition,basis):
 assert condition,name
 checks.append({'name':name,'passed':True,'basis':basis})
n=rows['neighbors']['response'];inc=rows['incoming']['response'];reach=rows['reach']['response'];bounded=rows['bounded']['response']
check('retained outgoing import',len(n['items'])==1 and n['items'][0]['source']['nativeSubjectId']=='symbol:src/index.ts::x','Exact retained source endpoint and one resolved import edge.')
check('retained incoming empty disclosure',not inc['items'] and bool(inc['context']['evidence']['resolutionLimitations']),'Empty retained traversal includes evidence limitations; never a proof that no callers/importers exist globally.')
check('retained reach',len(reach['items'])==1,'One reachable endpoint in this retained graph.')
check('explicit historical Run unaffected by latest',rows['historical']['response']==n,'Changing host.latestRunId does not change an explicit Run-bound response.')
check('work-bound emptiness not exact absence',bounded['context']['truncated'] and bounded['context']['countBasis']=='lower-bound' and bounded['termination']['class']=='indeterminate','Limit hit with owed work is indeterminate, even when no items were returned.')
check('wrong Run refused',rows['wrong-run']['code']=='IDENTITY.UNKNOWN' and rows['wrong-run']['detail']=='QUERY.VIEW_UNKNOWN','An unrelated requested Run cannot borrow this evidence.')
check('purged evidence unavailable',rows['purged']['code']=='HOST.IO_FAILURE' and rows['purged']['detail']=='evidence.purged','Trusted current availability refuses as unavailable rather than returning an empty graph.')
(ROOT/'query-checks1/assessment.json').write_text(json.dumps({'standing':'Author reference checks on exact admitted TS Run; synthetic host observations; not independent query reconstruction or storage/engine qualification.','passed':True,'checks':checks},indent=2)+'\n');print('PASS',len(checks),'author query checks')
