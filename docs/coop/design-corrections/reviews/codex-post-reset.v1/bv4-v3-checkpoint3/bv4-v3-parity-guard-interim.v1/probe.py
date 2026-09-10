"""Compare inherited versus active missing-required-field behavior; pure renderer reference only."""
from pathlib import Path
import json,hashlib,importlib.util,shutil
task=Path('/tmp/opensip-design-corrections');b=task/'bv4-corrections-author.v3/work';dc=b/'docs/coop/design-corrections';out=task/'bv4-v3-parity-guard-interim.v1';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths={'activeModel':dc/'workflows/workflows_model.v1.py','activeInventory':dc/'workflows/command-inventory.v1.json','inheritedModel':task/'candidate-subject.v13/docs/coop/design-corrections/workflows/workflows_model.v1.py'}
sources={}
for name,p in paths.items():
 q=out/(name+p.suffix);shutil.copy2(p,q);sources[name]={'path':str(p),'captured':q.name,'sha256':sha(q)}
cmd=next(c for c in json.loads(paths['activeInventory'].read_text())['commands'] if c['name']=='default')
models={}
for name in ('activeModel','inheritedModel'):
 s=importlib.util.spec_from_file_location(name,paths[name]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);models[name]=m
rows=[]
for absent in ('required-coverage','capability-availability'):
 parity={k:'synthetic-'+k for k in cmd['parityFields']};parity['findings']=[];assert absent in parity;del parity[absent]
 for name,m in models.items():
  try:
   value=m.render({'parity':parity,'envelope':{}},'json',cmd);rows.append({'missing':absent,'model':name,'outcome':'RETURNED','missingFromReturnedParity':absent not in value['parity']})
  except Exception as e:rows.append({'missing':absent,'model':name,'outcome':'REFUSE','exception':type(e).__name__,'error':str(e)})
for name,p in paths.items():assert sha(p)==sources[name]['sha256'],'Source changed during diagnostic'
r={'standing':'Interim pure field-projection reference comparison, synthetic unrelated field values. No real host exception conversion, full output-schema admission, renderer implementation or final-source assent claimed. Existing normative workflow8 says missing declared projection field is a required-delivery fault, not a partial success.','sources':sources,'cases':rows,'observation':'The newly added if-k-in-parity filter silently drops missing REQUIRED declared fields for JSON (including inherited required-coverage). The inherited direct lookup refused. Restore strict required-field behavior; initialize the new field explicitly from the selected empty/no-selection law rather than broadening all renderers to silently omit it.'}
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copy2(__file__,out/'probe.py');print(json.dumps(rows,indent=2))
