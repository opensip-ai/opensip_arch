"""Reproduce this history candidate in a mutable copy; not independent approval."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
PYTHON='/tmp/opensip-implementation/metadata-reference-env/bin/python'
outputs=['graph-query.history-candidate.schema.json','explicit-history-panel.schema.json','history-command-flags.json','history-route-goldens.json','common.history-candidate.schema.json','public-detail-registry.history-candidate.json','subject_run.py']
before={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in outputs}
rows=[]
for script in ['build_history.py','check.py','check_query.py','check_budget.py','mutants.py']:
 r=subprocess.run([PYTHON,'-I','-B',script],cwd=HERE,capture_output=True,text=True)
 name=script.removesuffix('.py');(HERE/('fullcheck-'+name+'.stdout')).write_text(r.stdout);(HERE/('fullcheck-'+name+'.stderr')).write_text(r.stderr)
 rows.append({'script':script,'exit':r.returncode});print(script,r.returncode,flush=True)
 if r.returncode:break
 if script=='build_history.py':assert before=={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in outputs},'generated source drift'
result={'standing':'Root local full reproduction; not actual-Claude review or product qualification','runs':rows,'allPassed':len(rows)==5 and all(r['exit']==0 for r in rows),'generatedByteIdentical':True}
(HERE/'fullcheck-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['allPassed'] else 1)
