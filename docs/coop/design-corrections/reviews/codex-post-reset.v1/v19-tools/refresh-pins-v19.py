from pathlib import Path
import json,hashlib
root=Path.cwd(); r=root/'docs/coop/design-corrections'
# Actual cross-unit imports and schema registries. Exclude generated reports and other
# pin manifests: they are review artifacts, never reference-model decision inputs.
shared=[]
for base in ['foundation','workflows','security','native']:
 for p in (r/base).rglob('*'):
  if not p.is_file() or '__pycache__' in p.parts:continue
  if p.suffix=='.py' or (p.suffix=='.json' and ('schema' in p.name or p.name in ('workflow-cases.v1.json','command-inventory.v1.json','native-capability-matrix.v2.json','capability-manifest-domains.v2.json','native-cases.v2.json'))):shared.append(p)
# Shared runtime reads and retained clone/CVE1 normative inputs, authenticated by every consuming suite.
shared += [root/'docs/coop/artifacts'/name for name in ('delivery.v4.json','fact-plane.v1.json','fact-identity-policy.v2.json','resolved-inputs.v2.json')]
shared += [r/'security/public-detail-cases.v1.json',r/'integration-fixtures.py',r/'integration-host-model.py',r/'discovery-defaults.py',r/'public-detail-registry.v1.json']
# Explicit newly published runtime normative tables, bound by the final source assessment.
a=json.loads((r/'reviews/codex-post-reset.v1/successor-source-assessment.v19.json').read_text())
assert a['finalSourceAssent'] is True
for row in a['normativeInputAdditions']:
 p=root/row['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 shared.append(p)
for unit,key,name in [('foundation','files','source-pins.v1.json'),('security','pins','source-pins.v1.json'),('native','pins','source-pins.v2.json'),('workflows','files','source-pins.v1.json')]:
 p=r/unit/name;d=json.loads(p.read_text());rows={v['path']:v for v in d[key] if not v['path'].endswith('native-fix-handoff.v3.md')}
 for extra in shared:
  rel=str(extra.relative_to(root));rows.setdefault(rel,{'path':rel})
 for row in rows.values():
  raw=(root/row['path']).read_bytes();row['sha256']=hashlib.sha256(raw).hexdigest()
  if 'bytes' in row:row['bytes']=len(raw)
 d[key]=sorted(rows.values(),key=lambda v:v['path']);p.write_text(json.dumps(d,indent=2)+'\n');print(unit,len(rows))
