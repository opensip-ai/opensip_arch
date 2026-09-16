import ast,importlib.util,json
from pathlib import Path
P=Path('/tmp/opensip-design-corrections/claude-planning-owner-correction.v2/scratch/controls/check_store_instance_lineage.py')
tree=ast.parse(P.read_text());f=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='reconstruct');ns={};exec(compile(ast.Module(body=[f],type_ignores=[]),str(P),'exec'),ns)
B=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/security')
s=importlib.util.spec_from_file_location('s9owner',B/'security_lifecycle_model_v1.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
fixtures=json.loads((B/'transition-journal-cases.v1.json').read_text())['records'];intent=fixtures['intentRepair'];assert not M.admit_transition_intent(intent)
j={**intent,'state':'COMMITTED','intentDigest':M.transition_intent_digest(intent)}
node=ns['reconstruct'](j,{'predecessorStoreRoot':'a'*32,'selectedStoreRoot':'a'*32})
print(json.dumps(node,indent=2))
same=node['predecessor']=={k:node[k] for k in ('storeInstanceId','storeGeneration','stateSchema')}
assert same,'Expected actual supplied reconstruction to form a self predecessor on same-store repair'
invalid=[]
for name in ['core-rollback','store-rollback']:
 i={**fixtures['intentCoreRollback' if name=='core-rollback' else 'intentStoreRollback'],'fromStoreGeneration':5,'fromStateSchema':1,'toStoreGeneration':4,'toStateSchema':1}
 invalid.append({'label':name+' schema retreats in v2 node_writing_property','input':i,'actualOwnerRefusals':M.admit_transition_intent(i)})
assert all(r['actualOwnerRefusals'] for r in invalid)
report={'standing':'Root counterexamples against completed Claude owner v2, not product tests','sameStoreRepair':{'ownerAdmitted':True,'reconstructedNode':node,'selfPredecessor':same},'labelledRollbackControls':invalid}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
