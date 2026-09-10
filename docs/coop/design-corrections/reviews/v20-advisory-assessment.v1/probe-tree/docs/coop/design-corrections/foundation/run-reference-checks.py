"""Verify the reviewed source inventory before executing its reference checks.
The review snapshot authenticates this launcher and its pin manifest externally.
This is not a hostile-host or self-authentication mechanism.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
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
    for script,report in [('check-foundation.py','foundation-report.json'),('check-identity.py','identity-report.json'),('check-product-quality.py','product-quality-report.json'),('check-product-configuration.py','product-configuration-report.json'),('check-array-orders.py','array-order-report.json')]:
        run=subprocess.run([sys.executable,'-I','-B',str(H/script),'--report',str(OUT/report)],capture_output=True,text=True,timeout=120)
        checks.append({'script':script,'exitCode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'reportSha256':hashlib.sha256((OUT/report).read_bytes()).hexdigest() if (OUT/report).exists() else None})
    result={'sourcePinsValid':True,'sourceFileCount':len(manifest['files']),'checksExecuted':True,'checks':checks,'passed':all(v['exitCode']==0 for v in checks),'productQualification':False}
Path(a.report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'}));sys.exit(not result.get('passed',False))
