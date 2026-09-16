"""Sequential candidate verification with explicit expected inventory differences."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent
label=sys.argv[1];rows=[]
phases=[(['check_frozen_inputs.py'],0),(['reproduce.py',label],0),(['run_checks.py',label],0),(['check_all_parent_cases.py'],1),(['reconcile_parent_cases.py'],0)]
for args,expected in phases:
 name=f'verification-{label}-{len(rows)+1:02}-{Path(args[0]).stem}'
 with (HERE/(name+'.stdout')).open('xb') as out,(HERE/(name+'.stderr')).open('xb') as err:
  p=subprocess.run([sys.executable,'-I','-B',str(HERE/args[0]),*args[1:]],cwd=HERE,stdout=out,stderr=err)
 rows.append({'args':args,'exitCode':p.returncode,'expectedExitCode':expected,'passed':p.returncode==expected,'stdout':name+'.stdout','stderr':name+'.stderr'})
 result={'standing':'Root candidate reference verification only; inventory exit1 records eight explicit predecessor-witness differences, checked by subsequent reconciliation; no actual Claude or product acceptance','phases':rows,'complete':len(rows)==len(phases),'passed':all(r['passed'] for r in rows)}
 (HERE/f'verification-{label}.json').write_text(json.dumps(result,indent=2)+'\n')
 if p.returncode!=expected:raise SystemExit(1)
print(json.dumps({'phases':len(rows),'passed':True}))
