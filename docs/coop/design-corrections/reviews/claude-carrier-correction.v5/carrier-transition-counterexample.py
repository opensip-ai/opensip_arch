import importlib.util,json,copy
from pathlib import Path
B=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/security')
s=importlib.util.spec_from_file_location('root_security_transition',B/'security_lifecycle_model_v1.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
fixtures=json.loads((B/'transition-journal-cases.v1.json').read_text())['records']
good=copy.deepcopy(fixtures['intentStoreMigrate']);assert M.admit_transition_intent(good)==[]
same=copy.deepcopy(good);same['toStateSchema']=same['fromStateSchema'];same['toStoreGeneration']=same['fromStoreGeneration']
refused=M.admit_transition_intent(same);assert 'TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE' in refused
newop=copy.deepcopy(same);newop['operation']='carrier-migrate';newref=M.admit_transition_intent(newop);assert newref
report={'standing':'Concrete frozen-owner admission, root review counterexample only','lawfulStoreMigration':{'input':good,'refusals':[]},'carrierOnlyUsingStoreMigrate':{'input':same,'refusals':refused},'inventedOperation':{'input':newop,'refusals':newref},'conclusion':'A carrier-only transition cannot silently reuse the closed logical store-migrate intent. A separate explicit private protocol or reviewed owner successor must define its exact intent, lease set and durable recovery footprint.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'carrierOnlyRefusals':refused,'inventedOperationRefusals':newref}))
