"""Prepare complete custody for prospective v15 application support; no stage assembled."""
from pathlib import Path
import json,hashlib,ast,shutil
b=Path(__file__).parent;p=b/'apply-v15-advisory-records.py';before=b/'apply-v15-advisory-records.before-support-custody.py';assert not before.exists();shutil.copy2(p,before)
s=p.read_text();needle="shutil.copyfile(__file__,support/Path(__file__).name)";assert s.count(needle)==1
s=s.replace(needle,needle+"\nfor name in ['v14-advisory-preparation.v1.json','v15-advisory-preparation.v1.json','prepare-v15-advisory-updater.py','apply-v14-advisory-records.py','apply-v15-advisory-records.before-support-custody.py','prepare-v15-support-custody.py','v15-support-custody-preparation.v1.json']:\n shutil.copyfile(Path(__file__).with_name(name),support/name)")
ast.parse(s);p.write_text(s);sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
(b/'v15-support-custody-preparation.v1.json').write_text(json.dumps({'standing':'Prepared metadata-custody addition only. No application assembly, validation, acceptance or activation executed. Prior v15 prepared updater preserved exactly.','target':p.name,'before':{'path':before.name,'sha256':sha(before)},'afterSha256':sha(p),'purpose':'Prospective application support retains earlier v14/v15 updater preparation accounts and source, plus this custody amendment; the separately reviewed application will capture the exact executed updater.'},indent=2)+'\n')
print('Prepared complete v15 updater support custody; no application assembled.')
