from pathlib import Path
import json,hashlib
BASE=Path(__file__).resolve().parent.parent
S=json.loads((BASE/'selection.json').read_text());assert S['sourceDirectory']=='apps/launch/' and S['logicalExecutable']=='opensip-launch' and S['releaseAssociation']=='host own signed release closure'
for k in ['componentRoleAdded','closureKindAdded','commandAdded','wireAdded','loaderMemberListAdded','productWorkspaceChanged','productInventoryChanged','launcherImplemented','platformQualified','effectiveL','productQualification']:assert S[k] is False
C=json.loads((BASE/'evidence/cases.json').read_text());out=[]
for c in C['cases']:
 state={k:True for k in C['fields']}
 for k in c['changed']:state[k]=False
 fate='checklist-satisfied' if all(state.values()) else 'duty-open'
 assert fate==c['expected'];out.append(dict(id=c['id'],fate=fate))
P=json.loads((BASE/'evidence/passages.json').read_text());assert len(P)==5
assert sum(p['parent']['path'].endswith('14-repository-and-module-layout.md') for p in P)==1
for p in P:
 if 'readiness-register' in p['parent']['path']:
  before=p['before'].split('|');after=p['after'].split('|');assert len(before)==len(after)==10
  for i in range(10):
   if i!=4:assert before[i]==after[i]
  assert before[4].strip() in after[4] and after[-2].strip()=='OPEN'
 if 'implementation-boundaries' in p['parent']['path']:assert p['before'].replace('`tools/README.md`','`tools/README.md`, `apps/launch/` (SD-3 host-closure launcher)')==p['after']
print(json.dumps(dict(passed=True,syntheticCases=out,passages=5,gateStandingAndBarsUnchanged=True,productImplemented=False,platformQualified=False),indent=2))
