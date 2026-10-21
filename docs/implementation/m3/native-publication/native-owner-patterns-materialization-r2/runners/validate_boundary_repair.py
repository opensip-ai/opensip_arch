from pathlib import Path
import os,subprocess,json
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
assert json.loads((F/'inherited-boundary-focused-r1/report.json').read_text())['allPassed']
for path in [F/'ecma-full-differential-r4/run.py',F/'native_mutations_r2.py',F/'companion_mutations_r2.py',F/'full_materialization_lane_r5.py']:
 print('RUN '+path.name,flush=True)
 subprocess.run([PY,'-I','-B',str(path)],cwd='/Users/sb/code',check=True)
print('REPAIRED DIFFERENTIAL/MUTATIONS/FULL OWNING SEQUENCE TERMINAL',flush=True)
