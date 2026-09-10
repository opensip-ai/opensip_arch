"""Verify the reviewed source inventory before executing its reference checks.
The review snapshot authenticates this launcher and its pin manifest externally.
This is not a hostile-host or self-authentication mechanism.

A child that does not finish within CHILD_TIMEOUT_SECONDS is a FAILED reference run and is
reported as one. Before this was handled, `subprocess.TimeoutExpired` propagated out of the loop
and past the write below, so the launcher exited 1 on the traceback while the PREVIOUS run's
report - `passed: true` - was still the file on disk. An unchanged report is not this run's
result. A timeout now produces a report of the SAME shape with the SAME five entries, `timedOut`
true on the entry that ran out of budget, `exitCode` null because none was observed, and
`reportSha256` null because a run that did not finish cannot claim the child report it did not
write. `passed` is false. The budget is a fixed constant, not a flag or an environment variable:
a caller must not be able to widen or narrow the bound that decides whether a run counts. The
pin sweep above still runs to completion before any child starts, unchanged.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
# Bound per child, not for the suite: the suite is bounded by 5*CHILD_TIMEOUT_SECONDS. The slowest
# child (check-identity.py) runs ~120s, close enough to the former 120s bound that ordinary host
# variation decided the outcome; 600s is ~5x that observed cost and still refuses a real hang.
CHILD_TIMEOUT_SECONDS=5  # SYNTHETIC INJECTION ONLY - forces check-identity.py to exceed its budget
p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--report-dir');a=p.parse_args()
OUT=Path(a.report_dir) if a.report_dir else H
OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((H/'source-pins.v1.json').read_text());failures=[]
for item in manifest['files']:
    path=ROOT/item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:failures.append(item['path'])
if failures:
    result={'sourcePinsValid':False,'changedOrMissing':failures,'checksExecuted':False,'productQualification':False}
else:
    checks=[]
    # TimeoutExpired carries BYTES on .stdout/.stderr even under text=True, so decoding is not
    # cosmetic: writing them raw would raise TypeError from json.dumps and skip the write again.
    text=lambda s:'' if s is None else s if isinstance(s,str) else s.decode('utf-8','replace')
    for script,report in [('check-foundation.py','foundation-report.json'),('check-identity.py','identity-report.json'),('check-product-quality.py','product-quality-report.json'),('check-product-configuration.py','product-configuration-report.json'),('check-array-orders.py','array-order-report.json')]:
        try:
            run=subprocess.run([sys.executable,'-I','-B',str(H/script),'--report',str(OUT/report)],capture_output=True,text=True,timeout=CHILD_TIMEOUT_SECONDS)
            code,out,err,timed=run.returncode,run.stdout,run.stderr,False
            sha=hashlib.sha256((OUT/report).read_bytes()).hexdigest() if (OUT/report).exists() else None
        except subprocess.TimeoutExpired as exc:
            code,out,err,timed,sha=None,text(exc.stdout),text(exc.stderr)+'\nTIMEOUT: no result after '+str(CHILD_TIMEOUT_SECONDS)+'s\n',True,None
        checks.append({'script':script,'exitCode':code,'stdout':out,'stderr':err,'reportSha256':sha,'timedOut':timed})
    result={'sourcePinsValid':True,'sourceFileCount':len(manifest['files']),'checksExecuted':True,'checks':checks,'passed':all(v['exitCode']==0 and not v['timedOut'] for v in checks),'timedOut':[v['script'] for v in checks if v['timedOut']],'childTimeoutSeconds':CHILD_TIMEOUT_SECONDS,'productQualification':False}
Path(a.report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'}));sys.exit(not result.get('passed',False))
