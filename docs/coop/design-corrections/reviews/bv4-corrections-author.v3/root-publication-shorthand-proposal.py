"""Root-owned editorial reconciliation of already selected coauthor publication laws, before final pins."""
from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((ev/'coauthor-assessment-bv4-v3.json').read_text());assert a['finalSourceAssent'] is True
out=ev/'publication-shorthand-v14';assert not out.exists()
changes=[]
p=root/'docs/v2/contracts/product-v1/native-evidence.md';text=p.read_text()
pairs=[('One\n  analysis step\'s selection becomes a `CapabilityAvailabilityStepV1`\n  (`release_absence_notices`), and the invocation\'s steps compose', 'One\n  analysis step\'s selection produces the `{noticeCount, notices[]}` leaf\n  (`release_absence_notices`); adding its `stepId` forms a\n  `CapabilityAvailabilityStepV1`, and the invocation\'s steps compose'),('declared parity field of the analysis commands (`default`, `analyze`, `fit`,\n  `audit`), so every applicable renderer carries it.', 'declared parity field of every `requestClass: analysis` command (`default`,\n  `analyze`, `fit`, `audit`, `repair-verify`), so every applicable renderer\n  carries it.')]
for old,new in pairs:assert text.count(old)==1;text=text.replace(old,new)
changes.append((p,text))
p=dc/'native/native-evidence.schemas.v2.json';text=p.read_text();old='its public route is the advisory native.capability-unavailable DomainDetail.';new='its public route is the advisory native.capability-unavailable notice in CommandEnvelope.availability, whose complete ownership tuple is defined in section 1.4.';assert text.count(old)==1;changes.append((p,text.replace(old,new)))
out.mkdir();rows=[]
for p,after in changes:
 rel=p.relative_to(root);before=sha(p);q=out/'before'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);p.write_text(after);q=out/'after'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);rows.append({'path':str(rel),'beforeSha256':before,'afterSha256':sha(p)})
(out/'account.json').write_text(json.dumps({'standing':'Root editorial corrections before final pinning. No behavioral law is added: workflow8 and actual command inventory already require all5analysis commands, native step schema already owns stepId, and the notice carrier already owns complete typed workspace attribution. Fresh independent review must cover these exact final bytes.','changes':rows,'coauthorAssentAppliesToEarlierBytes':True,'independentAcceptance':False},indent=2)+'\n')
print(json.dumps(rows,indent=2))
