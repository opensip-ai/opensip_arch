"""Capture selected root controls on final coauthor source; semantic assessment is separate."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=a.root.resolve();out=a.out.resolve();out.mkdir(exist_ok=False);here=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
h=json.loads((root.parent/'handoff.json').read_text());assert h['technicalAssent']['value'] is True
assert json.loads((root.parent/'response.json').read_text())['is_error'] is False
files=h['changedSource']['files'];before={r['path']:sha(root/r['path']) for r in files}
rows=[]
for name in ['probe-bv6-scope-overlap-v3.py','probe-bv6-scope-no-coverage-v1.py','probe-bv6-requirement-draft.py','probe-bv6-final-v3-imported.py']:
 source=here/name;shutil.copyfile(source,out/name)
 command=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(out/name),str(root)]
 r=subprocess.run(command,cwd=root,capture_output=True,timeout=120)
 result=out/(source.stem+'.result.json');result.write_bytes(r.stdout);(out/(source.stem+'.stderr.log')).write_bytes(r.stderr)
 parsed=False
 if r.returncode==0:
  try:json.loads(r.stdout);parsed=True
  except (ValueError,UnicodeError):pass
 rows.append({'probe':name,'sourceSha256':sha(source),'command':command,'exitCode':r.returncode,'result':result.name,'resultSha256':sha(result),'parsed':parsed})
 print(name,'exit',r.returncode,'parsed',parsed,flush=True)
assert all(sha(root/rel)==digest for rel,digest in before.items())
(out/'execution.json').write_text(json.dumps({'standing':__doc__,'sourceRoot':str(root),'sources':before,'executionSucceeded':all(r['exitCode']==0 and r['parsed'] for r in rows),'semanticAssessmentPending':True,'commands':rows},indent=2)+'\n')
shutil.copyfile(__file__,out/Path(__file__).name)
