"""Replay pinned author exports in fresh subprocesses; never claim independent review."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
EXPECTED_SOURCE='29ea3a6ee8c5bfce710816c4f6a818ef9e18a7dc6bf9b8efd944eb3e6b4e4493'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(root,row):
 rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
 path=root/rel;assert path.is_file() and sha(path)==row['sha256'],str(path)
 if 'bytes' in row:assert path.stat().st_size==row['bytes'],str(path)
p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
assert not a.out.exists(),'Use a new output directory; preserve earlier evidence.'
manifest=ROOT/'source-manifest.json';assert sha(manifest)==EXPECTED_SOURCE
source=json.loads(manifest.read_text())
for row in source['files']:checked(a.source,row)
package=json.loads((ROOT/'artifact-manifest.json').read_text())
for row in package['files']:checked(ROOT,row)
a.out.mkdir(parents=True);results=[]
for name,is_negative in [('checkpoint3',False),('normalized-examples6',False),('rust-selection-examples1',False),('semantic-controls1',True),('binding-controls',None)]:
 out=a.out/name
 cmd=[sys.executable,'-I','-B',str(ROOT/'check-export.v4.py'),'--input',str(ROOT/name),'--claims',str(ROOT/name/'claims.json'),'--source',str(a.source),'--out',str(out)]
 proc=subprocess.run(cmd,capture_output=True,text=True)
 (a.out/(name+'.stdout.json')).write_text(proc.stdout);(a.out/(name+'.stderr.txt')).write_text(proc.stderr)
 report=json.loads((out/'report.json').read_text());checks=report['checks']
 if is_negative is None:
  passed=proc.returncode==1 and len(checks)==3 and all(r['ownerAdmission']=='ADMIT' and ((r['name']=='ts-invalid-default-entry' and r['semanticAdmission']=='REFUSE' and 'ENUMERATION_BINDING_PROGRAM_ENTRY' in r['reason']) or (r['name']!='ts-invalid-default-entry' and r['semanticAdmission']=='ADMIT')) for r in checks)
 elif is_negative:
  passed=proc.returncode==1 and len(checks)==3 and all(r['ownerAdmission']=='ADMIT' and r['semanticAdmission']=='REFUSE' and r['reason']=='EVALUATOR_COMPLETE_PROOF_REPLAY' for r in checks)
 else:passed=proc.returncode==0 and report['passed'] is True and all(r['ownerAdmission']=='ADMIT' and r['semanticAdmission']=='ADMIT' for r in checks)
 results.append({'group':name,'negativeControls':is_negative,'passed':passed,'count':len(checks),'reportSha256':sha(out/'report.json')})
 print(name,passed,flush=True)
result={'standing':'Author reference package revalidation only. Seven valid synthetic Runs plus three separately reminted negative controls and three binding controls. Not independent reconstruction, compiler qualification or implementation authorization.','sourceManifestSha256':EXPECTED_SOURCE,'packageManifestSha256':sha(ROOT/'artifact-manifest.json'),'sourceFilesVerified':len(source['files']),'packageFilesVerified':len(package['files']),'groups':results,'passed':all(r['passed'] for r in results)}
(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],result
