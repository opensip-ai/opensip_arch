"""Source-pinned current evaluator reference checks, separate from profile2 history.

The frozen review manifest authenticates this launcher and its input pins.
These synthetic controls establish reference behavior, not product qualification.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
DC=HERE.parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
ledger=json.loads((HERE/'evaluator3-source-pins.v1.json').read_text())
invalid=[r['path'] for r in ledger['files'] if not (ROOT/r['path']).is_file() or hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']]
rows=[]
if not invalid:
    jobs=[('current-profile','foundation/check-current-profile.v3.py',[]),
          ('enumeration','foundation/check-enumeration.v1.py',['--receipt',str(a.out/'enumeration.receipt.json'),'--stdout']),
          ('atoms','foundation/check-atoms.v1.py',[]),
          ('execution-inputs','foundation/check-execution-inputs.v1.py',[]),
          ('composition','foundation/check-composition.v3.py',[]),
          ('full-replay','foundation/check-replay.v3.py',[]),
          ('native-replay','foundation/check-semantic-replay.v3.py',[]),
          ('execution-replay','foundation/check-execution-replay.v3.py',[]),
          ('candidate-replay','foundation/check-candidate-replay.v3.py',[]),
          ('policy-derivation','foundation/check-policy-derivation.v3.py',[]),
          ('faults','foundation/check-evaluator-faults.v3.py',[]),
          ('provider-attribution-return','foundation/check-provider-attribution-return.v2.py',[]),
          ('workflow-projection','workflows/check-workflow-projection.v3.py',[]),
          ('query-projection','workflows/check-query-projection.v3.py',['--report',str(a.out/'query-projection.receipt.json')]),
          ('comparison-knowledge','workflows/check-comparison-knowledge.v3.py',[]),
          ('analysis-seal','security/check-analysis-seal-adapter.v1.py',[])]
    for name,script,args in jobs:
        command=[sys.executable,'-I','-B',str(DC/script)]+args
        try:
            proc=subprocess.run(command,capture_output=True,text=True,timeout=600)
            code,stdout,stderr,timed=proc.returncode,proc.stdout,proc.stderr,False
        except subprocess.TimeoutExpired as exc:
            decode=lambda v: v.decode('utf-8','replace') if isinstance(v,bytes) else v or ''
            code,stdout,stderr,timed=None,decode(exc.stdout),decode(exc.stderr),True
        (a.out/(name+'.stdout')).write_text(stdout)
        (a.out/(name+'.stderr')).write_text(stderr)
        rows.append({'name':name,'command':command,'exitCode':code,'timedOut':timed,
                     'stdoutSha256':hashlib.sha256(stdout.encode()).hexdigest(),
                     'stderrSha256':hashlib.sha256(stderr.encode()).hexdigest()})
        print(name,code,'timeout' if timed else '',flush=True)
report={'standing':'source-pinned reference evidence, not independent acceptance or product qualification',
        'sourcePinsValid':not invalid,'changedOrMissing':invalid,'checks':rows,
        'passed':not invalid and bool(rows) and all(r['exitCode']==0 and not r['timedOut'] for r in rows),
        'productQualification':False}
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(not report['passed'])
