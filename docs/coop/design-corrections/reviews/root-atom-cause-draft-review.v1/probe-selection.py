from pathlib import Path
import importlib.util,json,hashlib
F=Path('/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation')
p=F/'atom_model.v1.py';s=importlib.util.spec_from_file_location('A',p);A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
u='a'*64;n='symbol'; lo='scope2:'+'1'*64;hi='scope2:'+'2'*64
cl='coverage2:'+'1'*64;ch='coverage2:'+'2'*64
sc=lambda:{'relation':'declares','resolution':'syntactic','sourceUniverse':u,'targetUniverse':u,'subjects':[n]}
cov=lambda d,nc:{'key':{'relation':'declares','resolution':'syntactic','sourceUniverse':u,'targetUniverse':u},'entry':{'coverage':'unknown','deficiency':d,'nativeCause':nc}}
i={'scopes':{lo:sc(),hi:sc()},'coverages':{cl:cov('budget-exhausted',None),ch:cov('input-closure-incomplete','lockfile-missing')},'coverageScopes':{ch:lo,cl:hi}}
selected=A._select_dep_coverages('declares','syntactic',u,u,i,{n},'symbol')
fold,refs=A._conservative_entry('declares',selected)
paired,sids,unpaired=A._coverages_for_current_source(i,'declares','syntactic',u,n)
print(json.dumps({'standing':'Synthetic helper-only inputs; NOT native schema/retained-Run admitted. Proves stated selection-order mismatch in same-kind multi-scope branch, not nondeterministic full Run.','sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'selected':[c for c,_ in selected],'ascendingExpected':sorted([cl,ch]),'actualCarrier':[fold['deficiency'],fold['nativeCause']],'outgoingPaired':[c for c,_ in paired],'scopes':sids},indent=2))
assert [c for c,_ in selected]!=sorted([cl,ch])
