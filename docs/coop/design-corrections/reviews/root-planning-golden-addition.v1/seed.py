"""Seed exactly one root-reviewed planning responsibility before the guarded planning rebind.
Execute only after the completed author's new golden is integrated; never removes the population guard.
"""
from pathlib import Path
import json,hashlib,copy,argparse
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args();S=a.source.resolve();O=a.evidence.resolve();assert not O.exists();O.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
digest=lambda x:sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
I=S/'docs/coop/design-corrections/workflows/command-inventory.v3.json';g=json.loads(I.read_bytes())['goldens'];at=next(i for i,x in enumerate(g) if x['id']=='policy-test-suite-inadmissible');row=g[at]
assert digest(row)=='7a2241c6cff1d1a75bec70de5c8eb84db46012e0a457734b2e9098f223be6b51','Golden changed; requires actual reassessment'
p=S/'docs/v2/architecture/implementation-coverage.v1.json';d=json.loads(p.read_bytes());assert sum(map(len,d['groups'].values()))==320
rows=d['groups']['workflowGoldens'];assert len(rows)==43 and all(x['id']!=row['id'] for x in rows)
template=next(x for x in rows if x['id']=='policy-test-imperative-key');assert template['owners']==['crates/host/src/policy.rs'] and template['milestone']=='M5' and template['verification']['owner']=='crates/host/tests/workflow_tests.rs' and template['verification']['standing']=='not-executed'
n=copy.deepcopy(template);n['id']=row['id'];n['source']={'key':'commands','selector':f'/goldens/{at}','valueSha256':digest(row)};n['reviewIssues']=[];rows.insert(next(i for i,x in enumerate(rows) if x['id']==template['id'])+1,n)
assert len(rows)==44 and sum(map(len,d['groups'].values()))==321
changes={p:(json.dumps(d,indent=2)+'\n').encode()}
for rel,pairs in [
 ('docs/v2/architecture/14-repository-and-module-layout.md',[('3. Check all 320 ownership mappings','3. Check all 321 ownership mappings')]),
 ('docs/v2/architecture/implementation-boundaries-and-build-plan.md',[
 ('The current inventory has 198 proposed files in 20 groups, 320 source-bound','The current inventory has 198 proposed files in 20 groups, 321 source-bound'),
 ('- Check all 320 mapping entries against the final accepted source populations','- Check all 321 mapping entries against the final accepted source populations')])]:
 q=S/rel;t=q.read_text()
 for old,new in pairs:assert t.count(old)==1,(rel,old);t=t.replace(old,new)
 changes[q]=t.encode()
report=[]
for q,b in changes.items():
 old=q.read_bytes();backup=O/'before'/q.relative_to(S);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old);q.write_bytes(b);report.append({'path':str(q.relative_to(S)),'beforeSha256':sha(old),'sha256':sha(b),'bytes':len(b)})
(O/'decision.json').write_text(json.dumps({'standing':'Root explicit ownership review and seed for one added existing-command refusal golden; author planning only, fresh final independent review pending','golden':row,'goldenValueSha256':digest(row),'mapping':n,'basis':'Residual invalid-suite admission uses existing policy-test command, CONFIG.INVALID error/detail and M5 host policy owner; adjacent two policy-test refusal goldens use these same owners. Existing workflow_tests responsibility exercises complete typed output/termination/exit. No new crate or module needed. This single new exact public case needs its own source-bound planned row.','mappingCount':321,'goldens':44,'unaffected':'198 files,20packages,32product gates,54recovery cases; every product case/gate remains unperformed','historical320CountsPreserved':True,'next':'Rebind five normative pin ledgers and then planning layer7; generated tables/source hashes remain pending until that rebind','files':report},indent=2)+'\n')
print('Seeded one reviewed planned row:321 mappings,44 goldens. Requires normal pin/planning rebind.')
