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
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import application_pins
recording_delta=application_pins.prepare(snapshot,files)
for f in files.rglob('*'):
 if f.is_file():q=scratch/f.relative_to(files);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,q)
runner=Path(__file__).with_name('run-application-reference-suites.py')
result=subprocess.run([py,'-I','-B',str(runner),'--root',str(scratch),'--out',str(support/'reference-rerun')],capture_output=True,text=True)
(support/'reference-rerun.log').write_text(result.stdout+result.stderr)
assert result.returncode==0,result.stderr
measured=json.loads((support/'reference-rerun/reference-checks.json').read_text());results=measured['commands']
assert measured['passed'] and len(results)==7
reportrel=dc+'native/native-evidence-report.v2.json';q=files/reportrel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(scratch/reportrel,q)
recording_delta['report']={'path':reportrel,'beforeSha256':sha(snapshot/reportrel),'afterSha256':sha(q),'actualResult':json.loads(q.read_text())['result']}
save('native-recording-delta.v1.json',recording_delta)
# Documentation application tooling is separately exercised in disposable synthetic roots.
# Synthetic ACCEPT labels in this test are never actual project review evidence.
for name in ['check-finalizer.py','check-finalizer.initial.py','finalize-application.before-selftest.py','finalizer-selftest-development-note.json','verify-applied.py','run-applied-reference-checks.py','legacy-current-before.json','legacy-preapplication-provenance.v1.json','harden-required-findings.v1.py','required-findings-hardening.v1.json','required-findings-selftest.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('required-findings-before.v1'),support/'required-findings-before.v1')
shutil.copytree(Path(__file__).with_name('public-custody-before-compaction.v1'),support/'public-custody-before-compaction.v1')
shutil.copytree(Path(__file__).with_name('row-map-input-before.v1'),support/'row-map-input-before.v1')
shutil.copytree(Path(__file__).with_name('subject-shape-before.v1'),support/'subject-shape-before.v1')
for name in ['check-review-envelope.v2.py','check-review-envelope.v2.report.json','subject-shape-integration.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
# v1 row checker/report retained as history; v2 is the portable current command.
for name in ['check-application-rows.v1.py','check-application-rows.v1.json','check-application-rows.v2.py','check-application-rows.v2.json','row-map-input-integration.v1.json','row-checker-portability.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['check-retain-public.v2.report.json','application-compaction-root-counterexamples.v1.json','public-custody-compaction-integration.v1.json','public-custody-real-stream-check.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['assemble-records.py','prepare-validation.py','launch-application-review.py','clarify-application-evidence.v1.py','evidence-clarification.v1.json','subject-envelope-adapter-custody.v1.json','clarify-scoped-owner-authority.v1.py','scoped-owner-clarification.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['evidence-clarification-before.v1','subject-envelope-adapter.v1','scoped-owner-clarification-before.v1']:
 shutil.copytree(Path(__file__).with_name(name),support/name)
shutil.copyfile(Path(__file__).with_name('relative-reference-clarification.v1.json'),support/'relative-reference-clarification.v1.json')
shutil.copytree(Path(__file__).with_name('relative-reference-before.v1'),support/'relative-reference-before.v1')
shutil.copyfile(Path(__file__).with_name('current-review-prompt-clarification.v1.json'),support/'current-review-prompt-clarification.v1.json')
shutil.copytree(Path(__file__).with_name('current-review-prompt-before.v1'),support/'current-review-prompt-before.v1')
shutil.copyfile(Path(__file__).with_name('v13-scope-clarification.v1.json'),support/'v13-scope-clarification.v1.json')
shutil.copytree(Path(__file__).with_name('v13-scope-before.v1'),support/'v13-scope-before.v1')
shutil.copyfile(Path(__file__).with_name('applied-summary-verifier-custody.v1.json'),support/'applied-summary-verifier-custody.v1.json')
shutil.copytree(Path(__file__).with_name('applied-summary-verifier-before.v1'),support/'applied-summary-verifier-before.v1')
shutil.copyfile(Path(__file__).with_name('application-review-advisory-coverage.v1.json'),support/'application-review-advisory-coverage.v1.json')
shutil.copytree(Path(__file__).with_name('application-review-advisory-coverage-before.v1'),support/'application-review-advisory-coverage-before.v1')
for name in ['prepare-v15-owner-guard.py','v15-owner-guard-custody.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('v15-owner-guard-before.v1'),support/'v15-owner-guard-before.v1')
for name in ['prepare-v16-owner-guard.py','v16-owner-guard-custody.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('v16-owner-guard-before.v1'),support/'v16-owner-guard-before.v1')
for name in ['prepare-blind-assessment-binding.v1.py','blind-assessment-binding.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('blind-assessment-binding-before.v1'),support/'blind-assessment-binding-before.v1')
for name in ['d9-obligation-preparation.v1.json','d9-support-preparation.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['d9-obligation-before.v1','d9-support-before.v1','d9-obligation-evidence']:
 shutil.copytree(Path(__file__).with_name(name),support/name)
shutil.copyfile(Path(__file__).with_name('reference-budget-preparation.v21.json'),support/'reference-budget-preparation.v21.json')
for name in ['dynamic-reference-budget.preparation.v1.json','dynamic-reference-budget.patch','successor-guide-variants.preparation.v1.json','assemble-records.successor.v1.py.guide-variants.patch','verify-applied.py.guide-variants.patch']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('reference-budget-before.v21'),support/'reference-budget-before.v21')
for name in ['prepare-v21-owner-account.py','v21-owner-account-custody.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('v21-owner-account-before.v1'),support/'v21-owner-account-before.v1')
for name in ['application_rows.py','application_pins.py','run-application-reference-suites.py','assemble-records.successor.v1.py','apply-advisory-records.successor.v1.py','bind-review-receipts.v1.py','review_envelope.py','coverage_contract.py','retain_public.py','launch-application-review.successor.v1.py','retain-application-review.successor.v1.py','check-retain-public.v1.py']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['bind-review-receipts.before-root-design-guard.v1.py','check-root-design-assent.v1.py','root-design-assent-guard.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
finalizer=files/(dc+'finalize-application.v1.py')
selftest=subprocess.run([py,'-I','-B',str(support/'check-finalizer.py'),'--source',str(finalizer),'--report',str(support/'finalizer-selftest.v1.json')],capture_output=True,text=True)
(support/'finalizer-selftest.log').write_text(selftest.stdout+selftest.stderr)
assert selftest.returncode==0,selftest.stderr
selftest_result=json.loads((support/'finalizer-selftest.v1.json').read_text())
assert selftest_result['failed']==[] and selftest_result['actualApplicationPerformed'] is False
assert selftest_result['sourceSha256']==sha(finalizer)
save('staged-reference-checks.v1.json',{'scratchRoot':str(scratch),'commands':results,'acceptedDesignFileCount':len(manifest['files']),'implementationQualification':False})
