"""Replay pinned author exports in fresh subprocesses; never claim independent review."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
EXPECTED_SOURCE='a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
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
# A group that crashes, or a query step that aborts, must still be RECORDED. Earlier this file
# asserted mid-flight, so a failing run produced no verification.json at all and the failure had
# to be reconstructed from stray stdout. Every expected admission, refusal and clause below is
# unchanged and no expectation is weakened; only the reporting path is.
for name,is_negative in [('checkpoint3',False),('normalized-examples6',False),('rust-selection-examples1',False),('semantic-controls1',True),('binding-controls',None)]:
 out=a.out/name
 cmd=[sys.executable,'-I','-B',str(ROOT/'check-export.v4.py'),'--input',str(ROOT/name),'--claims',str(ROOT/name/'claims.json'),'--source',str(a.source),'--out',str(out)]
 row={'group':name,'negativeControls':is_negative,'passed':False,'count':0,'reportSha256':None}
 try:
  proc=subprocess.run(cmd,capture_output=True,text=True)
  (a.out/(name+'.stdout.json')).write_text(proc.stdout);(a.out/(name+'.stderr.txt')).write_text(proc.stderr)
  report=json.loads((out/'report.json').read_text());checks=report['checks']
  if is_negative is None:
   passed=proc.returncode==1 and len(checks)==3 and all(r['ownerAdmission']=='ADMIT' and ((r['name']=='ts-invalid-default-entry' and r['semanticAdmission']=='REFUSE' and 'ENUMERATION_BINDING_PROGRAM_ENTRY' in r['reason']) or (r['name']!='ts-invalid-default-entry' and r['semanticAdmission']=='ADMIT')) for r in checks)
  elif is_negative:
   passed=proc.returncode==1 and len(checks)==3 and all(r['ownerAdmission']=='ADMIT' and r['semanticAdmission']=='REFUSE' and r['reason']=='EVALUATOR_COMPLETE_PROOF_REPLAY' for r in checks)
  else:passed=proc.returncode==0 and report['passed'] is True and all(r['ownerAdmission']=='ADMIT' and r['semanticAdmission']=='ADMIT' for r in checks)
  row.update(passed=passed,count=len(checks),reportSha256=sha(out/'report.json'),
             observed=[{'name':r['name'],'ownerAdmission':r['ownerAdmission'],'semanticAdmission':r['semanticAdmission'],'reason':r.get('reason')} for r in checks],
             exitCode=proc.returncode)
 except Exception as exc:
  row['failure']={'stage':'group','error':type(exc).__name__,'detail':str(exc)[:1000]}
 results.append(row)
 print(name,row['passed'],flush=True)
# Query reproduction is a separate measured boundary, now part of package verification.
query_commands = [
 [sys.executable,'-I','-B',str(ROOT/'check-author-query.py'),'--source',str(a.source),
  '--package',str(ROOT),'--out',str(a.out/'query-checks')],
 [sys.executable,'-I','-B',str(ROOT/'assess-author-query.py'),'--input',str(a.out/'query-checks'),
  '--out',str(a.out/'query-assessment.json')],
]
query_row={'group':'query','negativeControls':None,'passed':False,'count':0,'reportSha256':None}
try:
 for index,cmd in enumerate(query_commands):
  proc=subprocess.run(cmd,capture_output=True,text=True,timeout=600)
  (a.out/('query-step-%d.stdout' % index)).write_text(proc.stdout)
  (a.out/('query-step-%d.stderr' % index)).write_text(proc.stderr)
  if proc.returncode!=0:raise AssertionError('query step %d exited %d' % (index,proc.returncode))
 query=json.loads((a.out/'query-assessment.json').read_text())
 # Same expectation as before: all seven checks, all passed.
 if query['passed'] is not True or len(query['checks'])!=7:
  raise AssertionError('query assessment passed=%r checks=%d' % (query['passed'],len(query['checks'])))
 query_row.update(passed=True,count=len(query['checks']),reportSha256=sha(a.out/'query-assessment.json'))
except Exception as exc:
 query_row['failure']={'stage':'query','error':type(exc).__name__,'detail':str(exc)[:1000]}
results.append(query_row)
print('query',query_row['passed'],flush=True)
result={'standing':'Author reference package revalidation only. Seven valid synthetic Runs plus three separately reminted negative controls and three binding controls. Not independent reconstruction, compiler qualification or implementation authorization.','sourceManifestSha256':EXPECTED_SOURCE,'packageManifestSha256':sha(ROOT/'artifact-manifest.json'),'sourceFilesVerified':len(source['files']),'packageFilesVerified':len(package['files']),'groups':results,'passed':all(r['passed'] for r in results)}
(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],result
