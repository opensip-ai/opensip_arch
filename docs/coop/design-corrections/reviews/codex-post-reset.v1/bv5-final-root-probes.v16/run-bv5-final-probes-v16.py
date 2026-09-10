"""Capture root's final-source probes. Execution success is NOT semantic acceptance."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=a.root.resolve();out=a.out.resolve();out.mkdir(exist_ok=False);here=Path(__file__).parent
names=['probe-bv5-rc1-full-run.py','probe-bv5-resolved-classes.py','probe-bv5-scope-membership.py','probe-bv5-draft-rc1.py']
rows=[]
for name in names:
 source=here/name;shutil.copyfile(source,out/name)
 command=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(out/name),str(root)]
 r=subprocess.run(command,cwd=root,capture_output=True,timeout=120)
 result=out/(source.stem+'.result.json');result.write_bytes(r.stdout);(out/(source.stem+'.stderr.log')).write_bytes(r.stderr)
 parsed=False
 if r.returncode==0:
  try:json.loads(r.stdout);parsed=True
  except (ValueError,UnicodeError):pass
 rows.append({'probe':name,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'command':command,'exitCode':r.returncode,'result':result.name,'resultSha256':hashlib.sha256(r.stdout).hexdigest(),'parsed':parsed})
 print(name,'exit',r.returncode,'parsed',parsed,flush=True)
checks=['foundation/identity-model.py','native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','integration-fixtures.py']
report={'standing':'Executed root-selected final-source counterexample probes. Results require substantive positive/refusal assessment; exit0 only means probe executed. No product/independent/design/readiness acceptance.','sourceRoot':str(root),'executionSucceeded':all(r['exitCode']==0 and r['parsed'] for r in rows),'semanticAssessmentPending':True,'sources':[{'path':'docs/coop/design-corrections/'+s,'sha256':hashlib.sha256((root/'docs/coop/design-corrections'/s).read_bytes()).hexdigest()} for s in checks],'commands':rows}
(out/'execution.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/Path(__file__).name)
