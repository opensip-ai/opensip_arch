"""Assess actual proposed Markdown links against existing historical failures.
The sole absent future target allowed is the reviewed activation output.
"""
from pathlib import Path
import argparse, importlib.util, json, shutil, urllib.parse
p=argparse.ArgumentParser()
for name in ('root','stage'):p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();files=stage/'files';support=stage/'support'
spec=importlib.util.spec_from_file_location('links',Path(__file__).with_name('check-links.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
paths=sorted(str(p.relative_to(files)) for p in files.rglob('*.md'))
before=m.check(root,None,[p for p in paths if (root/p).is_file()]);after=m.check(root,files,paths)
key=lambda x:(x['from'],x['target'],x['reason'])
old={key(x) for x in before['failures']};inherited=[];generated=[];new=[]
activation='docs/coop/design-corrections/application-activation.v1.json'
finalizer=files/'docs/coop/design-corrections/finalize-application.v1.py'
assert finalizer.is_file() and activation in finalizer.read_text()
for row in after['failures']:
    path,_,fragment=row['target'].partition('#')
    dest=((root/row['from']).parent/urllib.parse.unquote(path)).resolve()
    if row['reason']=='missing path' and dest==root/activation and not fragment:
        generated.append(dict(row,disposition='Exact deterministic activation target written LAST by the reviewed finalizer after actual application ACCEPT; not claimed as existing evidence.'))
    elif key(row) in old:inherited.append(row)
    else:new.append(row)
support.mkdir(exist_ok=True)
result={'standing':'Exact staged current Markdown local-link assessment; inherited failures are preserved, not reported as passing.', 'paths':paths,'before':before,'after':after,'inheritedFailures':inherited,'futureGeneratedActivationLinks':generated,'unexplainedFailures':new}
(support/'application-link-assessment.v1.json').write_text(json.dumps(result,indent=2)+'\n')
for name in ['check-links.py','assess-links.py']:
    shutil.copyfile(Path(__file__).with_name(name),support/name)
print(json.dumps({'checked':after['checked'],'inheritedFailures':len(inherited),'futureActivationLinks':len(generated),'unexplainedFailures':len(new)}))
raise SystemExit(bool(new))
