"""Root02 history/typed-query behavioral mutation controls in private copies."""
from pathlib import Path
import json,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parent
work=Path(tempfile.mkdtemp(prefix='opensip-history02-mutants-'))
sites=[
 ('format-route','history.py',"raise HistoryRefusal('OUTPUT.FORMAT_NOT_APPLICABLE', 'REQUEST.UNKNOWN_OPTION')","raise HistoryRefusal()",'check.py','test_exact_route_precedence'),
 ('count-route','history.py',"raise HistoryRefusal('EVALUATION.SELECTION_LIMIT')","raise HistoryRefusal()",'check.py','test_exact_route_precedence'),
 ('current-run-internal','history.py',"if current_run_id is not None and not valid_run_id(current_run_id):\n        raise HistorySourceRefusal()","if current_run_id is not None and not valid_run_id(current_run_id):\n        raise HistoryRefusal()",'check.py','test_current_run_malformed_is_internal'),
 ('project-join','query_history.py',"require(item['projectId']==project_id and item['runId']==run_id)","require(item['runId']==run_id)",'check.py','test_typed_query_project_and_receipt_joins'),
 ('history-receipt-join','history.py',"elif row.get('state')!='present' or row.get('run')!=item['result']:","elif row.get('state')!='present':",'check.py','test_typed_query_project_and_receipt_joins'),
 ('double-read-snapshot','history.py',"    with acquire_snapshot() as snapshot:\n","    with acquire_snapshot(): pass\n    with acquire_snapshot() as snapshot:\n",'check.py','test_one_read_snapshot_includes_committed_pivot_and_is_released'),
 ('panel-row-order','history.py',"if selection!=expected or [row['runId'] for row in panel['runs']]!=expected['requestedRunIds']:","if selection!=expected:",'check.py','test_explicit_panel_union_current_identity_and_provenance'),
 ('panel-current-row','history.py',"        if (row['state']=='current-run')!=(row['runId']==current_run_id):\n            raise HistorySourceRefusal()\n",'', 'check.py','test_explicit_panel_union_current_identity_and_provenance'),
 ('mandatory-close-run','query_history.py',"actual_id=identity_model.close_run(run,source['objects'],source['blobs'])","actual_id=run_id",'check_query.py','lost-retained-byte-exercises-owner'),
 ('requested-run-join','query_history.py',"    require(actual_id==run_id)\n",'', 'check_query.py','wrong-requested-run'),
 ('receipt-plan-join','query_history.py',"require(result.get('runId')==actual_id and result.get('planId')==run['planId'])","require(result.get('runId')==actual_id)",'check_query.py','wrong-receipt-plan'),
 ('receipt-verdict-join','query_history.py',"require(seal[0]=='evaluation-seal' and result.get('verdict')==seal[1]['verdict'])","require(seal[0]=='evaluation-seal')",'check_query.py','wrong-receipt-verdict'),
]
rows=[]
for name,file,before,after,script,witness in sites:
 dst=work/name;dst.mkdir()
 for item in ROOT.iterdir():
  if item.is_file():shutil.copy2(item,dst/item.name)
 p=dst/file;s=p.read_text();assert s.count(before)==1,(name,s.count(before));p.write_text(s.replace(before,after))
 r=subprocess.run(['/tmp/opensip-implementation/metadata-reference-env/bin/python','-I','-B',script],cwd=dst,capture_output=True,text=True)
 caught=r.returncode==1 and witness in r.stderr and ('FAIL:' in r.stderr or 'AssertionError:' in r.stderr)
 rows.append({'id':name,'script':script,'witness':witness,'exit':r.returncode,'caught':caught,'stdout':r.stdout,'stderr':r.stderr})
 print(name,'caught' if caught else 'NOT CAUGHT',flush=True)
 result={'standing':'root02 behavioral controls; no independent review or product qualification','work':str(work),'total':len(sites),'completed':len(rows),'caught':sum(x['caught'] for x in rows),'rows':rows}
 (ROOT/'mutant-results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if all(r['caught'] for r in rows) else 1)
