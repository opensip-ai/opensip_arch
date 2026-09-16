"""Regenerate every proposed output and compare exact bytes to the prior build."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
label=sys.argv[1]
def outputs():
 rows=[]
 for name in ['composition-result.json','model-generation-result.json','metadata-composition-result.json','identity-composition-result.json']:
  rows.extend(json.loads((HERE/name).read_bytes())['outputs'])
 for name in ['planning-composition-result.json','output-policy-composition-result.json']:
  rows.append(json.loads((HERE/name).read_bytes())['output'])
 return {r['path']:hashlib.sha256((HERE/r['path']).read_bytes()).hexdigest() for r in rows}
before=outputs()
with (HERE/f'reproduce-{label}.stdout').open('xb') as out,(HERE/f'reproduce-{label}.stderr').open('xb') as err:
 proc=subprocess.run([sys.executable,'-I','-B',str(HERE/'regenerate.py'),'reproduce-'+label],cwd=HERE,stdout=out,stderr=err)
after=outputs();same=before==after
result={'standing':'Root exact proposed schema/model/owner generation reproducibility; no source selection or implementation acceptance','exitCode':proc.returncode,'outputCount':len(after),'before':before,'after':after,'passed':proc.returncode==0 and same}
(HERE/f'reproduction-{label}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'outputCount':len(after),'passed':result['passed']}));raise SystemExit(not result['passed'])
