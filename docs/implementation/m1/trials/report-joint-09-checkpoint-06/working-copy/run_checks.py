"""Run current joint checks with preserved per-process exits and public logs."""
from pathlib import Path
import subprocess,sys,json
HERE=Path(__file__).resolve().parent
label=sys.argv[1];rows=[]
# Feature checks produce the audit fixture for shared/projection regressions.
# Parent-base checks construct all scenarios consumed by catalogue/output checks.
# Run both producers before their consumers; never reuse previous-run fixtures.
for script in ['check_model_carriers.py','check_metadata.py','check_common_succession.py','check_identity_integration.py','check_new_plan.py','check_output_policy.py','check_planning.py','check_workflow5.py','check_document.py','check_catalogue_joins.py','check_feature_integration.py','check_shared_projection.py','check_parent_regression.py','check_query_commands.py','check_fit_documents.py','check_parent_bases.py','check_catalogue_sources.py','check_output_integration.py']:
 name=f'checks-{label}-{len(rows)+1:02}-{Path(script).stem}'
 with (HERE/(name+'.stdout')).open('xb') as out,(HERE/(name+'.stderr')).open('xb') as err:
  p=subprocess.run([sys.executable,'-I','-B',str(HERE/script)],cwd=HERE,stdout=out,stderr=err)
 rows.append({'script':script,'exitCode':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
 (HERE/f'checks-{label}.json').write_text(json.dumps({'standing':'Root combined reference checks only; not Claude or product acceptance','phases':rows,'passed':all(r['exitCode']==0 for r in rows)},indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
print(json.dumps({'phases':len(rows),'passed':True}))
