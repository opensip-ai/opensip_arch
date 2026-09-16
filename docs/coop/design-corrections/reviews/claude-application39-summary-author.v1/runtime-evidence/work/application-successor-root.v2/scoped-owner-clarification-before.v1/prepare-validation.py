"""Stage provenance-only pin delta and reproduce checks in a disposable accepted-source copy."""
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',type=Path,required=True);p.add_argument('--design-version',required=True);a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();files=stage/'files';support=stage/'support';support.mkdir(exist_ok=True)
dc='docs/coop/design-corrections/';py='/tmp/opensip-architecture-review-env/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,d):(support/n).write_text(json.dumps(d,indent=2)+'\n')
manifest=json.loads((root/(dc+f'reviews/candidate-subject.{a.design_version}.json')).read_text());snapshot=Path(manifest['snapshotRoot'])
assert all(sha(snapshot/r['path'])==r['sha256'] for r in manifest['files'])
scratch=stage.parent/(stage.name+'-validation');assert not scratch.exists();shutil.copytree(snapshot,scratch)
changed={str(p.relative_to(files)) for p in files.rglob('*') if p.is_file() and (not (root/p.relative_to(files)).exists() or sha(p)!=sha(root/p.relative_to(files)))}
intersections=[]
for unit in ['foundation','security','native','workflows']:
 for pin in (snapshot/(dc+unit)).glob('*pins*.json'):
  d=json.loads(pin.read_text())
  entries=d.get('pins',d.get('files',[]))
  if isinstance(entries,list):
   for r in entries:
    if isinstance(r,dict) and r.get('path') in changed:intersections.append({'manifest':str(pin.relative_to(snapshot)),'path':r['path']})
expected={dc+'native/source-pins.v2.json'};assert {r['manifest'] for r in intersections}==expected,intersections
assert {r['path'] for r in intersections}=={'docs/v2/architecture/03-configuration-and-security.md','docs/v2/architecture/10-mvp-and-future-scope.md'},intersections
pinrel=dc+'native/source-pins.v2.json';pins=json.loads((snapshot/pinrel).read_text());deltas=[]
for r in pins['pins']:
 if r['path'] in changed:
  old=r['sha256'];r['sha256']=sha(files/r['path']);deltas.append({'path':r['path'],'beforeSha256':old,'afterSha256':r['sha256']})
q=files/pinrel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(pins,indent=1)+'\n')
for f in files.rglob('*'):
 if f.is_file():q=scratch/f.relative_to(files);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,q)
commands=[('foundation',[dc+'foundation/run-reference-checks.py','--report',str(support/'foundation.json')]),('security',[dc+'security/check-security-lifecycle.v1.py','--report',str(support/'security.json')]),('native',[dc+'native/check_native_evidence.v2.py']),('workflows',[dc+'workflows/run-reference-checks.py','--report',str(support/'workflows.json')]),('workflow-surface',[dc+'workflows/check_workflows.v1.py','--report',str(support/'workflow-surface.json')]),('integration',[dc+'check-integration.py','--report',str(support/'integration.json')])]
results=[]
for name,args in commands:
 r=subprocess.run([py,'-I','-B']+args,cwd=scratch,capture_output=True,text=True);(support/(name+'.log')).write_text(r.stdout+r.stderr);results.append({'name':name,'command':[py,'-I','-B']+args,'exitCode':r.returncode});print(name,r.returncode,r.stdout[-250:],flush=True)
 assert r.returncode==0, name+' failed; inspect log'
reportrel=dc+'native/native-evidence-report.v2.json';q=files/reportrel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(scratch/reportrel,q)
save('native-recording-delta.v1.json',{'standing':'Prospective provenance-only current recording successor; accepted design archive unchanged','intersections':intersections,'sourceChanges':deltas,'pinManifest':{'path':pinrel,'beforeSha256':sha(root/pinrel),'afterSha256':sha(files/pinrel)},'report':{'path':reportrel,'beforeSha256':sha(root/reportrel),'afterSha256':sha(files/reportrel),'actualResult':json.loads((files/reportrel).read_text())['result']},'productContractModelSchemaChanges':False})
# Documentation application tooling is separately exercised in disposable synthetic roots.
# Synthetic ACCEPT labels in this test are never actual project review evidence.
for name in ['check-finalizer.py','check-finalizer.initial.py','finalize-application.before-selftest.py','finalizer-selftest-development-note.json','verify-applied.py','run-applied-reference-checks.py','legacy-current-before.json','legacy-preapplication-provenance.v1.json','harden-required-findings.v1.py','required-findings-hardening.v1.json','required-findings-selftest.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('required-findings-before.v1'),support/'required-findings-before.v1')
for name in ['assemble-records.py','prepare-validation.py','launch-application-review.py','clarify-application-evidence.v1.py','evidence-clarification.v1.json','subject-envelope-adapter-custody.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['evidence-clarification-before.v1','subject-envelope-adapter.v1']:
 shutil.copytree(Path(__file__).with_name(name),support/name)
finalizer=files/(dc+'finalize-application.v1.py')
selftest=subprocess.run([py,'-I','-B',str(support/'check-finalizer.py'),'--source',str(finalizer),'--report',str(support/'finalizer-selftest.v1.json')],capture_output=True,text=True)
(support/'finalizer-selftest.log').write_text(selftest.stdout+selftest.stderr)
assert selftest.returncode==0,selftest.stderr
selftest_result=json.loads((support/'finalizer-selftest.v1.json').read_text())
assert selftest_result['failed']==[] and selftest_result['actualApplicationPerformed'] is False
assert selftest_result['sourceSha256']==sha(finalizer)
save('staged-reference-checks.v1.json',{'scratchRoot':str(scratch),'commands':results,'acceptedDesignFileCount':len(manifest['files']),'implementationQualification':False})
