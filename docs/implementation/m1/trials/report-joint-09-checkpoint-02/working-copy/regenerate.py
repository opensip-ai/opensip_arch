"""Sequential generation with explicit exit statuses and preserved phase logs."""
from pathlib import Path
import subprocess,sys,json
HERE=Path(__file__).resolve().parent
label=sys.argv[1];rows=[]
for script in ['compose_sources.py','check_sources.py','generate_models.py','derive_budget.py','apply_budget.py','check_sources.py']:
 name=f'regeneration-{label}-{len(rows)+1:02}-{Path(script).stem}'
 with (HERE/(name+'.stdout')).open('xb') as out,(HERE/(name+'.stderr')).open('xb') as err:
  p=subprocess.run([sys.executable,'-I','-B',str(HERE/script)],cwd=HERE,stdout=out,stderr=err)
 rows.append({'script':script,'exitCode':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
 (HERE/f'regeneration-{label}.json').write_text(json.dumps({'phases':rows,'passed':all(r['exitCode']==0 for r in rows)},indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
print(json.dumps({'phases':len(rows),'passed':True}))
