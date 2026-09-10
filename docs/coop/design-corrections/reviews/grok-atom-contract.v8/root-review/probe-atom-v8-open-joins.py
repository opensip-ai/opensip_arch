import importlib.util,json,copy
from pathlib import Path
p=Path('/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation/check-atoms.v1.py')
s=importlib.util.spec_from_file_location('fixtures',p);F=importlib.util.module_from_spec(s);s.loader.exec_module(F);A=F.AM
f,g='ts-symbol:src/a.ts#f','ts-symbol:src/a.ts#g'
atom={'op':'none','relation':'references','minResolution':'resolved-binding','endpoint':'target','filters':[]}
subject={'universe':F.U1,'kind':'symbol','nativeSubjectId':f}
inputs=F.base_inputs(inventories=[F.inv_symbol(),F.inv_symbol(nid=g,qn='g')])
for args in [('references','resolved-binding',F.U1,F.U1,[f],'1'),('references','resolved-binding',F.U1,F.U2,[g],'2')]:
 rel,rung,su,tu,ids,tag=args;F.install_pair(inputs,*F.paired(rel,rung,su,tu,ids,tag=tag))
r=A.evaluate_atom(atom,subject,inputs);print(json.dumps({'case':'one-U-partition-does-not-prove-other-partition-searches-U','observed':r,'expected':'indeterminate','standing':'synthetic admitted-map reproduction only; no complete native graph'}))
inputs=F.base_inputs(inventories=[F.inv_symbol()])
F.install_pair(inputs,*F.paired('references','resolved-binding',F.U1,F.U1,[f],tag='1'))
unavailable=copy.deepcopy(inputs['enumerationPlan']['cells'][0]);unavailable['workspaceRoot']='other';unavailable['required']=False;unavailable['programBindings'][0]['universe']=None;inputs['enumerationPlan']['cells'].append(unavailable)
r=A.evaluate_atom({**atom,'endpoint':'source'},subject,inputs);print(json.dumps({'case':'optional-other-program-unavailable-poisons-outgoing','observed':r,'expected':'true','standing':'synthetic admitted-map reproduction only; independent required execution remains separate'}))
