"""Rebuild and verify from source-only staging with no prior generated fixtures."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
label=sys.argv[1]
dest=HERE.parent/('m1-report-joint-clean-'+label)
dest.mkdir()
inputs=['input-subjects.json','workflow-input-pins.json','supplemental-inputs.json']
files=list(HERE.glob('*.py'))+[HERE/n for n in inputs]
files += [p for p in (HERE/'parent-report08').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
rows=[]
for p in sorted(files):
 rel=p.relative_to(HERE);raw=p.read_bytes();target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 rows.append({'path':str(rel),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
assert not list(dest.glob('*.fixture.json'))
assert not (dest/'composed-sources').exists()
assert not (dest/'models').exists()
result={'standing':'Root source-only clean staging verification; external pinned subjects remain required, not a hermetic sandbox or product qualification','directory':str(dest),'initialFiles':rows,'initialGeneratedFixtures':0,'initialGeneratedSchemaAndModelDirectories':0,'phases':[],'passed':False}
outpath=HERE/('clean-staging-'+label+'.json')
for args in [['regenerate.py','initial'],['verify_candidate.py','clean']]:
 stem=Path(args[0]).stem
 with (dest/(stem+'.stdout')).open('xb') as out,(dest/(stem+'.stderr')).open('xb') as err:
  p=subprocess.run([sys.executable,'-I','-B',str(dest/args[0]),*args[1:]],cwd=dest,stdout=out,stderr=err)
 result['phases'].append({'args':args,'exitCode':p.returncode})
 outpath.write_text(json.dumps(result,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
result['verification']=json.loads((dest/'verification-clean.json').read_bytes())
result['passed']=result['verification']['complete'] and result['verification']['passed']
outpath.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'directory':str(dest),'passed':result['passed']}))
