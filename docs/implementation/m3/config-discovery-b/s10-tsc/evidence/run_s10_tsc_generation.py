# S10-TSC generation: the B-S10 runner, paths and standing changed only.
from pathlib import Path
from types import SimpleNamespace
import os,json,hashlib,importlib.util,subprocess,tempfile,time
W=Path('/Users/sb/code/opensip-ai/opensip-s10tsc');D=Path('/tmp/opensip-implementation/s10-tsc');O=D/'generation-r1';os.setpriority(os.PRIO_PROCESS,0,10)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
closure=json.loads((W/'tools/contracts/generator-closure.json').read_text());registry=json.loads((W/'schemas/registry.json').read_text());recipe=registry['recipes'][0]
assert recipe['generatorClosureSha256']==pin(W/'tools/contracts/generator-closure.json')['sha256'];assert set(recipe['sourceSha256s'])=={r['sourceSha256'] for r in registry['sources']}
for row in closure['files']:assert pin(W/row['path'])=={k:row[k] for k in ['bytes','sha256']},row['path']
# r2 (Codex B-S10-R1-RF-01): the standard recipe admission (tools/contracts/admission.py registry(), which generate_contracts.py runs
# first) must pass on the candidate before generation, so a stale recipe options/closure/source pin cannot be bypassed.
adm=load(W/'tools/contracts/admission.py','candidate_admission');_reg,_src,_recipes,_regsha=adm.registry(W);assert len(_recipes)==1 and _recipes[0][0]['optionsSha256']==pin(W/'tools/contracts/options.json')['sha256']
pipeline=load(W/'tools/contracts/pipeline.py','candidate_pipeline');args=SimpleNamespace(root=W,output=O,node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
# The native renderer is the existing exact selected 3.14.6 child image, not
# an alias substituted into its pinned runtime. Lead Python remains prescribed.
assert "'HOME':" not in (W/'tools/contracts/pipeline.py').read_text()
result=pipeline.run(args,selected_closure=closure['files'],provenance=dict(registrySha256=pin(W/'schemas/registry.json')['sha256'],generatorClosureSha256=recipe['generatorClosureSha256']))
root=O/result['outputRoot'];changed=[]
for row in result['outputs']:
 p=W/row['path'];raw=(root/row['path']).read_bytes();assert pin(root/row['path'])=={k:row[k] for k in ['bytes','sha256']}
 if p.read_bytes()!=raw:
  changed.append(dict(path=row['path'],before=pin(p),after=pin(root/row['path'])));p.write_bytes(raw)
(D/'generation-summary.json').write_text(json.dumps(dict(passed=result['passed'],result=result,changed=changed,standing='UNREVIEWED S10-TSC DETAIL VOCABULARY GENERATION (M3-B r8 SUCCESSOR S10); NO RESOLVER SEMANTICS',standardRecipeAdmissionPassed=True,HOMEOverrideRemoved=True,allChildrenPriorityInherited=10,actualQualification=False),indent=2)+'\n')
print('Generation PASS;',len(changed),'existing outputs changed; no HOME override or production claim.')
