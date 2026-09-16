from pathlib import Path
import sys,json,hashlib,contextlib,time
O=Path(__file__).parent
S=Path('/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1/work/source')
f=S/'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
files=[f,S/'docs/coop/design-corrections/workflows/workflows_model.v3.py',S/'docs/coop/design-corrections/workflows/workflows_model.v1.py']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p):sha(p) for p in files}
g={'__file__':str(f),'__name__':'__main__'};sys.argv=[str(f)];started=time.time()
with (O/'checker-stdout.json').open('w') as out, (O/'checker-stderr.txt').open('w') as err, contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
 try:exec(compile(f.read_bytes(),str(f),'exec'),g)
 except SystemExit as exc:checker_exit=exc.code
assert checker_exit==0,checker_exit
W=g['WF3'];adapter=g['_oc1_adapter'];calls=[]
def call(label,a):
 try:
  p=W.repair_preview(g['CW_PROJECT'],g['CW_TREE'],a,g['CW_RECIPE'],g['CW_FPS'][:1],g['CW_DELETE'],g['CW_REQS'],['**'],g['CW_TRUST'])
  row={'label':label,'outcome':'ADMIT','repairPlanId':p['repairPlanId'],'descriptor':p['descriptor']}
 except Exception as exc:row={'label':label,'outcome':'REFUSE','class':type(exc).__name__,'errorCode':getattr(exc,'error_code',None),'detail':getattr(exc,'detail',None),'message':str(exc)}
 calls.append(row)
call('lawful',adapter)
wrong=dict(adapter,runId='run3:'+'a'*64)
assert wrong['runId']!=adapter['runId']
call('same-retained-closure-and-plan-but-wrong-run-id',wrong)
retained=adapter['retained'];saved=retained.matched_findings
class RetainedEvidenceUnavailable(Exception):pass
def foreign():raise RetainedEvidenceUnavailable('foreign host defect')
retained.matched_findings=foreign
try:call('foreign-same-name-host-exception',adapter)
finally:retained.matched_findings=saved
report={'standing':'Root bounded current author-owner probe; actual admitted fixture from exact checker. No product or final-source acceptance. No consumer artifacts or repair.', 'source':str(S),'before':before,'after':{str(p):sha(p) for p in files},'checkerExit':checker_exit,'seconds':time.time()-started,'actualRunId':adapter['runId'],'calls':calls}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['before']==report['after'],'author files changed during probe'
print([(r['label'],r['outcome'],r.get('errorCode'),r.get('detail')) for r in calls],flush=True)
