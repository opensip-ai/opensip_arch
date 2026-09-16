"""Independent semantic controls against the reference binding/projection boundary."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
source=(HERE/'fit_output.py').read_text()
controls=[
 ('source-dependency-removed',"if source_id not in step['dependsOn'] or step['dependencyGate']!='completed':","if step['dependencyGate']!='completed':",'test_closed_parameter_schema_and_relation_checks'),
 ('source-gate-removed',"if source_id not in step['dependsOn'] or step['dependencyGate']!='completed':","if source_id not in step['dependsOn']:",'test_closed_parameter_schema_and_relation_checks'),
 ('resolved-project-is-placeholder',"'projectId':record['projectId'],'view':{'runId':result['runId']}","'projectId':'prj1-'+'a'*64,'view':{'runId':result['runId']}",'test_source_step_binds_actual_run_and_project_without_plan_mutation'),
 ('query-summary-join-removed',"if not equal_typed(query['result'],summary):",'if False:','test_exact_completed_summary_and_request_are_required'),
 ('resolved-request-join-removed',"if report.get('state')!='sealed-run-first-page' or not equal_typed(report.get('request'),request):","if report.get('state')!='sealed-run-first-page':",'test_exact_completed_summary_and_request_are_required'),
 ('response-admission-bypassed',"summary = admit_report_and_derive_summary(report, record['projectId'],request['view']['runId'])","summary = query['result']",'test_changed_page_parity_and_other_source_run_are_refused'),
 ('handle-custody-join-removed','if not equal_typed(expected,completed_handle):','if False:','test_private_handle_joins_request_step_and_completed_attempt'),
 ('uncompleted-handle-ignored','if completed_handle is not None:','if False:','test_noncompleted_query_has_total_null_parity_and_actual_outcome'),
 ('completed-report-dropped',"out['advisoryReport']=copy.deepcopy(report)","out['advisoryReport']=ephemeral_report()",'test_completed_page_survives_cancellation_and_actual_static_render'),
 ('unavailable-outcome-forged',"'queryOutcome':query['outcome']","'queryOutcome':'cancelled'",'test_noncompleted_query_has_total_null_parity_and_actual_outcome'),
 ('existing-report-conflict-ignored',"if 'advisoryReport' in out and not equal_typed(out['advisoryReport'],report):",'if False:','test_changed_page_parity_and_other_source_run_are_refused'),
]
scratch=Path(tempfile.mkdtemp(prefix='opensip-fit01-controls-'));rows=[]
for name,old,new,witness in controls:
 assert source.count(old)==1,name
 altered=source.replace(old,new);compile(altered,name,'exec')
 target=scratch/name;shutil.copytree(HERE,target);(target/'fit_output.py').write_text(altered)
 proc=subprocess.run([sys.executable,'-I','-B',str(target/'check.py')],cwd=target,capture_output=True,text=True,timeout=30)
 caught=proc.returncode==1 and ('FAIL: '+witness+' ') in proc.stderr and 'ERROR:' not in proc.stderr
 rows.append({'id':name,'witness':witness,'caught':caught,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
 print(name,caught,flush=True)
result={'standing':'Root reference controls, not actual independent review','total':len(rows),'caught':sum(r['caught'] for r in rows),'scratch':str(scratch),'rows':rows}
(HERE/'mutant-results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['caught']==result['total'] else 1)
