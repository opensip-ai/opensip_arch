"""Synthetic root timeout reproduction against exact prospective source; never an accepted suite run."""
from pathlib import Path
import json,hashlib,shutil,subprocess,datetime,time
base=Path('/tmp/opensip-design-corrections');snapshot=base/'candidate-subject.v20';overlay=base/'reference-hardening-final-peer.v1/proposed'
out=base/'codex-post-reset.v1/final-wrapper-timeout.v1';out.mkdir(exist_ok=False);copy=out/'work';copy.mkdir()
dc='docs/coop/design-corrections/';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger_rel=dc+'foundation/source-pins.v1.json';ledger=json.loads((snapshot/ledger_rel).read_text())
paths={x['path'] for x in ledger['files']}|{ledger_rel}
paths|={dc+'foundation/'+x for x in ('validation-report.json','foundation-report.json','identity-report.json','product-quality-report.json','product-configuration-report.json','array-order-report.json')}
for rel in sorted(paths):
 q=copy/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(snapshot/rel,q)
selected=[dc+'foundation/run-reference-checks.py',dc+'foundation/check-identity.py',dc+'workflows/workflows_model.v1.py']
source=[]
for rel in selected:
 q=overlay/rel;assert q.is_file();shutil.copyfile(q,copy/rel);source.append({'path':rel,'prospectiveSha256':sha(q)})
wrapper=copy/selected[0];text=wrapper.read_text();assert text.count('CHILD_TIMEOUT_SECONDS=600')==1
wrapper.write_text(text.replace('CHILD_TIMEOUT_SECONDS=600','CHILD_TIMEOUT_SECONDS=5  # ROOT SYNTHETIC FAILURE-PATH INJECTION ONLY'))
for x in ledger['files']:
 if x['path'] in selected:x['sha256']=sha(copy/x['path'])
ledger['standing']='ROOT SYNTHETIC VALIDATION COPY; three selected proposal inputs locally repinned, wrapper budget forced to5s; not frozen/accepted-source reproduction.'
(copy/ledger_rel).write_text(json.dumps(ledger,indent=2)+'\n')
assert all(sha(copy/x['path'])==x['sha256'] for x in ledger['files'])
report=copy/(dc+'foundation/validation-report.json');before=sha(report);assert json.loads(report.read_text())['passed'] is True
old_child=sha(copy/(dc+'foundation/identity-report.json'))
cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(wrapper),'--report',str(report)]
started=time.monotonic();r=subprocess.run(cmd,cwd=copy,capture_output=True,text=True,timeout=60);elapsed=time.monotonic()-started
(out/'stdout.txt').write_text(r.stdout);(out/'stderr.txt').write_text(r.stderr)
v=json.loads(report.read_text());assert r.returncode==1 and v['passed'] is False and v['sourcePinsValid'] is True
assert len(v['checks'])==5 and v['timedOut']==['check-identity.py'] and v['childTimeoutSeconds']==5
child=next(x for x in v['checks'] if x['script']=='check-identity.py')
assert child['exitCode'] is None and child['timedOut'] is True and child['reportSha256'] is None
assert 'TIMEOUT: no result after 5s' in child['stderr']
assert all(x['exitCode']==0 and x['timedOut'] is False for x in v['checks'] if x is not child)
assert sha(report)!=before and sha(copy/(dc+'foundation/identity-report.json'))==old_child
shutil.copyfile(report,out/'actual-failure-report.json');shutil.copyfile(wrapper,out/'synthetic-wrapper.py');shutil.copyfile(copy/ledger_rel,out/'synthetic-source-pins.json')
record={'standing':'Actual root synthetic timeout reproduction. Child budget deliberately changed600to5, copied inputs locally repinned. Expected failing wrapper exit1 observed; NOT a completed identity/foundation suite or product qualification.',
 'prospectiveSource':source,'command':cmd,'exitCode':r.returncode,'elapsedSeconds':elapsed,'aggregateReportBeforeSha256':before,'aggregateReportAfterSha256':sha(report),
 'staleChildReportStillPresentSha256':old_child,'timedOutEntryDeclinesChildReport':True,'allFiveEntriesPresent':True,'otherFourChildrenCompleted':True,
 'failureReport':{'path':'actual-failure-report.json','sha256':sha(out/'actual-failure-report.json')},'syntheticWrapperSha256':sha(out/'synthetic-wrapper.py'),
 'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'root-result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
