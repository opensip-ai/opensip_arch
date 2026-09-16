from pathlib import Path
import importlib.util,sys,json,copy,hashlib
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v35/docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
K=load('k35',F/'check-atoms.v1.py'); A=K.AM
out={}
for mode in ['none','f-only','both','g-only']:
 i=K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'),inventories=[K.inv_symbol(),K.inv_symbol(nid=K.G_SYM,qn='g')])
 K.install_pair(i,*K.paired('reachability','from-resolved-calls',K.U1,K.U1,[K.F_SYM,K.G_SYM],tag='1'))
 if mode in ['f-only','both']:K.install_pair(i,*K.paired('calls','resolved-callee',K.U1,K.U1,[K.F_SYM],tag='2'))
 if mode in ['g-only','both']:K.install_pair(i,*K.paired('calls','resolved-callee',K.U1,K.U1,[K.G_SYM],tag='4'))
 out[mode]={}
 for ep in ['target','source']:
  for op in ['none','all-covered']:
   r=A.evaluate_atom({'op':op,'relation':'reachability','minResolution':'from-resolved-calls','endpoint':ep,'filters':[]},K.F_SUBJ,copy.deepcopy(i))
   out[mode][ep+'/'+op]={k:r[k] for k in ['value','coverageIds','causes','nativeDeficiencies']}
p=Path(__file__).parent/'probe.json';p.write_text(json.dumps({'standing':'Source35 synthetic atom API only. Per-symbol dependency totality decision under independent assessment; no Run reachability asserted.','modelSha256':hashlib.sha256((F/'atom_model.v1.py').read_bytes()).hexdigest(),'cases':out},indent=2)+'\n')
for m,r in out.items():print(m,{k:v['value'] for k,v in r.items()})
