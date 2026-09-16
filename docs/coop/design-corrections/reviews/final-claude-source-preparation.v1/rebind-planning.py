"""Prepare a non-circular planning input layer after normative integration.
No acceptance, activation, implementation or product qualification.
"""
from pathlib import Path
import argparse,hashlib,json,importlib.util,shutil
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args()
T=a.source.resolve();O=a.evidence.resolve();assert not O.exists();O.mkdir(parents=True)
A=T/'docs/v2/architecture';C=A/'implementation-coverage.v1.json'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def save(p,raw):
 old=p.read_bytes() if p.exists() else None
 if old==raw:return
 if old is not None:
  q=O/'before'/p.relative_to(T);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def dump(d):return (json.dumps(d,indent=2)+'\n').encode()
d=json.loads(C.read_bytes());sources={};rows=[]
for k,r in d['sources'].items():
 raw=(T/r['path']).read_bytes();r['sha256']=sha(raw);r['bytes']=len(raw)
 if r.get('location')!='working-tree':rows.append({x:r[x] for x in ['path','sha256','bytes']})
 sources[k]=json.loads(raw) if r['path'].endswith('.json') else raw.decode()
# This manifest deliberately contains inputs only, excluding the planning records that pin it.
layer='docs/v2/architecture/implementation-normative-inputs.v1.json'
assert not (T/layer).exists(),'Do not rewrite a previously bound input layer; select a new version after changes.'
assert len({r['path'] for r in rows})==len(rows)
assert not any(r['path'].startswith('docs/v2/architecture/implementation-') for r in rows)
record={'standing':'Exact normative/reference inputs consumed by implementation planning; no acceptance or readiness. Planning records excluded to avoid a self-hash cycle. Final candidate manifest independently binds this input layer and all planning bytes.','files':sorted(rows,key=lambda r:r['path'])}
raw=dump(record);save(T/layer,raw);d['subjectManifest']=layer;d['subjectManifestSha256']=sha(raw)
spec=importlib.util.spec_from_file_location('planning_check',T/'docs/operations/check_implementation_planning.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
expected=m.expected_groups(sources)
assert set(expected)==set(d['groups'])
for group, mapping in expected.items():
 assert set(mapping)=={r['id'] for r in d['groups'][group]},'Changed population requires explicit ownership review: '+group
 for row in d['groups'][group]:
  key,selector,value=mapping[row['id']];row['source']={'key':key,'selector':selector,'valueSha256':m.digest(value)}
save(C,dump(d))
# Regenerate only owned blocks after all invariants pass; stale count guard must already be integrated.
m.validate_coverage(d,sources,json.loads((A/'repository-file-inventory.v1.json').read_bytes()))
r=json.loads((A/'commit-recovery-plan.v1.json').read_bytes());m.validate_recovery(r,json.loads((A/'repository-file-inventory.v1.json').read_bytes()),sources['securitySchema'])
plan=A/'implementation-boundaries-and-build-plan.md';text=plan.read_text();text=m.replace_section(text,'IMPLEMENTATION COVERAGE',m.render_coverage(d));text=m.replace_section(text,'COMMIT RECOVERY',m.render_recovery(r));save(plan,text.encode())
(O/'rebind.json').write_bytes(dump({'standing':'Planning source-layer binding only; final independent review pending','layer':layer,'sha256':sha(raw),'sourceCount':len(rows),'mappings':sum(map(len,d['groups'].values())),'failureCases':len(r['cases'])}))
print('Planning input layer and mappings rebound',len(rows))
