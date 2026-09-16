from pathlib import Path
import json,importlib.util,sys,hashlib
p=Path('/tmp/opensip-design-corrections/dependency-totality-successor.v1/source/docs/coop/design-corrections/foundation/check-atoms.v1.py');s=importlib.util.spec_from_file_location('K',p);K=importlib.util.module_from_spec(s);sys.modules['K']=K;s.loader.exec_module(K)
r={}
for label,partitions in [('merged',[[K.F_SYM,K.G_SYM]]),('split',[[K.F_SYM],[K.G_SYM]])]:
 i=K.totality_inputs(partitions,[([K.F_SYM],'2','unknown-carrier')]);v=K.AM.evaluate_atom({**K.REACH_ALL,'endpoint':'target'},K.F_SUBJ,i);r[label]={k:v[k] for k in ['value','causes','nativeDeficiencies','coverageIds']}
d={'standing':'Actual101author bytes, synthetic atom API only. Existing per-view carrier law means semantic unknown is invariant but cause record sets may differ under partition regrouping. No consumer material.','checkerSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cases':r,'sameValue':r['merged']['value']==r['split']['value'],'sameCauseSet':r['merged']['causes']==r['split']['causes']};(Path(__file__).parent/'probe.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2));assert d['sameValue'] and not d['sameCauseSet']
