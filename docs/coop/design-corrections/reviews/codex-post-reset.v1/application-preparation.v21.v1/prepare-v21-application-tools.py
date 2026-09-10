"""Prepare guarded future21 application tooling; does not assemble or apply records."""
from pathlib import Path
import ast,hashlib,json,shutil
b=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=(b/'apply-v20-advisory-records.py').read_text().replace('v20','v21').replace('V20','V21')
s=s.replace("'prepare-v21-advisory-updater.v1.json'","'prepare-v20-advisory-updater.v1.json','apply-v20-advisory-records.py','prepare-v21-advisory-updater.v1.json'")
p=b/'apply-v21-advisory-records.py';assert not p.exists();ast.parse(s);p.write_text(s)
(b/'prepare-v21-advisory-updater.v1.json').write_text(json.dumps({'standing':'Prepared only for actual accepted21+NEWblind9 after guarded assembly. Not executed; no staged grades or activation.','source':{'path':'apply-v20-advisory-records.py','sha256':sha(b/'apply-v20-advisory-records.py')},'prepared':{'path':p.name,'sha256':sha(p)}},indent=2)+'\n')
p=b/'run-applied-reference-checks.py';before=b/'reference-budget-before.v21';before.mkdir();shutil.copyfile(p,before/p.name)
s=p.read_text();assert s.count('timeout=180')==1
s=s.replace(' r=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=180);',' outer_timeout=3600 if name==\'foundation\' else 600\n r=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=outer_timeout);')
s=s.replace("'exitCode':r.returncode,'log'", "'exitCode':r.returncode,'outerTimeoutSeconds':outer_timeout,'log'")
ast.parse(s);p.write_text(s)
q=b/'prepare-validation.py';shutil.copyfile(q,before/q.name);s=q.read_text();anchor="finalizer=files/(dc+'finalize-application.v1.py')";assert s.count(anchor)==1
s=s.replace(anchor,"shutil.copyfile(Path(__file__).with_name('reference-budget-preparation.v21.json'),support/'reference-budget-preparation.v21.json')\nshutil.copytree(Path(__file__).with_name('reference-budget-before.v21'),support/'reference-budget-before.v21')\n"+anchor);ast.parse(s);q.write_text(s)
(b/'reference-budget-preparation.v21.json').write_text(json.dumps({'standing':'Prepared application orchestration only; source21foundation inner600perchild requires an outer budget with room for allfivechildbudgets. Actual postapplication runner uses3600foundation/600other. No product law, no application or behavioral test claimed; full independent application review still required.','files':[{'path':x.name,'beforeSha256':sha(before/x.name),'afterSha256':sha(x)} for x in [p,q]],'syntaxParsed':True,'actualApplicationExecuted':False},indent=2)+'\n')
print('Prepared guarded21advisory updater and application orchestration budget/support custody; no application performed')
