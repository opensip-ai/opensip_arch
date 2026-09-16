"""Prepare an application-only v16 updater, preserving all earlier preparation evidence."""
from pathlib import Path
import hashlib,json,shutil
b=Path(__file__).parent;src=b/'apply-v15-advisory-records.py';dest=b/'apply-v16-advisory-records.py'
assert not dest.exists();before=b/'apply-v15-advisory-records.before-v16.py';assert not before.exists();shutil.copyfile(src,before)
s=src.read_text().replace('v15','v16').replace('V15','V16')
# Earlier support preparation retains its actual historical filename and bytes.
start=s.index("for name in ['v14-advisory-preparation.v1.json'")
end=s.index("\n shutil.copyfile(Path(__file__).with_name(name),support/name)",start)
s=s[:start]+"for name in ['v14-advisory-preparation.v1.json','v15-advisory-preparation.v1.json','prepare-v15-advisory-updater.py','apply-v14-advisory-records.py','apply-v15-advisory-records.before-support-custody.py','prepare-v15-support-custody.py','v15-support-custody-preparation.v1.json','apply-v15-advisory-records.before-v16.py','prepare-v16-advisory-updater.py','v16-advisory-preparation.v1.json']:"+s[end:]
dest.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(b/'v16-advisory-preparation.v1.json').write_text(json.dumps({'standing':'Prepared v16 application summary routing only. No application stage assembled, no design/blind acceptance or activation inferred. Updater requires actual accepted frozen v16 plus a fresh accepted blind review and exact measured report equality.','source':{'path':src.name,'sha256':sha(src)},'beforeImage':{'path':before.name,'sha256':sha(before)},'prepared':{'path':dest.name,'sha256':sha(dest)},'earlierEvidencePreserved':True},indent=2)+'\n')
print('Prepared v16 application advisory updater; not executed.')
