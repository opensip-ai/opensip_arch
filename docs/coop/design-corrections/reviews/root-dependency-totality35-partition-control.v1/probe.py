from pathlib import Path
import importlib.util,sys,json,copy,hashlib
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v35/docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
K=load('k35',F/'check-atoms.v1.py'); A=K.AM
out={}
for grouped in [True,False]:
 for dep in ['f-only','both']:
  i=K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'),inventories=[K.inv_symbol(),K.inv_symbol(nid=K.G_SYM,qn='g')])
  if grouped:K.install_pair(i,*K.paired('reachability','from-resolved-calls',K.U1,K.U1,[K.F_SYM,K.G_SYM],tag='1'))
  else:
   K.install_pair(i,*K.paired('reachability','from-resolved-calls',K.U1,K.U1,[K.F_SYM],tag='1'))
   K.install_pair(i,*K.paired('reachability','from-resolved-calls',K.U1,K.U1,[K.G_SYM],tag='3'))
  K.install_pair(i,*K.paired('calls','resolved-callee',K.U1,K.U1,[K.F_SYM],tag='2'))
  if dep=='both':K.install_pair(i,*K.paired('calls','resolved-callee',K.U1,K.U1,[K.G_SYM],tag='4'))
  r=A.evaluate_atom({'op':'none','relation':'reachability','minResolution':'from-resolved-calls','endpoint':'target','filters':[]},K.F_SUBJ,copy.deepcopy(i))
  out[str(grouped)+'/'+dep]={k:r[k] for k in ['value','coverageIds','causes','nativeDeficiencies']}
p=Path(__file__).parent/'probe.json';p.write_text(json.dumps({'standing':'Source35 synthetic atom API only, not closedRun evidence; grouping changes no subject census or dependency evidence.','cases':out},indent=2)+'\n')
for n,r in out.items():print(n,r['value'])
assert out['True/f-only']['value']=='true' and out['False/f-only']['value']=='indeterminate'
assert out['True/both']['value']==out['False/both']['value']=='true'
